# flowcrate Workflow Guide

> [!CAUTION]
> **🛑 STOP! BEFORE ANY WORK, READ THIS:**
> 1. Check active work: `flowcrate list --status doing --json | Out-String`
> 2. If user says "bump version" / "release" → READ `09_release.md` FIRST
> 3. If user says "commit" → Use `flowcrate commit <id>` not `flowcrate link`
> 4. **FAILURE TO READ RULES = WORKFLOW VIOLATIONS**

> This document provides an overview of the flowcrate workflow system.
> Detailed sections are assembled automatically during GEMINI.md generation.

## Overview

flowcrate uses a Kanban-based workflow: **Backlog → Planned → Ready → Doing → Testing → Done**

Key principles:
- **Plan first** with 97%+ confidence before execution
- **Track time** by moving through Doing status
- **Test comprehensively** with edge case coverage
- **Document results** in walkthroughs for phases

## Trigger Word Rules

> [!IMPORTANT]
> **When user mentions these words, STOP and read the linked document FIRST:**

| User Says | Required Action |
|-----------|-----------------|
| "bump version", "release", "changelog" | READ `09_release.md` → Follow full release checklist |
| "commit", "attach commit" | Use `flowcrate commit <id>` (NOT `flowcrate link`) |
| "link plan", "attach plan" | Use `flowcrate update <id> --plan "path"` |
| "done", "mark done" | Check walkthrough linked → then `flowcrate move <id> done` |
| "push to workspace", "sync" | Check linked workspace status first |

## Section Organization

This workflow guide is split into focused modules:

0. **Session Rules** - [00_session_rules.md](./workflow/00_session_rules.md) - Pre-flight checks, session start rules
1. **Stages** - [01_stages.md](./workflow/01_stages.md) - Kanban stage definitions and rules
2. **Plan Standards** - [02_plan_standards.md](./workflow/02_plan_standards.md) - Quality requirements, confidence scoring
3. **Phased Execution** - [03_phased_execution.md](./workflow/03_phased_execution.md) - Breaking complex work into phases
4. **Edge Case Testing** - [04_edge_testing.md](./workflow/04_edge_testing.md) - Comprehensive test coverage requirements
5. **Safe Execution** - [05_safe_execution.md](./workflow/05_safe_execution.md) - Dry-run, backup, rollback strategies
6. **CLI Reference** - [06_cli_reference.md](./workflow/06_cli_reference.md) - flowcrate command examples
7. **Linking Rules** - [07_linking.md](./workflow/07_linking.md) - Plan/walkthrough artifact management
8. **Revision Workflow** - [08_revision.md](./workflow/08_revision.md) - Handling changes and backtracking
9. **Release Workflow** - [09_release.md](./workflow/09_release.md) - CommitID tracking, changelogs
10. **Architecture** - [10_architecture.md](./workflow/10_architecture.md) - Build verification, code organization
11. **Git Branching** - [11_git_branching.md](./workflow/11_git_branching.md) - Branch workflow, PR rules, lifecycle
12. **CLI Sync Rule** - [12_cli_sync_rule.md](./workflow/12_cli_sync_rule.md) - Auto-sync flowcrate CLI when rules are synced


## Quick Start

**Create a task:**
```bash
flowcrate create "Feature Title" -t feat -p 2 -d "Description" --json | Out-String
```

**Move to Doing (starts timer):**
```bash
flowcrate move <id> doing --json | Out-String
```

**Complete:**
```bash
flowcrate move <id> done --json | Out-String
git commit -m "feat(scope): description"
flowcrate commit <id>                    # Auto-detect from git HEAD
flowcrate commit <id> --sha <commit-sha>  # Manual SHA
```

## Critical Rules

> [!CAUTION]
> **MANDATORY: Read detailed sections before working!**
> - ALWAYS check `flowcrate list --status doing` before coding
> - NEVER skip Doing status (time tracking)
> - **NEVER leave cards in Doing after work is complete** — auto-move to Done (or Testing if manual verification needed)
> - Plans require 97%+ confidence before approval
> - **Plans MUST include confidence score** in frontmatter (e.g., `> **Confidence**: 92%`)
> - Edge cases MUST be documented in plans
> - After creating plan: `flowcrate update <id> --plan ".flowcrate/plans/PLAN_NAME.md"`
> - After creating walkthrough: `flowcrate update <id> --walkthrough ".flowcrate/walkthroughs/WALKTHROUGH_NAME.md"`
> - ⚠️ **Use relative path!** Filename-only breaks confidence score display

> [!WARNING]
> **VALID FLOWCRATE COMMANDS ONLY!**
> Do NOT invent/hallucinate commands. Valid commands are:
> - `flowcrate create` - Create new task
> - `flowcrate list` - List tasks
> - `flowcrate show <id>` - Show task details
> - `flowcrate move <id> <status>` - Move task to status
> - `flowcrate update <id> --plan/--walkthrough` - Link artifacts
> - `flowcrate checklist add/toggle/remove` - Manage checklist
> - `flowcrate commit <id>` - Attach commit SHA
> - `flowcrate time start/stop/add` - Time tracking
> 
> If unsure, run `flowcrate --help` or check `06_cli_reference.md` first!

## Task Types Reference

> Use appropriate task type when creating new tasks with `-t <type>`

| Type | Use Case | Color in GUI | Example |
|------|----------|--------------|---------|
| **feat** | New features, enhancements | Blue/Green | `flowcrate create "Add auth" -t feat` |
| **fix** | Bug fixes | Red | `flowcrate create "Fix login bug" -t fix` |
| **research** | Investigation, spike, audit | Purple/Yellow | `flowcrate create "Audit codebase" -t research` |
| **chore** | Maintenance, dependencies, tooling | Gray | `flowcrate create "Update deps" -t chore` |
| **docs** | Documentation only | Light Blue | `flowcrate create "Update README" -t docs` |
| **test** | Testing work, test infrastructure | Orange | `flowcrate create "Add E2E tests" -t test` |
| **refactor** | Code restructuring without behavior change | Cyan | `flowcrate create "Refactor utils" -t refactor` |
| **style** | Code formatting, linting fixes | Pink | `flowcrate create "Fix formatting" -t style` |

**Notes:**
- Type determines task prefix: `feat-xxxx`, `research-xxxx`, etc.
- Choose type based on PRIMARY purpose of the task
- When in doubt, use `research` for investigative work

_Detailed rules are in individual section files assembled during GEMINI.md generation._
