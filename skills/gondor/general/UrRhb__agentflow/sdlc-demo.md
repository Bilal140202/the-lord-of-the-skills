---
name: sdlc-demo
description: Quick 5-minute demo of AgentFlow. Creates a tiny 3-task project and runs one task end-to-end in the current session.
---

# /sdlc-demo

Experience AgentFlow in 5 minutes. This command creates a minimal demo project, decomposes it into 3 tasks on your Asana board, and builds one task end-to-end -- all within the current session.

## Prerequisites

Before running this demo, verify:

1. **Asana MCP connected** -- run `/sdlc-health` to check. The demo needs to create an Asana project.
2. **Git repository** -- you must be inside a git repo. Any project with a `package.json` works. If you do not have one, create a minimal project first:
   ```bash
   mkdir demo-project && cd demo-project
   git init && npm init -y
   ```
3. **Not on main branch** -- create a demo branch:
   ```bash
   git checkout -b agentflow-demo
   ```

If any prerequisite is missing, stop and tell the user exactly what to fix before proceeding.

## Process

### Step 1: Create Demo Spec (30 seconds)

Create a temporary `DEMO-SPEC.md` in the current directory with this content:

```markdown
# AgentFlow Demo Project

## Overview
A minimal hello-world project to demonstrate the AgentFlow pipeline.

## Tasks

### Task 1: Create greeting utility
Create `src/utils/hello.ts` that exports a `greet(name: string): string` function.
- Returns `"Hello, <name>! Welcome to AgentFlow."`
- Handle edge case: empty string returns `"Hello, World! Welcome to AgentFlow."`

### Task 2: Add unit tests (depends on Task 1)
Create `src/utils/__tests__/hello.test.ts` with test cases:
- greet("Alice") returns correct string
- greet("") returns default greeting
- greet with special characters works

### Task 3: Add npm script (depends on Task 1)
Add a `"greet"` script to `package.json` that runs: `npx ts-node -e "import {greet} from './src/utils/hello'; console.log(greet('Developer'))"`
```

Tell the user: "Created DEMO-SPEC.md with 3 tasks. Here is what will happen:"
- Task 1: Create a utility function (this one will be built live)
- Task 2: Write tests for it (would be built by Worker T3 in a full pipeline)
- Task 3: Add an npm script (would be built by Worker T2 in a full pipeline)

### Step 2: Decompose to Asana (1 minute)

Create an Asana project named `[SDLC] AgentFlow Demo` with the standard 8 sections:
- 0 - Needs Human
- 1 - Backlog
- 2 - Research
- 3 - Build
- 4 - Review
- 5 - Test
- 6 - Integrate
- 7 - Done

Create 3 tasks in the Backlog section with proper metadata headers:

**DEMO-001: Create greeting utility**
```
[SLOT:--] [STAGE:Backlog] [RETRY:0] [COST:~$0]

## Summary
Create a greeting utility function in TypeScript.

## Input State
Empty project with package.json.

## Output State
src/utils/hello.ts exists and exports greet(name: string): string.

## Acceptance Criteria
- [ ] greet("Alice") returns "Hello, Alice! Welcome to AgentFlow."
- [ ] greet("") returns "Hello, World! Welcome to AgentFlow."
- [ ] File exports are correct

## Verification Command
npx ts-node -e "import {greet} from './src/utils/hello'; console.log(greet('Test'))"

## Predicted Files
- src/utils/hello.ts (create)

## Dependencies
None

## Research Triggers
(none)

## Complexity
Simple
Estimated: 10 minutes
```

**DEMO-002: Add unit tests** (depends on DEMO-001)
```
[SLOT:--] [STAGE:Backlog] [RETRY:0] [COST:~$0]

## Summary
Add unit tests for the greeting utility.

## Input State
src/utils/hello.ts exists with greet function.

## Output State
src/utils/__tests__/hello.test.ts exists with passing tests.

## Acceptance Criteria
- [ ] 3 test cases covering normal, empty, and special character inputs
- [ ] All tests pass with npm test

## Verification Command
npm test -- --grep "hello"

## Predicted Files
- src/utils/__tests__/hello.test.ts (create)

## Dependencies
- DEMO-001 Create greeting utility -- function must exist before tests

## Research Triggers
(none)

## Complexity
Simple
Estimated: 10 minutes
```

**DEMO-003: Add npm greet script** (depends on DEMO-001)
```
[SLOT:--] [STAGE:Backlog] [RETRY:0] [COST:~$0]

## Summary
Add a "greet" npm script to package.json.

## Input State
src/utils/hello.ts exists. package.json exists.

## Output State
Running "npm run greet" prints a greeting to the console.

## Acceptance Criteria
- [ ] npm run greet executes without errors
- [ ] Output contains "Welcome to AgentFlow"

## Verification Command
npm run greet

## Predicted Files
- package.json (modify)

## Dependencies
- DEMO-001 Create greeting utility -- function must exist before script can call it

## Research Triggers
(none)

## Complexity
Simple
Estimated: 5 minutes
```

Also create a pinned Status task with the initial dashboard.

Tell the user:
- "Created [SDLC] AgentFlow Demo in Asana with 3 tasks in Backlog."
- Show the Asana project URL.
- "Now building Task 1 live..."

### Step 3: Build Task 1 (2-3 minutes)

Act as Worker T2 executing the Build stage for DEMO-001.

1. **Assign the task**: Update DEMO-001 metadata to `[SLOT:T2] [STAGE:Build]`. Move it to the Build section.

2. **Post start comment**: Add an Asana comment: `[BUILD:STARTED] Worker T2 beginning build for DEMO-001.`

3. **Create the file**: Write `src/utils/hello.ts`:
   ```typescript
   /**
    * Returns a greeting string for the given name.
    * Falls back to "World" if name is empty.
    */
   export function greet(name: string): string {
     const displayName = name.trim() || "World";
     return `Hello, ${displayName}! Welcome to AgentFlow.`;
   }
   ```

4. **Run lint gate** (if TypeScript is configured):
   - Try `npx tsc --noEmit` -- if tsconfig.json exists
   - Try `npx eslint src/` -- if eslint is configured
   - If neither is configured, note this and continue (demo project may be minimal)
   - Post result: `[LINT:PASS]` or `[LINT:SKIP] No TypeScript/ESLint config found (demo project).`

5. **Post heartbeat**: `[HEARTBEAT] T2 working on DEMO-001`

6. **Create a commit** on the current branch:
   ```bash
   git add src/utils/hello.ts
   git commit -m "feat(DEMO-001): add greeting utility"
   ```

7. **Post completion**: Add Asana comment: `[BUILD:COMPLETE] Created src/utils/hello.ts. Commit: <hash>.`

8. **Update metadata**: `[SLOT:T2] [STAGE:Build-Complete] [RETRY:0] [COST:~$0.50]`

### Step 4: Show Results (30 seconds)

Print a summary to the user:

```
=== Demo Complete ===

What just happened:
  1. DEMO-001 moved: Backlog -> Build -> Build-Complete
  2. File created: src/utils/hello.ts
  3. Asana comment thread shows the full audit trail:
     - [BUILD:STARTED]
     - [HEARTBEAT]
     - [LINT:PASS] (or SKIP)
     - [BUILD:COMPLETE]

In a full pipeline, here is what happens next:
  - Orchestrator (crontab) detects Build-Complete
  - DEMO-001 moves to Review (assigned to Worker T4)
  - T4 runs adversarial review: "list 3 things wrong before deciding to pass"
  - If approved: moves to Test (Worker T5)
  - T5 runs full test suite + coverage check
  - If passed: merges PR to main, runs integration check
  - Meanwhile, DEMO-002 and DEMO-003 unblock and get dispatched to T2/T3

Open Asana on your phone to see the board and comment thread.
```

Show the Asana project URL again.

### Step 5: Cleanup

Ask the user:

```
Keep the demo project?
  [keep]   Leave everything as-is (you can continue building DEMO-002 and DEMO-003)
  [delete] Remove the Asana project and demo files
```

**If keep:** Leave everything. Tell the user they can continue with:
- `claude -p '/sdlc-worker --slot T2'` to build remaining tasks
- Or set up the full pipeline with `./setup.sh --with-cron`

**If delete:**
1. Delete the Asana project (use the delete/archive project MCP call)
2. Remove the created files:
   ```bash
   rm -f src/utils/hello.ts
   rm -f DEMO-SPEC.md
   git reset HEAD~1  # Undo the demo commit
   ```
3. Tell the user: "Demo cleaned up. No artifacts remain."

## Key Message

Always end with:

```
You just saw one task go through the Build stage with full observability.
In a full pipeline, 4 workers handle Build/Review/Test/Integrate in parallel
across all tasks -- visible from your Kanban board.

Set up the full pipeline: ./setup.sh --with-cron
Full docs: https://github.com/UrRhb/agentflow
```
