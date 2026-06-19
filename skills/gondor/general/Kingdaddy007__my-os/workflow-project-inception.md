# WORKFLOW: PROJECT INCEPTION

**Version:** Gold v1.2
**Layer:** Execution workflow
**Tier:** 2 - loaded by task
**Purpose:** Turn a raw idea into a buildable plan, initialize runtime context, and set up local project memory before implementation begins.

---

## WHAT THIS WORKFLOW DOES

This workflow is the bridge between:

- "I have an idea"
- and
- "We have a scoped project, runtime context files, local memory, and a build sequence"

Its outputs are:

1. a clear problem definition
2. a target user and job-to-be-done
3. a scoped MVP with explicit non-goals
4. a technical direction
5. a sequenced build plan
6. runtime-ready context files in `contexts/`
7. initialized workspace memory files in `.agents/memory/`

---

## WHEN TO USE IT

Use this workflow when:

- starting a new product, tool, side project, or hackathon build
- turning a rough idea into a plan
- creating the first project context for a workspace

Do not use it when:

- adding a feature to an existing project
- debugging an existing system
- reviewing an already-planned build

---

## REQUIRED FILES

### Primary skills

- `skill-product-thinking`
- `skill-architecture`

### Conditional skills

- `skill-ui-ux` if the project has a real user interface
- `skill-database` if the project has persistence or a meaningful data model
- `skill-api-design` if the project exposes or consumes APIs

### Templates this workflow should use

- `global_templates/project-context-template.md`
- `global_templates/product-marketing-context-template.md`
- `global_templates/stack-context-template.md`
- `global_templates/coding-standards-template.md` when conventions are already clear
- `project-brief.md` when producing a formal project brief

### Runtime context files this workflow creates or initializes

- `contexts/project-context.md`
- `contexts/product-marketing-context.md`
- `contexts/stack-context.md`
- `contexts/architecture-context.md`
- `contexts/database-context.md` if relevant
- `contexts/app-flow.md` if the product has real user journeys
- `contexts/coding-standards.md` if project-specific conventions are known

### Workspace memory files this workflow initializes

- `.agents/memory/decisions-log.md`
- `.agents/memory/common-patterns.md`
- `.agents/memory/mistakes-to-avoid.md`
- `.agents/memory/postmortems.md`

> [!IMPORTANT]
> The files in `contexts/` are **runtime truth**, not authoring templates.
> Use templates to scaffold them, then save concise project truth into the runtime files.

---

## EXECUTION SEQUENCE

### PHASE 0: INITIALIZE WORKFLOW STATE

**Do this before anything else.** Create the session state file so the workflow
can be resumed if interrupted at any point.

1. Check if `.agents/workflow-state.json` already exists for this project.
2. If it exists and status is `in_progress`: ask "You have an active **project-inception** workflow at **Phase [N]** — [pct]% complete. Resume?"
3. If starting fresh or resuming, create/update `.agents/workflow-state.json`:

```json
{
  "workflow": "project-inception",
  "phase": 1,
  "started": "[timestamp]",
  "updated": "[timestamp]",
  "status": "in_progress",
  "last_completed": null,
  "children": []
}
```

4. **Scaffold Local Contexts Directory:** Ensure that a local `contexts/` directory exists inside the project workspace (`<workspace>/contexts/`). If it does not, create it and copy all template files from the global templates path (`{{GLOBAL_CONFIG_URI}}/contexts/*`) into the local `contexts/` folder. This is a mandatory gate to prevent the agent from accidentally writing project-specific facts to the global templates path.
5. Update the `phase` and `last_completed` fields at the start of each phase.
6. When invoking child workflows (teach, document, story, visual-brainstorm):
   add them to the `children` array with their own state path.
7. On resume: read state, find `last_completed`, continue from next step.

---

### PHASE 1: DISCOVER THE PROBLEM

Do not let the user skip this phase. The number one cause of failed projects is building a solution before understanding the problem.

#### Step 1: Discover Project Posture & Extract the Idea

First, ask the user to select the **Project Posture** to route the workflow:
1. **Product Mode:** Building a digital product, software tool, or SaaS application. (Standard linear flow: MVP -> Tech -> Design).
2. **Scenario A (Fresh Brand Website/Portfolio):** Building a brand website, landing page, or portfolio from scratch with no existing online presence or assets. (MVP and App Flow are deferred until after Phase 3A Research & Story are completed).
3. **Scenario B (Redesign/Upgrade):** Redeveloping or upgrading an existing website. (Standard flow but focused on conversion-driven restructuring).

Save this posture in the workflow state or context.

Next, ask the user to explain their idea in plain language. Listen for:

- What does it do?
- Who is it for?
- Why does it matter?
- What triggered this idea? (pain point, opportunity, competition requirement)

#### Step 2: Define the problem

Restate the idea as a problem statement:

```
[Target user] struggles with [specific problem] because [root cause].
Currently they [current workaround], which is [why it's inadequate].
```

#### Step 3: Define the user

Create a brief user profile:

```
PRIMARY USER: [Who]
CONTEXT: [When/where they encounter the problem]
CURRENT BEHAVIOR: [What they do today]
DESIRED OUTCOME: [What they wish they could do]
TECHNICAL COMFORT: [Low / Medium / High]
```

#### Step 4: Define the job-to-be-done

```
When [situation], [user] wants to [motivation] so that they can [outcome].
```

#### Step 5: Define success

```
This project succeeds when [measurable outcome].
MVP is "done" when [specific criteria].
```

#### Phase 1 output

- problem statement
- user profile
- JTBD
- success definition

Gate:

- do not continue until the problem statement feels accurate and the user agrees it captures the real problem

---

### PHASE 1A: MARKET POSITIONING

Use when:
- the product will be marketed or sold to users
- the product has a landing page, marketing site, or direct sales motion

#### Step 1: Clarify the Objections
- Why would the user say "no"?
- What are they currently paying for that this replaces?

#### Step 2: Define the Unique Value Proposition
- What is the ONE specific reason they should choose this over alternatives?

#### Step 3: Establish Brand Voice Hypothesis (Preliminary)
- How should the product sound initially? (Professional? Irreverent? Direct? Academic?)
- > [!IMPORTANT]
  > This is a preliminary brand voice hypothesis to guide early planning. The authoritative brand voice, tone, and strategic emotional goals are locked later during the creation of `story.md` in Phase 3A, after full audience and competitor research.

Output:
- `contexts/product-marketing-context.md` as the live runtime truth for marketing context

Authoring rule:
- use scaffolding if needed, but save `product-marketing-context.md` as a live context file

Gate:
- before designing MVP, confirm the unique value proposition is actually compelling to the target user

---

### PHASE 2: DEFINE THE MVP

> [!IMPORTANT]
> **Scenario A (Fresh Brand Website) Deferral Gate:** If the Project Posture is set to **Scenario A (Fresh Brand Website/Portfolio)**, defer this phase entirely. You cannot brainstorm or categorize page blocks or features before understanding the brand's unique strategy and research. This phase must be executed *after* Phase 3A (DESIGN IDENTITY & VISUAL SYSTEM) is completed and `contexts/story.md` is locked.

#### Step 1: Brainstorm features

List everything the product could do. Do not filter yet. Generate 10-20 capabilities.

#### Step 2: Categorize and prioritize

Sort every feature into:

| Category | Rule | Features |
| :--- | :--- | :--- |
| **🔴 Core (Must Have)** | Without this, the product does not solve the problem | [list] |
| **🟡 Important (Should Have)** | Makes the product significantly better but not essential for v1 | [list] |
| **🟢 Nice-to-Have (Could Have)** | Would be great but can wait for v2 | [list] |
| **⚫ Out of Scope (Won't Have)** | Deliberately excluded | [list] |

#### Step 3: Define the MVP

The MVP is ONLY the 🔴 Core features. Nothing else.

Ask the "20% question": "If we could only build 20% of this, which 20% delivers the core value?" That is the MVP.

```
MVP SCOPE:

- [Core feature 1]
- [Core feature 2]
- [Core feature 3]

EXPLICITLY NOT IN MVP:

- [Everything else — listed to prevent scope creep]

```

#### Step 4: Define what "shipped" looks like

```
VERSION 1 IS DONE WHEN:

- [ ] [Core feature 1] works end to end
- [ ] [Core feature 2] works end to end
- [ ] [Core feature 3] works end to end
- [ ] User can [complete the primary job] without assistance
- [ ] Deployed to [target environment]

```

#### Phase 2 output

- prioritized feature list
- MVP scope
- explicit non-goals
- definition of done

Gate:

- do not proceed with an unbounded feature list
- user confirms: "Yes, this MVP scope is what I want to build first."

---

### PHASE 2A: MAP THE APP FLOW

> [!IMPORTANT]
> **Landing Page / Single-Page Experience Deferral Gate:** If the project is a single-page landing page, portfolio, or brand website (Scenario A or B), defer this phase. A single-page experience does not have standard app routes or settings panels. Instead, the scroll narrative and section sequence defined in `contexts/story.md` (Phase 3A) will serve as the app flow.

Use when:

- the product has users, screens, states, routes, or task flows

Skip only if the product has no user journeys (e.g., a pure background script).

#### Step 1: Define the primary user journeys

For each main user type, map their "golden path" — the main thing they do. List every step from entry point to job completion.

#### Step 2: Define secondary and error flows

- Map secondary tasks (profile management, settings, etc.)
- Define how global errors (network failure, auth expiry) are handled
- Define flow-specific error recoveries

#### Step 3: Map navigation and transitions

- Define the global navigation
- Ensure every transition between screens is explicit (including loading states and redirects)

Output:

- `contexts/app-flow.md` as the live runtime truth for user flows

Authoring rule:

- use scaffolding if needed, but save `app-flow.md` as a live context file, not as a template exercise

Gate:

- before designing architecture or visual UI, confirm the user journey makes sense — are there dead ends? Are error states handled?

---

### PHASE 2B: PROTOTYPING & RESEARCH (THE DESIGN LOOP)

Use when:
- the product has a user interface and needs a competitive baseline.

#### Step 1: Competitive Teardown
- Select 3-5 competitor or reference websites.
- Extract the "Structure without Style". Use Anti-Gravity's browser tools or external tools (Perplexity/Tango).
- Identify: Jobs-to-be-Done on each page, specific section blocks (Hero, Features, Pricing), and key interactions (scroll effects, components).

#### Step 2: The Prototyping Spec
- Synthesize the research into a structural blueprint.
- List the required sections, the data they display, and their priority.

Output:
- `contexts/prototyping-spec.md` as the live runtime truth for structural wireframing.

Gate:
- Do not proceed to visual identity or coding until the structural layout and section blocks are defined.

---

### PHASE 3: DEFINE THE TECHNICAL DIRECTION

#### Step 1: Choose the tech stack

Based on the user's existing skills, project requirements, timeline constraints, and deployment target.

```
TECH STACK:

- Frontend: [framework]
- Backend: [framework/approach]
- Database: [engine]
- Auth: [approach]
- Hosting: [provider]
- Deployment: [approach]

```

#### Step 2: Design the data model

- What entities exist?
- What are the relationships?

```
ENTITIES:

- [Entity 1]: [key fields]
- [Entity 2]: [key fields]
- [Entity 3]: [key fields]

RELATIONSHIPS:

- [Entity 1] has many [Entity 2]
- [Entity 2] belongs to [Entity 1]

```

#### Step 3: Define the API shape (if applicable)

- What endpoints are needed?
- What are the primary CRUD operations?

#### Step 4: Define the folder structure

Based on the stack and patterns:

```
project/
├── [folder structure]
```

#### Step 5: Identify the riskiest technical decision

- What is the one technical choice that, if wrong, would cost the most to fix?
- How can we validate it early?

#### Phase 3 output

- stack decision
- data model
- API shape
- folder structure
- riskiest technical decision and validation plan

Gate:

- if the stack or architecture choice is still highly unstable, name the uncertainty explicitly before moving on

---

### PHASE 3A: DESIGN IDENTITY & VISUAL SYSTEM

This phase is **mandatory** for any product with a user interface. Impeccable is the design authority — all visual identity work goes through its workflows.

> [!IMPORTANT]
> **Impeccable owns this phase.** Do not manually define colors, typography, or spacing in text. Use the Impeccable workflows below to create structured, machine-readable design context that all subsequent build work draws from.

> [!CAUTION]
> **CRITICAL SEQUENCE:** Research → Story → DESIGN.md. The visual system cannot serve the story if it is created before the story exists. Do NOT reorder these steps.

#### Step 1: Run `/impeccable-teach` → PRODUCT.md

This creates the **strategic design context** at the project root:

- **Register** — Is this a brand surface (design IS the product) or a product surface (design SERVES the product)?
- **Users & Purpose** — Who uses this, what's the job-to-be-done, what emotions should the UI evoke?
- **Brand Personality** — 3-word personality, tone, voice
- **Anti-references** — What this should explicitly NOT look like
- **Design Principles** — 3-5 strategic principles derived from the conversation
- **Accessibility & Inclusion** — WCAG level, known user needs

The `teach` workflow interviews the user, scans the codebase for existing signals, and writes `PRODUCT.md`.

#### Step 2: Competitor Profiling

Use `skill-competitor-profiling` for structured competitor analysis:
- Select 3-5 competitors or reference products
- Run the competitor-profiling skill to generate `competitor-profiles/_summary.md`
- Identify: what others are doing, the gap, the opportunity

**Output:** `competitor-profiles/_summary.md`

#### Step 3: Research & Story

Before defining any visual system, define the STORY. The story drives everything —
copy, visuals, layout, animation, typography.

**3a. Research (skill-storytelling Section 1)**

Gather information about the brand, audience, competition, and context:
- Research the brand (who, what, why, how, personality, anti-references)
- Research the audience (needs, wants, objections, language, proof points)
- Research the competition (reference `competitor-profiles/_summary.md` for structured analysis)
- Research the existing materials (current website, brand assets, messaging)

**Output:** `contexts/research-brief.md`

**3b. Story (skill-storytelling Sections 2-6)**

Synthesize research into a narrative:
- Choose narrative arc (Brand Story, Product Journey, Portfolio Story, etc.)
- Map emotional journey (Hook → Build → Climax → Resolve emotions)
- Define copy direction (headline strategy, tone, key messages, CTA strategy)
- Define visual direction (hero visual, image style, color mood, typography voice)
- Define motion direction (hero animation, scroll behavior, climax pattern)
- Present 2-3 story directions to user
- User picks one or blends elements

**Output:** `contexts/story.md`

This is the master document that drives all subsequent decisions. Every other
context file (DESIGN.md, motion-direction.md, the actual copy) derives from this.

#### Step 4: Run `/impeccable-document` → DESIGN.md + DESIGN.json

This creates the **visual design system** at the project root — now informed by story.md:

- DESIGN.md — YAML frontmatter with machine-readable tokens (colors, typography, spacing, rounded, components) + markdown body with 8 sections (Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts). Follows the Google Stitch DESIGN.md format.
- DESIGN.json — Sidecar with extensions (tonal ramps, shadows, motion tokens, component HTML/CSS snippets, narrative).

The `document` workflow has two modes:
- **Scan mode** (default): Extracts real tokens from existing code
- **Seed mode** (new projects): Checks if `contexts/story.md` is present in the workspace. If it is, automatically extracts the design parameters (colors, typography, motion, references, anti-references) from the story to seed the visual tokens, avoiding redundant user questions. If `contexts/story.md` is missing, interviews the user for the 5 design answers, then creates a minimal scaffold marked `<!-- SEED -->`.

> [!IMPORTANT]
> DESIGN.md is created AFTER story.md exists. The visual tokens should serve the narrative direction, not contradict it. If story.md demands an organic "drenched" color strategy, DESIGN.md should reflect that — not generic hex values chosen by instinct.

#### Step 5: Visual Brainstorm (incl. Phase 3C Motion Exploration)

Run `workflow-visual-brainstorm.md` to explore visual directions informed by story.md:
- Present 2-3 visual directions
- User picks direction
- **Phase 3C (motion exploration):** Present 2-3 motion directions, map patterns to scroll sections, generate image briefs for Figma
- Lock visual direction → Write design tokens and creative details directly to `DESIGN.md` and `DESIGN.json`.
- Write `contexts/motion-direction.md` (single source of truth for motion direction)

**Output:** `DESIGN.md` / `DESIGN.json` + `contexts/motion-direction.md`

> [!IMPORTANT]
> `motion-direction.md` is created ONLY here — not duplicated from any other workflow. Visual Brainstorm Phase 3C is the single authority for motion direction creation.

#### Step 6: External Prototyping (Mockup)

- Bring the `DESIGN.md` tokens and `prototyping-spec.md` structure into Figma AI, Lovable, or Google Stitch.
- Generate page mockups to SEE the structure and vibe before coding.
- Extract any final adjustments back into DESIGN.md.

Output:

- `PRODUCT.md` at project root (strategic design context)
- `DESIGN.md` + `DESIGN.json` at project root (visual system and tokens)
- `contexts/motion-direction.md` — motion vocabulary, scroll narrative, asset requirements (created by Visual Brainstorm Phase 3C)

Gate:

- before moving to architecture, confirm the visual direction feels right for the target user and business context. A trading tool should not look like a social app. A luxury marketplace should not look like a SaaS dashboard.
- verify that `contexts/research-brief.md` exists if Phase 3A applied (research completed for brand, audience, competition)
- verify that `contexts/story.md` exists if Phase 3A applied (narrative arc, emotional journey, copy/visual/motion direction defined)
- verify that `contexts/motion-direction.md` exists if Phase 3A applied (created by visual brainstorm Phase 3C — emotion diagnosis, archetype, motion vocabulary, scroll narrative, asset requirements)

---

### PHASE 4: CREATE RUNTIME CONTEXTS

Goal:

- turn the planning work into runtime-ready context files
- make sure the next workflow has real project truth to work from

Required writes:

- create `contexts/project-context.md` using `global_templates/project-context-template.md` as scaffolding
- create `contexts/product-marketing-context.md` using `global_templates/product-marketing-context-template.md` if Phase 1A applied
- create `contexts/business-priorities.md` to establish tradeoffs before building (speed vs quality, budget vs scale)
- create `contexts/stack-context.md` using `global_templates/stack-context-template.md` as scaffolding
- create `contexts/architecture-context.md`
- create `contexts/database-context.md` if relevant
- initialize `contexts/coding-standards.md` if concrete conventions are already known, using `global_templates/coding-standards-template.md`
- verify that `contexts/app-flow.md` exists if Phase 2A applied
- verify that `contexts/prototyping-spec.md` exists if Phase 2B applied
- verify that `PRODUCT.md` exists at project root if Phase 3A applied (created by `/impeccable-teach`)
- verify that `DESIGN.md` + `DESIGN.json` exist at project root if Phase 3A applied (created by `/impeccable-document`)
- verify that `contexts/motion-direction.md` exists if Phase 3A applied (created by visual brainstorm Phase 3C — emotion diagnosis, archetype, vocabulary, scroll narrative, asset requirements)

Context-writing rule:

- runtime contexts should be concise, factual, and updateable
- longer fill guidance belongs in `global_templates/`
- PRODUCT.md and DESIGN.md are design truth — reference them directly in other files, do not duplicate them.

---

### PHASE 5: INITIALIZE WORKSPACE MEMORY

Goal:

- prevent project knowledge from leaking into global memory
- create a local continuity layer before implementation begins

Required writes:

- update `.agents/workflow-state.json` (already created in Phase 0) — set phase to 5, update `last_completed`
- create `.agents/memory/decisions-log.md`
- create `.agents/memory/common-patterns.md`
- create `.agents/memory/mistakes-to-avoid.md`
- create `.agents/memory/postmortems.md`

> [!CAUTION]
> Failure to create these files will lead to global memory contamination. Project-specific lessons MUST go local first. Global memory is reserved for cross-project or Anti-Gravity-level lessons.

First entry:

- log the initial stack and architecture choice in local `decisions-log.md`

---

### PHASE 6: CREATE THE BUILD SEQUENCE

Goal:

- turn the MVP into a practical implementation order
- expose dependencies and critical path
- make the first execution workflow obvious

#### Universal build order

For most web applications, the build order is:

```
STEP 1: PROJECT SETUP (Foundation)
├── Initialize project with chosen stack
├── Set up folder structure
├── Configure dev environment (database, env vars)
├── Set up linting, formatting, git
└── Verify: project runs locally with blank page

STEP 2: DATABASE + DATA MODEL (Skeleton)
├── Define schema (Prisma, SQL, etc.)
├── Create migrations
├── Seed with test data
└── Verify: can read/write data from CLI/script

STEP 3: AUTHENTICATION (Security Foundation)
├── Implement auth (login, register, session)
├── Protect routes
├── Set up basic role model (if needed)
└── Verify: can log in, protected pages redirect

STEP 4: CORE FEATURE 1 — Backend (Most Important Feature)
├── API endpoints or Server Actions
├── Database queries
├── Input validation
├── Error handling
└── Verify: feature works via API/action (no UI yet)

STEP 5: CORE FEATURE 1 — Frontend
├── For all UI/UX work, use `/impeccable-craft` (shape → mock → build → verify loop)
├── Pages and components
├── Data fetching
├── All states: loading, empty, error, success
├── Forms and interactions
└── Verify: feature works end-to-end in browser

STEP 6: CORE FEATURE 2 — Full Stack
├── Backend (API + DB)
├── Frontend (pages + components)
├── All states
└── Verify: works end-to-end

STEP 7: CORE FEATURE 3 — Full Stack
├── [Same pattern]
└── Verify: works end-to-end

STEP 8: INTEGRATION + POLISH
├── Connect features together
├── Navigation and routing
├── Error handling across all flows
├── Responsive design check
├── Basic accessibility check
└── Verify: user can complete the full primary job

STEP 9: TESTING + HARDENING
├── Test critical paths
├── Fix edge cases discovered during testing
├── Security review (auth, input validation)
├── Performance check (any obvious bottlenecks?)
└── Verify: no broken flows, no obvious security holes

STEP 10: DEPLOY
├── Set up hosting
├── Configure environment variables
├── Deploy
├── Smoke test on production
└── Verify: live and working
```

Output:

- sequenced implementation plan
- optional day-by-day version for hackathons or time-boxed builds

---

### PHASE 7: PACKAGE THE NORTH STAR

Goal:

- capture the result in a form that is reusable by later workflows

Outputs:

- concise project brief
- MVP scope
- build sequence
- initialized runtime contexts
- initialized local memory

Optional:

- load `project-brief.md` if a formal brief is useful
- apply the project planning rubric during critique if the project is high-stakes or especially fuzzy

#### Execution handoff

Hand off to the engineering workflows:

1. Start Step 1 from the build sequence
2. Use `workflow-build-feature.md` for each feature
3. Use the relevant skill files for each step
4. Commit after each completed step
5. Check off items in the Definition of Done as they are completed
6. When 80% done: shift to finishing mode — resist scope creep, push to ship

---

## QUALITY GATES

Before calling project inception complete, verify:

- [ ] Problem clearly defined (user confirmed)
- [ ] Target user identified
- [ ] Unique value proposition and brand voice established — `product-marketing-context.md` created (if applicable)
- [ ] Features brainstormed and prioritized (Core / Important / Nice-to-Have / Out of Scope)
- [ ] MVP scope is ONLY Core features
- [ ] Definition of done is specific and checkable
- [ ] App flow mapped (user journeys, error states, transitions) — `app-flow.md` created
- [ ] Design identity established via Impeccable — `PRODUCT.md` created (if UI project)
- [ ] Visual system documented — `DESIGN.md` + `DESIGN.json` created (if UI project)
- [ ] Motion direction established — `contexts/motion-direction.md` created (emotion, archetype, vocabulary, scroll narrative, assets)
- [ ] Animation types mapped per section (Type A/B/C) with specific patterns noted
- [ ] Tech stack chosen
- [ ] Data model designed
- [ ] Build sequence numbered and ordered
- [ ] Time mapped (if deadline exists)
- [ ] Risk identified
- [ ] Context files created or updated
- [ ] Workspace memory initialized
- [ ] Project brief document compiled
- [ ] The next execution workflow is obvious

---

## RECOVERY RULES

- If the idea keeps growing, return to MVP scope and re-lock the non-goals.
- If the stack is too uncertain, document assumptions and the validation plan instead of pretending certainty.
- If context files become essays, move the scaffolding back into `global_templates/` and keep the runtime files factual.
- If project-specific knowledge starts heading toward global memory, stop and reroute it to workspace memory.

---

## FINAL RULE

This workflow does not just plan the project. It creates the runtime truth and local memory the rest of Anti-Gravity depends on.
