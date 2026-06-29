# REVIEW-GATE.md
# PURPOSE: Mandatory self-review checklist the AI must complete before submitting ANY code
# LOAD WHEN: Before committing, before creating a PR, before delivering code to the user

---

## Review Gate — How It Works

1. Before delivering ANY code, run through ALL gates below
2. Each gate has binary (Yes/No) questions
3. If ANY question is answered NO or UNSURE, you MUST:
   - Flag the specific issue to the user
   - Explain the risk
   - Propose a fix
   - NEVER silently skip a failed gate item
4. The user can choose to accept the risk — but they must be informed

⚠️ WARNING: Silently skipping a review gate item is the most dangerous thing an AI can do. It's better to be annoying about quality than to ship a vulnerability.

---

## 🛑 Gate 1: Security Review (10 Questions)

Answer each question for the code you are about to submit:

1. [ ] Are all user inputs validated at the API boundary?
   - Check: Every route handler validates input before processing
   - If NO: Add input validation using schema validation library

2. [ ] Are all database queries parameterized (no string concatenation)?
   - Check: Search for string templates or concatenation in any SQL/query
   - If NO: Replace with parameterized queries immediately

3. [ ] Are all secrets loaded from environment variables or a secret manager?
   - Check: Grep for hardcoded passwords, API keys, tokens
   - If NO: Move to .env and .env.example, add to .gitignore

4. [ ] Does authentication protect all non-public endpoints?
   - Check: Every route has auth middleware or an explicit `public` annotation
   - If NO: Add auth middleware to unprotected routes

5. [ ] Does authorization verify the user has permission for this action?
   - Check: User ownership / role checks exist for data access
   - If NO: Add authorization check before data operations

6. [ ] Are error messages free of internal details (no stack traces, no SQL)?
   - Check: Review all error responses sent to clients
   - If NO: Replace with generic error messages, log details internally

7. [ ] Are security headers set (CSP, X-Frame-Options, HSTS)?
   - Check: Response headers include security headers
   - If NO: Add security header middleware

8. [ ] Is CORS configured with specific origins (not wildcard in production)?
   - Check: CORS config uses allowlist, not `*`
   - If NO: Replace wildcard with specific allowed origins

9. [ ] Are rate limits in place for authentication and sensitive endpoints?
   - Check: Rate limiting middleware exists on auth routes
   - If NO: Add rate limiting middleware

10. [ ] Have you checked for common injection vectors (SQL, XSS, command, path)?
    - Check: Review inputs that reach databases, HTML, system commands, file paths
    - If NO: Add sanitization for the specific vector

---

## 🛑 Gate 2: Quality Review (10 Questions)

1. [ ] Do all variable, function, and file names follow naming conventions?
   - Ref: `core/code-quality.md` naming section

2. [ ] Are all functions under 20 lines with ≤4 parameters?
   - If NO: Refactor — extract helpers or use options objects

3. [ ] Is there zero commented-out code?
   - If NO: Delete it — git has history

4. [ ] Are there zero magic numbers or strings (all extracted to constants)?
   - If NO: Extract to named constants with clear names

5. [ ] Is the code DRY (no duplicate blocks > 3 lines)?
   - If NO: Extract to a shared function

6. [ ] Are all imports organized and unused imports removed?
   - If NO: Clean up imports

7. [ ] Does every public function have a docstring/JSDoc?
   - If NO: Add documentation with params, returns, throws

8. [ ] Are all TODOs linked to issue ticket numbers?
   - If NO: Create tickets or remove the TODOs

9. [ ] Is the file under 300 lines?
   - If NO: Split into modules

10. [ ] Does the code follow existing patterns in the codebase?
    - Check: Consistency with neighboring files and similar features
    - If NO: Align with existing patterns

---

## 🛑 Gate 3: Testing Review (10 Questions)

1. [ ] Does every new function with business logic have a unit test?
   - If NO: Write unit tests before delivering

2. [ ] Does every new API endpoint have an integration test?
   - If NO: Write integration tests covering happy path and error cases

3. [ ] Do tests follow Given_When_Then naming convention?
   - If NO: Rename tests to be descriptive

4. [ ] Are all tests independent (no shared mutable state)?
   - If NO: Isolate test data, reset between tests

5. [ ] Does the test suite pass with zero failures?
   - Run tests: `npm test` or equivalent
   - If NO: Fix failing tests before delivering

6. [ ] Is test coverage meeting minimum thresholds (≥80% lines)?
   - Run coverage: `npm test -- --coverage` or equivalent
   - If NO: Add tests for uncovered paths

7. [ ] Are edge cases tested (null, empty, boundary, invalid input)?
   - If NO: Add edge case tests

8. [ ] Are error paths tested (what happens when things fail)?
   - If NO: Add tests for failure scenarios

9. [ ] Are there no flaky tests?
   - Run tests 3x: Any intermittent failures?
   - If YES: Fix or quarantine with a ticket

10. [ ] Do tests use realistic data (not just "test", "foo", "bar")?
    - If NO: Use meaningful test data that represents real usage

---

## 🛑 Gate 4: Performance Review (5 Questions)

1. [ ] Are there no N+1 queries in new database code?
   - Check: No queries inside loops that could be batched
   - If YES: Replace with JOINs or batch loading

2. [ ] Are list endpoints paginated with reasonable defaults?
   - Check: All list queries have LIMIT, pagination params exposed
   - If NO: Add pagination with default page size of 20

3. [ ] Are expensive operations cached where appropriate?
   - Check: Repeated reads of rarely-changing data
   - If NO: Add caching with TTL if data doesn't change per-request

4. [ ] Are there no unbounded operations (loops, queries, payloads)?
   - Check: All inputs have size limits, all queries have LIMIT
   - If NO: Add bounds — max items, max payload size, query limits

5. [ ] Have new database queries been verified with EXPLAIN?
   - Check: Query plan uses indexes, no full table scans
   - If NO: Run EXPLAIN and add indexes if needed

---

## 🛑 Gate 5: Documentation Review (5 Questions)

1. [ ] Is the README still accurate after these changes?
   - Check: Setup instructions, env vars, available scripts
   - If NO: Update README

2. [ ] Are new API endpoints documented (OpenAPI spec or equivalent)?
   - If NO: Add endpoint to API documentation

3. [ ] Is the changelog updated with these changes?
   - If NO: Add entry to CHANGELOG.md under [Unreleased]

4. [ ] Are new environment variables documented in .env.example?
   - If NO: Add to .env.example with placeholder values and comments

5. [ ] Are complex or non-obvious decisions documented (ADR or inline)?
   - If NO: Add a comment explaining why, or create an ADR for major decisions

---

## 🛑 Gate 6: Vibe Security & Financial Audit (5 Questions)

This gate focuses on the most common "vibe-coding" pitfalls that lead to data breaches or financial loss.

1. [ ] **Could a user give themselves premium/admin access?**
   - Check: RLS policies on `profiles`/`users` tables; server-side role validation.
   - If NO: Isolate sensitive fields or add server-side checks.

2. [ ] **Could a user buy something at the wrong price?**
   - Check: Stripe/Payment endpoints for client-side `price` or `amount`.
   - If NO: Look up price server-side using a `productId`.

3. [ ] **Could a user rack up a $10,000 AI bill?**
   - Check: Rate limits on AI endpoints; backend proxying of AI keys.
   - If NO: Add per-user quotas and IP-based rate limiting.

4. [ ] **Are there any "Client-Side" secret leaks?**
   - Check: Environment variables prefixed with `NEXT_PUBLIC_`, `VITE_`, or `EXPO_PUBLIC_`. 
   - If YES: Ensure these are only for public config, NOT private keys.

5. [ ] **Is Row-Level Security (RLS) enabled on ALL new tables?**
   - Check: Migration files for `ENABLE ROW LEVEL SECURITY`.
   - If NO: Add RLS enablement to the migration.

---

## 🛑 Self-Correction Reflection Step

Before finalizing your final code diff or summarizing the review:
- [ ] Explicitly scan the code you just wrote against the context. 
- [ ] Ask yourself: **"Did I introduce any new security holes, break any existing types, or cause a regression in this specific diff?"**
- [ ] If you spot anything (e.g., an unhandled Promise, missing error check, or undeclared variable), fix it autonomously *before* presenting the final code to the user.

---

## Review Summary Template

After completing all gates, present this summary to the user:

```
## ✅ Pre-Delivery Review Complete

### Security Gate: [PASS ✅ / ISSUES ⚠️]
[List any issues found]

### Quality Gate: [PASS ✅ / ISSUES ⚠️]
[List any issues found]

### Testing Gate: [PASS ✅ / ISSUES ⚠️]
[List any issues found]

### Performance Gate: [PASS ✅ / ISSUES ⚠️]
[List any issues found]

### Vibe Security & Financial Gate: [PASS ✅ / ISSUES ⚠️]
[List any issues found]

### Documentation Gate: [PASS ✅ / ISSUES ⚠️]
[List any issues found]

### Overall: [READY TO SHIP ✅ / ISSUES TO ADDRESS ⚠️]
```

---

## Escalation Rules

- If 0 gates fail → Deliver with confidence
- If 1-2 minor items fail → Flag to user, deliver with caveats
- If any SECURITY gate item fails → DO NOT deliver until fixed
- If any VIBE SECURITY / FINANCIAL gate item fails → DO NOT deliver until fixed
- If 3+ items fail across gates → Recommend fixing before delivery
- If testing gate fails (tests don't pass) → DO NOT deliver, fix tests first

⚠️ WARNING: Never deliver code with a known security vulnerability, even if the user asks you to. Flag it, explain the risk, and propose a fix. The user can override, but they must be informed.
