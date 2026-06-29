# README — SKILLS FOLDER

**Location:** `.antigravity/skills/`
**Layer:** 5 — Specialized Skill Domains
**Loading Tier:** 2 — **LOADED BY TASK**

***

## PURPOSE

This folder contains Anti-Gravity's domain expertise — specialized
"field manuals" that govern HOW to think and act in specific engineering
domains. Each skill file is a behavioral instruction set, NOT an
informational wiki.

If `core/` is the brain, `skills/` is the professional training. Each
skill is a lens that changes what Anti-Gravity pays attention to, what
questions it asks, what patterns it searches for, and what it considers
"done."

Skills are not educational essays. They are operational behavior modules.
A skill is only good if activating it changes how Anti-Gravity behaves
on real work in that domain.

***

## INVENTORY

| # | File | Primary Mode | What It Governs |
| :--- | :--- | :--- | :--- |
| 1 | [skill-coding.md]({{GLOBAL_CONFIG_URI}}/skills/coding/SKILL.md) | Builder | Implementation quality, readability, error handling, conventions |
| 2 | [skill-architecture.md]({{GLOBAL_CONFIG_URI}}/skills/architecture/SKILL.md) | Architect | System decomposition, boundaries, coupling and cohesion, patterns |
| 3 | [skill-debugging.md]({{GLOBAL_CONFIG_URI}}/skills/debugging/SKILL.md) | Debugger | Symptom vs cause, evidence gathering, hypothesis ranking, root cause |
| 4 | [skill-review-audit.md]({{GLOBAL_CONFIG_URI}}/skills/review-audit/SKILL.md) | Reviewer | Correctness, maintainability, security, anti-patterns, code smells |
| 5 | [skill-security.md]({{GLOBAL_CONFIG_URI}}/skills/security/SKILL.md) | Security | STRIDE, trust boundaries, auth and authz, input validation, secrets |
| 6 | [skill-ui-ux.md]({{GLOBAL_CONFIG_URI}}/skills/ui-ux/SKILL.md) | Designer | User flows, cognitive load, states, accessibility, interaction |
| 7 | [skill-testing.md]({{GLOBAL_CONFIG_URI}}/skills/testing/SKILL.md) | Builder / Reviewer | Test strategy, test levels, edge cases, regression prevention |
| 8 | [skill-performance.md]({{GLOBAL_CONFIG_URI}}/skills/performance/SKILL.md) | Performance | Bottleneck detection, profiling, measure-first optimization |
| 9 | [skill-database.md]({{GLOBAL_CONFIG_URI}}/skills/database/SKILL.md) | Architect / Builder | Schema design, indexing, migrations, access patterns |
| 10 | [skill-api-design.md]({{GLOBAL_CONFIG_URI}}/skills/api-design/SKILL.md) | Architect / Builder | Contract design, versioning, error handling, backward compatibility |
| 11 | [skill-devops-infra.md]({{GLOBAL_CONFIG_URI}}/skills/devops-infra/SKILL.md) | Architect / Debugger | CI/CD, environments, observability, deployment, incident response |
| 12 | [skill-refactoring.md]({{GLOBAL_CONFIG_URI}}/skills/refactoring/SKILL.md) | Optimizer | Debt identification, safe refactoring, Strangler Fig, scope control |
| 13 | [skill-research-analysis.md]({{GLOBAL_CONFIG_URI}}/skills/research-analysis/SKILL.md) | Research | Structured investigation, evidence quality, comparison methodology |
| 14 | [skill-product-thinking.md]({{GLOBAL_CONFIG_URI}}/skills/product-thinking/SKILL.md) | Cross-cutting | Jobs-to-be-Done, scoping, success metrics, opportunity cost |

***

## LOADING RULES

**Load the PRIMARY skill for the active mode. Load up to 2 SECONDARY
skills if the task spans domains. Do NOT load skills that are not
relevant. A focused skill set is better than broad skill clutter.**

The `activation-engine.md` in `core/` defines which skills to load for
each task type.

**Typical load: 1–3 skill files per task. Never load all 14.**

Typical loading examples:

- Debugging task → `skill-debugging.md` + maybe testing or review
- Architecture task → `skill-architecture.md` + maybe database or security
- Feature build → `skill-coding.md` + maybe testing, security, or UI/UX
- Performance task → `skill-performance.md` + maybe database or architecture

***

## WHAT SKILLS ANSWER

- What expertise should Anti-Gravity activate for this task?
- What does good behavior look like in this domain?
- What questions should be asked before acting?
- What anti-patterns should be avoided?
- What output shape is expected?

***

## EVERY SKILL FILE CONTAINS

Every skill file follows the same required structure:

1. **Mindset** — How an expert thinks in this domain
2. **Activation Triggers** — When to load, red flags when neglected, mode transitions
3. **Objectives** — What good looks like
4. **Decision Framework** — How to evaluate options
5. **Core Principles** — Rules that change behavior
6. **Lenses** — Inspection dimensions to check explicitly
7. **Behavioral Workflow** — Step-by-step process matching `execution-workflow.md` phases
8. **Key Diagnostic Questions** — What an expert asks before acting
9. **Non-Negotiable Checklist** — What must never be skipped
10. **Anti-Patterns** — What weak behavior looks like and why
11. **Output Contract** — How answers should be structured
12. **Examples of Good Behavior** — What excellent output looks like

***

## CRITICAL DESIGN RULE

**Skill files contain BEHAVIORAL INSTRUCTIONS — not information dumps.**

✅ Right: "When debugging: 1. Restate the symptom precisely. 2. Separate symptom from cause. 3. Gather evidence before hypothesizing."

❌ Wrong: "Debugging is the process of finding and resolving defects in software."

A skill file that informs but does not change behavior is failing its
purpose.

***

## INTERACTION WITH OTHER FOLDERS

| Folder | Relationship |
| :--- | :--- |
| `core/` | Skills INHERIT from core. Core principles override skill-specific guidance. Skills should not contradict core files. |
| `contexts/` | Skills provide universal HOW. Contexts provide project-specific WHAT — stack, conventions, architecture. Skills plus Contexts together equal grounded expertise. |
| `workflows/` | Workflows define task sequence. Skills define domain behavior inside that sequence. Workflows may chain multiple skills at different steps. |
| `templates/` | Templates provide deliverable format after a skill has done the domain work. |
| `rubrics/` | Each skill has a corresponding rubric for quality evaluation. Skill = how to do it. Rubric = how to judge it. |

***

## SKILL-TO-RUBRIC MAP

| Skill | Corresponding Rubric |
| :--- | :--- |
| `skill-coding.md` | `code-quality-rubric.md` |
| `skill-debugging.md` | `debugging-rubric.md` |
| `skill-architecture.md` | `architecture-rubric.md` |
| `skill-ui-ux.md` | `ux-rubric.md` |
| `skill-security.md` | `security-rubric.md` |
| `skill-testing.md` | `testing-rubric.md` |
| `skill-performance.md` | `performance-rubric.md` |
| `skill-api-design.md` | `api-quality-rubric.md` |
| `skill-review-audit.md` | `communication-rubric.md` |
| `skill-product-thinking.md` | `release-readiness-rubric.md` |

***

## QUALITY BAR FOR FILES IN THIS FOLDER

A strong skill file:

- Has a clear, distinct purpose in its domain
- Is behavioral — tells Anti-Gravity how to think and act, not what a topic is
- Follows the required section structure exactly
- Has strong activation logic — when to load, when not to
- Defines what good and bad behavior look like
- Includes anti-patterns with WHY they are harmful
- Includes examples of good behavior
- Includes an operational workflow
- Is self-contained — readable without other skill files loaded
- References which core files it inherits from
- Makes Anti-Gravity visibly stronger in that domain

A weak skill file:

- Overlaps heavily with another skill
- Reads like a tutorial instead of a behavior file
- Contains only definitions, not action guidance
- Duplicates core concepts excessively
- Does not materially change how Anti-Gravity would behave on real tasks

***

## COMMON MISTAKES TO AVOID

- Turning skill files into informational essays
- Duplicating `core/` concepts excessively inside skill files
- Loading too many skills for one task
- Creating skills that should really be contexts or workflows
- Making every skill sound the same without domain-specific discipline
- Treating activation as always-on — skills are loaded by task, not by default

***

## MAINTENANCE

Update skill files when:

- Expert behavior patterns are refined based on experience
- New anti-patterns are discovered in real work
- New activation triggers are identified
- The domain evolves — new tools, new best practices, new standards

Expected frequency: one to three updates per quarter.

***

## FINAL RULE

`skills/` should make Anti-Gravity behave like a specialist when the
task requires one — without losing the discipline of the core system.

A skill is only good if activating it changes how Anti-Gravity behaves
on real work in that domain.

