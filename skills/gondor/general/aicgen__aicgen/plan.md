# /plan

Produce a phased, checkpoint-driven implementation plan based on the spec and research findings.

**Pre-condition:** An active spec with a `## Research Findings` section must exist — if research has not been run, warn the user and ask them to confirm they want to skip it before proceeding.

**Steps:**
1. Read the active spec (including research findings) from `docs/specs/`
2. Analyse the codebase to understand existing structure, patterns, and conventions
3. Break the implementation into phases — each phase must be independently verifiable
4. For each phase, list: files to create or modify, key decisions, and how to verify it is complete
5. Identify risks and propose mitigations
6. Create `docs/plans/` directory if it does not exist
7. Save the plan to `docs/plans/{spec-name}.md`
8. Confirm the file was saved and prompt the user to run `/build`
