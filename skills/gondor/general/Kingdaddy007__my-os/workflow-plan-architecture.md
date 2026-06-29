# WORKFLOW: PLAN ARCHITECTURE (FULL SOURCE)

**Version:** Gold v1.1 (Master Merge)
**Layer:** 8 — Execution Workflow
**Tier:** 2 — Loaded by task
**File:** workflows/workflow-plan-architecture-SOURCE.md
**Primary Mode:** Architect
**Secondary Modes:** Research, Security, Performance, Product Thinking
**Purpose:** The systematic sequence for making architectural decisions — from understanding requirements through evaluating options to documenting the decision with tradeoffs and implementation guidance. Ensures architectural decisions are made deliberately rather than defaulting to whatever pattern is most familiar.
**Loaded When:** Designing a new system or module, restructuring existing architecture, evaluating technology choices, defining service or module boundaries, or making decisions that will be expensive to reverse.
**Inherits From:** execution-workflow.md (universal process)

---

## WHAT THIS WORKFLOW DOES

This workflow ensures architectural decisions are made deliberately — with requirements understood, options evaluated, tradeoffs documented, and failure modes considered.

Without this workflow, architecture tends to be either over-engineered for a team that does not need that complexity, or under-designed and growing organically until the codebase becomes unmaintainable. Both extremes are caused by the same root issue: choosing a shape before understanding the problem.

---

## ACTIVATION

### Use When

- "How should I structure this?"
- "What architecture should we use?"
- "Should we split this into [X]?"
- "What technology should we use for [Y]?"
- "Plan the architecture"
- "How should these components interact?"
- "Monolith or microservices?"
- "What should live where?"
- Starting a new project or major feature
- Redesigning an existing module or system
- Any decision that will be expensive to reverse

### Do NOT Use When

- Implementing already-decided architecture → use `workflow-build-feature.md`
- Debugging an architectural issue → use `workflow-debug-issue.md`
- Refactoring without changing architecture → use `workflow-refactor-module.md`
- Quick Type 2 technology comparison → use Research Mode directly with a time-box
- Reviewing a finished diff where architecture is already embodied → use `workflow-review-code.md`

---

## DECISION CLASSIFICATION

Before investing deep analysis, classify the decision:

| Classification | Definition | Analysis Investment | Use This Workflow? |
| :--- | :--- | :--- | :--- |
| **Type 1 — Irreversible, High-Stakes** | Hard to undo, high blast radius if wrong | Full workflow, all steps, ADR documented | ✅ Full workflow |
| **Type 1.5 — Partially Reversible** | Costly but possible to undo | Steps 1 through 4 at moderate depth, brief ADR | ✅ Abbreviated workflow |
| **Type 2 — Reversible, Low-Stakes** | Easy to change later | Time-boxed 30 to 60 minutes, brief reasoning | ❌ Skip workflow |

**Most engineering decisions are Type 2.** Do not use this full workflow for library selection, naming conventions, or internal tooling choices.

---

## REQUIRED FILES

### Skills — Always Load

| Priority | Skill | Why |
| :--- | :--- | :--- |
| Primary | `skill-architecture` | System decomposition, boundaries, patterns |
| Secondary | `skill-product-thinking` | Ensuring architecture serves user needs |
| Secondary | `skill-research-analysis` | Option evaluation methodology |

### Skills — Load When Relevant

| Condition | Skill |
| :--- | :--- |
| Architecture involves data layer decisions | `skill-database` |
| Architecture involves API or service boundaries | `skill-api-design` |
| Architecture has security-sensitive components | `skill-security` |
| Architecture is driven by performance requirements | `skill-performance` |
| Architecture involves deployment or infrastructure | `skill-devops-infra` |

### Contexts — Always Load

- `project-context.md`
- `architecture-context.md`
- `business-priorities.md`
- `stack-context.md`
- `domain-rules.md`

### Contexts — Load When Relevant

| Condition | Context |
| :--- | :--- |
| Data architecture decisions | `database-context.md` |
| Infrastructure decisions | `infra-context.md` |
| API architecture decisions | `api-conventions.md` |
| Security architecture | `security-baselines.md` |

---

## REQUIRED INPUTS

At minimum, Anti-Gravity should have or establish before proceeding:

- a clearly stated or inferable system or problem objective
- enough context to understand the main constraints
- scale expectations
- ownership and team boundaries
- reversibility concerns and timeline pressure

### If inputs are incomplete

Do NOT jump straight into boxes and arrows. Instead:

1. Define the real architectural decision being made
1. Identify the minimum constraint set that shapes the answer
1. State assumptions explicitly
1. Ask clarification only when missing information would materially change the architecture recommendation

---

## EXECUTION SEQUENCE

---

### STEP 1 — UNDERSTAND THE REQUIREMENTS

**Mode:** Architect
**Goal:** Know WHAT the architecture must accomplish before deciding HOW. An architecture that does not serve the requirements is wrong regardless of how elegant it is.

**Gate:** Do NOT evaluate solutions until requirements are clearly defined.

#### Functional Requirements (Step 1)

1. **Identify Capabilities:**
   - What capabilities must the system provide?
   - What user problems does it solve? Check `project-context.md`
   - What workflows must it support?
   - What success looks like after the architecture decision

#### Non-Functional Requirements (Step 1)

| Dimension | Question | How to Quantify |
| :--- | :--- | :--- |
| Scale | How many users, requests, records? | Current: [X]. In 12 months: [Y] |
| Performance | What latency is acceptable? | p95 target: [X]ms |
| Availability | What uptime is required? | Target: [X]% |
| Consistency | How important is data consistency? | Strong for [X], eventual acceptable for [Y] |
| Security | What data sensitivity level? | Per `security-baselines.md` |
| Compliance | Any regulatory requirements? | GDPR, SOC 2, etc. |

#### Constraints (Step 1)

1. **Assess Limitations:**
   - Team size and expertise — check `project-context.md`
   - Budget constraints — check `business-priorities.md`
   - Timeline constraints
   - Technology constraints — check `stack-context.md`
   - Organizational constraints
   - Already-locked architectural decisions that must be respected

#### Current State Assessment (Step 1)

1. **Audit Existing System:**
   - What is the current architecture? Check `architecture-context.md`
   - What works well and should be preserved?
   - What is causing pain and needs to change?
   - What technical debt or drift exists?
   - What cannot realistically change right now?

#### Output (Step 1)

```text
Architectural objective: [what is being decided]
Decision focus: [boundaries / deployment / data / extensibility / scale]
Functional requirements: [list]
Non-functional requirements: [quantified where possible]
Hard constraints: [list]
Current state: [brief assessment]
Success looks like: [measurable condition]
```

---

### STEP 2 — MAP THE SYSTEM AND IDENTIFY TENSIONS

**Mode:** Architect
**Goal:** Understand the full system context and expose the tradeoffs that make this a real architecture problem.

#### System Mapping Actions (Step 2)

1. **Component Inventory:**
   - Identify major functional areas and their boundaries
   - Map main actors and flows
   - Identify inputs, outputs, and dependencies
   - Identify what data each component owns
   - Identify integration points with external systems
   - Identify critical paths and likely failure domains
   - Identify what must remain stable versus what needs flexibility
   - Apply the deep module principle: is each component's interface simple while hiding internal complexity?

#### Architectural Tensions (Step 2)

1. **Expose Tradeoffs:**
   - Identify the primary tensions: speed vs flexibility, simplicity vs scale, coupling vs coordination cost, centralization vs autonomy
   - Identify what would be gained by one direction and sacrificed by another
   - Separate current needs from imagined future needs
   - Identify what is hard to reverse if chosen badly

#### Output (Step 2)

```text
Component map: [major parts and boundaries]
Data flow: [how data moves through the system]
Integration points: [external connections and failure behavior]

Primary tensions:

- [tension 1]
- [tension 2]

Hard-to-reverse choices:

- [list]

```

#### Gate (Step 2)

If no real tension is visible, the problem may be smaller than assumed — or not architectural yet. Do not fabricate complexity.

---

### STEP 3 — GENERATE OPTIONS

**Mode:** Architect
**Goal:** Identify at least three viable architectural approaches before evaluating any of them.

**RULE:** Never evaluate fewer than 3 options. A single option is a default, not a decision.

#### Option Specification (Step 3)

For Each Option, Define:

| Dimension | What to Specify |
| :--- | :--- |
| Description | What is this approach in one paragraph? |
| Components | What are the major parts and how do they connect? |
| Technology | What specific technologies would be used? |
| Data model | How would data be structured and stored? |
| Deployment | How would this be deployed and operated? |
| Scale path | How does this approach handle 10x growth? |
| Failure modes | How can this break? What is the blast radius? |
| Team fit | Can the current team build and maintain this? |
| Migration path | How do we get from current state to this? |

#### Option Generation Safeguards (Step 3)

1. **Boring Technology Bias:** Include the most boring option that still solves the problem. Boring means well-understood, well-documented, and frequently debugged.
1. **Gray Thinking:** Are options unnecessarily polarized? Monolith versus microservices often misses modular monolith.
1. **Framing Bias:** Are all options within the current frame? Look for a fresh perspective.
1. **Anti-Comfort:** If one option feels obviously right, look harder at the others.
1. **Overkill Check:** Would any option be overkill for the current stage? Name that explicitly.

#### Output (Step 3)

```text
Option A: [name — usually the boring or simplest option]
[description, components, technology, data, deployment, scale, failure modes, team fit, migration path]

Option B: [name]
[same dimensions]

Option C: [name]
[same dimensions]
```

---

### STEP 4 — EVALUATE TRADEOFFS

**Mode:** Architect
**Goal:** Compare options systematically against real requirements. If the recommendation is not visibly tied to the criteria, the decision is still too opinion-shaped.

#### Evaluation Matrix (Step 4)

| Criterion                      | Weight | Option A | Option B | Option C |
| :----------------------------- | :----- | :------- | :------- | :------- |
| Meets functional requirements  | High   | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ |
| Meets performance requirements | Med    |          |          |          |
| Team expertise fit             | High   |          |          |          |
| Implementation cost            | Med    |          |          |          |
| Operational complexity         | Med    |          |          |          |
| Migration risk                 | High   |          |          |          |
| Reversibility                  | High   |          |          |          |
| Infrastructure cost            | Med    |          |          |          |
| Time to implement              | Med    |          |          |          |
| Scale path clarity             | Med    |          |          |          |
| Security posture               | High   |          |          |          |
| Failure blast radius           | High   |          |          |          |

#### Analysis Frameworks (Step 4)

1. **The 2 AM Test:** "It is 2 AM. This component is failing. A mid-level engineer who did not build it is on-call. Can they fix it without tribal knowledge?"
1. **What Would Have to Be True:** "What would have to be true about our situation for this option to be the right choice?"
1. **Pre-Mortem:** "It is 6 months from now and this architecture has failed. What went wrong?"
1. **Steel-Manning:** Before rejecting an option, articulate its strongest version. Why would a smart engineer choose it?

#### Output (Step 4)

```text
Criteria comparison: [matrix filled in]
2 AM test result for each option: [assessment]
Pre-mortem on leading option: [risks surfaced]
Recommendation: [option and primary reason]
Tradeoffs accepted: [what is being sacrificed]
```

---

### STEP 5 — DEFINE THE ARCHITECTURE SHAPE AND BOUNDARIES

**Mode:** Architect
**Goal:** Make the recommendation explicit and structurally clear enough that implementation can proceed without inventing architecture ad hoc.

#### Structural Definition (Step 5)

1. **Shape Boundaries:**
   - State the recommended architecture direction
   - Define the major boundaries clearly
   - Define what responsibilities live where
   - Define key interactions between parts
   - Define data ownership and mutation boundaries
   - Identify what should remain tightly coupled and what should not
   - Avoid premature decomposition where simpler structure fits
   - Define where security and observability concerns must live

#### Runtime Implications (Step 5)

1. **Operational Audit:**
   - How does data flow across boundaries?
   - What happens at integration points when external systems fail?
   - How does the architecture affect change velocity and debugging?
   - Does the architecture assume organizational maturity the team does not have?
   - How does it look on a static diagram versus in production at 2 AM?

#### Output (Step 5)

```text
Recommended shape: [description]

Major boundaries:

- [boundary 1: what lives here, what does not]
- [boundary 2]

Interaction model:

- [how parts communicate]
- [data ownership rules]
- [integration failure behavior]

Operational implications:

- [deployment]
- [observability]
- [rollback]

```

#### Gate (Step 5)

If boundaries are still fuzzy after this step, implementation will invent the real architecture later without coordination.

---

### STEP 6 — DOCUMENT THE DECISION AS AN ADR

**Mode:** Architect → Communicator
**Goal:** Make the decision and document it in a way that prevents re-litigation and informs future work.

#### Load Template (Step 6)

- [REQUIRED] Load [architecture-decision-record.md]({{GLOBAL_CONFIG_URI}}/global_templates/architecture-decision-record.md)
- Follow the structure and guidance in the template exactly to record the decision.

#### Post-ADR Actions (Step 6)

1. **Sync Contexts:**
   - Update `architecture-context.md` if this moves the needle
   - Update `stack-context.md` for new technology
   - Update `database-context.md` for data shifts
   - Log the decision in `memory/decisions-log.md`

---

### STEP 7 — DEFINE IMPLEMENTATION PATH

**Mode:** Architect → Builder Mode transition
**Goal:** Translate architecture into implementable direction so future work inherits the decision cleanly.

#### Phased Implementation (Step 7)

1. **Define Sequence:**
   - What should be built first — foundation, highest-risk, or highest-value?
   - What can run in parallel?
   - What are the dependencies between phases?
   - Note where future workflow files should inherit the architecture choice

#### Migration Protocol (Step 7)

1. **Move Strategy:**
   - What is the step-by-step migration path?
   - What can be done incrementally versus all at once?
   - What are the rollback points?
   - Consider Strangler Fig pattern for legacy systems

#### Verification Plan (Step 7)

1. **Audit Success:**
   - How will the architecture be verified as it is built?
   - What metrics will indicate success or emerging problems?
   - When should the team pause and evaluate?

#### Output (Step 7)

```text
Build first: [list]
Defer or keep open: [list]

Migration sequence: [steps if applicable]
Verification checkpoints: [when and what to check]
```

---

## CHECKPOINTS AND QUALITY GATES

| Gate | Condition | Action |
| :--- | :--- | :--- |
| Gate 1 — Objective vague | Cannot state what structural decision is being made | Suspend and clarify first |
| Gate 2 — Constraints weak | Recommendation made without scale or team context | Re-gather constraints before deciding |
| Gate 3 — Single option | Only one option considered or alternatives are straw-men | Generate 3 viable options |
| Gate 4 — Operational risk | Design assumes maturity the team does not have | Simplify or re-scope |
| Gate 5 — Fuzzy boundaries | Implementation still depends on invented future decisions | Define more granular boundaries |
| Gate 6 — No Pre-Mortem | Risks not surfaced before commitment | Run pre-mortem before finalizing |

---

## QUALITY GATE CHECKLIST

Before delivering an architecture recommendation:

- [ ] Decision classified as Type 1, 1.5, or 2
- [ ] Requirements defined: functional, non-functional, constraints
- [ ] Current state assessed — what works, what does not, what cannot change
- [ ] System mapped with boundaries, data flow, and integration points
- [ ] Architectural tensions identified
- [ ] At least three options generated
- [ ] Boring technology option included
- [ ] Gray-thinking check applied — no false polarization
- [ ] Options evaluated against requirements systematically via matrix
- [ ] Tradeoffs explicitly named — gains AND sacrifices per option
- [ ] 2 AM test applied to leading option
- [ ] What Would Have to Be True test applied
- [ ] Pre-mortem conducted for leading option
- [ ] Steel-man applied to rejected options
- [ ] Architecture shape defined with clear boundaries and ownership
- [ ] Operational and data implications inspected
- [ ] Decision documented as ADR with assumptions and review triggers
- [ ] Relevant context files updated
- [ ] Implementation path defined with phases and verification

---

## WORKFLOW ANTI-PATTERNS

| Anti-Pattern | Why It Is Harmful | How This Workflow Prevents It |
| :--- | :--- | :--- |
| Diagram-First Architecture | Architecture becomes aesthetic rather than operational | Define problem and constraints before shaping the system |
| Pattern Worship | System inherits complexity that does not fit its real needs | Choose simplest structure that survives failure |
| Future-Fantasy | Current simplicity is sacrificed for hypothetical pain | Design for current reality plus near-adjacent change |
| Unbounded Architecture | Implementation ends up inventing architecture ad hoc | Define responsibilities and boundaries explicitly |
| Single Option Bias | Confirmation bias shapes the entire analysis | Generate at least three options before evaluating |

---

## FAILURE MODES AND ESCALATION PATHS

| Failure Mode | What It Looks Like | Escalation |
| :--- | :--- | :--- |
| Non-Architectural | Decision is smaller than initially framed | Return to feature-level logic |
| Pure Research | Main need is exploration without commitment | Switch to research-analysis mode |
| Product Aspiration | System shape depends on unclear user goals | Bring in product reasoning first |
| Stack Vacuum | Cannot finalize without stack decisions | Separate what is decided from what is open |
| Deep Refactor | Architecture change is not implementation-trivial | Coordinate with refactor planning |

---

## FINAL RULE

Choose the simplest architecture that solves the actual problem, survives likely failure, and remains understandable to the people who will have to change it later.

An architecture that looks elegant on a diagram but fails the 2 AM test, cannot be explained to the team, or requires organizational maturity that does not exist is not a good architecture for this project right now.

---

## VERSION HISTORY

| Version | Date | Changes |
| :--- | :--- | :--- |
| Gold v1.1 | Initial | Established the systematic sequence for making architectural decisions |
