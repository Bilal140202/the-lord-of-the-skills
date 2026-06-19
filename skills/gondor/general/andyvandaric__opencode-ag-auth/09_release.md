### 🔗 CommitID Tracking & AI Summary

After committing code changes, attach the commit to the task:

```bash
# Attach commit to task (auto-detects HEAD)
flowcrate commit <task-id>

# Specify commit SHA manually
flowcrate commit <task-id> --sha <commit-sha>

# Attach MULTIPLE commits at once (comma-separated or repeated --sha)
flowcrate commit <task-id> --sha abc1234,def5678
flowcrate commit <task-id> --sha abc1234 --sha def5678
```

> [!NOTE]
> **Multi-Commit Support**: Tasks can have multiple commits attached. New commits are **appended** (not replaced) and stored as a JSON array. Duplicate commits are ignored.

> [!CAUTION]
> **MANDATORY: Every commit MUST be attached to a task card!**
> - After `git commit`, run `flowcrate commit <task-id>` immediately
> - No orphan commits allowed - all work must be tracked
> - AI summary auto-generated from plan/walkthrough content
> - Unattached commits = untraceable work = workflow violation

**AI Summary Generation (Automatic):**
The `flowcrate commit` command generates an AI-powered summary using this priority:

| Content Available | AI Action |
|-------------------|-----------|
| Plan + Walkthrough | Generate rich summary from both documents |
| Plan only | Generate summary from plan content |
| No plan/walkthrough | Fallback to `{type}: {commit_message}` |

**Example Output:**
```
ℹ️ Task feat-47ed already has 1 commit(s): bb43ee9
📎 Attaching 1 commit(s): cc12345
🤖 Generating AI summary from plan/walkthrough...
✅ Attached 1 commit(s) to task feat-47ed (total: 2)
📝 Summary: This task delivered a system to track Git commit IDs...
```

> [!TIP]
> The AI summary uses `gemini-2.5-flash` via Antigravity API to create concise 2-3 sentence summaries from plan/walkthrough content.

---

## 🚀 Release Workflow

> [!IMPORTANT]
> **Before any release, generate changelog from git commits**

> [!CAUTION]
> **MANDATORY: Every version bump MUST include a git tag!**
> - After `git commit -m "chore(release): vX.Y.Z"`, run `git tag vX.Y.Z` immediately
> - Missing tags = `flowcrate changelog` cannot auto-detect release boundaries
> - Push tags with `git push origin --tags`
> - No untagged releases allowed = workflow violation

### Complete Release Checklist

> [!TIP]
> **NEW: All-in-One Release Command (Recommended)**
> Use `flowcrate release` to automate the entire workflow in one command.

**Option 1: Automated Release (Recommended) ⚡**

```bash
# ═══════════════════════════════════════════════════════════════
# SINGLE COMMAND - Does everything automatically:
# ═══════════════════════════════════════════════════════════════
# ✅ Generates AI-enhanced changelog
# ✅ Bumps version in all project files
# ✅ Creates git commit
# ✅ Creates git tag
# ═══════════════════════════════════════════════════════════════

# Patch release (bug fixes) - 0.10.5 → 0.10.6
flowcrate release patch

# Minor release (new features) - 0.10.5 → 0.11.0
flowcrate release minor

# Major release (breaking changes) - 0.10.5 → 1.0.0
flowcrate release major

# Preview changes first (dry-run)
flowcrate release patch --dry-run

# Skip AI (faster)
flowcrate release patch --no-ai

# pnpm aliases (convenience)
pnpm release           # = flowcrate release patch
pnpm release:minor     # = flowcrate release minor
pnpm release:major     # = flowcrate release major
pnpm release:dry       # = flowcrate release patch --dry-run

# ═══════════════════════════════════════════════════════════════
# FINAL STEP: Push to Remote
# ═══════════════════════════════════════════════════════════════

git push && git push --tags
```

**Option 2: Manual Release (Legacy) 🔧**

```bash
# ═══════════════════════════════════════════════════════════════
# STEP 1: Generate Changelog
# ═══════════════════════════════════════════════════════════════

# Auto-detect since last version (default, recommended)
flowcrate changelog --apply

# With AI-enhanced descriptions
flowcrate changelog --ai --apply

# Preview without applying
flowcrate changelog --dry-run

# From specific version
flowcrate changelog --since v0.10.5 --apply

# Legacy: from FlowCrate tasks instead of git
flowcrate changelog --tasks -o CHANGELOG_DRAFT.md

# ═══════════════════════════════════════════════════════════════
# STEP 2: Review and Update CHANGELOG.md
# ═══════════════════════════════════════════════════════════════

# Review the generated draft
# Copy relevant sections to CHANGELOG.md
# Replace [Unreleased] with version number and date
# Format: ## [X.Y.Z] - YYYY-MM-DD

# ═══════════════════════════════════════════════════════════════
# STEP 3: Version Bump
# ═══════════════════════════════════════════════════════════════

pnpm version:patch   # 0.2.1 → 0.2.2 (bug fixes only)
pnpm version:minor   # 0.2.1 → 0.3.0 (new features)
pnpm version:major   # 0.2.1 → 1.0.0 (breaking changes)

# ═══════════════════════════════════════════════════════════════
# STEP 4: Commit Changelog + Version Changes
# ═══════════════════════════════════════════════════════════════

git add -A
git commit -m "chore(release): vX.Y.Z"

# ═══════════════════════════════════════════════════════════════
# STEP 5: Create Git Tag (MANDATORY!)
# ═══════════════════════════════════════════════════════════════

git tag vX.Y.Z    # ⚠️ NEVER skip this step!

# ═══════════════════════════════════════════════════════════════
# STEP 6: Merge to Main (if on feature branch)
# ═══════════════════════════════════════════════════════════════

git checkout main
git merge <feature-branch> --no-ff -m "Merge <branch>: vX.Y.Z"

# ═══════════════════════════════════════════════════════════════
# STEP 7: Push to Remote
# ═══════════════════════════════════════════════════════════════

git push origin main --tags
```

### Finding Last Version Bump Commit

```bash
# flowcrate changelog auto-detects (preferred)
flowcrate changelog --dry-run
# Output: 📋 Generating changelog from git commits (since v0.10.5)

# Manual: find the last tag
git describe --tags --abbrev=0

# Manual: find the last release commit
git log --oneline --grep="chore(release)" -n 1

# --since accepts version strings (auto-resolves to commit hash)
flowcrate changelog --since v0.10.5
```

### Version Bump Decision Table

| Commits Since Last Release | Version Type |
|---------------------------|--------------|
| Only `fix:` commits | `version:patch` |
| Any `feat:` commits | `version:minor` |
| Breaking changes (marked with `!`) | `version:major` |

### Changelog Format (Keep A Changelog)

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Features
- **Feature Name**: Description with AI summary. (task-id)

### Bug Fixes
- **Bug Name**: What was fixed. (task-id)

### Changed
- **Component**: What changed.

---
```

> [!TIP]
> **Pro Tips:**
> - Always run `pnpm clean` before building installers after version bump
> - Use `git log <last-tag>..HEAD --oneline` to review all commits
> - AI-generated summaries from `flowcrate changelog` are more descriptive than commit messages

