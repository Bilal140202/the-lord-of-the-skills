# /build

Execute the next (or a specified) phase of the current implementation plan.

**Pre-condition:** An active plan must exist in `docs/plans/` — if none is found, tell the user to run `/plan` first and stop.

**Steps:**
1. Read the active plan from `docs/plans/`
2. Determine the next incomplete phase (or the phase specified by the argument)
3. Announce which phase is being executed and what it covers
4. Implement the phase step by step, following existing codebase patterns and conventions
5. After completing the phase, summarise what was changed and what was created
6. Mark the phase as complete in the plan file
7. Run any tests relevant to the completed phase and report results
8. Pause and ask: "Phase {n} complete. Continue to phase {n+1}?" before proceeding
