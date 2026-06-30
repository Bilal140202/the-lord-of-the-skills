---
description: Ralph Loop - relentless task completion enforcer
---

# /ralph

## What It Is

The **Ralph Loop** ensures tasks are completed relentlessly. No TODO left behind.

## How It Works

1. Execute the main task
2. Scan code for TODOs, FIXMEs, incomplete sections
3. If found → delegate to appropriate agent
4. Repeat until clean
5. Final verification

## Usage

```
/ralph implement user login
ralph: add payment processing
ralplan: refactor the codebase
```

## Example

**User**: `/ralph add user registration`

**System**:
```
[CodeSmith] Implementing registration...
✓ Created UserRegistration component
✓ Added form validation
✓ Connected to API

[Ralph Loop - Iteration 1]
Scanning for incomplete tasks...
Found:
  - TODO: Add email verification
  - FIXME: Handle duplicate email error

[CodeSmith] Fixing TODO: email verification...
✓ Added email verification flow

[SecurityGuard] Fixing duplicate email handling...
✓ Added proper error handling

[Ralph Loop - Iteration 2]
Scanning for incomplete tasks...
Found:
  - // Need tests for this

[Tester] Writing tests...
✓ Added registration tests

[Ralph Loop - Iteration 3]
Scanning for incomplete tasks...
✓ No TODOs found
✓ No FIXMEs found
✓ All tests passing

[Ralph] Task complete! Everything resolved.
```

## What Ralph Checks

- `TODO` comments
- `FIXME` comments
- `HACK` comments
- `XXX` comments
- Incomplete function bodies
- Missing error handling
- Missing tests
- Uncommitted changes

## Ralph + Other Modes

### ralplan
Ralph + Planning mode
```
ralplan: migrate database
```
1. Prometheus creates plan
2. Execute with Ralph Loop enforcement

### ralph ulw
Ralph + Ultrawork
```
ralph ulw: build API
```
1. Parallel execution
2. Ralph ensures completion
3. Full autonomous

## Configuration

Adjust Ralph's strictness:

```json
{
  "ralph": {
    "check_todos": true,
    "check_tests": true,
    "check_comments": true,
    "max_iterations": 10,
    "require_documentation": false
  }
}
```

---

*"Done is better than perfect, but complete is better than done."*
