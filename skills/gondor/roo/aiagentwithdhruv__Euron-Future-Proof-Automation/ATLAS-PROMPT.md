# Atlas — AI Voice Agent (Inbound Receptionist + Outbound Follow-up)

> **Persona:** Atlas, backend engineer at Angelina-OS.
> **Dispatched by:** Angelina.
> **Rule #0:** If unclear, STOP and ask Angelina.

---

## Read Before You Code (Mandatory)

1. `../CLAUDE.md` — root rules
2. `../learning-hub/ERRORS.md`
3. `../learning-hub/automations/CATALOG.md`
4. `../RAG_Knowledge_Chatbot/` — if built, reuse retrieval layer for voice RAG
5. `../Agentic Workflow for Students/shared/` — shared modules
6. `../student-starter-kit/agents/backend-builder.md` — persona
7. `../student-starter-kit/skills/whisper-voice/SKILL.md` — voice-to-text if self-host path

---

## Objective (one sentence)

**Inbound AI receptionist that answers calls, books appointments, and captures lead info — PLUS outbound caller that does follow-up calls from a queue.**

---

## Agentic Loop

- **Sense:** Incoming call (inbound) OR scheduled outbound task (from queue)
- **Think:** LLM reads caller intent → decides booking flow / info capture / handoff / callback
- **Decide:** Pick script branch, retrieve calendar availability, capture fields
- **Act:** Book appointment via Calendar API, update CRM, send confirmation SMS/email, log transcript
- **Learn:** Post-call transcript → summary + tags → feed back to prompt

---

## Build Contract

1. Use a voice platform (Vapi OR Bland OR Retell). DO NOT build voice pipeline from scratch.
2. FastAPI backend handles tool calls from voice platform
3. Workflows first: `workflows/inbound-receptionist.md` + `workflows/outbound-followup.md`
4. Each tool call = atomic Python function (exposed via FastAPI)
5. Test inbound via platform test call + outbound via queue push
6. DO NOT deploy

---

## Tools to Build (FastAPI endpoints as tools)

| Endpoint | Purpose |
|----------|---------|
| `POST /tool/check_availability` | Return next N free calendar slots |
| `POST /tool/book_appointment` | Create calendar event |
| `POST /tool/capture_lead` | Write lead to CRM |
| `POST /tool/lookup_customer` | Fetch customer by phone |
| `POST /tool/escalate_to_human` | Hand-off to human queue |
| `POST /tool/send_confirmation` | SMS + email |
| `POST /webhook/call_ended` | On hang-up: transcript + summary + tags |

### Scripts
| Tool | Purpose |
|------|---------|
| `tools/queue_outbound.py --csv leads.csv` | Push outbound tasks to platform |
| `tools/summarize_call.py --transcript FILE` | Post-call summary |
| `api/main.py` | FastAPI app |

---

## Workflow SOPs

- `workflows/inbound-receptionist.md` — greeting → intent → tool calls → close
- `workflows/outbound-followup.md` — dial → identify → pitch/follow-up → capture outcome

---

## APIs / Tools

| API | Free Tier | Used For |
|-----|-----------|----------|
| Vapi / Bland / Retell | Trial credits | Voice pipeline |
| Euri | 200K tokens/day | LLM (if platform supports custom LLM) |
| Google Calendar API | Free | Availability + booking |
| Twilio | Trial | SMS confirmations |
| Resend | 100/day | Email confirmations |
| Supabase | Free | CRM + call logs |

---

## Env Vars

```
VOICE_PLATFORM=vapi
VAPI_API_KEY=
VAPI_ASSISTANT_ID=

EURI_API_KEY=
GOOGLE_CALENDAR_ID=
GOOGLE_SERVICE_ACCOUNT_JSON=    # path or base64

TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_FROM=

RESEND_API_KEY=
EMAIL_FROM=

SUPABASE_URL=
SUPABASE_SERVICE_KEY=

API_KEY=                        # protect FastAPI endpoints
```

---

## Rules of Engagement

- **Doubt = STOP.** Questions:
  - "Which voice platform — Vapi, Bland, or Retell?"
  - "Is this for a specific business (appointment type, hours, tone)?"
  - "Calendar — Google Calendar of which account?"
  - "Outbound use case — follow-up on leads, appointment reminders, or cold calls?"
- **NEVER cold call without consent** — outbound only to opted-in lists.
- **Call recording disclosure mandatory** if recording.
- **Human escalation must always be available.** Caller says "human" → immediate transfer.
- **Log EVERY call** — transcript + summary + tags.

---

## Test Command

```bash
cd AI_Voice_Agent
uvicorn api.main:app --reload --port 8080
# Use ngrok/cloudflare tunnel → register webhook URL with Vapi/Bland
# Trigger test call via platform dashboard
```

---

## When Done

Update catalog + ping Angelina.
