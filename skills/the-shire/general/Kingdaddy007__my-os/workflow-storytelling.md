# WORKFLOW: STORYTELLING

**Version:** Gold v1.0
**Layer:** Execution workflow
**Tier:** 2 — loaded by task
**Purpose:** Formal workflow for the storytelling process. Defines entry gates, session approval points, iteration contracts, and exit criteria for creating `contexts/story.md` — the master narrative document that drives all subsequent design and animation decisions.

---

## WHAT THIS WORKFLOW DOES

This workflow governs the creation of `contexts/story.md`. It provides:
- Entry criteria (what must exist before storytelling begins)
- Session gates (when to pause and get approval)
- Iteration contract (how many rounds, what triggers a lock)
- Exit criteria (what must be true before story.md is locked)
- Handoff (what to invoke after story.md is locked)

---

## WHEN TO USE IT

Use this workflow when:
- Starting a new brand or marketing project
- Defining the narrative direction for a landing page
- Re-positioning an existing brand
- The project needs copy direction, visual direction, or motion direction

Do not use it when:
- Writing actual copy (use `skill-copywriting`)
- Editing existing copy (use `skill-copy-editing`)
- Technical research (use `skill-research-analysis`)

---

## REQUIRED FILES

### Skills to Load
- `skills/storytelling/SKILL.md` (narrative authority)
- `skills/storytelling/library/matching-guide.md` (mechanics that fit the brand archetype)

### Context Files Required (Entry Gate)
- `PRODUCT.md` — must exist (register, personality, audience)
- `contexts/research-brief.md` — must exist (do not proceed without it)

---

## EXECUTION SEQUENCE

### PHASE 1: LOAD CONTEXT

**Mode:** Designer (Discovery)

1. **Read PRODUCT.md** — extract register, brand personality, audience, anti-references
2. **Read `contexts/research-brief.md`** — extract brand summary, audience summary, competition summary, key insights
3. **Load `skill-storytelling`** — Sections 1-6
4. **Load `skills/storytelling/library/matching-guide.md`** — find mechanics that fit the brand archetype

**Gate:** Do NOT proceed if `PRODUCT.md` or `contexts/research-brief.md` does not exist.
If research-brief.md is missing, run skill-storytelling Section 1 (Research) first.

---

### PHASE 2: PRESENT 2-3 STORY DIRECTIONS

**Mode:** Designer (Exploration)

Based on the loaded context, present 2-3 story directions:

```
Direction A: [name]
- Approach: [Truby / McKee / Campbell / Calvino / Villeneuve / Miller / Lynch]
- Controlling Idea: [value shift formula]
- Emotional mode: [inner / outer / other]
- Form: [journey / room / gallery / universe]
- Narrative arc: [Brand Story / Product Journey / Hero's Journey / etc.]
- Why this works: [reasoning tied to brand personality and audience]

Direction B: [name]
- Approach: [different approach]
- Controlling Idea: [different value shift]
- Emotional mode: [different mode]
- Form: [different form]
- Narrative arc: [different arc]
- Why this works: [reasoning]

Direction C: [name]
- Approach: [another approach]
- Controlling Idea: [another value shift]
- Emotional mode: [another mode]
- Form: [another form]
- Narrative arc: [another arc]
- Why this works: [reasoning]
```

**Gate:** Wait for user approval before proceeding. User picks one direction or blends elements from multiple. Do NOT develop a direction without explicit user choice.

---

### PHASE 3: DEVELOP APPROVED DIRECTION

**Mode:** Designer (Construction)

Work through `skill-storytelling` Sections 2-6:

1. **Find the Story** (Section 2) — apply the chosen approach (Truby, McKee, Campbell, etc.)
2. **Structure the Story** (Section 3) — choose narrative arc, form, section breakdown
3. **Map the Emotions** (Section 4) — emotional modes, emotional arcs by archetype, pacing
4. **Design the Experience** (Section 5) — integration matrix (copy says / visual shows / animation does), proof mechanisms, trust techniques, copy direction, visual direction, motion direction
5. **Brand Archetype Storytelling** (Section 6) — apply the archetype-specific storytelling style

**Refinement:** Use `skill-copy-editing` Seven Sweeps Framework for systematic refinement of the story's copy direction.

**Gate:** Present the developed story (not yet written to file) for final approval. Show:
- Controlling idea
- Emotional arc
- Section breakdown
- Copy direction
- Visual direction
- Motion direction

Wait for explicit user approval before locking.

---

### PHASE 4: PRESENT STORY FOR FINAL APPROVAL

**Mode:** Communicator (Review)

Show the complete story document structure:

```markdown
# STORY: [BRAND NAME]

## The One Thing
[One sentence: what's the ONE message that must come through?]

## The Controlling Idea
[Value shift formula]

## The Designing Principle
[Abstract metaphor]

## Who Is the Hero?
[User as hero, brand as mentor]

## Section Breakdown
[Each section: purpose, headline direction, body direction, visual direction, layout direction, animation direction, emotion, proof mechanism]

## Copy Direction
[Headline strategy, tone, key messages, CTA strategy]

## Visual Direction
[Hero visual, image style, color mood, typography voice, layout rhythm]

## Motion Direction
[Hero animation, scroll behavior, climax pattern, resolve pattern, easing personality]
→ See contexts/motion-direction.md for implementation details.

## Brand Archetype
[Which archetype, storytelling style]

## Emotional Journey
[Section 1 emotion → Section 2 emotion → ... → Final emotion]
```

**Gate:** Ask: "Does this story feel right? Any adjustments before we lock it?"
Wait for explicit approval. Do NOT write story.md without user saying yes.

---

### PHASE 5: LOCK AND WRITE

**Mode:** Builder (Delivery)

1. **Write `contexts/story.md`** — the full story document as approved in Phase 4
2. **Confirm lock** — state clearly: "Story locked. This is now the source of truth for all subsequent design and animation decisions."
3. **Handoff** — "Next: Run `/impeccable-document` to build DESIGN.md from this story."

**Exit criteria:**
- [ ] `contexts/story.md` exists and is written
- [ ] User has explicitly approved the story
- [ ] Controlling idea is defined
- [ ] Section breakdown covers all page sections
- [ ] Copy direction is defined (headline strategy, tone, key messages, CTA)
- [ ] Visual direction is defined (hero visual, image style, color mood, typography voice)
- [ ] Motion direction is defined (hero animation, scroll behavior, climax pattern)
- [ ] Brand archetype is identified

---

## WHAT'S NEXT

After storytelling is complete (story.md locked):

1. **For visual system creation** → Run `/impeccable-document` to build DESIGN.md informed by story.md.
2. **For visual exploration** → Run `workflow-visual-brainstorm.md` to explore visual directions and create motion-direction.md (Phase 3C).
3. **For copywriting** → Use `skill-copywriting` — it will read story.md for copy direction constraints.

Story.md is the narrative foundation. Every subsequent Impeccable workflow reads it.

---

## QUALITY GATES

| Gate | Condition | Action |
|------|-----------|--------|
| Gate 1 — Missing context | PRODUCT.md or research-brief.md does not exist | Do not proceed. Create missing context first. |
| Gate 2 — No direction chosen | User has not approved a story direction | Present directions again. Do not develop without choice. |
| Gate 3 — No final approval | User has not explicitly approved the story | Present refined story. Do not lock without yes. |
| Gate 4 — Incomplete story | Any exit criterion is unmet | Complete missing element before writing story.md. |
