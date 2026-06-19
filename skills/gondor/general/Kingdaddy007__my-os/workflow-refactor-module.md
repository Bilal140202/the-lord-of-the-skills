# WORKFLOW: REFACTOR MODULE (FULL SOURCE)

**Version:** Gold v1.1 (Master Merge)
**Layer:** 8 — Execution Workflow
**Tier:** 2 — Loaded by task
**File:** workflows/workflow-refactor-module-SOURCE.md
**Primary Mode:** Optimizer
**Secondary Modes:** Builder, Reviewer, Architect, Debugger
**Purpose:** The systematic sequence for improving code structure without changing external behavior — from identifying what to improve through safe transformation to verified behavioral preservation. Enforces the discipline of locking behavior with tests BEFORE changing structure, and verifying preservation AFTER.
**Loaded When:** Improving code quality, reducing tech debt, restructuring modules, extracting shared code, or preparing code for new feature work.
**Inherits From:** execution-workflow.md (universal process)

---

## WHAT THIS WORKFLOW DOES

This workflow ensures refactoring is safe, scoped, and valuable — not a disguised rewrite or an open-ended cleanup session that never finishes.

Without this workflow, refactoring either does not happen and tech debt grows, happens recklessly and introduces regressions, or scope-creeps into a rewrite that stalls the team.

---

## ACTIVATION

### Use When

- "Clean up this code"
- "This module is messy — simplify it"
- "Refactor this module"
- "Reduce technical debt in [area]"
- "Extract shared logic from these components"
- "Make this maintainable"
- "Restructure [module] for better maintainability"
- "This area is too tangled"
- Preparing a messy module for new feature work
- Code review flagged structural issues that need addressing

### Do NOT Use When

- Fixing a specific bug → use `workflow-debug-issue.md`
- Adding new behavior → use `workflow-build-feature.md`
- Changing architecture — new boundaries or new services → use `workflow-plan-architecture.md`
- Optimizing performance → use `workflow-optimize-performance.md`
- Broad cleanup with no clear module boundary
- Cosmetic changes with no structural goal

If the real problem is architecture-level rather than local structure, escalate to `workflow-plan-architecture.md`.

---

## REQUIRED FILES

### Skills — Always Load

| Priority | Skill | Why |
| :--- | :--- | :--- |
| Primary | `skill-refactoring` | Safe methodology, Strangler Fig, scope control |
| Primary | `skill-coding` | Implementation quality standards |
| Secondary | `skill-testing` | Characterization tests, behavior preservation |
| Secondary | `skill-review-audit` | Code quality assessment |

### Skills — Load When Relevant

| Condition | Skill |
| :--- | :--- |
| Refactoring involves boundary changes | `skill-architecture` |
| Underlying bugs discovered during refactor | `skill-debugging` |

### Contexts — Always Load

- `coding-standards.md`
- `stack-context.md`
- `architecture-context.md`
- `domain-rules.md`

### Contexts — Load When Relevant

| Condition | Context |
| :--- | :--- |
| Moving code across architecture boundaries | `architecture-context.md` (deep load) |
| Adding significant test coverage | `testing-standards.md` |
| Refactoring data access layer | `database-context.md` |

---

## REQUIRED INPUTS

At minimum, Anti-Gravity should have or establish before proceeding:

- a clearly identified module or bounded target area
- enough context to understand what the module currently does
- what behavior must remain unchanged
- what tests or safeguards exist
- what level of change risk is acceptable

### If inputs are incomplete

Do NOT begin by moving files and renaming at random. Instead:

1. Define the exact module boundary first
1. Identify what behavior must remain stable
1. State assumptions explicitly
1. Ask clarification only when missing information materially changes module scope or refactor risk

---

## EXECUTION SEQUENCE

---

### STEP 1 — ASSESS THE CURRENT STATE

**Mode:** Optimizer
**Goal:** Understand what exists and why it is problematic before touching anything. Code that seems messy may contain hard-won business logic that is not yet understood.

**CRITICAL RULE:** Ask before starting: "Is this difficult because the code is bad, or because I lack the domain context?" Understand the code BEFORE deciding to refactor it.

#### Read the Code Thoroughly (Step 1)

1. **Internal Audit:**
   - What does this code actually do?
   - What is the intended responsibility?
   - What are the inputs, outputs, and side effects?
   - What depends on this code? What does it depend on?
   - What does the module currently own?

#### Problem Taxonomy (Step 1)

| Problem Type | Signal | Example |
| :--- | :--- | :--- |
| Mixed Responsibilities | One module doing multiple unrelated things | A function that validates input, queries DB, and sends email |
| Duplication | Same logic repeated across multiple locations | Identical auth check in many different places |
| Complexity | Deep nesting, long functions, unclear flow | 200-line function with 5 levels of nesting |
| Wrong Abstraction | Abstraction that makes code harder, not easier | Generic processor handling unrelated types via type switches |
| Naming Confusion | Names that mislead or do not match behavior | `handleUpdate` that also creates and deletes |
| Boundary Violation | Code reaching into modules it should not | Feature A directly querying Feature B's records |
| Dead Code | Code that is never executed | Functions with zero callers, unreachable branches |

#### Impact Assessment (Step 1)

1. **Quantify Drag:**
   - How does this structural problem affect development velocity?
   - How often does it cause bugs or confusion?
   - Does it block upcoming feature work?
   - Is this refactoring urgent or can it wait?

#### Decision Matrix (Step 1)

| Signal | Refactor | Rewrite / Strangler Fig |
| :--- | :--- | :--- |
| Business logic is correct, structure is messy | ✅ | |
| Fundamental design is wrong | | ✅ |
| Test coverage exists or can be added | ✅ | |
| No tests exist and behavior is undocumented | Caution ||
| Module is small and bounded | ✅ | |
| Module is large with deep dependencies || Consider Strangler Fig |

#### Output (Step 1)

```text
Refactor target: [exact files, classes, functions, or package area]
In scope: [list]
Out of scope: [list — even adjacent messy areas]

Specific problems: [list by type]
Impact: [how it affects development]
Decision: [refactor / rewrite / Strangler Fig]
```

#### Gate (Step 1)

If the module boundary is fuzzy, the refactor will likely sprawl. Define the exact boundary before proceeding.

---

### STEP 2 — LOCK BEHAVIOR WITH TESTS

**Mode:** Builder
**Goal:** Ensure current behavior is captured so refactoring cannot silently break it.

**This step is NON-NEGOTIABLE. Never refactor without test coverage.**

#### Coverage Audit (Step 2)

1. **Check Safeguards:**
   - What tests exist for this code?
   - Do they test behavior (good) or implementation details (fragile)?
   - Are there gaps in coverage for important behavior?
   - What behavior must continue to hold after refactoring?

#### Behavior Contract (Step 2)

1. **Define Constants:**
   - What inputs does this code accept?
   - What outputs does it produce for each input?
   - What side effects does it have?
   - What error behavior does it have?

These are the things that MUST NOT change during refactoring.

#### Characterization Tests (Step 2)

Characterization tests document CURRENT behavior — even quirky or unexpected behavior.

```typescript
// Characterization test — documenting current behavior
it('should return empty array when project has no tasks (not null)', () => {
  // This may or may not be the ideal behavior, but it is what
  // the code currently does and what consumers expect
  const result = getTasksForProject('empty-project');
  expect(result).toEqual([]);
});
```

#### Output (Step 2)

A test suite that locks current behavior. All tests must pass before any structural changes begin.

#### Gate (Step 2)

If tests cannot be written because the code is too tangled, make the code testable first. Do not refactor blind.

---

### STEP 3 — PLAN THE REFACTORING

**Mode:** Optimizer
**Goal:** Define exactly what will change, in what order, and with what strategy.

#### Scope Declaration (Step 3)

```text
What will change: [specific list]
What will NOT change: [specific list]
Behavior preserved: [specific list]
```

#### Selection Strategy (Step 3)

| Strategy | When to Use | How It Works |
| :--- | :--- | :--- |
| Extract | Logic is mixed together | Pull out focused functions, hooks, or modules |
| Rename | Names are misleading | Rename to reflect actual behavior |
| Inline | Abstraction adds no value | Remove wrapper, use implementation directly |
| Move | Code is in wrong location | Move to correct module per architecture |
| Simplify | Unnecessary complexity | Flatten nesting, remove dead branches |
| Decompose | Mixed responsibilities | Split into parts with clear ownership |
| Strangler Fig | Large module, high risk | Build replacement alongside old code |

#### Staging & Time-Boxing (Step 3)

1. **Sequence Steps:**
   - Order from lowest risk to highest risk
   - Each step should leave the code in a valid working state
   - Identify natural commit points
1. **Set Limits:**
   - Set a maximum time (hours) for the refactoring
   - Define what constitutes "good enough"

#### Output (Step 3)

```text
Primary refactor strategy: [choice and reason]
Staged plan:

  1. [step]
  2. [step]
Time box: [X hours]
Stop condition: [what constitutes done]
```

---

### STEP 4 — EXECUTE THE REFACTORING

**Mode:** Builder
**Goal:** Transform the code structure while preserving behavior.

**THE GOLDEN RULE: Run tests after EVERY change. Not at the end. After every single step.**

#### Transformation Workflow (Step 4)

1. **Iterative Change:**
   1. Make one refactoring move (extract, rename, move, or simplify)
   1. Run the full test suite
   1. If tests pass: commit
   1. If tests fail: revert and understand why before proceeding
   1. NEVER stack multiple refactoring steps before testing

#### Implementation Rules (Step 4)

1. **Adhere to Standards:**
   - Follow `coding-standards.md` conventions
   - Use domain terminology from `domain-rules.md` in new names
   - Avoid mixing unrelated redesign work into the refactor
   - Delete dead code mercilessly — git preserves history
   - Preserve public interfaces (exports) where possible

#### Gate (Step 4)

If work starts expanding into adjacent modules, re-bound immediately.

---

### STEP 5 — VERIFY

**Mode:** Reviewer
**Goal:** Confirm behavior is preserved and quality has genuinely improved.

#### Behavioral Integrity (Step 5)

1. **Run Full Suite:**
   - [ ] ALL characterization tests pass
   - [ ] ALL existing tests pass
   - [ ] Preserved interfaces match their pre-refactor contracts
   - [ ] Manual verification of key user flows

#### Structural Audit (Step 5)

1. **Verify Improvements:**
   - [ ] Problems from Step 1 are resolved
   - [ ] Code is more readable
   - [ ] Responsibilities are clearer
   - [ ] Duplication is reduced
   - [ ] Complexity is reduced (nesting, length)
   - [ ] Naming is accurate

#### Collateral Check (Step 5)

1. **Assess Impact:**
   - [ ] No unrelated code was changed
   - [ ] No new dependencies introduced
   - [ ] No flaky tests introduced

#### Gate (Step 5)

If the module is not meaningfully easier to work in, it may not have earned its cost.

---

### STEP 6 — DELIVER

**Mode:** Communicator
**Goal:** Communicate the refactoring result clearly.

#### Delivery Structure (Step 6)

```markdown

## Refactoring Summary

### What Was Refactored

[Module affected]

### Why

[Specific problems from Step 1]

### What Changed — Structure

[List of extractions, moves, renames, simplifications]

### What Did NOT Change — Behavior

[Explicit behavioral contracts preserved]

### Quality Improvements

- Before: [problem]
- After: [improvement]

### Remaining Debt

[What was NOT addressed and why]
```

---

## SCOPE CREEP PREVENTION

### Temptations vs Solutions

| Temptation | Danger | Solution |
| :--- | :--- | :--- |
| "While I am here..." | Expands scope, increases risk | Note it. Create a separate task. |
| "Secret Rewrite" | Architecture logic collapse | Stop. Assess if a rewrite is justified. |
| "New Feature Mixing" | High regression risk | Finish refactor first. Commit. Then start feature. |
| "Post-Cleanup Testing" | Invisible breakage | Run tests after every change. Non-negotiable. |
| "Adjacent-Debt magnetism" | Scope destruction | Capture it separately. |

---

## CHECKPOINTS AND QUALITY GATES

| Gate | Condition | Action |
| :--- | :--- | :--- |
| Gate 1 — Boundary unstable | Target keeps expanding | Re-bound immediately |
| Gate 2 — Behavior vague | Module responsibilities unclear | Clarify behavior first |
| Gate 3 — Safety nets weak | Verification insufficient for change size | Reduce scope or strengthen protection |
| Gate 4 — Structural leverage | Architecture-level problem exposed | Escalate broad issue explicitly |
| Gate 5 — Cosmetic only | Looks cleaner but friction unchanged | Refactor did not earn its cost |
| Gate 6 — Untestable | Code cannot be tested | Make testable first |

---

## WORKFLOW ANTI-PATTERNS

| Anti-Pattern | Why It Is Harmful | Workflow Prevention |
| :--- | :--- | :--- |
| Secret System Rewrite | Safety collapses; refactor never finishes | Keep boundary explicit; escalate broader issues |
| Cosmetic Only Churn | Churn rises but debt remains | Target the highest-friction structural problem |
| Interface Drift | Downstream consumers break silently | State interface stability requirements explicitly |
| Adjacent-Debt Magnetism | Risk expands beyond planned scope | Capture adjacent debt separately |
| Refactoring Without Tests | Regressions reached production | Run tests after every individual transformation |

---

## FAILURE MODES AND ESCALATION PATHS

| Failure Mode | What It Looks Like | Escalation |
| :--- | :--- | :--- |
| Not Bounded | Boundary is system-wide | Split work or escalate to architecture |
| Public Instability | Interface changes break many consumers | Stabilize interface or add better verification |
| Ownership Issues | Problems come from architecture | Escalate wider issue explicitly |
| No Test Entry | Cannot add tests without refactoring | Make testable first (Pass 1) |
| Rewrite Scale Drift | Scope grown to rewrite scale | Re-scope honestly or relabel effort |

---

## FINAL RULE

Refactor to make the next change cheaper, safer, and clearer — not merely to make today's diff look cleaner.

The test of a successful refactor is not whether the code looks better right now. It is whether the next engineer who needs to change this module finds it meaningfully easier to understand and modify than before.

---

## VERSION HISTORY

| Version | Date | Changes |
| :--- | :--- | :--- |
| Gold v1.1 | Initial | Established the systematic sequence for improving code structure without changing behavior |
