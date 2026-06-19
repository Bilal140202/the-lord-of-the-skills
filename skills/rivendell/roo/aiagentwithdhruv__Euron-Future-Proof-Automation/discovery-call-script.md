# Discovery Call Script — BANT+ Framework

> 30-minute structure. Use the prep brief (`.tmp/briefs/{prospect_id}.md`) before the call.

---

## Objectives (in priority)

1. Decide if this is a fit for the 30-day sprint offer.
2. Uncover the one workflow that hurts the most (confirm the pain hypothesis).
3. Understand decision process (who signs the PO, on what timeline).
4. Earn the right to send a proposal.

---

## Structure (30 min)

### 0-2 min — Frame the call
> "Appreciate you making time. My goal today isn't to pitch — it's to figure
> out if what we do is actually a match for where you're trying to go. If it
> is, I'll send a tight proposal. If not, I'll tell you who is. Cool?"

### 2-10 min — Their situation (LISTEN)
Open questions. Let them talk. Take notes verbatim — their words become the
proposal's "Your situation" section.

- "What's the most manual thing your team does right now?"
- "When did that start feeling painful?"
- "What does good look like in 6 months?"
- "What have you tried already, and what didn't work?"

### 10-18 min — BANT+ (discover, not interrogate)
Weave these in — don't read them off.

- **B**udget: "What does a project like this typically look like budget-wise at your company?" (you're calibrating, not asking their number)
- **A**uthority: "Who else weighs in on a decision like this?"
- **N**eed: Already uncovered in open questions. Restate their pain in your words and confirm.
- **T**imeline: "If we started tomorrow, what would change for you in 30 days?"
- **+** **Pain severity**: "On a scale of 1-10, how much is this costing you right now?"
- **+** **Decision process**: "How do decisions like this get made internally?"

### 18-25 min — Position the offer (tie it to their words)
> "Based on what you said about {X}, here's what I'd propose..."
> 30-day sprint. One automation. $5-15K. Pilot-first.
> Reference the case study from offer.yaml that's closest to their vertical.

### 25-30 min — Close
Two options:
> "Two options from here: I send a 1-page proposal by Friday and we schedule
> a 20-min review Monday. Or, if you'd rather loop in {decision-maker} first,
> I send you an intro doc to share. Which feels right?"

---

## Red flags (slow down or disqualify)

- Can't articulate the pain in concrete terms → not ready
- Wants 50 features → scope mismatch; politely disqualify
- Budget is 10x smaller than offer → politely exit
- Decision "by committee of 7" → long cycle; qualify hard
- "We already have an in-house AI team of 10" → disqualifier

---

## Green flags (move fast)

- Names a specific workflow + a specific cost (hours/$ lost)
- Already tried 1-2 partial solutions that didn't stick
- One or two decision-makers (founder + head of X)
- "We were just talking about this last week"

---

## After the call

1. Write call notes to `.tmp/notes/{prospect_id}-YYYY-MM-DD.md`
2. Mark prospect `call_done` in state
3. Generate proposal:
   ```bash
   python stages/06_proposal/generate_draft.py \
     --prospect-id prs_abc123 \
     --notes-file .tmp/notes/prs_abc123-2026-04-20.md \
     --confirmed-pain "Manual CRM routing"
   ```
4. Review, edit, send proposal via your preferred channel (Notion / Docs / PDF)
5. If they said no: mark `lost`, add `do_not_contact: true` if they asked to be removed

---

## Output of the call (the ONE thing that matters)

A clear yes/no on:
- "Does the 30-day sprint offer solve their most painful workflow?"

If yes → proposal by Friday.
If no → polite exit, log, learn.
