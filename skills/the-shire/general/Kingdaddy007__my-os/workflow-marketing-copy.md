# WORKFLOW: MARKETING COPY & STRATEGY (FULL SOURCE)

**Version:** Gold v1.0
**Layer:** 8 — Execution Workflow
**Tier:** 2 — Loaded by task
**File:** workflows/workflow-marketing-copy.md
**Primary Mode:** Marketer / Copywriter
**Secondary Modes:** Product Thinking, Designer
**Purpose:** The systematic sequence for generating high-converting marketing copy, sales strategy, and competitor profiling. Ensures all copy is anchored in the target user's psychology and objections, not just clever words.
**Loaded When:** Writing landing pages, homepages, sales emails, competitor analysis, pricing pages, or any copy designed to persuade and convert.
**Inherits From:** execution-workflow.md (universal process)

---

## REQUIRED FILES

### Skills — Always Load

| Priority | Skill | Why |
| :--- | :--- | :--- |
| Primary | `skill-copywriting` | Core frameworks for headlines, CTAs, and page flow |
| Primary | `skill-marketing-psychology` | Cognitive biases, urgency, and persuasion triggers |
| Secondary | `skill-copy-editing` | Refining and polishing the draft |

### Skills — Load When Relevant

| Condition | Skill |
| :--- | :--- |
| Structuring the layout of a landing page | `skill-page-cro` |
| Researching the market | `skill-competitor-profiling` |
| Writing copy for sales teams | `skill-sales-enablement` |

### Contexts — Always Load

- `product-marketing-context.md` (Crucial for UVP and brand voice)
- `project-context.md` (For business goals)

### Contexts — Load When Relevant

| Condition | Context |
| :--- | :--- |
| Integrating with UI design | `PRODUCT.md` or `DESIGN.md` |

---

## REQUIRED INPUTS

Before writing a single word, establish:
- What type of page or asset is this?
- What is the ONE primary action the visitor must take?
- Do we have the `product-marketing-context.md` available? (If not, switch to Phase 1A of `workflow-project-inception.md` to define it first).

---

## EXECUTION SEQUENCE

### STEP 1 — ANCHOR IN THE CONTEXT
**Mode:** Marketer
**Goal:** Understand exactly who we are talking to and what we want them to do.

1. **Review Audience:** Who are they, and what problem are they actively trying to solve?
2. **Review UVP:** What makes this product undeniably better for this specific audience?
3. **Review Voice:** How should we sound?

**Gate:** Do NOT start writing until you know exactly what the Primary CTA is.

---

### STEP 2 — PSYCHOLOGY ALIGNMENT
**Mode:** Marketer
**Goal:** Determine which psychological levers will actually move this specific audience.

1. **Identify the Core Emotion:** Are they moving toward pleasure (gain) or away from pain (relief)?
2. **Select Persuasion Triggers:** 
   - Is Social Proof the biggest missing piece?
   - Is there authentic Urgency or Scarcity?
   - Do we need to apply Risk Reversal (guarantees)?
3. **Address Objections:** List the top 3 reasons they will hesitate, and plan where to dismantle them on the page.

---

### STEP 3 — DRAFTING THE CORE ASSETS
**Mode:** Marketer
**Goal:** Write the actual copy, starting with the most important elements first.

1. **The Hero Section (Above the Fold):**
   - Write 3-5 variations of the main Headline. 
   - Ensure the Headline focuses on the *transformation* or *benefit*, not the feature.
   - Write the Subheadline (clarifies the headline, adds specificity).
   - Write the Primary CTA button (Action verb + Value).
2. **The Argument (Below the Fold):**
   - Social Proof section (who else trusts us).
   - Problem Agitation section (showing we understand the pain).
   - Solution & Features (translated into benefits).
   - Objection Handling (FAQ or risk reversal).
   - Final CTA (recap value and ask again).

---

### STEP 4 — REFINEMENT & CRO
**Mode:** Reviewer (Copy Editor)
**Goal:** Tighten the copy and maximize conversion probability.

1. **Clarity Check:** Is there any industry jargon? Remove it.
2. **Brevity Check:** Cut adverbs. Shorten sentences. Make it punchy.
3. **CRO Check:** Are there too many competing CTAs? Is the layout supporting the reading flow? 
4. **Tone Check:** Does it sound like the defined Brand Voice?

---

### STEP 5 — DELIVER
**Mode:** Communicator
**Goal:** Present the copy clearly to the user with the underlying rationale.

Format the output clearly by page section. For key headlines or CTAs, always present 2-3 options with a brief explanation of the psychological angle behind each.

---

## QUALITY GATES

- [ ] Does the headline clearly state the benefit?
- [ ] Is the CTA an action word (not just "Submit")?
- [ ] Did we address the primary objection?
- [ ] Is the tone correct?
