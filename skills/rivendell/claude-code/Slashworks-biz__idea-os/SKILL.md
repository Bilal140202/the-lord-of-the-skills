---
name: idea-os
description: Use when a user shares a raw product idea or problem statement and wants a structured pipeline from clarifying questions through deep research, a PRD, and a phased execution plan — written as files they can take forward. This is an end-to-end idea-to-build-ready workflow, not a quick-feedback skill (use `idea-refine` for that) and not a PRD editor (use `product-management` for that). Trigger phrases include "I have an idea for…", "help me build X", "validate and plan this concept", "what should I build?" — when the user clearly wants the full multi-phase artifact output, not a one-shot answer. Covers market sizing, SWOT, JTBD, competitor mapping, positioning, distribution, MVP slicing, metrics, platform and stack recommendations, a user-journey diagram (mermaid), phased build with kill criteria, and adapts depth to idea complexity.
---

# idea-os

An **operating system** for turning a raw idea into a build-ready plan. Takes a rough problem statement and produces four files: clarifying questions, deep research, a PRD, and a phased execution plan with platform/stack picks, a user-journey diagram, and kill criteria.

## What it produces

Four files in the current working directory (use `pwd`). Filenames are canonical.

1. `questions.md` — sharp clarifying questions (skip if the brief is already dense or run is autonomous)
2. `research.md` — market, competitors, SWOT, JTBD, distribution, risks, insights
3. `PRD.md` — problem, users, scope, non-goals, metrics, solution shape
4. `plan.md` — user journey + mermaid, platform + stack, phased build, kill criteria, next steps

## Workflow — 5 phases, in order

Do not skip or reorder. Weak inputs produce weak outputs; each phase feeds the next.

### Phase 1 — Triage

Classify the idea on two axes. Depth of research, PRD, plan, and question-count scale with tier; vocabulary scales with sophistication.

**Idea tier (T1/T2/T3) — complexity:**
- **T1 (Simple)** — single-user utility, weekend hobby, CLI, small app with no network effects
- **T2 (Moderate)** — multi-user app, SaaS MVP, AI wrapper with distinct users and workflows
- **T3 (Complex)** — marketplace, two-sided network, B2B SaaS with procurement, regulated or deep tech

**Sophistication (S1/S2/S3) — builder vocabulary:**
- **S1** — first-time builder, non-technical. Explain every term, no frameworks by name
- **S2** — hobbyist or junior PM. Introduce frameworks with one-line definitions
- **S3** — founder, senior PM, shipped before. Use the full vocabulary

State your classification in one line (e.g. "T2 · S2 — moderate SaaS, builder has shipped before") before proceeding. If ambiguous, ask at most one question.

See `references/clarifying-questions.md` for the question bank tiered to these levels.

### Phase 2 — Clarify

Write `questions.md` using `assets/questions-template.md`. Pick 4–18 questions (count scales with complexity) matched to the idea type — SaaS, marketplace, consumer, AI wrapper, dev tool, hardware, content. Group into three buckets: **Who and Pain · Scope and Wedge · Constraints and Goals**.

Every question must be actionable — the answer must change what you build. Generic questions ("who is your user?") are rejected; force specifics ("describe the last time your target user hit this pain — what did they do instead?").

After writing, **stop and wait** for answers. Do not research yet.

Skip `questions.md` entirely if the brief is already dense; state assumptions and proceed.

### Phase 3 — Research

Write `research.md` using `assets/research-template.md`. Use WebSearch + WebFetch for real signal. Never hallucinate numbers; flag `[assumption]` or cut.

**Pre-flight checklist** (a floor):
- ≥5 WebSearches + 2 WebFetches on named competitors (pricing, positioning, traction)
- ≥1 search on market size / category growth with a sourced number
- ≥1 search on "why now" — tech, behavioral, regulatory, or cost unlock
- 1 community scan (Reddit, HN, Discord, FB group) where the target user congregates
- Note the date of every source

Sections required (depth scales with complexity):

1. Problem validation → `references/research-frameworks.md`
2. Jobs-to-be-done → `references/research-frameworks.md#jtbd`
3. Market (TAM/SAM/SOM, segmentation, WTP) → `references/market-analysis.md`
4. Competitors (direct, indirect, substitutes; positioning map; feature matrix) → `references/competitor-analysis.md`
5. SWOT → `references/research-frameworks.md#swot`
6. Distribution (first 100 users, channel CAC, founder actions) → `references/distribution.md`
7. Risks
8. Insights — 3–7 non-obvious findings that change the build. Most valuable section; no filler.

### Phase 4 — PRD

Write `PRD.md` using `assets/PRD-template.md`. Anatomy + tier-scaled sections + anti-patterns in `references/prd-structure.md`. Non-goals section is mandatory — it's where bad PRDs die.

### Phase 5 — Plan

Write `plan.md` using `assets/plan-template.md`. Must include:

1. User journey (text + mermaid) → `references/user-journey.md`
2. Platform recommendation with reasoning tied to research → `references/platform-recommendation.md`
3. Stack recommendation (conservative / modern / cutting-edge matrix) → `references/stack-recommendation.md`
4. Phase breakdown (MVP → v1 → target) with scope, success metrics, kill criteria, distribution per phase → `references/mvp-slicing.md`
5. Metrics per phase (North Star + inputs + counter) → `references/metrics-framework.md`
6. Immediate next steps (3–5 actions for the next 1–2 weeks)

## Autonomous mode

When there's no live user (batch run, test, dry-run, or the user said "just proceed"): still write `questions.md` to make decisions legible, then simulate plausible answers consistent with a stated persona at the chosen tier. At the top of `research.md`, add an **Assumptions in lieu of answers** block listing each assumed answer and flagging the load-bearing ones. The reader should see exactly what you decided for them.

## Output conventions

- Write to `pwd` unless user specifies
- Use the target-market currency consistently (USD, INR, EUR, etc.)
- Relative links between files (`[PRD](PRD.md)`)
- Header block at top of each file: idea title, date (ISO), tier (T1/T2/T3) + sophistication (S1/S2/S3)
- Render on GitHub — mermaid, tables, clean headings

## Top anti-patterns

- Generic SWOT ("good team" — cut)
- Unsourced TAM numbers — source it or flag `[assumption]`
- PRD with no non-goals — reject
- Plan with no kill criteria — not a plan
- MVP as a feature checklist — MVP is a thin vertical slice, one user one job end-to-end
- Platform recommendation before understanding user context — research first

More in `references/prd-structure.md` (PRD anti-patterns) and `references/mvp-slicing.md` (MVP traps).

## Example

`examples/example-notion-for-dog-trainers.md` is a reference-only walkthrough showing the quality bar. Do not load it unless you need calibration — it's 500+ lines.
