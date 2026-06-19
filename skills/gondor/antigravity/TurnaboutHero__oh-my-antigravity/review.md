---
name: review
description: Performs a comprehensive code review
---

# /review Command

Perform a thorough code review on the specified file or recent changes.

## Instructions

When the user runs `/review`, do the following:

1. **Scope Identification**: Determine what code to review (file, function, or recent git diff)
2. **Quality Check**: Review for:
   - Code style and formatting
   - Potential bugs or edge cases
   - Performance issues
   - Security vulnerabilities
   - Best practices adherence
3. **Feedback**: Provide constructive feedback with specific line references
4. **Suggestions**: Offer concrete improvements with code examples

## Arguments

- `$1` - File path or "diff" for recent changes

## Example Usage

```
/review src/components/Button.tsx
/review diff
/review
```

## Review Checklist

- [ ] Naming conventions
- [ ] Error handling
- [ ] Documentation/comments
- [ ] Test coverage
- [ ] DRY principle
- [ ] Single responsibility
