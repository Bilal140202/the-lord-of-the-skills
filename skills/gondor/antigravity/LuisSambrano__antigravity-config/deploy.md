---
description: Deploy to production via Vercel after quality and security gates pass.
---

# /deploy

Deploys the current project to production.

## Steps

1. TypeScript: 0 errors required.
2. ESLint: 0 errors required.
3. Build: must complete successfully.
4. Security: no exposed secrets, environment variables validated.
5. Execute: vercel --prod

## Output format

```
Deploy: [project-name]

TypeScript: 0 errors
ESLint: 0 errors
Build: success
Deploy: complete
URL: https://project.vercel.app
```

If any gate fails, report the error and block deployment.
