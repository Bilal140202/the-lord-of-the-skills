# Prompt: rank_findings_v1

**Purpose:** Rank classified findings by business relevance.
**Variables:** `{business_context}`, `{findings_json}`, `{top_n}`
**Output:** JSON only, array of `{change_id, rank, score, rationale}`.

---

You are ranking competitive intelligence findings for a team building in: **{business_context}**.

You will be given a list of findings already tagged (pricing / launch / hire / partnership / press / site / other).

## Task

Score each finding from 1 (low) to 10 (high) on business relevance. Return JSON:

```json
[
  {
    "change_id": "<id>",
    "rank": <1..N>,
    "score": <1..10>,
    "rationale": "<one sentence — why this matters to us, given {business_context}>"
  }
]
```

Rules:
- **Higher score** = finding that would change our strategy, pricing, positioning, or roadmap if we acted on it.
- **Lower score** = noise, minor site tweak, low-signal press.
- Return all findings, sorted by `rank` ascending (rank 1 = most important).
- Return top {top_n} or all findings, whichever is smaller.
- Response MUST be a single valid JSON array. No prose.

## Findings

```json
{findings_json}
```
