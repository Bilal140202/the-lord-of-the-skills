# Playbook: Repo Janitor and Workstreams

Use this playbook for repository cleanup, branch hygiene, workstream separation, or cases where the current branch does not match the requested task.

## 1. Audit First (No Changes)
- Capture current branch, default branch, remotes, and working-tree status.
- Review recent commits, changed files, and local and remote branch lists.
- Identify merged versus unmerged branches and any uncommitted or unpushed work.
- Summarize evidence before proposing cleanup actions.

## 2. Detect Workstream Mismatch
- State the current workstream, current branch, and intended outcome.
- If the request does not match the current branch, separate the work before editing.
- Prefer creating a safe scoped branch over mixing unrelated tasks into an existing branch.

## 3. Plan Before Cleanup
- Categorize branches or changes as keep, merge, archive, delete, or review.
- Prefer non-destructive options such as merge, archive, or cherry-pick over history rewriting.
- Provide dry-run or inspection commands before real cleanup commands when possible.
- Prepare rollback steps and backup points before any destructive cleanup.

## 4. Execute Safely (After Approval for Destructive Steps)
- Create a backup tag or branch before deleting or rewriting anything.
- Prune stale tracking references and clean merged branches first.
- Move unrelated work with stash or cherry-pick workflows instead of mixing scopes.
- Keep all commands explicit and reversible when possible.

## 5. Verify and Document
- Re-check branch status, diffs, and validation results after cleanup.
- Confirm the repository is easier to navigate and that no intended work was lost.
- Update README, contribution notes, or branch guidance when workflow expectations changed.
