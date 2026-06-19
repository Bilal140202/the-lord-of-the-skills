# Cart Recovery SOP

## Objective

Recover abandoned checkouts through a 3-step email/WhatsApp sequence using
discount codes only — never auto-charging.

## Non-negotiable

**Recovery is DISCOUNT-ONLY.** This module will never place an order on a
customer's behalf, will never charge a card, will never "reserve" stock.
The only action is a message with a link back to the cart, optionally
carrying a discount code.

## Inputs

- `cart.abandoned_candidate` webhook events (Shopify `checkouts/update`
  or `carts/update`).

## Steps

1. **Record candidate** (`modules/cart_recovery/detect_abandoned.py::record_candidate`)
   - persist to `.tmp/carts.json` + `Carts` table
   - status starts at `candidate`, recovery_step = 0
2. **Promotion scan** (`detect_abandoned.py --scan`, cron every 30 min)
   - cart untouched for `ABANDONED_CART_DELAY_MIN` minutes -> step 1
   - step 1 + `ABANDONED_CART_STEP2_HRS` hrs -> step 2
   - step 2 + `ABANDONED_CART_STEP3_DAYS` days -> step 3
3. **Send per-step copy** (`modules/cart_recovery/send_recovery_email.py::send_for_row`)
   - step 1: no discount, friendly check-in
   - step 2: email + `DISCOUNT_CODE_RECOVERY` @ 10%
   - step 3: last nudge, same code
4. **Attribution** (`modules/cart_recovery/track_recovery.py::attribute`)
   - on `order.created`, match email to an abandoned cart within 72 hrs
   - mark recovered + attribute revenue to `Carts` row

## Cron / scheduling

For the MVP the scan runs off a cron or n8n trigger. A drop-in entry:

```
*/30 * * * * cd <repo>/D2C_Ecommerce_Suite && \
  python modules/cart_recovery/detect_abandoned.py --scan > .tmp/scan.log
```

## Outputs

- `Carts` rows at each step + `Stage=recovery_step_N`
- Sender receipts
- (on recovery) `Carts` row with `Status=recovered`, `Revenue`, `RecoveredOrderID`

## Failure modes

- Cart missing email/phone -> skipped, still recorded
- No abandoned_checkout_url -> step copy still works, URL reads "(cart
  link unavailable)"; email still sends
- Duplicate promotion (cart seen twice) -> idempotent — same cart_id
  overwrites the row
