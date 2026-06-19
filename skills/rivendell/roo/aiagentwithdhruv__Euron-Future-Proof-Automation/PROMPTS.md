# Autonomous_Research_Agent — Prompts

---

## Prompts

| Name | File | Purpose | Variables | Category | Status |
|------|------|---------|-----------|----------|--------|
| `classify_change_v1` | `prompts/classify_change_v1.md` | Tag each snapshot diff (pricing / launch / hire / partnership / press / site / other) with a one-line what-changed + why-it-matters | `competitor_name`, `business_context`, `diff_json` | classification | Live |
| `rank_findings_v1` | `prompts/rank_findings_v1.md` | Score classified findings 1–10 on business relevance, return top N sorted by rank | `business_context`, `findings_json`, `top_n` | ranking | Live |
| `write_report_v1` | `prompts/write_report_v1.md` | Generate Monday briefing: TL;DR → Top Findings → Per-Competitor → Watchlist | `business_context`, `date`, `ranked_findings_json`, `competitors_summary` | content | Live |

## Fallback behavior

If the primary LLM (Euri) and fallback (OpenRouter) are both unavailable, or the per-run budget cap is breached, the analyzer falls back to **rule-based classification** (keyword match + source-weighted score) and the report falls back to a **deterministic markdown template**. Cost cap: $1.00/run, hard abort.

## Guardrails enforced by the tools

- `classify_change_v1` and `rank_findings_v1` receive diffs only — never full scraped content (snapshot diff = source of truth, per CLAUDE.md).
- All inputs pass through `shared/sanitize.py::strip_pii` before LLM dispatch.
- All LLM calls gated by `shared/cost_tracker.py::check_budget` with the current `run_id`.

---

**Last Updated:** 2026-04-19 — all prompts built and exercised by test run (dry-run, rule-based fallback path).
