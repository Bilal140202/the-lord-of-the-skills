---
name: draft_reply_v1
purpose: Draft a support reply grounded in KB chunks, human-approved before send
variables: subject, body, intent, sentiment, context
output: strict JSON { subject, body }
---

Inbound email —
Subject: {{subject}}
Body:
{{body}}

Classified as:
  intent:    {{intent}}
  sentiment: {{sentiment}}

KB chunks (you may cite inline as [chunk_id]):
{{context}}

Write a draft reply. A human will approve or edit before it goes out.

Return STRICT JSON:

{
  "subject": "Re: ...",
  "body": "60-140 words plain text. Address the customer's question using ONLY the KB chunks above. If the KB doesn't cover it, say so and offer to connect them with a human."
}

Absolute rules (the orchestrator strips violations, but do not produce them in the first place):
- Never state a specific price. No dollar/rupee amounts.
- Never commit to refunds, replacements, or specific shipping timelines.
- Never promise 'within 24 hours', 'by tomorrow', or any specific SLA.
- If you can't ground a claim in the KB, don't make the claim.
