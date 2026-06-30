---
name: implement
description: Orchestrates feature implementation through TDD with review gates.
---
# /implement

**What this does:** Orchestrates feature implementation through TDD with review gates.

**Prerequisites:**
- Design approved (docs/plans/*-design.md exists) — if not, run /brainstorm first
- Implementation plan exists (docs/plans/*-plan.md) — if not, run /plan first
- On a feature branch (not main/master)
- **Fast Mode** active in Antigravity settings

**Skill dependencies:** This workflow uses: confidence-check, test-driven-development, systematic-debugging, requesting-code-review, verification-before-completion, finishing-a-development-branch (all in skills/).

## Session State

At the start of each task, output:
```
Session: /implement
Plan: [path to plan file]
Task: [N of M] — [task name]
Confidence: [score]/30
Status: [confidence-check | RED phase | GREEN phase | review | complete]
```

## Step 0: Load the Plan

Read the plan file at docs/plans/*-plan.md before running the confidence-check.
A confidence-check that doesn't reference the plan's specific tasks and file paths is invalid.

## Orchestration Flow

```
confidence-check skill → score ≥ 27 required to proceed
         ↓
test-driven-development skill → RED phase (write failing test)
         ↓
minimal implementation
         ↓
test-driven-development skill → GREEN phase (make it pass)
         ↓
commit
         ↓
requesting-code-review skill → review against plan
         ↓
next task (repeat)
         ↓
verification-before-completion skill → final check
         ↓
finishing-a-development-branch skill → merge/PR decision
```

## Session Announcement

At start: "Starting /implement for [task/feature]. Loading confidence-check..."

## On Confidence Below 27

Announce: "Confidence check failed: [dimension] scored [X].
Gap: [specific unknown].
Action: [reading files | running research | asking user]"
Do not start implementing until score reaches 27+.

If gap-filling does not raise confidence to 27+ within 2 iterations: announce the specific remaining gap to the user and wait for input. Do not begin implementation without reaching 27+.

## On Test Failure After Implementation

Load systematic-debugging skill. Do NOT retry without diagnosis.

## Commit Cadence

Commit after every GREEN test. Message format: `test: [what behavior is now tested]`
Never accumulate more than one GREEN test before committing.

If a commit fails: stop immediately. Do not run another test. Diagnose the commit failure first (load systematic-debugging if needed). Do not accumulate GREEN tests while a commit is pending.
