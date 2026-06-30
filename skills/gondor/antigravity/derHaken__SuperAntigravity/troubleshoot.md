---
name: troubleshoot
description: Orchestrates systematic debugging sessions.
---
# /troubleshoot

**What this does:** Orchestrates systematic debugging sessions.

Load systematic-debugging skill — it owns the 4-phase process.

## Orchestration (what this workflow adds)

**Before loading the skill:**
1. Confirm the issue is reproducible: "Can you trigger this consistently? Yes/No?"
   If No — flaky issue protocol:
   Phase 1 priority changes: (1) check timing dependencies and async race conditions; (2) check environment-specific state (caches, file locks, network timeouts); (3) document reproduction rate (e.g., "fails 3 of 10 runs"). Do not attempt a fix until you can reproduce failure at least once on demand or can explain why consistent reproduction is impossible.
2. Gather: exact error message, stack trace, and "when did this last work?"

**Phase names match the systematic-debugging skill exactly:**
- Phase 1: Root Cause Investigation
- Phase 2: Pattern Analysis
- Phase 3: Hypothesis and Testing
- Phase 4: Implementation

Use these names when reporting status. Do not rename phases.

**After Phase 4:**
- Load verification-before-completion skill before declaring fixed
- Write a regression test and commit both the fix and the test together:
  - Commit message: `fix: [bug description]` + `test: [bug description] no longer occurs` (two-line message or two separate commits)
  - Test function name: follows project's existing naming convention for regression tests

## Escalation Path

Note: If the systematic-debugging skill's 3-fix architectural escalation triggers before Phase 4 completes, follow the skill's escalation path first. The path below applies only when the full 4-phase process completes without resolution.

If all 4 phases complete and issue is unresolved:
1. Document in BLOCKERS.md: symptom, what was tried, what was ruled out
2. Load deep-research skill to look for similar issues in official docs/issues
3. If still unresolved: present findings to user with specific question ("I've ruled out X and Y — is there something about the deployment environment I'm missing?")

## What NOT to Do
- Do NOT retry the same failing command without a new hypothesis
- Do NOT declare fixed without running verification-before-completion
- Do NOT guess and check — form hypothesis first
