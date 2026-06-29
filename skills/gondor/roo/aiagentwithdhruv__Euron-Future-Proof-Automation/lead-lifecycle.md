# Workflow: Lead Lifecycle (Score → Route → Follow-up → Stage → Report)

> **Objective (one sentence):** Auto-score new leads, route to the right owner with the right track, fire first-touch + create tasks + advance stage, and ship a weekly health report — hands-off.

---

## Inputs

| Input | Type | Required | Default |
|-------|------|----------|---------|
| `--source` | string | yes | — (one of `airtable` \| `hubspot` \| `zoho`) |
| `--since` | ISO date | no | reads `.tmp/last_run.json`, falls back to 7 days ago |
| `--dry-run` | bool | no | `false` (no writes to CRM, no emails sent) |
| `--max-leads` | int | no | `50` (per-cycle cap to bound cost) |

---

## Tools (in execution order)

1. `tools/fetch_leads.py` — Pull new/changed leads from the chosen CRM since last run
2. `tools/score_lead.py` — Score each lead 0-100 (LLM via Euri, fallback heuristic)
3. `tools/route_lead.py` — Assign owner + pick follow-up track from score
4. `tools/update_crm.py` — Write score, owner, stage back into CRM
5. `tools/send_followup.py` — Send first-touch email per track (Resend)
6. `tools/advance_stage.py` — Move stage forward where eligible
7. `tools/run_crm_cycle.py` — Orchestrates 1-6, idempotent
8. `tools/weekly_report.py` — Friday 09:00 — markdown + Slack

---

## Steps (Numbered SOP)

### Step 1 — Fetch new leads since last run
```bash
python tools/fetch_leads.py --source $SOURCE --since-state .tmp/last_run.json --output .tmp/new_leads.json
```
- Reads `last_run_at` from `.tmp/last_run.json` (creates if missing → defaults to T-7d)
- Filters out lead IDs already in `processed_lead_ids[source]` (defensive idempotency)
- Caps results at `--max-leads`
- Output: `.tmp/new_leads.json` — array of normalized lead dicts

### Step 2 — Score each lead (LLM)
```bash
python tools/score_lead.py --input .tmp/new_leads.json --output .tmp/scored_leads.json
```
- Loads scoring prompt from `workflows/scoring-prompt-v1.md`
- LLM via Euri (`gpt-4o-mini`) — 1 call per lead, batched 10 at a time
- Returns `{score: int 0-100, reasoning: str, signals: list[str]}` per lead
- Falls back to deterministic heuristic if Euri key missing or call fails
- Cost: ~$0.001 per lead

### Step 3 — Route by score
```bash
python tools/route_lead.py --input .tmp/scored_leads.json --output .tmp/routed_leads.json
```
- **Score ≥ 90** → `hot` → owner from round-robin → track `first_call_24h`
- **Score 60-89** → `warm` → owner from round-robin → track `nurture_5_email`
- **Score < 60** → `cold` → no human owner → track `long_drip_monthly`
- Owner pool from `config/owners.yaml`; pointer persisted in `.tmp/owner_pointer.json`
- Capacity cap from `config/owners.yaml.max_open_leads_per_owner` (skips full owners)

### Step 4 — Update CRM with score + owner + stage
```bash
python tools/update_crm.py --source $SOURCE --input .tmp/routed_leads.json
```
- Writes `score`, `owner_email`, `track`, `stage` fields to each lead
- Stage field name resolved via `config/stages.yaml` (per-CRM mapping)
- Skipped entirely if `--dry-run`

### Step 5 — Fire first-touch email per track
```bash
python tools/send_followup.py --input .tmp/routed_leads.json --touch first
```
- Looks up template from `config/tracks.yaml[track].touches[0]`
- Renders Jinja-style placeholders (`{{name}}`, `{{company}}`, `{{owner_first_name}}`)
- Sends via Resend; logs message_id back into the lead record
- Skipped if `--dry-run` (just logs what *would* send)

### Step 6 — Create owner task + schedule next touchpoint
```bash
python tools/update_crm.py --source $SOURCE --input .tmp/routed_leads.json --create-tasks
```
- For `hot`: "Call within 24h" task on owner's queue
- For `warm`: "Review nurture sequence at day 3" task
- For `cold`: no human task — just sequenced drip
- `next_touch_at` ISO timestamp written to lead

### Step 7 — Advance stage where eligible
```bash
python tools/advance_stage.py --source $SOURCE --input .tmp/routed_leads.json
```
- `hot` + first email sent → stage = `Contacted`
- `warm` + first email sent → stage = `Nurture`
- `cold` → stage stays `New`
- Stage names resolved via `config/stages.yaml`

### Step 8 — Persist run state for idempotency
- `.tmp/last_run.json` updated with:
  - `last_run_at` = now (UTC ISO)
  - `processed_lead_ids[source]` += newly processed IDs
  - `last_run_summary` = `{leads_processed, hot, warm, cold, errors}`
- Run log written to `runs/YYYY-MM-DD-lead-lifecycle.md`

### Step 9 — Weekly: generate health report
```bash
python tools/weekly_report.py --source $SOURCE --week $(date +%V) --post-slack
```
- Pulls 7-day stats from CRM (new leads, scored, routed, conversion-by-stage)
- LLM writes 1-paragraph narrative ("This week: …")
- Output: `runs/YYYY-WW-crm-health.md` + Slack post via `SLACK_WEBHOOK_URL`

---

## Outputs

| Output | Location | Format |
|--------|----------|--------|
| New leads | `.tmp/new_leads.json` | JSON array (normalized lead dicts) |
| Scored leads | `.tmp/scored_leads.json` | JSON array with `score`, `reasoning` |
| Routed leads | `.tmp/routed_leads.json` | JSON array with `owner_email`, `track`, `stage` |
| Run state | `.tmp/last_run.json` | Last run timestamp + processed IDs |
| Owner pointer | `.tmp/owner_pointer.json` | Round-robin index per role |
| Run log | `runs/YYYY-MM-DD-lead-lifecycle.md` | Markdown summary |
| Weekly report | `runs/YYYY-WW-crm-health.md` | Markdown report |

---

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| `EnvironmentError: missing HUBSPOT_API_KEY` | Wrong source picked or missing env | Check `.env` and `--source` flag |
| `Airtable 422 INVALID_REQUEST_UNKNOWN` | Missing `Score` field in base | Add `Score` (Number) + `Owner Email` (Email) + `Track` (Single select) + `Stage` (Single select) columns |
| `HubSpot 401 UNAUTHENTICATED` | Expired private app token | Regenerate at app.hubspot.com → Settings → Integrations |
| `Zoho 401 INVALID_TOKEN` | Refresh token expired (14 days) | Re-OAuth flow; update `ZOHO_REFRESH_TOKEN` |
| `Euri rate limit / 429` | Daily quota burned | `score_lead.py` falls back to heuristic — runs continue |
| `Resend 422 You can only send to verified domain` | Free tier sandbox | Either verify domain OR set `EMAIL_FROM=onboarding@resend.dev` |
| `Slack 404 channel_not_found` | Wrong webhook | Recreate webhook in Slack app settings |
| `BudgetExceededError` | Daily $5 cap hit | Stop. Investigate. Don't catch and continue. |
| LLM returns malformed JSON | Model hallucination | `score_lead.py` re-prompts once, then falls back to heuristic |
| Same lead processed twice | Race condition on `last_run.json` | `processed_lead_ids` dedup catches it (Step 1 filter) |

---

## Cost Estimate (per cycle)

| Component | Cost |
|-----------|------|
| CRM API calls | $0 (HubSpot free / Zoho free / Airtable free) |
| Euri LLM scoring | ~$0.001 × leads (free 200K tokens/day) |
| Resend email | $0 (100/day free) |
| Slack webhook | $0 |
| **Total per cycle (≤ 50 leads)** | **≤ $0.05** |

---

## Idempotency Contract

**Re-running the same cycle within 5 minutes MUST be a no-op.** Two safeguards:

1. **State file:** `.tmp/last_run.json` advances `last_run_at` only on successful Step 8.
2. **ID dedup:** `processed_lead_ids[source]` is checked in Step 1 — already-processed IDs are filtered out even if they fall in the time window.

If the cycle crashes mid-run, state is NOT advanced. Re-run picks up from the last successful checkpoint.

---

## Deployment (later — DO NOT during build)

- Local dev: `python tools/run_crm_cycle.py --source airtable --dry-run`
- Cron (15 min): n8n schedule node → HTTP request to a wrapper endpoint
- GitHub Actions (hourly): see root `DEPLOY.md` § "Scheduled Tasks"
