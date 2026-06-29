# Workflow: Outbound Follow-Up

> **Objective:** AI voice agent calls a queue of opted-in leads, delivers a personalized follow-up pitch, captures the outcome (interested / not-interested / callback / voicemail), and updates CRM — with consent checks and strict compliance guardrails.

---

## Non-Negotiable Rules

1. **Consent is mandatory.** Only call numbers flagged `consent_outbound = true` in the CRM or CSV. Never cold-call.
2. **Recording disclosure** on every call, stated by the AI in the first 5 seconds if recording.
3. **Time-of-day gate.** No calls outside business hours in the caller's timezone (default 9am-7pm local).
4. **DNC (Do Not Call) check.** Skip any number on the DNC list before dialing.
5. **Human escalation** always honored — caller says "stop" / "human" / "remove me" → immediate stop + flag.
6. **Max 1 call per lead per day.** Retry after 48h if no answer; max 3 attempts total.

---

## Agentic Loop

- **Sense:** Scheduled task fires (cron or push) → outbound queue has N leads ready.
- **Think:** For each lead: check consent + DNC + timezone gate + last-call window. LLM personalizes the opener from `outbound_followup_v1` using `{lead_name, last_touch, offer}`.
- **Decide:** Proceed to dial OR skip (reason logged). If picking up, assistant drives the script; branches on caller response (interested / not / callback / voicemail).
- **Act:** Vapi places the call. Tools `capture_lead_outcome`, `send_confirmation`, `escalate_to_human` as needed.
- **Learn:** Post-call webhook → summary + tags; update lead status; feed back into next-touch prompt.

---

## Inputs

| Input | Source | Notes |
|-------|--------|-------|
| Lead CSV | `leads.csv` | Columns: `name, phone, email, consent_outbound, last_touch, offer, notes, timezone` |
| Business context | `.env` | Template context |
| Vapi outbound config | `.env` (`VAPI_API_KEY`, `VAPI_ASSISTANT_ID`, `VAPI_PHONE_NUMBER_ID`) | Must be a verified number |
| DNC list | Supabase `dnc_list` table | Phone numbers to always skip |

---

## Tools Used

| Step | Tool / Endpoint | When |
|------|-----------------|------|
| 0 | `tools/queue_outbound.py --csv leads.csv` | CLI — pushes tasks to Vapi's outbound API |
| 1 | `POST /tool/lookup_customer` | Assistant uses at call start to confirm identity |
| 2 | `POST /tool/capture_lead` (with `outcome` field) | Record outcome + notes |
| 3 | `POST /tool/send_confirmation` | If lead says yes, send follow-up email/SMS |
| 4 | `POST /tool/escalate_to_human` | If lead requests callback from a human |
| 5 | `POST /webhook/call_ended` | Every call, without exception |

---

## Steps

### 0. Pre-Flight (CLI, before any dialing)
- Run `python tools/queue_outbound.py --csv leads.csv --dry-run` first.
- Script validates every row:
  - Phone format E.164.
  - `consent_outbound == true`.
  - Not in DNC list.
  - Timezone known.
  - Local time between `OUTBOUND_WINDOW_START` and `OUTBOUND_WINDOW_END`.
  - Not already attempted ≥3 times.
- Dry-run prints a summary: `N eligible, M skipped (reasons)`.
- If it looks right, run without `--dry-run` to actually push.

### 1. Assistant Opens the Call
- First line: "Hi, this is {business} calling for {lead_name} — is this a good time?"
- If recording: add "this call is being recorded" in the same breath.
- If wrong person answers: "Sorry to bother you, we'll try again later" → end → mark `outcome = wrong_person`.

### 2. Deliver Personalized Pitch
- Use `outbound_followup_v1` prompt, filled with `{lead_name, last_touch, offer}`.
- Keep it under 20 seconds before first caller turn.
- Example: "I'm following up on our conversation last Tuesday about the {offer} — we have a spot open this week if you're still interested."

### 3. Branch on Caller Response

| Response | Action |
|----------|--------|
| Interested | Offer 2 slots → if accepted, call `book_appointment` (same as inbound); else `capture_lead` with `outcome = interested, follow_up_on = <date>` |
| Not interested | Thank them, ask consent to remove from list, `capture_lead` with `outcome = not_interested`; if they say "remove me", add to DNC |
| Callback / busy | `capture_lead` with `outcome = callback, callback_requested_at = <ISO8601>` |
| Voicemail | Leave ≤15s templated message → `capture_lead` with `outcome = voicemail` |
| Hostile / "stop" / "remove" | Apologize briefly, add to DNC, end call, `capture_lead` with `outcome = dnc_requested` |
| Asks for human | `escalate_to_human` with priority=normal; hand off if available else capture callback |

### 4. Close
- "Thanks for your time — have a good day."
- End call.

### 5. Post-Call (automatic)
- `/webhook/call_ended` fires with transcript + outcome.
- Summarize + tag via `post_call_summary` prompt.
- Update `leads.status`, `leads.last_call_at`, `leads.call_count`, `call_logs` row.

---

## Outputs

| Output | Destination |
|--------|-------------|
| Updated lead record | Supabase `leads` |
| Call log + transcript + summary | Supabase `call_logs` |
| DNC additions | Supabase `dnc_list` |
| Calendar event (if booked) | Google Calendar |
| Follow-up email / SMS | Resend / Twilio |

---

## Error Handling

| Failure | What Happens |
|---------|--------------|
| Number rings with no answer | Vapi reports `no_answer`; script queues retry in 48h (max 3 attempts) |
| Voicemail detected | Leave short script; mark outcome; do NOT retry same day |
| Call fails mid-conversation | Post-call webhook still fires with whatever transcript exists; outcome = `incomplete`, agent flags for human |
| Vapi API 4xx on queue push | Fail loudly in CLI; show reason; no partial queue |
| Consent field missing/false | Row skipped; logged in `runs/YYYY-MM-DD-outbound.md` with reason |
| Tool endpoint 401 | Shared secret mismatch — fix API_KEY in `.env` + Vapi assistant config |

---

## Consent + Compliance Checklist

- [ ] Lead has `consent_outbound = true` (timestamped source required)
- [ ] Phone not in DNC list
- [ ] Local time within OUTBOUND_WINDOW
- [ ] Not already called in last 48h
- [ ] Max 3 attempts not exceeded
- [ ] Recording disclosure in script (if recording on)
- [ ] "Stop/remove" honored instantly
- [ ] Outcome logged for every attempt

**If any of the above fails → do not call. Log reason in `runs/`.**

---

## Cost Estimate

| Call Type | Cost |
|-----------|------|
| Voicemail drop (~15s) | ~$0.03 |
| Short rejection (~30s) | ~$0.05 |
| Engaged follow-up (~3-5 min) | ~$0.20-0.50 |
| Booked appointment | ~$0.30-0.60 |

Budget check: per-run limit $2.00, daily $5.00. `queue_outbound.py` estimates total cost before pushing and asks confirmation if > $2.

---

## Test Plan

1. Create a small `leads.test.csv` with 1 row = your own number, `consent_outbound=true`.
2. `python tools/queue_outbound.py --csv leads.test.csv --dry-run` → verify it says "1 eligible".
3. Run without `--dry-run` → answer your phone → test the script end-to-end.
4. Verify `call_logs` row + `leads.status` updated + confirmation email/SMS arrived.
5. Repeat test saying "remove me" → verify DNC entry created + next push skips that number.
6. Do NOT run on real leads until both tests pass.

---

## Related

- `workflows/inbound-receptionist.md`
- `prompts/outbound_followup_v1.md`
- `prompts/post_call_summary.md`
- `tools/queue_outbound.py`
- `api/main.py`
