# leet — the goal prompt (drop into a fresh session to bootstrap the repo)

> *A self-contained brief. Paste the block in §0 as a `/goal` (or the first prompt
> of a new session) in an empty directory where the new `leet` repo will live. The
> rest of this file is the reference the goal points at — concept, the falsifiable
> validation target, and the minimal spine that reaches it. Written 2026-06-14 as
> the next-step companion to `docs/products-leet-fleet-harness.md` (the design) and
> issue #158 (the public vision thread). Names no private path; safe to copy.*

---

## 0. The goal prompt (copy this verbatim)

```
GOAL: Bootstrap `leet` — a fleet-first coding harness built verification-first — as a
new standalone repo, and drive it to its FIRST FALSIFIABLE VALIDATION: a $0,
model-free A/B simulation proving the one claim no competitor can make — that a fleet
of agents on one repo, admitted through a pre-write file-tree lease and banked only on
git-evidence, loses ZERO collisions and banks ZERO lies, where a believe-the-agent
control arm loses both.

leet embeds the DOS kernel (`pip install dos-kernel`) as its trust substrate and is one
"conductor" driver of it (it does NOT fork or reinvent the kernel). The loop is a
closed-loop controller with the agent as the plant inside it:
PICK -> DECLARE -> ADMIT -> DISPATCH -> STEER -> BANK -> STOP, every edge a kernel verdict,
the stop condition residual-empty-against-ground-truth (not budget).

DONE means, in order:
1. A new git repo `leet/` exists with: README stating the thesis + honest limits, a
   pyproject depending on `dos-kernel`, a `leet/` package, a `tests/` dir, and CI that
   runs the suite.
2. The minimal spine runs end-to-end on a SIMULATED fleet (deterministic fake "agents",
   no model tokens, no network): the conductor PICKs units, DECLAREs extent to an intent
   ledger, ADMITs via `dos lease-lane` (real WAL write-back), DISPATCHes to fake workers
   in isolated worktrees, STEERs on `dos liveness`/`completion`, and BANKs only on
   `dos verify` + `dos commit-audit`.
3. A validation harness `validate/fleet_ab.py` runs a 2-arm A/B (believe vs adjudicate)
   over a seeded synthetic workload and prints a results table with the honesty
   invariants checked. The adjudicate arm must show prevention=100%, banked_lies=0;
   the believe arm must show surviving silent overwrites > 0 and banked_lies > 0 as the
   fleet grows. A DISJOINT-workload control must tie both arms at zero (the self-falsifier).
4. The whole thing is `$0` and reproducible from one command:
   `python -m validate.fleet_ab --sweep`. Numbers committed to `validate/RESULTS.md`
   with the kernel SHA stamped.

VALIDATION IS THE POINT, not feature breadth. Build the THINNEST spine that makes the
A/B claim falsifiable and either confirms or refutes it. If it refutes, say so plainly —
a refuted claim honestly reported is a success of the method.

Reference: docs/leet-goal-prompt.md (this file's full concept + spine), 
docs/products-leet-fleet-harness.md (the design), docs/333 / docs/98 / docs/197 in the
dos-kernel repo (the conceptual spine). Work in the new `leet/` repo, not in dos-kernel.
Commit when a unit is green; do not push or create the GitHub remote without asking.
```

---

## 1. The concept, expanded (what the agent is building toward)

leet is the **controller**; the agents are the **plant** (docs/333). Every other 2026
harness is an agent loop with a grader bolted onto the seams it happens to expose
(tool-return + end-of-run). That is a fork, not a spectrum: a bolt-on can only read the
agent's own narration, has no notion of declared extent (so it stops on budget), and its
admission seams are all post-effect (so it can only detect collisions, never prevent
them). leet threads three things through from the first type:

1. **Ground truth is a first-class input channel** — git ancestry, the diff footprint,
   the lease WAL, the OS exit code — read directly, never scraped from narration.
   Narration is read but **demoted at the door** to a hint that must clear a non-forgeable
   checkpoint.
2. **The unit of work carries its own completion predicate** — declared extent written to
   a distrusted intent ledger **before step one**, so *residual = declared − verified* is
   computable at every step and the stop condition is residual-empty, not budget.
3. **Admission is a pre-effect gate** — `arbitrate`/`lease` over file-tree disjointness at
   the write chokepoint, where prevention is still possible.

The kernel already ships all of this, pure and vendor-free, over CLI + MCP + `import dos`.
leet is the **conductor** — one driver of that seam (docs/98). It owns the fanout, the
cadence, the isolation backend, and the UX; the kernel owns the truth oracle (`verify`)
and the lock manager (`arbitrate` via `dos lease-lane`). The kernel does not care which
driver runs.

### The loop, concretely

| Step | What leet does | Kernel verdict it calls | Byte-author of the verdict |
|---|---|---|---|
| **PICK** | choose the next fresh unit | `enumerate`/`pickable`/`cooldown`/`pick_priority` | the attempt ledger |
| **DECLARE** | write the unit's extent to `intent.jsonl` *before* work | (intent ledger surface) | recorded pre-game |
| **ADMIT** | lease the tree before any write | `dos lease-lane acquire` (pure `arbitrate` + WAL append) | live leases + tree geometry |
| **DISPATCH** | launch the worker in an isolated workspace | — (isolation driver) | — |
| **STEER** | between steps, read the heading | `liveness` / `productivity` / `completion` / `verify-result` | git/journal delta, env deltas, the `<synthetic>` stamp |
| **BANK** | ship only on git evidence | `dos verify` + `dos commit-audit` | git ancestry + the diff |
| **STOP** | residual empty, or surface a decision | `completion` (CONVERGING vs THRASHING) | git-verified residual |

---

## 2. What validation looks like (the falsifiable target — build toward THIS)

Validation here is not "it runs." It is a **falsifiable A/B**, in the exact lineage the
dos-kernel `benchmark/fleet_horizon/` rig already proves (believe vs adjudicate, with
honesty invariants and a self-falsifier). The claim, stated so it could be wrong:

> **CLAIM.** On a fleet of N agents contending on a shared region, leet's
> adjudicate arm (pre-write lease + git-evidence bank) loses zero collisions
> (prevention = 100%) and banks zero lies, while a believe arm (same agents, no lease,
> bank-on-self-report) accumulates surviving silent overwrites and banked lies that
> **grow monotonically with N**. On a genuinely disjoint workload, BOTH arms tie at zero
> — the gap exists only where contention bites.

### The three things the validation harness must show

1. **The discriminator metric — prevented vs detected.** Count `refused_writes`
   (prevented at contention) vs `detected_collision` (caught after the fact because the
   lease view lagged) and the surviving `silent_overwrite` (a clobber `verify` cannot
   undo). The headline is `prevention_rate`. The believe arm's prevention collapses to 0%
   the moment fleet ≥ 4; the adjudicate arm holds 100%.

2. **The honesty invariants (pin these in tests — they make the result trustworthy).**
   - Same seed → **identical `real_ships`** across both arms (leet gets no better agent;
     the only thing that differs is whether it believes the agent).
   - **`banked_lies == 0` in the adjudicate arm** (git evidence catches the lie
     regardless of how confident the narration was).
   - **`banked_lies > 0` and `silent_overwrites > 0` in the believe arm** at fleet ≥ 4
     (the control demonstrably has the disease).

3. **The self-falsifier (the benchmark proves its own boundary).** Run a *truly disjoint*
   workload (every unit's footprint pairwise-disjoint). The arbiter never refuses, lease
   visibility is irrelevant, and **both arms tie at zero**. If the gap does NOT vanish on
   a disjoint workload, the metric is measuring the wrong thing — fix the metric, not the
   threshold. This is the honest falsifier that separates a real result from a rigged one.

### What a PASS and a REFUTE both look like

- **PASS:** the table shows the monotonic gap on the shared workload and the tie on the
  disjoint one; the invariant tests are green. leet's central claim is now *demonstrated*,
  not asserted — on a simulator, $0, reproducible.
- **REFUTE (also a success of the method):** e.g. the lease write-back races and the
  adjudicate arm *also* loses a collision, or `verify` banks a lie because the fake agent
  forged the non-forgeable rung. Report it plainly with the failing number. A refuted
  claim honestly reported is the whole point of building the harness — it found the hole
  before a user did.

> The model-in-the-loop version (real agents, real tokens, real SWE-bench-style tasks)
> is the *next* validation tier and is explicitly OUT OF SCOPE for the first spine. The
> simulator is the right first target because it isolates the trust property from model
> quality — exactly why dos-kernel's FleetHorizon leads with the $0 simulator arm.

---

## 3. The minimal spine — the thinnest path to that validation

Build in this order. Each step is a green-testable unit; commit when green. Resist
breadth — the goal is the A/B, and everything not on its critical path is a distraction.

### Spine step 1 — the repo skeleton

- `git init leet`; `pyproject.toml` with `dependencies = ["dos-kernel"]`; a `leet/`
  package, a `tests/` dir, a `validate/` dir; a CI workflow running `pytest`.
- README: the one-line thesis, the 7-step loop, and the **honest-limits** section copied
  from the design doc (conformance ≠ correctness; tree-disjointness necessary-not-sufficient;
  PDP/no-PEP; co-resident-verifier trap; witness coverage is a subset). Leading with the
  limits is the leet move — a harness that only stated its thesis would be the self-report
  it exists to refuse.

### Spine step 2 — the `Workspace` and `Worker` seams (fakes first)

- `Workspace` interface: `create(run_id) -> path`, `commit(path, files, subject)`,
  `cleanup()`. One real impl: **git worktree** (cheapest; `git worktree add` per run).
  Container/microVM are later drivers behind the same seam — do NOT build them now.
- `Worker` interface: `run(unit, workspace) -> WorkerResult`. For validation, the only
  impl is a **deterministic `FakeWorker`** seeded from the unit + a seed: it "edits" a
  declared set of files, sometimes (controlled by the workload) collides with another
  unit's files, and sometimes **lies** (claims success while writing nothing / an empty
  commit) — so the believe arm has something to be wrong about.

### Spine step 3 — the conductor loop (the heart)

- `Conductor.run(workload, *, arm)` implementing PICK → DECLARE → ADMIT → DISPATCH →
  STEER → BANK → STOP. Two arms behind one loop body (the FleetHorizon pattern — the only
  thing the arm changes is the trust seam, never the agent):
  - **adjudicate arm:** ADMIT calls `dos lease-lane acquire` and gates on exit code; BANK
    calls `dos verify` + `dos commit-audit` and banks only on SHIPPED + clean audit.
  - **believe arm:** ADMIT is a no-op (or a stale in-process view); BANK trusts the
    worker's `result.claimed_done`.
- Use the kernel from the CLI/MCP boundary (subprocess `dos ...` or `import dos` pure
  calls) — never reimplement a verdict. The run-dir per unit holds `intent.jsonl` + the
  lease WAL (let `dos lease-lane` own the WAL).

### Spine step 4 — the validation harness

- `validate/fleet_ab.py`: a seeded synthetic workload generator with two modes —
  `shared(ratio)` (units contend on a shared file pool) and `disjoint()` (pairwise-disjoint
  footprints, the self-falsifier). Sweep fleet sizes {2,4,8,12}, run both arms, collect
  `{real_ships, banked_lies, refused, detected, silent_overwrites, prevention_rate}`.
- `python -m validate.fleet_ab --sweep` prints the table and writes `validate/RESULTS.md`
  with the kernel SHA stamped (steal the freshness-stamp idea from dos-kernel's runner).
- `tests/test_invariants.py`: pin the three honesty invariants of §2.2. These tests are
  the proof the result is trustworthy, not the demo.

### What is deliberately NOT in the first spine

Real models / tokens · container & microVM isolation drivers · the picker's full
anti-churn substrate (a trivial FIFO pick is fine for the A/B) · `resume`/recovery ·
the supervisor/PID-1 population control · the completion-certificate UX · MCP server ·
multi-host dialects. Each is a real later step; none is on the critical path to the
falsifiable claim. Add them only after the A/B passes or refutes.

---

## 4. Why this sequencing (the discipline)

The one constraint that recurs everywhere in the DOS lineage is **witness coverage**:
build where the witness is deterministic first. The simulator is the maximal-coverage,
zero-cost, fully-deterministic environment — so it is where the trust claim is cleanest to
prove or break. Proving the spine on a simulator, $0, before spending a single model
token, is the same move dos-kernel's FleetHorizon makes and the reason its collision
result is credible. Get the A/B to pass (or refute) there first; everything else composes
off a validated core.

> If at any point the kernel cannot witness what leet needs (a soft goal with no
> git-checkable effect, a pure-text worker with no commits), the correct output is
> `ABSTAIN` routed to a human — never a fabricated reading. A sensor that lies when blind
> is worse than no sensor. Build that honesty in from step 1.
