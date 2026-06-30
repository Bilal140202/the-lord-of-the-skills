---
name: classify_sentiment
purpose: Disambiguate sentiment for reviews where stars + keywords disagree
variables: rating, text
output: strict JSON { sentiment, reason }
---

Star rating:   {{rating}}
Review text:
{{text}}

The rule-based classifier is unsure. Read the text and decide: positive,
neutral, or negative — based on the TONE of the text, not just the rating.

Return STRICT JSON:

{
  "sentiment": "positive" | "neutral" | "negative",
  "reason": "<= 20 words, one sentence."
}
