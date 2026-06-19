---
description: Project health report — git state, quality checks, and actionable recommendations.
---

# /status

Generates a project health report.

## Steps

1. TypeScript: run tsc --noEmit. Report error count.
2. ESLint: run npx eslint . --ext .ts,.tsx. Report error and warning count.
3. Build: run npm run build. Report pass/fail.
4. Git: run git status --short and git log --oneline -5.
5. If applicable: accessibility score, Core Web Vitals, SEO metadata.

## Output format

```
Status: [project-name]

PASSED
- TypeScript: 0 errors
- ESLint: 0 errors
- Build: success
- Git: clean, synced with origin/main

NEEDS ATTENTION
- Performance: 78/100 (oversized hero asset)

RECOMMENDATIONS
1. Convert hero image to WebP.
```
