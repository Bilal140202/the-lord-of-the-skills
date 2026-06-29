---
name: reorder_suggestion
purpose: Explain a reorder quantity suggestion in plain English for ops
variables: sku, product_title, last_30d_sales, current_stock, velocity_per_day, days_of_cover, suggested_qty, target_cover_days
output: strict JSON { reason }
---

SKU:                 {{sku}}
Product:             {{product_title}}
Last 30d sales:      {{last_30d_sales}}
Current stock:       {{current_stock}}
Velocity per day:    {{velocity_per_day}}
Days of cover:       {{days_of_cover}}
Target cover days:   {{target_cover_days}}
Suggested reorder:   {{suggested_qty}}

Return STRICT JSON:

{
  "reason": "One sentence (<= 30 words). Plain English. State the velocity, current cover in days, and why the suggested qty hits the target cover. No emojis. No markdown."
}

Rules:
- Do NOT change the numbers. Quote them verbatim.
- Do NOT recommend auto-ordering. This is a suggestion, nothing more.
