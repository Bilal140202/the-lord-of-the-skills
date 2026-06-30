# Playbook: Project Start Checklist

Use this checklist before initiating implementation on a new request.

## Intake
- [ ] Clarify objective, scope, and constraints.
- [ ] Define success criteria and non-goals.
- [ ] Classify task through `routers/prompt-router.md`.
- [ ] Determine whether the task is beginner-facing and whether extra explanation depth is needed.

## Preparation
- [ ] Load primary role module and needed supporting roles.
- [ ] Load required guardrails.
- [ ] Identify dependencies and risks.
- [ ] Identify the scoped task and protected zones.
- [ ] Confirm whether existing UI, public exposure, credentials, or repository history could be affected.

## Execution Plan
- [ ] Draft step-by-step implementation plan.
- [ ] Create validation checklist (lint/test/manual checks).
- [ ] Confirm documentation updates required.
- [ ] Decide whether environment-changing steps should be agent-run or user-run.
- [ ] Prepare rollback notes for any high-impact or irreversible action.

## Ready to Implement
- [ ] Plan approved against minimal-change principle.
- [ ] Security and UI preservation requirements acknowledged.
- [ ] Workstream and branch match the request, or a safe new branch/worktree is chosen.
- [ ] Initial status summary prepared.
