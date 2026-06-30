# Support — Ticket Flow SOP

## Objective

Classify an inbound support email, draft a grounded reply using the product
KB, queue it for human approval, send on approval.

## Why human-in-the-loop

Support replies are high-trust, high-risk. Hallucinations that commit us to
refunds, timelines, or pricing are expensive. v1 is human-in-the-loop; the
LLM only drafts.

## Inputs

A JSON file with `{subject, body, from_email}` (in production this will be
populated by an IMAP poller — not part of this module).

## Steps

1. `modules/support/classify_email.py`
   - rule-based baseline + LLM refinement when ambiguous
   - emits `{intent, priority, sentiment, team, classifier}`
2. `modules/support/draft_reply.py`
   - retrieves top-k KB chunks (keyword overlap over `knowledge/*.md`)
   - LLM draft with strict 'no prices / no commitments' guardrails
   - post-filter strips dollar/rupee amounts and specific timelines
   - persists `.tmp/tickets/<id>.draft.json`
3. `modules/support/ticket_workflow.py::run_inbound`
   - writes the `Tickets` row
   - appends to `.tmp/approval_queue.jsonl`
   - Slack alerts the team
4. A human approves via `ticket_workflow.py approve --ticket-id ...`
   - optional `--edits-file` to override subject/body
   - sends via Resend
   - original + edits stored alongside for future prompt tuning

## Guardrails

| Layer          | What it does                                     |
|----------------|--------------------------------------------------|
| Prompt         | Tells the LLM: no prices, no timelines, no SLAs  |
| Post-filter    | Regex-strips `$ / ₹ / INR / USD` amounts         |
| Timing filter  | Replaces `within N hours/days` with `[timing varies]` |
| Human approval | Nothing is sent without explicit approve         |

## Outputs

- `Tickets` row (Airtable or local sink)
- `.tmp/tickets/<id>.draft.json`
- Slack notification
- (on approval) Resend send receipt + `.tmp/tickets/<id>.edits.json`
  with the original + approver edits

## Failure modes

- LLM unavailable -> classifier falls back to rules; drafter writes a
  generic 'a human will reply' holding message
- Resend missing -> send() returns a dry-run receipt, nothing goes out,
  ticket remains in `awaiting_approval`
