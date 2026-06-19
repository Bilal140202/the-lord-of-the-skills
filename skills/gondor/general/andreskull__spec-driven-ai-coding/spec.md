# Spec Generation Workflow

## ⚠️⚠️⚠️ CRITICAL ENFORCEMENT - READ BEFORE EXECUTING ⚠️⚠️⚠️

**THIS WORKFLOW HAS STRICT FILE CREATION LIMITS:**

**✅ ALLOWED FILES (ONLY 2):**
1. `docs/features/feature-name/requirements.md`
2. `docs/features/feature-name/README.md`

**❌ FORBIDDEN FILES (DO NOT CREATE):**
- `tasks.md` ← **ABSOLUTELY FORBIDDEN**
- `design.md` ← **ABSOLUTELY FORBIDDEN**
- `spec.md` ← **ABSOLUTELY FORBIDDEN**
- Any other files ← **ABSOLUTELY FORBIDDEN**

**BEFORE CREATING ANY FILE, ASK YOURSELF:**
- "Is this file `requirements.md` or `README.md`?"
- If NO → **DO NOT CREATE IT**
- If YES → Proceed only if user confirmed

**IF YOU CREATE `tasks.md` OR `design.md`, YOU HAVE FAILED THIS WORKFLOW.**

---

Generate a feature specification using Chain-of-Thought reasoning. This workflow creates ONLY the requirements document after confirming understanding with the user.

## 🚨🚨🚨 READ THIS FIRST - ABSOLUTE REQUIREMENT 🚨🚨🚨

**BEFORE CREATING ANY FILES, YOU MUST:**

1. ✅ Understand the request
2. ✅ Research the codebase  
3. ✅ **PRESENT A PREVIEW** using the format below
4. ✅ **ASK: "Does this match your intent? Should I proceed with creating requirements.md?"**
5. ✅ **STOP AND WAIT FOR USER RESPONSE**
6. ✅ **ONLY CREATE FILES AFTER USER EXPLICITLY CONFIRMS** (e.g., "yes", "proceed", "looks good")

**⛔ YOU ARE ABSOLUTELY FORBIDDEN FROM:**
- Creating `requirements.md` immediately after identifying the feature
- Using `write` or `search_replace` tools before showing preview
- Proceeding to file creation without user confirmation
- Assuming user approval - you MUST wait for explicit confirmation
- **Creating `design.md` or `tasks.md` (these are created by `/plan` workflow, NOT `/spec`)**
- **Creating any files other than `requirements.md` and `README.md`**

**IF YOU CREATE `requirements.md` WITHOUT FOLLOWING STEPS 1-5 ABOVE, YOU HAVE VIOLATED THIS WORKFLOW.**
**IF YOU CREATE `design.md` OR `tasks.md`, YOU HAVE VIOLATED THIS WORKFLOW.**

---

## Phased Workflow

**This workflow ONLY creates `requirements.md` and `README.md` after user confirmation. Do NOT proceed to design or tasks.**

**🚨 CRITICAL: ALLOWED FILES ONLY**
- ✅ `docs/features/feature-name/requirements.md`
- ✅ `docs/features/feature-name/README.md`
- ❌ **NOTHING ELSE - NO OTHER FILES**

The workflow is:
1. **`/spec`** → Understands request → Shows preview → **Asks for confirmation** → **WAITS** → Creates `requirements.md` + `README.md` → **STOPS for review**
2. User reviews and approves requirements
3. **`/plan`** → Creates `design.md` → **STOPS for review** (separate workflow, NOT `/spec`)
4. User reviews and approves design
5. **`/plan`** (run again) → Creates `tasks.md` → **STOPS for review** (separate workflow, NOT `/spec`)

**The `/spec` workflow does NOT create design.md or tasks.md. Those are created by the `/plan` workflow in separate runs.**

## Process

### Step 1: Understand and Analyze

Use XML blocks to structure your thinking:

```xml
<thinking>
[Your reasoning process - analyze the request, identify key requirements, consider constraints]
- What feature is being requested?
- What are the key requirements?
- Are there any ambiguities that need clarification?
- What context is needed from the codebase?
</thinking>
```

### Step 2: Research and Gather Context

**CRITICAL: Before proceeding, you MUST read the requirements format rule:**

1. **Read `@.agent/rules/global/requirements-format.md`** - This defines the exact format for requirements.md
2. Understand the structure: User Stories, Functional Requirements, Acceptance Criteria
3. **Note what NOT to include:**
   - ❌ Database schemas (belongs in `design.md`)
   - ❌ API endpoint details (belongs in `design.md`)
   - ❌ Technical implementation details (belongs in `design.md`)
   - ❌ Architecture diagrams (belongs in `design.md`)
   - ❌ Code or pseudocode (belongs in `tasks.md`)
4. **Requirements.md focuses on WHAT (user-facing), not HOW (technical)**

Then:
- Read relevant documentation files
- Search codebase for related implementations
- Identify dependencies and constraints
- Check existing feature specifications

### Step 3: Create Preview (DO NOT CREATE FILE YET)

**🚨🚨🚨 CRITICAL: YOU MUST STOP HERE AND SHOW A PREVIEW. DO NOT CREATE ANY FILES YET. 🚨🚨🚨**

**⛔ YOU ARE FORBIDDEN FROM CREATING `requirements.md` AT THIS STAGE. ⛔**

**⛔ YOU ARE FORBIDDEN FROM USING THE `write` OR `search_replace` TOOLS TO CREATE FILES YET. ⛔**

**YOU MUST PRESENT THE PREVIEW BELOW AND WAIT FOR USER CONFIRMATION BEFORE CREATING ANY FILES.**

Present a summary in this EXACT format (copy this format exactly):

```
## 📋 Preview: Requirements Specification

### Feature Identified
[Feature Name]

### What I Understood
[Brief description of what you understood from the request]

### Key Requirements I Plan to Document
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

### Questions/Clarifications Needed
- [Any ambiguities or questions]

### Proposed Structure
- User stories: [count]
- Acceptance criteria: [count]
- Technical constraints: [if any]

---

**❓ Does this match your intent? Should I proceed with creating requirements.md?**

**Reply with "yes" or "proceed" to continue, or provide feedback to adjust.**
```

### Step 4: Wait for User Confirmation

**🚨 STOP HERE. DO NOT CREATE ANY FILES UNTIL THE USER CONFIRMS.**

**YOU MUST WAIT FOR THE USER TO RESPOND BEFORE CREATING `requirements.md`.**

**DO NOT PROCEED TO STEP 5 UNTIL USER EXPLICITLY CONFIRMS.**

Wait for the user to:
- Confirm understanding is correct (e.g., "yes", "proceed", "looks good")
- Request changes or clarifications
- Approve proceeding with requirements.md creation

**IF YOU CREATE `requirements.md` WITHOUT USER CONFIRMATION, YOU HAVE VIOLATED THIS WORKFLOW.**

### Step 5: Create Requirements (Only After Explicit Confirmation)

**ONLY proceed to this step if the user has explicitly confirmed (e.g., "yes", "proceed", "looks good").**

**DO NOT proceed if the user hasn't responded yet.**

**🚨🚨🚨 BEFORE CREATING ANY FILES - MANDATORY VERIFICATION 🚨🚨🚨**

**STOP. Read this checklist. Answer each question:**

1. ❓ "What files am I about to create?"
   - ✅ Answer: "requirements.md and README.md ONLY"
   - ❌ If you answer includes "tasks.md" or "design.md" → **STOP. DO NOT CREATE.**

2. ❓ "Am I creating tasks.md?"
   - ✅ Answer: "NO"
   - ❌ If you answer "YES" → **STOP. DO NOT CREATE tasks.md.**

3. ❓ "Am I creating design.md?"
   - ✅ Answer: "NO"
   - ❌ If you answer "YES" → **STOP. DO NOT CREATE design.md.**

4. ❓ "How many files will I create?"
   - ✅ Answer: "2 files: requirements.md and README.md"
   - ❌ If you answer more than 2 → **STOP. REVIEW YOUR PLAN.**

**Only proceed if ALL answers are correct. If ANY answer is wrong, STOP and review this workflow.**

**🚨 BEFORE CREATING FILES - VERIFY THIS CHECKLIST:**

✅ I will create ONLY these 2 files:
- `docs/features/feature-name/requirements.md`
- `docs/features/feature-name/README.md`

❌ I will NOT create:
- `design.md` (created by `/plan` workflow)
- `tasks.md` (created by `/plan` workflow)
- `spec.md` (wrong filename)
- Any other files

**If you plan to create ANY file other than requirements.md or README.md, STOP and review this workflow.**

Create `docs/features/feature-name/` directory with:

```xml
<requirements>
[Clear, specific requirements - what needs to be built, user stories, acceptance criteria]
</requirements>
```

**CRITICAL FILE STRUCTURE:**
- Create directory: `docs/features/feature-name/` (where feature-name is kebab-case of the feature)
- Create file: `docs/features/feature-name/requirements.md` (NOT `spec.md`, NOT in root)
- Create file: `docs/features/feature-name/README.md`

1. **`docs/features/feature-name/requirements.md`** - The "What": User stories & acceptance criteria
   - **MUST follow the format defined in `@.agent/rules/global/requirements-format.md`**
   - Extract from `<requirements>` XML block
   - **Structure REQUIRED:**
     - Overview (business context)
     - User Stories (As a... I want... so that...)
     - Functional Requirements (WHAT, not HOW)
     - Acceptance Criteria (Given/When/Then format)
     - Non-Functional Requirements (performance, security)
   - **DO NOT include:** Database schemas, API endpoints, technical implementation details
   - **File MUST be named `requirements.md` and located in `docs/features/feature-name/`**

2. **`docs/features/feature-name/README.md`** - Feature overview & operation
   - Brief description, overview, how to use
   - **File MUST be named `README.md` and located in `docs/features/feature-name/`**

**⛔ ABSOLUTELY FORBIDDEN - DO NOT CREATE:**
- `spec.md` (wrong filename)
- Files in root directory (wrong location)
- `design.md` (created later by `/plan` workflow, NOT by `/spec`)
- `tasks.md` (created later by `/plan` workflow, NOT by `/spec`)
- Any implementation plan files
- Any design documents
- Any task lists

**✅ ONLY ALLOWED FILES:**
- `docs/features/feature-name/requirements.md`
- `docs/features/feature-name/README.md`

**IF YOU CREATE ANY FILE OTHER THAN `requirements.md` OR `README.md`, YOU HAVE VIOLATED THIS WORKFLOW.**

## Final Verification After File Creation

**After creating files, STOP and verify:**

✅ **I created ONLY these 2 files:**
- `docs/features/feature-name/requirements.md`
- `docs/features/feature-name/README.md`

❌ **I did NOT create:**
- `design.md` (created by `/plan` workflow, NOT `/spec`)
- `tasks.md` (created by `/plan` workflow, NOT `/spec`)
- `spec.md` (wrong filename)
- Any other files

**If you created ANY file other than requirements.md or README.md, you have violated this workflow. STOP and report the error.**

**🚨🚨🚨 CRITICAL: YOU MUST STOP HERE 🚨🚨🚨**

**Inform the user:**
"I have created `requirements.md` and `README.md` in `docs/features/feature-name/`. Please review them. The design and tasks will be created separately using the `/plan` workflow after you approve the requirements."

**DO NOT create any additional files. DO NOT proceed to design or task creation.**

**⛔ ABSOLUTELY FORBIDDEN:**
- Creating `design.md` (created later by `/plan`)
- Creating `tasks.md` (created later by `/plan`)
- Creating any files other than `requirements.md` and `README.md`

**✅ ONLY CREATE:**
- `docs/features/feature-name/requirements.md`
- `docs/features/feature-name/README.md`

**STOP HERE. Do NOT create design.md or tasks.md.**

## Subagent Tags

You can delegate specific aspects to specialized subagents:

- `[Subagent:Research]` - For codebase research and pattern discovery

## 🚨 CRITICAL RULES - READ CAREFULLY

### BEFORE creating any files - MANDATORY STEPS:

1. ✅ Understand the request completely
2. ✅ Research the codebase and gather context
3. ✅ **SHOW A PREVIEW** of what you plan to create (use the format in Step 3)
4. ✅ **EXPLICITLY ASK**: "Does this match your intent? Should I proceed with creating requirements.md?"
5. ✅ **WAIT FOR USER RESPONSE** - Do NOT create files until user confirms

### ⛔ FORBIDDEN ACTIONS:

- ❌ **DO NOT create `requirements.md` immediately after identifying the feature**
- ❌ **DO NOT create files without showing preview first**
- ❌ **DO NOT proceed to file creation without user confirmation**
- ❌ **DO NOT assume user approval - you MUST wait for explicit confirmation**

### ✅ AFTER user explicitly confirms (e.g., "yes", "proceed"):

- Create `docs/features/feature-name/` directory
- Create `requirements.md` and `README.md`
- **STOP and wait for user review**

### Additional Rules:

- **ONLY create `requirements.md` and `README.md`**
- **⛔ ABSOLUTELY FORBIDDEN: Creating `design.md` or `tasks.md`**
- **⛔ ABSOLUTELY FORBIDDEN: Creating any implementation plan files**
- **STOP and wait for user review after creating requirements.md**
- Do NOT create Cursor's native `.plan.md` files in `~/.cursor/plans/`
- Always use `docs/features/feature-name/` directory structure
- Use Cursor's **Agent mode** (not Plan mode) when running this workflow to avoid `.plan.md` creation

**CRITICAL REMINDER:** The `/spec` workflow ONLY creates requirements. Design and tasks are created by the `/plan` workflow in separate phases. Do NOT create `design.md` or `tasks.md` in this workflow.

## Example of Correct Behavior:

```
[After identifying feature and researching]

## 📋 Preview: Requirements Specification

### Feature Identified
Instrument Resolution

### What I Understood
You want me to create requirements for the Instrument Resolution feature 
from downstream_pipeline_spec.md, which is currently unimplemented and 
unspecified in the features folder.

### Key Requirements I Plan to Document
1. Multi-step instrument matching (exact ticker → OpenFIGI → fuzzy match)
2. Automatic FinancialInstrument creation from OpenFIGI results
3. Pending queue for unresolved instruments

❓ Does this match your intent? Should I proceed with creating requirements.md?

[WAIT FOR USER RESPONSE - DO NOT CREATE FILE YET]
```

## Guidelines

- Be specific and actionable
- Consider edge cases and error handling
- Think about testing strategy
- Consider performance implications
- Document assumptions and constraints

## Integration

- **MUST read `@.agent/rules/global/requirements-format.md`** before creating requirements.md
- **MUST read `@.agent/rules/global/spec-workflow-enforcement.md`** before executing this workflow
- **MUST follow the format defined in `requirements-format.md`** (user stories, acceptance criteria, NOT technical specs)
- **MUST follow the enforcement rules in `spec-workflow-enforcement.md`** (only 2 files, no tasks.md, no design.md)
- References `planner-gate.md` for structure enforcement
- Works with `spec-driven-expert` skill for auto-discovery
- Output feeds into `/plan` workflow for detailed planning

## Requirements Format Reference

**CRITICAL:** Before creating `requirements.md`, you MUST:

1. **Read `@.agent/rules/global/requirements-format.md`** to understand the correct format
2. **Follow the structure defined in that rule:**
   - Overview
   - User Stories (As a... I want... so that...)
   - Functional Requirements (WHAT, not HOW)
   - Acceptance Criteria (Given/When/Then format)
   - Non-Functional Requirements

**DO NOT include in requirements.md:**
- ❌ Database schema definitions (belongs in `design.md`)
- ❌ API endpoint details (belongs in `design.md`)
- ❌ Technical implementation details (belongs in `design.md`)
- ❌ Code or pseudocode (belongs in `tasks.md`)

**Requirements.md focuses on WHAT needs to be built (user-facing), not HOW (technical implementation).**
