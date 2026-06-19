# Pipeline Flow — Client Acquisition System

> **6-stage outbound SOP.** Scrape → Enrich → Qualify → Outreach → Discovery → Proposal.
> **Owner:** Atlas | **Phase:** 8 | **Last verified:** 2026-04-19

---

## Objective (one sentence)

Take an ICP definition, produce qualified, personalized outreach that converts to booked discovery calls and proposal-ready prospects — with CAN-SPAM + DPDP compliance and sane rate limits.

---

## Inputs

- `config/icp.yaml` — industry, geography, company size, role, tech signals
- `config/offer.yaml` — service name, deliverable, price band, hero case study
- CLI flags: `--limit N`, `--dry-run`, `--stage <name>`, `--resume <run_id>`

## Primary Outputs

- `state/pipeline.json` — every prospect's stage + status (state store)
- `.tmp/drafts/` — LinkedIn DMs awaiting human send
- `.tmp/proposals/` — generated proposal markdown
- `runs/YYYY-MM-DD-pipeline.md` — execution log

---

## Stage 1 — Scrape (`stages/01_scrape/`)

**Goal:** Produce a raw prospect list matching ICP.

| Tool | When to use |
|------|-------------|
| `google_maps.py` | Local service businesses (dental, construction, real estate, home services) |
| `linkedin_search.py` | B2B with named roles (founders, heads of X, directors) |
| `apollo_export.py` | Large-scale B2B with firmographic filters |

**Output shape** (common schema, written to state):
```json
{
  "prospect_id": "prs_abc123",
  "company": "Acme Dental",
  "website": "https://acmedental.ae",
  "city": "Dubai",
  "country": "UAE",
  "contact_name": "Dr. Ali",
  "contact_role": "Owner",
  "email": null,
  "linkedin_url": null,
  "phone": "+971...",
  "source": "google_maps",
  "scraped_at": "2026-04-19T10:00:00Z",
  "stage": "scraped",
  "status": "pending_enrich"
}
```

**Gotcha:** Always dedupe by domain + phone. One prospect per company (not per employee) unless the ICP targets multiple roles.

---

## Stage 2 — Enrich (`stages/02_enrich/`)

**Goal:** For every scraped prospect, add: verified email, LinkedIn profile, company context (pain hypothesis signal).

| Tool | Input | Output field(s) |
|------|-------|-----------------|
| `find_email.py` | domain + (optional) name | `email`, `email_confidence` |
| `linkedin_profile.py` | name + company | `linkedin_url`, `role`, `bio_summary` |
| `company_context.py` | domain | `website_summary`, `tech_stack[]`, `signals[]` |

**Rate limits:**
- Hunter.io: 25/mo free → cache aggressively in `state/enrich_cache.json`
- Apollo: 50 credits free → only call if Hunter returns nothing

**Skip condition:** If email confidence <60 AND no LinkedIn URL → `status: unreachable`. Don't waste outreach credits.

---

## Stage 3 — Qualify (`stages/03_qualify/`)

**Goal:** Score prospect fit 0-100 against ICP + offer.

**Tool:** `score_fit.py` (LLM — `euri/gpt-4o-mini`)

**Scoring rubric** (max 100):
- Industry match: 25
- Size match (employees / revenue): 20
- Geography match: 10
- Role seniority (decision-maker): 20
- Signal strength (hiring, funding, tech stack, recent content): 25

**Thresholds:**
- `fit_score >= 70` → proceed to outreach
- `50-69` → queue for nurture (drip only, no 1:1 hook)
- `<50` → archive, do not contact

Output: `fit_score: int`, `fit_reasoning: str`, `pain_hypothesis: str` (saved to state).

---

## Stage 4 — Outreach (`stages/04_outreach/`)

**Goal:** Send hyper-personalized first touch. Draft LinkedIn DM. Schedule followups.

**Rules (non-negotiable):**

1. **Every email must include:**
   - Physical postal address (CAN-SPAM)
   - One-click unsubscribe link (CAN-SPAM)
   - Clear sender identity (name + company)
   - Honest subject line (CAN-SPAM)
   - DPDP lawful-basis note (legitimate interest for B2B OR opt-in for B2C)
2. **Rate limits** (enforced in code):
   - 50 emails/day/sender max
   - 1 email per prospect per 3 days
   - If a prospect has `do_not_contact: true` OR appears in `state/suppression.json` → abort
3. **Every message personalized** — must contain at least one company-specific hook (not "I saw your website"). If LLM returns a generic message, re-prompt or skip.
4. **LinkedIn DM = draft only.** Write to `.tmp/drafts/linkedin/{prospect_id}.md`. Human copies and sends. No automation against LinkedIn ToS.

**Tools:**
| Tool | Purpose |
|------|---------|
| `personalize_email.py` | Generate subject + body with company-specific hook |
| `send_email.py` | Send via Resend. Enforces compliance + rate limits. |
| `linkedin_dm.py` | Generate DM draft → `.tmp/drafts/linkedin/` |
| `followup_sequence.py` | Schedule day-3, day-7, day-14 variants |

**Unsubscribe flow:** `EMAIL_UNSUBSCRIBE_URL` in `.env` points at a public endpoint (or mailto). Every unsubscribe click/email adds the address to `state/suppression.json`.

---

## Stage 5 — Discovery (`stages/05_discovery/`)

**Goal:** When a prospect replies positively, book a discovery call and prep.

**Reply detection:** Handled manually (MVP) OR via Resend inbound webhook → `state/replies.json`.

**Tools:**
| Tool | Purpose |
|------|---------|
| `booking_link.py` | Return prefilled Cal.com/Calendly URL for this prospect |
| `prep_brief.py` | Generate 1-page pre-call brief (prospect context + pain hypothesis + 3 discovery questions tailored to ICP) |

Output: `.tmp/briefs/{prospect_id}.md` — read before the call.

**Discovery framework:** BANT+ (Budget, Authority, Need, Timeline, + Pain severity + Decision process). See `workflows/discovery-call-script.md`.

---

## Stage 6 — Proposal (`stages/06_proposal/`)

**Goal:** Turn raw call notes into a structured proposal draft.

**Tool:** `generate_draft.py`

**Input:** call notes markdown + `config/offer.yaml` + prospect record
**Output:** `.tmp/proposals/{prospect_id}-YYYY-MM-DD.md` with sections:
1. Executive summary (1 paragraph)
2. Understanding of their situation (quotes from call)
3. Proposed approach (3-step)
4. Deliverables
5. Timeline
6. Investment (range from offer.yaml)
7. Next steps (2-option close)

**Manual step:** Review, edit, approve → send via separate channel (Docs/Notion). Automation stops at draft — NEVER auto-send proposals.

---

## Stage Transitions (State Machine)

```
scraped
  → enriched       (Stage 2 ok)
  → unreachable    (Stage 2 no email + no LI)
enriched
  → qualified      (score >= 70)
  → nurture        (score 50-69)
  → archived       (score <50)
qualified
  → contacted      (first email sent)
contacted
  → engaged        (reply positive)
  → no_reply       (after 3 followups, 21 days)
engaged
  → booked         (discovery call scheduled)
booked
  → call_done      (call happened, notes logged)
call_done
  → proposal_sent  (human sends proposal)
proposal_sent
  → won | lost
```

Every transition writes a row to `state/transitions.log` with timestamp + reason.

---

## Orchestrator: `tools/run_pipeline.py`

```bash
# Dry-run end-to-end with 5 prospects (no real calls, no real sends)
python tools/run_pipeline.py --icp config/icp.yaml --limit 5 --dry-run

# Real: single stage only
python tools/run_pipeline.py --stage 02_enrich --limit 20

# Real: full loop, 50 prospects
python tools/run_pipeline.py --icp config/icp.yaml --limit 50
```

**Orchestrator behavior:**
- Loads state
- Finds prospects matching stage-entry status
- Runs stage tool(s) on them
- Updates state after each prospect
- Respects `--dry-run` (pipes through every tool; no emails, no paid-API calls)
- Writes `runs/YYYY-MM-DD-pipeline.md` summary at end

---

## Learn (KPIs Tracked Per Run)

Dashboard (`tools/dashboard.py`) reads `state/` and shows:

| Metric | Target |
|--------|--------|
| Scrape → Qualified rate | >30% |
| Qualified → Contacted rate | 100% |
| Contacted → Replied rate | >8% |
| Replied → Booked rate | >40% |
| Booked → Proposal rate | >80% |
| Proposal → Won rate | >25% |

Track per ICP segment + per message variant (A/B).

---

## Compliance Checklist (Every Send)

- [ ] Unsubscribe link present + working
- [ ] Physical postal address in footer
- [ ] Sender name + email honest (no spoofing)
- [ ] Subject line truthful (no fake Re: / Fwd:)
- [ ] Prospect NOT in `state/suppression.json`
- [ ] Rate limit check passed (50/day, 1/prospect/3days)
- [ ] DPDP lawful-basis declared (legitimate interest OR opt-in)
- [ ] Personalization hook present (LLM check)

If ANY box unchecked, abort send. Log to `runs/` with reason.

---

## Failure Modes + Recovery

| Failure | Handling |
|---------|----------|
| Scraper returns 0 results | Broaden query, try alt scraper, notify user |
| Hunter credits exhausted | Fall through to Apollo; if both dry, mark `unreachable` |
| LLM returns generic copy | Re-prompt once; if still generic, skip (don't send) |
| Resend rate limit hit | Pause sender, resume next day |
| Prospect replies "unsubscribe" | Add to suppression IMMEDIATELY, confirm via email |
| Proposal generation fails | Keep call notes in `.tmp/briefs/`, flag for manual draft |

Every failure → log entry in `learning-hub/ERRORS.md`.

---

## Related Workflows

- `outreach-templates.md` — canonical copy templates by ICP
- `discovery-call-script.md` — BANT+ framework for calls
