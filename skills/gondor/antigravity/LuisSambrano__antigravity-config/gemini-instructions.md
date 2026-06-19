# GEMINI — Antigravity Global Rules (Template)

**Version**: 3.1.0
**Status**: Active

---

## 🌌 Core Principles

**Standard**: All technical, architectural, and operational decisions must align with [Protocol Zero](rules/protocol-zero.md).

### Core Engineering Principles

1. **Local Workspace as Source of Truth**
   - Development is performed locally.
   - GitHub serves as a mirror of the local state.
   - Final state is pushed from local to remote.

2. **Quality Standards**
   - Automated tests, builds, and linting must pass before committing or pushing code.
   - TypeScript strict mode is enabled by default.

3. **Documentation and Intent**
   - Documentation is required for all projects.
   - Architecture should be visualized when necessary (e.g., Mermaid).
   - Comments explain business logic ("Why") rather than syntax.

4. **Professional Autonomy**
   - Implementation autonomy is expected within established standards.
   - All actions and decisions must be transparent and documented.

5. **Continuous Improvement**
   - Every session aim to refine the codebase and reduce technical debt through incremental refactoring.

### Key Metrics

- **Security**: Mandatory RLS, data validation, and sanitization.
- **Accessibility**: Compliance with WCAG 2.1 AA standards.
- **Performance**: High Core Web Vitals scores.
- **Maintainability**: Clear, modular, and self-documenting code.

### Project Structure

**Standard**: Follow [architecture-standards.md](rules/architecture-standards.md)

```
project/
├── .agent/                    # Configuration and controls
│   ├── rules/
│   ├── workflows/
│   └── templates/
├── app/                       # Next.js App Router
├── components/
│   ├── ui/
│   ├── features/
│   └── layouts/
├── lib/
│   ├── api/
│   ├── utils/
│   └── hooks/
├── types/
└── README.md
```

<!-- CUSTOMIZE: Add additional README files for your preferred languages -->

### Pre-Commit Checklist (MANDATORY)

```bash
npm run build  # ✅ Must pass
npm run lint   # ✅ 0 errors
tsc --noEmit   # ✅ 0 type errors
```

---

## 🤖 AUTOMATIC BEHAVIORS (ALWAYS ACTIVE)

These behaviors apply AUTOMATICALLY without the user asking.

### 📋 Rules Reference

- [protocol-zero.md](rules/protocol-zero.md) — Philosophy
- [architecture-standards.md](rules/architecture-standards.md) — Architecture
- [code-standards.md](rules/code-standards.md) — Code
- [quality-gates.md](rules/quality-gates.md) — Quality

### 🚀 Before Writing Code (Pre-Code Gate)

**Trigger**: Before creating/editing any file

1. ✅ Verify project has `.agent/` directory
2. ✅ Verify `README.md` exists
3. ✅ Verify `tsconfig.json` with `strict: true`
4. ✅ Verify linter is configured
5. ✅ If anything is missing, create it automatically

### ✍️ While Writing Code (During-Code Gate)

#### Naming Conventions

- ✅ Components: `PascalCase.tsx`
- ✅ Pages: `page.tsx`, `layout.tsx`
- ✅ API Routes: `route.ts`
- ✅ Utilities: `camelCase.ts`
- ✅ Hooks: `use*.ts`
- ✅ Types: `*.types.ts`
- ✅ Variables: `camelCase`
- ✅ Constants: `SCREAMING_SNAKE_CASE`
- ✅ Functions: `camelCase` (verb: `fetchUser`, `createArticle`)
- ✅ Booleans: `is*`, `has*`, `can*`

#### Import Order (Automatic)

```typescript
// 1. React
import React from "react";

// 2. External libraries (alphabetical)
import { motion } from "framer-motion";

// 3. Internal (alphabetical)
import { Button } from "@/components/ui/button";

// 4. Types
import type { User } from "@/types/user.types";

// 5. Styles
import "./styles.css";
```

#### TypeScript Strict

- ✅ Never use `any` (use `unknown` + type guard)
- ✅ Interfaces for public objects
- ✅ Types for unions/intersections
- ✅ Descriptive generics (`TInput`, `TOutput`, not `T`, `U`)

#### Error Handling (Mandatory)

```typescript
// ✅ ALWAYS use try-catch in async
async function fetchUser(id: string) {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error("Error fetching user:", { id, error });
    return null;
  }
}
```

#### Comments (WHY not WHAT)

```typescript
// ✅ CORRECT: Explains WHY
// We increment here instead of useEffect to avoid re-renders
count++;

// ❌ WRONG: Explains WHAT (obvious)
// Increment the counter
count++;
```

#### JSDoc (Mandatory for Exports)

```typescript
/**
 * Fetches user data from Supabase with caching.
 *
 * @param userId - The UUID of the user
 * @returns User object or null if not found
 * @throws {Error} If Supabase client not initialized
 */
export async function fetchUser(userId: string): Promise<User | null> {
  // Implementation
}
```

### ✅ After Writing Code (Post-Code Gate)

```bash
# 1. TypeScript Type Check
tsc --noEmit

# 2. ESLint
npx eslint . --ext .ts,.tsx --max-warnings 0

# 3. Build Verification
npm run build
```

**If it fails**: Report errors to user BEFORE proceeding.

### 📝 Before Commit (Pre-Commit Gate)

**Verify**:

- ✅ No `.env` files in staging
- ✅ No hardcoded secrets
- ✅ No large files (> 10MB)
- ✅ `.gitignore` includes `node_modules/`, `.env*`, `.DS_Store`
- ✅ Commit follows conventional commits: `<type>(<scope>): <description>`
- ✅ No `console.log` in production
- ✅ No `TODO` without issue
- ✅ No commented code without reason

**Valid Commit Types**: `feat`, `fix`, `refactor`, `style`, `docs`, `test`, `chore`

### 🚀 Before Delivery (Pre-Delivery Gate)

#### Quality Summary

```bash
tsc --noEmit && \
npx eslint . --ext .ts,.tsx --max-warnings 0 && \
npm run build
```

#### UI Checklist (if applicable)

- ✅ Accessibility (alt text, labels, ARIA, contrast ≥ 4.5:1, keyboard nav)
- ✅ Responsive (375px, 768px, 1024px, 1440px)
- ✅ Dark mode (legible text, visible borders)
- ✅ SEO (title, meta description, OG tags)
- ✅ Performance (LCP < 2.5s, FID < 100ms, CLS < 0.1)

#### QA Report Format

```markdown
## 🔍 Quality Assurance Report

### ✅ Passed (X/Y checks)

- TypeScript: 0 errors
- ESLint: 0 errors, 0 warnings
- Build: Success

### ⚠️ Needs Attention (X items)

- ...

### ❌ Failed (X critical issues)

- ...

### 📝 Recommendations

1. ...
```

**Action**: Only deliver if 0 critical failures (❌)

### 🎯 Automatic Stack Detection

**Next.js**: Server Components by default, `'use client'` only when necessary, `next/image`, `next/font`.

**Supabase**: RLS on all tables, Auth SSR (`@supabase/ssr`), singleton client.

### 🚨 Severity Levels

| Level       | Label           | Examples                                 |
| ----------- | --------------- | ---------------------------------------- |
| ❌ Critical | Blocks delivery | Build fail, TS errors, secrets leaked    |
| ⚠️ High     | Needs attention | Lint warnings, Lighthouse < 90           |
| 📝 Medium   | Recommendation  | TODOs without issue, minor optimizations |

---

## 🔴 CRITICAL: Verify Before Affirm

- Run commands to verify changes (build, lint, test)
- Check file contents after edits
- Verify build passes after code changes
- Test functionality when applicable
- Confirm git status after commits

**When uncertain**: State uncertainty explicitly. Offer to research/verify. Provide sources.

---

## 🟠 CRITICAL: Premium Quality Standards

### Code Quality

- ✅ TypeScript strict mode
- ✅ Zero ESLint errors/warnings
- ✅ Comprehensive error handling
- ✅ Loading, empty, and error states
- ✅ Responsive design (mobile-first)
- ✅ Dark mode compatibility
- ✅ Accessibility (WCAG 2.1 AA)

### Never Deliver

- ❌ Placeholder solutions
- ❌ Missing error states
- ❌ Non-responsive layouts
- ❌ Accessibility violations
- ❌ Magic numbers without constants
- ❌ `console.log` in production

---

## 🟡 Progressive Enhancement

- Start simple, add complexity gradually
- **Small** (1-2 files, < 50 lines) → Proceed
- **Medium** (3-5 files, < 200 lines) → Explain first
- **Large** (> 5 files or > 200 lines) → Implementation plan required

---

## 🟡 Challenge Assumptions

**Object if**: Time > 4h, requires arch changes, could break things, unclear scope, violates best practices.

**Framework**: Acknowledge → Explain concern → Provide alternative → Ask for clarification.

---

## 🗺️ Internal Workflow Routing

<!-- CUSTOMIZE: Add your own workflows here -->

**When user says**: "Create a component..." → Read & follow `create-component.md`
**When user says**: "Deploy..." → Read & follow `deploy.md`
**When user says**: "Create a README..." → Read & follow `create-readme.md`

---

## 🔒 Security Standards

### Never Commit

- ❌ `.env` files
- ❌ API keys or secrets
- ❌ Passwords or tokens
- ❌ Private keys

### Always Use

- ✅ Environment variables
- ✅ `.gitignore` for sensitive files
- ✅ RLS policies
- ✅ Input validation
- ✅ Output sanitization

---

## 📊 Git Standards

### Conventional Commits

**Format**: `<type>(<scope>): <description>`

**Examples**:

- `feat(auth): implement SSR authentication`
- `fix(ui): correct dark mode contrast`
- `refactor(api): extract fetch logic to module`
- `docs: add project README`

---

**End of GEMINI.md**
