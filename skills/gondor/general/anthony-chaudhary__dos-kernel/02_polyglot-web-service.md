# Playbook 02 — a fleet on a polyglot web service

> **Archetype:** a SaaS storefront monorepo — `src/api/` (backend),
> `web/` (frontend), `src/worker/` (jobs), `deploy/` + `terraform/` (infra).
> **The DOS feature:** concurrent **disjoint lanes**. You want three agents
> editing the API, the frontend, and the worker *in parallel* — but never two
> agents in the same files, and never anyone in infra while a deploy is live.
>
> **Workspace:** [`../workspaces/acme-store/`](../workspaces/acme-store/) — `cd`
> there to run every command below for real.

This is the canonical "why not just run N agents?" answer. Plain parallelism on
a shared tree gives you silent overwrites and merge-conflict detonations. DOS
turns "spin up N sessions" into a *steerable* system: the arbiter decides who may
touch what, so the fleet is concurrent where it's safe and serialized where it
isn't.

---

## The shape

`acme-store/dos.toml` declares the lane taxonomy:

```toml
[lanes]
concurrent = ["api", "web", "worker"]   # parallel iff their trees are disjoint
exclusive  = ["infra"]                   # runs alone
autopick   = ["api", "web", "worker"]    # walk order for a bare "any free lane"

[lanes.trees]
api    = ["src/api/**", "src/shared/**"]
web    = ["web/**"]
worker = ["src/worker/**"]
infra  = ["deploy/**", "terraform/**", ".github/**"]
```

Confirm DOS reads it:

```bash
cd examples/workspaces/acme-store
dos doctor --workspace .
```
```text
concurrent lanes    api, web, worker
exclusive lanes     infra
autopick ladder     api, web, worker
admission predicates disjointness, self-modify
```

> `admission predicates` lists the two always-on built-ins on a clean install;
> a `pip install`ed `dos.predicates` plugin (e.g. `examples/dos_ext`'s
> `budget-guard`) would also appear. See [playbook 01](01_onboard-a-repo.md#step-1--point-dos-at-your-repo).

## Step 1 — the parallel case: two agents, two disjoint lanes

Agent A is working the API. It holds a lease:
`{lane: api, lane_kind: cluster, tree: ["src/api/**"]}`.

Agent B wants the frontend. Before it starts, it asks the arbiter:

```bash
dos arbitrate --workspace . --lane web --kind cluster \
  --leases '[{"lane":"api","lane_kind":"cluster","tree":["src/api/**"]}]'
```

The arbiter runs the **tree-disjointness algebra**: `web/**` shares no prefix
with `src/api/**`, so they cannot collide. Verdict:

```json
{"outcome": "acquire", "lane": "web", "lane_kind": "cluster",
 "tree": ["web/**"], "auto_picked": false, "free_clusters": [],
 "reason": "cluster lane 'web' free — admitted.", "pick_count": null}
```
```text
exit code: 0
```

`outcome: "acquire"` → Agent B may start. **The exit code mirrors the outcome
(0 = acquire, 1 = refuse)**, so the launching script just branches on `$?`.

Run it for a third agent on `worker` against *both* live leases and you get
`acquire` again — three disjoint lanes, three agents, zero coordination meetings.

## Step 2 — the collision case: two agents want the same lane

Now Agent B asks for `api` while Agent A already holds it:

```bash
dos arbitrate --workspace . --lane api --kind cluster \
  --leases '[{"lane":"api","lane_kind":"cluster","tree":["src/api/**"]}]'
```

The arbiter won't put two agents in `src/api/**`. But `acme-store` has *other*
free concurrent lanes, so instead of a dead stop it **auto-picks** one:

```json
{"outcome": "acquire", "lane": "web", "auto_picked": true,
 "reason": "auto-picked free cluster lane 'web' (requested 'api' was busy)."}
```

The requested lane was busy, so the arbiter reassigned Agent B to a free lane
(`web`) rather than colliding. If you *don't* want reassignment — you specifically
need `api` and nothing else — read the `reason`: it tells you `api` was busy, and
your loop can choose to wait rather than take the substitute.

> **When there is no free lane**, the verdict flips to `outcome: "refuse"`
> (exit 1) with `free_clusters: []`. A refuse means a *real* collision with no
> safe alternative — the loop should wait or stop, **not** `--force`. `--force`
> is an operator override for deliberate edits, never an automation default.

## Step 3 — the exclusive case: nobody edits infra mid-deploy

The `infra` lane is **exclusive** — it touches `deploy/`, `terraform/`, and CI,
whose blast radius is the whole system. While an infra change is live, any other
request for it is refused outright (no auto-pick across an exclusive boundary):

```bash
dos arbitrate --workspace . --lane infra --kind global \
  --leases '[{"lane":"infra","lane_kind":"global","tree":["terraform/**"]}]'
#   outcome: refuse   (an exclusive lane is live; it runs alone)   exit 1
```

This is the rule that stops two agents from racing a `terraform apply`.

## Step 4 — plan and ship a batch on a lane (the dispatch screenplay)

Steps 1–3 are the raw `arbitrate` syscall. The shipped **`/dos-dispatch`** skill
(it comes in the wheel — see [HACKING.md Axis 5](../../docs/HACKING.md)) chains it
into a full cycle: **discover → take a lane → snapshot the work → gate → ship →
archive.** The skeleton, all driven by `dos` verbs:

```bash
# 0. discover the layout (never hardcode lane names or paths)
dos doctor --workspace . --json        # read .lanes and .paths.runs

# 1. take the lane lease (Step 1 above) — proceed only on `acquire`
dos arbitrate --workspace . --lane web --kind cluster --leases "$LIVE"

# 2. snapshot the portfolio into a packet (the /dos-next-up skill)
/dos-next-up --scope web

# 3. gate the empty case BEFORE launching a no-op ship:
dos gate --workspace . <packet>.dispositions-<tag>.json
```

The gate returns a **typed verdict, and the verdict is the exit code**:

| Verdict | Exit | Meaning | What the loop does |
|---|---|---|---|
| `LIVE` | 0 | there is dispatchable work | ship it |
| `DRAIN` | 3 | empty backlog | skip the ship, archive a no-op |
| `STALE-STAMP` | 4 | shipped-but-unstamped drift | skip, surface for reconciliation |
| `BLOCKED` | 5 | picks gated (soak/operator) | skip, surface |
| `RACE` | 6 | lost a render race | retry the snapshot once |

You can see the two ends without a real packet using inline picks:

```bash
dos gate --workspace . --picks-json '[{"series":"CART","phase":"CART3","live":true}]'
#   LIVE  1 live pick(s) — packet has dispatchable work        exit 0

dos gate --workspace . --picks-json '[{"series":"CART","phase":"CART3","live":false,"drop_reason":"already shipped"}]'
#   DRAIN  no live picks and no recoverable signal — backlog genuinely drained   exit 3
```

`LIVE` → Step 4 launches the per-pick prompts the snapshot rendered. Anything
else → the loop skips the ship and records why. **You never launch a dispatch on
a 0-pick packet** — that's the whole reason the gate exists.

## Step 5 — what the fleet looks like running

Put Steps 1–4 in a loop per agent and you have the picture from
[the FleetHorizon benchmark](../../benchmark/fleet_horizon/README.md): the
arbiter is the throttle. Disjoint work runs wide; overlapping work serializes on
the lease; the exclusive lane is a global barrier. The dividend is measurable —
the benchmark shows the human-review fraction dropping from 100% (every agent's
claim hand-checked) toward ~22% as the kernel absorbs the verification the
operator would otherwise do by hand.

## Anti-patterns (each is a real failure this prevents)

- ❌ **`--force`-ing past a refuse in automation.** A refuse with empty
  `free_clusters` is a genuine collision. Forcing it puts two agents in the same
  files — exactly the silent-overwrite failure DOS exists to stop. Wait or pick a
  free lane from `free_clusters`.
- ❌ **Hardcoding lane names or run paths in your launcher.** Read them from
  `dos doctor --json`. The taxonomy is *data*; a launcher that bakes in `api`/`web`
  breaks the moment the repo's lanes change.
- ❌ **Launching a ship on an un-gated packet.** Gate first. `DRAIN`/`STALE-STAMP`
  mean "don't ship" — a launcher that skips the gate burns agent-launches on no-op
  packets.
- ❌ **Treating two agents on disjoint trees as a conflict.** They're not — that's
  the *point*. Let the arbiter admit them concurrently; don't add a coarse
  repo-wide lock on top.

## Recap

```bash
cd examples/workspaces/acme-store
dos doctor --workspace . --json                                  # discover lanes + paths
dos arbitrate --workspace . --lane web --kind cluster --leases "$LIVE"   # may I run here?
dos gate --workspace . <packet>                                  # is there work to ship?
#   acquire + LIVE → ship;  refuse → wait/pick free lane;  DRAIN → skip
```

Next: the temporal question — *is a running agent actually advancing?* — is in
[playbook 04](04_data-ml-pipeline.md). The refusal-heavy infra case is in
[playbook 05](05_infra-monorepo.md).
