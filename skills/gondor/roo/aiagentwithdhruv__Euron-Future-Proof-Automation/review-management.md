# Review Management SOP

## Objective

Collect reviews, classify sentiment, thank positive reviewers, escalate
negative ones, leave neutral for human approval.

## Platforms supported

- **Shopify** — reviews dumped as JSON (Judge.me / Yotpo export path).
- **Local fixtures** — JSONL, for dev + tests.
- **Google / Trustpilot** — stubs. Implemented behind an explicit API key
  + budget approval from Angelina.

## Steps

1. **Collect** (`modules/reviews/collect_reviews.py`)
   - `--shopify-json` or `--local`
   - normalises into `{review_id, platform, product_id, rating, text,
     author, author_email, created_at}`
2. **Classify sentiment** (`modules/reviews/classify_sentiment.py`)
   - rule baseline first (rating + keywords)
   - LLM refinement only when ambiguous (3-star, or 4-5 star with
     negative keywords)
3. **Route & reply** (`modules/reviews/auto_reply.py::handle_one`)
   - positive + has `author_email`: auto-reply thank-you
   - negative: draft stored at `.tmp/review_drafts/<id>.json`, Slack
     escalation to CX
   - neutral: draft stored, no send, no escalation
4. **Persist** `Reviews` row with sentiment, rating, status.

## Guardrails

- Negative reviews NEVER auto-send. Humans approve.
- `review_reply_negative` prompt forbids refund/replacement/SLA promises.
- If a review contains a slur / threat, the drafter writes a one-line
  holding response and the handler escalates to Slack.

## Outputs

- `Reviews` rows
- Positive replies (email)
- `.tmp/review_drafts/<id>.json` for neutral + negative
- Slack escalation for negative

## Scheduling

Reviews are polled (not webhook-driven, yet). Suggested cron:

```
30 * * * * cd <repo>/D2C_Ecommerce_Suite && \
  python modules/reviews/auto_reply.py --review-file .tmp/incoming_reviews.jsonl --dry-run
```

Swap `--dry-run` off once Angelina green-lights live sending.
