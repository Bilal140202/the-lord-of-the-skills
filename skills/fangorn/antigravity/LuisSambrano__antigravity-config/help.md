---
description: List all available workflows and their slash commands.
---

# /help

Lists all available workflows and context-triggered skills.

## Workflows (explicit invocation)

| Command | Purpose |
|---|---|
| /status | Project health: git state, lint, build, quality metrics. |
| /deploy | Production deployment via Vercel with quality and security gates. |
| /pre-push | Security and quality gate. Run before every push. |
| /idea | Technical feasibility evaluation for a new concept or feature. |
| /issue | Autonomous research + GitHub Issue creation. |
| /trello | Trello board and card management via API. |
| /notebook | NotebookLM project memory management. |
| /til | Today I Learned - append entry to the knowledge base repo. |
| /check-security | Full OWASP-based security audit of the current project. |

## Skills (context-triggered, no explicit invocation)

Skills load automatically based on the user prompt. See skills/index.md for the full catalog.
