---
name: review
description: name: review
---
# Review

Code review against plan, requirements, and quality standards.

Load code-reviewer agent for the full process.

## Review Checklist

### Plan Compliance
- [ ] Does the implementation match what was planned?
- [ ] Are all acceptance criteria met?
- [ ] Any scope creep (things added that weren't planned)?

### Code Quality
- [ ] Is the code readable without needing comments to explain it?
- [ ] Are functions doing one thing?
- [ ] Is error handling present at system boundaries?
- [ ] Are there tests for the new behavior?

### Security
- [ ] Any user input that isn't validated?
- [ ] Any secrets or credentials in the code?
- [ ] Any new endpoints missing authorization?

### Performance
- [ ] Any N+1 queries (loop containing a database call)?
- [ ] Any synchronous blocking I/O in an async context?
- [ ] Any unbounded data fetching (missing LIMIT on queries)?
- [ ] Any unnecessary re-computation inside loops?

## Issue Severity
- **Critical**: Blocks shipping — security vulnerabilities, broken functionality
- **High**: Should fix before shipping — significant quality issues
- **Medium**: Fix soon — technical debt, missing tests
- **Low**: Nice to have — style, minor improvements

## Example Review Output

```
=== CODE REVIEW ===
Task reviewed: [task N from plan]
Reviewer: code-reviewer agent

PLAN COMPLIANCE: PASS
- All acceptance criteria met
- No scope creep detected

CODE QUALITY: 2 issues
- MEDIUM: auth.js:45 — function is 87 lines, extract token validation to separate function
- LOW: Missing error message context in catch block at user.js:102

SECURITY: PASS (no auth/input handling changes)

PERFORMANCE: PASS

OVERALL: APPROVED WITH SUGGESTIONS
Blocker count: 0 | Suggestions: 2
```
