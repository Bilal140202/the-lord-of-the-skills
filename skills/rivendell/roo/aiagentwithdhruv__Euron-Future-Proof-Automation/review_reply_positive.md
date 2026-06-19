---
name: review_reply_positive
purpose: Thank a positive reviewer by email
variables: review_text, customer_name, rating
output: strict JSON { subject, body }
---

A customer left a positive review.

Reviewer first name: {{customer_name}}
Their rating:        {{rating}}
Their review text:   {{review_text}}

Write a short thank-you email. Warm, specific, no corporate voice.

Return STRICT JSON:

{
  "subject": "<= 8 words, warm",
  "body": "40-90 words plain text. Reference one concrete thing they said (paraphrase, don't quote). End with an open invitation to reach out if anything ever goes wrong. No sales pitch, no discount offers, no asking for another review."
}
