# Prompt Library — Master Index

> Every prompt created or used across ALL automation projects is tracked here.
> When you create a prompt anywhere in this repo, add it here.

---

## How This Works

1. **Global prompts** live in `prompts/` (reusable across projects)
2. **Project prompts** live inside each project's `PROMPTS.md` (project-specific)
3. **This file** indexes everything — one line per prompt, grouped by project

---

## Global Prompts (`prompts/`)

### Automation
| Prompt | File | Description |
|--------|------|-------------|
| n8n Workflow Builder | `prompts/automation/n8n-workflow-builder.md` | Generate n8n workflow JSON from natural language |
| Webhook Orchestrator | `prompts/automation/webhook-orchestrator.md` | Design event-driven webhook pipelines |
| Batch Processor | `prompts/automation/batch-processor.md` | Process files/data in batch with error handling |

### Coding
| Prompt | File | Description |
|--------|------|-------------|
| FastAPI CRUD Generator | `prompts/coding/fastapi-crud-generator.md` | Generate full CRUD API with FastAPI |
| Code Review Checklist | `prompts/coding/code-review-checklist.md` | Structured code review with security focus |
| Refactor to Clean Arch | `prompts/coding/refactor-to-clean-arch.md` | Refactor messy code to clean architecture |
| Systematic Debug | `prompts/coding/debug-systematic.md` | Systematic debugging with hypothesis testing |

### Content
| Prompt | File | Description |
|--------|------|-------------|
| YouTube Script Writer | `prompts/content/youtube-script-writer.md` | Write engaging YouTube tutorial scripts |
| LinkedIn Post Generator | `prompts/content/linkedin-post-generator.md` | Create LinkedIn posts with hooks and CTAs |
| Course Module Designer | `prompts/content/course-module-designer.md` | Design structured course modules with exercises |

### Research
| Prompt | File | Description |
|--------|------|-------------|
| Tech Comparison | `prompts/research/tech-comparison.md` | Compare technologies with pros/cons matrix |
| Codebase Explorer | `prompts/research/codebase-explorer.md` | Explore and document an unfamiliar codebase |
| Market Research | `prompts/research/market-research.md` | Research market landscape for a product/service |

---

## Project Prompts

<!-- When a new automation project is created, add a section here -->

### AI_News_Telegram_Bot
| Prompt | Description |
|--------|-------------|
| _(no project-specific prompts yet)_ | |

### Blotato_Social_Media
| Prompt | Description |
|--------|-------------|
| _(no project-specific prompts yet)_ | |

### Salesforce_PDF_Filler
| Prompt | Description |
|--------|-------------|
| _(no project-specific prompts yet)_ | |

### Scrape Data from Google Map
| Prompt | Description |
|--------|-------------|
| _(no project-specific prompts yet)_ | |

### Futuristic_Space_Shooter
| Prompt | Description |
|--------|-------------|
| _(no project-specific prompts yet)_ | |

---


### Social-Media-Automations
| Prompt | Description |
|--------|-------------|
| _(no project-specific prompts yet)_ | |

---

## Active Projects — Dispatched to Atlas (2026-04-19)

> Each has an `ATLAS-PROMPT.md` = full build brief.

### Multi_Channel_Onboarding (Phase 3) — BUILT
| Prompt | Description |
|--------|-------------|
| `personalize_welcome_v1` | One-shot per-channel welcome copy (email + WhatsApp + Slack alert) from one JSON user profile. Template fallback when no LLM key. |
| _(deferred)_ `segment_user` | MVP uses explicit `segment` field on signup; auto-segmentation deferred to v2. |

### CRM_Automation (Phase 3) — Built 2026-04-19
| Prompt | Description |
|--------|-------------|
| `score_lead_v1` | Score lead 0-100 + band + signals + reasoning. Versioned at `CRM_Automation/workflows/scoring-prompt-v1.md`. Heuristic fallback in `tools/score_lead.py::heuristic_score()` mirrors v1 exactly. |
| `weekly_narrative` | One-paragraph weekly CRM health narrative (LLM, with deterministic-template fallback). Inline in `tools/weekly_report.py`. |
| `followup_first_touch` | First-touch email body per track (hot/warm/cold). Templated in `config/tracks.yaml` with `{{name}}`, `{{company}}`, `{{owner_first_name}}`, `{{owner_calendar_url}}` placeholders. |
| _(deferred)_ `route_decision` | Routing is deterministic (band → track + round-robin owner) — no LLM call needed. Promote to LLM-driven only when capacity-aware decisions add real value. |

### AI_Support_Ticket_System (Phase 4) — Built 2026-04-19
| Prompt | File | Description | Status |
|--------|------|-------------|--------|
| `classify_ticket_v1` | `AI_Support_Ticket_System/prompts/classify_ticket_v1.md` | Intent + priority + sentiment + team (euri/gpt-4o-mini, keyword fallback) | Live |
| `draft_reply_v1` | `AI_Support_Ticket_System/prompts/draft_reply_v1.md` | Reply using KB + tone constraints (euri/gpt-4o-mini, template fallback) | Live |
| `guardrail_check` | `AI_Support_Ticket_System/prompts/guardrail_check.md` | Reference for regex rules enforced by `tools/guardrail.py` | Reference |

### RAG_Knowledge_Chatbot (Phase 4) — Built 2026-04-19
| Prompt | File | Description | Status |
|--------|------|-------------|--------|
| `answer_with_cite_v1` | `RAG_Knowledge_Chatbot/prompts/answer_with_cite_v1.md` | Grounded answer + citations from chunks — enforces no-cite-no-send | Live |
| `clarify_question` | `RAG_Knowledge_Chatbot/prompts/clarify_question.md` | One short clarifying Q when query is ambiguous | Staged |
| `chunk_summary` | `RAG_Knowledge_Chatbot/prompts/chunk_summary.md` | One-line summary per ingested chunk | Staged |

### AI_Voice_Agent (Phase 4) — Built 2026-04-19
| Prompt | File | Description | Status |
|--------|------|-------------|--------|
| `receptionist_system_v1` | `AI_Voice_Agent/prompts/receptionist_system_v1.md` | Inbound greeting + intent flow + booking script (compiled into Vapi assistant) | Live |
| `outbound_followup_v1` | `AI_Voice_Agent/prompts/outbound_followup_v1.md` | Opted-in outbound follow-up with consent + DNC gates | Live |
| `post_call_summary` | `AI_Voice_Agent/prompts/post_call_summary.md` | Structured JSON summary + tags on every `/webhook/call_ended` | Live |

### Autonomous_Research_Agent (Phase 4) — Built 2026-04-19
| Prompt | File | Description | Status |
|--------|------|-------------|--------|
| `classify_change_v1` | `Autonomous_Research_Agent/prompts/classify_change_v1.md` | Tag each snapshot diff as pricing/launch/hire/partnership/press/site/other + one-line why-it-matters | Live |
| `rank_findings_v1` | `Autonomous_Research_Agent/prompts/rank_findings_v1.md` | Score findings 1–10 vs business context, return top N | Live |
| `write_report_v1` | `Autonomous_Research_Agent/prompts/write_report_v1.md` | Weekly Monday briefing (TL;DR → Top Findings → Per-Competitor → Watchlist) | Live |

### VPS_AI_Stack_Deploy (Phase 5)
| Prompt | Description |
|--------|-------------|
| `debug_deploy_failure` | Diagnose a failed deploy step |
| `rollback_plan` | Propose rollback given state |

### D2C_Ecommerce_Suite (Phase 6) — Built 2026-04-19
| Prompt | File | Description | Status |
|--------|------|-------------|--------|
| `order_confirmation_v1` | `D2C_Ecommerce_Suite/prompts/order_confirmation_v1.md` | Personalized order confirmation (email + WhatsApp). Strict JSON, no fabricated pricing. Template fallback when Euri is unavailable. | Live |
| `cart_recovery_v1` | `D2C_Ecommerce_Suite/prompts/cart_recovery_v1.md` | Recovery email per step (step=1 no discount / 2+3 with code). Never claims charges or reservations. | Live |
| `review_reply_positive` | `D2C_Ecommerce_Suite/prompts/review_reply_positive.md` | Warm thank-you reply for positive reviews. Auto-sends when reviewer email is present. | Live |
| `review_reply_negative` | `D2C_Ecommerce_Suite/prompts/review_reply_negative.md` | Draft make-it-right reply. Never auto-sent — queued for human approval + Slack escalation. | Live |
| `reorder_suggestion` | `D2C_Ecommerce_Suite/prompts/reorder_suggestion.md` | One-sentence explanation of a reorder qty suggestion. Numbers are deterministic — LLM only writes the human-facing reason. | Live |
| `classify_ticket_v1` | `D2C_Ecommerce_Suite/prompts/classify_ticket_v1.md` | Classify support email (intent/priority/sentiment/team) with enum whitelist. Rule-based fallback. | Live |
| `draft_reply_v1` | `D2C_Ecommerce_Suite/prompts/draft_reply_v1.md` | KB-grounded support reply. Strict "no prices, no timelines, no SLAs" contract. Post-filter strips violations. | Live |
| `classify_sentiment` | `D2C_Ecommerce_Suite/prompts/classify_sentiment.md` | Tie-break sentiment classifier used only when the rule baseline is ambiguous (3-star, star/keyword disagreement). | Live |

### Client_Acquisition_System (Phase 8) — Built 2026-04-19
| Prompt | File | Description | Status |
|--------|------|-------------|--------|
| `score_fit_v1` | `Client_Acquisition_System/prompts/score_fit_v1.md` | Score prospect 0-100 vs ICP + offer with subscores + pain hypothesis (euri/gpt-4o-mini, JSON mode, stub fallback) | Live |
| `personalize_email_v1` | `Client_Acquisition_System/prompts/personalize_email_v1.md` | Cold email subject + body with company-specific hook. Compliance footer auto-appended. Aborts if no hook found. | Live |
| `linkedin_dm_v1` | `Client_Acquisition_System/prompts/linkedin_dm_v1.md` | LinkedIn DM draft (40-80 words, no links, peer tone). Writes to `.tmp/drafts/linkedin/` — human sends. | Live |
| `followup_variant` | `Client_Acquisition_System/prompts/followup_variant.md` | Day 3 / Day 7 / Day 14 variants (bump / value-add / break-up). Scheduled into `state/followups.json`. | Live |
| `prep_brief_v1` | `Client_Acquisition_System/prompts/prep_brief_v1.md` | 1-page pre-call brief (who / pain / 3 Qs / success path / red flags) | Live |
| `proposal_draft_v1` | `Client_Acquisition_System/prompts/proposal_draft_v1.md` | 7-section proposal markdown from call notes + offer.yaml (summary / situation / approach / deliverables / timeline / investment / next steps) | Live |

---

## Adding a New Prompt

```
1. Write the prompt file using the template:
   cp prompts/templates/PROMPT_TEMPLATE.md prompts/<category>/<name>.md

2. Add it to this file under the right section

3. If it's project-specific, also add it to the project's own PROMPTS.md
```

---

**Total Prompts:** 12 global + 41 project-specific (across 10 new projects)
**Last Updated:** 2026-04-19 — D2C_Ecommerce_Suite built (Atlas); 8 prompts live (3 added: classify_ticket_v1, draft_reply_v1, classify_sentiment)
