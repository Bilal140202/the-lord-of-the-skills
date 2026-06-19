---
name: research
description: Multi-source research before acting on unknowns. Produces sourced findings with confidence levels ready for downstream use.
---
# /research

**What this does:** Multi-source research before acting on unknowns. Produces sourced findings with confidence levels ready for downstream use.

**When to use:** Before implementing with unfamiliar tech, validating an approach, comparing options, or answering questions that need current information.
**When NOT to use:** If the answer is in the existing codebase — read the code first.

## Session Announcement

At start, output:
```
Session: /research
Questions to answer:
  1. [question]
  2. [question]
Loading deep-research skill...
```

## Orchestration

This workflow invokes the deep-research skill and adds session coordination:

1. **List questions explicitly** before searching — state what decisions depend on the answers
2. **Load deep-research skill** — follow its full 5-step process
3. **Apply quality gate** — deep-research checklist must score 4/5 before acting on findings
4. **State decision alignment** — before handing off: "Decision: [what I'm about to decide]. Finding that supports it: [key finding + confidence]"
5. **Hand off** to downstream workflow

## Key Claim Definition

A claim is key if it meets **any** of criteria (a), (b), or (c) as defined in the deep-research skill.
Do not re-derive the criteria here — refer to the skill for the authoritative definition.

## Completion Gate

Before passing findings to any downstream skill or workflow:
- [ ] deep-research quality checklist scored 4/5 or higher
- [ ] Each key claim has 2+ corroborating sources
- [ ] Decision + supporting finding stated explicitly (the Validation Step)
- [ ] Confidence level declared for each finding

If any item fails: gather more sources. Do not hand off low-confidence findings to /brainstorm, /plan, or /design.

## Error Path

If sources are inaccessible: follow the deep-research skill's Error Path exactly.
Announce the failure reason and confidence level before presenting findings.
Do not present training-data knowledge as researched knowledge.

## Example Output

```
Session: /research
Questions: Is Prisma ORM suitable for 50k DAU Node.js app?

Research complete.

Question: Is Prisma ORM suitable for a Node.js app with 50k daily active users?
Finding: Yes, with connection pooling (PgBouncer) required for high concurrency.
Confidence: High — 3 primary sources agree
Sources:
  - prisma.io/docs/guides/performance/connection-pool (official)
  - prisma.io/blog/prisma-at-scale (official blog, 2024)
  - github.com/prisma/prisma/issues/12345 (confirmed at scale by maintainer)
Caveats: Benchmarks from 2024; Prisma 6.x characteristics may differ. Connection pool config is critical.

Quality checklist: 5/5 ✓
Decision: Use Prisma with PgBouncer for connection pooling.
Key finding: Official docs confirm PgBouncer required at this scale.

Handing off to: /plan (architecture confirmation)
```

## Handoff

Research output is consumed by:
- **/brainstorm** — feasibility phase (load before proposing technical approaches)
- **/plan** — architecture confirmation (load before writing implementation tasks)
- **/design** — options evaluation (load before comparing approaches)
- **User directly** — for questions the user asked explicitly

State which workflow receives these findings before ending the session.
