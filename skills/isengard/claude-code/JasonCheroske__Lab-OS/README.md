---
created: 2026-04-17
updated: 2026-04-17
---

# Agnostic skills

Place skills here that work **regardless of which AI harness** you use (Cursor, Claude Code, Antigravity, or any other tool). Agnostic skills should not reference harness-specific invocation syntax (e.g. `/skill-name` is Cursor-specific).

## What belongs here

- Workflow guides written in plain language that any agent or human can follow step-by-step.
- Reference docs that describe how to work in this lab without assuming a specific tool.

## What does not belong here

- Cursor-specific skills using `/skill-name` syntax → use `.cursor/skills/` instead.
- Config files specific to one harness → use `.<harness>/` instead.

## Current skills

| Skill | Description |
|-------|-------------|
| `harness-fetch/` | Fetch and set up harness-specific config from `.ai/.<harness>/` |
