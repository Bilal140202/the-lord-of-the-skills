# Auxiliary Self Agent

Date: 2026-06-09

## Context

The user wants a CCB-specific role named `ccb_self` that understands CCB
runtime rules, tmux mounting, provider context repair, and message-chain
diagnostics. It should help users and other agents recover from CCB-related
failures, including broken agent context, stuck panes, missing replies, and
restart needs.

That role must not become another runtime authority. It should be useful in the
same way a human operator is useful: available for diagnosis and maintenance,
but not required for every agent to continue working.

Naming update: [006-future-modification-guardrails.md](006-future-modification-guardrails.md)
supersedes the early `agentroles.ccb_self` spelling. The canonical Role Pack id
is now `agentroles.ccb_self`.

## Decision

`ccb_self` is an auxiliary maintenance agent.

Its stable role id is `agentroles.ccb_self`, and its default project-local
agent name is `ccb_self`. It may be mounted as a normal configured agent in an
ops window.

`ccb_self` may diagnose, recommend, and perform authorized maintenance for CCB
runtime health, tmux evidence, provider context, config reload, and
message/job lineage. It must not own the user's original business task and must
not become a daemon lifecycle dependency.

## Consequences

- Other configured agents continue running if `ccb_self` fails.
- `ccbd`, keeper, mailbox dispatch, provider session binding, and tmux
  namespace validity must not depend on `ccb_self`.
- Runtime authority remains in CCB control-plane services and authority files,
  not in the role's memory, tools, or pane state.
- Repair of a failed task chain should return to the original target agent
  unless the user explicitly retargets the task.
- Mutating repairs must go through CCB commands or CCB MCP wrappers, not direct
  writes to authority files or raw destructive tmux commands.
- Role content should be distributed through the role catalog or local role
  source, not kept as production role payload in `ccb_source`.
