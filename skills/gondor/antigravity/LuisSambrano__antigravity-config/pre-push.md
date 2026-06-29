---
description: Security and quality gate. Run before every git push and before marking any task complete.
---

# /pre-push

Mandatory gate before every push. Not optional.

## Steps

1. Build gate
   npm run build
   Zero errors required.

2. Environment variable scan
   grep -rn "NEXT_PUBLIC_" app/ --include="*.ts" --include="*.tsx"
   Expected: any NEXT_PUBLIC_ variable must be intentionally public. Remove prefix from anything that should be server-only.

3. Secrets scan
   grep -rn "password\|api_key\|secret\|token" app/ --include="*.ts" --include="*.tsx" | grep -v process.env | grep -v "//"
   Expected: zero matches.

4. Hardcoded domain scan
   grep -rn "https://" app/ --include="*.ts" --include="*.tsx" | grep -v process.env
   Expected: domains must come from environment variables.

5. TypeScript strict check
   npx tsc --noEmit
   Zero errors required.

6. Git status
   git status --short && git log --oneline -3
   Working tree must be clean before push.

## Output format

```
Pre-push Gate: [project-name]

Build:            pass
NEXT_PUBLIC_:     0 violations
Secrets:          0 matches
Hardcoded domains: 0 matches
TypeScript:       0 errors
Git:              clean

Safe to push.
```

If any check fails:

```
Pre-push Gate FAILED: [project-name]

[check]: [violation detail]
[file:line] [offending value]

Push blocked. Fix violations before proceeding.
```
