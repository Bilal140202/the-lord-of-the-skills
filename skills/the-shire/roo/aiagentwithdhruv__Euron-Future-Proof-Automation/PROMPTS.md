# CRM_Automation — Prompts

> Project-specific prompts. When a prompt evolves materially, fork to a new version
> file (e.g. `scoring-prompt-v2.md`) and leave the prior version intact for back-compat.

---

## Prompts

| Name | File | Purpose | Variables | Category |
|------|------|---------|-----------|----------|
| `score_lead_v1` | `workflows/scoring-prompt-v1.md` | Score lead 0-100 with reasoning + band | `name, email, company, title, source, intent_signals, created_at, raw_notes` | classification |
| `weekly_narrative` | inline in `tools/weekly_report.py` | One-paragraph narrative summarizing the week | `stats_json, source` | report |
| `followup_first_touch` | `config/tracks.yaml` | First-touch email per track | `name, company, owner_first_name, owner_calendar_url` | content |

---

## Versioning

- `score_lead_v1` is the active scoring rubric (B2B SaaS ICP, 4-dimension 100-point scale).
- When the rubric is materially edited (new dimension, threshold change, new override), fork to v2 — `tools/score_lead.py` reads from `workflows/scoring-prompt-v1.md` by default.
- Heuristic fallback in `tools/score_lead.py::heuristic_score()` mirrors v1 exactly. Update both when v1 evolves.

---

## How To Add a New Prompt

1. Add the prompt content to either:
   - `workflows/<name>-vN.md` (versioned, scoring-style)
   - `config/<name>.yaml` (templated, content-style)
   - inline in the consuming tool (one-off)
2. Add a row to the table above
3. Add a one-liner under `### CRM_Automation` in the root `PROMPTS.md`

---

**Last Updated:** 2026-04-19
