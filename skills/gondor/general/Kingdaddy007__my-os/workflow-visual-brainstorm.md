# WORKFLOW: VISUAL BRAINSTORMING

**Version:** Gold v1.1 (Impeccable Integration)
**Layer:** 8 — Execution Workflow
**Tier:** 2 — Loaded by task
**File:** workflows/workflow-visual-brainstorm.md
**Purpose:** The systematic sequence for generating visual design previews
          and design briefs during brainstorming and project inception —
          making design direction visible before implementation begins.
**Loaded When:** Starting a new UI project, defining visual identity,
              choosing between design directions, or preparing mockups.
**Inherits From:** execution-workflow.md (8-phase universal process)
**Note:** This workflow bridges the gap between text-based design decisions
       and actual visual output. It uses two paths: direct HTML previews
       (fast, built-in) and Google Stitch briefs (high-fidelity, external).

> [!IMPORTANT]
> **Impeccable now handles primary visual direction.** Use `/impeccable-teach` + `/impeccable-document` to establish design context, and `/impeccable-shape` for task-specific visual direction probes. This workflow remains useful as a **supplementary brainstorming tool** for quick HTML previews (Path A) and Stitch briefs (Path B) when exploring visual options before committing to the Impeccable design system.

---

## WHAT THIS WORKFLOW DOES

This workflow produces visual artifacts that help the user SEE design
decisions before committing to implementation. It prevents the most
expensive mistake in UI development: building something that looks
different from what the user imagined.

The output of this workflow is:

1. A visual preview of the design direction (HTML file or Stitch mockup)
2. Confirmed design tokens (colors, fonts, spacing) written to context files
3. A clear "this is what we're building" visual reference

---

## ACTIVATION

### Use When

- "I want to see what this will look like before we build it"
- "Let's figure out the visual direction"
- Phase 3A of workflow-project-inception (Visual Identity)
- "Show me some color options / layout options / typography options"
- "I want to mockup this in Stitch"
- "Prepare a design brief for me"
- Designing the first screen of a new application

### Do NOT Use When

- The visual identity is already locked and you're building production UI → use `workflow-design-ui.md`
- You're debugging or fixing an existing UI → use `workflow-debug-issue.md`
- The product has no user interface (CLI tools, pure backends)

---

## REQUIRED FILES

### Skills to Load

| Priority | Skill | Why |
| :--- | :--- | :--- |
| Primary | `skill-ui-ux` | Design principles that inform visual direction |
| Primary | `skill-storytelling` | Narrative constraints from story.md |
| Primary | `skill-cinematic-motion` | Motion vocabulary for Phase 3C exploration |
| Conditional | `skill-product-thinking` | If visual direction needs to align with user/business goals |

### Context Files to Load

| Context | When |
| :--- | :--- |
| `PRODUCT.md` | Required (defines register, users, brand personality) |
| `DESIGN.md` | If it exists (read existing color/typography/spacing tokens) |
| `DESIGN.json` | If it exists (read existing design details/components) |
| `stack-context.md` | If generating Path A previews (know what CSS framework is in use) |

---

## EXECUTION SEQUENCE

### PHASE 1: UNDERSTAND THE VISUAL NEED (5 minutes)

#### Mode: Designer (Discovery)

Before generating anything, clarify:

1. **What needs visualization?**
   - Color palette only → Path A (quick HTML)
   - Typography comparison → Path A (quick HTML)
   - Full page layout → Path B (Stitch brief) or Path A (wireframe)
   - Complete design direction → Both paths sequentially

2. **Is there existing visual context?**
   - Check for `PRODUCT.md` and `DESIGN.md` / `DESIGN.json`
   - Ask: "Are there reference products that capture your desired look?"

3. **What's the decision to make?**
   - "Light or dark?" — Show both
   - "This layout or that layout?" — Show both
   - "What colors?" — Show 2-3 palette options

**Gate:** Do NOT generate a preview until the question being answered is clear.

---

### PHASE 2: CHOOSE THE PATH (2 minutes)

Present the two options:

**Path A — HTML Preview (I generate it now, you see it in 60 seconds):**
Best for: quick color/typography/spacing decisions, simple layout wireframes.

**Path B — Google Stitch Brief (I prepare the brief, you run it in Stitch):**
Best for: full page mockups, complex layouts, production-quality visual fidelity.

Recommend one. Let the user decide.

**Gate:** Path is explicitly chosen before generation begins.

---

### PHASE 3A: EXECUTE — HTML PREVIEW PATH (10-15 minutes)

#### Mode: Builder (Preview Generation)

1. **Plan the preview sections** — List what the HTML file will contain
2. **Generate the HTML** — Single self-contained file:
   - Inline CSS (no external stylesheets)
   - Google Fonts via `@import` in `<style>` block
   - No JavaScript unless needed for interactive comparison
   - Dark background by default (most products target dark mode)
   - Responsive layout
   - Clear section labels explaining what each area shows
3. **Save the file** — Save to conversation artifacts directory
4. **Open in browser** — Use browser subagent to navigate to the file
5. **Capture and present** — Take a screenshot for discussion

#### Iteration Loop

After presenting:

- Ask: "What would you change? Colors, typography, layout, spacing?"
- Apply the requested changes
- Regenerate and re-present
- Repeat until the user says "looks good"

**Gate:** User explicitly approves the visual direction.

---

### PHASE 3B: EXECUTE — STITCH BRIEF PATH (10-15 minutes)

#### Mode: Designer (Brief Preparation)

1. **Gather all inputs**:
   - Visual mood (3-5 adjectives)
   - Reference products (2-3 with specific things to borrow)
   - Anti-references (what it should NOT look like)
   - Layout structure
   - Components needed
   - Color direction (even approximate)
   - Typography preferences

2. **Generate the design brief** using the template from the SKILL.md

3. **Include context files**:
   - If `DESIGN.md` / `DESIGN.json` exists, include current design system tokens and component patterns

4. **Present to user**:
   "Here's your Stitch brief. Steps:

   1. Go to stitch.google.com
   2. Paste this brief as your prompt
   3. Optionally attach the DESIGN.md file for more context
   4. Iterate in Stitch until you're happy
   5. Come back here and tell me 'I'm done with Stitch' — I'll extract the design tokens"

5. **Wait for return** — When the user comes back with approved Stitch output, proceed to Phase 4

**Gate:** User returns from Stitch with an approved direction.

---

### PHASE 4: LOCK THE DESIGN DIRECTION (5 minutes)

#### Mode: Architect (Decision Capture)

Regardless of which path was used:

1. **Extract design tokens**:
   - Background colors (CSS custom properties)
   - Text colors (primary, secondary, muted)
   - Accent/brand color
   - Feedback colors (success, warning, error)
   - Font families (headline, body, mono)
   - Type scale (sizes for headings, body, caption)
   - Spacing base unit
   - Border radius tokens
   - Shadow/elevation tokens

2. **Write to context**:
   - Run `/impeccable-document` or create/update `DESIGN.md` + `DESIGN.json` with all design tokens
 
3. **State the decision clearly**:
   "Visual direction locked: [1-2 sentence summary]. All tokens written to DESIGN.md / DESIGN.json."

---

### PHASE 5: HAND OFF (2 minutes)

#### Mode: Communicate

Transition to the next phase:

- If during project inception → return to `workflow-project-inception.md` Phase 3A Step 6 (External Prototyping) or Phase 4 (Runtime Contexts), whichever is next in your current position.
- If standalone design session → summarize decisions and suggest next workflow (workflow-design-ui or workflow-build-feature)

---

### PHASE 3C: ANIMATED PROJECT EXPLORATION

When the project involves cinematic motion (scroll animations, 3D, video),
add this phase after visual direction is locked (Phase 4).

**Load:** `skill-cinematic-motion` Section 1 (Creative Direction)

#### Step 1: Motion Direction Exploration

Present 2-3 motion directions based on the brand archetype:

| Direction | Hero Approach | Scroll Style | Climax | Why |
|-----------|--------------|-------------|--------|-----|
| Direction A | [pattern] | [style] | [pattern] | [reasoning] |
| Direction B | [pattern] | [style] | [pattern] | [reasoning] |
| Direction C | [pattern] | [style] | [pattern] | [reasoning] |

Example for a luxury wellness brand:
| Direction | Hero Approach | Scroll Style | Climax | Why |
|-----------|--------------|-------------|--------|-----|
| A: Editorial | SplitText chars + pinned section | Deliberate, sparse | Video mask reveal | High-fashion feel, bold typography |
| B: Warm | SplitText lines + gentle parallax | Smooth, breathing | Image mask expansion | Approachable, trustworthy |
| C: Minimal | Slow image zoom + fade text | Subtle, quiet | Bento grid reveals | Clean, confident, understated |

**Gate:** User picks a direction or blends elements from multiple.

#### Step 2: Pattern Selection

Based on the chosen direction, map specific patterns to each scroll section:

```
Hook (first section): [pattern name] — [brief description]
Build (middle sections): [pattern name] — [brief description]
Climax (one section): [pattern name] — [brief description]
Resolve (final sections): [pattern name] — [brief description]
```

#### Step 3: Asset Brief

For each section that needs external assets, generate a brief for the user
to create in Figma (or other tools):

**Image brief template:**
- Subject: [what's in the image]
- Setting: [background/environment]
- Lighting: [warm, cool, dramatic, soft]
- Mood: [emotional tone]
- Color palette: [dominant colors from DESIGN.md]
- Style: [editorial, lifestyle, product-focused, abstract]
- Dimensions: [aspect ratio, e.g., 16:9, 1:1, 4:3]

**For video assets:** Use `skill-cinematic-motion` Section 5 > AI Video
Prompt Template.

**Gate:** User confirms they can create/provide the assets, or placeholders
are agreed upon.

#### Step 4: Write Motion Direction

Create `contexts/motion-direction.md` with:
- Emotion diagnosis
- Brand archetype
- Motion vocabulary (easing, speed, density)
- Scroll narrative (hook → build → climax → resolve)
- Pattern selection per section
- Asset requirements (images, videos, 3D models)
- Placeholder strategy

**Gate:** Motion direction locked. File created.

#### Step 5: Hand Off to Animate

Transition to `workflow-impeccable-animate.md`:
- Motion direction is already established
- Asset planning is already done
- Pattern selection is already confirmed
- The animate workflow starts at Step 4 (Implement)

---

## QUALITY GATES

- **G1 (Clarity):** No preview generated without a clear question to answer
- **G2 (Path):** Path A or B explicitly chosen — not assumed
- **G3 (Approval):** User explicitly approves the visual direction before tokens are exported
- **G4 (Export):** Design tokens written to `DESIGN.md` / `DESIGN.json` — not left only in the preview

---

## ANTI-PATTERNS THIS WORKFLOW PREVENTS

| Anti-Pattern | How This Workflow Prevents It |
| :--- | :--- |
| "Build it and I'll tell you if I like it" | Visual preview shown before any production code |
| Describing colors in text | Path A renders actual color swatches |
| Generic Stitch prompts producing generic mockups | Path B generates detailed, specific design briefs |
| Design decisions lost after brainstorming | Phase 4 exports everything to context files |
| Spending 2 hours on a mockup that should take 5 minutes | Path A is designed for 60-second previews |
