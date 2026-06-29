# Agent Global Rules

Version: 4.0.0

Read rules/protocol.md before executing any task. This file is a condensed reference.

## Core Directives

1. Local codebase is the source of truth.
2. Read rules/protocol.md before planning.
3. Load relevant skills from skills/ based on the user prompt.
4. For frontend tasks, locate DESIGN.md in the project root. Fallback: minimalist layout, readable contrast, scale 0.98 on tap.
5. Follow GitOps Continuous Commit after task completion.

## Skill Loading

Skills in skills/ are loaded autonomously based on task context:
- UI tasks -> skills/web/design-system
- Next.js tasks -> skills/web/nextjs
- React tasks -> skills/web/react
- Performance tasks -> skills/web/web-vitals
- AI tasks -> skills/ai/
- Security tasks -> skills/core/api-security or skills/core/pentest
- Automation tasks -> skills/tools/

## Slash Commands

/status -> workflows/status.md
/deploy -> workflows/deploy.md
/pre-push -> workflows/pre-push.md
/idea -> workflows/idea.md
/issue -> workflows/issue.md
/trello -> workflows/trello.md
/notebook -> workflows/notebook.md
/til -> workflows/til.md
/check-security -> workflows/check-security.md
/help -> workflows/help.md
