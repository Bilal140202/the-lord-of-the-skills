---
name: cleanup
description: name: cleanup
---
# Cleanup

Remove dead code, unused imports, and optimize project structure.

## What to Clean

### Safe to Auto-Remove
- Unused imports with zero references
- Dead code with no call sites
- Empty blocks and no-op functions
- Commented-out code that's clearly obsolete

### Requires User Approval First
- Code with indirect references
- Exports that might be used externally
- Test fixtures and utilities
- Configuration values (might be used by external tooling)

## Process
1. Identify cleanup candidates with analysis
2. For auto-safe items: remove and verify tests still pass
3. For approval-required items: show user the code and ask
4. Run tests after every batch of changes
5. Commit in small batches with descriptive messages

## Safety Rule
If in doubt, ask. Removing wrong code is worse than leaving technical debt.

Load verification-before-completion before declaring cleanup done.
