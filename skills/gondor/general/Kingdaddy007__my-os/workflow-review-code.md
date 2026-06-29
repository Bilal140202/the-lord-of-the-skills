# WORKFLOW: REVIEW CODE (FULL SOURCE)

**Version:** Gold v1.1 (Master Merge)
**Layer:** 8 — Execution Workflow
**Tier:** 2 — Loaded by task
**File:** workflows/workflow-review-code-SOURCE.md
**Primary Mode:** Reviewer
**Secondary Modes:** Security, Architect, Performance, Builder
**Purpose:** The systematic sequence for reviewing code — evaluating correctness, security, maintainability, and quality against project standards. Transforms code review from subjective "looks good to me" into structured evaluation with prioritized findings.
**Loaded When:** Reviewing a PR, auditing existing code, self-reviewing before delivery, or evaluating code quality of a module.
**Inherits From:** execution-workflow.md (universal process)

---

## WHAT THIS WORKFLOW DOES

This workflow ensures reviews catch what matters — logic flaws, security issues, missing edge cases — and do not waste time on what does not, such as style preferences that should be automated.

Without this workflow, reviews either rubber-stamp code with a quick approval, or bikeshed on formatting while missing critical bugs.

---

## ACTIVATION

### Use When

- "Review this code"
- "Check this PR"
- "Audit this module"
- "Is this code good?"
- "What is wrong with this?"
- "Should this be approved?"
- Self-review before delivering your own code
- Evaluating code quality of an existing codebase section

### Do NOT Use When

- Fixing a specific bug → use `workflow-debug-issue.md`
- Building new code → use `workflow-build-feature.md`
- Refactoring for improvement → use `workflow-refactor-module.md`
- Performance optimization → use `workflow-optimize-performance.md`
- Designing a system from scratch with no artifact to review
- Open-ended technology comparison with no concrete implementation

---

## REQUIRED FILES

### Skills — Always Load

| Priority | Skill | Why |
| :--- | :--- | :--- |
| Primary | `skill-review-audit` | Review methodology and severity classification |
| Secondary | `skill-security` | Security is checked on EVERY review without exception |

### Skills — Load When Relevant

| Condition | Skill |
| :--- | :--- |
| Code involves data processing, queries, or rendering | `skill-performance` |
| Code involves structural decisions or module boundaries | `skill-architecture` |
| Evaluating test quality alongside code | `skill-testing` |
| Deep structural debt found | `skill-refactoring` |

### Contexts — Always Load

- `coding-standards.md`
- `stack-context.md`
- `architecture-context.md`
- `domain-rules.md`

### Contexts — Load When Relevant

| Condition | Context |
| :--- | :--- |
| Auth, input, or security code | `security-baselines.md` |
| Business logic | `domain-rules.md` |
| Test quality being evaluated | `testing-standards.md` |
| UI components being reviewed | `DESIGN.md` |
| API changes | `api-conventions.md` |
| Database changes | `database-context.md` |

---

## REQUIRED INPUTS

At minimum, Anti-Gravity should have or establish before proceeding:

- the code, diff, patch, or implementation artifact to review
- a stated or inferable objective for the change
- enough project context to understand where the change fits

### Strongly preferred inputs

- linked requirement, ticket, or problem statement
- tests or verification evidence accompanying the change
- known constraints such as security, compatibility, or rollout risk
- surrounding architecture assumptions

### If inputs are incomplete

Do NOT immediately review line-by-line in a vacuum. Instead:

1. Infer the likely intent from the change shape
2. State the missing context explicitly
3. Review with appropriately calibrated confidence
4. Ask clarification only when missing context would materially change severity or approval judgment

---

## EXECUTION SEQUENCE

---

### STEP 1 — UNDERSTAND THE CHANGE

**Mode:** Reviewer
**Goal:** Understand what the code is supposed to do before evaluating how it does it. Never judge implementation before understanding intent.

#### Actions (Step 1)

1. **Read context first — not the code:**
   - What is the stated purpose of this change?
   - What user or system problem does it solve?
   - What approach was chosen?
   - Are there linked requirements, tickets, or design docs?
   - Is this feature work, a bug fix, a refactor, an optimization, hardening, or cleanup?

1. **Assess the scope:**
   - How many files changed?
   - Is this a focused change or does it touch many areas?
   - If more than 400 lines: flag it

1. **Identify risk level:**

| Risk Signal | Implication |
| :--- | :--- |
| Touches auth, permissions, or session handling | Security review is mandatory |
| Modifies database schema | Check migration safety and backward compatibility |
| Changes shared utilities used by many features | High blast radius — extra scrutiny |
| Adds new dependencies | Check maintenance, license, bundle size, alternatives |
| Modifies financial or payment logic | Highest scrutiny — verify all calculations |
| Simple copy change or typo fix | Low risk — lightweight review |

1. **Identify critical paths and blast radius:**
   - What critical paths does the change touch?
   - What data integrity, auth, state, financial, or user-critical surfaces are affected?
   - Estimate the blast radius if the change is wrong

#### Output (Step 1)

```text
This change [does X] to solve [Y].
Risk level: [low / medium / high]
Critical areas touched: [list]
Blast radius if wrong: [description]
Focus areas: [specific concerns]
```

#### Gate (Step 1)

If the intent is ambiguous enough that severity would change depending on interpretation, note the ambiguity before proceeding. Do not spend equal effort everywhere — focus hardest where failure would matter most.

---

### STEP 2 — CHECK AUTOMATED GATES

**Mode:** Reviewer
**Goal:** Confirm automated checks have passed before investing human review time. If automated checks fail, stop and ask for fixes first.

#### CI Pipeline Checks (Step 2)

- [ ] Type checking passes
- [ ] Linting passes
- [ ] Tests pass
- [ ] Build succeeds

#### Automated Quality Checks (Step 2)

- [ ] No new untyped values introduced without justification
- [ ] No suppressed type errors in production code without comment
- [ ] No disabled linting rules without justification
- [ ] Lock file changes are consistent with dependency changes

#### Gate (Step 2)

If any automated check fails: stop review and request fixes before continuing. Human review time should not be spent on work that automated systems already rejected.

---

### STEP 3 — REVIEW FOR CORRECTNESS

**Mode:** Reviewer
**Goal:** Does this code actually do what it claims under real conditions?

**This is the highest-priority review dimension. Do not get distracted by minor style issues while core correctness remains uncertain.**

#### Actions (Step 3)

1. **Logic verification:**
   - Trace the primary code path end-to-end
   - Does the logic match the stated intent?
   - Are conditionals correct? Watch for inverted conditions, off-by-one errors, and wrong operators
   - Are loops bounded? Can they infinite loop?
   - Does the change solve the real problem or a narrower symptom?

2. **Edge case analysis:**
   - What happens with null, undefined, empty inputs?
   - What happens with extremely large inputs?
   - What happens with malformed data?
   - What happens with concurrent requests?
   - What happens if external dependencies fail?
   - Are state transitions and lifecycle edges handled?

3. **State management:**
   - Are state changes intentional and visible?
   - Could state become inconsistent?
   - Are race conditions possible?

4. **Data integrity:**
   - Are database operations in transactions where needed?
   - Could partial failures leave data in an inconsistent state?
   - Are soft-delete filters applied to queries?

#### Output (Step 3)

A correctness assessment with identified concerns or confidence level.

#### Gate (Step 3)

Correctness uncertainty takes priority over all other review concerns. Do not allow style or preference discussions to dominate while correctness is unresolved.

---

### STEP 4 — REVIEW FOR SECURITY

**Mode:** Security
**Goal:** Identify security vulnerabilities.

### This step is NEVER skipped — not even for small changes

#### Input Validation (Step 4)

- [ ] All user input validated server-side
- [ ] Client-side validation present but NOT trusted for security
- [ ] File uploads validated for type, size, and content

#### Authentication and Authorization (Step 4)

- [ ] Protected endpoints check authentication
- [ ] Authorization checked for the specific resource and action
- [ ] Role-based permissions match `security-baselines.md`
- [ ] No authorization bypass paths exist

#### Data Exposure (Step 4)

- [ ] Sensitive data not logged — passwords, tokens, PII
- [ ] API responses do not leak internal data
- [ ] Error messages do not expose stack traces or internal details
- [ ] Secrets are not hardcoded or committed

#### Injection Prevention (Step 4)

- [ ] SQL queries parameterized — check raw queries specifically
- [ ] User-generated HTML sanitized before rendering
- [ ] No unsafe dynamic evaluation patterns

#### Gate (Step 4)

If a security, data, or critical runtime path is changed without adequate verification, escalate the severity of the finding. Do not soften security findings to avoid conflict.

---

### STEP 5 — REVIEW FOR MAINTAINABILITY

**Mode:** Reviewer
**Goal:** Will this code be understandable and changeable by someone else in six months?

#### Readability (Step 5)

- Can a developer unfamiliar with this code understand it immediately?
- Are names descriptive and consistent with domain terminology from `domain-rules.md`?
- Is complex logic explained with comments that explain WHY, not just WHAT?
- Are functions focused on one responsibility?

#### Convention Compliance (Step 5)

- Does this follow `coding-standards.md`?
- Does it match patterns in `architecture-context.md`?
- Are imports, exports, and file placement correct?
- If new patterns are introduced, are they justified and documented?

#### Complexity Assessment (Step 5)

- Is there a simpler version that achieves the same result?
- Are there unnecessary abstractions?
- Are there deeply nested conditions that could be flattened?
- Are functions too long? More than 30 lines is a signal, not a hard rule.

#### Test Quality (Step 5)

- Do tests verify behavior, not implementation details?
- Are edge cases covered?
- Are tests independent with no shared mutable state?
- Are test names descriptive using "should [behavior] when [condition]" format?
- Is the most important behavior actually covered, not just present?
- Are there happy-path-only gaps?

#### Gate (Step 5)

A change can be functionally correct and still structurally harmful. Do not confuse one with the other. Passing weak tests is not the same as strong evidence.

---

### STEP 6 — REVIEW FOR ARCHITECTURE

**Mode:** Architect
**Goal:** Does this change fit the system structure?

Only apply this step in depth when the change affects system structure.

#### Module Boundaries (Step 6)

- Does this respect module ownership rules?
- Does it create cross-module dependencies that should not exist?
- Is new code placed in the correct directory and layer?

#### Dependency Direction (Step 6)

- Do dependencies flow in the correct direction?
- Does any shared code import from feature-specific code?
- Are new external dependencies justified by the problem they solve?

#### Patterns (Step 6)

- Does this follow existing patterns?
- If a new pattern is introduced, is it documented and justified?
- Could this pattern be reused, or is it a one-off?

#### Gate (Step 6)

If the review reveals significant structural debt, load `skill-refactoring.md` and distinguish immediate fixes from deeper cleanup work before finalizing findings.

---

### STEP 7 — CLASSIFY AND VALIDATE FINDINGS

**Mode:** Reviewer
**Goal:** Turn raw observations into review-ready judgment. Ensure findings are fair, defensible, and not inflated by personal preference.

#### Finding Severity Model (Step 7)

| Severity | Definition | Blocks Merge? |
| :--- | :--- | :--- |
| 🔴 Critical | Logic error, security vulnerability, data corruption risk, broken functionality | YES |
| 🟠 High | Missing error handling, architectural violation, significant unhandled edge case | YES unless explicitly accepted |
| 🟡 Medium | Readability issue, naming improvement, missing test, minor convention violation | NO |
| 🟢 Low | Style suggestion, alternative approach, minor improvement | NO |
| 💬 Note | Question, observation, or teaching moment — not a defect claim | NO |

#### Validation Check (Step 7)

Before finalizing findings, verify:

- Are findings evidence-based, specific, relevant, and actionable?
- Did the review overfocus on taste over impact?
- Were major risks missed while reviewing minor style points?
- Are preferences being presented as critical defects?
- Is severity calibrated to actual risk, not emotional annoyance?

#### Approval Decision (Step 7)

- **Approve as-is** — no blocking issues found
- **Approve with caveats** — minor issues noted, not blocking
- **Request revision** — must-fix issues identified
- **Block** — critical issues that cannot be deferred

State the minimum changes needed for approval when not ready. Do not leave the author guessing whether a finding is blocking or advisory.

---

### STEP 8 — DELIVER REVIEW

**Mode:** Communicator
**Goal:** Present findings clearly with rationale so the next action is obvious.

#### Load Template (Step 8)

- [REQUIRED] Load [code-review-report.md]({{GLOBAL_CONFIG_URI}}/global_templates/code-review-report.md)
- Follow the structure and guidance in the template exactly to deliver the code review findings.

#### Tone Rules (Step 8)

Phrase feedback as suggestions, not commands:

- ✅ "What do you think about naming this `userEmail` for clarity?"
- ❌ "Rename this variable."

Explain WHY, not just WHAT:

- ✅ "This catch block swallows the error silently — if the save fails, the user will not know. Consider showing an error state."
- ❌ "Add error handling."

Assume good intent:

- ✅ "I might be missing context — is there a reason this skips validation?"
- ❌ "You forgot to validate the input."

Acknowledge strengths alongside problems:

- ✅ "The error handling pattern here is really clean — consistent with our conventions."

---

## REVIEW TIME MANAGEMENT

| PR Size | Time Budget | Approach |
| :--- | :--- | :--- |
| Under 100 lines | 10-15 min | Quick pass through all steps |
| 100-300 lines | 20-30 min | Full process, normal depth |
| 300-400 lines | 30-45 min | Full process, deeper analysis |
| Over 400 lines | Flag for split | "This PR is too large for effective review. Can we split it?" |

**Rule:** Limit review sessions to 60 minutes maximum. Reviewer fatigue degrades quality. If the review needs more time, take a break and return.

---

## SELF-REVIEW VARIANT

When reviewing your own code before delivery:

1. Follow the same steps 3 through 6 above
2. Apply the Anti-Comfort safeguard: if the code feels obviously fine, look harder
3. Read the code as if you have never seen it before
4. Ask: "If someone else wrote this, what would I flag?"
5. Check the `skill-coding` Non-Negotiable Checklist
6. If you cannot find anything to improve, you probably are not looking critically enough

---

## CHECKPOINTS AND QUALITY GATES

| Gate | Condition | Action |
| :--- | :--- | :--- |
| Gate 1 — Intent unclear | Cannot determine what the change is for | Note ambiguity before reviewing; review with calibrated confidence |
| Gate 2 — Automated checks failing | CI, type, lint, or build failing | Stop review, request fixes first |
| Gate 3 — Correctness unresolved | Core logic still uncertain | Do not allow style discussions to dominate |
| Gate 4 — High-risk surfaces without verification | Security or data path changed without adequate evidence | Escalate severity of the finding |
| Gate 5 — Findings not classified | Blocking versus optional still unclear | Review output is incomplete — classify before delivering |
| Gate 6 — Review drift into preference | Review has become mostly style opinion | Re-anchor on correctness, safety, and maintainability |

---

## QUALITY GATE CHECKLIST

Before delivering a code review:

- [ ] Understood the purpose of the change before reading code
- [ ] Risk level assessed and focus areas identified
- [ ] Automated checks confirmed passing
- [ ] Correctness reviewed — logic, edge cases, state, data integrity
- [ ] Security reviewed — validation, auth, data exposure, injection
- [ ] Maintainability reviewed — readability, conventions, complexity
- [ ] Test quality reviewed if tests are present
- [ ] Architecture reviewed if structural change
- [ ] Findings classified by severity with blocking status clear
- [ ] Each finding includes WHY it matters and a suggested fix
- [ ] Approval status stated explicitly with conditions if not ready
- [ ] Tone is collaborative and constructive
- [ ] Strengths acknowledged alongside issues
- [ ] Review validates its own findings for preference inflation

---

## WORKFLOW ANTI-PATTERNS

| Anti-Pattern | Why It Is Harmful | How This Workflow Prevents It |
| :--- | :--- | :--- |
| Style-First Reviewing | Focusing on naming trivia, formatting, or taste while core correctness or risk remains uncertain | Inspect correctness, safety, and maintainability first. Style that can be automated should be automated, not reviewed manually |
| Drive-By Approval | Approving because the diff is small, the tests pass, or the code looks clean at a glance | Understand intent, affected paths, and verification quality before approving |
| Blocking on Preference | Turning stylistic preference into a must-fix issue without real risk justification | Classify findings by actual severity and be honest about what is optional |
| Review Without Approval Conditions | Listing issues but never stating whether the change is approvable or what must change first | State approval status and minimum blocking conditions explicitly |
| Review as Rewrite | Rewriting large portions of the submitted code rather than identifying issues with the existing approach | Identify the problem and suggest a direction. Let the author implement the fix |

---

## FAILURE MODES AND ESCALATION PATHS

| Failure Mode | What It Looks Like | Escalation |
| :--- | :--- | :--- |
| Architecture Shift | Review target is actually an architectural decision | Escalate to architecture reasoning, return with that decision clarified |
| Incomplete Target | Code too incomplete to review meaningfully | State incompleteness explicitly, review only what can be judged reliably |
| Product Mismatch | Main problem is weak requirements, not weak code | Switch to product or feature-build reasoning to clarify intent |
| Deep Debt Found | Review uncovers significant structural debt | Load `skill-refactoring.md`, distinguish immediate fixes from cleanup |
| Domain Gap | Review crosses into security or performance specialization | Load relevant skill before finalizing findings |

---

## FINAL RULE

A good review improves the quality and trustworthiness of the codebase by identifying the highest-impact issues clearly, fairly, and in priority order.

Do not review to demonstrate thoroughness. Review to make the codebase better.

---

## VERSION HISTORY

| Version | Date | Changes |
| :--- | :--- | :--- |
| Gold v1.1 | Initial | Established the systematic sequence for reviewing code |
