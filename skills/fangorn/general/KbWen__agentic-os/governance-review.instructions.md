---
applyTo: "{AGENTS.md,CLAUDE.md,GEMINI.md,.github/copilot-instructions.md,.github/instructions/**/*.md,.agent/**/*.md,.agentcortex/**/*.md,docs/**/*.md,tests/guard/**/*.py}"
---

# Governance Review Instructions

Apply these when reviewing Agentic OS governance, workflow, adapter, and documentation changes.

- Confirm the change points to the canonical source instead of duplicating long governance text.
- Check whether new durable rules are backed by a validator, guard test, or explicit evidence requirement.
- Flag stale metadata across `docs/specs/_product-backlog.md`, `.agentcortex/context/current_state.md`, specs, and archived Work Logs.
- Prefer small, reversible changes and concrete test evidence.
- For tool adapters, verify the adapter is short, tool-specific, and redirects detailed behavior to `AGENTS.md` or `.agent/workflows/`.
