---
name: subagent-orchestration
description: Use when deciding whether to split a coding task into parallel exploration, bounded review fan-out, or single-writer delegated work instead of keeping it in one agent.
---

# Subagent Orchestration

Use subagents as a harness, not as a reflex. The goal is higher signal per token, not more parallelism.

## When to Use

Use this skill when:
- The work can be split into independent read-heavy tasks
- Multiple review lenses would improve confidence
- One bounded implementer can own the write path while others explore or review
- The workflow will cross stages and needs an explicit handoff contract

Do not use this skill when:
- A single agent can complete the task without context pressure
- Multiple subagents would edit the same files or shared state
- The host cannot support the needed delegation model safely

## Default Orchestration Policy

Fan out only when the delegated scopes are independent and at least one of these is also true:
- The task is non-trivial or cross-cutting
- Independent review would materially change confidence

1. Parallelize read-heavy work first.
2. Keep write ownership narrow.
3. Define a handoff contract before multi-stage delegated work starts.
4. Require synthesis after any fan-out.
5. Require evidence in every subagent return.
6. Keep review and research subagents read-only with the minimum tools they need.
7. Keep lightweight workers on narrow tasks and reserve final judgment for the parent.
8. Escalate risky changes to human review.

Default budget:
- Research split: 2-4 subagents
- Review fan-out: 3 reviewers
- Implementation: 1 writer
- Delegation rounds: one research split and one review fan-out per user request or change objective unless the human asks for another scoped pass

Collapse back to one agent when:
- Tasks share files or state
- Findings become repetitive
- Coordination cost exceeds likely speedup

Mandatory human gate:
- Stop and ask before auth changes, public API changes, migrations, destructive operations, external contract changes, or overlapping or unclear concurrent writes.
- Stop and ask before changes that affect shared behavior, shared tests, or more than one owned file group unless ownership is explicitly disjoint and low risk.
- If risk is unclear, default to stop and ask.

Handoff contract minimum:
- Scope and owner
- Acceptance criteria
- Evidence expected on return
- Next-step handoff note

## Host Compatibility

Use the host-specific limits in [references/host-compatibility-and-limits.md](references/host-compatibility-and-limits.md) before delegating. Do not assume every host supports the same depth, communication model, or permission model.

## Required Patterns

Use these references as needed:
- [references/orchestration-patterns.md](references/orchestration-patterns.md)
- [references/handoff-contracts.md](references/handoff-contracts.md)
- [references/review-fanout-and-synthesis.md](references/review-fanout-and-synthesis.md)
- [references/anti-patterns.md](references/anti-patterns.md)

## Non-Negotiable Rules

- Never run overlapping multi-writer edits without hard ownership boundaries.
- Never hand work to the next stage without a readable handoff artifact.
- Never accept summary-only subagent output without evidence.
- Never fan out reviewers and skip synthesis.
- Never give edit-capable permissions to read-only review or research work.
- Never keep adding subagents when the output quality is already flattening.
