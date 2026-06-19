---
created: 2026-04-17
updated: 2026-04-17
---

---
name: harness-fetch
description: >-
  Guides a user through fetching and setting up their chosen AI harness config from .ai/.<harness>/ into their local working environment. Use when the user says /harness-fetch, asks how to set up Cursor, Claude, or another harness for this lab, or wants to pull pre-built harness config without committing personal artifacts.
created: 2026-04-05
updated: 2026-04-05
status: phase-2-planned
---

# Harness Fetch (`/harness-fetch`)

> **Status:** Planned (phase 2). This skill is a **design stub**. The workflow below describes the intended behavior when implemented. For now, follow the manual steps.

**Purpose:** Pull the pre-built AI harness configuration from `.ai/.<harness>/` into the correct location in your local working environment—without committing personal artifacts to the repo.

## When to use

- First time opening this lab in a new harness (Cursor, Claude Code, Antigravity, etc.)
- After pulling updates that changed `.ai/.<harness>/` skills or rules
- When setting up a new machine for an existing lab

## Harnesses supported

| Harness | Config source | Where it should live locally |
|---------|--------------|------------------------------|
| Cursor | `.ai/.cursor/` | `.cursor/` at repo root (or workspace root) |
| Claude Code | `.ai/.claude/` | `.claude/` at repo root |
| (your harness) | `.ai/.<harness>/` | wherever `.<harness>/` is expected |

## Workflow (manual steps until skill is implemented)

1. **Identify your harness** — which AI tool are you using?

2. **Check what is available:**
   ```bash
   ls .ai/
   ```
   Look for `.<your-harness>/` alongside `.cursor/` and other entries.

3. **Copy or symlink the config:**

   **Option A — Copy (safest):**
   ```bash
   cp -r .ai/.cursor/ .cursor/
   ```

   **Option B — Symlink (stays in sync automatically):**
   ```bash
   ln -s .ai/.cursor .cursor
   ```
   On Windows: `mklink /D .cursor .ai\.cursor` or configure your harness to look inside `.ai/`.

4. **Verify your harness picks up the config** — open your harness tool and confirm skills/rules are available.

5. **Do not commit personal artifacts:**
   - `.cursor/settings.json`, `.cursor/chat/`, `.claude/` at the repo root are gitignored.
   - Only `.ai/` is committed—never the root-level harness config that contains your personal data.

## Adding your harness to this lab

If `.ai/.<your-harness>/` does not exist yet:

1. Create the folder: `.ai/.<your-harness>/skills/` and `.ai/.<your-harness>/rules/`
2. Adapt the skills from `.ai/.cursor/` as a starting point.
3. Add a `README.md` inside `.ai/.<your-harness>/` documenting what the config does.
4. Consider contributing it back upstream if it would benefit others.

## Phase 2 implementation notes

When fully implemented, this skill will:
- Detect which harness the user is working in
- Copy or link `.ai/.<harness>/` to the appropriate location automatically
- Report which skills and rules were activated
- Warn about any missing harness-specific content

This skill is harness-agnostic by design: written in plain instructions any agent or human can follow, not tied to any single tool's invocation format.
