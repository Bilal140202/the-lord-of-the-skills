# Git Workflow

> Best practices for Git version control and collaboration.

---

## 🤖 AI Agent Enforcement

> [!CAUTION]
> **AI agents MUST create feature branches before implementation!**

### Pre-Code Checklist
```bash
# 1. Check current branch
git branch --show-current

# 2. If on main/master, create branch FIRST
git checkout -b <type>/<task-id>-<description>

# 3. Check remote status (affects PR workflow)
git remote -v
```

### Branch from Task ID
| Task Type | Branch Prefix | Example |
|-----------|---------------|---------|
| feat-xxxx | `feat/` | `feat/1234-user-auth` |
| bug-xxxx | `fix/` | `fix/5678-login-crash` |
| chore-xxxx | `chore/` | `chore/9abc-update-deps` |

### Post-Done Cleanup
```bash
# After task moved to done
git checkout main
git merge --squash <branch-name>
git commit -m "<type>(<scope>): <description>"
git branch -d <branch-name>
```

---

## Branch Naming

### Convention
```
<type>/<short-description>

# Examples
feat/user-authentication
fix/login-validation-error
chore/update-dependencies
docs/api-documentation
refactor/database-layer
```

### Branch Types
| Type | Purpose |
|------|---------|
| `feat/` | New features |
| `fix/` | Bug fixes |
| `chore/` | Maintenance, dependencies |
| `docs/` | Documentation only |
| `refactor/` | Code restructuring |
| `test/` | Adding/updating tests |

---

## Commit Message Format

### Semantic Commits
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Examples
```
feat(auth): add JWT refresh token support

Implemented automatic token refresh with 15-minute expiry.
Tokens are stored securely in httpOnly cookies.

Closes #123

---

fix(api): handle null response from external service

The upstream API now returns null instead of empty array
when no results found. Added null check to prevent crash.

---

chore(deps): update dependencies to latest versions
```

### Types
| Type | When to Use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `chore` | Maintenance, no code logic change |
| `docs` | Documentation only |
| `refactor` | Code restructure, no behavior change |
| `test` | Adding/modifying tests |
| `style` | Formatting, whitespace |
| `perf` | Performance improvement |

---

## Workflow Strategies

### Feature Branch Workflow
```bash
# 1. Create feature branch from main
git checkout main
git pull origin main
git checkout -b feat/new-feature

# 2. Make commits
git add .
git commit -m "feat(component): add initial structure"

# 3. Keep updated with main
git fetch origin
git rebase origin/main

# 4. Push and create PR
git push -u origin feat/new-feature
```

### Hotfix Workflow
```bash
# For urgent production fixes
git checkout main
git checkout -b fix/critical-bug
# ... fix the bug ...
git commit -m "fix(auth): prevent session hijacking"
git push -u origin fix/critical-bug
# Merge to main immediately after review
```

---

## Pull Request Process

### PR Checklist
- [ ] Code follows project style guide
- [ ] Tests pass locally
- [ ] New code has appropriate tests
- [ ] Documentation updated if needed
- [ ] No merge conflicts
- [ ] PR description explains changes

### PR Title Format
```
<type>(<scope>): <description>

# Same format as commit messages
feat(dashboard): add real-time updates
fix(api): handle rate limiting correctly
```

### PR Description Template
```markdown
## What
Brief description of what this PR does.

## Why
Reason for the change (link to issue if applicable).

## How
High-level overview of implementation approach.

## Testing
How to test these changes.

## Screenshots
If UI changes, include before/after screenshots.
```

---

## Merge Strategies

### Squash and Merge (Recommended)
- Combines all PR commits into one
- Keeps main branch history clean
- Use for feature branches

### Rebase and Merge
- Replays commits on top of main
- Preserves commit history
- Use when each commit is meaningful

### Merge Commit
- Creates merge commit
- Preserves branch history
- Use for large feature branches

---

## Release Management

### Tagging Releases
```bash
# Create annotated tag
git tag -a v1.2.0 -m "Release v1.2.0"

# Push tag
git push origin v1.2.0
```

### Version Bump
```bash
# Patch (1.2.0 → 1.2.1) - Bug fixes
pnpm version:patch

# Minor (1.2.0 → 1.3.0) - New features
pnpm version:minor

# Major (1.2.0 → 2.0.0) - Breaking changes
pnpm version:major
```

---

## Common Commands

### Daily Commands
```bash
git status              # Check working tree status
git diff               # View unstaged changes
git add .              # Stage all changes
git commit -m "msg"    # Commit with message
git push               # Push to remote
git pull --rebase      # Pull and rebase
```

### Branch Management
```bash
git branch -a          # List all branches
git checkout -b name   # Create and switch to branch
git branch -d name     # Delete local branch
git push -d origin name # Delete remote branch
```

### History
```bash
git log --oneline -n 10      # Last 10 commits, short
git log --graph --oneline    # Visual branch history
git blame file.ts            # Who changed each line
```

### Undo Changes
```bash
git checkout -- file.ts      # Discard unstaged changes
git reset HEAD file.ts       # Unstage file
git reset --soft HEAD~1      # Undo last commit, keep changes
git reset --hard HEAD~1      # Undo last commit, discard changes
```

---

## Best Practices

- ✅ Write clear, descriptive commit messages
- ✅ Keep commits atomic (one logical change per commit)
- ✅ Rebase feature branches before merging
- ✅ Delete merged branches
- ✅ Use `.gitignore` for build artifacts
- ❌ Don't commit secrets or credentials
- ❌ Don't force push to shared branches
- ❌ Don't commit large binary files
