# Orders — Lifecycle SOP

## Objective

Carry a customer through every touchpoint of their purchase: confirm on
create, notify on ship, schedule a review ask after fulfilment.

## Inputs

- Normalised event dict (see `tools/events.py`) with topic `order.*`.

## Tools used

| Tool                                      | When                         |
|-------------------------------------------|------------------------------|
| `tools/senders/email.py`                  | confirmation + tracking      |
| `tools/senders/whatsapp.py`               | confirmation + tracking      |
| `tools/llm.py` + `prompts/order_confirmation_v1.md` | confirmation copy |
| `tools/airtable_client.py`                | persist order row            |
| `modules/orders/send_confirmation.py`     | order.created / order.paid   |
| `modules/orders/tracking_update.py`       | order.shipped / order.shipping_updated / order.fulfilled |
| `modules/orders/request_review.py`        | schedule review ask on order.fulfilled |

## Steps

1. `order.created` or `order.paid`
   1.1 Compose confirmation copy (LLM-first, template fallback)
   1.2 Email (if `email`) + WhatsApp (if `phone`)
   1.3 Record `Orders` row with `Stage=confirmed`
2. `order.shipped` / `order.shipping_updated` / `order.fulfilled`
   2.1 Skip if no tracking number AND no tracking URL
   2.2 Send shipping update email + WhatsApp
   2.3 Upsert `Stage=shipped` + `Tracking` + `TrackingURL`
3. `order.fulfilled` additionally:
   3.1 Schedule review ask at `now + REVIEW_REQUEST_DELAY_DAYS`
   3.2 Upsert `Stage=review_scheduled` + `ReviewDueAt`
4. A separate cron / n8n (or `request_review.py --send-test`) actually
   sends the review ask when `ReviewDueAt <= now`.

## Outputs

- Sender receipts (channel, provider, id)
- Airtable rows (or local `.tmp/airtable/Orders.jsonl`)

## Error handling

- Missing email AND phone -> `status: skipped, reason: no_contact`.
- Invalid phone -> WhatsApp row is skipped, email still fires.
- LLM unavailable -> deterministic template copy.
