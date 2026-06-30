---
name: git
description: name: git
---
# Git

Git operations with intelligent commit messages.

## Smart Commit Protocol
1. Run `git status` — understand what changed
2. Run `git diff` — review actual changes
3. Stage specific files (never `git add .` blindly)
4. Generate commit message following Conventional Commits:
   - `feat:` new feature
   - `fix:` bug fix
   - `refactor:` code change without behavior change
   - `test:` test additions/changes
   - `docs:` documentation only
   - `chore:` maintenance tasks

## Commit Message Format

```
type(scope): short description

Optional longer explanation of WHY, not what.
```

## Safety Rules
- NEVER force push to main/master
- NEVER commit secrets, .env files, or credentials
- NEVER skip pre-commit hooks (--no-verify)
- NEVER amend published commits
- Always investigate before using --force

## Branch Naming
- Features: `feat/description`
- Fixes: `fix/description`
- Experiments: `experiment/description`

## Common Operations
```
git status                    # What changed
git diff                      # Review changes
git add path/to/file          # Stage specific files
git commit -m "feat: add X"   # Commit with message
git log --oneline -10         # Recent history
git stash                     # Save work temporarily
```
