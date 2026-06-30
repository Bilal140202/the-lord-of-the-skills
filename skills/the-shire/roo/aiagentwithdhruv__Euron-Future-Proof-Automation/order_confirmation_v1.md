---
name: order_confirmation_v1
purpose: Personalized order confirmation copy (email + WhatsApp)
variables: customer_name, items, total, eta, order_name
output: strict JSON { subject, body, whatsapp }
---

You write the order-confirmation message for a direct-to-consumer brand.

Customer first name: {{customer_name}}
Order name/ID:       {{order_name}}
Items ordered:
{{items}}
Total:               {{total}}
Estimated delivery:  {{eta}}

Return STRICT JSON (no markdown, no commentary) with exactly this shape:

{
  "subject": "short, warm, <= 9 words — confirms their order",
  "body": "plain-text email body, 80-130 words. Warm, concise. Must mention the order name, list a short summary of items if natural, restate the ETA, and close with a single reassuring sentence. No pricing fabrication — use only the total provided. No discount offers.",
  "whatsapp": "under 240 chars, first-person friendly, no hashtags, 0-1 emoji, must include the order name and a short ETA"
}

Rules:
- Never invent items, prices, or timelines beyond what's provided.
- Never ask the customer to click suspicious links.
- First name only on greetings.
- No placeholders — produce final copy.
