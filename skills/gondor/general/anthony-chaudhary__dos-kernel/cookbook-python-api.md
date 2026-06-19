# Cookbook — driving DOS from Python

> For when you're **embedding** the kernel in your own tool (an orchestrator, a
> bot, a CI script) rather than shelling out to the `dos` CLI. The syscalls are
> plain functions; the CLI is a thin shell over them. Everything here is the same
> mechanism the CLI uses.

Every recipe is self-contained and was run against the shipped package. Import
paths are stable public surface (`dos.oracle`, `dos.arbiter`, `dos.config`,
`dos.reasons`, `dos.stamp`).

> **The one rule for library callers:** pass your config **explicitly**
> (`oracle.is_shipped(..., cfg=my_cfg)`, `arbiter.arbitrate(..., config=my_cfg)`).
> An explicit config wins over everything — it's the right call for a long-lived
> process serving multiple workspaces. Don't rely on the process-global
> `set_active()` in a server; build a config and pass it.

---

## Recipe 1 — "did this phase ship?" from code

The truth syscall, as a function. Returns a `ShipVerdict` with `.shipped`,
`.source`, `.sha`:

```python
import dos
from dos import oracle

cfg = dos.default_config("/path/to/repo")     # generic config rooted at the repo
verdict = oracle.is_shipped("AUTH", "AUTH2", cfg=cfg)

print(verdict.shipped)   # True / False
print(verdict.source)    # "registry" | "grep" | "none"  — which rung answered
print(verdict.sha)       # the commit that proves it (when shipped)
print(verdict.to_dict()) # {"plan": "AUTH", "phase": "AUTH2", "shipped": ..., "source": ...}
```

`source="none"` means *no evidence at all* — not a reported failure. The function
is pure over its inputs: registry first (if you pass `state=`), then the git-log
grep rung, then ancestry-checked. No plan document required.

## Recipe 2 — build a config for your repo's conventions

Three ways to get a `SubstrateConfig`, in increasing specificity:

```python
import dos
from dos import config

# (a) the generic default, rooted at a workspace
cfg = dos.default_config("/path/to/repo")

# (b) load a repo's dos.toml ([lanes]/[paths]/[stamp]/[reasons]) — the same
#     readback the CLI does. This is usually what you want.
cfg = config.load_workspace_config("/path/to/repo")

# (c) the reference job taxonomy (rarely needed outside the origin repo)
cfg = config.load_workspace_config("/path/to/repo", job=True)
```

`load_workspace_config` is the honest one-call equivalent of what `dos doctor`
sees: it reads the workspace's `dos.toml` and folds the four data tables onto the
base. A workspace with no `dos.toml` degrades to the generic default.

To override a field in code (e.g. inject a lane taxonomy without a TOML file),
`dataclasses.replace` it — `SubstrateConfig` is a frozen dataclass with fields
`lanes`, `paths`, `reasons`, `stamp`, `plan_meta_schema`:

```python
import dataclasses
from dos import config

lanes = config.LaneTaxonomy(
    concurrent=("api", "web"),
    exclusive=("infra",),
    autopick=("api", "web"),
    trees={"api": ("src/api/**",), "web": ("web/**",), "infra": ("deploy/**",)},
)
cfg = dataclasses.replace(dos.default_config("."), lanes=lanes)
```

## Recipe 3 — "may this loop run on lane L?"

The admission kernel is pure: state in, decision out, no I/O. Perfect for
embedding in a scheduler.

```python
from dos import arbiter

decision = arbiter.arbitrate(
    requested_lane="web",
    requested_kind="cluster",
    requested_tree=["web/**"],
    live_leases=[{"lane": "api", "lane_kind": "cluster", "tree": ["src/api/**"]}],
    config=cfg,
)

print(decision.outcome)        # "acquire" | "refuse"
print(decision.lane)           # the lane to run on (may differ — auto-pick)
print(decision.reason)         # human-readable why
print(decision.free_clusters)  # alternatives if refused
print(decision.to_dict())
```

Disjoint trees → `acquire`. Overlapping with a free alternative → `acquire` on
the reassigned lane. Overlapping with no alternative → `refuse`. The built-in
safety predicates (`disjointness`, `self-modify`) run by default; you don't have
to wire them.

> **Pure means testable.** Because `arbitrate` takes the live leases as data and
> returns a decision, you can unit-test your concurrency policy without spawning
> a single agent — assert on `decision.outcome` for hand-built lease lists.

## Recipe 4 — classify a batch into a typed gate verdict

```python
from dos import gate_classify

result = gate_classify.classify_packet([
    {"series": "AUTH", "phase": "AUTH2", "live": True},
    {"series": "AUTH", "phase": "AUTH1", "live": False, "drop_reason": "shipped",
     "ship_via": "direct", "plan_doc_stamped": False},
])

print(result.verdict.value)   # "LIVE" | "DRAIN" | "STALE-STAMP" | "BLOCKED" | "RACE"
print(result.reason)
for d in result.evidence:
    print(d.series, d.phase, d.live)
```

The disposition fields the classifier reads: `live`, `drop_reason`, `ship_via`,
`plan_doc_stamped`, `claim_tag`. Decision order is most-specific-first (any
`live` → `LIVE`; else shipped-but-unstamped → `STALE-STAMP`; else soft-claimed/
quota → `BLOCKED`; else `DRAIN`). A dict with no `phase` raises
`MalformedDisposition` — catch it; don't let it read as a drain.

## Recipe 5 — add a block reason in code (the registry is data)

The refusal vocabulary is a `ReasonRegistry` on the config — immutable, extended
by value. This is the code form of a `[reasons]` table in `dos.toml`:

```python
import dataclasses, dos
from dos.reasons import BASE_REASONS, ReasonSpec

reasons = BASE_REASONS.extend([
    ReasonSpec(token="LANE_PARKED_FOR_BUDGET", category="OPERATOR_GATE",
               refusal=True, summary="lane parked: monthly token budget hit",
               fix="raise the budget cap, or /replan"),
])
cfg = dataclasses.replace(dos.default_config("."), reasons=reasons)

# now the reason is emittable / verifiable / refusable through the same calls a
# built-in uses:
import dos.wedge_reason as wr
print(wr.is_known_reason("LANE_PARKED_FOR_BUDGET"))   # True
print(wr.category_for("LANE_PARKED_FOR_BUDGET"))      # NoPickCategory.OPERATOR_GATE
print(wr.is_refusal("LANE_PARKED_FOR_BUDGET"))        # True
```

`extend()` returns a **new** registry (the original is frozen) — a process's
active reason set is a value on the config, never a global a plugin mutates.
`category` must be one of `TRUE_DRAIN`, `OPERATOR_GATE`, `STALE_CLAIM`,
`MISROUTE`, `UNCLASSIFIED` (the `ReasonSpec` constructor enforces it).

## Recipe 6 — declare a ship grammar in code

The `[stamp]` table, as a value. Generic (no dir prefix) vs dir-scoped:

```python
import dataclasses, dos
from dos.stamp import StampConvention, GENERIC_STAMP_CONVENTION

# generic: a bare "AUTH2: ..." counts
cfg = dataclasses.replace(dos.default_config("."), stamp=GENERIC_STAMP_CONVENTION)

# dir-scoped: ships must be "src/AUTH: AUTH2 ..." or "lib/..."
conv = StampConvention(subject_dirs=("src", "lib"), style="grep")
cfg = dataclasses.replace(dos.default_config("."), stamp=conv)

verdict = oracle.is_shipped("AUTH", "AUTH2", cfg=cfg)   # uses the declared grammar
```

You can also load one from a `dos.toml`'s `[stamp]` table directly:

```python
from dos import stamp
conv = stamp.load_from_toml("/path/to/repo/dos.toml")
```

## Recipe 7 — a minimal embedded gate

Putting it together — a function your tool can call to decide whether to dispatch:

```python
import dataclasses, dos
from dos import config, oracle, arbiter

def may_dispatch(repo, series, phase, lane, live_leases):
    """Return (ok, why). Embeds verify + arbitrate."""
    cfg = config.load_workspace_config(repo)

    # 1. don't re-ship something already shipped
    v = oracle.is_shipped(series, phase, cfg=cfg)
    if v.shipped:
        return False, f"{series} {phase} already shipped ({v.sha}, via {v.source})"

    # 2. don't collide with a live lane
    d = arbiter.arbitrate(
        requested_lane=lane, requested_kind="cluster",
        requested_tree=list(cfg.lanes.tree_for(lane)),
        live_leases=live_leases, config=cfg,
    )
    if d.outcome != "acquire":
        return False, f"lane refused: {d.reason}"

    return True, f"clear to run on lane {d.lane}"
```

That's `verify` + `arbitrate` composed — the two questions every dispatch should
ask, as a pure function with no global state.

## Recipe 8 — make verify a *structural* property (`dos.verified`)

Every recipe above is opt-in at the call site — someone has to remember to call
`is_shipped`. `dos.verified` flips that: decorate the code path that must only
run against verified work, and forgetting is no longer possible. The gate
adjudicates on **every call** (not at decoration time), raising a typed
`NotShippedError` that carries the full verdict:

```python
from dos import verified, NotShippedError

# decorator: the body runs only if (AUTH, AUTH2) verifiably shipped
@verified("AUTH", "AUTH2", workspace="/path/to/repo")
def publish_release_notes():
    ...

# context manager: same gate, and you get the verdict (which rung answered)
with verified("AUTH", "AUTH1", cfg=my_cfg) as verdict:
    print(verdict.source)   # "registry" | "grep-artifact" | "grep-subject"

try:
    publish_release_notes()
except NotShippedError as e:
    print(e.verdict.to_dict())  # the refusing verdict, structured
```

Config resolution follows the library rule: explicit `cfg=` wins, then
`workspace=` (that repo's `dos.toml`, the same readback the CLI does), then the
process-active config. Because the check runs at call time, a gate built before
its phase ships opens the moment the evidence lands in git — and never before.
The raise happens in *your* process: the kernel stays advisory; your code is
what refuses to run.

---

## Notes on the public surface

- **Stable, public:** `dos.default_config`, `dos.job_config`, `dos.set_active`,
  `dos.active`, `dos.SubstrateConfig`, and the syscall modules `dos.oracle`,
  `dos.arbiter`, `dos.gate_classify`, `dos.wedge_reason`, `dos.picker_oracle`,
  plus the seam-data modules `dos.reasons`, `dos.stamp`, `dos.config`.
- **Pass `cfg=`/`config=` explicitly** in any long-lived process. The
  process-global `set_active()` is a convenience for scripts and the CLI, not for
  a server fielding concurrent workspaces.
- The same recipes are available **over MCP** (no Python at all) — see
  [`cookbook-ci-integration.md`](cookbook-ci-integration.md) and
  [`src/dos_mcp/README.md`](../../src/dos_mcp/README.md).
