---
name: ry-start
description: "Выполни полный Gemini rldyour task lifecycle. EN: full Gemini rldyour task lifecycle."
---

# Purpose

Implement a scoped task in this Gemini adapter with validated code, docs, and
sync state.

# Native Gemini Boundary

Use Gemini-native commands, skills, subagents, hooks, policies, and settings.
Gemini subagents are local delegation helpers, not cmux orchestration.

# When To Use

Use when the owner asks Antigravity CLI to implement or repair a scoped task.

# Inputs

- User request and acceptance criteria.
- Context from `ry-init` when needed.
- Source files, validators, tests, and relevant official documentation.

# Procedure

1. Gather enough context before editing.
2. Plan the smallest coherent change.
3. Implement using local patterns and Gemini-native surfaces.
4. Run scope-matching validators and tests.
5. Sync memories/docs/fullrepo only when project policy allows and facts changed.

# Evidence Required

Changed paths, commands run, validator/test results, release or runtime evidence,
and remaining blockers.

# Forbidden Actions

No fake green checks, unbounded hooks, secrets, runtime caches, hidden
orchestrators, or branch deletion without explicit owner confirmation.

# Acceptance Checks

The changed scope passes its adapter validators plus the root integration gates
that reference it.

# Failure Reporting

Lead with blockers and exact failed commands, then list safe next actions.

