# Agent Instructions

Version: 4.0.0

This file is the global configuration entry point. Read rules/protocol.md before executing any task.

## Engineering Principles

Local workspace is the source of truth. GitHub is a synchronization layer only.
TypeScript strict mode is enabled by default.
Documentation is required for all projects.
Comments explain business logic (why), not syntax (what).
Every session must reduce technical debt through incremental refactoring.

## Quality Gates

### Pre-Code
Before creating or editing any file:
- Verify project has a rules or .agent directory.
- Verify README.md exists.
- Verify tsconfig.json with strict: true.
- Verify linter is configured.
- If any item is missing, create it automatically.

### During Code

Naming:
- Components: PascalCase.tsx
- Pages: page.tsx, layout.tsx
- API routes: route.ts
- Utilities: camelCase.ts
- Hooks: use*.ts
- Types: *.types.ts
- Constants: SCREAMING_SNAKE_CASE
- Booleans: is*, has*, can*

Import order:
1. React
2. External libraries (alphabetical)
3. Internal modules (alphabetical)
4. Types
5. Styles

TypeScript:
- Never use any. Use unknown with type guard.
- Interfaces for public objects.
- Types for unions and intersections.
- Descriptive generics (TInput, TOutput).

Error handling: Always use try-catch in async functions. Return null on failure, never swallow errors silently.

Comments: Explain why, not what. JSDoc required for all exported functions.

### Post-Code
tsc --noEmit
npx eslint . --ext .ts,.tsx --max-warnings 0
npm run build

Report all errors to the user before proceeding.

### Pre-Commit
- No .env files in staging.
- No hardcoded secrets or API keys.
- No large files over 10MB.
- .gitignore includes node_modules/, .env*, .DS_Store.
- No console.log in production code.
- No TODO without a linked issue.
- No commented-out code without explanation.
- Commit format: type(scope): description

### Pre-Delivery
UI checklist:
- Accessibility: alt text, labels, ARIA, contrast >= 4.5:1, keyboard navigation.
- Responsive: 375px, 768px, 1024px, 1440px.
- Dark mode: legible text, visible borders.
- SEO: title, meta description, OG tags.
- Performance: LCP < 2.5s, FID < 100ms, CLS < 0.1.

## Workflow Routing

User says: create a component -> follow workflows/
User says: deploy -> follow workflows/deploy.md
User says: /status -> follow workflows/status.md
User says: /pre-push -> follow workflows/pre-push.md
User says: /idea -> follow workflows/idea.md
User says: /issue -> follow workflows/issue.md
User says: /trello -> follow workflows/trello.md
User says: /notebook -> follow workflows/notebook.md
User says: /til -> follow workflows/til.md
User says: /check-security -> follow workflows/check-security.md

## Stack Defaults

Next.js: Server Components by default. Use client directive only when required. Use next/image and next/font.
Supabase: RLS on all tables. Auth via @supabase/ssr. Singleton client.

## Security

Never commit: .env files, API keys, tokens, passwords, private keys.
Always use: environment variables, .gitignore for sensitive files, RLS policies, input validation, output sanitization.

## Severity Reference

CRITICAL: Blocks delivery. Build failure, TypeScript errors, secrets leaked.
HIGH: Needs attention before merge. Lint warnings, Lighthouse below 90.
MEDIUM: Recommendation. Minor optimizations, TODOs without issues.
