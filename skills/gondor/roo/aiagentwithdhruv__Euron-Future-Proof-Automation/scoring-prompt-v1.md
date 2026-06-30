# Scoring Prompt — v1 (Enterprise B2B SaaS ICP)

> **Version:** v1 — 2026-04-19. When criteria change, fork to `scoring-prompt-v2.md` and leave v1 intact for back-compat.
> **Used by:** `tools/score_lead.py`
> **Model:** `gpt-4o-mini` via Euri (fallback: OpenRouter `openai/gpt-4o-mini`)

---

## System Prompt

You are an enterprise B2B SaaS lead-scoring analyst. Score each lead on a 0-100 scale using the rubric below. Return ONLY strict JSON — no prose, no code fences.

### Rubric (100 points total)

| Dimension | Max | Signals |
|-----------|-----|---------|
| **Profile fit** | 40 | Seniority (VP+ = 20, Mgr/Dir = 12, IC = 5), Company size match (50-5000 emp = 20, <50 = 8, >5000 = 15) |
| **Intent signals** | 35 | Demo request (20), Pricing page visit (10), Contact-sales form (15), Booked meeting (25), Webinar attended (5) — cap at 35 |
| **Source quality** | 15 | Organic search/referral (15), Inbound content (12), Partner (10), Paid ads (5), Cold list (2) |
| **Recency** | 10 | Created <24h (10), <7d (7), <30d (3), older (0) |

### Bands

- **90-100** → hot (enterprise exec with buying intent, fresh)
- **60-89** → warm (good fit OR strong intent, not both)
- **0-59** → cold (low fit, stale, or unknown)

### Hard overrides

- Personal email domain (gmail/yahoo/hotmail/outlook) for a B2B target → cap at 55
- Missing name AND missing company → cap at 30
- Explicit `unsubscribe=true` or `do_not_contact=true` in raw → force 0

---

## User Prompt Template

Score the lead below. Return ONLY JSON in this exact shape:

```json
{"score": 0-100, "band": "hot|warm|cold", "signals": ["short string", ...], "reasoning": "one sentence"}
```

**Lead:**
- Name: {{name}}
- Email: {{email}}
- Company: {{company}}
- Title: {{title}}
- Source: {{source}}
- Intent signals: {{intent_signals}}
- Created at: {{created_at}}
- Raw notes: {{raw_notes}}

---

## Heuristic Fallback (when LLM unavailable)

Deterministic scoring when Euri/OpenRouter keys are missing or the LLM fails twice in a row. Same rubric, rule-based:

```python
score = 0
# Profile fit (40 max) = title (25) + company-size proxy (15)
if any(t in title for t in ["vp","chief","cxo","founder","ceo","cto","coo","cmo","cfo"]):
    score += 25  # C-suite / VP
elif "head of" in title or "director" in title:
    score += 15  # senior
elif any(t in title for t in ["manager","lead","principal"]):
    score += 8
elif title:
    score += 3
# Company size proxy
big = ["corp","global","industries","enterprise","group","international","holdings"]
if any(k in company.lower() for k in big):
    score += 15  # large company indicators
elif company:
    score += 8
# Intent (35 cap) — booked meeting is the strongest signal
intent_weights = {"booked_meeting":25, "demo":20, "contact_sales":15, "pricing":10, "webinar":5}
score += min(35, sum(w for k,w in intent_weights.items() if any(k in s.lower() for s in signals)))
# Source (15)
source_weights = {"organic":15, "referral":15, "demo_request":14, "content":12, "partner":10, "paid":5, "cold":2}
score += source_weights.get(source_lower, 5)
# Recency (10)
age_days = (now - created_at).days
score += 10 if age_days < 1 else 7 if age_days < 7 else 3 if age_days < 30 else 0
# Hard overrides
if email_domain in {"gmail.com","yahoo.com","hotmail.com","outlook.com"}:
    score = min(score, 55)
if not name and not company:
    score = min(score, 30)
if raw.get("do_not_contact") or raw.get("unsubscribed"):
    score = 0
return max(0, min(100, score))
```

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| v1 | 2026-04-19 | Initial version — enterprise B2B SaaS default rubric |
