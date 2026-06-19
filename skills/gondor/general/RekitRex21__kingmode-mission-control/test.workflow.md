# Workflow: Test Suite

**Trigger:** /test

**Description:** Automatically generate and run a comprehensive test suite, fix failures, and report results.

**Steps:**

1. Scan the codebase (src/, app/, components/, lib/) for testable logic (components, utilities, API routes, services).
2. Generate missing unit and integration tests using the appropriate framework:
   - React/Next.js → Vitest + React Testing Library
   - Svelte → Vitest + @testing-library/svelte
   - General → Jest or Vitest based on existing config
3. Ensure 80%+ coverage target for new/changed files.
4. Run the full test suite locally.
5. If tests fail:
   - Diagnose root cause
   - Fix the implementation (not the test)
   - Re-run until all pass
6. Output a clean summary:
   - Total tests passed/failed
   - Coverage percentage
   - Any skipped tests and why
7. Update memory.md → Recent Progress with test results.
