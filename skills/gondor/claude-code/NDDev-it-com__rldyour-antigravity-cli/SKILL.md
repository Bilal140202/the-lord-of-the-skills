---
name: ry-sync
description: "Синхронизируй Gemini docs, memories, git и fullrepo. EN: synchronize Gemini docs, memories, git, and fullrepo."
---

# Purpose

Finalize Gemini adapter work into synchronized source, docs, memories, git,
GitHub, and fullrepo state.

# Native Gemini Boundary

Use Gemini-native docs and runtime surfaces. Fullrepo is a branch policy, not a
Gemini runtime feature.

# When To Use

Use at the end of a completed task or when a Stop/post-task sync hook asks for
final synchronization.

# Inputs

- Current git status and upstream state.
- Serena memory freshness state.
- Instruction docs state.
- Fullrepo policy and branch state.

# Procedure

1. Confirm memories are current before docs/fullrepo sync.
2. Inspect uncommitted changes and exclude secrets, runtime markers, caches, and
   browser artifacts.
3. Run scope-matching checks.
4. Commit/push coherent source changes when appropriate.
5. Publish fullrepo only when policy allows and report advisory branch cleanup.

# Evidence Required

Git status, memory state, validator output, commit/tag IDs, fullrepo state, and
GitHub sync status.

# Forbidden Actions

Do not delete branches, force-push, publish fullrepo, or mutate system configs
unless policy and owner authorization allow that exact action.

# Acceptance Checks

Working tree is clean, memories are current, runtime markers are absent, and
fullrepo state matches policy.

# Failure Reporting

Report exact blockers and the command needed to clear each one.

