# GEMINI.md — Project Rules for Antigravity IDE

## Overview
This project uses a modular AI rules suite stored in `.ai-suite/`.
Follow the rules in these files to produce secure, reliable, production-quality code.

## 🔒 Security (Always Active)
Read and enforce `.ai-suite/core/security.md` in EVERY session.
Never skip security rules regardless of task type or urgency.

## 📋 Session Initialization
1. Read `.ai-suite/MASTER.md` — understand the rule system and file mapping
2. Read `.ai-suite/core/security.md` — security rules (ALWAYS)
3. Follow `.ai-suite/workflows/session-start.md` — session initialization
4. Check `dev-log.md` — understand prior session context
5. Load phase-specific files based on the user's first message (see MASTER.md)

## 📚 Companion Rule Files

### Core Rules (Always Active)
- `.ai-suite/core/security.md` — Security controls, OWASP Top 10, secrets management
- `.ai-suite/core/code-quality.md` — Naming, function design, refactoring triggers
- `.ai-suite/core/error-handling.md` — Error taxonomy, logging, retry patterns

### Phase Rules (Load by Task)
Load from `.ai-suite/phases/` based on current task:
- `01-project-init.md` — Project scaffolding and setup
- `02-requirements.md` — Scope, user stories, acceptance criteria
- `03-system-design.md` — Architecture decisions, ADRs, component boundaries
- `04-database.md` — Schema design, migrations, indexing
- `05-api-design.md` — REST conventions, contracts, status codes
- `06-frontend.md` — Components, state, accessibility, responsiveness
- `07-backend.md` — Services, DI, config, middleware
- `08-testing.md` — Test pyramid, coverage, flaky test policy
- `09-cicd.md` — Pipelines, environment promotion, rollback
- `10-observability.md` — Logging, metrics, alerting, tracing
- `11-performance.md` — Profiling, caching, load testing
- `12-maintenance.md` — Tech debt, dependencies, deprecation
- `13-documentation.md` — README, API docs, runbooks, ADRs

### Workflow Rules
- `.ai-suite/workflows/session-start.md` — Session initialization procedure
- `.ai-suite/workflows/task-handoff.md` — Context preservation between sessions
- `.ai-suite/workflows/review-gate.md` — Pre-delivery self-review checklist

## 🚦 Pre-Delivery Review
Before delivering ANY code:
1. Complete ALL gates in `.ai-suite/workflows/review-gate.md`
2. Security gate (10 questions) — blocking if failed
3. Quality gate (10 questions)
4. Testing gate (10 questions)
5. Performance gate (5 questions)
6. Documentation gate (5 questions)
7. Flag all failures to the user — never skip silently

## ⚠️ Non-Negotiable Rules
- NEVER hardcode secrets in source code
- NEVER use string concatenation in SQL queries
- NEVER expose internal error details to users
- NEVER skip the security review gate
- ALWAYS validate user input server-side
- ALWAYS handle errors explicitly
- ALWAYS use parameterized database queries
- ALWAYS check authentication and authorization

## 🛠️ Project-Specific Configuration
<!-- Add project-specific rules, tech stack preferences, and overrides below -->
<!-- Example: -->
<!-- - This project uses Next.js 14 with App Router -->
<!-- - Use Supabase for database and authentication -->
<!-- - All API routes go in src/app/api/ -->
