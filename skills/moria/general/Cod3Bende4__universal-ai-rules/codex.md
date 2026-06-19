# CODEX CLI ADAPTER
# PURPOSE: Ready-to-use AGENTS.md template for OpenAI Codex CLI
# LOAD WHEN: Setting up the AI rules suite in a project using OpenAI Codex CLI

---

## Setup Instructions

1. Copy the template below into `AGENTS.md` at the project root
2. Ensure the `.ai-suite/` directory exists with all rule files
3. Codex CLI reads AGENTS.md for project-specific agent instructions

---

## AGENTS.md Template

```markdown
# AGENTS.md — Project Rules for Codex CLI

## Rule System
This project uses a comprehensive AI rules suite stored in `.ai-suite/`.
These rules produce secure, reliable, production-quality code.

## Session Start
1. Read `.ai-suite/MASTER.md` — understand the rule system
2. ALWAYS read `.ai-suite/core/security.md` — security is mandatory
3. Follow `.ai-suite/workflows/session-start.md` Steps 1-5
4. Load phase files from `.ai-suite/phases/` based on the current task

## Core Rules (Always Active)
- `.ai-suite/core/security.md` — OWASP Top 10, secrets, input validation
- `.ai-suite/core/code-quality.md` — Naming, functions, file structure
- `.ai-suite/core/error-handling.md` — Errors, logging, retries

## Phase Rules (Load by Task)
| Task | File |
|---|---|
| New project | `.ai-suite/phases/01-project-init.md` |
| Requirements | `.ai-suite/phases/02-requirements.md` |
| Architecture | `.ai-suite/phases/03-system-design.md` |
| Database | `.ai-suite/phases/04-database.md` |
| API design | `.ai-suite/phases/05-api-design.md` |
| Frontend | `.ai-suite/phases/06-frontend.md` |
| Backend | `.ai-suite/phases/07-backend.md` |
| Testing | `.ai-suite/phases/08-testing.md` |
| CI/CD | `.ai-suite/phases/09-cicd.md` |
| Monitoring | `.ai-suite/phases/10-observability.md` |
| Performance | `.ai-suite/phases/11-performance.md` |
| Maintenance | `.ai-suite/phases/12-maintenance.md` |
| Documentation | `.ai-suite/phases/13-documentation.md` |

## Pre-Delivery Checklist
Before completing any task, run ALL gates in `.ai-suite/workflows/review-gate.md`:
- Security gate (10 questions) — blocking
- Quality gate (10 questions)
- Testing gate (10 questions)
- Performance gate (5 questions)
- Documentation gate (5 questions)

## Critical Rules
- NEVER hardcode secrets — environment variables only
- NEVER concatenate strings in SQL — parameterized queries only
- NEVER expose internal errors to users — generic messages only
- ALWAYS validate input server-side — client validation is UX only
- ALWAYS run review gates before delivery — flag failures explicitly

## Session End
Follow `.ai-suite/workflows/task-handoff.md` to save context.
```

---

## Codex CLI-Specific Notes

- Codex CLI reads `AGENTS.md` from the project root
- Codex supports sandboxed execution — test commands can run safely
- Keep AGENTS.md focused on rules — detailed content lives in `.ai-suite/`
- Codex works well with explicit, step-by-step instructions
- For multi-file tasks, reference specific `.ai-suite/` files for detailed rules
