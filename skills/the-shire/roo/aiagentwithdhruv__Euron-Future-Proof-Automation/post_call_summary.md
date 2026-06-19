# Prompt: post_call_summary

> **Purpose:** Summarize + tag a completed call transcript. Used by the `/webhook/call_ended` handler after every call.
> **Category:** summary
> **Variables:** `transcript`, `call_direction`, `duration_s`, `caller_phone`, `business_name`
> **Model:** `euri/gpt-4o-mini` (fast + cheap; falls back to `euri/gpt-4o` if output parsing fails).

---

## System Prompt

```
You analyze completed phone call transcripts for {business_name} and return structured data. You never hallucinate. You never invent facts. If a field is unknown, return null.
```

---

## User Prompt Template

```
Below is a phone call transcript. Direction: {call_direction} (inbound or outbound).
Duration: {duration_s} seconds. Caller phone: {caller_phone}.

TRANSCRIPT:
---
{transcript}
---

Return a single JSON object with exactly these fields:

{
  "summary": "2-3 sentence neutral summary. No editorializing.",
  "outcome": "one of: booked | info_given | lead_captured | escalated_to_human | not_interested | callback_requested | voicemail | wrong_person | dnc_requested | incomplete | other",
  "tags": ["short", "lowercase", "tags", "max 6"],
  "sentiment": "one of: positive | neutral | negative",
  "caller_intent": "one of: book_appointment | info_request | existing_customer | complaint | human | sales_follow_up | unknown",
  "action_items": ["list of concrete follow-ups for the team, if any"],
  "customer_name": "name the caller gave, or null",
  "customer_email": "email the caller gave, or null",
  "booking_ref": "booking ID if one was created, or null",
  "needs_human_review": true | false,
  "confidence": 0.0-1.0
}

Rules:
- Return JSON only. No markdown. No prose outside the JSON.
- Use null (not empty strings) for missing optional fields.
- "action_items" is empty list [] if there's nothing to do.
- "needs_human_review" = true if: caller was upset, transcript was incomplete, caller asked something the AI could not answer, or compliance-sensitive content came up (complaints, legal, medical advice, payment disputes).
- "confidence" reflects how clean/complete the transcript was — low confidence if STT looked garbled.
```

---

## Expected Output Shape

```json
{
  "summary": "Caller asked to book a cleaning for next Tuesday. Offered 2pm slot which she accepted. Confirmation SMS and email sent.",
  "outcome": "booked",
  "tags": ["new_patient", "cleaning", "tuesday", "sms_sent"],
  "sentiment": "positive",
  "caller_intent": "book_appointment",
  "action_items": [],
  "customer_name": "Priya Mehta",
  "customer_email": "priya@example.com",
  "booking_ref": "bk_01HX...",
  "needs_human_review": false,
  "confidence": 0.92
}
```

---

## Fallback Behavior

If the model returns invalid JSON:
1. Retry once with `euri/gpt-4o` (higher-quality).
2. If still invalid, store the raw transcript + a stub record: `{"summary": "Auto-summary failed; see transcript", "outcome": "other", "needs_human_review": true, "confidence": 0.0}`.
3. Flag `call_logs.summary_status = "failed"` and alert — never drop the call log itself.

---

## Notes

- Runs async after the webhook returns 200 — never block Vapi on the summary.
- PII (name, email) is stored in the CRM separately; duplicating in the summary is fine but flag with `needs_human_review=true` if anything unexpected appears (SSN, credit card number, etc.).
- Cost: ~$0.0005 per 3-min call on `gpt-4o-mini`.
