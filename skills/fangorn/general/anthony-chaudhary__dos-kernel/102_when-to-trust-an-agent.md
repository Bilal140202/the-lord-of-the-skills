# When to trust an agent — the trust-asymmetry the kernel is actually built on

> **"The kernel is the part that doesn't believe the agents" is a slogan, and
> taken literally it is false: a kernel that trusts *nothing* an agent says cannot
> admit a lane, schedule a pick, or read a `--scope`. The honest law is narrower
> and more useful — *the kernel trusts structure, never content; it trusts
> commitments made before the temptation to lie existed, never claims made after;
> and it trusts only where a wrong "yes" is cheap to detect and cheap to undo.*
> This note states that law, derives it from where the kernel already obeys it (and
> the one place it doesn't), and uses it to reframe DOS's value as "better than the
> next-best alternative on a named problem," not "an unclaimed quadrant."**

This is a theory note in the family of [`79`](79_primitives-not-features.md) (the
syscalls are small), [`82`](182_the-kernel-is-a-taxonomy-of-refusal.md) (every
syscall is a *no*), [`84`](183_how-much-does-this-lean-on-git.md) (git is necessary,
not sufficient), and [`89`](89_the-lane-is-a-region-lock.md) (a lane is a
region-lock). Those notes each defend one mechanism. This one steps back and asks
the question *underneath* all of them — **when is it reasonable to trust an agent
at all?** — because the slogan answers "never," the code answers "sometimes," and
the gap between those two answers is where the next design decisions live.

It carries no litmus and ships no mechanism. It is the conceptual frame that
[`90_open-research-areas.md`](90_open-research-areas.md) needs in order to rank its
own open questions, and it is the honest counterweight to the
[adversarial audit](#7-see-also) that found the kernel violating its own founding
slogan in one specific, fixable place.

---

## 1. The slogan is false, and admitting that is the whole point

Strip the kernel to what it actually does on a single `dos arbitrate` call and
count the agent-supplied inputs it *believes*:

- It believes the agent **asked** for a lane (the request is real, not forged).
- It believes the **`--scope` / tree** the agent declared is the region it intends
  to touch.
- It believes the **run-id** the agent presents decodes to a real start time.
- It believes the **commit subject** the agent wrote, far enough to grep it.

A kernel that believed *none* of these could not function. So "never believe the
agents" is not a description of the code — it is a description of a *posture*, and
the posture needs a precise statement or it drifts into either over-claim (we
check everything — we don't) or incoherence (we trust nothing — we can't).

The precise statement has three clauses, and the rest of this note is their
derivation and their consequences:

> **The trust law.**
> 1. **Trust structure, never content.** Believe that a request is well-formed;
>    never believe what it claims about the world.
> 2. **Trust commitments, never reports.** Believe a statement an agent made
>    *before* it could know how to game the check; never believe a statement made
>    *after* the work, when "done" is the rewarded answer.
> 3. **Trust only where a wrong "yes" is cheap.** Believe a claim whose
>    mis-trust is *detectable* (an independent check exists) and *reversible* (the
>    cost of acting on a wrong trust is bounded). Where mis-trust is silent and
>    irreversible, do not trust — restructure, refuse, or route to a human.

Each clause is a thing the kernel *already does somewhere* — and stating it as a
law turns scattered good instincts into a test you can apply to the next feature.

---

## 2. Clause 1 — trust structure, never content (the Linux honesty thing)

The Unix/Linux kernel is the canonical "doesn't believe userland" system, and it
is worth being exact about *what* it disbelieves, because the precision is the
lesson. A syscall crosses the trust boundary carrying arguments. The kernel:

- **Trusts the *form*.** `write(fd, buf, n)` is a well-typed request; the kernel
  believes you asked to write. The calling convention, the syscall number, the
  register layout — all trusted, because they are *structure*, and structure is
  checkable at the boundary by construction (a malformed syscall doesn't parse).
- **Distrusts every *claim about the world* the arguments encode.** `buf` is a
  userspace pointer the process *claims* is readable; the kernel **never
  dereferences it on faith** — it validates the pointer is in the process's
  address space (`copy_from_user`), because a claim about memory the process makes
  is exactly the thing a hostile or buggy process gets wrong. `fd` is checked
  against the file table. `n` is bounds-checked.

The kernel trusts that you *spoke*; it does not trust what you *said about the
world outside the conversation*. That is clause 1, and DOS obeys it precisely:

| DOS believes (structure) | DOS does NOT believe (content) |
|---|---|
| the `verify(plan, phase)` request is well-formed | that the phase **shipped** — it reads git ancestry instead ([`84`](183_how-much-does-this-lean-on-git.md)) |
| the `refuse(reason)` token is in the closed vocabulary | that the reason is the *true* cause — the vocabulary just makes the claim checkable ([`82`](182_the-kernel-is-a-taxonomy-of-refusal.md)) |
| the run-id is a syntactically valid CID | nothing about what the run *did* — that needs the journal |
| the request *names* a lane and a tree | **← here is the crack; see §5** |

The closed reason vocabulary is the sharpest instance: a *free-text* reason would
be content the kernel would have to interpret; a *closed enum* is structure — the
kernel believes only "this token is one of eight," which is checkable, and refuses
to believe anything about why. **The whole "closed-enums-as-data" design
([`HACKING.md`](HACKING.md)) is clause 1 mechanized:** force every agent claim into
a *structural* shape the kernel can validate at the boundary, so it never has to
believe *content*.

---

## 3. Clause 2 — trust commitments, never reports (the plan is the predicate)

This is the deepest clause and the one the kernel under-exploits today. It answers
the question the operator actually posed: *if an agent generates a plan, then does
the work as a blackbox, and the work is checked against the plan — is that
trustworthy?* The answer is **yes, and the reason is a real asymmetry, not a vibe.**

### 3.1 The asymmetry: a plan is a pre-commitment, a "done" is a post-hoc report

Consider the two things an agent emits:

- **A plan, written *before* the work.** At plan time the agent does not yet know
  what the work will reveal, where it will get stuck, or which shortcut would
  satisfy the checker. The plan is therefore a statement made *before the
  temptation to lie has a target*. It is a **commitment**, in the precise
  cryptographic sense (commit-then-reveal): a value fixed before the committer
  could know how to game what it will later be checked against.
- **A "done," emitted *after* the work.** By construction this is the moment
  "done" is the rewarded answer — the agent is now optimizing the report against
  whatever it has learned the checker wants. It is a **report**, and a report is
  the single most-gamed signal in the entire agent stack (the reward-hacking
  literature; [`84 §2`](183_how-much-does-this-lean-on-git.md)'s flake floor).

The plan and the "done" can contain the *identical sentence* — "implement X in
file Y" — and have **opposite trust value**, purely because of *when* they were
emitted relative to the work. That is clause 2: trust is a function of *timing
against temptation*, not of content.

### 3.2 What the plan actually buys you: it converts an undecidable question into a decidable one

Here is the move, and it is the load-bearing idea of this whole note. The question
*"did the agent do good work?"* is **undecidable by any mechanical oracle** —
correctness is a non-trivial semantic property and Rice's theorem forecloses it
([`84 §3.3`](183_how-much-does-this-lean-on-git.md), and the audit's Rice rung).
You cannot check it; you can only judge it (a human, or an advisory judge —
[`87`](87_the-adjudicator-trust-ladder.md)).

But *"does the work conform to the plan?"* is a **different question, and it is
mechanically decidable** — it is a conformance check between two artifacts, both
present, neither a self-report:

- the plan declares a predicate (these files, this phase, this acceptance shape);
- the work leaves an artifact (the diff's touched files, the commit ancestry, the
  test result);
- conformance is `artifact ⊨ predicate`, computed at the boundary.

**The plan is the instrument that converts an unverifiable correctness question
into a verifiable conformance question.** This is *exactly* the shape of every
checkable thing the kernel already has:

- [`verify()`](183_how-much-does-this-lean-on-git.md) checks *a commit conforms to a
  ship-stamp grammar* — the grammar is the committed predicate.
- [`scope.py`](85_extending-the-verifiable-surface.md) (`SCOPE_CREEP`/`WRONG_TARGET`)
  checks *the diff's footprint conforms to the lane's declared tree* — the
  declared tree is the committed predicate.
- [`arbitrate()`](89_the-lane-is-a-region-lock.md) checks *the requested region
  conforms to disjointness with live leases* — the lease set is the committed
  state.

Every one of these is "blackbox work, checked against a prior commitment." **The
plan-as-predicate is not a new idea bolted onto DOS — it is the generalization of
what DOS already is.** The kernel is, read this way, a *conformance engine over
agent-authored commitments*, and the slogan should be: **we don't verify the work;
we verify the work against a commitment the agent made before it could game the
check.**

### 3.3 The honesty condition: the commitment must be *binding* and *prior*

A commitment only carries trust if two things hold, and naming them tells you
exactly how the pattern fails:

- **Prior** — fixed before the work (and before the agent could observe the
  check's responses). A "plan" the agent rewrites *after* hitting a wall, to match
  what it actually did, is not a commitment — it is a report wearing a plan's
  clothes. (The kernel analogue: a ship-stamp grammar declared in `dos.toml`
  *before* the run is a commitment; one the agent edits mid-run is not. This is why
  [`SELF_MODIFY`](73_admission-predicate-plan.md) guarding the config-and-kernel
  path is *epistemic*, not moral — an agent that can rewrite the predicate
  mid-flight has destroyed the priorness that made the predicate trustworthy.)
- **Binding** — the work is actually checked against it, and divergence has a
  consequence. A plan nobody checks the work against is decoration. (The kernel
  analogue: `scope.py` exists but, per the audit, the arbiter admits on the
  declared tree at contention time and only checks conformance *post-hoc* — the
  commitment is prior but not yet *binding at the moment it matters*. §5.)

The single sentence: **trust a blackbox iff its output is checked against a prior,
binding commitment the blackbox could not edit after the fact.** Where that holds,
the agent's *internal process* is irrelevant — let it be as much a blackbox as you
like, because you are not trusting the process, you are trusting the conformance of
its artifact to a commitment. Where it does not hold, you are trusting a report,
and the kernel's whole thesis says don't.

---

## 4. Clause 3 — trust only where a wrong "yes" is cheap (detectable + reversible)

Clauses 1 and 2 tell you *what shape* of claim to trust. Clause 3 tells you *when
the stakes permit it*, and it is the clause that decides **kernel vs driver vs
human** — the layering question the operator raised ("obviously unclear things
belong in drivers, but there has to be something").

A claim is safe to trust to the degree its mis-trust is:

- **Detectable** — an independent check exists that catches a wrong trust. (Git
  ancestry detects a false "shipped." `scope.py` detects a tree the diff escaped.)
- **Reversible** — the cost of having acted on a wrong trust is bounded and
  undoable. (A local commit is reversible. A refused lane is reversible. A *silent
  overwrite of another agent's work* is **not** — "you cannot un-clobber"
  ([`98`](98_the-orchestrator-is-a-driver.md)). A sent email, a moved payment, a
  prod deploy are not — [`84 §3.4`](183_how-much-does-this-lean-on-git.md).)

This is the **blast-radius / reversibility** axis [`82 §3(a)`](182_the-kernel-is-a-taxonomy-of-refusal.md)
gestures at, promoted to the decision rule for *where a check belongs*:

| Detectable? | Reversible? | Trust posture | Lives in |
|---|---|---|---|
| yes | yes | **trust the blackbox, check the artifact** | the **kernel** — a deterministic conformance verdict (`verify`, `arbitrate`, `scope`) |
| yes | no | trust, but check **before** the effect, and prevent not detect | the **kernel at the contention/pre-effect boundary** (the §5 fix; `dos lease-lane` before a write) |
| no (needs judgment) | yes | **route to an advisory judge**, fail-to-abstain | a **driver** ([`87`](87_the-adjudicator-trust-ladder.md), `drivers/llm_judge`) |
| no | no | **route to a human**, do not auto-act | the **operator** (`dos decisions`, the actuation boundary) |

Read top to bottom this *is* the trust ladder ORACLE → JUDGE → HUMAN
([`87`](87_the-adjudicator-trust-ladder.md)), but derived from first principles
rather than asserted: **you descend the ladder exactly as detectability and
reversibility fall away.** The kernel owns the (detectable, reversible) cell
because that is the only cell where a *deterministic* verdict is both possible
(detectable) and safe to act on (reversible). The "obviously unclear things" the
operator mentioned are the bottom two rows — *not detectable mechanically* — and
that is precisely *why* they belong in drivers (judgment) or with the human, never
in the kernel. **The layering is not a taste; it is clause 3 applied to each
claim.**

> **The one-line test for "does this belong in the kernel?"** — *Can a wrong "yes"
> be caught by an independent check (detectable) and undone (reversible)?* Two
> yeses → a deterministic kernel verdict. Any no → it is a judge's or a human's,
> i.e. a driver or the decisions queue. The kernel is the home of the cheap-to-be-
> wrong, artifact-grounded conformance check, and nothing else.

---

## 5. Where the kernel breaks its own law (and the fix the audit named)

A note that only lists the clean parts is propaganda ([`82 §5`](182_the-kernel-is-a-taxonomy-of-refusal.md)
set this honesty bar). The law above is violated in exactly one place, and naming
it sharply is the point.

**The arbiter trusts a report at the moment it should trust a commitment.**
`arbitrate()` / `overlap_verdict` admit or refuse a lane purely on the agent's
**declared `tree` / `--scope`** (`lane_overlap.py:149`). By clause 2 a declared
write-set *can* be a fine commitment — it is prior (declared before the work). But
it is not **binding at the moment it matters**: the arbiter admits two lanes at
contention time on their *declared* trees, and the *conformance* check
(`scope.py`: did the diff stay in the tree?) runs only **after** the commit lands.
So the trust is:

- prior ✔ (the tree was declared first),
- detectable ✔ (`scope.py` catches a diff that escaped its tree),
- **reversible ✘** — two agents that each *under-declare* their trees are admitted
  concurrently, both write, and one silently clobbers the other. `scope.py` flags
  it afterward, but *"you cannot un-clobber"* ([`98`](98_the-orchestrator-is-a-driver.md)).

This is the (detectable, **not** reversible) row of the §4 table being handled as
if it were (detectable, reversible) — collision-*detection* where the irreversible
blast radius demands collision-*prevention*. It is the same prevented-vs-detected
gap [`98`](98_the-orchestrator-is-a-driver.md) measures for a no-write-back
harness, living *inside* the arbiter's own trust model. The deterministic-DB
analogy ([`89 §5`](89_the-lane-is-a-region-lock.md)) makes the omission precise:
Calvin sequences on declared write-sets too, but pairs it with a *reconnaissance
query + restart-on-misprediction* precisely because a declared set can be wrong.
DOS imports the analogy and omits the safeguard.

**The fix is dictated by clause 3, not invented:** for an irreversible effect, the
check must be *binding before the effect*, not detective after it. Concretely —
make the declared tree a binding pre-commitment by **enforcing the write stays
inside it at the edit boundary** (the pre-effect check), so a write outside the
declared tree is *refused*, not *recorded*. That converts the declared scope from a
report the arbiter believes into a commitment the work is held to — which is what
clause 2 required all along. (This is a driver-shaped enforcement hook over an
unforgeable artifact — the same shape as `scope.py`, moved from after the commit to
before the write.)

> **SHIPPED (2026-06-03) — the enforcement half.** `dos.scope.gate` is the
> binding pre-effect gate: the SAME containment algebra as `scope.classify`, but
> returning an ALLOW/REFUSE *decision* a caller acts on at the edit boundary
> instead of an advisory grade it files post-hoc. A write outside the declared
> tree is *refused, not recorded* — collision-PREVENTION, the (detectable, **not**
> reversible) cell of §4's table handled at the pre-effect boundary as the trust
> law demands. Surfaced as `dos scope-gate` (ALLOW=0 / SCOPE_CREEP=5 /
> WRONG_TARGET=6) so an edit-time hook / a single-writer commit broker / a foreign
> orchestrator can refuse an out-of-tree patch *before applying it*. The reference
> consumer is the job repo's `scripts/commit_broker.py` fence — its one real write
> chokepoint now routes through the kernel verdict (behind a flag; default-off is
> byte-identical). The gate enforces the *already-declared* tree; it does **not**
> predict the write-set — that precision work (general write-set prediction, the
> Calvin/OLLP reconnaissance problem) stays the open research of
> [`90 §1–§2`](90_open-research-areas.md). Baseline + the prevented-vs-detected
> numbers the gate moves: [`_baselines/scope-gate-pre-effect-2026-06-03.md`](_baselines/scope-gate-pre-effect-2026-06-03.md).

The honest restatement of the slogan, post-audit: **the kernel doesn't believe
agents' *reports*; it does, knowingly, believe their *prior commitments* — and its
one bug is a place where it believed a prior commitment without making it
binding before an irreversible effect.**

---

## 6. Framing the core problems — and why DOS beats the *next-best* thing

"Unclaimed quadrant" is the wrong axis, and the [adversarial audit](#7-see-also)
retired it (Limen, the "Right to History" sovereignty kernel, EviBound, Cedar,
Temporal all occupy adjacent cells). The right axis is sharper and more honest:
**for each concrete problem, what is the next-best thing a competent team reaches
for, and on what *specific* sub-case does DOS beat it?** A substrate earns its keep
one named problem at a time, not by owning a quadrant.

Below, each core problem is framed as the operator asked — concretely, against the
real alternative — using the trust law to say exactly where DOS wins and where it
should *concede*.

### 6.1 "Two agents clobber each other's files."

- **Next-best:** isolated **git worktrees + merge** — the optimistic-concurrency
  default now shipped by Claude Code, Codex, and Cursor. Let everyone write in
  isolation; reconcile at merge.
- **Where the next-best wins (concede it):** *disjoint or low-contention* work, and
  conflicts that a clean textual merge resolves. AgenticFlict measures only ~28% of
  agent PRs conflicting at all — so for the majority, worktrees are cheaper and DOS's
  pessimistic lock is pure tax. [`98 §5`](98_the-orchestrator-is-a-driver.md) already
  concedes this explicitly, and it is the right call.
- **Where DOS wins (the only claim worth making):** the **shared hot region** where
  a clean textual merge **silently** produces a broken or clobbered result —
  last-write-wins that *looks* like success and detonates downstream as a hand-merge
  ([`81 §2.2`](81_velocity-economics-and-the-fleet-benchmark.md)). That is the
  (detectable-late, **irreversible**) cell where *prevention* beats *detection*, and
  worktree+merge has no prevention story — it discovers the clobber after both
  branches exist. DOS's win is **not "more concurrency"; it is "no silent
  irreversible clobber on the contended region,"** via `arbitrate` + `dos lease-lane`
  pre-write (and, per §5, an edit-time scope gate to make it binding).
- **The trust-law reading:** worktrees trust the blackbox and check at merge
  (fine when reversible); DOS must justify itself *only* on the irreversible cell,
  and should stop selling pessimism anywhere else.

### 6.2 "An agent says it's done; it isn't."

- **Next-best:** read the PR / run the test suite / trust the model's report.
- **Where the next-best wins:** when the work's *quality/correctness* is the
  question — tests and human review are the only instruments, and DOS explicitly
  does **not** compete there (Rice's theorem; `verify` is artifact-existence, not
  correctness — [`84 §3.3`](183_how-much-does-this-lean-on-git.md)).
- **Where DOS wins:** the **flake floor** — work that is *shape-identical to
  success* from the outside (claimed done, files touched, everything a report-reader
  sees) where **only the artifact (a real, reachable commit) separates a flake from a
  ship** ([`84 §2`](183_how-much-does-this-lean-on-git.md)). A report-reader (even a
  very good model) is structurally the wrong instrument there; a deterministic
  ancestry check is the right one. This is the cleanest DOS win and it survives the
  audit intact — *because it is precisely the (detectable, reversible) cell where a
  prior commitment (the ship-stamp grammar) makes conformance decidable.*
- **The honest bound:** raise the forgery cost from "a sentence" to "a reachable
  commit of the right shape." Not unforgeable (the audit's `--allow-empty` /
  Goodhart point stands), but strictly stronger than believing a report, and
  hardenable rung-by-rung ([`85`](85_extending-the-verifiable-surface.md)).

### 6.3 "An agent run hangs / spins."

- **Next-best:** **Kubernetes liveness probes**, **Ray `max_restarts`**, **systemd
  `WatchdogSec` + `Restart=on-watchdog`**, **Erlang/OTP supervisors** — all of which
  detect "running but not making progress" *and* **auto-remediate** (restart).
- **Where the next-best wins (today, honestly):** *everywhere it applies*, because
  it closes the loop. DOS's `liveness()` + watchdog **detect and propose but do not
  enact** ([`99`](99_runtime-validation-and-the-actuation-boundary.md), [`101`](101_watchdog-driver-and-the-poll-cadence.md)),
  which — by clause 3 — is the right restraint *only* for the (not-reversible /
  ambiguous) case. For the unambiguous case (a run STALLED for 4 hours, no commits,
  no heartbeat), restart is cheap and the incumbents just do it. The audit's sharp
  line: *K8s catches "running but unable to make progress" and restarts it; DOS
  detects the same on a bespoke journal and asks a human to paste a kill command* —
  re-injecting the human latency into the very speed incident
  ([`99 §2.1`](99_runtime-validation-and-the-actuation-boundary.md)) it was built for.
- **Where DOS *could* win (the fix the law dictates):** two genuine differentiators
  the incumbents lack — (a) the verdict is **evidence-grounded** (git/journal delta,
  not a self-reported `/healthz` the agent controls — clause 1), and (b) it is a
  **pure, replayable** verdict, not an opaque kubelet decision. But to beat the
  next-best it must **close the loop on the high-confidence cell**:
  *confidence-tiered* auto-halt — auto-stop the unambiguous STALLED-past-budget run
  (detectable + the stop is reversible: you can relaunch), *propose-only* the
  ambiguous SPINNING one (judgment needed). A flat never-enact rule cedes the whole
  problem to Ray/K8s; clause 3 says enact exactly where mis-trust is cheap.
- **The deeper honesty:** `liveness()` is a *failure detector*, and FLP /
  Chandra-Toueg prove a perfect one is impossible asynchronously — so SPINNING is an
  unreliable verdict on a threshold, not ground truth. That is fine (every failure
  detector is), but it means liveness must be sold as *advisory evidence feeding a
  tiered actuator*, never as a clean oracle. ([`90 §5`](90_open-research-areas.md) is
  the ROC/threshold research this implies.)

### 6.4 The pattern across all three

DOS wins on a *named, narrow* cell every time — and it is **always the same cell**:
*(an unforgeable artifact exists) × (mis-trust is silent or irreversible)*. That is
the cell where (a) a report-reader is the wrong instrument because the lie is
shape-identical to truth, and (b) detection-after is too late because you cannot
undo the effect. **That intersection is DOS's actual product** — not "a trust
kernel" in the abstract, but *the deterministic conformance check for the
specific cell where reports fail and rollback is impossible.* Everywhere else
(reversible, or judgment-bound, or disjoint) the next-best alternative is as good or
better, and the honest move — which [`98 §5`](98_the-orchestrator-is-a-driver.md)
already models — is to **concede those cells loudly** and integrate with the
incumbent (worktrees, Ray, the human) rather than reinvent it weaker.

---

## 7. The synthesis (one paragraph)

"Never trust the agents" was always shorthand. The real law is that the kernel
trusts **structure** (a well-formed request — the Linux `copy_from_user` posture),
trusts **prior commitments** (a plan/scope/stamp fixed before the temptation to lie
had a target — the commit-then-reveal asymmetry that turns the undecidable "is this
good work?" into the decidable "does this work conform to its commitment?"), and
trusts **only where a wrong yes is detectable and reversible** (which is *why* the
kernel owns the deterministic-conformance cell and drivers/humans own the rest — the
ORACLE→JUDGE→HUMAN ladder derived, not asserted). Read this way DOS is a
*conformance engine over agent-authored commitments*, its one real bug is a place
where it believed a prior commitment without making it binding before an
irreversible effect (the arbiter's declared-tree trust), and its honest pitch is not
an unclaimed quadrant but a single hard-won cell: **the deterministic check for the
case where a report would be believed, the lie is shaped exactly like the truth, and
you cannot un-do the damage after the fact.** That cell is small, it is real, and on
it DOS beats every next-best alternative — which is a stronger thing to be able to
say than "nobody else has built this."

---

## 8. See also

- [`182_the-kernel-is-a-taxonomy-of-refusal.md`](182_the-kernel-is-a-taxonomy-of-refusal.md)
  — every syscall is a *no*; §3(a)'s blast-radius/reversibility field is clause 3's
  seed, and §4's epistemic/moral line is clause 2's priorness seen from the side.
- [`183_how-much-does-this-lean-on-git.md`](183_how-much-does-this-lean-on-git.md) —
  the flake floor (§6.2's win) and the necessary-not-sufficient ceiling (why
  correctness is a judge's, not the kernel's).
- [`85_extending-the-verifiable-surface.md`](85_extending-the-verifiable-surface.md)
  — `scope.py` (the conformance check of §3.2) and the deeper-rung hardening §6.2
  leans on; §5's fix is its pre-effect sibling.
- [`87_the-adjudicator-trust-ladder.md`](87_the-adjudicator-trust-ladder.md) — the
  ORACLE→JUDGE→HUMAN ladder §4 derives from detectability + reversibility.
- [`89_the-lane-is-a-region-lock.md`](89_the-lane-is-a-region-lock.md) — the
  region-lock and the Calvin analogy whose missing safeguard §5 names.
- [`98_the-orchestrator-is-a-driver.md`](98_the-orchestrator-is-a-driver.md) —
  prevented-vs-detected and "you cannot un-clobber" (the irreversible cell of §6.1);
  the concede-the-disjoint-case model §6.4 generalizes.
- [`99_runtime-validation-and-the-actuation-boundary.md`](99_runtime-validation-and-the-actuation-boundary.md)
  / [`101_watchdog-driver-and-the-poll-cadence.md`](101_watchdog-driver-and-the-poll-cadence.md)
  — the actuation boundary §6.3 argues should become confidence-tiered.
- [`90_open-research-areas.md`](90_open-research-areas.md) — the open questions this
  frame ranks: §5's edit-time gate (its §1–§2), §6.3's liveness ROC (its §5).
- **Adversarial conceptual audit (2026-06-02)** — the skeptic's brief this note
  answers: the verified prior-art twins that retired "unclaimed quadrant", and the
  three internal contradictions (arbiter declared-tree trust, the ⅓ fractional-lock,
  liveness as an FLP-bounded detector). Recorded in the project memory
  (`project-dos-adversarial-audit-2026-06-02`).
- **Field instance — trustworthy fan-out ships (job repo, 2026-06-04)** — clauses
  1–3 proven live outside the kernel: a `/dispatch` fleet shipped 5/5 clean through
  an *adapter that lied* (`dispatch_loop_iter_driver` latched a foreign `chained_ts`
  and mis-reported `BLOCKED`). The consuming orchestrator trusted **structure**
  (`git merge-base --is-ancestor HEAD` on each pick, traced to the child run naming
  its own loop ts — §7's "reachable commit of the right shape") over **content** (the
  verdict token), reproducing `verify()`'s `registry ⋈ ancestry` rung
  ([`109`](109_non-git-evidence-in-the-verify-verdict.md)) by hand at the point its
  adapter mis-fed it. The job-side throughline — *the clean SHIP and the honest STOP
  come from one design: an orchestrator that stays out of the work and refuses to
  believe its own tooling* — is clause 1 (structure-not-content) read from the
  consumer side. Write-up: `job/docs/trustworthy-fanout-ships.md`.
```
