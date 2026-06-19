## 🏗️ Build Mode Rules
> **CRITICAL**: Use correct build mode to save time.

| Context | Command | Time |
|---------|---------|------|
| Development/Testing | `cargo build` | ~1-2s |
| Final Verification | `cargo build --release` | ~5min |
| CI/CD Pipeline | `cargo build --release` | ~5min |

### ❌ DO NOT
- Use `--release` for iterative development/testing
- Wait 5 minutes for release build when dev build suffices
- Do release build during feature implementation

### ✅ DO
- Use **dev build** (`cargo build`) for quick iteration
- Only use **release build** AFTER `pnpm version:*` (bump version)
- Release build is for final verification before creating release tag

---

## Auto-Approve Commands
- **flowcrate CLI**: ALL `flowcrate` commands (list, create, update, move, show, delete, time)
- Testing commands (`pytest`, `npm test`, `pnpm test`, `make test`, etc.)
- Building commands (`npm run build`, `pnpm dev`, `pnpm build`, etc.)
- Invoke commands for testing endpoints
- Linting commands, Dev server commands

## Require Review
- **Implementation**: All code changes that implement new features
- **Commit**: All git commits MUST have message reviewed

## Full Auto Agent (No Review)
- Research and exploration codebase
- Debugging and troubleshooting
- File reading and analysis
- Documentation reading
- Running tests, Building projects
- taskkill and powershell commands

---

## Commit Message Format
Use semantic release format:
- `feat(scope): description` - New features
- `fix(scope): description` - Bug fixes  
- `chore(scope): description` - Maintenance
- `docs(scope): description` - Documentation

## Pre-Commit Cleanup Rules
> **MANDATORY**: Delete temp/AI-generated files before EVERY commit.
- `*_output.txt`, `test_output.txt` - AI test output
- `digest/` folder - Code digest exports
- `*.tmp`, `*.log` - Temporary files

---

## Feature Preservation Rules
> **CRITICAL**: New features MUST preserve all existing functionality.
### ❌ DO NOT
- Remove or disable existing features when adding new ones
- Break existing data persistence
- Skip calling service methods that were previously called
- "Simplify" by removing functionality
### ✅ DO
- Review existing code flow before refactoring
- Ensure all persistence calls are preserved
- Test that old features still work after changes

## File Size & Refactoring Rules
| Lines | Status | Action |
|-------|--------|--------|
| < 500 | ✅ OK | Normal development |
| 500-800 | ⚠️ WARN | Consider splitting |
| 800-1000 | 🔴 REVIEW | Notify user, plan refactor |
| 1000+ | 🚫 BLOCK | Refactor mandatory first |

### 🔍 Audit / Refactor Approach
> [!CAUTION]
> **For audits, refactors, or redundancy removal:**
> - ❌ **DO NOT** use regex or search patterns to identify sections
> - ❌ **DO NOT** rely on heading detection (may miss context)
> - ✅ **DO** read file per 100 lines incrementally for complete understanding
> - ✅ **DO** commit changes BEFORE starting large refactors
> - ✅ **DO** document what will be removed before deletion
>
> **Rationale:** Regex/patterns can cause fatal code loss by missing context or false positives.

---

## 🏗️ Reusable Components & Clean Architecture
> **CRITICAL**: Prefer reuse over duplication.

### ♻️ Reusability Rules
1. **Dialogs**: Use `FormDialog.tsx` as the base wrapper for all modal forms.
2. **CRUD**: Use `lib/crud.ts` for all standard Task/Project operations (create, update, delete, move).
3. **Feedback**: Always use `invokeWithFeedback` (or wrappers) to ensure user gets toast notifications.

### 🧹 Clean Architecture Checklist
| Check | Action |
|-------|--------|
| **No Duplicated Constants** | Import from `lib/constants.ts` |
| **No Inline Forms** | Create separate Dialog file (e.g. `CreateTaskDialog.tsx`) |
| **No Inline API Calls** | Move to `lib/crud.ts` or service file |
| **Shared Types** | Define in `src-ui/types.ts` or component props interface |
| **i18n Ready** | Use keys for labels, not hardcoded strings |

### 🚫 Anti-Patterns to Avoid
- ❌ Hardcoding status/priority arrays in each component
- ❌ Manually invoking Tauri commands without error handling/feedback view
- ❌ Inline form logic inside complex parent components (like Header)
