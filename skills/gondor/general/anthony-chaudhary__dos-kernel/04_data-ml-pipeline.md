# Playbook 04 — a data / ML pipeline and the "is it advancing?" problem

> **Archetype:** an `ingest → train → serve` pipeline. Jobs are long (a training
> run holds a shared GPU box for tens of minutes), and **a long job's logs don't
> tell you whether it's making progress or wedged in a retry loop.**
> **The DOS features:** an **exclusive long-horizon lane** (only one job owns the
> accelerator) plus the **liveness verdict** — the temporal sibling of `verify`:
> *is this run advancing, spinning, or stalled?*
>
> **Workspace:** [`../workspaces/riverflow/`](../workspaces/riverflow/).

`verify` distrusts a *finished* claim ("I shipped P"). A long-running pipeline
needs the in-flight version: an agent that's been "training" for 40 minutes is
either advancing or stuck retrying the same failing step — and from the outside
they look identical. This playbook covers the shipped concurrency story for that
shape, then the temporal verdict that closes the loop on it.

---

## The shape

```toml
[lanes]
concurrent = ["ingest", "serve"]   # disjoint trees → run in parallel
exclusive  = ["train"]             # owns the GPU box → runs alone

[lanes.trees]
ingest = ["ingest/**", "schemas/**"]
serve  = ["serve/**"]
train  = ["train/**", "models/**"]
```

```bash
cd examples/workspaces/riverflow
dos doctor --workspace .
#   concurrent lanes    ingest, serve
#   exclusive lanes     train
```

## Step 1 — concurrency around a long job (shipped)

`ingest` and `serve` touch disjoint trees, so they admit concurrently — you can
backfill data while the inference service is being updated:

```bash
dos arbitrate --workspace . --lane serve --kind cluster \
  --leases '[{"lane":"ingest","lane_kind":"cluster","tree":["ingest/**"]}]'
#   outcome: acquire        exit 0
```

But `train` is **exclusive**: it monopolizes the accelerator, a resource the
file-tree algebra can't see. An exclusive lane is admitted on *liveness alone* —
it runs by itself. While a training job holds it, a second `train` request is
refused:

```bash
dos arbitrate --workspace . --lane train --kind global \
  --leases '[{"lane":"train","lane_kind":"global","tree":["train/**"]}]'
#   outcome: refuse   (an exclusive lane is live; it runs alone)   exit 1
```

That single refusal is what stops two jobs from fighting over one GPU. This is
why you model a *shared resource* as an exclusive lane even when the file trees
wouldn't collide — the lane is standing in for the accelerator.

## Step 2 — verify pipeline phases shipped (shipped)

`riverflow` stamps ships with the bare phase id (`subject_dirs = []`), so a
commit `FEAT7: ship feature store` is recognized with no prefix:

```bash
dos verify --workspace . FEAT FEAT7
#   SHIPPED FEAT FEAT7 <sha> (via grep-subject)      exit 0    (in a real checkout)
```

Same truth syscall as [playbook 03](03_oss-library-release.md) — useful here for
gating "is the feature-store migration actually in before we point training at
it?"

## Step 3 — the temporal verdict: ADVANCING / SPINNING / STALLED

> **Status: incoming (LVN, [`docs/82_liveness-oracle-plan.md`](../../docs/82_liveness-oracle-plan.md)).**
> The liveness *verdict* is the fourth distrust syscall — the temporal completion
> of `verify`. The pure kernel classifier exists; the `dos liveness` CLI verb is
> landing. The shape below is the design contract, so you can build against it.
> Until the verb ships, drive the classifier from
> [code](cookbook-python-api.md) (`dos.liveness.classify`).

Here's the problem it solves. A training agent reports, every few minutes, "still
training, making progress." You can't verify that from its self-report — that's
exactly the kind of narration DOS doesn't believe. Liveness asks **ground truth**
instead:

- **Is the commit count moving?** (commits since the run's start SHA)
- **Is the run's journal emitting events?** (heartbeats / lane-journal writes)
- **How old is the newest sign of life?** (wall-clock since the last heartbeat)

…and classifies the run, never reading the agent's own "I'm fine":

| Verdict | Meaning | Typical action |
|---|---|---|
| **ADVANCING** | ground truth is moving — commits/events since start | let it run |
| **SPINNING** | alive (heartbeating) but **no forward progress** — the retry-loop case | intervene: it's burning the GPU going nowhere |
| **STALLED** | no sign of life within the window | reap it; the run is dead |

The intended CLI (the verdict *is* the exit code, like `gate`):

```bash
# (incoming) — RID is the run-id minted at job start; START_SHA is HEAD when it began
dos liveness --workspace . --run-id "$RID" --start-sha "$START_SHA"
#   ADVANCING  3 commits since start            exit 0
#   SPINNING   heartbeating but 0 commits in 38m   exit 3   ← the stuck-training case
#   STALLED    no heartbeat in 41m                  exit 4
```

`SPINNING` is the one that earns its keep on a pipeline: a job that's *alive but
not progressing* is the failure mode a long training run hides best. Liveness
surfaces it from evidence, so your watchdog (or the
[decisions queue](06_debug-a-stuck-fleet.md)) can act instead of waiting out the
full timeout.

> **Liveness is `loop_decide`'s sibling, but it reads ground truth, not
> self-report.** Same role — "should this keep going?" — but where a naive
> watchdog asks the agent, liveness asks git and the journal. That's the whole
> DOS posture applied to time.

## Step 4 — close the loop on a fleet of long jobs

Combine the three: the arbiter keeps one job per GPU (Step 1), `verify` gates the
phase dependencies (Step 2), and liveness turns "spin up N training sessions and
hope" into a *steerable* system — you can see which runs are advancing, which are
spinning, and reallocate the accelerator accordingly. That's the
["closed-loop control"](../../docs/82_liveness-oracle-plan.md) the distrust
syscalls give a fleet: sensors (`verify`, `liveness`) plus actuators (`arbitrate`,
`refuse`) plus the operator console (`dos decisions`).

## Anti-patterns

- ❌ **Trusting "still making progress" from a long job.** That's the narration
  liveness exists to replace. Ask the commit/journal evidence.
- ❌ **Modeling a shared GPU as a concurrent lane because the file trees don't
  overlap.** The trees aren't the constraint — the accelerator is. Make it
  exclusive so the arbiter serializes it.
- ❌ **Waiting out a full timeout on a wedged run.** `SPINNING` is detectable from
  evidence well before the timeout; surface it and intervene.

## Recap

```bash
cd examples/workspaces/riverflow
dos arbitrate --workspace . --lane serve --kind cluster --leases "$LIVE"   # ingest+serve concurrent
dos arbitrate --workspace . --lane train --kind global --leases "$LIVE"    # train is exclusive → refuse if held
dos verify    --workspace . FEAT FEAT7                                      # phase dependency check
# (incoming) dos liveness --run-id $RID --start-sha $SHA                    # advancing / spinning / stalled
```

Next: the refusal-heavy infra case ([05](05_infra-monorepo.md)); when something
*is* spinning, the full troubleshooting flow is in
[06](06_debug-a-stuck-fleet.md).
