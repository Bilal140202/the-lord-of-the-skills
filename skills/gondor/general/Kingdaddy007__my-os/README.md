# README — WORKFLOWS FOLDER

**Location:** `.gemini/config/workflows/`
**Layer:** 8 — Execution Patterns
**Loading Tier:** 2 — **LOADED BY TASK**

***

## PURPOSE

This folder contains repeatable execution sequences for common engineering
tasks. While skills tell Anti-Gravity HOW to think, workflows tell it
WHAT STEPS TO FOLLOW and in what order.

Each workflow chains multiple operating modes and skill files together,
ensuring the right thinking happens at the right time. They prevent
the most common engineering mistake: jumping to execution without
understanding, analyzing, or planning first.

If:

- `core/` = how Anti-Gravity thinks
- `skills/` = what domain expertise it has
- `contexts/` = what world it is operating in

Then:

- `workflows/` = how it proceeds through real tasks

This folder turns good reasoning into repeatable process. It turns
intelligence into repeatable action.

***

## WHAT THIS FOLDER ANSWERS

- What sequence should Anti-Gravity follow for this kind of task?
- What should happen first, second, and last?
- What checks are specific to this task type?
- What typical mistakes should this workflow prevent?

***

## INVENTORY

| # | File | Trigger | Key Discipline Enforced |
| :--- | :--- | :--- | :--- |
| 1 | [workflow-build-feature.md]({{GLOBAL_CONFIG_URI}}/workflows/workflow-build-feature.md) | "Build", "implement", "add feature" | Problem definition before coding |
| 2 | [workflow-debug-issue.md]({{GLOBAL_CONFIG_URI}}/workflows/workflow-debug-issue.md) | "Fix", "broken", "error", "bug" | Evidence before code changes |
| 3 | [workflow-review-code.md]({{GLOBAL_CONFIG_URI}}/workflows/workflow-review-code.md) | "Review", "check", "audit" | Structured evaluation by severity |
| 4 | [workflow-design-ui.md]({{GLOBAL_CONFIG_URI}}/workflows/workflow-design-ui.md) | "UI", "design", "component", "page" | State coverage before implementation |
| 5 | [workflow-security-audit.md]({{GLOBAL_CONFIG_URI}}/workflows/workflow-security-audit.md) | "Security audit", "vulnerability check" | STRIDE across trust boundaries |
| 6 | [workflow-plan-architecture.md]({{GLOBAL_CONFIG_URI}}/workflows/workflow-plan-architecture.md) | "How should I structure", "architecture" | Requirements before solutions, 3+ options |
| 7 | [workflow-refactor-module.md]({{GLOBAL_CONFIG_URI}}/workflows/workflow-refactor-module.md) | "Refactor", "clean up", "tech debt" | Tests before structural changes |
| 8 | [workflow-design-api.md]({{GLOBAL_CONFIG_URI}}/workflows/workflow-design-api.md) | "Create endpoint", "API design" | Contract before implementation |
| 9 | [workflow-optimize-performance.md]({{GLOBAL_CONFIG_URI}}/workflows/workflow-optimize-performance.md) | "Slow", "optimize", "performance" | Measurement before optimization |
| 10 | [workflow-ship-to-production.md]({{GLOBAL_CONFIG_URI}}/workflows/workflow-ship-to-production.md) | "Deploy", "ship", "release" | Verification before and monitoring after |
| 11 | [workflow-project-inception.md]({{GLOBAL_CONFIG_URI}}/workflows/workflow-project-inception.md) | "Idea", "start project", "plan" | Problem definition before feature planning |

***

## LOADING RULES

**Load ONE workflow per task. Never load multiple workflows simultaneously.**

The `activation-engine.md` in `core/` maps task types to workflows.
If a task genuinely spans multiple workflow types — for example, build
a feature AND deploy it — execute them SEQUENTIALLY. Finish one before
starting the next.

Choosing the right workflow:

- Feature work → `workflow-build-feature.md`
- Debugging → `workflow-debug-issue.md`
- Code review → `workflow-review-code.md`
- Architecture planning → `workflow-plan-architecture.md`
- Performance work → `workflow-optimize-performance.md`
- Release → `workflow-ship-to-production.md`

Choose the workflow that best matches the actual job being done.

***

## EVERY WORKFLOW CONTAINS

Every workflow file follows the same required structure:

1. **What This Workflow Does** — Purpose and what it prevents
2. **Activation** — When to use and when NOT to use
3. **Required Files** — Which skills and contexts to load with priority
4. **Execution Sequence** — Step-by-step process with gates between steps
5. **Quality Gate Checklist** — What must be true before marking complete

***

## HOW WORKFLOWS RELATE TO THE 8-PHASE EXECUTION WORKFLOW

The universal 8-phase sequence lives in `core/execution-workflow.md`:

Understand → Contextualize → Analyze → Plan →
Execute → Verify → Critique → Communicate

Each specialized workflow in this folder implements that same sequence
but with domain-specific steps for each phase. For example:

- `workflow-debug-issue.md` Phase 1 (Understand) = "Restate the symptom precisely"
- `workflow-build-feature.md` Phase 1 (Understand) = "Define the user problem"
- `workflow-plan-architecture.md` Phase 1 (Understand) = "Define functional and non-functional requirements"

Same phases. Different content per domain.

***

## WORKFLOW-TO-SKILL MAP

| Workflow | Primary Skill | Secondary Skills |
| :--- | :--- | :--- |
| Build Feature | `skill-coding` | `skill-architecture`, `skill-testing`, `skill-security` |
| Debug Issue | `skill-debugging` | `skill-review-audit`, `skill-testing` |
| Review Code | `skill-review-audit` | `skill-security` (always), `skill-performance` |
| Design UI | `skill-ui-ux` | `skill-coding`, `skill-architecture` |
| Security Audit | `skill-security` | `skill-review-audit`, `skill-architecture` |
| Plan Architecture | `skill-architecture` | `skill-product-thinking`, `skill-database` |
| Refactor Module | `skill-refactoring` | `skill-testing`, `skill-coding` |
| Design API | `skill-api-design` | `skill-security`, `skill-coding` |
| Optimize Performance | `skill-performance` | `skill-database`, `skill-coding` |
| Ship to Production | `skill-devops-infra` | `skill-review-audit`, `skill-security` |

***

## INTERACTION WITH OTHER FOLDERS

| Folder | Relationship |
| :--- | :--- |
| `core/` | Workflows extend and implement the 8-phase sequence from `execution-workflow.md`. Workflows are governed by `operating-modes.md` discipline rules. Core provides the universal backbone; workflows give mission-specific operating procedures. |
| `skills/` | Workflows load specific skills at each step. A workflow usually activates one primary skill and up to two supporting skills. Skills provide behavioral depth; workflows provide the sequence. |
| `contexts/` | Workflows specify which context files to load. Context grounds the workflow in project reality and prevents wrong-stack or wrong-domain execution. |
| `templates/` | Templates may reference context files when producing project-specific output. |
| `rubrics/` | Workflows use rubrics during the Critique phase — Phase 7 — for self-evaluation before finalization. |

***

## WHAT A WORKFLOW IS AND IS NOT

A workflow should be:

- Task-shaped and procedural
- Shorter and more executable than a skill file
- A reusable operating path from task start to output
- Clear about which files to activate and when

A workflow is not:

- A skill replacement
- A philosophy document or essay
- A mode description
- So abstract that it stops guiding real action

***

## QUALITY BAR FOR FILES IN THIS FOLDER

A strong workflow file:

- Has clear "Use When" and "Do NOT Use When" sections
- Specifies exactly which skills and contexts to load
- Has explicit gates between steps — "Do NOT proceed until..."
- Ends with a quality gate checklist
- Is followable without additional guidance
- Prevents the most common mistake for that task type
- Makes the task easier to execute consistently
- Reduces random mode drift and common failure modes

A weak workflow file:

- Duplicates the universal workflow too closely without adding domain-specific value
- Lacks task-specific checks
- Overlaps heavily with another workflow
- Is so generic that it changes nothing in practice
- Is so abstract that real tasks cannot be driven from it

***

## COMMON MISTAKES TO AVOID

- Treating workflow files as mode descriptions
- Loading multiple workflows for one task simultaneously
- Forgetting to align workflows with the universal 8-phase process
- Creating workflows that should really just be skill behavior
- Making workflows so abstract that they stop guiding real action
- Conflating workflow files with context or skill files

***

## MAINTENANCE

Update workflows when:

- The team's development process changes
- New tools or practices change the execution sequence
- A workflow consistently produces suboptimal results
- New skills are added that should be integrated into existing workflows

Expected frequency: one to two updates per quarter.

***

## FINAL RULE

A workflow should make Anti-Gravity more repeatable, more disciplined,
and less chaotic on a real task. Recurring engineering tasks should
feel repeatable, disciplined, and easier to execute well under real
pressure.

If a workflow does not improve task execution quality, it is too vague.

