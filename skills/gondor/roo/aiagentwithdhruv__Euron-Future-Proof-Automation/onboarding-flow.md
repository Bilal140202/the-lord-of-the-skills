# Workflow: Multi-Channel Onboarding Flow

> **Objective:** When a new user signs up, orchestrate a sequenced welcome across Email -> WhatsApp -> Slack internal alert -> scheduled Day 2 + Day 5 follow-ups. Driven by one signup trigger, powered by AI personalization.
>
> **Phase:** 3 (No-Code Automation Mastery — Week 6: Multi-Channel Communication)
> **Owner:** Atlas
> **Last Verified:** 2026-04-19

---

## Agentic Loop Mapping

| Stage | What Happens | Where |
|-------|--------------|-------|
| **Sense** | Receive signup JSON (webhook / CSV / Supabase row) | `receive_signup.py` |
| **Think** | LLM reads profile, generates per-channel copy | `personalize_copy.py` |
| **Decide** | Pick channel sequence + cadence (segment-based) | `run_onboarding.py` |
| **Act** | Email -> WhatsApp -> Slack -> queue follow-ups | `send_*.py` + `schedule_followup.py` |
| **Learn** | Log every dispatch, mark failures for next tune | `runs/*.md` |

---

## Inputs

| Field | Type | Required | Example |
|-------|------|----------|---------|
| `signup` | path to JSON file | yes | `.tmp/fake_signup.json` |
| `--dry-run` | flag | no (default off) | render + log only, no external calls |
| `--segment-override` | string | no | force segment (e.g. `enterprise`) |

### Signup payload schema (JSON)

```json
{
  "user_id": "usr_0001",
  "name": "Priya Sharma",
  "email": "priya@example.com",
  "phone": "+919876543210",
  "language": "en",
  "signup_source": "landing-page-hero",
  "product_interest": "automation-bootcamp",
  "segment": "student",
  "timezone": "Asia/Kolkata",
  "signed_up_at": "2026-04-19T10:15:00Z"
}
```

### Required `.env` keys

| Key | Used by | Required? |
|-----|---------|-----------|
| `EURI_API_KEY` | personalize_copy | optional (template fallback) |
| `RESEND_API_KEY` | send_email | required (unless `--dry-run`) |
| `EMAIL_FROM` | send_email | required (unless `--dry-run`) |
| `TWILIO_ACCOUNT_SID` + `TWILIO_AUTH_TOKEN` + `TWILIO_WHATSAPP_FROM` | send_whatsapp | required (unless `--dry-run`) |
| `SLACK_WEBHOOK_URL` | send_slack | required (unless `--dry-run`) |

---

## Outputs

| Output | Location | Purpose |
|--------|----------|---------|
| Orchestration receipt | stdout JSON | machine-parseable result |
| Run log | `runs/YYYY-MM-DD-<user_id>.md` | audit trail |
| Personalized copy | `.tmp/<user_id>/copy.json` | what got sent |
| Follow-up queue | `.tmp/followup_queue.json` | Day 2 + Day 5 scheduled tasks |

---

## Steps (numbered SOP)

### Step 1 — Receive signup
- **Tool:** `python tools/receive_signup.py --signup <path>`
- **Action:** Load JSON file, sanitize string fields, validate email + phone format.
- **Success:** Writes cleaned user dict to `.tmp/<user_id>/user.json`; stdout `{"status":"success","user_id":"..."}`.
- **Failure branch:**
  - Malformed JSON -> exit 2, log "invalid_payload"
  - Missing required field (email or name) -> exit 2, log "missing_fields"
  - Invalid email format -> exit 2, log "invalid_email"

### Step 2 — Validate + enrich user data
- **Tool:** same `receive_signup.py` (enrich inline)
- **Action:** Derive `segment` if absent (default: `student`), ensure `language` defaults to `en`, normalize phone to E.164.
- **Success:** Enriched user JSON persisted.
- **Failure branch:** Missing both language + timezone -> default to `en` + `UTC`, warn, continue.

### Step 3 — Generate personalized copy (AI)
- **Tool:** `python tools/personalize_copy.py --user .tmp/<user_id>/user.json`
- **Action:** Call Euri `gpt-4o-mini` (temp 0.7) with segment + language + product_interest. Produces 3 variants: email (subject+body), whatsapp (short message), slack (internal alert for team).
- **Success:** Writes `.tmp/<user_id>/copy.json`.
- **Failure branch:**
  - No `EURI_API_KEY` -> use deterministic template, log "llm_fallback_template".
  - LLM returns unparseable JSON -> 1 retry; on repeat -> template fallback.
  - Budget guard: skip if daily cost budget exceeded.

### Step 4 — Send welcome email (channel 1)
- **Tool:** `python tools/send_email.py --to <email> --subject <s> --body <b> [--dry-run]`
- **Action:** POST to Resend (`https://api.resend.com/emails`) with `Bearer RESEND_API_KEY`. Fallback: SMTP if `RESEND_API_KEY` missing but SMTP vars set.
- **Success:** Stdout `{"status":"success","channel":"email","receipt":"<id>"}`.
- **Failure branch:**
  - 4xx (bad request) -> log + exit 1, skip downstream channels? NO — continue with remaining channels, mark this one failed.
  - 429 rate limit -> retry once after 2s.
  - No provider keys + not dry-run -> fail fast with clear error.

### Step 5 — Send WhatsApp welcome (channel 2)
- **Tool:** `python tools/send_whatsapp.py --to <phone> --message <m> [--dry-run]`
- **Action:** POST to Twilio Messages API (`https://api.twilio.com/2010-04-01/Accounts/{SID}/Messages.json`). Auth = Basic (SID + token). Body uses `whatsapp:` prefix.
- **Success:** Returns Twilio SID.
- **Failure branch:**
  - Unapproved template (Twilio error 63016) -> log + mark degraded, do NOT crash pipeline.
  - Trial account + non-verified number (error 21608) -> warn, mark degraded.
  - Network timeout -> 1 retry.

### Step 6 — Fire internal Slack alert (channel 3)
- **Tool:** `python tools/send_slack.py --channel internal --message <m> [--dry-run]`
- **Action:** POST to `SLACK_WEBHOOK_URL`. Body: `{"text": <m>}` with signup summary (name, email, segment).
- **Success:** HTTP 200 + body `ok`.
- **Failure branch:**
  - 404 webhook -> log "slack_webhook_invalid", continue.
  - Any error here is non-blocking (internal alert is nice-to-have).

### Step 7 — Schedule Day 2 nudge
- **Tool:** `python tools/schedule_followup.py --user <id> --delay-days 2 --message <m>`
- **Action:** Append an entry to `.tmp/followup_queue.json` with `due_at` = `now + 2d`, `channel` = `email`, `status` = `pending`.
- **Success:** Returns scheduled task id.
- **Failure branch:** Write failure -> log + raise (queue corruption is a real bug).

### Step 8 — Schedule Day 5 deep-value email
- **Tool:** `python tools/schedule_followup.py --user <id> --delay-days 5 --message <m>`
- **Action:** Same as Step 7 but `delay_days=5` and `variant` = `deep-value`.

### Step 9 — Log everything
- **Action:** `run_onboarding.py` writes `runs/YYYY-MM-DD-<user_id>.md` with per-step status, duration, receipts, errors. Also emits final stdout JSON.
- **Output example:**
  ```json
  {
    "status": "success",
    "user_id": "usr_0001",
    "channels_sent": ["email", "whatsapp", "slack"],
    "channels_failed": [],
    "scheduled": ["day2-nudge", "day5-deep-value"]
  }
  ```

---

## Error-Handling Matrix

| Step | Error | Blocking? | Response |
|------|-------|-----------|----------|
| 1 | Invalid JSON | yes | Exit 2 |
| 1 | Missing email | yes | Exit 2 |
| 2 | Missing optional fields | no | Fill defaults, warn |
| 3 | LLM down / no key | no | Template fallback |
| 4 | Email send failed | no (continue) | Mark channel failed, proceed |
| 5 | WhatsApp send failed | no (continue) | Mark channel failed, proceed |
| 6 | Slack failed | no (continue) | Log only |
| 7-8 | Queue write failed | yes | Exit 1 |

**Rule:** Channel failures at Steps 4-6 are logged but do NOT abort the pipeline. Onboarding should always at least log and schedule follow-ups, even if a live channel is temporarily down.

---

## Cost Estimate (per signup)

| Tool | Cost | Notes |
|------|------|-------|
| personalize_copy (Euri) | $0.00 | Free tier 200K tokens/day |
| send_email (Resend) | $0.00 | Free tier 100/day |
| send_whatsapp (Twilio) | ~$0.005 | Trial credits cover dev |
| send_slack | $0.00 | Webhooks are free |
| **Total / run** | **< $0.01** | well under $2 per-run guard |

---

## Dry-Run Contract

`--dry-run` passed to `run_onboarding.py` must:
1. Still load + validate signup
2. Still call personalize_copy (free tier)
3. Skip ALL external network calls in Steps 4-6 (print payload instead)
4. Still write to follow-up queue (it's local)
5. Still log to `runs/`

This guarantees we can test the full pipeline without sending real messages.

---

## Test Command

```bash
python tools/run_onboarding.py --signup .tmp/fake_signup.json --dry-run
# Expected stdout:
# {"status":"success","user_id":"usr_0001","channels_sent":["email","whatsapp","slack"],"channels_failed":[],"scheduled":["day2-nudge","day5-deep-value"]}
```

---

## Deployment (not in scope — Angelina dispatches separately)

Candidate triggers once Angelina approves prod:
- n8n webhook node -> `run_onboarding.py`
- Supabase DB webhook -> HTTP endpoint wrapping this pipeline
- GitHub Actions batch mode for CSV imports

---

## Changelog

- **2026-04-19** — Initial SOP written by Atlas before any Python built.
