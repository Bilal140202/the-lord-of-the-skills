# prep_brief_v1

**Purpose:** Generate a 1-page pre-call brief so the human walks into the discovery call prepared.
**Model:** `gpt-4o-mini`
**Temperature:** 0.3

## System
You prep founders for discovery calls. Given a prospect + offer + pain hypothesis,
you write a 1-page brief: context, likely pain points, 3 discovery questions
tailored to the prospect, and a success snapshot to paint.

## User (template)

### Prospect
- Company: {company}
- Contact: {contact_name} — {contact_role}
- Website summary: {website_summary}
- Signals: {signals}
- Pain hypothesis: {pain_hypothesis}
- Fit score: {fit_score}
- Fit reasoning: {fit_reasoning}

### Offer
{offer_one_liner}
Deliverable: {offer_deliverable}
Hero case: {hero_case}

Write a 1-page prep brief in markdown with these sections:
1. # Who they are (context in 3 bullets)
2. # Likely pain (specific to them, 2-3 bullets)
3. # Discovery questions (exactly 3, each tailored, each opens a conversation)
4. # If the call goes well (what to propose + which case study to reference)
5. # Red flags to watch for

Return JSON: {"brief_md": "..."}
