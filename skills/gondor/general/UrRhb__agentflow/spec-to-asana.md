---
name: spec-to-asana
description: Convert a SPEC.md into a structured Kanban board with atomic tasks, dependencies, and acceptance criteria for the AgentFlow pipeline.
---

# /spec-to-asana

Convert a product spec into a fully structured Kanban project board for the AgentFlow pipeline.

## Prerequisites

Before running, you need:
1. A SPEC.md file (or a product idea to brainstorm into one)
2. Access to your PM tool's MCP integration (e.g., Asana MCP)
3. The AgentFlow conventions: read `conventions.md`

## Process

### Phase 1: Spec Acquisition

If a SPEC.md path is provided as argument, read it.

If no argument provided, ask the user:
- "What product/feature are you building?"
- Help create a SPEC.md
- Save to a `docs/specs/` directory

### Phase 2: Project Setup

1. **Determine project code**: Check conventions.md for existing codes. If new project, ask user for 3-letter code.

2. **Read the project's file structure**:
   ```
   Glob: **/*.ts, **/*.tsx, **/*.js pattern in the project directory
   ```
   This gives predicted files context for decomposition.

3. **Read package.json**: Get current dependencies (needed for research trigger evaluation).

4. **Select model cost profile**: Ask the user: "Which Claude model will workers use? (sonnet/opus)" This sets the cost profile in conventions.md (affects cost ceilings and guardrails).

### Phase 3: Decompose

Read the decomposition prompt: `prompts/decompose.md`

For each phase/section in the SPEC.md:
1. Break into atomic tasks following the decomposition rules
2. Map dependencies between tasks
3. Evaluate research triggers per task
4. Detect and resolve shared-file conflicts

### Phase 4: Validate

Run the decomposition validator (from decompose.md) BEFORE creating anything in the PM tool:

1. **Rubric check**: All 9 fields present per task
2. **Topological sort**: No circular dependencies
3. **File conflict check**: Parallel tasks don't share files
4. **Atomicity check**: No task modifies > 5 files
5. **Verification command check**: All commands are valid bash
6. **Safety check**: All verification commands use only safe commands (npm, npx, node, curl localhost). No external URLs, no `rm -rf`, no `eval`, no `sudo`.

If validation fails, fix the decomposition. Do NOT proceed with invalid tasks.

### Phase 5: Create in PM Tool

**Step 1: Create the project**

Create the project with 8 sections:

```
project_name: "[SDLC] <CODE> Phase <N> - <Phase Title>"
sections:
  - name: "0 - Needs Human"
    tasks: []
  - name: "1 - Backlog"
    tasks: [... all atomic tasks ...]
  - name: "2 - Research"
    tasks: []
  - name: "3 - Build"
    tasks: []
  - name: "4 - Review"
    tasks: []
  - name: "5 - Test"
    tasks: []
  - name: "6 - Integrate"
    tasks: []
  - name: "7 - Done"
    tasks: []
```

Each task in the Backlog section includes the full description template from conventions.md.

**Step 2: Set dependencies**

After project creation, set dependencies between tasks using the PM tool's API. Batch updates where possible.

**Step 3: Create pinned Status task**

Create a task in "0 - Needs Human" section:

```
name: "SDLC Status"
description: |
  [STATUS] [SPEC_HASH:<sha256 of SPEC.md>]
  ---
  ## System Status
  Active: 0 tasks
  Completed: 0/<total> tasks
  Total retries: 0
  Est. cost: ~$0
  Blocked: 0
  ETA: not started
```

This serves as the dashboard and spec drift detector.

**Step 4: Add decomposition summary comment**

Post a comment on the Status task:

```
## Decomposition Summary

Phase: <phase title>
Total tasks: <N>
Sub-phases: <N>
Dependencies: <N edges>
Research required: <N tasks>
Estimated total cost: ~$<N>

### Dependency Graph
<sub-phase groupings showing parallel tracks>

### Risk Assessment
- Highest-dependency task: [CODE-NNN] (blocks N others)
- Longest chain: [CODE-001] → [CODE-003] → [CODE-007] (3 deep)
- Shared-file serializations: N
```

### Phase 6: Confirm

Show the user:
1. Total tasks created
2. Sub-phase groupings
3. Dependency graph summary
4. Estimated timeline (tasks / estimated parallelism x avg time)
5. Link to the Kanban board

Ask: "Board created. Want me to start the workers, or do you want to review the board first?"

## Error Handling

- If PM tool API fails: report the error, show what was attempted
- If SPEC.md is too vague: ask user for clarification before decomposing
- If decomposition produces > 30 tasks for a single phase: warn user, suggest splitting the phase
- If topological sort finds a cycle: report which tasks form it, ask user how to restructure

## Notes

- This skill does NOT start any workers or orchestration. It only creates the board structure.
- The user can modify the board manually after creation (add/remove tasks, change descriptions)
- Re-running this skill on the same spec will create a NEW project (won't modify existing)
