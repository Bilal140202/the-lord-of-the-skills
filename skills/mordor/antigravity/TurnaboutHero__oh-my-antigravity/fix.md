---
name: fix
description: Analyzes errors and proposes fixes automatically
---

# /fix Command

Analyze the provided error and propose a fix.

## Instructions

When the user runs `/fix`, do the following:

1. **Identify the Error**: Look at the most recent error message in the conversation or terminal output
2. **Analyze Root Cause**: Determine why the error occurred
3. **Propose Solution**: Provide a clear, actionable fix
4. **Implement**: If approved, apply the fix automatically

## Arguments

- `$ARGUMENTS` - Optional description of the error or file to fix

## Example Usage

```
/fix
/fix TypeError in utils.js
/fix the authentication bug
```
