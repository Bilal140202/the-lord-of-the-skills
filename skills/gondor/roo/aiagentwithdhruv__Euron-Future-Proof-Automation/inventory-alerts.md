# Inventory Alerts SOP

## Objective

Catch low-stock variants early, alert the ops team exactly once per drop,
suggest a reorder quantity based on velocity. Never auto-order.

## Steps

1. **Poll** (`modules/inventory/check_stock_levels.py --poll`)
   - Shopify primary, Woo fallback
   - emits a per-variant list with `low=True` where qty <= threshold
2. **Alert** (`modules/inventory/alert_low_stock.py::run`)
   - de-dupe against `.tmp/stock_state.json` — only alert when qty is
     new-or-worse than the last known state
   - single digest Slack + optional ops email (if `OPS_EMAIL` set)
   - append `Stock` row with `Status=low_stock`
3. **Reorder suggestion** (`modules/inventory/suggest_reorder.py::suggest`)
   - deterministic math: `velocity_per_day`, `days_of_cover`,
     `suggested_qty = ceil(velocity * target_cover - stock)`
   - LLM writes the human-facing one-sentence reason only — numbers
     stay pure

## Schedules

```
0 8 * * *  cd <repo>/D2C_Ecommerce_Suite && \
  python modules/inventory/alert_low_stock.py
```

## Auto-order is OFF

Per Angelina's brief. `suggest_reorder.suggest()` returns
`auto_order_enabled: false` — the flag exists so future toggling is
explicit. Do NOT flip it without a written go-ahead.

## Outputs

- Slack digest (ops)
- Optional email to `OPS_EMAIL`
- `Stock` rows in Airtable / local sink
- `.tmp/stock_state.json` — holds last-alerted qty per variant

## Failure modes

- No platform configured -> empty list, no alerts. (Logged as info.)
- Platform rate-limited (429) -> returns empty list, retries next run.
