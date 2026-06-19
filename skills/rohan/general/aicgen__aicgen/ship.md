# /ship

Pre-flight wrap-up — verify everything is ready, then draft a PR description.

**Steps:**
1. Run the full test suite — stop and report if any tests fail
2. Read the active spec and plan
3. Verify that `docs/specs/{name}.md` and `docs/plans/{name}.md` are up to date
4. Check for uncommitted changes and list them
5. Draft a PR description referencing the spec and plan:
   ```
   ## Summary
   {goal from spec}

   ## Changes
   {summary of phases completed}

   ## Spec
   docs/specs/{name}.md

   ## Plan
   docs/plans/{name}.md

   ## Test plan
   {acceptance criteria from spec as a checklist}
   ```
6. Present the PR description to the user for review
7. Ask: "Ready to commit and push?" — if yes, stage all changes and create a commit with a conventional commit message
