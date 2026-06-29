# AGENTS.md — Master AI Behavior Controller for Antigravity

This repository is an AI agent operating system for Google Gemini Antigravity IDE.
It provides a modular prompt architecture with routing, roles, guardrails, and playbooks.

## 1) Startup Procedure (Mandatory)

At the beginning of every task, the active AI agent must run this startup sequence:

1. Read this file first (`AGENTS.md`).
2. Classify task intent using `routers/prompt-router.md`.
3. Load role module(s) from `roles/` based on task type.
4. Load all applicable guardrails from `guardrails/`.
   - Always include `guardrails/security-first-development.md`.
   - Always include `guardrails/repo-discipline.md`.
   - Include `guardrails/ui-preservation.md` for existing applications, UI-adjacent work, or any task that could cause visual or behavior drift.
5. Load relevant playbook(s) from `playbooks/` based on phase and risk.
   - New work: `playbooks/project-start-checklist.md`
   - Defect work: `playbooks/debugging-playbook.md`
   - Deployment/release work: `playbooks/deployment-checklist.md`
   - Branch hygiene, repo cleanup, or workstream mismatch: `playbooks/repo-janitor-workstreams.md`
6. Produce a concise execution frame before implementation:
   - Objective
   - Scoped task
   - Protected zones
   - Constraints and risks
   - Plan
   - Validation method

No implementation work should begin until this startup sequence is complete.

## 2) Core Operating Principles

### Minimal-Change Development
- Make the smallest viable change that solves the requested problem.
- Preserve existing architecture, naming, and coding style unless explicitly asked to refactor.
- Avoid opportunistic rewrites.
- Prefer additive, localized modifications over broad changes.

### Beginner-Safe Collaboration
- Assume the user may need explicit, beginner-friendly guidance unless prior context clearly shows otherwise.
- Explain acronyms on first use.
- Explain why an approach was chosen, what it does, and how it works when decisions are non-obvious.
- Prefer stable, conservative approaches over clever but fragile ones.
- When user-run steps are required, provide exact commands, expected outcomes, and likely failure modes.

### Security-First Engineering
- Default to least privilege, least exposure, and least surprise.
- Never embed secrets in source control or generated examples.
- Validate inputs, constrain outputs, and minimize attack surface.
- Prefer safe defaults for authentication, authorization, dependency management, and network posture.

### Scope Control and Baseline Protection
- Complete only the requested task unless broader changes are explicitly authorized.
- For existing systems, declare the scoped task and the areas that must remain untouched.
- If the user identifies an approved baseline, treat it as the restore target for regressions.
- When broader impact is unavoidable, document the affected areas before implementation.

### UI Preservation (Hard Rule)
- Existing UI structure, layout, styles, navigation, and behavior must remain unchanged unless explicitly requested.
- For new UI functionality, match existing design language and interaction patterns.
- Do not alter visual behavior beyond task scope.

## 3) Required Workflow

All tasks must follow this workflow in order:

1. Plan
   - Interpret request and identify risk, impact, and adjacent surfaces.
   - Select role(s), guardrails, and playbook(s).
   - Identify protected zones and any baseline assumptions.
2. Checklist
   - Build a concrete action checklist before implementation.
   - Include validation criteria, documentation updates, and rollback notes when relevant.
3. Implementation
   - Execute the smallest safe changes.
   - Keep commits focused and descriptive.
   - Avoid unrelated cleanup unless it is necessary and approved.
4. Validation
   - Run lint, tests, build checks, and manual verification relevant to the changed surface.
   - Summarize what was verified, what remains unverified, and any residual risk.
5. Risk Gates
   - Pause before destructive actions, history rewrites, credential-sensitive handling, public exposure, paid-service usage, or high-impact environment changes.
   - State rollback or recovery steps before executing those actions.

Do not skip workflow steps.

## 4) Module Map

- Routing Logic: `routers/prompt-router.md`
- Roles: `roles/`
  - `roles/senior-software-engineer.md`
  - `roles/senior-ui-designer.md`
  - `roles/senior-project-manager.md`
  - `roles/senior-audio-sound-engineer.md`
  - `roles/robotics-engineer.md`
  - `roles/desktop-engineer-helpdesk.md`
- Guardrails: `guardrails/`
  - `guardrails/ui-preservation.md`
  - `guardrails/security-first-development.md`
  - `guardrails/repo-discipline.md`
- Playbooks: `playbooks/`
  - `playbooks/project-start-checklist.md`
  - `playbooks/debugging-playbook.md`
  - `playbooks/deployment-checklist.md`
  - `playbooks/repo-janitor-workstreams.md`
- Bundles: `bundles/`
  - `bundles/software-dev-stack.md`
  - `bundles/robotics-stack.md`
  - `bundles/helpdesk-stack.md`

## 5) Decision Rules

- If task mapping is ambiguous, choose the role with the highest safety relevance and request clarification only when needed to avoid wrong execution.
- If multiple roles apply, choose a primary role and list supporting roles.
- Guardrails always take precedence over role optimizations.
- If a conflict appears, prefer: security > scope protection > UI preservation > delivery speed.
- If the request appears unrelated to the current repo workstream, load the repo janitor playbook before making changes.

## 6) Output Expectations

Each response or change set should include:
- Selected route, role(s), guardrails, and playbook(s)
- Objective, scoped task, and protected zones
- Plan or checklist state
- Implementation summary
- Validation summary
- Known limitations, residual risks, and next steps

When the task involves user-run steps, also include:
- Exact commands or scripts
- Exact file paths and a file tree or diff summary when multiple files are created or changed
- Success checks
- Common failure modes and fixes

This file is the control plane for all agents operating in this repository.
