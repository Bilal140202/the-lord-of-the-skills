---
name: cart_recovery_v1
purpose: Abandoned-cart recovery copy per step (1hr / 24hr / 3d)
variables: customer_name, step, items, discount_code, discount_pct, cart_url
output: strict JSON { subject, body, whatsapp }
---

Customer first name: {{customer_name}}
Step:                {{step}}   (1 = 1 hour, 2 = 24 hours, 3 = 3 days)
Items they saw:      {{items}}
Discount code:       {{discount_code}}   (empty on step 1)
Discount pct:        {{discount_pct}}    (0 on step 1)
Cart URL:            {{cart_url}}

Tone by step:
- Step 1: friendly check-in, NO discount. Ask if something went wrong.
- Step 2: include the code + pct off. Time-bounded urgency, not panic.
- Step 3: last nudge, low-pressure. Mention the code is still live. Offer to walk away gracefully.

Return STRICT JSON (no markdown):

{
  "subject": "short, <= 9 words",
  "body": "plain-text email body, 70-120 words. Plain text, no markdown. No pricing fabrication. No threats of deletion beyond what's true (we keep carts around).",
  "whatsapp": "<= 240 chars, friendly, 0-1 emoji, must include the cart URL and (step>1) the code"
}

Absolute rules:
- Never claim we've 'charged' them or 'reserved stock'. We have not.
- Never invent timelines for stock running out.
- First name only.
- Do NOT invent a discount code or percentage — use exactly what's passed in.
