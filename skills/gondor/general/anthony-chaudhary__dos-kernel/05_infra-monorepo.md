# Playbook 05 — refusals that keep an infra fleet from detonating

> **Archetype:** a platform monorepo — Terraform (`live/`, `terraform/`), k8s
> manifests (`k8s/`, `helm/`), reusable modules (`modules/`), runbooks. Blast
> radius is real: a bad `terraform apply` takes down a cluster.
> **The DOS feature:** the **refusals**. Exclusive lanes, the **self-modify
> guard**, and the operator-gated **`BLOCKED`** verdict. On infra, the value of a
> fleet is mostly in what it *won't* let two agents do at once.
>
> **Workspace:** [`../workspaces/gravel/`](../workspaces/gravel/).

The other playbooks are about admitting safe concurrency. This one is about the
opposite face of the same kernel: **refusing unsafe concurrency.** DOS's most
important syscall is structured refusal — a *legible* "no, and here's exactly
why," not a silent lock. On infra that legibility is the product.

---

## The shape

Almost everything that touches live state is **exclusive**; only pure code
(modules) and docs are concurrent-safe:

```toml
[lanes]
concurrent = ["modules", "docs"]
exclusive  = ["tfstate", "cluster"]      # touch real cloud / a live cluster → run alone

[lanes.trees]
modules = ["modules/**"]
docs    = ["docs/**", "runbooks/**"]
tfstate = ["live/**", "terraform/**"]
cluster = ["k8s/**", "helm/**"]
```

```bash
cd examples/workspaces/gravel
dos doctor --workspace .
#   concurrent lanes    modules, docs
#   exclusive lanes     tfstate, cluster
#   admission predicates disjointness, self-modify
```

> `admission predicates` shows the two clean-install built-ins; a `pip install`ed
> `dos.predicates` plugin (e.g. `examples/dos_ext`'s `budget-guard`) would also
> appear. See [playbook 01](01_onboard-a-repo.md#step-1--point-dos-at-your-repo).

## Refusal 1 — two agents can't both apply Terraform

`tfstate` is exclusive. While one agent holds it (a `terraform apply` in flight),
a second request is refused — there is no auto-pick across an exclusive boundary,
because there is no "equivalent free lane" for live cloud state:

```bash
dos arbitrate --workspace . --lane tfstate --kind global \
  --leases '[{"lane":"tfstate","lane_kind":"global","tree":["live/**"]}]'
```
```text
{"outcome": "refuse", ...,
 "reason": "an exclusive lane is live (lane='tfstate', kind='global', ...);
            it touches the whole portfolio — wait for it to finish."}
```
```text
exit code: 1
```

The second agent gets a *reason*, not a hang. Its loop reads `outcome: "refuse"`
and waits. This is the difference between "two `apply`s raced and one clobbered
the other's state" and "the second one waited its turn."

## Refusal 2 — an agent can't rewrite the kernel adjudicating it

This one is **built-in and always-on**, independent of `gravel`'s lanes: the
**self-modify guard**. A lease whose tree includes the orchestrator's own running
code is refused with the typed `SELF_MODIFY` reason:

```bash
dos arbitrate --workspace . --lane modules --kind cluster \
  --tree src/dos/arbiter.py --leases '[]'
```
```text
{"outcome": "refuse", ...,
 "reason": "lane 'modules' would edit the orchestrator's own running code
            (src/dos/arbiter.py) — refusing to let a live loop rewrite the
            kernel that is adjudicating it (SELF_MODIFY). Pass --force only if
            you are deliberately editing the kernel between loop runs."}
```
```text
exit code: 1
```

Why this matters on a platform team: the fleet that manages your infra often
*includes* the tooling that runs the fleet. The guard stops a live loop from
editing the referee mid-flight — a foot-gun that's invisible until it isn't.
It carries a real reason token you can look up:

```bash
dos man wedge SELF_MODIFY
#   NAME        SELF_MODIFY — ...
#   CATEGORY    ...
#   REFUSAL?    yes — route to /replan
```

> **`--force` is the one override**, and it's an *operator* action, not an
> automation path. Forcing the self-modify refuse is how you *deliberately* edit
> the kernel between runs. A loop should never `--force`; a human at a terminal,
> knowing exactly what they're doing, may.

## Refusal 3 — the typed gate verdicts (work exists, but don't ship it)

When you snapshot a batch on the `modules` lane and gate it, you get a **typed
verdict** — and on infra the non-`LIVE` verdicts are the interesting ones,
because "there's work but it's not safe to dispatch right now" is the normal
state. Each verdict is a distinct exit code so your loop branches on it:

```bash
# A pick that shipped in git but the change-doc never got stamped (false drain):
dos gate --workspace . --picks-json \
  '[{"series":"NET","phase":"NET3","live":false,"drop_reason":"shipped","ship_via":"direct","plan_doc_stamped":false}]'
#   STALE-STAMP  1 pick(s) shipped in git but plan-doc unstamped (NET NET3) — false drain, not an empty backlog
#   exit 4   → don't ship; reconcile the stamp (a /dos-replan stamps it)

# A pick soft-claimed by a sibling run, or blocked on a quota/credential window:
dos gate --workspace . --picks-json \
  '[{"series":"NET","phase":"NET3","live":false,"drop_reason":"soft_claimed","claim_tag":"run-0900Z"}]'
#   BLOCKED  1 pick(s) blocked by a sibling soft-claim or quota (NET NET3) — work exists but is not dispatchable now
#   exit 5   → don't ship; surface to the operator (e.g. a change-freeze window)

# Genuinely nothing to do:
dos gate --workspace . --picks-json '[]'
#   DRAIN  no live picks and no recoverable signal — backlog genuinely drained
#   exit 3   → skip the ship, archive a no-op
```

| Verdict | Exit | On infra it means |
|---|---|---|
| `LIVE` | 0 | dispatchable change — proceed |
| `DRAIN` | 3 | nothing queued — skip |
| `STALE-STAMP` | 4 | shipped but the change-doc lagged — reconcile, don't re-ship |
| `BLOCKED` | 5 | change-freeze / sibling claim / quota — surface, don't force |
| `RACE` | 6 | lost a render race — retry the snapshot once |

A **contract error** (a malformed or missing packet) is exit 2 — never a silent
fall-through to `DRAIN`:

```bash
dos gate --workspace . --picks-json '[{"live":false}]'
#   error: disposition is missing 'phase' (or 'phase_id'): {'live': False}
#   exit 2
```

That distinction is the point of a *typed* gate: a broken producer fails loud
instead of looking like "nothing to do."

## Putting it together — the operator console

Refusals 1–3 all surface through one place: the
[operator-decision queue](06_debug-a-stuck-fleet.md). A `BLOCKED` change, a
`--force`-worthy self-modify, an exclusive-lane contention — they land in
`dos decisions` as rows tagged with who can resolve them (`HUMAN` / `ORACLE` /
`JUDGE`). On a platform team that queue is your change-control board, derived from
kernel state instead of maintained by hand:

```bash
dos decisions            # what needs a human right now
dos decisions --all      # include ORACLE/JUDGE-resolvable rows
```

## Anti-patterns

- ❌ **`--force` in an automated infra loop.** A refuse on `tfstate` is a real
  collision with live state; forcing it is how you get two `apply`s racing. Force
  is a human-at-a-terminal override, full stop.
- ❌ **Reading a `BLOCKED`/`STALE-STAMP` gate as "drained."** They are *not* empty
  backlogs — `BLOCKED` means a change-freeze or sibling claim; `STALE-STAMP` means
  reconcile a lagging doc. The distinct exit codes exist so you don't conflate them.
- ❌ **Modeling live cloud state as a concurrent lane** because two changes "touch
  different files." The constraint isn't the files — it's the shared live state.
  Make it exclusive.
- ❌ **Letting the fleet edit its own tooling.** The self-modify guard is on for a
  reason; don't route around it in automation.

## Recap

```bash
cd examples/workspaces/gravel
dos arbitrate --workspace . --lane tfstate --kind global --leases "$LIVE"   # exclusive → refuse if held
dos arbitrate --workspace . --lane modules --kind cluster --tree src/dos/arbiter.py --leases '[]'  # SELF_MODIFY refuse
dos gate --workspace . --picks-json '<dispositions>'                        # LIVE/DRAIN/STALE-STAMP/BLOCKED/RACE
dos decisions                                                               # the refusals that need a human
```

Next: when a refusal or a stuck agent has you confused, the full troubleshooting
flow + FAQ is [06](06_debug-a-stuck-fleet.md).
