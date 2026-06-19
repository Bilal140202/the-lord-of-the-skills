# Client_Acquisition_System — Prompts

> All prompts used by the 6-stage pipeline. Each file lives in `prompts/`.
> Stage that calls it → model → behavior when no LLM key is set.

---

## Live Prompts

| Name | File | Stage | Model | Variables | Fallback |
|------|------|-------|-------|-----------|----------|
| `score_fit_v1` | `prompts/score_fit_v1.md` | 03_qualify | `gpt-4o-mini` (JSON mode) | `icp_yaml`, `offer_yaml`, prospect fields | `llm.stub_response("score_fit")` — returns fit_score=78 |
| `personalize_email_v1` | `prompts/personalize_email_v1.md` | 04_outreach/personalize_email | `gpt-4o` (JSON mode) | offer fields, prospect fields, `pain_hypothesis` | Stub subject + body with placeholder hook |
| `linkedin_dm_v1` | `prompts/linkedin_dm_v1.md` | 04_outreach/linkedin_dm | `gpt-4o` (JSON mode) | offer one_liner, prospect fields | Stub DM |
| `followup_variant` | `prompts/followup_variant.md` | 04_outreach/followup_sequence | `gpt-4o-mini` (JSON mode) | `prior_subject`, `prior_body`, `days_since`, prospect fields | Stub "[DRY-RUN] Day N follow-up" subject + body |
| `prep_brief_v1` | `prompts/prep_brief_v1.md` | 05_discovery/prep_brief | `gpt-4o-mini` (JSON mode) | offer fields, prospect fields including `fit_reasoning` | Stub 1-page brief |
| `proposal_draft_v1` | `prompts/proposal_draft_v1.md` | 06_proposal/generate_draft | `gpt-4o` (JSON mode) | `call_notes`, `offer_yaml`, `confirmed_pain` | Stub 7-section proposal |

---

## Prompt Design Rules

1. **JSON-mode always.** Every prompt returns structured JSON so downstream code never parses prose.
2. **Abort path mandatory for outreach prompts.** `personalize_email_v1` must return `{"abort": true, "reason": "..."}` if it can't find a specific hook — we never spray.
3. **Compliance-neutral.** Prompts don't generate the unsubscribe footer — `shared/compliance.py` appends it deterministically post-LLM.
4. **No PII exfiltration.** Prospect data goes to the LLM via system+user messages only. Never logged raw with masked secrets.
5. **Deterministic stubs.** Every prompt has a stub fallback in `shared/llm.stub_response()` so tests + dry-runs don't need API keys.

---

## How LLM routing works

Priority order (in `shared/llm.py`):
1. `EURI_API_KEY` → `https://api.euron.one/api/v1/euri` (free 200K tokens/day)
2. `OPENROUTER_API_KEY` → `https://openrouter.ai/api/v1`
3. `OPENAI_API_KEY` → `https://api.openai.com/v1`
4. No key → `llm.stub_response()` used (dry-run-safe)

Models per task (configurable via `EURI_MODEL_*` env vars):
- Qualify + followup + brief → `gpt-4o-mini` (cheap, fast, accurate enough)
- Personalize email + DM + proposal → `gpt-4o` (quality matters, low volume)

---

**Last Updated:** 2026-04-19 — all 6 prompts live, stubs verified in dry-run
