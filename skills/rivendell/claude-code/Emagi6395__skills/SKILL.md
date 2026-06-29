---
name: tournament-search
description: >
  Solves complex, open-ended problems using a knockout tournament mechanism. Generates an
  initial population of diverse candidate answers, pairs them into head-to-head matches,
  produces a hybrid "child" solution from each pair, and advances the best of the three
  through a bracket until a winner emerges. Use this skill whenever the user wants to
  competitively select the best answer from a field of alternatives, asks for a "tournament"
  or "bracket" style search, wants a faster alternative to full evolutionary search, or uses
  phrases like: "run a tournament on this", "bracket-style search", "let solutions compete",
  "knockout search", "find the best answer by elimination", or "which solution wins?".
  Also trigger when the problem is open-ended and the user wants a clear winner quickly
  rather than a deep multi-generation refinement.
---

# Tournament-Search

Knockout bracket search: generate diverse candidates, run head-to-head matches, synthesize a hybrid per match, advance the best of 3 (Parent A, Parent B, Hybrid) until one champion emerges. Includes a 3rd-place playoff. Faster than evo-search; quality ceiling is bounded by initial population diversity.

---

## Step 0: Problem Intake & Rubric

Identify problem type, constraints, audience, and scope. If ambiguous, ask one question.

### Trait Logging (off by default)
Activate when the user says things like *"keep the best ideas from losers"*, *"log traits"*,
or *"don't throw away good ideas"*. When active: before each elimination, extract and record
the loser's single most distinctive feature into a trait log for review at the end.

### Rubric Construction

Detect which mode applies:

| Mode | Trigger | Action |
|------|---------|--------|
| A: Auto | User gave only the problem | Generate 4–6 domain-appropriate criteria |
| B: Guided | User hinted at priorities | Generate rubric, weight toward stated priorities |
| C: Manual | User gave explicit criteria | Convert each into a scored rubric entry with anchors |

In all modes: augment vague criteria into scorable definitions, and always add:
> **Overall Fitness (30%):** "Would a knowledgeable expert prefer this over a competent
> but unremarkable response?" Scored holistically. Prevents narrow-criteria gaming.

**Present the rubric to the user and wait for confirmation before proceeding.**

Rubric format:
```
| Criterion      | Description              | Weight | Max |
|----------------|--------------------------|--------|-----|
| [Name]         | [Definition + anchors]   | X%     | 10  |
| Overall Fitness| Expert holistic score    | 30%    | 10  |
Weighted Total = Σ(score × weight)  [max = 10.00]
```

---

## Step 1: Initial Population & Bracket Draw

Default population: **8 candidates** (3 rounds + playoff). Fast mode: **4 candidates**
(2 rounds + playoff). Population must be a power of 2; round up if the user requests
an odd number and generate an extra candidate.

Generate all candidates using these diversity frames before scoring any:

| # | Frame |
|---|-------|
| 1 | Conventional / mainstream |
| 2 | Contrarian / challenges assumptions |
| 3 | First-principles / bottom-up |
| 4 | Analogy-led / draws from another domain |
| 5 | Risk-focused / emphasizes what could go wrong |
| 6 | Synthesis / combines multiple angles |
| 7 | Minimalist / most parsimonious |
| 8 | Maximalist / most comprehensive |

Score each candidate and display:
```
INITIAL POPULATION
| # | Frame        | Fitness | Key Strength  |
|---|--------------|---------|---------------|
| 1 | Conventional | X.X     | [one phrase]  |
```

**Bracket draw is random.** Shuffle candidate numbers and pair sequentially. Show the
bracket to the user before starting matches.

```
BRACKET DRAW
Match 1: [A] vs [B]
Match 2: [C] vs [D]
Match 3: [E] vs [F]
Match 4: [G] vs [H]
```

---

## Step 2: Run the Tournament

### Every Match Follows These 3 Steps:

**1. Synthesize a Hybrid**
Generate a third solution that inherits the key strength of each parent without their primary weaknesses. The hybrid must be a genuine conceptual synthesis, not a text blend. If trait logging is active, record each parent's most distinctive feature before generating the hybrid.

**2. Score All Three**
Evaluate Parent A, Parent B, and the Hybrid against the rubric. Record fitness and a
one-line diagnosis per competitor.

**3. Advance the Winner**
Highest scorer advances. On a tie, prefer the Hybrid.

Match display format:
```
MATCH [N]: [Candidate A] vs [Candidate B]
|          | Fitness | Strength     | Weakness     |
|----------|---------|--------------|--------------|
| Parent A | X.X     | [one phrase] | [one phrase] |
| Parent B | X.X     | [one phrase] | [one phrase] |
| Hybrid   | X.X     | [one phrase] | [one phrase] |
→ ADVANCES: [winner] (X.X)
[→ TRAIT LOGGED from [loser]: [one sentence]  ← only if trait logging is active]
```

### 8-Candidate Bracket

```
QUARTER-FINALS    (Matches 1–4): 4 winners advance
SEMI-FINALS       (Matches 5–6): 2 winners → Final | 2 losers → 3rd-Place Playoff
3RD-PLACE PLAYOFF (Match 7)    : L1 vs L2 → 🥉
FINAL             (Match 8)    : W1 vs W2 → 🏆
```

### 4-Candidate Bracket

```
SEMI-FINALS       (Matches 1–2): 2 winners → Final | 2 losers → 3rd-Place Playoff
3RD-PLACE PLAYOFF (Match 3)    : L1 vs L2 → 🥉
FINAL             (Match 4)    : W1 vs W2 → 🏆
```

---

## Step 3: Output

### 3.1 Podium Summary
```
🥇 1st — [Frame/description]   Score: X.X
🥈 2nd — [Frame/description]   Score: X.X
🥉 3rd — [Frame/description]   Score: X.X
```

### 3.2 Contrast Table (show before full solutions)
```
| Rank | Score | Defining Strength | Best Used When          |
|------|-------|-------------------|-------------------------|
| 🥇   | X.X   | [one phrase]      | [context where #1 wins] |
| 🥈   | X.X   | [one phrase]      | [context where #2 wins] |
| 🥉   | X.X   | [one phrase]      | [context where #3 wins] |
```

### 3.3 Full Solutions
Output all 3 podium solutions in full, labeled with rank and score.
User can override with plain language: *"just show me the winner"* → top_k=1.

### 3.4 Rubric Breakdown
Show per-criterion scores for the champion (1st place) only.

### 3.5 Bracket Recap
```
QF:    [A](X.X) vs [B](X.X) → [winner](X.X) ✓
       ...
SF:    [W1](X.X) vs [W2](X.X) → [winner](X.X) ✓  | Loser → playoff
       ...
3rd:   [L1] vs [L2] → 🥉 [winner](X.X)
Final: [W5] vs [W6] → 🏆 [champion](X.X)
```

### 3.6 Trait Log (only if trait logging was active)
```
TRAIT LOG: Ideas from Eliminated Candidates
- [Round 1, Candidate X]: [one-sentence description of their best feature]
- ...
These traits did not reach the final but may be worth incorporating manually.
```

---

## Parameters

| Parameter     | Default | Options             | Effect                                     |
|---------------|---------|---------------------|--------------------------------------------|
| population    | 8       | 4 or 8              | Initial candidates (must be power of 2)    |
| rubric_mode   | auto    | auto/guided/manual  | How the rubric is built                    |
| trait_logging | off     | on / off            | Log best traits from eliminated candidates |
| top_k         | 3       | 1–3                 | Podium solutions shown in full             |
| show_bracket  | true    | true / false        | Show full bracket recap                    |
| show_trace    | true    | true / false        | Show per-match score tables                |

Users set parameters in plain language. Examples:
- *"Quick tournament, 4 candidates"* → population=4
- *"Keep the best ideas from losers"* → trait_logging=on
- *"Just show me the winner"* → top_k=1
- *"Use these criteria: impact, clarity, feasibility"* → rubric_mode=manual

---

## Scoring Guidance

Score honestly. Inflated scores make match outcomes meaningless. A mediocre-but-coherent
answer scores 5–6. The hybrid winning its match is the ideal outcome; if hybrids consistently
lose to parents, make the synthesis more targeted. Keep candidate length appropriate to the
problem. Verbosity must not inflate fitness scores.
