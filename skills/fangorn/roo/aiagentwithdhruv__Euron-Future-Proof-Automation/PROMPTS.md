# AI_Support_Ticket_System — Prompts

---

## Prompts

| Name | File | Purpose | Variables | Category |
|------|------|---------|-----------|----------|
| `classify_ticket_v1` | `prompts/classify_ticket_v1.md` | Intent + priority + sentiment + team | `subject`, `body` | classification |
| `draft_reply_v1` | `prompts/draft_reply_v1.md` | Generate reply using KB + tone constraints | `first_name`, `subject`, `body`, `intent`, `team`, `kb_context` | content |
| `guardrail_check` | `prompts/guardrail_check.md` | Reference doc — rules enforced by `tools/guardrail.py` regex | — | safety |

---

## Notes

- Classifier + drafter both degrade gracefully when no LLM key is configured (keyword + template fallbacks).
- `guardrail_check` is NOT an LLM prompt — rules are enforced by deterministic regex/Luhn in `tools/guardrail.py`. The markdown file documents the rules for reviewers.
- All prompts use Euri `gpt-4o-mini` as primary, OpenRouter/OpenAI as fallbacks via the OpenAI-compatible SDK.

---

**Last Updated:** 2026-04-19
