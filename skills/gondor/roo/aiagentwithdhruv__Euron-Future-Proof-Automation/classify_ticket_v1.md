---
name: classify_ticket_v1
purpose: Classify an inbound support email into intent/priority/sentiment/team
variables: subject, body, intents, priorities, teams
output: strict JSON { intent, priority, sentiment, team }
---

Subject: {{subject}}
Body:
{{body}}

Classify into these enums:

- intent    — one of: {{intents}}
- priority  — one of: {{priorities}}   (P1 = urgent/legal/safety, P2 = blocking, P3 = standard, P4 = feedback/spam)
- sentiment — one of: positive, neutral, negative
- team      — one of: {{teams}}

Return STRICT JSON (no markdown, no prose):

{
  "intent": "...",
  "priority": "...",
  "sentiment": "...",
  "team": "..."
}

Rules:
- Never invent a new enum value. Pick from the lists above.
- If the email looks like spam or a marketing blast, set intent=spam, priority=P4, team=cx.
- If the email mentions harm, legal, or a chargeback, force priority=P1.
