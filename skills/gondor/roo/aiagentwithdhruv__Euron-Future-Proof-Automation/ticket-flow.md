# Workflow — Ticket Flow (Email → Classify → Draft → Approve → Send)

> **Phase:** 4 | **Owner:** Atlas | **Status:** v1 (human-in-the-loop mandatory)

---

## Objective

Turn every new support email into a classified, drafted, guardrailed ticket in an approval queue — **never auto-send**. On human approval the drafted reply is sent and the ticket is marked resolved.

---

## Agentic Loop Mapping

| Loop Step | This Workflow |
|-----------|---------------|
| **Sense** | `fetch_emails.py` — IMAP poll OR fixture file |
| **Think** | `classify_ticket.py` — LLM: intent + priority + sentiment + team |
| **Decide** | `draft_reply.py` + KB match — pick template, compose reply |
| **Act (stage 1)** | `guardrail.py` + `create_ticket.py` + `notify_team.py` — safeguard draft, store ticket, notify team |
| **Act (stage 2)** | `approval_queue.py` + `send_reply.py` — human approves, reply sends |
| **Learn** | approval edits captured in ticket store for future prompt tuning |

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| New emails | IMAP (Gmail App Password) or `--fixtures path.json` | Yes |
| Knowledge base | `knowledge/` markdown files | Yes |
| Env vars | `.env` (see `.env.example`) | Yes in real mode, optional in `--dry-run` |

## Outputs

| Output | Location |
|--------|----------|
| Tickets | `.tmp/tickets.json` (MVP) or Airtable |
| Approval queue | `.tmp/approval_queue.json` |
| Slack notifications | Slack webhook in real mode / `.tmp/slack_outbox.jsonl` in dry-run |
| Sent replies | Resend in real mode / `.tmp/sent_replies.jsonl` in dry-run |
| Run log | `runs/YYYY-MM-DD-ticket-cycle.md` |

---

## Step-by-Step SOP

### Step 1 — Fetch emails

**Tool:** `tools/fetch_emails.py`

**Real mode:**
```
python tools/fetch_emails.py --since 15 --output .tmp/new_emails.json
```
Polls `imap.gmail.com` using `IMAP_USER` + `IMAP_PASS` (**Gmail App Password ONLY**, never the real Google password).

**Dry-run / test:**
```
python tools/fetch_emails.py --fixtures .tmp/fake_emails.json --output .tmp/new_emails.json
```

**Output schema:** list of `{id, from, subject, body, received_at}`.

**Error handling:**
- Auth fail → stop, surface error (don't retry — most likely wrong App Password).
- Connection timeout → 3 retries, exponential backoff.
- Empty inbox → exit 0, log "no new emails".

---

### Step 2 — For each email

#### 2a. Classify

**Tool:** `tools/classify_ticket.py`

```
python tools/classify_ticket.py --email-json .tmp/new_emails.json --output .tmp/classified.json
```

LLM (Euri `gpt-4o-mini`, free 200K tokens/day) returns:
```json
{
  "intent": "billing | technical | refund | feedback | spam | other",
  "priority": "P1 | P2 | P3 | P4",
  "sentiment": "positive | neutral | negative | angry",
  "team": "billing | engineering | success | trust-safety | triage",
  "reasoning": "one-sentence why"
}
```

**Fallback:** If LLM key missing or call fails → keyword-based classifier (same pattern as `AI_News_Telegram_Bot/tools/rank_news.py`).

**Priority rules (fallback):**
- P1: words matching `outage|down|broken|urgent|emergency|can't login`
- P2: words matching `refund|billing error|overcharged|not working`
- P3: default for questions
- P4: feedback / thanks / newsletter

---

#### 2b. Create ticket

**Tool:** `tools/create_ticket.py`

```
python tools/create_ticket.py --input .tmp/classified.json --output .tmp/tickets.json
```

Store: Airtable if `AIRTABLE_API_KEY` set, else local JSON at `.tmp/tickets.json`. Ticket ID format: `TICKET-YYYYMMDD-HHMMSS-NNNN`.

**Fields:** id, email_id, from, subject, body_excerpt, intent, priority, sentiment, team, status (`open|awaiting-approval|approved|sent|spam`), draft, edits[], created_at, updated_at.

---

#### 2c. Draft reply

**Tool:** `tools/draft_reply.py`

```
python tools/draft_reply.py --ticket-id TICKET-... --kb ./knowledge/ --output .tmp/drafts.json
```

Load KB file matching intent (`billing.md`, `technical.md`, `refund.md`, `general.md`), pass to LLM with prompt `draft_reply_v1`, produce draft body.

**Tone:** polite, helpful, non-committal. No binding promises, no pricing quotes. If the question can't be answered safely from KB → draft says "Thanks — I've escalated this to the right team; we'll follow up within one business day." and flag `needs_human_answer=True`.

---

#### 2d. Guardrail

**Tool:** `tools/guardrail.py`

```
python tools/guardrail.py --input .tmp/drafts.json --output .tmp/guarded_drafts.json
```

**6-layer guardrail (adapted from `student-starter-kit/skills/guardrail-pipeline/`):**

1. **Policy** — draft length ≤ 2000 chars, no external URLs except approved domains.
2. **Input** — sender email stored separately; all OTHER PII stripped before LLM saw body (handled in 2a).
3. **Instructional** — prompt enforces no price quotes / no guarantees / no legal commitments.
4. **Execution** — draft text ONLY, no tool-call syntax or code blocks leaked.
5. **Output (critical):**
   - Strip PII: SSN, credit card (Luhn-pattern), phone, account numbers, DOB.
   - Block pricing: `$\d+`, `₹\d+`, `Rs\.?\s*\d+`, `£\d+`, "%discount", "will cost", "priced at", "fee is".
   - Block commitments: "guarantee", "promise", "I commit", "definitely will", "by tomorrow", "within X hours" (unless X ≥ 24).
6. **Monitoring** — every flag → append to `.tmp/guardrail_log.jsonl` with ticket_id, layer, pattern, action (strip|block|warn).

**Action on block:** mark ticket `needs_human_answer=True`, set draft to safe fallback ("Thanks for your note — a team member will reply personally within one business day."), keep raw draft for review.

---

#### 2e. Push to approval queue

Happens inside `create_ticket.py` — ticket status set to `awaiting-approval`, entry appended to `.tmp/approval_queue.json`.

---

### Step 3 — Notify team on Slack

**Tool:** `tools/notify_team.py`

```
python tools/notify_team.py --ticket-id TICKET-... 
```

In real mode: POST to `SLACK_WEBHOOK_URL` with `{ticket_id, priority, intent, team, from, subject, draft_preview, approval_cmd}`.
In dry-run: append payload to `.tmp/slack_outbox.jsonl`.

Message format:
```
:ticket: *TICKET-20260419-...* [P1 | billing]
From: alice@example.com
Subject: Double-charged on invoice 123
Team: billing
Draft preview:
  "Hi Alice, thanks for flagging this..."
Approve: python tools/approval_queue.py --approve TICKET-20260419-...
```

---

### Step 4 — Human approval

**Tool:** `tools/approval_queue.py`

List pending:
```
python tools/approval_queue.py --list
```

Show full ticket:
```
python tools/approval_queue.py --show TICKET-...
```

Edit draft (captures edit diff → learn loop):
```
python tools/approval_queue.py --edit TICKET-... --text "Final reply body"
```

Approve + send:
```
python tools/approval_queue.py --approve TICKET-...
```

On `--approve` → calls `send_reply.py` → on success marks ticket `sent` + `resolved_at=now()`.

Reject / mark spam:
```
python tools/approval_queue.py --reject TICKET-... --reason "spam|duplicate|other"
```

---

### Step 5 — Send reply

**Tool:** `tools/send_reply.py`

```
python tools/send_reply.py --ticket-id TICKET-... 
```

Real mode: POST to Resend `/emails` using `RESEND_API_KEY` and `EMAIL_FROM`. Respect In-Reply-To / References headers so the reply threads correctly.
Dry-run: append `{ticket_id, to, subject, body}` to `.tmp/sent_replies.jsonl`.

---

### Step 6 — Learn

**Captured automatically by `approval_queue.py`:**

- Every `--edit` stores `{original_draft, edited_text, ticket_id}` in `.tmp/draft_edits.jsonl`.
- Future: `tools/tune_prompt.py` analyzes edits, proposes prompt updates. (Out of scope v1.)

---

### Step 7 — Log run

Every run of `run_ticket_cycle.py` writes `runs/YYYY-MM-DD-ticket-cycle.md`:
- Inputs (fixtures path or since-minutes)
- Emails fetched
- Tickets created
- Drafts generated
- Guardrail flags
- Slack notifications sent
- Total cost
- Errors encountered

---

## Orchestrator

**Tool:** `tools/run_ticket_cycle.py`

```
python tools/run_ticket_cycle.py --dry-run --fixtures .tmp/fake_emails.json
```

Runs Steps 1 → 3 in sequence (Steps 4–5 are operator-driven, not auto). Never auto-approves, never auto-sends.

Flags:
- `--dry-run` — skip IMAP, Slack, Resend real calls; use fake sinks.
- `--fixtures PATH` — load emails from JSON instead of IMAP.
- `--limit N` — process at most N emails.

---

## Cost Estimate

| Call | Per email | Model |
|------|-----------|-------|
| Classify | ~300 input + 80 output tokens | euri/gpt-4o-mini (free) |
| Draft | ~600 input + 250 output tokens | euri/gpt-4o-mini (free) |

At Euri free tier (200K/day) ≈ **~200 tickets/day free**. Zero USD cost expected. Budget cap `$2/run` enforced via `shared/cost_tracker.py`.

---

## Known Failure Modes

| Failure | Cause | Handling |
|---------|-------|----------|
| IMAP auth fail | Wrong App Password | Stop, error — do NOT retry (rate limited) |
| LLM JSON parse fail | Model returned prose | Fallback to keyword classifier |
| Guardrail blocks draft | PII/pricing/commitment detected | Replace with safe fallback, flag for human |
| Slack webhook 404 | Bad URL | Log locally, continue (notification is non-critical) |
| Resend 422 | Missing `from` domain verified | Stop send, surface to operator |
| Fixture file missing | Wrong path | Exit 1 with clear error |

---

## Deployment

**DO NOT DEPLOY v1.** Locally test with fixtures only. Deployment checklist for v1.1:

- [ ] Gmail App Password generated + `.env` populated
- [ ] Resend domain verified + sender email configured
- [ ] Slack webhook URL configured
- [ ] Airtable base + table schema created
- [ ] n8n schedule trigger (or GitHub Actions cron) configured to run `run_ticket_cycle.py` every 2-5 min
- [ ] Alert on 3 consecutive failed runs

---

**Last updated:** 2026-04-19 | Atlas
