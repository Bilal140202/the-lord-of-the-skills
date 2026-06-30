# followup_variant

**Purpose:** Generate follow-up email variants (day 3, day 7, day 14) that don't sound like spam.
**Model:** `gpt-4o-mini`
**Temperature:** 0.5

## Variants
- Day 3 — "bumping this up" style. 40-60 words. Mention one new angle.
- Day 7 — value-add. Share one specific insight relevant to their pain. 70-100 words.
- Day 14 — "permission to close your file". 30-50 words. Classic break-up email.

## System
You write follow-ups that feel human. Each one has a distinct tone and a new reason to reply.
No "just checking in." Ever.

## User (template)

### Prior email
Subject: {prior_subject}
Body: {prior_body}

### Prospect
- Company: {company}
- Pain hypothesis: {pain_hypothesis}
- Signals: {signals}

### Days since first touch
{days_since}

Return JSON: {"subject": "...", "body": "..."}
