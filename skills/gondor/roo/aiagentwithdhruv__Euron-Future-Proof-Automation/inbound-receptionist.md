# Workflow: Inbound Receptionist

> **Objective:** AI receptionist answers inbound business calls, identifies intent, books appointments on calendar, captures lead info, escalates to a human on demand, and logs a transcript + summary for every call.

---

## Agentic Loop

- **Sense:** Phone rings at the business number. Vapi (or Bland/Retell) picks up and streams audio + partial transcripts.
- **Think:** LLM classifies caller intent from the opening exchange — `book_appointment | info_request | existing_customer | complaint | human | unknown`.
- **Decide:** Pick a script branch. Pull calendar availability or customer record if needed. Decide which tool endpoint to call next.
- **Act:** Call FastAPI tool endpoints to `check_availability`, `book_appointment`, `capture_lead`, `lookup_customer`, `escalate_to_human`, or `send_confirmation`. Talk back to the caller with short, specific lines.
- **Learn:** On hang-up, Vapi POSTs the transcript to `/webhook/call_ended`. We summarize, tag, and store for future prompt tuning.

---

## Inputs

| Input | Source | Notes |
|-------|--------|-------|
| Caller phone number | Vapi call object (`call.from`) | Used for customer lookup + dedup |
| Business context | `.env` (`BUSINESS_NAME`, `BUSINESS_HOURS`, `BUSINESS_SERVICES`) | Templated into `receptionist_system_v1` |
| Calendar | Google Calendar via service account | `GOOGLE_CALENDAR_ID` in `.env` |
| CRM | Supabase `leads` + `customers` tables | Via tool endpoints only |

---

## Tools Used (in order of typical flow)

| Step | Tool Endpoint | When |
|------|---------------|------|
| 1 | `POST /tool/lookup_customer` | On call start, lookup by `call.from` |
| 2 | `POST /tool/check_availability` | Caller asks to book |
| 3 | `POST /tool/book_appointment` | Caller confirms a slot |
| 4 | `POST /tool/capture_lead` | New caller, no existing record |
| 5 | `POST /tool/send_confirmation` | Post-booking — SMS + email |
| 6 | `POST /tool/escalate_to_human` | Caller says "human/agent/representative" OR assistant confidence drops |
| 7 | `POST /webhook/call_ended` | Vapi fires on hang-up — always |

---

## Steps

### 1. Greet + Identify
- Play greeting from `receptionist_system_v1` with `{business_name}`, `{hours}`, `{services}` interpolated.
- Immediately call `lookup_customer` with `phone = call.from`.
- If found: greet by name ("Hi Priya, welcome back to {business}").
- If not found: neutral greeting.

### 2. Classify Intent
- Let caller speak one full sentence. LLM classifies intent.
- Branches:
  - `book_appointment` → go to step 3.
  - `info_request` → answer from `business_services` / FAQ; offer booking at the end.
  - `existing_customer` → pull their last booking; offer reschedule/cancel.
  - `complaint` → skip to step 6 (escalate).
  - `human` → skip to step 6 (escalate) immediately.
  - `unknown` → ask one clarifying question, then reclassify. After 2 failed clarifications → escalate.

### 3. Booking Flow (if applicable)
- Call `check_availability` with `{service_type, date_preference, duration_minutes}`.
- Receptionist reads back top 2-3 slots ("I have Tuesday at 3pm or Wednesday at 11am — which works?").
- Caller picks → call `book_appointment` with `{slot_id, customer_name, customer_phone, customer_email, service_type, notes}`.
- On success: read back confirmation, tell them an SMS + email is on its way.
- Call `send_confirmation` with the booking ID.

### 4. Capture Fields (if new lead)
- If lookup_customer returned nothing AND caller didn't book, still capture what you heard:
  - Name, reason for calling, best contact method.
- Call `capture_lead` with fields collected + call transcript excerpt + source = `"inbound_voice"`.

### 5. Handle Edge Cases
- Caller asks a question outside scope → acknowledge, offer escalation.
- Caller insists on speaking with a human → **always honor immediately**. No gating.
- Noisy line / STT failure → "I'm having trouble hearing you, let me transfer you to someone" → escalate.

### 6. Escalation
- Call `escalate_to_human` with `{call_id, reason, transcript_so_far, priority}`.
- Receptionist says a handoff line: "I'm connecting you to a teammate — one moment."
- Vapi transfers to the `HUMAN_HANDOFF_NUMBER` configured in `.env`.
- If no human is available: offer callback → capture_lead with `callback_requested = true`.

### 7. Close
- Recap what was booked / captured.
- "Thanks for calling {business}. Goodbye."
- End call.

### 8. Post-Call (automatic via webhook)
- Vapi fires `/webhook/call_ended` with full transcript + recording URL + tool call log.
- Server runs `summarize_call` prompt → stores `{call_id, summary, tags, sentiment, outcome, duration_s, recording_url}` in Supabase `call_logs`.

---

## Outputs

| Output | Destination |
|--------|-------------|
| Calendar event | Google Calendar (`GOOGLE_CALENDAR_ID`) |
| Lead / customer record | Supabase `leads` or `customers` |
| Confirmation SMS | Twilio → caller's phone |
| Confirmation email | Resend → caller's email (if captured) |
| Call transcript + summary | Supabase `call_logs` |

---

## Error Handling

| Failure | What Happens |
|---------|--------------|
| `check_availability` returns no slots | Assistant offers a callback; `capture_lead` with `callback_requested = true` |
| `book_appointment` 4xx/5xx | Assistant apologizes, offers to take details manually; escalate to human |
| Calendar auth fails | Return 503 from tool; assistant falls back to capture + human follow-up |
| SMS/email fails | Log warning; don't fail the call — booking already exists |
| Caller says "stop" / "hang up" / silence > 15s | End call cleanly; fire webhook |
| Tool endpoint unreachable | Vapi retries per its config; if still failing, assistant tells caller "something's wrong, let me transfer" → escalate |

---

## Consent + Compliance

- **Recording disclosure:** First line of the greeting states "This call is being recorded for quality" if recording is enabled. Non-negotiable.
- **PII:** Phone numbers and emails are stored; no credit card or health data captured via voice.
- **Human escalation:** ALWAYS available. Caller says "human" at any point → immediate transfer. No AI gating allowed.
- **Data retention:** Follow business retention policy; default 90 days on recordings, permanent on summaries/transcripts.

---

## Cost Estimate (per call)

| Component | Cost |
|-----------|------|
| Vapi voice minutes | ~$0.05-0.10/min |
| LLM (classification + summary) | Euri free tier covers most; ~$0.001 if overflow to paid |
| Twilio SMS | ~$0.0075/msg |
| Resend email | Free ≤100/day |
| **Total per 3-min call** | **~$0.20-0.35** |

---

## Test Plan

1. Run `uvicorn api.main:app --reload --port 8080`.
2. Start a tunnel: `cloudflared tunnel --url http://localhost:8080` (stable URL, free).
3. In Vapi dashboard: set assistant's tool webhook base to the tunnel URL. Set API key header to match `API_KEY` from `.env`.
4. Use Vapi's "Test Call" from the dashboard (web mic, no real phone needed).
5. Say: "Hi, I'd like to book an appointment for next Tuesday."
6. Verify:
   - `lookup_customer` called with caller ID.
   - `check_availability` returns slots.
   - `book_appointment` creates a real Calendar event (use a test calendar).
   - Confirmation SMS + email arrive.
   - `/webhook/call_ended` fires and `call_logs` row is written.
7. Repeat with "I want to speak to a human" → verify immediate escalation path.
8. Do NOT hit production phone number until QA pass is clean.

---

## Related

- `workflows/outbound-followup.md`
- `prompts/receptionist_system_v1.md`
- `prompts/post_call_summary.md`
- `api/main.py`
