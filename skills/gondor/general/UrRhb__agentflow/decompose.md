# Decomposition Prompt

You are decomposing a SPEC.md section into atomic tasks for the AgentFlow pipeline.

## Input

You will receive:
1. A SPEC.md file (or section of one)
2. The project code (e.g., APP, API)
3. The phase number and title
4. The project's existing file structure (from `ls` or `Glob`)
5. The project's `package.json` dependencies (for research trigger evaluation)

## Output

Produce a JSON array of atomic tasks, each with ALL required fields from the decomposition quality rubric.

## Process

### Step 1: Read and understand the spec section

Identify:
- Features to build
- Data models needed
- API endpoints needed
- UI components needed
- External integrations needed
- Testing requirements

### Step 2: Break into atomic tasks

Each task must satisfy ALL atomicity rules:
- Single PR (one pull request)
- Single concern (one service, route, or component)
- Independently testable (at least one test)
- < 2 hours of estimated work
- <= 5 files modified
- Clear verification command

### Step 3: Map dependencies

For each task, identify which other tasks must be Done before it can start.

Rules:
- Dependencies must flow forward (no circular dependencies)
- Shared infrastructure tasks (models, middleware, config) come first
- UI tasks depend on their API endpoints
- Test-only tasks are rare — tests should be part of each feature task

### Step 4: Evaluate research triggers

For each task, check:
- [ ] Uses external library not in package.json
- [ ] Involves a domain the codebase hasn't touched
- [ ] Task description says "investigate" or "evaluate"
- [ ] First of its kind in this project

### Step 5: Detect shared-file conflicts

For all tasks that share NO dependency relationship (can run in parallel):
- Check if their predicted files overlap
- If overlap → add a dependency to serialize them
- Prefer: the task that creates the file depends on nothing; the task that modifies it depends on the creator

### Step 6: Generate dependency graph

Run a topological sort on the dependency graph:
- If cycle detected → STOP. Restructure by extracting a shared "foundation" task that breaks the cycle.
- Diamond dependencies with shared files → serialize the diamond (add dependency between the two parallel legs)

## Task JSON Format

```json
{
  "task_code": "APP-001",
  "name": "Create Express server scaffold",
  "description": "<full task description using the template from conventions.md>",
  "input_state": "Empty project directory with package.json",
  "output_state": "src/index.ts exports running Express app, src/routes/ directory exists",
  "acceptance_criteria": [
    "Express server starts on port from env",
    "Health check endpoint returns 200",
    "Error handling middleware catches unhandled errors"
  ],
  "verification_command": "npm test -- --grep 'server' && npx tsc --noEmit",
  "predicted_files": {
    "create": ["src/index.ts", "src/routes/health.ts", "tests/server.test.ts"],
    "modify": ["package.json"]
  },
  "dependencies": [],
  "research_triggers": {
    "external_library": false,
    "new_domain": false,
    "investigate": false,
    "first_of_kind": true
  },
  "research_required": true,
  "complexity": "M",
  "branch": "feat/APP-001-express-scaffold"
}
```

## Validation Checklist (run BEFORE creating in PM tool)

After generating all tasks, validate:

1. **Rubric check**: Every task has all 9 required fields
   - input_state, output_state, acceptance_criteria (>=1 item), verification_command, predicted_files, dependencies, research_triggers, complexity, branch

2. **Topological sort**: Dependency graph has no cycles
   - Build adjacency list from dependencies
   - Run Kahn's algorithm or DFS-based topo sort
   - If cycle → report which tasks form the cycle

3. **File conflict check**: No two parallel tasks modify the same file
   - "Parallel" = tasks with no dependency relationship between them
   - If conflict → add dependency to serialize

4. **Atomicity check**: No task creates+modifies > 5 files total

5. **Verification syntax check**: Every verification command is valid AND safe shell syntax
   - Allowed commands: `npm`/`npx` commands, `node` commands, `curl` to localhost only, `grep`/`test` commands
   - Reject any command containing: `curl`/`wget`/`fetch` to external URLs, `rm -rf`, `sudo`, `eval`, backticks executing arbitrary code, pipes to `sh`/`bash`
   - No obvious syntax errors

6. **Naming check**: All task codes are sequential and unique

If ANY validation fails, fix the decomposition BEFORE creating tasks. Do not create invalid tasks.

## Grouping into Sub-phases

After validation, group tasks into sub-phases of 3-5 parallel tasks (tasks with no dependency between them). This helps the orchestrator understand which tasks can run concurrently.

```
Sub-phase 1 (foundation):
  [APP-001] Create Express scaffold
  [APP-002] Create database connection

Sub-phase 2 (models + middleware):
  [APP-003] Create User model (depends on APP-001, APP-002)
  [APP-004] Create JWT middleware (depends on APP-001)
  [APP-005] Create error handling middleware (depends on APP-001)

Sub-phase 3 (features):
  [APP-006] Build upload API (depends on APP-003, APP-004)
  [APP-007] Build parser service (depends on APP-001)
  ...
```
