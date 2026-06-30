# Master Orchestration SOP

How events flow from Shopify / Woo into the right D2C sub-module.

---

## Objective

One webhook receiver. Five sub-modules. HMAC verified + idempotent before
any handler runs. Handlers fire asynchronously so the store's webhook
worker is never blocked by our own I/O.

---

## Request lifecycle

```
POST /webhook/shopify
   |
   v
1. Read RAW body (bytes)
2. Verify X-Shopify-Hmac-Sha256 against SHOPIFY_WEBHOOK_SECRET
      FAIL -> 401 hmac_mismatch
3. Check X-Shopify-Topic against SHOPIFY_SUPPORTED_TOPICS
      SKIP -> 200 {status: "ignored"}
4. Parse JSON body
      FAIL -> 400 invalid_json
5. Idempotency
      event_key = X-Shopify-Webhook-Id OR sha256(body)
      already seen? -> 200 {status: "duplicate"}
6. Normalize payload via tools/events.py
      -> dict {source, topic, event_id, order|cart|product, raw, occurred_at}
7. log_run("webhook", "received", ...)
8. Queue dispatch in FastAPI BackgroundTasks
9. Return 200 {status: "accepted", topic, event_id}

(async) _dispatch_event(event)
   order.*        -> modules/orders/handler.handle
                      + (on order.fulfilled) modules/reviews/handler.handle
   cart.*         -> modules/cart_recovery/handler.handle
   product.*      -> modules/inventory/handler.handle
   inventory.*    -> modules/inventory/handler.handle
   each handler wrapped in try/except so no module can poison others
```

---

## Invariants

- **HMAC first.** Never parse, never log the body until HMAC checks pass.
- **Idempotent by default.** Shopify retries on any 5xx / timeout; our
  receiver must therefore be safe to replay.
- **No auto-charge.** Ever. Even if a module looked like it could.
- **Discount-only recovery.** Cart recovery never places orders, never
  reserves inventory, never charges a card.
- **No raw LLM output sent to customers.** Support drafts run through a
  guardrail (`modules/support/draft_reply.py::strip_prices`) and wait for
  a human before sending.

---

## Topic map (Shopify)

| Shopify topic          | Canonical topic          | Handler                         |
|------------------------|---------------------------|---------------------------------|
| `orders/create`        | `order.created`           | orders.handler                  |
| `orders/paid`          | `order.paid`              | orders.handler                  |
| `orders/fulfilled`     | `order.fulfilled`         | orders.handler + reviews.handler|
| `orders/updated`       | `order.updated`           | orders.handler (noop)           |
| `fulfillments/create`  | `order.shipped`           | orders.handler                  |
| `fulfillments/update`  | `order.shipping_updated`  | orders.handler                  |
| `checkouts/create`     | `cart.created`            | cart_recovery.handler           |
| `checkouts/update`     | `cart.abandoned_candidate`| cart_recovery.handler           |
| `carts/create`         | `cart.created`            | cart_recovery.handler           |
| `carts/update`         | `cart.abandoned_candidate`| cart_recovery.handler           |
| `products/update`      | `product.updated`         | inventory.handler               |
| `inventory_levels/update`| `inventory.updated`     | inventory.handler               |

WooCommerce topics (`order.*`, `product.*`) pass through with conservative
normalisation in `tools/events.py`.

---

## Observability

- Every receive + every handler call appends to `runs/YYYY-MM-DD-<module>.jsonl`.
- `tools/dashboard.py` rolls those up into a human summary.
- Local Airtable mode appends rows to `.tmp/airtable/*.jsonl` (regeneratable,
  disposable).

---

## Failure modes

| Failure                  | Behaviour                                       |
|--------------------------|--------------------------------------------------|
| HMAC mismatch            | 401; nothing else recorded beyond a warning log |
| Missing webhook secret   | 500; we refuse to process anything              |
| Malformed JSON           | 400                                             |
| Duplicate event          | 200 with `status: duplicate`; no handler runs   |
| Handler throws           | Caught; logged as `runs/... event: error`; webhook still returned 200 on accept |
| LLM unavailable          | Every module has a deterministic fallback       |
| Platform creds missing   | Senders + clients fall back to dry-run / local sink |
