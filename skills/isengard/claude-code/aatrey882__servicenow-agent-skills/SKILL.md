---
name: servicenow-agent-skills
description: >
  Expert-level agent skills for the entire ServiceNow development ecosystem.
  Covers Fluent SDK metadata (.now.ts), legacy scripting (GlideRecord, Script Includes,
  Client Scripts, g_form), and CLI setup (now-sdk auth, build, install). Use when
  generating, reviewing, or explaining any ServiceNow code.
license: MIT
compatibility: Claude Code, Cursor, VS Code Copilot, Antigravity, Codex
---

# ServiceNow Agent Skills Suite

This is a multi-skill suite. Each sub-skill contains its own `SKILL.md` with hard rules, reference files, and example assets. **Do not pre-load all sub-skills.** Read only the one that matches the current task.

## Sub-Skill Router

| Task Signal | Sub-Skill to Read |
|-------------|-------------------|
| `.now.ts` files, Fluent SDK imports, `@servicenow/sdk/core`, Table/ACL/BusinessRule metadata, `now.config.json` | `./sn-sdk-fluent/SKILL.md` |
| GlideRecord, Script Includes, Business Rules (legacy), Client Scripts, `g_form`, `g_user`, `gs.log` | `./sn-scripting/SKILL.md` |
| `now-sdk` CLI commands, project scaffolding, OAuth/Basic auth setup, environment configuration | `./sn-sdk-setup/SKILL.md` |

## Hard Rules

1. **Route before generating.** Identify the workspace type (Fluent SDK vs. legacy scripting vs. setup) and read the matching sub-skill's `SKILL.md` before writing any code.
2. **Never mix paradigms.** If the workspace contains `now.config.json` or `.now.ts` files, the project uses the Fluent SDK — do not generate GlideRecord code. If the workspace has no Fluent markers, use `sn-scripting`.
3. **One sub-skill per task.** Each sub-skill has its own reference files and examples. Read from the active sub-skill only — do not cross-reference between them unless explicitly directed by that skill's instructions.
