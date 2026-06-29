# Prompt — guardrail_check (reference, rules enforced in code)

> **Purpose:** Document the rules enforced by `tools/guardrail.py`. The guardrail itself is pure Python regex — not an LLM call — so this file exists for human reference only.
> **Category:** safety

---

## 6-Layer guardrail (adapted from `student-starter-kit/skills/guardrail-pipeline/SKILL.md`)

| Layer | What it checks | Action on fail |
|-------|----------------|----------------|
| 1 Policy | Draft length ≤ 2000 chars. External URLs restricted to approved domain list (empty by default → no external URLs). | Block + safe fallback |
| 2 Input | Sender email is the only PII allowed. Body was already PII-stripped before LLM call. | N/A (runtime check) |
| 3 Instructional | Prompt enforces tone constraints. Checked by regex after generation (see 5). | N/A (prompt-level) |
| 4 Execution | Reject drafts containing tool syntax, code fences, SQL, shell commands, raw JSON. | Block |
| 5 Output | Strip/block PII, pricing, commitments, guarantees. | Strip or block |
| 6 Monitoring | Every flag appended to `.tmp/guardrail_log.jsonl`. | Always runs |

---

## Layer 5 patterns (code-enforced in `guardrail.py`)

### PII — STRIP
- SSN: `\b\d{3}-\d{2}-\d{4}\b`
- Credit card (13–19 digits, space/dash separators): Luhn-validated pattern
- Phone: `\b(?:\+?\d{1,3}[\s\-]?)?(?:\(\d{3}\)|\d{3})[\s\-]?\d{3}[\s\-]?\d{4}\b`
- Generic account number: `\baccount\s*(?:#|number|no\.?)?\s*[:\-]?\s*\d{6,}\b`
- DOB: `\b(?:\d{1,2}[\/\-]){2}\d{2,4}\b`

### Pricing — BLOCK (if found → ticket routed to human)
- `\$\s*\d`, `₹\s*\d`, `Rs\.?\s*\d`, `€\s*\d`, `£\s*\d`
- Numeric + currency word: `\b\d+\s*(USD|EUR|GBP|INR|rupees?|dollars?|euros?|pounds?)\b`
- "will cost", "priced at", "costs you", "fee is", "charge(d)? \$"
- Percentages claiming discount: `\b\d{1,3}\s*%\s*(off|discount)\b`

### Commitments — BLOCK
- "guarantee(d|s)?", "promise", "I commit", "definitely will", "assure you"
- "within (1|2|3|4|5|6|12) hour(s)?", "by (tomorrow|end of day|EOD)"
- "we will refund", "you will get a refund", "approved for a refund"

### Safe fallback text
When a draft is blocked:

> "Hi {first_name}, thanks for reaching out — I've routed this to the right team and someone will reply personally within one business day. Best, Support team"

---

## Why regex, not LLM

LLM guardrails are probabilistic. These rules are non-negotiable (no pricing quotes, no refund promises, no PII leaks). Deterministic regex + Luhn is the right layer for these constraints. An LLM can still hallucinate a price even with instruction not to — the post-filter catches it.
