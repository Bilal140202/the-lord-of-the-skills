# WORKFLOW: DESIGN UI — IMPECCABLE COMMAND CENTER

**Version:** Gold v2.0 (Impeccable Authority)
**Layer:** 8 — Execution Workflow
**Tier:** 2 — Loaded by task
**File:** workflows/workflow-design-ui.md
**Primary Mode:** Designer
**Secondary Modes:** Builder, Product Thinking, Architect, Performance, Reviewer, Security
**Purpose:** The master orchestration workflow for all UI/UX design work. Routes to the correct Impeccable workflow based on the task, maps the 3-tier lifecycle, and provides UX-specific execution for flow mapping, state coverage, and accessibility.
**Loaded When:** Building frontend components, designing user flows, creating new pages or views, improving existing UI, improving usability, or designing interaction states.
**Inherits From:** execution-workflow.md (universal process)

**Design Authority:** Impeccable owns all visual design, UI craft, and motion work. This workflow is the routing layer that tells Anti-Gravity WHICH Impeccable workflow to run and WHEN. The passive design knowledge (craft laws, anti-patterns) lives in `skills/ui-ux/SKILL.md`.

---

## THE IMPECCABLE DESIGN LIFECYCLE

All design work follows this 3-tier lifecycle. These workflows are not optional add-ons — they ARE the design execution system.

### TIER 1: CONTEXT CREATION — "Who are we designing for?"

Run once per project, during **Project Inception** (Phase 3A).

| Workflow | What It Creates | When |
| :--- | :--- | :--- |
| `/impeccable-teach` | **PRODUCT.md** — strategic design context (register, users, brand personality, anti-references, design principles) | Start of any new project with UI |
| Research + Story (skill-storytelling) | **contexts/research-brief.md** + **contexts/story.md** — master narrative document driving all design | After PRODUCT.md exists, before any visual system is defined |
| `/impeccable-document` | **DESIGN.md** + **DESIGN.json** — visual system (tokens, typography, colors, components, do's/don'ts) | After story.md exists, so visual tokens serve the narrative |
| Visual Brainstorm (incl. Phase 3C) | **contexts/motion-direction.md** — scroll motion direction | After DESIGN.md exists; Phase 3C creates motion-direction.md as single authority |

PRODUCT.md and DESIGN.md live at the project root alongside Anti-Gravity's `contexts/` files. Anti-Gravity contexts handle engineering and product truth; Impeccable contexts handle design truth.

**Sequence is critical:** teach → research → story → document → visual-brainstorm → prototype.

### TIER 2: BUILD — "How do we make this feature look and work?"

Run during **Build Feature** (Step 7c — Client Layer) for every UI task.

| Workflow | What It Does | When |
| :--- | :--- | :--- |
| `/impeccable-shape` | Creates a **task-specific design brief** — discovery interview, visual direction probes, confirmed brief with scope, states, hierarchy, interaction model | Before coding any UI. Produces the blueprint. |
| `/impeccable-craft` | **Full build loop** — runs shape internally → generates visual mock → builds production code → browser verification → critique-and-fix loop | The "golden path" for building any UI feature end-to-end |
| `/impeccable-live` | **Real-time browser editing** — select elements, pick a design action, get AI-generated variants hot-swapped via HMR | When a dev server is running and you want interactive variant exploration |

**Craft is the default.** When building a new UI feature, run `/impeccable-craft`. It handles everything: shape (planning), mock (visual direction), build (implementation), and verify (browser inspection). You only run `/impeccable-shape` separately when you want the design brief without the build.

### TIER 3: REFINEMENT — "How do we make it better?"

Run **post-build**, any time an existing UI needs improvement.

#### Review & Scoring

| Workflow | What It Does | Use When |
| :--- | :--- | :--- |
| `/impeccable-audit` | Technical quality scorecard (a11y, perf, responsive, theming, anti-patterns). Scores 0-20. | Post-build technical review |
| `/impeccable-critique` | Design director review — Nielsen heuristics, AI slop detection, cognitive load assessment. Scores 0-40. | Post-build design review |

#### Targeted Refinement

| Workflow | What It Adjusts | Use When |
| :--- | :--- | :--- |
| `/impeccable-polish` | Final detail pass — spacing, states, transitions, alignment, design system drift | "Make it production-ready" |
| `/impeccable-bolder` | Amplifies contrast, hierarchy, atmospheric treatment, visual confidence | "It feels weak / generic / timid" |
| `/impeccable-quieter` | Reduces visual noise, softens palette, calms motion, increases whitespace | "It feels noisy / overwhelming" |
| `/impeccable-distill` | Simplifies — removes excess, sharpens hierarchy, reduces cognitive load | "It's cluttered / confusing" |
| `/impeccable-clarify` | Fixes confusing wording, labels, error messages, state communication | "Users don't understand what's happening" |

#### Specific Dimension Rework

| Workflow | Dimension | Use When |
| :--- | :--- | :--- |
| `/impeccable-colorize` | Color strategy — palette, contrast, tonal relationships | "The colors aren't working" |
| `/impeccable-typeset` | Typography — type pairing, scale, hierarchy, weight strategy | "The typography feels off / flat" |
| `/impeccable-layout` | Spatial structure — grid, composition, information density | "The layout doesn't feel right" |
| `/impeccable-adapt` | Responsiveness — behavior across viewports and contexts | "It breaks on mobile / tablet" |
| `/impeccable-animate` | Motion — adds `motion` (Framer Motion) transitions, scroll-driven effects | "It feels static / lifeless" |
| `/impeccable-delight` | Personality — micro-interactions, easter eggs, celebration moments | "It works but has no soul" |
| `/impeccable-overdrive` | Convention breaking — pushes past safe design into unexpected territory | "It's correct but boring — take risks" |

#### Special Purpose

| Workflow | Purpose | Use When |
| :--- | :--- | :--- |
| `/impeccable-onboard` | Onboarding — empty states, tours, progressive disclosure, first-time flows | Building onboarding experiences |
| `/impeccable-extract` | Extracts design tokens from existing code into structured format | Capturing an existing design system |
| `/impeccable-optimize` | Performance optimization of UI assets and rendering | UI is slow, images too large |

---

## MOTION STANDARD

Motion is planned during Project Inception (Phase 3A) and executed during
Build (via `/impeccable-animate`). The motion direction is captured in
`contexts/motion-direction.md` and consumed by `skill-cinematic-motion`.

### Motion Type Mapping

Assign to every major page section during design:
- **Type A (Static):** Standard layout, no major animation. Text, forms, data tables.
- **Type B (Code Animation):** Scroll reveals, parallax, hover effects. Built with GSAP or `motion`.
- **Type C (Cinematic Video):** AI-generated video. Use `skill-cinematic-motion` Section 5 (AI Video Prompt Template).

### Motion Planning (During Inception)

After `/impeccable-teach` (PRODUCT.md) and `/impeccable-document` (DESIGN.md):

1. **Run diagnostic walkthrough** (skill-cinematic-motion Section 1):
   - Name the emotion (physical-object words)
   - Select brand archetype from the matrix
   - Choose what NOT to use
   - Select scroll rhythm

2. **Explore visual directions** (workflow-visual-brainstorm Phase 3C):
   - Present 2-3 motion directions
   - User picks one or blends elements
   - Map patterns to scroll sections
   - Generate image briefs for Figma

3. **Write motion-direction.md** with:
   - Emotion diagnosis, archetype, motion vocabulary
   - Scroll narrative (hook → build → climax → resolve)
   - Pattern selection per section
   - Asset requirements

### Motion Execution (During Build)

Via `/impeccable-animate`:
- Reads motion-direction.md (pre-established direction)
- Loads skill-cinematic-motion (patterns, anti-patterns, checklists)
- Iterates with mockup review (Step 4A)
- Verifies with non-negotiable checklist

### Register Rules

**Brand register** (landing pages, portfolios, campaigns):
- Ambitious motion allowed. Scroll-triggered transitions, typographic choreography.
- One well-orchestrated page-load with staggered reveals.

**Product register** (dashboards, apps, tools):
- 150-250ms state-change motion only. No page-load choreography.
- Motion conveys state — feedback, reveal, loading.

---

## HOW IMPECCABLE CONNECTS TO ANTI-GRAVITY

### During Project Inception

```
Phase 1-3: Problem, MVP, Stack (Anti-Gravity owns)
    │
Phase 3A: Design Identity (Impeccable takes over)
    ├── STEP 1: /impeccable-teach → PRODUCT.md
    │       ↓ (when PRODUCT.md exists)
    ├── STEP 2: Competitor profiling → competitor-profiles/_summary.md
    │       ↓
    ├── STEP 3: Research (skill-storytelling Section 1)
    │   ├── Research the brand (who, what, why, how)
    │   ├── Research the audience (needs, wants, objections)
    │   ├── Research the competition (reference competitor-profiles/_summary.md)
    │   └── Write contexts/research-brief.md
    │       ↓ (when research-brief.md exists)
    ├── STEP 3b: Story (skill-storytelling Sections 2-6)
    │   ├── Choose narrative arc (Brand Story, Product Journey, etc.)
    │   ├── Map emotional journey (Hook → Build → Climax → Resolve)
    │   ├── Define copy direction (headline strategy, tone, key messages)
    │   ├── Define visual direction (hero visual, image style, color mood)
    │   ├── Define motion direction (hero animation, scroll behavior)
    │   ├── Present 2-3 story directions to user
    │   ├── User picks one or blends elements
    │   └── Write contexts/story.md
    │       ↓ (when story.md exists)
    ├── STEP 4: /impeccable-document → DESIGN.md + DESIGN.json
    │       (now informed by story.md — visual tokens serve narrative)
    │       ↓ (when DESIGN.md exists)
    ├── STEP 5: Visual Brainstorm (workflow-visual-brainstorm.md)
    │   ├── Explore visual directions (2-3 options, informed by story.md)
    │   ├── User picks direction
    │   ├── Phase 3C (motion exploration — single authority for motion-direction.md)
    │   │   ├── Present 2-3 motion directions (informed by story.md)
    │   │   ├── Map patterns to scroll sections
    │   │   ├── Generate image briefs for Figma
    │   │   └── Write contexts/motion-direction.md
    │   └── Lock visual direction → DESIGN.md + DESIGN.json
    │       ↓ (when visual direction is locked)
    ├── STEP 6: External prototyping (Figma AI, Stitch, Lovable)
    │
Phase 4-7: Contexts, Memory, Build Sequence (Anti-Gravity owns)
```

**Handoff rules:**
- After `/impeccable-teach` → next is Competitor profiling
- After Competitor profiling → next is Research (skill-storytelling Section 1)
- After Research → next is Story (skill-storytelling Sections 2-6)
- After Story → next is `/impeccable-document` (DESIGN.md now informed by story)
- After `/impeccable-document` → next is Visual Brainstorm
- After Visual Brainstorm → next is external prototyping or Build
- Visual Brainstorm Phase 3C is the SINGLE authority for creating motion-direction.md
- story.md is consumed by copywriting, visual brainstorm, document, and animate
- motion-direction.md is consumed by `/impeccable-animate` and `/impeccable-craft` during Build

### During Build Feature

```
Steps 1-6: Define, Context, Scope, Risks, Shape, Verify (Anti-Gravity owns)
    │
Step 7c — Client Layer (Impeccable takes over)
    ├── /impeccable-craft (full loop: shape → mock → build → verify)
    │   OR
    ├── /impeccable-shape → then manual build using SKILL.md craft laws
    │
Steps 8-11: Review, Verify, Deliver, Memory (Anti-Gravity owns)
    └── During Step 8: consider /impeccable-audit or /impeccable-critique
```

### Post-Build Diagnosis

```
UI exists → identify the issue → pick the right workflow:
    Weak?     → /impeccable-bolder
    Noisy?    → /impeccable-quieter or /impeccable-distill
    Static?   → /impeccable-animate (reads motion-direction.md if it exists)
    Generic?  → /impeccable-delight
    Broken?   → /impeccable-audit → fix → /impeccable-polish
```

**Note:** If motion-direction.md was created during inception, `/impeccable-animate`
already knows the brand archetype, motion vocabulary, and pattern selection.
It skips the diagnostic and goes straight to implementation.

If motion-direction.md doesn't exist (animation wasn't planned during inception),
`/impeccable-animate` runs the diagnostic walkthrough from skill-cinematic-motion
Section 1 to establish the direction before implementing.

---

## MOCKUPS & EXTERNAL PROTOTYPING

### Visual Exploration (Phase 3A Step 3)

Use `workflow-visual-brainstorm.md` for visual exploration BEFORE implementation:

1. **Path A — HTML Previews:** Quick color/typography/spacing comparisons. 60-second previews.
2. **Path B — Stitch Briefs:** Full page mockups via Google Stitch.
3. **Path C — Animated Project Exploration:** For projects with animation (Phase 3C):
   - Present 2-3 motion directions
   - Map patterns to scroll sections
   - Generate image briefs for Figma
   - Write `contexts/motion-direction.md`

**Handoff:** After visual direction is locked → proceed to external prototyping or Build.

### External Prototyping (Phase 3A Step 4)

1. **Figma AI:** Use `DESIGN.md` tokens and image briefs from Phase 3C to generate product images, lifestyle photos, hero images.
2. **Google Stitch / Lovable:** Bring `DESIGN.md` tokens and `prototyping-spec.md` to generate high-fidelity mockups.
3. **Quick HTML Previews:** Use `workflow-visual-brainstorm.md` Path A for fast comparisons.

**Handoff:** After prototyping → proceed to Build (Phase 4-7).

---

## UX-SPECIFIC EXECUTION (BELOW)

The sections below handle UX tasks that don't require visual craft — user flow mapping, state coverage, information architecture, accessibility audits, and interaction design. For building actual UI with visual craft, use `/impeccable-craft` above.

---

## ACTIVATION

### Use When

- "Build this page / screen / view"
- "Create this component"
- "Design the user flow for [feature]"
- "Improve the UX of [feature]"
- "Make this responsive"
- "Fix the accessibility of [component]"
- "Design this form / onboarding / dashboard / navigation"
- "Make this more intuitive"
- Any task that produces user-facing interface elements

### Do NOT Use When

- Building API endpoints with no UI → use `workflow-build-feature.md`
- Reviewing existing UI code → use `workflow-review-code.md`
- Optimizing UI performance → use `workflow-optimize-performance.md`
- Planning overall system architecture → use `workflow-plan-architecture.md`
- Debugging a broken system → use `workflow-debug-issue.md`

If the task includes both design and implementation, complete design steps first, then transition to Builder Mode.

---

## REQUIRED FILES

### Skills — Always Load

| Priority | Skill | Why |
| :--- | :--- | :--- |
| Primary | `skill-ui-ux` | Design thinking, state coverage, accessibility |
| Primary | `skill-coding` | Component implementation quality |
| Secondary | `skill-product-thinking` | User goal and friction framing |

### Skills — Load When Relevant

| Condition | Skill |
| :--- | :--- |
| Building a new module or page structure | `skill-architecture` |
| UI requires new API endpoints | `skill-api-design` |
| UI handles auth flows or sensitive data | `skill-security` |
| Responsiveness or rendering cost matters | `skill-performance` |
| Type B animations (scroll, parallax, 3D, video scrub) | `skill-cinematic-motion` |
| Type B micro-interactions (hover, state transitions) | `skill-advanced-frontend-execution` |
| Crafting the narrative for a brand surface | `skill-storytelling` |
| Writing marketing copy (headlines, CTAs, sections) | `skill-copywriting` |
| Researching competitors | `skill-competitor-profiling` |

### Contexts — Always Load

- `prototyping-spec.md`
- `PRODUCT.md`
- `DESIGN.md`
- `stack-context.md`
- `coding-standards.md`
- `architecture-context.md`
- `project-context.md`
- `business-priorities.md`
- `domain-rules.md`

### Contexts — Load When Relevant

| Condition | Context |
| :--- | :--- |
| UI enforces business rules | `domain-rules.md` |
| Auth or permission UI | `security-baselines.md` |
| Consuming API data | `api-conventions.md` |
| Project involves animation | `motion-direction.md` |
| Crafting narrative for brand surface | `story.md` |
| Research completed for brand/audience/competition | `research-brief.md` |

---

## REQUIRED INPUTS

At minimum, Anti-Gravity should have or establish before proceeding:

- the user goal
- the relevant screen, flow, or problem area
- who the user is
- what constraints matter
- whether the task is new design, redesign, UX improvement, component design, or UI critique

### If inputs are incomplete

Clarify the user goal before designing. Do NOT start designing components against an unclear user task.

---

## EXECUTION SEQUENCE

---

### STEP 1 — UNDERSTAND THE USER GOAL

**Mode:** Designer
**Goal:** Define what the user needs to accomplish — not what the screen looks like.

**Gate:** Do NOT start designing components until the user goal and flow are clear.

#### Actions (Step 1)

1. **Identify the user:**
   - Which user type is this for? Check `project-context.md` user types
   - What is their skill level and tolerance for complexity?
   - What device and context are they in — desktop focus session, mobile quick check, or something else?

1. **Identify the job:**
   - What is the user trying to accomplish?
   - Frame as Job-to-be-Done:
     > "When [situation], the user wants to [motivation] so that [outcome]"

   - What does the user have BEFORE this interaction?
   - What do they have AFTER?
   - Distinguish the feature request from the actual user need

1. **Identify the flow:**
   - What triggered the user to arrive at this screen?
   - What are the possible exits: success, cancel, error, navigation?
   - Is this a single interaction or a multi-step process?
   - Where does friction or confusion likely occur?
   - Where are the likely drop-off points?

1. **Identify constraints:**
   - What data is available to show?
   - What actions can this user take? Check role permissions
   - What are the responsive requirements? Check `DESIGN.md`
   - What are the accessibility requirements?
   - What platform or device assumptions matter?
   - Does this fit an existing screen pattern or is it more open?

#### Output (Step 1)

```text
User: [who]
Job: When [situation], they want to [motivation] so that [outcome]
Arrives from: [trigger]
Leaves via: [success path] or [alternative paths]
Constraints: [list]
Friction points: [where confusion likely occurs]
```

---

### STEP 2 — MAP ALL STATES

**Mode:** Designer
**Goal:** Identify every possible state the UI must handle BEFORE building anything.

**This is the most commonly skipped step and the number one cause of UI bugs in production.**

**Gate:** Do NOT start building until every state has a defined design approach.

#### State Map (Step 2)

For every view, screen, or component, define all of these:

| State | Questions to Answer | Design Decision |
| :--- | :--- | :--- |
| **Loading — initial** | What does the user see while data fetches for the first time? | Skeleton placeholder matching content shape, or full-page spinner? Check `DESIGN.md` loading patterns |
| **Loading — refresh** | What during background data refresh? | Show stale data with subtle indicator, or skeleton again? |
| **Empty — first use** | No data yet because user has not created any? | Illustration + friendly message + CTA to create first item |
| **Empty — filtered** | Filters or search return no results? | Lighter message + suggestion to adjust filters |
| **Success** | Normal, data-present state | The primary design |
| **Partial** | Some data present but incomplete? | Graceful fallbacks: initials for avatar, placeholder for missing description |
| **Error — field** | Form validation error? | Inline error below field, red border, aria-describedby |
| **Error — action** | Failed mutation: save failed, delete failed? | Toast notification with retry option |
| **Error — page** | Full page data fetch failure? | Error card with retry button replacing content area |
| **Permission denied** | User lacks access? | Message with redirect or limited view |
| **Destructive confirmation** | Before irreversible actions? | Modal with typed confirmation for high-severity, simple confirm for low |
| **Optimistic update** | Immediate UI change before server confirms? | Immediate visual change, revert on failure |
| **Disabled or pending** | Awaiting condition or permission? | Disabled state with clear visual treatment |

#### Output (Step 2)

A state map table listing every state with the design decision for each.

---

### STEP 3 — MAP THE FLOW AND INFORMATION PRIORITIES

**Mode:** Designer
**Goal:** Understand the full journey and clarify what each screen or state must communicate before touching component or layout decisions.

#### Flow Mapping Actions (Step 3)

- Outline the flow from start to finish
- Identify entry point, main steps, user decisions, system responses, and completion point
- Identify what the user must know at each step
- Identify what decision should be obvious next
- Identify where confusion could happen

#### Information Priority Actions (Step 3)

- Identify what must be visible immediately
- Identify the primary action — there should be one
- Identify secondary actions
- Define what information can be deferred or hidden
- Determine whether the screen is action-heavy, information-heavy, confirmation-heavy, or error-recovery-heavy

#### Output (Step 3)

```text
Flow outline: [steps and transitions]
Friction map: [where confusion likely occurs]
Information hierarchy: [what must be immediate vs deferred]
Action hierarchy: [primary, secondary, tertiary]
```

---

### STEP 4 — DESIGN THE LAYOUT AND COMPONENTS

**Mode:** Designer
**Goal:** Plan the component structure, visual hierarchy, and responsive behavior before writing any code.

#### Visual Hierarchy (Step 4)

- What is the PRIMARY action on this screen? Make it most prominent
- What is the SECONDARY information? Supporting, less prominent
- What is TERTIARY content? Metadata, least important
- Apply `DESIGN.md` typography scale: largest equals most important

#### Component Selection (Step 4)

- What components from `DESIGN.md` will be used?
- Are any new components needed? Prefer existing over new
- What variants and sizes are appropriate?
- Avoid inventing new patterns unless existing ones are insufficient

#### Layout Structure (Step 4)

- What is the page layout: single column, sidebar plus content, grid?
- How does it change at each responsive breakpoint?
- Reference `DESIGN.md` responsive breakpoints

#### Interaction Design (Step 4)

- What are the clickable and interactive elements?
- What feedback does each interaction provide: hover, active, loading?
- What keyboard shortcuts apply if any?
- Is tab order logical?

#### Information Density (Step 4)

- Is there too much on the screen creating cognitive load?
- Can anything be hidden behind progressive disclosure: accordion, show more, tabs?
- Is the most important information visible without scrolling?

#### Output (Step 4)

Component structure description covering which components, how they are arranged, responsive behavior, and interaction patterns.

#### Gate (Step 4)

If the primary action is not obvious, or hierarchy is weak, redesign before building. Visual neatness does not compensate for weak UX structure.

---

### STEP 5 — IMPLEMENT

**Mode:** Builder
**Goal:** Build the UI with full state coverage and accessibility.

Load `skill-coding` and follow its behavioral workflow.

#### 5a — Component Structure (Step 5)

1. Create component files following `architecture-context.md` placement rules
1. Define component props with TypeScript
1. Decide Server Component versus Client Component using `coding-standards.md` decision table
1. Set up data fetching via React Query hook or Server Component

#### 5b — Happy Path First (Step 5)

1. Build the success state — the primary, data-present view
1. Use design system components from `DESIGN.md`
1. Apply Tailwind classes following spacing, typography, and color tokens
1. Ensure correct responsive behavior at each breakpoint

#### 5c — All Other States — Do NOT Skip (Step 5)

1. **Loading state:** Implement skeleton or spinner per `DESIGN.md` patterns
1. **Empty — first use:** Implement with appropriate messaging and CTA
1. **Empty — filtered:** Implement with filter adjustment suggestion
1. **Error — action:** Implement toast or inline with retry
1. **Error — page:** Implement error card with retry button
1. **Partial state:** Implement graceful fallbacks for missing data
1. **Permission state:** Implement role-based visibility if applicable

#### 5d — Interaction States (Step 5)

1. Hover, focus, active states on all interactive elements
1. Loading and disabled states on buttons during async operations
1. Destructive action confirmation per `DESIGN.md` patterns
1. Optimistic updates where appropriate — revert on failure

#### 5e — Accessibility — Non-Negotiable (Step 5)

1. All interactive elements keyboard-accessible
1. Focus indicators visible — check `DESIGN.md` focus styles
1. All images have alt text — decorative images use `alt=""`
1. Form fields have associated labels — visible or screen-reader-only
1. Error messages connected via `aria-describedby`
1. Dynamic content changes announced via `aria-live`
1. Modal focus trap and Escape to close
1. Color contrast ratios met — 4.5:1 body text, 3:1 large text
1. `prefers-reduced-motion` respected

#### 5f — Responsive Behavior (Step 5)

1. Test at each breakpoint from `DESIGN.md`
1. Mobile touch targets minimum 44 by 44 pixels
1. Content reflows appropriately — no horizontal scrolling on mobile
1. Navigation adapts appropriately at small breakpoints

---

### STEP 6 — VERIFY

**Mode:** Reviewer
**Goal:** Confirm every state works correctly, responsively, and accessibly.

#### State Coverage Verification (Step 6)

- [ ] Loading state — initial — displays correctly
- [ ] Loading state — refresh — displays correctly
- [ ] Empty state — first use — displays correctly with CTA
- [ ] Empty state — filtered — displays correctly with suggestion
- [ ] Success state — displays correctly with real-looking data
- [ ] Partial state — handles missing fields gracefully
- [ ] Error state — field validation — displays correctly
- [ ] Error state — action failure — displays correctly
- [ ] Error state — page-level — displays correctly with retry
- [ ] Permission denied state — displays correctly

#### Responsive Verification (Step 6)

- [ ] Desktop layout correct
- [ ] Tablet layout correct
- [ ] Mobile layout correct
- [ ] No horizontal scrolling at any breakpoint
- [ ] Touch targets adequate on mobile

#### Accessibility Verification (Step 6)

- [ ] Full keyboard navigation works — Tab, Shift+Tab, Enter, Escape
- [ ] Focus indicators visible on all interactive elements
- [ ] Screen reader announces content correctly
- [ ] Color contrast passes — verified in browser DevTools
- [ ] Form labels associated with inputs
- [ ] Error messages connected to fields via aria-describedby
- [ ] Modal focus trap and Escape behavior correct

#### Interaction Verification (Step 6)

- [ ] Hover states work on all interactive elements
- [ ] Loading states show during async operations
- [ ] Destructive confirmations fire before destructive actions
- [ ] Optimistic updates show and revert correctly on failure
- [ ] No state results in a blank screen or raw error output

#### UX Quality Check (Step 6)

- Is the user goal obvious?
- Is the next action obvious?
- Is this too crowded?
- Are error and recovery paths clear?
- Could a first-time user succeed without explanation?
- Is visual neatness hiding real UX weakness?

---

### STEP 7 — CRITIQUE

**Mode:** Reviewer
**Goal:** Challenge whether the design is truly good, not just neat.

#### Ask (Step 7)

- Is this feature-first instead of user-goal-first?
- Is the hierarchy weak?
- Are states underdesigned?
- Is visual neatness hiding real UX weakness?
- Is the flow too complicated?
- Am I optimizing for visual tidiness or user success?
- Is anything hidden that users should not have to hunt for?
- Is there too much competing for attention?
- Are we over-designing without regard for implementation reality?

#### Output (Step 7)

Final UX quality check, caveats, and refinement suggestions if needed.

---

### STEP 8 — DELIVER

**Mode:** Communicator
**Goal:** Present the UI work clearly with context, rationale, and verification guidance.

#### Delivery Structure (Step 8)

```markdown

## What Was Built

[1-2 sentence summary of the UI feature]

## User Goal

[Job-to-be-Done statement]

## Flow Structure

[Sequence of steps, entry, exits, friction points addressed]

## States Implemented

- Loading: [approach]
- Empty (first use): [approach]
- Empty (filtered): [approach]
- Success: [approach]
- Partial: [approach]
- Error (field): [approach]
- Error (action): [approach]
- Error (page): [approach]
- Permission denied: [approach if applicable]

## Components Used

[List of design system components used]

## Responsive Behavior

[How the layout changes at each breakpoint]

## Accessibility

[Summary of accessibility measures implemented]

## Key Decisions

[Non-obvious design or implementation decisions and rationale]

## Tradeoffs and Constraints

[Where simplicity competed with flexibility, density with readability]

## What to Test

[How to manually verify each state]

## Next Steps

[Deferred scope, Phase 2 items, follow-up work]
```

---

## CHECKPOINTS AND QUALITY GATES

| Gate | Condition | Action |
| :--- | :--- | :--- |
| Gate 1 — User goal unclear | Cannot state what the user is trying to accomplish | Clarify before designing anything |
| Gate 2 — States not mapped | Any state left undefined before building | Complete state map before coding |
| Gate 3 — Hierarchy weak | Primary action not obvious | Redesign before building |
| Gate 4 — Design system ignored | New patterns invented where existing ones exist | Align with design system before continuing |
| Gate 5 — Accessibility skipped | Any accessibility checklist item unaddressed | Accessibility is non-negotiable — address before delivery |
| Gate 6 — Responsive untested | Layout not verified at all breakpoints | Test at all breakpoints before marking complete |

---

## QUALITY GATE CHECKLIST

Before marking UI work complete:

- [ ] User goal clearly defined before design began
- [ ] Job-to-be-Done statement written
- [ ] Flow mapped with entry, exits, and friction points identified
- [ ] ALL states mapped and designed — loading, empty, partial, success, error, permission, destructive
- [ ] Information and action hierarchy defined
- [ ] Design system components used consistently
- [ ] No new patterns invented where existing ones serve the need
- [ ] Happy path implemented correctly
- [ ] All non-happy states implemented — do not skip
- [ ] Interaction states complete — hover, focus, active, loading, disabled
- [ ] Responsive behavior verified at all breakpoints
- [ ] Touch targets adequate on mobile
- [ ] Accessibility requirements met — keyboard, screen reader, contrast, labels, aria attributes
- [ ] Form patterns follow `DESIGN.md` conventions
- [ ] Destructive actions have appropriate confirmation
- [ ] Error messages are user-friendly and actionable
- [ ] No state results in a blank screen or raw error
- [ ] Delivery summary written with states, decisions, and test steps

---

## WORKFLOW ANTI-PATTERNS

| Anti-Pattern | Why It Is Harmful | How This Workflow Prevents It |
| :--- | :--- | :--- |
| Component-First Design | Interface gets built for what is easy to build, not what helps the user succeed | Define the user goal and job before touching any component or layout decision |
| Happy-Path-Only UI | Loading, empty, and error states exist in production every day | Map all states at Step 2 before writing code |
| Visual Neatness Over UX Clarity | Users fail to accomplish their goal even though UI looks polished | Prioritize user task completion over visual tidiness |
| Ignoring Accessibility | A meaningful portion of users cannot use product effectively | Treat accessibility as non-negotiable at Step 5e |
| Feature-Centric Design | Cognitive load increases and most important action gets lost | Design around the user's next meaningful action |

---

## FAILURE MODES AND ESCALATION PATHS

| Failure Mode | What It Looks Like | Escalation |
| :--- | :--- | :--- |
| Missing API | Cannot build the UI without a contract | Switch to `workflow-design-api.md` first |
| Architecture Gap | Component placement or data flow unclear | Load `skill-architecture.md`, resolve before building |
| Auth Boundary | Access rules affect what is shown | Load `skill-security.md` and `security-baselines.md` |
| Design Gap | No existing component serves the need | Document gap, propose new pattern with justification |
| Product Mismatch | Confusion caused by unclear product decisions | Switch to product thinking before designing |

---

## FINAL RULE

Design the interface around the user's next meaningful action — not around everything the system could possibly show, and not around what is easiest to build.

---

## VERSION HISTORY

| Version | Date | Changes |
| :--- | :--- | :--- |
| Gold v1.1 | Initial | Established the systematic sequence for designing and implementing UI |
