## 🔧 flowcrate CLI Commands

> [!IMPORTANT]
> **Development vs Production Commands**
> 
> | Context | CLI | Notes |
> |---------|-----|-------|
> | **Production/User** | `flowcrate` | Installed CLI binary |
> | **Development** | `cargo test --lib` | For running tests during development |
> | **Development** | `pnpm tauri:dev` | For running GUI during development |
> 
> This workflow uses `flowcrate` for all task management. Development commands like `cargo test` are only for AI agents during implementation verification.

> [!IMPORTANT]
> **AI Agent CLI Best Practices**
> - **ALWAYS add `--json`** to ALL flowcrate CLI commands
> - **For full output**: Write to temp file, read with view_file, then delete:
>   ```powershell
>   flowcrate list --status backlog --json | Out-File -FilePath .flowcrate_output.json -Encoding UTF8
>   # Then use view_file tool to read .flowcrate_output.json
>   Remove-Item .flowcrate_output.json -Force
>   ```
> - **For simple commands**: Use `--json | Out-String` for inline reading
> - **ALWAYS search before creating** to prevent duplicate cards

### Session Start
```bash
flowcrate list --status ready --json | Out-String   # Find approved tasks
flowcrate list --status doing --json | Out-String   # Check in-progress
flowcrate move <id> doing --json | Out-String       # Start working
```

### Project Initialization

> [!IMPORTANT]
> **`flowcrate init` is automatically called when opening a project via GUI.**
> For CLI-only usage, manually run init before any other commands.

```bash
# Initialize a new flowcrate project (creates .flowcrate/ structure)
flowcrate init --json | Out-String

# Interactive mode (default) prompts:
# 1. Creates .flowcrate/flowcrate.db (SQLite database)
# 2. Syncs .gemini/GEMINI.md with project rules (auto)
# 3. Prompts: "📋 Generate PROJECT_STANDARDS.md? [Y/n]"

# This creates:
# - .flowcrate/flowcrate.db (SQLite database)
# - .flowcrate/PROJECT_STANDARDS.md (if prompted 'y')
# - .gemini/GEMINI.md (AI rules index)
# - .gemini/rules/ (modular rules including workflow/)
```

> [!TIP]
> **100% GUI/CLI Parity:** CLI `flowcrate init` now matches GUI's full wizard.
> Both create DB + sync rules + optionally generate PROJECT_STANDARDS.md.

### Configuration Management

```bash
# List all preferences
flowcrate config list --json | Out-String

# Get specific preference
flowcrate config get <key> --json | Out-String

# Set preference
flowcrate config set <key> <value> --json | Out-String

# Reset all preferences to defaults
flowcrate config reset --json | Out-String
```

**Available Config Keys:**
| Key | Type | Description |
|-----|------|-------------|
| `theme` | string | `light`, `dark`, `system` |
| `auto_backup_enabled` | bool | Enable scheduled backups |
| `auto_backup_frequency` | string | `daily`, `weekly`, `before_sync` |
| `backup_location` | string | Custom backup directory path |
| `editor_font_size` | int | Editor font size in pixels |
| `show_completed_tasks` | bool | Show done tasks in lists |
| `compact_mode` | bool | Use compact UI layout |

### Backup & Restore

> [!IMPORTANT]
> **Auto-backups are created before sync operations** (push/pull).
> Custom backup location is respected across all backup operations.

```bash
# Export backup to file
flowcrate backup export [-o <output>] [--include-files] [--workspace <id>] --json | Out-String

# Import backup from file
flowcrate backup import <input> [--mode replace|merge|dry-run] [--skip-existing] --json | Out-String
```

**Backup Modes:**
| Mode | Description |
|------|-------------|
| `merge` | Add new tasks, update existing (default) |
| `replace` | Clear and restore from backup |
| `dry-run` | Preview changes without applying |

### Task Management
```bash
# ALWAYS search before creating to prevent duplicates
# Search matches ALL fields: title, id, description, planLink, 
# walkthroughLink, status, type, summary, commitId, assignee, tags
flowcrate list --search "<keyword>" --json | Out-String

# Create Task (with optional description and workspace)
flowcrate create "<title>" -t <type> [-p <0-3>] [-d "<description>"] [-w "<workspace>"] --json | Out-String

# Link Plan (MANDATORY for Planned status - use relative path!)
flowcrate update <id> --plan ".flowcrate/plans/PLAN_FEAT_NAME.md" --json | Out-String

# Link Walkthrough (when moving to Done - use relative path!)
flowcrate update <id> --walkthrough ".flowcrate/walkthroughs/WLKTH_FEAT_NAME.md" --json | Out-String
# ⚠️ IMPORTANT: Filename-only (e.g., "WLKTH_FEAT_NAME.md") breaks confidence score display!

# Other Update Flags
flowcrate update <id> --title "New Title" --json | Out-String
flowcrate update <id> --description "New description" --json | Out-String
flowcrate update <id> --status "ready" --json | Out-String
flowcrate update <id> --priority 1 --json | Out-String
flowcrate update <id> --task-type "bug" --json | Out-String

# Other Commands
flowcrate list [--status <status>] [--search "term"] [--workspace <name|id>] --json | Out-String
flowcrate show <id> --json | Out-String
flowcrate move <id> <status> --json | Out-String
flowcrate delete <id> [-f] --json | Out-String
```

### Workspace Management
```bash
# List all workspaces (DO THIS at session start!)
flowcrate workspace list --json | Out-String

# Create task in specific workspace (by name or ID)
flowcrate create "<title>" -t <type> -w "Development" --json | Out-String
flowcrate create "<title>" -t <type> -w "ws-4139" --json | Out-String

# Workspace CRUD
flowcrate workspace create "<name>" --icon "📁" --color blue --json | Out-String
flowcrate workspace update <id> --name "New Name" --json | Out-String
flowcrate workspace delete <id> -f --json | Out-String

# Set default workspace for new tasks
flowcrate workspace default <workspace-id> --json | Out-String

# AI-assisted task migration to workspaces
flowcrate workspace migrate --dry-run --json | Out-String   # Preview
flowcrate workspace migrate --apply --json | Out-String     # Apply
```

> [!IMPORTANT]
> **Workspace Assignment Rules**
> 1. **ALWAYS** run `flowcrate workspace list` at session start to know available workspaces
> 2. **Infer workspace from context**:
>    - Development/coding/debugging tasks → "Development" or similar dev workspace
>    - Marketing/content tasks → "Marketing" workspace if exists
>    - User-specified workspace → Use exact workspace
> 3. **If unsure which workspace**: Ask user or use default workspace
> 4. **NEVER leave unassigned** unless user explicitly says "no workspace" or no workspaces exist

### Clone Task (Research → Implementation)
```bash
# Clone a task with new type/title/status
flowcrate clone <source-id> -t feat --title "Implement: <new title>" -s ready --json | Out-String

# What gets cloned: title, description, plan_link, priority
# What does NOT get cloned: time entries, walkthrough, commitId, summary
```

### Plans Management (Multi-Plan Support)

> [!IMPORTANT]
> **Tasks can have multiple plans linked.** Use these commands to manage plans:

```bash
# ============================================
# FIND TASKS WITH PLANS (Global View)
# ============================================

# List all tasks - shows planLink field for each
flowcrate list --json | Out-String

# Search for tasks with specific plan content
flowcrate list --search "API" --json | Out-String

# Filter by status to find planned tasks
flowcrate list --status planned --json | Out-String

# ============================================
# MANAGE PLANS FOR SPECIFIC TASK
# ============================================

# List all plans linked to a task
flowcrate plans <task-id> list --json | Out-String

# Add a plan to a task (supports multiple plans per task)
flowcrate plans <task-id> add "<plan-path>" --json | Out-String
# Example:
flowcrate plans feat-1234 add ".flowcrate/plans/PLAN_FEAT_1234_BACKEND.md" --json | Out-String
flowcrate plans feat-1234 add ".flowcrate/plans/PLAN_FEAT_1234_FRONTEND.md" --json | Out-String

# Remove a plan from a task
flowcrate plans <task-id> remove "<plan-path>" --json | Out-String
```

**GUI Support:**
- Click "+ Add Plan" button in task detail to add plans
- Hover over plan badge to show (×) remove button
- Multiple plans display as pill badges with type icons
- Use Filters sidebar to filter by "Has Plans"

### Walkthrough Management

> [!IMPORTANT]
> **Walkthroughs document completed work.** Attach when moving task to Done.

```bash
# Add walkthrough to a task (filename only, stored as basename)
flowcrate walkthrough <task-id> add "<walkthrough-path>" --json | Out-String
# Example:
flowcrate walkthrough feat-1234 add ".flowcrate/walkthroughs/WLKTH_FEAT_1234_FEATURE.md" --json | Out-String

# Remove walkthrough from a task
flowcrate walkthrough <task-id> remove --json | Out-String
```

**Storage Format:**
- **Stored**: filename only (e.g., `WLKTH_FEAT_1234_FEATURE.md`)
- **Resolved**: UI auto-resolves to `.flowcrate/walkthroughs/` for preview
- **Why basename**: Cleaner UI display, path resolution handled automatically

**GUI Support:**
- Click "Link Walkthrough..." button in task detail
- Walkthrough badge shows filename, click to preview


### Checklist Management
```bash
flowcrate checklist add <id> "<item text>" --json | Out-String    # Add item
flowcrate checklist toggle <id> <position> --json | Out-String    # Toggle done/not done
flowcrate checklist list <id> --json | Out-String                 # List all items
```

### Time Tracking
```bash
flowcrate time start <id> --json | Out-String       # Start timer
flowcrate time stop <id> --json | Out-String        # Stop timer
flowcrate time log <id> <minutes> -d "desc" --json | Out-String  # Manual entry
flowcrate time show <id> --json | Out-String        # View entries
flowcrate time delete <entry-id> --json | Out-String # Delete time entry
```

### Release Management (All-in-One Workflow)

> [!IMPORTANT]
> **`flowcrate release` automates the entire release workflow:** version bump + changelog + git commit + tag.
> Replaces old workflow (pnpm version:patch + pnpm release:tag).

```bash
# Standard releases (with AI-enhanced changelog)
flowcrate release patch --json | Out-String       # 0.10.5 → 0.10.6
flowcrate release minor --json | Out-String       # 0.10.5 → 0.11.0
flowcrate release major --json | Out-String       # 0.10.5 → 1.0.0

# Preview changes (dry run - NO modifications)
flowcrate release patch --dry-run --json | Out-String

# Skip AI changelog generation (faster)
flowcrate release patch --no-ai --json | Out-String

# Skip changelog entirely (version bump + commit + tag only)
flowcrate release patch --skip-changelog --json | Out-String

# Manual version override
flowcrate release patch --version 1.0.0 --json | Out-String

# CI/CD mode (no prompts)
flowcrate release patch --force --json | Out-String
```

**What It Does:**
1. ✅ Discovers version files (package.json, Cargo.toml, tauri.conf.json, pyproject.toml, VERSION)
2. ✅ Detects current version
3. ✅ Bumps version (semver-compliant)
4. ✅ Generates changelog (with AI enhancement by default)
5. ✅ Updates all version files in sync
6. ✅ Creates git commit: `chore(release): vX.Y.Z`
7. ✅ Creates git tag: `vX.Y.Z`

**Error Handling:**
- ❌ No git repo → "Run 'git init' first"
- ❌ No version files → "Create VERSION file or use --version flag"
- ❌ Tag exists → "Delete tag or use different bump"
- ⚠️ Uncommitted changes → Warning (use --force to skip)
- ⚠️ Version mismatch → Uses highest version, aligns all files

**Integration with pnpm:**
```bash
pnpm release        # Alias for: flowcrate release patch
pnpm release:minor  # Alias for: flowcrate release minor
pnpm release:major  # Alias for: flowcrate release major
pnpm release:dry    # Alias for: flowcrate release patch --dry-run
pnpm release:no-ai  # Alias for: flowcrate release patch --no-ai
```

**After Release:**
```bash
# Push to remote (tags + commits)
git push && git push --tags
```

**Supported Project Types:**
| Type | Version Files Discovered |
|------|-------------------------|
| Tauri App | package.json, src-tauri/Cargo.toml, tauri.conf.json |
| Rust CLI | Cargo.toml |
| Node.js | package.json |
| Python | pyproject.toml |
| Generic | VERSION file |

> [!TIP]
> **Full documentation**: See `.flowcrate/walkthroughs/WLKTH_FEAT_6D74_RELEASE_COMMAND.md`

### Changelog Generation (Standalone)

> [!NOTE]
> **Standalone changelog generation** (separate from release workflow). Supports Keep-a-Changelog and legacy formats.

```bash
# Generate from git commits (default: Keep-a-Changelog format)
flowcrate changelog --json | Out-String

# Generate with Gitmoji icons
flowcrate changelog --emoji --json | Out-String

# Generate since specific version/tag
flowcrate changelog --since v0.10.5 --json | Out-String

# Preview without AI enhancement (dry run)
flowcrate changelog --dry-run --json | Out-String

# Use AI to enhance commit descriptions
flowcrate changelog --ai --json | Out-String

# Apply directly to CHANGELOG.md
flowcrate changelog --apply --json | Out-String
flowcrate changelog --ai --apply --json | Out-String  # With AI + apply

# Use legacy FlowCrate format instead of Keep-a-Changelog
flowcrate changelog --format flowcrate --json | Out-String

# Save to custom file
flowcrate changelog -o RELEASE_NOTES.md --json | Out-String

# Generate from task cards instead of git commits
flowcrate changelog --tasks --json | Out-String
```

**Output Formats:**
| Format | Section Names | Use Case |
|--------|---------------|----------|
| `keepachangelog` (default) | Added, Changed, Deprecated, Removed, Fixed, Security | Industry standard (https://keepachangelog.com) |
| `flowcrate` | Features, Improvements, Bug Fixes, Security | Legacy FlowCrate format |

**Section Mapping:**
| Commit Type | Keep-a-Changelog | FlowCrate Legacy |
|-------------|------------------|------------------|
| `feat:` | Added | Features |
| `fix:` | Fixed | Bug Fixes |
| `refactor:`, `perf:`, `style:` | Changed | Improvements |
| `docs:` | Changed | Improvements |

**Emoji Support (Gitmoji Standard):**
| Type | Emoji | Description |
|------|-------|-------------|
| `feat:` | ✨ | New features |
| `fix:` | 🐛 | Bug fixes |
| `perf:` | ⚡ | Performance improvements |
| `refactor:` | ♻️ | Code refactoring |
| `docs:` | 📝 | Documentation |
| `test:` | ✅ | Tests |
| `chore:` | 🔧 | Maintenance |

**Examples:**
```bash
# Production release changelog (AI + emoji + Keep-a-Changelog)
flowcrate changelog --since v0.10.5 --ai --emoji --apply --json | Out-String

# Quick preview for internal review
flowcrate changelog --since HEAD~20 --dry-run --json | Out-String

# Legacy format for backward compatibility
flowcrate changelog --format flowcrate -o CHANGES.txt --json | Out-String
```

**Integration with Release Command:**
- `flowcrate release` uses `changelog` internally with:
  - `--format keepachangelog` (default)
  - `--emoji false` (default for releases)
  - `--ai true` (unless `--no-ai` specified)
  - `--apply true` (unless `--dry-run`)

### Activity Log (History Tracking)

> [!IMPORTANT]
> **Before resuming work on a task (especially from Testing → Doing)**, read the activity log to understand previous attempts and avoid repeating mistakes.

```bash
# View last 10 activity entries for a task
flowcrate activity <id> --json | Out-String

# View more entries
flowcrate activity <id> --limit 20 --json | Out-String
```

**Activity entries include:**
| Field | Description |
|-------|-------------|
| `action` | Type: `status_change`, `commit_attached`, `created`, etc. |
| `statusFrom` | Previous status (for status changes) |
| `statusTo` | New status (for status changes) |
| `commitId` | Git commit SHA (for commit events) |
| `details` | Human-readable description |
| `createdAt` | Timestamp of the activity |

**AI Agent Rules for Activity Log:**
- ✅ **READ** activity log when picking up tasks from Testing/Doing
- ✅ **CHECK** for previous failed attempts before making changes
- ✅ Activity is **auto-logged** on status changes and commit attachments
- ❌ Do NOT repeat the same fix that previously failed (read the log first!)

### RAG Search (Search Similar Done Cards)

> [!IMPORTANT]
> **BEFORE creating a new implementation plan**, search for similar Done cards to get context from past implementations.

```bash
# Search similar Done cards (use when creating plans)
flowcrate rag "authentication jwt" --limit 5 --json | Out-String

# Reindex all Done cards (run once after updating flowcrate)
flowcrate rag --reindex --json | Out-String
```

**When to Use RAG Search:**
| Scenario | Action |
|----------|--------|
| Creating new implementation plan | Search for similar features |
| Picking up Testing → Doing task | Search for related prior fixes |
| Starting work on complex feature | Get context from similar cards |

**How to Use RAG Context:**
1. Search with relevant keywords from task title/description
2. Review returned Done cards for patterns/approaches
3. Inject relevant references in plan:
   > **Reference Cards:** feat-abc1 implemented JWT auth with refresh tokens, follow similar pattern.

**AI Agent Rules for RAG:**
- ✅ **SEARCH** before creating plans for complex features
- ✅ **REFERENCE** similar Done cards in implementation plans
- ✅ Cards are **auto-indexed** when moving to done
- ❌ Do NOT skip RAG search for non-trivial features

### Rules Management (Project Stack Detection)
```bash
# Detect project tech stack (Rust, TypeScript, Python, etc.)
flowcrate rules detect --json | Out-String

# Sync rules with detected stack (updates .gemini/GEMINI.md)
flowcrate rules sync --json | Out-String

# Preview changes without modifying
flowcrate rules sync --dry-run --json | Out-String

# Force sync (overwrite local changes)
flowcrate rules sync --force --json | Out-String

# Cleanup old backups (keep last N)
flowcrate rules cleanup --keep 3 --json | Out-String
```

### Push/Pull Sync Commands

> [!IMPORTANT]
> **Ownership Semantics (Fixed in Phase 3):**
> - **Push**: SOURCE → TARGET transfer. SOURCE becomes read-only mirror, TARGET becomes owner.
> - **Pull**: Reclaim ownership from synced task.

```bash
# Push task to linked workspace
flowcrate push <task-id> "<target-workspace>" --json | Out-String

# Force re-push (update existing)
flowcrate push <task-id> "<target-workspace>" --force --json | Out-String

# Hide source task after push
flowcrate push <task-id> "<target-workspace>" --hide --json | Out-String

# Push entire workspace
flowcrate push-workspace <source-ws> <target-ws> --json | Out-String
flowcrate push-workspace <source-ws> <target-ws> --dry-run --json | Out-String  # Preview
flowcrate push-workspace <source-ws> <target-ws> --force --json | Out-String    # Force update

# Pull task (reclaim ownership)
flowcrate pull <task-id> --json | Out-String
flowcrate pull <task-id> --force --json | Out-String
flowcrate pull <task-id> --delete --json | Out-String  # Delete from source

# Linked Workspace Management
flowcrate linked list --json | Out-String              # List linked workspaces
flowcrate linked scan --json | Out-String              # Auto-detect workspaces
flowcrate linked add "<name>" "<path>" --json | Out-String  # Add workspace
flowcrate linked remove "<name>" --json | Out-String   # Remove workspace
flowcrate linked pull --workspace "<name>" --json | Out-String  # Pull all from workspace
flowcrate linked pull --workspace "<name>" --internal-workspace ws-1234 --json | Out-String  # Pull specific internal workspace

# ⚠️ DANGER: These commands DELETE data - require --force
flowcrate linked clean "<name>" --force --json | Out-String  # DELETE all tasks from linked DB
flowcrate linked reset "<name>" --force --json | Out-String  # DELETE DB file and recreate empty

# Restore full ownership (use --reset-sync ONLY, updates root repo's sync flags):
flowcrate linked clean "<name>" --reset-sync --force --json | Out-String  # Delete + reset ownership
# To ONLY reset ownership without deleting, run from SUB-REPO targeting main repo:
# cd sub-repo && flowcrate linked clean main-repo --reset-sync --force
```

**After Push:**
| Location | State | Can Edit? |
|----------|-------|-----------|
| SOURCE | `is_synced=1` | ❌ Read-only mirror |
| TARGET | `is_synced=0` | ✅ Owner, can edit |

### Priority Guidelines
| Priority | Use Case |
|----------|----------|
| P0 🔴 | Blocking bug, crash, data loss |
| P1 🟠 | Major bug, core feature broken |
| P2 🟡 | Minor bug, UX issue (default) |
| P3 🟢 | Enhancement, nice-to-have |

---

## Quick Reference

| User Says | AI Action |
|-----------|-----------|
| "ini ide bagus" / "good idea" | → Backlog |
| "buatkan plan" / "create plan" | Create plan → Planned |
| "approved" / "lanjut" / "ok" / "proceed" | → Ready (or → Doing if explicit) |
| "kerjakan sekarang" / "start now" | → Doing |
| "sudah bisa" / "works" / "bagus" / "verified" | → Done |
| "tidak sesuai" / "change X" / "revise" | Revision (see above) |
| "batal" / "cancel" | Close task with note |
| **"fix this" / "tolong fix" / "bug" / "not working"** | **Create bug card → Doing → Fix** |

---

## 🚦 Workflow Enforcement Matrix

| Current Status | User Says "fix this" | AI MUST Do |
|----------------|---------------------|------------|
| **No card exists** | - | Create card → Move to Doing → Fix |
| **Backlog** | - | Move to Doing → Fix |
| **Planned** | - | Move to Ready → Doing → Fix |
| **Ready** | - | Move to Doing → Fix |
| **Doing** | - | Already correct, proceed with fix |
| **Done** | "reopen" / "fix again" | Create NEW bug card → Doing → Fix |

> [!CAUTION]
> **FORBIDDEN TRANSITIONS:**
> - ❌ Backlog → Done (skips time tracking)
> - ❌ Ready → Done (skips time tracking)
> - ❌ No card → Done (no tracking at all)
> - ❌ Backlog → Testing (skips Doing)

---

## 📁 .flowcrate/ Directory Structure

Every project using flowcrate MUST have this structure:

```
.flowcrate/
├── flowcrate.json           # Task database (auto-generated)
├── plans/                  # Implementation plans
│   ├── PLAN_FEAT_XXXX_NAME.md   # Feature plans
│   └── PLAN_PHASE_X_NAME.md     # Phase plans
└── walkthroughs/           # Completion walkthroughs
    └── WLKTH_FEAT_XXXX_NAME.md
```

> [!CAUTION]
> **Artifact Location Rules:**
> - Implementation Plans → `.flowcrate/plans/`
> - Walkthroughs → `.flowcrate/walkthroughs/`
> - **DO NOT** write to `~/.gemini/antigravity/brain/` for project artifacts

### Naming Conventions
| Type | Format | Example |
|------|--------|---------|
| Feature Plan | `PLAN_FEAT_<ID>_<NAME>.md` | `PLAN_FEAT_DB73_TIME_TRACKING.md` |
| Bug Fix Plan | `PLAN_BUG_<ID>_<NAME>.md` | `PLAN_BUG_1234_CRASH_FIX.md` |
| Phase Plan | `PLAN_PHASE_<N>_<NAME>.md` | `PLAN_PHASE_9_RUSQLITE_MIGRATION.md` |
| Walkthrough | `WLKTH_<TYPE>_<ID>_<NAME>.md` | `WLKTH_FEAT_DB73_TIME_TRACKING.md` |

### Plan File Template
```markdown
# [Title]

> **Status**: ✅ DONE | 🚧 IN PROGRESS | 📝 PLANNING

## Goal
[Brief description]

## Proposed Changes
[File-level changes]

## Verification Plan
[How to test]
```
