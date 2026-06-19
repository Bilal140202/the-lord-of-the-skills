# GSD Orchestration

## Pattern

GSD workflows are orchestrators. They spawn specialized agents (skills) to do work. Each agent runs in a **fresh context window** to prevent context rot.

## Your Role

When a `/gsd-*` workflow runs, you are the orchestrator:

1. Parse the workflow
2. Spawn the required agents/skills
3. Parallelize where indicated
4. Collect results from files
5. Route to next step

## Spawning Agents

When workflows indicate agent spawning:

```
Task(subagent_type="gsd-executor", ...)
Task(subagent_type="gsd-planner", ...)
```

Spawn the corresponding skill in a fresh context. Pass the required files as context.

## Parallel Execution

When multiple agents can run simultaneously (same wave, no dependencies), spawn them in parallel:

```
Wave 1: gsd-executor (Plan 01), gsd-executor (Plan 02), gsd-executor (Plan 03)
→ Run all three in parallel

Wave 2: gsd-executor (Plan 04)
→ Run after Wave 1 completes
```

## Agent → Skill Mapping

| Agent | Skill | Purpose |
|-------|-------|---------|
| `gsd-executor` | `gsd-executor` | Execute PLAN.md |
| `gsd-planner` | `gsd-planner` | Create PLAN.md files |
| `gsd-debugger` | `gsd-debugger` | Investigate bugs |
| `gsd-verifier` | `gsd-verifier` | Verify goals achieved |
| `gsd-phase-researcher` | `gsd-phase-researcher` | Research before planning |
| `gsd-project-researcher` | `gsd-project-researcher` | Research domain ecosystem |
| `gsd-research-synthesizer` | `gsd-research-synthesizer` | Combine research outputs |
| `gsd-roadmapper` | `gsd-roadmapper` | Create ROADMAP.md |
| `gsd-plan-checker` | `gsd-plan-checker` | Verify plans achieve goals |
| `gsd-codebase-mapper` | `gsd-codebase-mapper` | Analyze existing codebase |
| `gsd-integration-checker` | `gsd-integration-checker` | Check cross-phase wiring |

## Model Selection

Workflows reference model tiers. Map to Gemini models:

| Workflow Reference | Use Model | For |
|-------------------|-----------|-----|
| `opus` | **Gemini 3 Pro (High)** | Planning, complex reasoning, architectural decisions |
| `sonnet` | **Gemini 3 Pro (Low)** | Execution, standard implementation work |
| `haiku` | **Gemini 3 Flash** | Verification, quick checks, simple tasks |

When spawning agents, use the appropriate model tier based on the agent type:

| Agent | Model Tier |
|-------|------------|
| `gsd-planner` | Gemini 3 Pro (High) |
| `gsd-roadmapper` | Gemini 3 Pro (High) |
| `gsd-phase-researcher` | Gemini 3 Pro (High) |
| `gsd-project-researcher` | Gemini 3 Pro (High) |
| `gsd-executor` | Gemini 3 Pro (Low) |
| `gsd-debugger` | Gemini 3 Pro (Low) |
| `gsd-verifier` | Gemini 3 Pro (Low) |
| `gsd-plan-checker` | Gemini 3 Pro (Low) |
| `gsd-research-synthesizer` | Gemini 3 Pro (Low) |
| `gsd-codebase-mapper` | Gemini 3 Pro (Low) |
| `gsd-integration-checker` | Gemini 3 Flash |

## Tool Name Mapping

Workflows may reference these tools. Use the equivalent:

| Workflow Reference | Use |
|-------------------|-----|
| `AskUserQuestion` | `question` |
| `SlashCommand` | `skill` |
| `TodoWrite` | `todowrite` |
| `Task` | Spawn skill in fresh context |
| `Read` | Read file |
| `Write` | Write file |
| `Edit` | Edit file |
| `Bash` | Run command |
| `Glob` | Find files by pattern |
| `Grep` | Search file contents |
| `WebFetch` | Fetch URL content |
| `WebSearch` | Search web |

## Command Format

Commands use hyphen format: `/gsd-help`, `/gsd-new-project`, `/gsd-plan-phase`

## File References

Workflows reference files with `@` prefix. Read those files:
- `@.planning/STATE.md` → Read `.planning/STATE.md`
- `@~/.gemini/antigravity/get-shit-done/templates/project.md` → Read that template

## Context Passing

Before spawning an agent, read the files it needs and pass them:

| Agent | Required Context |
|-------|------------------|
| `gsd-executor` | PLAN.md, STATE.md, PROJECT.md |
| `gsd-planner` | ROADMAP.md, STATE.md, CONTEXT.md, RESEARCH.md |
| `gsd-verifier` | PLAN.md files, ROADMAP.md, REQUIREMENTS.md |
| `gsd-debugger` | Bug description, relevant source files |
| `gsd-phase-researcher` | Phase goal, CONTEXT.md if exists |
| `gsd-project-researcher` | PROJECT.md, research focus area |
| `gsd-roadmapper` | PROJECT.md, REQUIREMENTS.md, research/SUMMARY.md |
| `gsd-plan-checker` | ROADMAP.md, all PLAN.md files for phase |
| `gsd-codebase-mapper` | Focus area (tech/arch/quality/concerns) |

Agents write results to `.planning/` files. Read those files to continue orchestration.

## Workflow Orchestration

### /gsd-execute-phase {N}

1. Read all PLAN.md files for phase N
2. Group by wave (from frontmatter)
3. For each wave:
   - Spawn `gsd-executor` for each plan in parallel
   - Wait for all to complete (SUMMARY.md files written)
4. After all waves: Spawn `gsd-verifier`
5. Report results

### /gsd-plan-phase {N}

1. Load context (ROADMAP, STATE, CONTEXT.md if exists)
2. If `workflow.research` enabled: Spawn `gsd-phase-researcher`
3. Spawn `gsd-planner` with all context
4. If `workflow.plan_check` enabled: Spawn `gsd-plan-checker`
5. If issues found: Spawn `gsd-planner` again with feedback
6. Commit and report

### /gsd-new-project (with research)

1. Gather project context through questioning
2. Spawn 4 `gsd-project-researcher` agents in parallel:
   - Focus: STACK
   - Focus: FEATURES
   - Focus: ARCHITECTURE
   - Focus: PITFALLS
3. Spawn `gsd-research-synthesizer` to combine outputs
4. Spawn `gsd-roadmapper` to create roadmap
5. Present for approval

### /gsd-verify-work {N}

1. Spawn `gsd-verifier` with phase context
2. If gaps found: Present to user, offer to create fix plans
3. If fix plans needed: Spawn `gsd-planner` for gaps
4. Report verification results

### /gsd-debug

1. Spawn `gsd-debugger` with bug description
2. Debugger investigates, forms hypotheses, tests
3. When root cause found: Fix and verify
4. Report resolution

## Checkpoint Handling

Some plans have `autonomous: false` in frontmatter. When executing these:

1. Execute until checkpoint reached
2. Present checkpoint context to user
3. Get user input/decision
4. Continue execution with user's input

Checkpoints are for: authentication setup, API key configuration, external service decisions.

## Deviation Handling

During execution, handle deviations:

| Deviation Type | Action |
|---------------|--------|
| Bug discovered | Auto-fix, document in SUMMARY.md |
| Missing critical functionality | Auto-add (security, validation, error handling), document |
| Blocker (missing import, dependency) | Auto-fix, document |
| Architectural change needed | Stop, ask user, document decision |

## Commit Format

After completing tasks, commit with this format:

```
{type}({phase}-{plan}): {description}

Task: {N}.{P}.{T}
Phase: {N}

Co-Authored-By: Gemini <noreply@google.com>
```

Types: `feat`, `fix`, `test`, `refactor`, `perf`, `docs`, `chore`

## State Persistence

All state lives in `.planning/` files:
- `STATE.md` - Current position, decisions, blockers
- `SUMMARY.md` - What agents accomplished
- `VERIFICATION.md` - Verification results
- `config.json` - Workflow settings

These persist across context windows. Read them to resume or continue.

Update `STATE.md` after:
- Decisions made
- Tasks completed
- Blockers encountered
- Before ending session

## Config Settings

Read `.planning/config.json` for workflow settings:

```json
{
  "mode": "interactive",
  "depth": "standard",
  "model_profile": "balanced",
  "workflow": {
    "research": true,
    "plan_check": true,
    "verifier": true
  }
}
```

- `workflow.research`: Whether to spawn researcher before planning
- `workflow.plan_check`: Whether to spawn plan checker after planning
- `workflow.verifier`: Whether to spawn verifier after execution

## Directory Structure

```
.planning/
├── PROJECT.md
├── REQUIREMENTS.md
├── ROADMAP.md
├── STATE.md
├── config.json
├── research/
│   ├── SUMMARY.md
│   ├── STACK.md
│   ├── FEATURES.md
│   ├── ARCHITECTURE.md
│   └── PITFALLS.md
├── codebase/
│   └── {analysis files}
├── phases/
│   └── {NN}-{name}/
│       ├── {NN}-CONTEXT.md
│       ├── {NN}-RESEARCH.md
│       ├── {NN}-{PP}-PLAN.md
│       ├── {NN}-{PP}-SUMMARY.md
│       └── {NN}-VERIFICATION.md
├── quick/
│   └── {NNN}-{slug}/
├── debug/
│   └── resolved/
└── todos/
    ├── pending/
    └── done/
```

## Fresh Context Rule

Each spawned agent runs in fresh context. This prevents context rot and gives each agent full context budget.

Results pass between agents via `.planning/` files, not memory.

## Reference Files

GSD reference docs are at `~/.gemini/antigravity/get-shit-done/`:
- `references/` - Methodology docs (questioning, checkpoints, git-integration, etc.)
- `templates/` - File templates (project.md, requirements.md, plan.md, etc.)
- `workflows/` - Detailed workflow definitions

Read these when you need methodology guidance or templates.
