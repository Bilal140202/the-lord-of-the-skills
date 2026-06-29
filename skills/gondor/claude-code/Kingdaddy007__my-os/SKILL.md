---
name: coding
description: >
  Use this skill when writing, modifying, or generating code of any kind.
  Activated when the user asks to build features, implement functions, create
  components, write endpoints, set up forms, wire things together, or produce
  any working implementation. Trigger phrases: "build this", "implement",
  "write the code for", "create a function that", "add this endpoint", "make
  it work", "update this code to", "wire this together".
  Do NOT use for: pure architectural decisions before implementation starts
  (use architecture skill), root-cause debugging of existing broken code
  (use debugging skill).
---

# Coding

## WHEN TO USE THIS

- Writing new code: functions, components, modules, services, endpoints
- Modifying existing code to change behavior
- Refactoring local implementation details while preserving behavior

## NEVER DO

- Write code before understanding what it needs to accomplish
- Skip error handling because the happy path works
- Create an abstraction for fewer than 3 concrete cases
- Optimize before profiling proves there is a bottleneck
- Leave commented-out code, debug statements, or unused imports
- Write clever/compressed code that trades clarity for brevity
- Proceed when architecture is unresolved — flag it first

---

## IMPLEMENTATION PRIORITIES (in order)

1. **Readability** — Can a new engineer understand this without asking? If the code requires a comment explaining WHAT it does, rename until the name makes it obvious.
2. **Correctness** — Handle null, empty, malformed, extremely large, concurrent, and failed-dependency cases. Write happy path first, then add each failure mode.
3. **Maintainability** — Small focused functions, explicit dependencies, no global state, pure logic separated from side effects.
4. **Convention compliance** — Match the existing codebase's naming, layering, and patterns. Consistency beats local brilliance.
5. **Performance** — Only after profiling proves a bottleneck. Optimize surgically behind a clean interface.
6. **Testability** — Isolate side effects. Favor pure functions for logic. Design seams where tests can inject fakes.

---

## CODING LENSES

Run these before and during implementation:

| Lens | Question |
| --- | --- |
| Intent | Is business intent obvious from names alone — without reading the body? |
| Scope | Does this function/module have exactly one job? |
| Abstraction | Is this layer necessary now, or am I abstracting for imagined futures? |
| Boundaries | Are inputs validated at entry points? Are outputs intentional? |
| Error behavior | What happens on failure, timeout, malformed input? Handled or swallowed? |
| State/side effects | Where exactly does state change? Is the order obvious? |
| Testability | Can important behavior be verified without heroic setup? |
| Consistency | Does this match the surrounding codebase's patterns? |
| Simplicity | Is there a simpler version that satisfies the same requirements? |
| Change safety | What will break when someone edits this? Are dependencies explicit? |

---

## EXECUTION SEQUENCE

### New code

1. Define the interface first — inputs, outputs, errors, side effects
2. Write the most readable, obvious solution (no optimization yet)
3. Use names that reflect domain/business meaning, not vague mechanical detail
4. Add error handling for each failure mode before moving on

### Modifying existing code

1. Read surrounding code until you understand the local design intent
2. Identify what behavior must stay unchanged before touching anything
3. Make the smallest change that achieves the goal
4. Check sibling functions — if one had the bug, the twin probably does too

### When unclear

1. State the ambiguity explicitly
2. Ask if it materially affects implementation
3. If architecture is unresolved, flag it — don't code around it

---

## ANTI-PATTERNS

| Anti-Pattern | What It Is | Fix |
| --- | --- | --- |
| Cleverness trap | Nested ternaries, bitwise tricks, compressed chains | Write the obvious version. Lines are free. |
| Premature abstraction | Interface with 1 implementation, factory for 2 classes | Wait for 3 concrete cases (Rule of Three) |
| Premature optimization | Complex data structures for theoretical perf gains | Write simple. Profile. Optimize the measured bottleneck only. |
| God function | 200-line function doing validation, logic, DB, API, logging | Extract: orchestrating function reads like a table of contents |
| Shallow module | Wrapper that adds nothing over the underlying call | Only wrap when adding error handling, retry, logging, or domain adaptation |
| Silent failure | Empty catch, returning null instead of throwing, ignoring 500s | Fail fast. Log with context. Force callers to handle failure cases. |
| Copy-paste programming | Same 15 lines across 8 files with minor variations | Extract after 3+ concrete cases. Patch all copies immediately in the meantime. |
| Context ignorance | Solves the local request but violates surrounding architecture | Read the architecture before implementing. Match layer, naming, responsibility. |

---

## MANDATORY VERIFICATION TRACE

Before declaring done, follow data from origin → through every transformation → to final consumer.

**Example:** "Color injected at line X → sanitizeCandleBar at line Y returns `{time, open, high, low, close, color}` → series.update() at line Z receives all required fields. Confirmed."

If a parallel function exists (`sanitizeTickPoint` ↔ `sanitizeCandleBar`): verify BOTH.

---

## NON-NEGOTIABLE CHECKLIST

- [ ] All variables and functions are named for business/domain intent (not `data`, `flag`, `process`, `check`)
- [ ] Functions have one clear responsibility and ≤3 parameters (use options object if more needed)
- [ ] All foreseeable error paths are handled — no empty catch blocks without documented justification
- [ ] No external dependency failures are silently ignored
- [ ] No commented-out code, debug statements, or unused imports remain
- [ ] Code follows existing project naming, layering, and style
- [ ] Structural verification trace completed before delivery

---

## OUTPUT SHAPE

**Simple implementation:** Brief statement of what was built → Code → What to verify

**Moderate implementation:** Objective restatement → Approach and rationale → Code → Assumptions made → Edge cases and error handling → What to verify

**Complex implementation:** All of the above + Key design decisions explained + Testing recommendations + Security/performance considerations if relevant + Next steps
