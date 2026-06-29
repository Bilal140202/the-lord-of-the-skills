---
name: workflow-impeccable-animate
description: >
  Impeccable animate workflow. Adds cinematic motion, scroll storytelling,
  3D product showcases, and micro-interactions. Register-aware — adapts
  motion vocabulary to brand or product context.
---

# WORKFLOW: ANIMATE — CINEMATIC MOTION

**Version:** Gold v2.0
**Layer:** 8 — Execution Workflow
**Tier:** 2 — Loaded by task
**File:** workflows/workflow-impeccable-animate.md
**Purpose:** Add motion, animation, and cinematic storytelling to a UI. Routes
to the correct motion approach based on register (brand vs product) and loads
the appropriate skill patterns.
**Loaded When:** "It feels static / lifeless", "add scroll animations", "build
a 3D product viewer", "make this cinematic", "add micro-interactions", or any
task producing animated web surfaces.
**Inherits From:** execution-workflow.md (universal process)
**Loads:** `skill-cinematic-motion` (primary), `skill-ui-ux` (design laws)
**Reads:** `contexts/motion-direction.md` (emotion, archetype, vocabulary — created
during project inception Phase 3A), `PRODUCT.md` (register), `DESIGN.md` (tokens)

---

## STEP 1 — DETECT REGISTER AND CONTEXT

Read these files in order:

1. **`contexts/motion-direction.md`** — if it exists, it has everything:
   emotion diagnosis, brand archetype, motion vocabulary, scroll narrative,
   asset requirements. Use this as the primary source.

2. **`contexts/story.md`** — read after motion-direction.md and validate that
   motion-direction.md still matches the story's emotional intent. The story
   defines the WHY (emotional intent, narrative rhythm); motion-direction.md
   defines the HOW (specific patterns, easing values, scroll timelines).
   If they conflict, the story's intent wins — adjust motion accordingly.

3. **`PRODUCT.md`** — if motion-direction.md doesn't exist, read PRODUCT.md
   for register (brand vs product) and brand personality.

4. **If neither exists**, load `skill-cinematic-motion` Section 1 (Register
   Detection) and follow its diagnostic walkthrough to determine register,
   emotion, and archetype from the task description.

**Do not duplicate register rules here.** The skill's Register Detection and
Diagnostic Walkthrough are the single source of truth.

### Required Inputs

Before animating, confirm:
- The user goal (what should the user feel or accomplish?)
- The register (brand or product)
- The brand archetype (from motion-direction.md or skill diagnostic)
- The surface type (full page, single section, component, interaction)
- Performance constraints (mobile-first? heavy 3D OK?)

If any are unclear, ask before proceeding.

---

## STEP 2 — SELECT MOTION VOCABULARY

Load `skill-cinematic-motion` Section 1 (Creative Direction). It contains:
- Diagnostic walkthrough (emotion → motion → what NOT to use)
- Brand-to-motion matrix (7 archetypes → easing, speed, density, scroll, 3D)
- Worked examples (luxury wellness, tech startup, restaurant)
- Scroll narrative architecture (hook → build → climax → resolve)
- Restraint rules (when NOT to animate)

**Do not duplicate the matrix here.** The skill is the single source of truth
for motion decisions. This workflow handles process; the skill handles knowledge.

### Motion Type Mapping

| Motion Type | What It Is | Implementation |
|-------------|-----------|----------------|
| Type A (Static) | Standard layout, no major animation | CSS transitions for hover/focus only |
| Type B (Code Animation) | Scroll reveals, parallax, 3D, video scrub | GSAP + ScrollTrigger + R3F (see `skill-cinematic-motion` Sections 2-3) |
| Type C (Cinematic Video) | AI-generated video backgrounds | Use `skill-cinematic-motion` Section 5 (AI Video Prompt Template) for generation briefs |

Assign motion type to every major page section during design.

---

## STEP 3 — PLAN THE ANIMATION STRATEGY

### For Brand Register

Identify:
- **Hero moment:** What's the ONE signature animation? (Video scrub? 3D viewer? Text reveal?)
- **Scroll choreography:** Which sections get pinned? Which get parallax? Where's the climax?
- **Density rhythm:** Alternate between full-bleed visual, text-only, and massive typography.
- **Restraint points:** Where should there be NO animation? (Navigation, footer, mobile)

### For Product Register

Identify:
- **Feedback layer:** Which interactions need acknowledgment? (Buttons, toggles, forms)
- **Transition layer:** Which state changes need smoothing? (Show/hide, expand/collapse)
- **Loading layer:** Skeleton states, progress indicators
- **Delight moments:** One or two subtle surprises, not everywhere

---

## STEP 3A — PLAN ASSETS

Before implementing, classify every section by what it needs. Some things the
code creates. Some things you need to bring from outside.

Load `skill-cinematic-motion` Section 5 (Asset Planning). It contains:
- Asset classification table (what code creates vs what's external)
- AI video prompt template + examples
- 3D model requirements template
- Placeholder strategy
- Output template for presenting assets to the user

**Do not duplicate the templates here.** The skill is the single source of truth
for asset planning. This workflow says WHEN to plan assets; the skill says HOW.

Present the asset plan to the user before implementation begins.

---

## STEP 3B — VISUAL CONCEPT (Brand Register Only)

**Skip for product register** — micro-interactions are low cost to rebuild if wrong.

Before writing any GSAP code, validate the animation direction visually:

1. **Create a frame-by-frame description** of each animation act:
   - What does the user see at 0%, 25%, 50%, 75%, 100% scroll?
   - For 3D/R3F: describe the camera position and scene state at each scroll milestone
   - For scroll reveals: describe what enters, from where, with what easing

2. **Present to user for approval:**
   ```
   Hook (0-25%): [description of what user sees, animation behavior]
   Build (25-50%): [description]
   Climax (50-75%): [description — the peak moment]
   Resolve (75-100%): [description — easing down to CTA]
   ```

3. **If approved** → proceed to Step 4 (Implement)
4. **If changes needed** → revise plan and repeat

**Gate:** Do not implement cinematic animation without user approval of the visual concept.
For a solo developer in sprint bursts, a wrong-direction cinematic build is a sprint-killer.

---

## STEP 4 — IMPLEMENT

Load `skill-cinematic-motion` and follow the relevant section.

**Important:** Use placeholders from Step 3A for any external assets that haven't
been provided yet. Build the full animation system with placeholders, then swap
real assets when they arrive. Don't block on asset delivery.

### Brand Register Implementation

1. **Set up stack:** Vite + React + Tailwind + GSAP + R3F (if 3D needed)
2. **Create constants layer:** Separate all copy into `constants/index.js`
3. **Build CSS design system:** `index.css` with `@theme` tokens and `@utility` classes
4. **Build sections following scroll narrative:** Hook → Build → Climax → Resolve
5. **Apply motion patterns from skill Section 2:** Video scrub, parallax, mask, scatter, SplitText
6. **If 3D needed, apply skill Section 3:** Zustand store, R3F Canvas, studio lighting, model switching
7. **Mobile performance gate:** Apply MOBILE SCROLL STRATEGY — disable pinned sections and video scrubbing, but replace with CSS reveal cascade (`.reveal-on-scroll`). Each narrative act (Hook, Build, Climax, Resolve) must remain visually distinct via background changes, typography scale shifts, and reveal timing. Never collapse into a raw vertical stack.
8. **Deploy:** Vercel or Hostinger with SSL

### Product Register Implementation

Apply `skill-cinematic-motion` Section 4 (Framer Motion). It contains:
duration guide, easing rules, 8 interactive states, focus rings, reduced
motion patterns, and code patterns for state transitions, modals, hover
cards, staggered lists, and page transitions.

**Do not duplicate the rules here.** The skill is the single source of truth
for product-register motion.

### Asset Swap

When real assets arrive, follow `skill-cinematic-motion` Section 5 (Asset
Integration) for the exact swap procedures.

---

## STEP 4A — ITERATE

Animation is not one-shot. After building, show the result and get feedback.

### Mockup Review

1. **Show the result** — open in browser, scroll through the full page
2. **Ask specific questions:**
   - "Does the scroll speed feel right for this brand?"
   - "Is the climax moment strong enough?"
   - "Does the hero reveal match the brand personality?"
   - "Any section feel too fast, too slow, too busy, too empty?"
3. **Apply feedback** — adjust timing, easing, density, or patterns
4. **Re-show** — repeat until satisfied

### When to Loop Back

- "The hero feels too aggressive" → slow down easing, reduce SplitText stagger
- "The middle is boring" → add parallax, increase density, alternate structure
- "The climax isn't strong enough" → upgrade pattern (fade → mask expansion)
- "It feels too template-y" → check slop test (brand.md), adjust typography/colors
- "Try a different style" → return to motion-direction.md, pick a different direction

### When to Proceed

User says: "Looks good" / "That works" / "Ship it"

---

## STEP 5 — VERIFY

Run `skill-cinematic-motion` Non-Negotiable Checklist. Every item must pass.
The checklist covers register detection, GSAP patterns, 3D patterns, mobile
gating, accessibility, and deployment.

### Deployment Verification (workflow-specific)

- [ ] Production build (`npm run build`) compiles without errors
- [ ] HTTPS/SSL configured for production
- [ ] All assets served from correct paths (no broken images/videos)

---

## STEP 6 — CRITIQUE

Ask:
- Is the motion serving the brand, or is it decoration?
- Would a user say "AI made that" (slop test)?
- Is the scroll rhythm monotonous? (Same density throughout = boring)
- Are there moments of rest between high-intensity sections?
- Does the 3D viewer add value, or is it a tech demo?
- On mobile, does it still work without the animation?

---

## STEP 7 — DELIVER

```markdown
## What Was Built
[1-2 sentence summary of the animated feature]

## Register & Motion Vocabulary
[Brand/Product] → [archetype] → [easing, speed, density choices]

## Animation Strategy
[Hero moment, scroll choreography, density rhythm, restraint points]

## Sections Implemented
- Hook: [approach]
- Build: [approach]
- Climax: [approach]
- Resolve: [approach]

## Technical Stack
[GSAP, R3F, Zustand, Framer Motion — which were used and why]

## Mobile Behavior
[What was disabled, what was kept, what was replaced]

## Key Decisions
[Non-obvious choices and rationale]

## What to Test
[How to verify each animation works]
```

---

## QUALITY GATES

| Gate | Condition | Action |
|------|-----------|--------|
| Register unclear | Cannot determine brand vs product | Clarify before animating |
| Motion type mismatch | Dashboard with cinematic parallax | Correct to product register |
| No mobile fallback | Pinned sections work on desktop only | Add `useMediaQuery` guard |
| Video not re-encoded | Standard MP4 used for scroll scrub | Re-encode with `ffmpeg -g 1` |
| No reduced motion | `prefers-reduced-motion` ignored | Add crossfade alternatives |
| Slop test fail | Looks generic/AI-generated | Rework visual identity |

---

## ANTI-PATTERNS

Consult `skill-cinematic-motion` Anti-Patterns table. It maps "Vibe Coding
(Anti-Pattern)" to "Cinematic Standard (Engineering)" for 16 specific patterns.

---

## ACTIVATION CHECKPOINTS

In long conversations, context gets lost. At these points, explicitly
(re-)load the skill or re-read context files:

| Checkpoint | What to Do | Why |
|-----------|-----------|-----|
| After PRODUCT.md is created | Load skill Section 1, run diagnostic walkthrough | Establish motion direction while brand is fresh |
| Before implementing any section | Re-read `contexts/motion-direction.md` | Confirm pattern selection still matches the direction |
| User says "make it look better" | Load skill Section 1 + brand.md Slop Test | Re-evaluate if current patterns serve the brand |
| User provides new assets | Load skill Section 5 (Asset Integration) | Follow correct swap procedures |
| User says "try a different style" | Return to motion-direction.md, pick new direction | Don't assume the first choice is final |
| User says "add 3D" | Load skill Section 3, check if R3F is installed | 3D has different dependency chain |
| Long gap between implementation steps | Re-read DESIGN.md and motion-direction.md | Context may have shifted |
| User changes brand direction | Re-run full diagnostic walkthrough | Motion vocabulary must match new direction |

**Don't assume the AI remembers.** In long conversations, explicitly re-load
the skill and re-read context files at each checkpoint.

---

## FINAL RULE

Motion should serve the brand and guide the user. A luxury site with snappy
elastic transitions is wrong. A dashboard with cinematic parallax is wrong.
Match the motion to the personality. When in doubt, do less.
