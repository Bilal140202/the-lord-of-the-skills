---
name: review_reply_negative
purpose: Draft a make-it-right reply to a negative review (human approves before send)
variables: review_text, customer_name, rating
output: strict JSON { subject, body }
---

A customer left a negative review.

Reviewer first name: {{customer_name}}
Their rating:        {{rating}}
Their review text:   {{review_text}}

Draft a respectful, calm, non-defensive reply. A human will approve or edit
this before it goes out.

Return STRICT JSON:

{
  "subject": "<= 8 words — acknowledges the issue without over-apologising",
  "body": "50-110 words plain text. Acknowledge what went wrong in their words (paraphrase). Do NOT promise a refund, replacement, or specific timeline — those are decisions a human makes. Ask for the order number if helpful. Sign off from 'CX Team'."
}

Absolute rules:
- Never commit to a refund amount, replacement, or shipping timeline.
- Never blame the customer.
- Never admit legal liability.
- If the review contains a slur or threat, write a one-line holding response and escalate to a human immediately.
