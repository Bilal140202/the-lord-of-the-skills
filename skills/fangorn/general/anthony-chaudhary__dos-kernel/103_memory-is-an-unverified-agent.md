# Memory is an unverified agent — recall is a `verify()` problem

> **An agent's persistent memory is a fleet of self-narrating workers writing to
> shared state, read back later without anyone checking whether what they wrote is
> still true. That is the exact problem DOS exists to solve, pointed inward. The
> memory file says "FIXED in cli.py:1000"; the code moved two commits ago; the
> memory didn't; and at recall time the claim is injected into context wearing the
> authority of a fact. This note states the memory problems we are actually seeing,
> shows each one is a syscall DOS already ships (`verify` / `liveness` / `refuse` /
> `arbitrate` / the run-id spine), and derives a recall discipline from the doc-102
> trust law: *a memory is a prior commitment, not a present fact — trust its
> structure, re-verify its content against ground truth at recall, and surface the
> verdict, never the raw claim.***

This is a theory note in the family of [`82`](182_the-kernel-is-a-taxonomy-of-refusal.md)
(every syscall is a *no*), [`84`](183_how-much-does-this-lean-on-git.md) (git is
necessary, not sufficient), and especially [`102`](102_when-to-trust-an-agent.md)
(trust structure not content; trust prior commitments not reports; trust only where
a wrong "yes" is cheap). Doc 102 derived the trust law from the kernel's own
mechanisms. This note **applies that finished law to a substrate we run every day
and have never adjudicated: the agent's own memory.** It carries one litmus (§7)
and proposes a small mechanism shaped exactly like the existing syscalls — a memory
*driver* over the kernel, never a kernel change.

It exists because the problem is not hypothetical. §1 reproduces it on this very
repo's memory store, with a claim that is provably stale today.

---

## 1. The problem, reproduced (not hypothesized)

The agent operating this repo keeps a file-based memory: ~80 markdown files
(~400 KB of body text) plus a 15 KB / 100-line `MEMORY.md` index that is loaded
into context **every session**. The store has the precise pathology DOS was built
for. Three measured facts:

1. **35 of the ~100 index lines assert a *completed state*** — "SHIPPED", "FIXED",
   "DONE", "LANDED", "BUILT", "cut". Each was true when written and is a *report*,
   in the doc-102 sense — emitted after work, frozen at write time, never
   re-checked against the code.
2. **64 of the ~80 files hard-code a write-time date** (`2026-06-0x`) in their body.
   The timestamp is the one thing guaranteed to be honest *and* the one thing that
   guarantees the surrounding claim is aging.
3. **At least one such claim is stale *right now*.** The memory
   `project-dos-quality-audit-2026-06-02` opens with: *"RED SUITE (live, must-fix):
   `cli.py:1000/1025` does `from dos.drivers import watchdog` → 2 failed, 905
   passed."* Run the check today:

   ```bash
   $ grep -n "from dos.drivers import watchdog" src/dos/cli.py
   1024:    `from dos.drivers import watchdog`. The distinction is real, ...   # ← a comment, not an import
   $ git log --oneline | grep watchdog
   a7a145d cli: resolve the watchdog driver by name, not a static import      # ← already fixed
   ```

   The breach was fixed in commit `a7a145d`; the only remaining occurrence in
   `cli.py` is *inside a comment explaining the fix*. The two tests the memory warns
   are red are green. `config.ensure()` — which the same memory lists as an
   un-done refinement — shipped in `2600110` (`config.py:946`). `py.typed` —
   "missing" per the memory — ships as of `3488a4c`.

A session that recalls that memory today inherits a **confident, wrong instruction**
to go fix a breach that no longer exists. The memory did its job — it stored what
was true — and is now *actively harmful* precisely because recall presents it as a
fact rather than as a dated claim awaiting re-verification.

This is not a memory-hygiene nit. **It is the founding DOS problem** — a worker that
narrated a state, the ground truth moved, the narration didn't, and a later reader
believed the narration. The whole kernel is the answer to "don't believe that." We
just never pointed it at our own notes.

---

## 2. Memory *is* a fleet of unreliable workers writing shared state

Line up the DOS problem statement against the memory store, field for field:

| DOS's premise | The memory store |
|---|---|
| many **autonomous agents** | many **past sessions**, each a different agent-instance |
| that are **self-narrating** | each memory is a session's *self-report* of what it learned/did |
| writing **effects to shared state** | appending files + index lines to one shared store |
| read by others who **can't see the work** | a later session reads the claim with **zero access** to the work that produced it |
| **without believing what they say they did** | …except here we *do* believe it — recall injects the raw claim as context |

The match is exact, and it exposes the asymmetry doc-102 §3 is built on. A memory
written *after* work is a **report** — the most-gamed, least-trustworthy signal in
the stack — yet recall treats it with *more* authority than a live report, because
it arrives pre-loaded, unattributed to its (now-stale) moment, and stripped of the
evidence that once backed it. We took the single weakest signal class and gave it
the strongest delivery channel. The harness even wraps recalled memories in a
`<system-reminder>` and notes they "reflect what was true when written … verify it
still exists before recommending it" — i.e. **the platform already knows memory is
a report and asks the agent to re-verify by hand.** Doing that by hand does not
scale to 80 files; it is exactly the manual check DOS mechanizes for ship-state.

The reframe, stated once: **a memory file is a lane-journal entry, not a fact.** It
records that *a past run claimed something*. Whether the claim still holds is a
`verify()` question, to be answered at recall against ground truth — never assumed.

---

## 3. Every memory problem is a syscall we already ship

The value of the reframe is that the solutions are not new — they are the existing
syscalls, re-aimed. Each observed memory failure mode is one of them.

### 3.1 Stale "FIXED/SHIPPED" claims → `verify()`

The §1 failure is `verify()`'s home turf. `verify(plan, phase)` already answers
"did this *actually* ship?" from git ancestry, never from self-report, and **works
with no plan present** (`source="none"`). A memory whose body says "SHIPPED commit
9866239" or "FIXED in cli.py:1000" carries, structurally, *a claim of a shipped
state* — which is precisely the claim `verify` adjudicates.

So recall should not surface `"FIXED: cli.py RED breach"`. It should surface the
**verdict of re-checking that claim now**:

```
[memory project-dos-quality-audit · claim "cli.py RED breach" · STALE
   (git: fixed in a7a145d; the import the memory flags is now a comment)]
```

The memory becomes the *prior commitment*; `verify` (or a cheap grep/ancestry probe
in its spirit) becomes the *binding check at read time*; the agent sees conformance,
not narration. This is doc-102's clause-2 move verbatim: convert the undecidable
"is this memory still right?" into the decidable "does this claim conform to ground
truth right now?"

### 3.2 Aging facts with no freshness signal → `liveness()`

64 files freeze a date and never move. That is a **liveness** question — not "is
this memory true?" but "is this memory still *moving with* the thing it describes?"
`liveness()` already distinguishes ADVANCING / SPINNING / STALLED from a git/journal
delta, never from a "still fresh!" self-report. The same verdict shape applies to a
memory:

- **FRESH** — the files/commits the memory names have not moved since it was
  written (its evidence is unchanged → the claim likely holds).
- **DRIFTING** — the named region has changed since the memory's date (re-verify
  before trusting).
- **STALE** — the named artifact is gone, or `verify` now disagrees.

The evidence is gathered the same way `liveness` already does it — `git_delta` over
the paths/SHAs the memory references since the memory's own timestamp — and the
verdict is **pure** over that evidence. A memory dated `2026-06-02` that names
`cli.py:1000` is trivially classifiable: `cli.py` changed in `a7a145d` *after* that
date → DRIFTING → re-verify → STALE. No new mechanism; `liveness.classify` with the
memory's `(date, named-paths)` as the `ProgressEvidence`.

### 3.3 Confidently-wrong recall → `refuse()` (the abstain rung)

The deepest fix is the cheapest. Today recall has exactly one outcome: *inject the
claim*. It has no vocabulary for **"I am not sure this is still true."** That is the
missing structured refusal. The closed-reason discipline ([`82`](182_the-kernel-is-a-taxonomy-of-refusal.md),
[`HACKING.md`](HACKING.md)) says: don't emit free-text confidence, emit a token from
a closed set. A recall verdict should be one of:

`RECALL_FRESH` · `RECALL_DRIFTING` · `RECALL_STALE` · `RECALL_UNVERIFIABLE`

— and on anything but `FRESH`, recall should **present the memory hedged, or
withhold it**, the way `run_judge` *fails to abstain* ([`87`](87_the-adjudicator-trust-ladder.md),
[`judges.py`]). A memory that can't be checked (names no concrete artifact — a pure
opinion or a positioning take) is `RECALL_UNVERIFIABLE`: fine to surface, but
*marked* as unfalsifiable, never as fact. The single highest-leverage change in this
whole note is giving recall a **way to say "no, or not sure"** instead of only "yes."

### 3.4 Index bloat / 80 overlapping files → `arbitrate()` (a region-lock on the index)

The index grows because writes never contend. Two sessions each add a memory about
the same subject (the recurring "concurrent SCV collision" / "concurrent automation"
pattern, already recorded *twice* in this store) with no admission control. That is
the **arbiter's** problem: a memory write is a lane request over a *topic region*,
and a new write whose topic overlaps an existing memory's region should be
*refused-and-redirected to an update*, exactly as `arbitrate` redirects a busy lane
to a free one. "Update the existing file rather than create a duplicate" — already
the stated rule in the memory spec — is **`arbitrate` applied to the index**, today
enforced only by the writer's goodwill. The disjoint-region check is `lane_overlap`
over topic slugs instead of file globs; the verb is the same.

### 3.5 The store as a whole → the run-id spine + lane journal

A memory that recorded *which run wrote it, against which workspace SHA* would carry
its own provenance — the [`run_id`](../src/dos/run_id.py) + [`lane_journal`](../src/dos/lane_journal.py)
spine, which is exactly "sortable, lineage-carrying" identity plus an append-only
record of who-did-what-when. The memory frontmatter already half-does this
(`originSessionId`); it is one field short of being a spine entry (the workspace SHA
at write time), which is the single datum §3.2's liveness check needs and §3.1's
verify wants. **Memory provenance is the spine, under-populated.**

---

## 4. The recall discipline (the trust law, applied)

Doc 102's three clauses resolve the design without a single new principle:

- **Clause 1 — trust structure, never content.** Trust a memory's *form* (it is a
  well-formed record that a past run claimed X about region R on date D). Never trust
  its *content* (that X is true now). The frontmatter is structure → believed; the
  body is a claim → re-checked. This is `copy_from_user` for recall: validate the
  pointer (the named artifact exists), don't dereference the claim on faith.
- **Clause 2 — trust commitments, never reports.** A memory is a **prior
  commitment** (fixed at date D, before the agent could know how the future would
  diverge) — which is the *good* kind of trust, but only once it is made **binding**
  by checking the present against it. An unchecked memory is "a report wearing a
  plan's clothes" (102 §3.3): present-tense authority for a past-tense claim.
- **Clause 3 — trust only where a wrong "yes" is cheap.** A *checkable* memory (names
  a file/commit/flag — §3.1's 8 such index lines, §3.2's 64 dated bodies) lands in
  the (detectable, reversible) cell → **re-verify deterministically at recall**. An
  *un-checkable* memory (a positioning judgment, a preference) is not mechanically
  decidable → surface it, but **marked `UNVERIFIABLE`**, the judge/human cell, never
  dressed as a verified fact.

The one-line discipline, in the shape of 102's one-line kernel test:

> **At recall, a memory is a dated claim, not a fact. If it names a concrete
> artifact, re-verify the claim against ground truth *now* and surface the verdict
> (`FRESH`/`DRIFTING`/`STALE`); if it names nothing checkable, surface it tagged
> `UNVERIFIABLE`. Never inject a memory's raw content as if recall had confirmed
> it.**

This is the same posture the kernel takes toward `verify` over a commit subject: the
claim is believed *to the extent an independent artifact backs it, checked at the
moment of use*, and not one inch further.

---

## 5. Why this is a driver, not a kernel change (and not a kernel dependency)

Critically, **none of this touches `src/dos/`.** The kernel already ships every
verdict this needs — `verify` (ship-state), `liveness.classify` (freshness from a
delta), the closed-reason refusal discipline, `arbitrate`/`lane_overlap` (region
disjointness), the run-id/journal spine. A "memory referee" is a **consumer of those
syscalls**, on the same side of the line as `dos_mcp` and the release tooling
([CLAUDE.md] layering): it `import dos`, the kernel never imports it.

Concretely it is a small driver / CLI verb that, given a memory store:

1. parses each memory's frontmatter (structure — clause 1) and extracts any named
   artifacts from the body (paths, `commit <sha>`, `cli.py:NNN`, `--flag`,
   `function()`);
2. for each, runs the matching kernel verdict — `verify` for a ship/commit claim,
   `liveness.classify` over `git_delta` since the memory's date for a freshness
   claim, an `exists?` probe for a named-file claim;
3. emits a closed-vocabulary recall verdict per memory, and
4. routes the non-`FRESH` ones to the operator the way [`decisions`](../src/dos/decisions.py)
   already routes the four refusal sources — *"these 5 memories are STALE; here is
   the git evidence; archive or update?"*

That is `dos decisions` with a fifth source (recalled-memory drift), and `verify`
fanned out over a memory store instead of a plan registry — both are projections we
already build. The memory store is, in DOS terms, **just another workspace with a
journal; adjudicate it like one.** (The dogfood ritual in [CLAUDE.md] — *don't take
the kernel's behavior on faith, run the syscalls and read the verdict* — is the
whole argument: we have been exempting our own memory from the one discipline the
repo is about.)

A note on the irreversibility axis (102 §4): recall mis-trust is *detectable*
(the git check exists) and *reversible* (a hedged or withheld memory is recoverable;
nothing is clobbered). So by clause 3 the **verdict belongs in the kernel-shaped
deterministic cell** and the *action* (hedge / withhold / archive) is safe to
automate — unlike the arbiter's irreversible-clobber bug, there is no "you cannot
un-recall" hazard. This is a clean (detectable, reversible) cell, which is why the
mechanism can be fully deterministic and advisory-routed rather than human-gated.

---

## 6. What this does *not* claim (the honesty section, per 82 §5 / 102 §5)

- **It does not make memory trustworthy — it makes recall *honest about
  un-trust*.** `verify` over a commit doesn't prove the work is *good* (Rice;
  [`84 §3.3`](183_how-much-does-this-lean-on-git.md)); likewise re-verifying a memory
  doesn't prove its *judgment* was right, only that its *checkable claims* still
  conform. A memory's opinion ("positioning X beats Y") stays `UNVERIFIABLE` forever
  — and that is correct, not a gap.
- **It does not catch the lie that is shape-identical to truth.** A memory could
  name a commit that exists but mis-describe it; `verify` raises the forgery cost
  from "a sentence" to "a real artifact of the right shape" (102 §6.2) and no
  further. Strictly stronger than believing the raw claim; not unforgeable.
- **It does not solve the *write*-side judgment** of what deserves a memory — that
  is the `feedback-save-thinking-in-docs-not-memory` rule (substantive thinking →
  a doc, memory → pointers + non-derivable facts), which is a *policy* and stays a
  policy. This note governs **recall**, the read path. The two compose: fewer,
  pointer-shaped memories (the write rule) that are re-verified at read (this note).
- **It does not auto-delete.** Like the watchdog ([`101`](101_watchdog-driver-and-the-poll-cadence.md))
  and `liveness`, it **records and proposes** — STALE → routed to the decisions
  queue, not silently purged. The operator (or a future confidence-tiered rung,
  102 §6.3) decides; the mechanism only refuses to *launder* a stale claim into a
  fact.

---

## 7. The litmus

> **A recalled memory is presented with a freshness verdict, never as bare content.**
> A memory whose body names a concrete artifact (a path, a commit SHA, a
> `file:line`, a flag, a function) MUST be re-checked against ground truth at recall
> and surfaced with a closed-vocabulary verdict (`RECALL_FRESH` / `RECALL_DRIFTING` /
> `RECALL_STALE` / `RECALL_UNVERIFIABLE`); a memory naming nothing checkable is
> surfaced tagged `RECALL_UNVERIFIABLE`. The check is a *consumer* of the existing
> syscalls (`verify`, `liveness.classify`, an `exists?` probe over `git_delta`) — no
> module under `src/dos/` imports the memory driver, the same one-way arrow as
> `dos_mcp` and `scripts/`.

Grep-checkable in spirit the same way the others are: the memory referee lives
outside `src/dos/` (a driver, the MCP surface, or dev tooling under `.claude/`);
`import .*memory_referee` must not appear under `src/dos/`. And the dogfood proof
is the §1 reproduction inverted: point the referee at this repo's own memory store
and it must return `RECALL_STALE` for the `cli.py RED breach` claim with the
`a7a145d` git evidence — if it ever returns `FRESH` for a claim git disagrees with,
the discipline has drifted from the code, exactly as a broken `verify` would.

---

## 8. The synthesis (one paragraph)

We built a kernel whose entire reason to exist is that an agent's report of what it
did is the least trustworthy signal in the system — and then we wired the agent's
*own memory*, which is nothing but a pile of frozen reports, straight into context
as fact. The §1 reproduction is not an embarrassment to hide; it is the cleanest
possible proof that the thesis is real and that we under-apply it. Every memory
failure we see is a syscall we already ship, re-aimed: stale "FIXED" is `verify`,
aging facts is `liveness`, confidently-wrong recall is the missing `refuse`/abstain
rung, index bloat is `arbitrate` over topic regions, and provenance is the run-id
spine one field short. The fix is not a kernel change and not a new principle — it
is doc-102's trust law applied to a substrate we exempted: **a memory is a prior
commitment, not a present fact; trust its structure, re-verify its content against
ground truth at the moment of recall, and surface the verdict instead of the
claim.** The kernel is the part that doesn't believe the agents. Memory is the agent
we forgot to stop believing.

---

## 9. See also

- [`102_when-to-trust-an-agent.md`](102_when-to-trust-an-agent.md) — the trust law
  (structure/commitment/cheap-wrong-yes) this note applies; §4's detectable×reversible
  table places recall in the clean (yes,yes) cell.
- [`182_the-kernel-is-a-taxonomy-of-refusal.md`](182_the-kernel-is-a-taxonomy-of-refusal.md)
  — every syscall is a *no*; §3.3's `RECALL_*` set is the closed-reason discipline
  applied to recall.
- [`183_how-much-does-this-lean-on-git.md`](183_how-much-does-this-lean-on-git.md) —
  git necessary-not-sufficient; the bound on what re-verifying a memory can and
  can't prove (§6).
- [`87_the-adjudicator-trust-ladder.md`](87_the-adjudicator-trust-ladder.md) — the
  fail-to-abstain discipline §3.3's hedged-recall mirrors; `UNVERIFIABLE` is the
  abstain rung.
- [`99`](99_runtime-validation-and-the-actuation-boundary.md) /
  [`101_watchdog-driver-and-the-poll-cadence.md`](101_watchdog-driver-and-the-poll-cadence.md)
  — record-and-propose, never silently enact (§6's no-auto-delete stance).
- `CLAUDE.md` — the layering (§5's "consumer, not kernel" placement) and the DOS-on-DOS
  dogfood ritual the §1/§7 reproduction extends to the memory store.
