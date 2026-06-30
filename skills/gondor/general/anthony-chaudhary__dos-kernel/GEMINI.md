# DOS — the part that doesn't believe the agents

This extension gives you the DOS trust syscalls as tools. DOS exists because an
agent's word about its own work is the weakest signal in the loop. A worker can
*say* it shipped a fix, *say* the tests pass, *say* it booked the reservation —
and be wrong, or lying, with full confidence. DOS answers those questions from
**ground truth** instead: git history, the file tree, a clock. Never from what
the agent said it did.

Use these tools before you trust a claim, not after.

## The rule

When you — or another agent, or the user — claim that a piece of work is
**done**, do not trust the claim. Check it. The tools below check it for you.

- **Before you report a task, phase, or feature as finished**, call
  `dos_verify` (did this plan/phase actually ship?) or `dos_commit_audit` (does
  this commit's message match what its diff actually did?). If the witness does
  not confirm the claim, say so plainly — do not report done.
- **Before two agents edit the same area at once**, call `dos_arbitrate` to find
  out whether their file trees collide. Disjoint trees may run together; an
  overlap is a refuse, and the tool names a free lane instead.
- **When you must decline or report blocked**, use `dos_refuse_reasons` /
  `dos_check_reason` to pick a structured reason from the closed set, instead of
  free-text prose a system can't verify.
- **Before you rely on a cited legal case**, call `dos_citation_resolve` to
  confirm it exists in a real reporter — the antidote to a fabricated citation.

## Why this matters

The failure DOS catches is the *confident phantom*: a write the agent authored
and believes, contradicted by a witness the agent wrote zero bytes of. A booking
"confirmed" that is not in the database. A `fix:` commit that only touched a
README. A `--allow-empty "implemented the cache"` that changed nothing. Each one
looks done. Each one is caught by reading the evidence, not the narration.

So: read the evidence. The tools are how.

## Setup

These tools need the `dos-kernel` Python package on the same machine:

```bash
pip install 'dos-kernel[mcp]'
```

Then verify the syscalls work against a plain git repo:

```bash
dos verify --workspace . PLAN PHASE   # did (plan, phase) actually ship?
dos commit-audit --workspace . HEAD   # does HEAD's subject match its diff?
```

Full tour: https://github.com/anthony-chaudhary/dos-kernel — `dos quickstart`
for the 60-second caught-lie demo.
