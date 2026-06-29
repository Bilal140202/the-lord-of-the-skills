# WORKFLOW: BUILD FEATURE (FULL SOURCE)

**Version:** Gold v1.1 (Master Merge)
**Layer:** 8 — Execution Workflow
**Tier:** 2 — Loaded by task
**File:** workflows/workflow-build-feature-SOURCE.md
**Primary Mode:** Builder
**Secondary Modes:** Architect, Security, Reviewer, Designer, Teacher
**Purpose:** The complete step-by-step sequence for building a new feature from initial request through to shipped, verified, production-quality code. Prevents coding before understanding, scope creep, architectural misplacement, and unverified delivery.
**Loaded When:** Building new functionality, adding a feature, implementing a new user capability, or creating a new module.
**Inherits From:** execution-workflow.md (universal process)

---

## WHAT THIS WORKFLOW DOES

This workflow transforms a feature request into shipped, production-quality code. It chains multiple operating modes and skill files together in the correct sequence, ensuring nothing is skipped.

Without this workflow, feature building tends to jump straight to coding — skipping problem definition, architecture, and verification. This workflow forces the right sequence every time.

---

## ACTIVATION

### Use When

- "Build this feature"
- "Add [capability] to the app"
- "Implement [functionality]"
- "Create a new [module / component / endpoint / page]"
- "What is the best way to build this?"
- "Give me the implementation plan"
- Any task that adds NEW functionality to the product

### Do NOT Use When

- Fixing a bug → use `workflow-debug-issue.md`
- Reviewing existing code → use `workflow-review-code.md`
- Refactoring without behavior change → use `workflow-refactor-module.md`
- Planning architecture without building → use `workflow-plan-architecture.md`
- Optimizing performance → use `workflow-optimize-performance.md`
- Pure research or option comparison without a build decision

If the task starts ambiguous, clarify whether the user wants architecture, implementation, review, or explanation before activating this workflow.

---

## REQUIRED FILES

### Core Files

- `core/anti-gravity-core.md`
- `core/system-thinking.md`
- `core/expert-cognitive-patterns.md`
- `core/operating-modes.md`
- `core/activation-engine.md`
- `core/execution-workflow.md`
- `core/conflict-resolution.md`
- `core/communication-standards.md`
- `core/quality-bar.md`

### Skills — Always Load

| Priority | Skill | Why |
| :--- | :--- | :--- |
| Primary | `skill-coding` | Implementation |
| Secondary | `skill-architecture` | Structure decisions |
| Secondary | `skill-testing` | Tests alongside code |

### Skills — Load When Relevant

| Condition | Skill | Why Relevant |
| :--- | :--- | :--- |
| Auth, input, or sensitive data involved | `skill-security` | Protection |
| Feature has a user interface | `skill-ui-ux` | Visuals |
| Feature involves API endpoints | `skill-api-design` | Contracts |
| Feature involves schema changes | `skill-database` | Data Persistence |
| Product problem is unclear | `skill-product-thinking` | Clarity |
| Option comparison needed | `skill-research-analysis` | Logic |
| Refactor required first | `skill-refactoring` | Maintenance |

### Contexts — Always Load

- `stack-context.md`
- `coding-standards.md`
- `architecture-context.md`
- `domain-rules.md`
- `project-context.md`

### Contexts — Load When Relevant

| Condition | Context | Purpose |
| :--- | :--- | :--- |
| UI work | `PRODUCT.md` (project root) | Strategic design context (register, brand, anti-references) |
| UI work | `DESIGN.md` (project root) | Visual system tokens (colors, typography, spacing, components) |
| UI work | `DESIGN.md` | Supplementary design patterns |
| Schema changes | `database-context.md` | Schema |
| API work | `api-conventions.md` | Endpoints |
| Auth or security surfaces | `security-baselines.md` | Safety |
| Prioritization decisions | `business-priorities.md` | Focus |
| Testing requirements | `testing-standards.md` | Quality |

---

## REQUIRED INPUTS

At minimum, Anti-Gravity should have or establish before proceeding:

- feature objective
- expected behavior
- relevant constraints
- target system area
- enough context to identify architectural fit

### If inputs are incomplete

Do NOT stop automatically. Instead:

1. Infer the minimum safe assumptions if risk is low
2. State those assumptions explicitly
3. Ask clarification only when missing information would materially change the build path

---

## EXECUTION SEQUENCE

---

### MANDATORY STOP-AND-VERIFY GATE

>
> **[CONTEXT AMNESIA FAILSAFE]**
> Do NOT proceed to Step 1 until you have SILENTLY verified that all required context files and skill files have been read using tool calls.

### STEP 0 — WORKSPACE ISOLATION (MANDATORY)

**Goal:** Create a clean, isolated workspace before writing any implementation code.

Before writing any implementation code:

1. Create a new git branch from the current clean state:
   `git checkout -b feature/<short-name>`
   Or, if the IDE supports it, create a git worktree:
   `git worktree add ../feature-<short-name> -b feature/<short-name>`

2. Run the project's test suite / build command to verify a clean baseline.
   If the baseline is red (pre-existing failures), STOP and report to the user.
   Do NOT proceed with implementation on a broken baseline unless the user explicitly overrides.

3. All implementation work happens on this branch/worktree.
   The main working tree stays untouched until merge.

This step is non-negotiable. If the adapter or environment does not support
worktrees, use a standard branch. If git is not initialized, initialize it first.

---

### STEP 1 — DEFINE THE FEATURE OBJECTIVE

**Goal:** Understand what is actually being built and why before building anything.

#### Load Template (Step 1)

- [REQUIRED] Load [feature-plan.md]({{GLOBAL_CONFIG_URI}}/global_templates/feature-plan.md)
- Follow the structure and guidance in the template to scope and plan the feature before implementation.

#### Action: Define Objective (Step 1)

1. Restate the feature in plain, practical terms
2. Separate the requested solution from the underlying user or system need
3. Identify the Job-to-be-Done:
   > "When [situation], the user wants to [motivation] so they
   > can [expected outcome]"

4. Define the success metric:
   > "We will know this worked when [measurable behavior] changes"

5. Identify the riskiest assumption — the thing that, if wrong, invalidates the effort
6. Identify whether this is user-facing, internal, operational, or infrastructure-facing

#### Output: Objective statement (Step 1)

A short objective statement:

```text
We are building X so that Y user/system can achieve Z outcome.
Success looks like: [measurable condition].
```

#### Gate: Objective Clarity

If the feature objective is still vague, clarify or set explicit assumptions before proceeding. Do NOT start architecture or coding against an unclear objective.

Ask if needed: "What specific user problem does this solve?"

---

### STEP 2 — GROUND THE FEATURE IN CONTEXT

**Goal:** Place the feature inside the existing project, stack, and architecture reality. Prevent implementing in the wrong layer.

#### Action: Establish Context (Step 2)

1. Load relevant context files
2. Identify where in the current system this feature belongs
3. Identify the correct layer, module, or component for the change
4. Check domain rules and permission constraints that apply
5. Identify adjacent components, services, or flows affected
6. Identify project-level constraints that shape the build
7. Note whether the feature touches security, performance, data, or UX-sensitive surfaces
8. **CHECK MEMORY (MANDATORY — workspace first, then global):**
   - Scan `.agents/memory/decisions-log.md` then `antigravity/memory/decisions-log.md` — has a related decision been made before?
   - Scan `.agents/memory/common-patterns.md` then `antigravity/memory/common-patterns.md` — does a proven pattern exist?
   - Scan `.agents/memory/mistakes-to-avoid.md` then `antigravity/memory/mistakes-to-avoid.md` — have we hit traps in this area?

#### Output: Context Frame (Step 2)

A short context frame:

- placement in system
- relevant constraints
- known dependencies
- local standards that apply

#### Gate: Context Alignment

If the feature cannot be placed cleanly into the current system, escalate briefly to architectural clarification before continuing.

---

### STEP 3 — DEFINE SCOPE AND NON-GOALS

**Goal:** Prevent feature sprawl. Clarify what is included versus excluded before a single line is written.

#### Action: Control Scope (Step 3)

1. Define the minimum feature scope that satisfies the objective
2. Identify explicit non-goals
3. Separate core path from optional or future enhancements
4. Identify the smallest version that still delivers core value
5. Decide whether the work should be split into phases or stages
6. Make tradeoffs explicit — reduce scope before reducing quality

#### Output: Scope Definition (Step 3)

```text
In scope:

- [item]
- [item]

Out of scope (deferred):

- [item]
- [item]

```

#### Gate: Scope Locking

If the feature keeps expanding during planning, split the work instead of silently absorbing more requirements. Do NOT proceed with an unbounded scope.

---

### STEP 4 — IDENTIFY RISKS, DEPENDENCIES, AND ASSUMPTIONS

**Goal:** Make visible what could complicate or invalidate the build before implementation begins.

#### Action: Identify Risks (Step 4)

1. Identify technical dependencies
2. Identify data, API, UI, security, or rollout dependencies
3. Identify assumptions the implementation depends on
4. Identify major risks:
   - compatibility
   - migration
   - performance
   - trust boundary
   - rollback risk
5. If risks are high and reversibility is low, deepen the planning and verification steps rather than rushing execution

#### Output: Risk Log (Step 4)

A short dependency, assumption, and risk list.

#### Gate: Risk Awareness

High-risk, low-reversibility features require stronger verification planning at Step 6 before proceeding.

---

### STEP 5 — DESIGN THE IMPLEMENTATION SHAPE

**Goal:** Make structural decisions before writing implementation code.

#### Action: Design Shape (Step 5)

1. **Check existing architecture:**
   - Does this fit an existing module or need a new one?
   - Which feature directory does this belong in?
   - Are there existing patterns to follow?

2. **Define the data model** (if new data is involved):
   - What entities are created or modified?
   - What are the relationships?
   - Does the schema need migration?
   - Check `database-context.md` for conventions

3. **Define the API** (if new endpoints needed):
   - What endpoints are created?
   - Request and response shapes?
   - Check `api-conventions.md` for format

4. **Define the component structure** (if UI involved):
   - What components are needed?
   - What states must be handled: loading, empty, error, success?
   - Check `DESIGN.md` for available components

5. **Identify security considerations:**
   - Does this touch auth, user input, or sensitive data?
   - What authorization checks are needed?
   - Check `security-baselines.md` if applicable

6. **Define the implementation sequence:**
   - What should be built first?
   - What depends on what?
   - What can be built independently?

7. Keep outer layers thin and business logic explicit
8. Avoid speculative abstraction

#### Output: Architecture Shape (Step 5)

```text
Implementation shape:

- UI component / endpoint / service / repository / migration
- Main state and side-effect boundaries
- Data flow and interaction points
- Implementation order

```

#### Gate: Structural Fit

If the implementation shape is fighting the existing architecture, pause and adjust before coding. If the feature is complex enough, ask: "Want me to document this as an ADR before proceeding?"

---

### STEP 6 — DEFINE VERIFICATION STRATEGY BEFORE CODING

**Goal:** Know how success and safety will be verified before implementation begins. Not after.

#### Action: Plan Verification (Step 6)

1. Identify what should be tested and at what level
2. Identify critical edge cases and failure paths
3. Define manual or observational verification if needed
4. Decide what instrumentation or logging is necessary for confidence
5. Identify analytics or success-signal instrumentation if adoption tracking matters

#### Output: Verification Plan (Step 6)

```text
Verification plan:

- Test targets: [list]
- Critical edge cases: [list]
- Failure paths: [list]
- Confidence gaps: [list]
- Runtime signals if relevant: [list]

```

#### Gate: Verifiability

If there is no credible verification path, reduce scope or redesign before building. Do NOT implement a feature you cannot verify.

---

### MICRO-TASK RULE (MANDATORY)

Every implementation plan produced at Step 5/6 MUST be broken into tasks that take 2-5 minutes each.

Each task must specify:

- **Exact files** to create or modify
- **The specific change** (what code to write, what to add/remove)
- **Verification command** (test to run, build to check, output to confirm)
- **Completion evidence** (what "done" looks like — a passing test, a screenshot, a log line)

Tasks that are vague ("set up the component"), unbounded ("implement the feature"),
or missing verification steps are rejected. Rewrite them.

Why: Smaller tasks reduce hallucination, make rollbacks trivial, and give the user
constant progress visibility.

#### Automatic Dispatch Trigger

If the resulting micro-task list has MORE THAN 3 tasks, you MUST proactively offer to use the Task Dispatch workflow.

State to the user:
> "We have [N] tasks here. To protect our context window and prevent hallucination, I recommend we dispatch the isolated tasks (like [Task X] and [Task Y]) to separate chat windows using `/workflow-task-dispatch`. Should I generate the Task Briefs for you?"

Do NOT automatically start executing a massive sequence without offering this choice.

---

### STEP 7 — IMPLEMENT

**Goal:** Build the feature cleanly, correctly, and in the right mode.

Load `skill-coding` and follow its behavioral workflow.

#### Stage: 7a — Database Layer

1. Update schema following `database-context.md` conventions
2. Create migration
3. Write query functions in `features/[feature]/queries/`
4. Add indexes for expected access patterns

#### Stage: 7b — Server Layer

1. Define Zod validation schema in `features/[feature]/schemas/`
2. Implement Server Action or API route
3. Follow the pattern:
   **Validate → Authenticate → Authorize → Execute → Return Result**

4. Handle all error paths — never just the happy path
5. Follow `coding-standards.md` conventions

#### Stage: 7c — Client Layer (Impeccable Design Authority)

> [!IMPORTANT]
> **All UI work goes through Impeccable.** Studio-grade quality is the default standard, not an upgrade. Load `skill-ui-ux` and follow the Impeccable lifecycle.

1. **Load design context:** Read `PRODUCT.md` (strategic) and `DESIGN.md` (visual tokens) from the project root. These are the design truth files created during Project Inception Phase 3A.
2. **Run `/impeccable-craft`** for the full UI build loop:
   - **Shape:** Creates a task-specific design brief (discovery, visual probes, confirmed scope)
   - **Mock:** Generates visual direction for confirmation
   - **Build:** Implements production-quality components
   - **Verify:** Browser inspection and critique-and-fix loop
3. Build components in `features/[feature]/components/`
4. Create data hooks in `features/[feature]/hooks/`
5. Follow `DESIGN.md` tokens for all color, typography, spacing, and component styling
6. Handle ALL states: loading, empty, error, success, partial, disabled
7. Implement optimistic updates where appropriate
8. Apply `motion` (Framer Motion) for all Type B animations per the animation mapping

**After the craft build loop completes,** evaluate whether a refinement pass is needed:
- Feels weak or generic? → `/impeccable-bolder`
- Feels static or lifeless? → `/impeccable-animate`
- Too cluttered? → `/impeccable-distill`
- Final production polish? → `/impeccable-polish`

#### Stage: 7d — Testing

1. Follow `testing-standards.md`
2. Server Actions: integration tests covering validation, auth, happy path, and error paths
3. Business logic: unit tests covering calculations, transformations, state transitions
4. Components: test user-visible behavior, not implementation details
5. DO NOT defer tests to later — they ship with the code

#### Implementation Rules

- Do not silently widen scope during implementation
- Do not redesign unrelated systems
- Do not skip validation or error paths in sensitive areas
- Keep changes coherent and reviewable
- Preserve consistency with surrounding code and project standards
- Avoid unrelated cleanup unless it materially reduces risk

#### Gate: Implementation Integrity

Code must pass the `skill-coding` Non-Negotiable Checklist before proceeding to self-review. If complexity is growing unexpectedly, stop and reassess scope or structure.

---

### STEP 8 — SELF-REVIEW

**Goal:** Catch issues before they reach another reviewer or production.

Load `skill-review-audit` and evaluate against:

1. **Correctness:** Does it actually solve the defined problem?
2. **Edge cases:** What happens with empty, null, malformed, or extreme inputs?
3. **Error handling:** Are all failure paths handled? Any silent failures?
4. **Security:** Input validated? Auth checked? Secrets managed correctly?
5. **Conventions:** Does it follow `coding-standards.md`? Match surrounding code?
6. **Naming:** Descriptive and consistent with domain terminology?
7. **Complexity:** Is there a simpler version that works? Any premature abstraction?
8. **Tests:** Are the right behaviors tested? Missing edge cases?
9. **Performance:** Any N+1 queries, unnecessary re-renders, or expensive operations?
10. **Accessibility:** (if UI) Keyboard navigable? Screen reader friendly? Color contrast?

Also ask:

- Is this too broad?
- Is this over-engineered?
- Is the feature in the right place architecturally?
- Did implementation quality get sacrificed for speed?
- What future risk or debt was introduced?

#### Output: Self-Correction List

List any issues found and fix them before delivery.

---

### STEP 9 — VERIFY BEHAVIOR AND REGRESSION RISK

**Goal:** Ensure the feature works and does not silently damage adjacent behavior.

#### Action: Verify Behavior (Step 9)

1. Verify the primary success path against acceptance criteria
2. Verify critical edge and failure cases
3. Check regressions in nearby behavior
4. Confirm instrumentation or observability signals if applicable
5. Note what is verified versus not yet verified

#### Output: Verification Status (Step 9)

```text
Verified:

- [item]
- [item]

Not yet verified:

- [item]

```

#### Gate: Readiness

Do NOT call the feature done because the happy path worked once. Adjacent behavior, failure paths, and rollout risk all count.

#### Verification Evidence Gate (MANDATORY)

No task or workflow can be declared complete without verification evidence.

Acceptable evidence (at least one required):

- A test that was red, then green after the change
- A build/lint command that passes
- A command output showing the expected behavior
- A screenshot or log demonstrating the fix
- A structural verification trace (data flow from origin to consumer)

"I believe it works" is NOT evidence. "It should work" is NOT evidence.
Run the verification. Show the output. Then declare done.

---

### STEP 9A — MERGE REVIEW GATE (MANDATORY)

**Goal:** Two-stage self-review before branch finalization or task sequence completion.

#### Stage 1: Spec Compliance

- Does the implementation match what was asked for?
- Are there missing requirements?
- Is there scope creep (things built that weren't requested)?

#### Stage 2: Code Quality

- Error handling on foreseeable failures?
- Security basics addressed?
- Naming and patterns consistent with project standards?
- No dead code, no commented-out blocks, no TODOs without tickets?

If either stage has blocking issues, fix them before declaring complete.
Report the review results to the user with a summary.

---

### STEP 10 — DELIVER

**Goal:** Present the work clearly with context and rationale so it is understandable, reviewable, and ready for handoff.

#### Delivery Structure

```text

## What Was Built

[1-2 sentence summary of the feature]

## Approach

[Brief description of approach and key decisions]

## Files Changed

[List of files created or modified]

## Key Decisions

[Non-obvious decisions and why they were made]

## Assumptions

[Anything assumed that the user should verify]

## What to Test

[How to verify the feature works — manual testing steps]

## What to Watch

[Risks, edge cases, or things to monitor after deployment]

## Deferred Scope

[Items explicitly moved to Phase 2 or future work]

## Next Steps

[Follow-up work or rollout considerations]
```

#### Communication Rules

- Explain non-obvious decisions
- Do not bury assumptions
- Keep the user clear on what was built versus deferred
- State tradeoffs explicitly — do not hide costs

---

### STEP 11 — POST-SHIP & MEMORY CAPTURE (MANDATORY)

**Goal:** Lock in what was learned. Without this step, every session starts from zero.

1. Verify the feature works in staging or production
2. Check error monitoring for new errors introduced
3. If instrumented: check analytics for adoption signals
4. Update relevant context files if conventions or patterns changed

#### Memory Capture Checklist (MANDATORY — do not skip)

Ask these 4 questions before closing. Write to **workspace memory** (`.agents/memory/`) for project-specific entries. Write to **global memory** (`antigravity/memory/`) ONLY for cross-project lessons (tooling, process, AI config).

- [ ] **Decisions:** Were any Type 1/1.5 architectural or technology decisions made? → Log to `.agents/memory/decisions-log.md`
- [ ] **Patterns:** Did a reusable solution pattern emerge that applies beyond this feature? → Log to `.agents/memory/common-patterns.md`
- [ ] **Mistakes:** Did any bug, misstep, or wrong path cost real time to fix? → Log to `.agents/memory/mistakes-to-avoid.md`
- [ ] **Postmortem:** Did anything break in a way that revealed a systemic weakness? → Log to `.agents/memory/postmortems.md`

If workspace memory files do not exist, create them (copy format from global templates).
If ALL 4 answers are "no," state: "No memory entries needed — session was routine."
If ANY answer is "yes," write the entry NOW before closing. Do not defer.

---

## SCOPE MANAGEMENT RULES

### When scope starts growing during implementation

1. Stop coding
2. Refer back to Step 3 scope boundary
3. Ask explicitly:
   > "This is growing beyond the defined scope. The new item is
   > [X]. Should I: (a) add it to this feature, (b) defer it to
   > Phase 2, or (c) skip it entirely?"

4. Do NOT silently expand scope

### When requirements are discovered during implementation

1. Document the discovery
2. If it affects the architecture from Step 5, STOP and revisit
3. If it is an edge case, handle it and add a test
4. If it is a new feature, defer to Phase 2

---

## CHECKPOINTS AND QUALITY GATES

| Gate | Condition | Action |
| :--- | :--- | :--- |
| Gate 1 — Objective ambiguity | Feature objective unclear enough that build paths diverge | Pause for clarification or explicit assumptions |
| Gate 2 — Scope inflation | Feature keeps expanding during planning | Split the work before continuing |
| Gate 3 — Architecture mismatch | Feature does not fit cleanly into current system | Resolve placement before coding |
| Gate 4 — No verification path | Feature cannot be validated credibly | Reduce risk or redesign before building |
| Gate 5 — Hidden rollout risk | Deployment or migration risk is meaningful | Add rollback and staged rollout thinking |

---

## QUALITY GATE CHECKLIST

Before marking a feature complete:

- [ ] Problem clearly defined with success metric
- [ ] Architecture reviewed and documented even briefly
- [ ] Scope locked with explicit non-goals
- [ ] Risks and assumptions made visible
- [ ] Code follows `coding-standards.md`
- [ ] All foreseeable error paths handled
- [ ] Tests written and passing
- [ ] Security considerations addressed if applicable
- [ ] Accessibility verified if UI
- [ ] Self-review completed against `skill-review-audit` checklist
- [ ] No commented-out code, debug statements, or unused imports
- [ ] Delivery summary written with assumptions and next steps
- [ ] Adjacent behavior checked for regression

---

## FAILURE MODES AND ESCALATION PATHS

| Failure Mode | What It Looks Like | Escalation |
| :--- | :--- | :--- |
| Feature is actually an architecture problem | Build cannot proceed without structural decisions | Escalate to architecture planning, then return |
| Feature is actually a research question | Core issue is option evaluation, not implementation | Switch to `skill-research-analysis.md` |
| Feature reveals blocking technical debt | Debt makes safe delivery impossible | Load `skill-refactoring.md`, decide whether to refactor first or isolate |
| Feature touches critical security or data boundaries | Auth, trust boundary, or sensitive data at risk | Load security and database skills, strengthen risk handling |
| Feature is program-sized, not feature-sized | Scope is too large for a single feature workflow | Split into multiple features or a planning workflow |

---

## WORKFLOW ANTI-PATTERNS

### Coding Before Scope

**What it looks like:** Starting implementation before deciding what is in scope and what is out.

**Why it is harmful:** The feature quietly expands and becomes harder to verify or review.

**Instruction:** Lock scope and non-goals before implementation.

### Happy-Path Completion Illusion

**What it looks like:** Declaring the feature done because the main path appears to work once.

**Why it is harmful:** Regressions, edge cases, and rollout risks remain hidden.

**Instruction:** Verify primary path, failure paths, and adjacent behavior deliberately.

### Architecture by Accident

**What it looks like:** Choosing where feature logic lives based on convenience in the moment rather than structure.

**Why it is harmful:** Local hacks become long-term system shape.

**Instruction:** Choose implementation placement intentionally at Step 5.

### Scope Creep Under Good Intentions

**What it looks like:** Repeatedly adding small extras because they seem helpful.

**Why it is harmful:** The feature becomes larger, riskier, and less coherent than planned.

**Instruction:** Record extras as future work unless they are truly necessary for the core outcome.

### Solving the Wrong Problem

**What it looks like:** Implementing the requested shape perfectly while missing the actual user need.

**Why it is harmful:** The feature ships and does not move the metric.

**Instruction:** Separate solution from need at Step 1.

### Silent Scope Expansion

**What it looks like:** Scope growing during implementation without explicit team awareness.

**Why it is harmful:** Reviews, estimates, and trust all break.

**Instruction:** Surface scope changes explicitly and get a decision before continuing.

---

## RECOVERY RECIPES

> When something goes wrong mid-workflow, DO NOT improvise. Check this section first.

### Build Fails After Code Changes

```

1. Check the EXACT error message — read it fully, don't skim
2. Check if the error is in YOUR changed files or in a dependency
3. If syntax error → fix in place, do not restructure
4. If import/require error → verify the module path exists and is spelled correctly
5. If type error → check that function signatures match their callers
6. Scan memory/mistakes-to-avoid.md for matching patterns
7. If the error makes no sense → revert last change, rebuild, confirm clean state, re-apply incrementally
```

### Tests Fail After Implementation

```

1. Run the SINGLE failing test in isolation — is it the test or the code?
2. Check if the test was written against OLD behavior that your feature intentionally changed
3. If the test assumptions are stale → update the test to match new behavior
4. If the test catches a real bug → fix the code, not the test
5. Check for race conditions if tests pass sometimes and fail other times
6. Never delete a failing test to "fix" the problem
```

### Session Interrupted Mid-Workflow

```

1. Read task.md for current phase and completed steps
2. Announce: "Resuming [workflow] from Phase [N] — [phase name]"
3. Re-load the context and skill files listed in the workflow header
4. Check the task.md notes and key pending items
5. Resume from the START of the interrupted phase (not the middle)
6. Do NOT restart the entire workflow from Phase 1
```

### Feature Scope Keeps Growing

```

1. STOP coding immediately
2. Return to Step 3 (Scope Definition)
3. List the new items that appeared
4. Ask: "These items appeared during implementation: [list]. Should I: (a) include now, (b) defer to Phase 2, or (c) skip?"
5. Update the scope definition before continuing
6. Do NOT silently absorb new requirements
```

### Architecture Doesn't Fit

```

1. STOP before forcing the code into the wrong place
2. Return to Step 5 (Design Shape)
3. Identify WHY it doesn't fit — wrong layer? wrong module? missing abstraction?
4. Check architecture-context.md for guidance
5. If the issue is structural → escalate to /workflow-plan-architecture
6. If the issue is small → adjust placement, document the reason
```

### Context Files Are Empty

```

1. Announce: "Context file [filename] is empty — I'm working without project-specific guidance"
2. Ask: "Do you want me to populate [filename] based on what I know about your project?"
3. If yes → fill it now, then resume the workflow
4. If no → proceed with explicit generic assumptions, state them clearly
5. NEVER silently default to generic advice when a context file exists but is empty
```

---

## WORKFLOW STATE TRACKING

This workflow integrates with `task.md`.

**On activation:** Check `task.md` for existing state or create a new checklist.
**After each step:** Update `task.md` with current phase, status, and notes.
**On interruption:** State file preserves progress for next session.

Phase map for state tracking:

```
1_define_objective → 2_ground_context → 3_define_scope → 4_identify_risks →
5_design_shape → 6_verification_plan → 7_implement → 8_self_review →
9_verify → 10_deliver → 11_post_ship
```

---

## SUCCESS STANDARD

This workflow succeeds when:

- a feature solves the intended problem
- scope is controlled and explicit
- architectural fit is preserved
- risks are visible before implementation
- verification is clear and complete
- the implementation is maintainable and coherent
- the user understands what was built and what remains

---

## FINAL RULE

Build the smallest correct feature in the right place, with clear behavior and visible verification — not the broadest or flashiest implementation.

When in doubt, reduce scope before reducing quality.
