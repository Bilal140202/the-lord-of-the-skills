# 🌿 Git Branching & PR Workflow

> [!CAUTION]
> **MANDATORY: AI agents MUST follow branching discipline before writing code!**

---

## Pre-Implementation Branch Check

Before moving any task to `Doing` or writing ANY code, AI agent MUST:

```bash
# Step 1: Check current branch
git branch --show-current

# Step 2: If on main/master, create feature branch FIRST
git checkout -b <type>/<task-id>-<short-name>
```

### Branch Naming Convention
```
<type>/<task-id>-<short-description>

# Examples:
feat/d043-branching-rules
fix/580b-sync-git-root
chore/f467-refactor-tasks
```

| Task Type | Branch Prefix | Example |
|-----------|---------------|---------|
| feat-xxxx | `feat/` | `feat/d043-user-auth` |
| bug-xxxx | `fix/` | `fix/580b-login-crash` |
| chore-xxxx | `chore/` | `chore/f467-cleanup` |
| docs-xxxx | `docs/` | `docs/abc1-api-docs` |

---

## AI Agent Enforcement Matrix

| Stage | Required Action |
|-------|-----------------|
| Before `flowcrate move <id> doing` | Check branch, create if on main |
| Before first file edit | Verify NOT on main/master |
| Before commit | Verify branch name format matches task |
| After `flowcrate move <id> done` | Merge to main, delete branch |

### Allowed Direct Main Commits
- ❌ **NEVER** for: features, bugs, refactors, complex changes
- ⚠️ **ONLY** for: trivial typo/docs fixes (1-2 lines max)

---

## Branch Lifecycle Management

> [!IMPORTANT]
> **Feature branches are TEMPORARY. Delete after merge!**

### When to Delete Branch

| Task Status | Branch Action |
|-------------|---------------|
| `done` + committed | ✅ Merge to main, delete local & remote |
| `done` + no changes | ⚠️ Check if changes exist, delete if empty |
| `cancelled/blocked` | 🗑️ Delete without merge |
| `revision needed` | Keep branch, continue work |

### Branch Cleanup Commands
```bash
# After task is Done and merged
git checkout main
git pull origin main
git branch -d <branch-name>           # Delete local
git push origin --delete <branch-name> # Delete remote (if pushed)

# List stale branches (merged but not deleted)
git branch --merged main | grep -v "main"
```

---

## PR Workflow (Remote Detection)

> [!IMPORTANT]
> **AI agent MUST detect remote status before deciding workflow!**

### Remote Detection
```bash
# Check if remote exists
git remote -v

# Possible outcomes:
# 1. No output → Local-only repo
# 2. origin → Has remote
```

### Decision Flow

```
Has Remote? (git remote -v)
├─ NO → Local-only workflow
│       └─ Direct commits to main OK
│
└─ YES → Check project type
         ├─ Solo project → Feature branch → direct push → merge local
         └─ Team project → Feature branch → PR → review → merge
```

### Workflow by Repo Type

| Repo Type | Remote? | Collaborators? | Workflow |
|-----------|---------|----------------|----------|
| Local dev | ❌ No | N/A | Direct commit OK |
| Personal project | ✅ Yes | ❌ Solo | Branch → push → merge local |
| Team project | ✅ Yes | ✅ Yes | Branch → PR → review → merge |
| Open source | ✅ Yes | ✅ Public | Fork → branch → PR to upstream |

---

## Merge Strategy

| Branch Type | Strategy | Reason |
|-------------|----------|--------|
| Feature (feat/) | **Squash** | Clean history, single commit |
| Bugfix (fix/) | **Squash** | Clean history |
| Hotfix (urgent) | **Merge** | Preserve timeline for audit |
| Release | **Merge** | Preserve all commits for changelog |

### Merge Commands
```bash
# Squash merge (default for features)
git checkout main
git merge --squash <branch-name>
git commit -m "<type>(<scope>): <description>"

# Regular merge (for releases/hotfixes)
git merge --no-ff <branch-name>
```

---

## AI Agent Post-Done Checklist

1. ✅ Verify all changes committed
2. ✅ Merge branch to main (squash or rebase)
3. ✅ Delete local branch
4. ✅ Delete remote branch (if exists)
5. ✅ Verify main branch is clean
