# Plan Command

Generate a detailed implementation plan from a specification. This command works in phases with user review between each phase.

## 🚨 CRITICAL RULE: ONE PHASE PER RUN

**YOU CAN ONLY EXECUTE ONE PHASE PER RUN. AFTER COMPLETING A PHASE, YOU MUST STOP AND WAIT FOR USER REVIEW BEFORE PROCEEDING TO THE NEXT PHASE.**

**⛔ FORBIDDEN:**
- Creating both `design.md` AND `tasks.md` in the same run
- Proceeding to Phase 2 immediately after Phase 1
- Skipping user review between phases

**✅ REQUIRED:**
- Execute ONE phase per run
- STOP after completing each phase
- Inform user and wait for review/approval
- Only proceed to next phase after explicit user confirmation

## Phased Workflow

**This command works in phases. Only proceed to the next phase after user review and approval.**

1. **Phase 1: Design** (if `design.md` doesn't exist)
   - Creates `design.md` → **STOPS for review**
   - User reviews and approves design
   - **MUST wait for user confirmation before Phase 2**

2. **Phase 2: Tasks** (if `design.md` exists but `tasks.md` doesn't exist)
   - **ONLY if user has reviewed and approved Phase 1**
   - Creates `tasks.md` → **STOPS for review**
   - User reviews and approves tasks

**Do NOT create both files in one run. Check what exists and only create the next file.**

## Prerequisites

Before running this command:
- Ensure `docs/features/feature-name/requirements.md` exists
- Review the requirements to understand the feature scope

**Note:** This command works with spec-driven format (`docs/features/feature-name/`), NOT Cursor's native `.plan.md` files in `~/.cursor/plans/`

## Process

**Step 1: Check what exists**
- Check if `docs/features/feature-name/design.md` exists
- Check if `docs/features/feature-name/tasks.md` exists

**Step 2: Determine which phase to execute**

**CRITICAL RULE:** You can ONLY execute ONE phase per run. After completing a phase, you MUST STOP and wait for user review before proceeding to the next phase.

### Phase 1: Create Design (if design.md doesn't exist)

**ONLY execute this phase if `design.md` doesn't exist.**
**If `design.md` already exists, skip to Phase 2 (but only if user has reviewed Phase 1).**

```xml
<check_requirements>
[Verify docs/features/feature-name/requirements.md exists and contains required sections]
</check_requirements>

<requirements_analysis>
[Analyze requirements, identify dependencies, clarify ambiguities]
</requirements_analysis>

<design_refinement>
[Refine design decisions, identify components, define interfaces]
</design_refinement>
```

**Output:** Create ONLY `docs/features/feature-name/design.md`
- Architecture overview
- Component specifications
- Data flow diagrams
- Integration points
- Technology choices and patterns

**🚨🚨🚨 CRITICAL: YOU MUST STOP HERE 🚨🚨🚨**

**DO NOT CREATE `tasks.md` YET.**
**DO NOT PROCEED TO PHASE 2.**
**WAIT FOR USER TO REVIEW AND APPROVE `design.md`.**

After creating `design.md`:
1. Inform the user: "I have created `design.md`. Please review it."
2. **STOP and wait for user response**
3. Only proceed to Phase 2 (creating `tasks.md`) after user explicitly confirms they've reviewed and approved the design

### Phase 2: Create Tasks (if design.md exists but tasks.md doesn't exist)

**🚨 CRITICAL: Only proceed to Phase 2 if:**
- `design.md` exists AND has been reviewed/approved by the user
- User has explicitly confirmed they want to proceed to task creation
- You are NOT in the same run as Phase 1

**If you just created `design.md` in Phase 1, you MUST STOP and wait for user review before proceeding to Phase 2.**

```xml
<check_design>
[Verify docs/features/feature-name/design.md exists and contains required sections]
[Verify user has reviewed and approved design.md - if not, STOP and ask for review]
</check_design>

<task_breakdown>
[Break down tasks into subtasks, identify dependencies, estimate effort]
</task_breakdown>

<test_requirements>
[For each implementation task, specify test requirements using real services]
</test_requirements>

<validation>
[Verify plan completeness, check for missing pieces, validate approach]
</validation>
```

**Output:** Create ONLY `docs/features/feature-name/tasks.md`
- Ordered task list
- Dependencies between tasks
- Acceptance criteria per task
- Estimated effort
- Implementation sequence
- **Test requirements for each task (using real services, no mocks)**

**CRITICAL: Test Requirements in Tasks**

When creating tasks, you MUST include test requirements that specify:
- **Real Services Only:** Tests must use real APIs, real BigQuery, real GCS, real databases
- **No Mocks:** Explicitly state "DO NOT use mocks, stubs, or fake implementations"
- **Test Creation:** Each implementation task must have a corresponding test task/subtask
- **Test Execution:** Tests must be run immediately after creation
- **Test Types:** Specify integration tests for external services, unit tests for pure logic

**Example task format:**
```markdown
- [ ] **Task 1.1**: Implement OpenFIGI API integration
  - [ ] Create OpenFIGIResource class
  - [ ] Implement lookup_ticker method
  - [ ] **Test:** Create integration test using real OpenFIGI API (no mocks)
    - Test must call actual OpenFIGI endpoint
    - Test must verify real API responses
    - Run test immediately after implementation
```

**🚨🚨🚨 CRITICAL: YOU MUST STOP HERE 🚨🚨🚨**

**DO NOT PROCEED TO ANY OTHER TASKS.**
**WAIT FOR USER TO REVIEW AND APPROVE `tasks.md`.**

After creating `tasks.md`:
1. Inform the user: "I have created `tasks.md`. Please review it."
2. **STOP and wait for user response**
3. Do NOT proceed to implementation or any other steps

## Sequence Enforcement

- **Requirements** must exist before **Design**
- **Design** must exist before **Tasks**
- Cannot skip phases or work out of order
- Each phase must be complete and reviewed before moving to the next
- **Only create ONE file per run** (either design.md OR tasks.md, not both)

## Integration

- References `planner-gate.md` for content structure
- Ensures Requirements → Design → Tasks sequence
- Works with `task-manager.md` for Definition of Done
- Output feeds into execution phase

## Testing Policy for Task Planning

**When creating tasks in `tasks.md`, you MUST include test requirements:**

### Real Services Testing Policy

**⛔ FORBIDDEN in test requirements:**
- Using mocks, stubs, or fake implementations
- Using test doubles for APIs, BigQuery, GCS, or databases
- Skipping tests or marking tasks complete without tests

**✅ REQUIRED in test requirements:**
- Use real APIs (OpenFIGI, external APIs, etc.)
- Use real BigQuery (actual project and dataset)
- Use real GCS (actual buckets and objects)
- Use real databases (actual connections and data)
- Create tests immediately after implementation
- Run tests immediately after creation
- Ensure all tests pass before proceeding

### Test Requirements Format

Each implementation task MUST include:
1. **Test subtask** that specifies:
   - Test type (integration/unit/e2e)
   - Real services to use (no mocks)
   - What to verify
   - When to run (immediately after implementation)

**Example:**
```markdown
- [ ] **Task 1.1**: Implement API integration
  - [ ] Create API client
  - [ ] **Test:** Integration test with real API
    - Use actual API endpoint (no mocks)
    - Verify real responses
    - Run: `pytest tests/test_api.py -v` immediately after implementation
```

## Best Practices

- Break large tasks into smaller, manageable pieces
- Identify and document dependencies early
- **Include test requirements for every implementation task (using real services)**
- Plan for error handling and edge cases
- Estimate effort realistically (including test creation and execution time)
