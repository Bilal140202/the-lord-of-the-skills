# Playbook 06 — debug a stuck fleet (troubleshooting + FAQ)

> **Goal:** the cross-cutting reference for when something's off — `verify` says
> `via none` and you expected a ship, an agent's been "working" for an hour, a
> dispatch keeps getting refused. Each entry is a symptom → the one command that
> diagnoses it → the fix.

DOS is built so that *every* refusal and negative is legible — there are no
silent failures to guess at. So debugging is mostly **asking the right syscall
and reading its answer.** This page is the index of those questions.

---

## `verify` says `NOT_SHIPPED ... (via none)` but I know it shipped

`(via none)` means **no rung found evidence** — registry empty *and* git history
has no commit your grammar recognizes as a ship.

**First, rule out the empty-repo case** (the one a brand-new workspace hits): if
you just ran `dos init` and haven't committed anything yet — or you're not in a
git repo at all — there is simply nothing for the oracle to read, and `via none`
is correct. `doctor` says so out loud:

```bash
dos doctor --workspace .
#   verifiability        no commits to read (not a git repo, or empty history)
```

If you see that line, the fix isn't DOS — it's `git init` + an actual
`<PHASE-ID>: …` commit (see the [QUICKSTART](../../docs/QUICKSTART.md) §3). Once
`doctor` reports a real commit count, come back here.

**Otherwise, it's almost always the stamp grammar**, not a missing ship. Diagnose
in two steps:

```bash
# 1. What grammar is active?
dos doctor --workspace .
#   stamp convention    src|docs  [style=grep]      ← requires a "src/"/"docs/" prefix

# 2. Does that grammar match your repo's real ship commits?
dos doctor --workspace . --check
```

If `--check` reports a finding, your declared `[stamp]` doesn't match how you
actually stamp ships. Fix `[stamp].subject_dirs` in `dos.toml`:

- ships look like `AUTH2: ...` (no dir) → `subject_dirs = []`
- ships look like `src/AUTH: AUTH2 ...` → `subject_dirs = ["src", ...]`

Then re-verify. See [playbook 03 Step 2](03_oss-library-release.md) for the
grammar-matters walkthrough. If `--check` is clean and `verify` *still* says
`via none`, the ship genuinely isn't in `HEAD`'s ancestry — check you're on the
right branch (a ship on an un-merged branch is correctly "not shipped").

## The stamp `--check` finding I didn't expect
<a id="the-stamp-check-finding-i-didnt-expect"></a>

You ran `dos doctor --check` and got:

```text
finding: declared [stamp] (subject_dirs=src, docs) recognizes none of this
repo's N recent ship-shaped commit(s) — e.g. '<some commit>'. verify will
resolve `via none` for real ships; reconcile [stamp] ...
```

Two causes:

1. **Your grammar really is wrong** — the common case. Reconcile `subject_dirs`
   to your actual convention (above).
2. **You're running `--check` in a directory that isn't its own git repo** — e.g.
   one of the [example workspace fixtures](../workspaces/), which live *inside*
   the DOS repo. `--check` then walks up to the **parent** repo's history and
   judges your grammar against *those* commits, which of course don't match.
   This is the rail working correctly against the wrong history. Run `--check`
   inside an actual checkout of the repo you're configuring, and it judges the
   right commits.

To see which repo's history `--check` is reading:

```bash
git -C . rev-parse --show-toplevel      # the repo whose commits --check scans
```

## An agent has been "working" for ages — is it actually advancing?

This is the **liveness** question (the temporal sibling of `verify`). Don't trust
the agent's "still making progress" — ask ground truth: is the commit count
moving, is its journal emitting events, how old is the last sign of life?

> **Status:** the liveness *verdict* is incoming (`docs/82`, the `dos liveness`
> verb is landing — see [playbook 04 Step 3](04_data-ml-pipeline.md)). The
> classifier exists in the kernel today (`dos.liveness.classify`); drive it from
> [code](cookbook-python-api.md) until the verb ships.

The verdict you're looking for is **`SPINNING`** — alive (heartbeating) but no
forward progress, i.e. wedged in a retry loop. That's the failure a long run
hides best, and it's detectable from evidence well before the timeout.

**Want the whole fleet at once, not one run? `dos top`.** It is the live-ops
watchdog screen — one row per lane, and a held lane's chip *is* the liveness
verdict (🟢 ADVANCING / 🟡 SPINNING / 🔴 STALLED), so a stuck agent is visible at
a glance without naming a run-id. Read-only; leave it open in a side terminal
during a fleet run:

```bash
dos top                 # live, auto-refreshing (needs the `[tui]` extra: pip install dos-kernel[tui])
dos top --once          # one frame (CI / pipe / no-rich); the plain-text floor
dos top --json          # the machine-readable snapshot
```

It works in a brand-new repo with zero config (best-effort `dos init` on first
run), and with no leases yet it shows the lane roster plus a recent-commits strip
— so it's useful from the first commit. `dos liveness` answers *one* run; `dos
top` is the dashboard over *all* of them.

For one run specifically, the manual version of the same check:

```bash
# how many commits has this run produced since it started?
git log --oneline <start-sha>..HEAD | wc -l      # 0 over a long window = suspicious
```

## A dispatch keeps getting `refuse`d

Read the `reason` — the arbiter always says why. Run the arbitration and look:

```bash
dos arbitrate --workspace . --lane <L> --kind <K> --leases '<LIVE>' --pretty
```

| `reason` mentions… | What it is | Fix |
|---|---|---|
| `exclusive lane is live` | someone holds an exclusive lane (e.g. a deploy) | wait — it runs alone by design |
| `would edit the orchestrator's own running code (SELF_MODIFY)` | the tree includes kernel code | don't include `src/dos/**`; or `--force` if you're deliberately editing the kernel |
| overlap / `free_clusters: []` | a real file-tree collision, no free alternative | wait, or narrow the tree so it's disjoint |
| `free_clusters: ["x", "y"]` | requested lane busy, but others are free | take one of those instead |

The rule: **a refuse is information, not an error to route around.** `--force` is
an operator override for deliberate kernel edits — never an automation default.
Forcing past a real collision is how you get the silent overwrites DOS exists to
prevent.

## What do all these reason codes mean?

The refusal vocabulary is self-documenting. List it, then drill in:

```bash
dos man wedge                       # every reason + its category
```
```text
LANE_DRAINED                               TRUE_DRAIN
LANE_BLOCKED_ON_SOAK_GATED_PHASES          OPERATOR_GATE
LANE_LEASE_HELD_BY_LIVE_DISPATCH_LOOP      OPERATOR_GATE
LANE_ALL_INFLIGHT_OR_DEFERRED              STALE_CLAIM
SELF_MODIFY                                MISROUTE
...
```
```bash
dos man wedge SELF_MODIFY            # a full man page for one reason
dos man lane                        # the same, for your lanes
```

The categories tell you *who resolves it*: `TRUE_DRAIN` (nothing to do),
`OPERATOR_GATE` (needs a human decision), `STALE_CLAIM` (a claim that should be
reaped), `MISROUTE` (a routing bug).

## What's waiting on me? — the decisions queue

The refusals and gates that need a human surface in one place:

```bash
dos decisions                       # the HUMAN-resolvable queue ("what needs me")
dos decisions --all                 # include ORACLE/JUDGE-resolvable rows too
dos decisions show 1                # full detail on decision #1
```

A clean queue:

```text
# operator decisions
  (none pending)
```

Each row is tagged with its **resolver kind** — `HUMAN` (you decide), `ORACLE`
(deterministic — the kernel can rule), `JUDGE` (an LLM adjudicator can rule). The
queue is a *projection* over kernel state, not a hand-maintained list, so it can't
drift from reality.

`dos decisions` answers *what needs me* (the actionable inbox); **`dos top`**
(above) answers *what's running now* (the live dashboard). They are sibling
read-only projections over the same kernel state — the queue is the to-do list,
`dos top` is the situation screen.

## `gate` returned exit 2 / "missing 'phase'"

Exit 2 is a **contract error** — the packet (or `--picks-json`) was malformed or
missing, *not* a verdict. A typed gate fails loud here instead of pretending the
backlog is drained:

```text
error: disposition is missing 'phase' (or 'phase_id'): {'live': False}
```

Fix the producer: every disposition needs a `phase` (or `phase_id`). The gate's
distinct codes — `LIVE`=0, `DRAIN`=3, `STALE-STAMP`=4, `BLOCKED`=5, `RACE`=6,
contract-error=2 — exist precisely so a broken producer never looks like "nothing
to do." See [playbook 05 Refusal 3](05_infra-monorepo.md).

## `doctor` printed a `DISPATCH_STATE_PATH` / env-override warning

You have a stray `DISPATCH_STATE_PATH` or `JOB_FANOUT_STATE_PATH` in your shell.
Under the `.dos/` layout that var makes `verify`/`judge` read *that* file instead
of the workspace's `.dos/` state — a silent footgun, so `doctor` surfaces it
loudly. Unset it unless you set it on purpose:

```bash
unset DISPATCH_STATE_PATH JOB_FANOUT_STATE_PATH
```

## A `.dos/` directory appeared in my repo — what is it?

DOS's per-project state home: run records, leases, the lane journal. It's created
on the **first persisting command** (a `lease`, a captured `--force`) — never by a
read-only `verify`/`doctor`/`man`. It ships a self-ignoring `.gitignore`, so it
won't pollute your commits, and it's safe to delete (`dos reindex` rebuilds the
central view from what survives). Read-only syscalls in a stranger's repo write
nothing.

---

## FAQ

**Q. Do I need plan documents / the dispatch workflow to use DOS?**
No. `verify` works against a plain git repo with no plan and no registry — it
answers from history alone (`source="none"` when there's no evidence). The lanes,
the dispatch skills, the decisions queue are all opt-in. Start with `verify`.

**Q. Does `verify` check that my code is correct / tested?**
No — and deliberately. `verify` distrusts *claims about state* ("it shipped"), not
*judgment* ("it's correct"). Correctness is your tests' job. DOS removes the
bookkeeping lie so humans spend attention on the part that needs judgment. (See
the [taxonomy of refusal](../../docs/182_the-kernel-is-a-taxonomy-of-refusal.md).)

**Q. Why does an overlapping lane sometimes `acquire` (reassigned) and sometimes
`refuse`?**
If the requested lane is busy but *other* concurrent lanes are free, the arbiter
auto-picks a free one (`acquire`, with a reason naming the reassignment). If there
is no free alternative, it `refuse`s. Read the `reason`/`free_clusters` to tell
which happened. ([Playbook 02 Step 2](02_polyglot-web-service.md).)

**Q. When is `--force` legitimate?**
When *you, an operator at a terminal*, are deliberately doing the thing the
refusal guards — e.g. editing the kernel between loop runs (the `SELF_MODIFY`
case). Never inside an automated loop. `--force` is the single escape hatch and it
records an attributable HUMAN override.

**Q. What's the default stamp grammar, and which way should I move it?**
With no `[stamp]` table the grammar is **generic** (`any/no dir prefix`) — it
recognizes a bare `AUTH2: ...` / `AUTH: AUTH2 ...` ship in any commit subject, so
`verify` works out of the box on a repo it's never seen (`dos init` scaffolds this
generic default). The direction you move it is *tighter*: declaring
`subject_dirs = ["src", ...]` narrows recognition to ships scoped under those
dirs. That's the safe direction to move toward, because the dangerous error is a
*false* "shipped" — a too-strict grammar fails visibly (`via none`), while a
too-loose one would silently mark unshipped work done. The generic default is
already the most permissive recognizer, so on your own repo you only ever narrow
it. ([HACKING.md](../../docs/HACKING.md).)

**Q. The `dos doctor --json` `admission_predicates` lists `budget-guard` — where
did that come from?**
That's the example plugin from [`examples/dos_ext/`](../dos_ext/). It only appears
if `dos_ext` is pip-installed in your environment; the always-on built-ins are
`disjointness` and `self-modify`. A clean install shows just those two.

**Q. How do I add my own block reason / renderer / safety predicate?**
That's *extending* the kernel, covered in
[`docs/HACKING.md`](../../docs/HACKING.md) and the
[`examples/dos_ext/`](../dos_ext/) skeleton — data in `dos.toml`, behavior via
`entry_points`. These playbooks are the *usage* layer; HACKING is the *extension*
layer.

**Q. Can an agent call DOS directly instead of shelling out?**
Yes — the [MCP server](../../src/dos_mcp/README.md) exposes `verify`/`arbitrate`/
the refusal vocabulary/`doctor` as MCP tools, so Claude Desktop / Cursor / Cline /
an Agent-SDK app can call the referee with zero Python coupling. Wiring snippet in
[`cookbook-ci-integration.md`](cookbook-ci-integration.md).

---

### The diagnostic cheat sheet

```bash
dos doctor --workspace .            # what's active? (lanes, stamp, predicates, env warnings)
dos doctor --workspace . --check    # does my stamp grammar match real ships?
dos verify --workspace . P PH       # did it ship? (via grep-subject = yes-with-receipt, via none = no evidence)
dos arbitrate ... --pretty          # why was a dispatch refused? (read .reason / .free_clusters)
dos man wedge [REASON]              # what does this refusal code mean?
dos decisions [--all]               # what's waiting on a human?
```
