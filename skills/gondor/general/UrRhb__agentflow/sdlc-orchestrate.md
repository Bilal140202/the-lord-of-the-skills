---
name: sdlc-orchestrate
description: Stateless orchestrator sweep for the AgentFlow pipeline. Reads Kanban state, dispatches tasks, handles transitions, tracks costs, detects issues. Run via crontab every 15 min.
---

# /sdlc-orchestrate

Perform one stateless orchestration sweep of all AgentFlow projects.

This is a ONE-SHOT command. It reads state, makes decisions, updates the Kanban board, and exits. It does NOT run continuously. Durability comes from invoking this via real crontab:

```bash
# Default (every 15 min, ~$48/day):
*/15 * * * * ~/.claude/sdlc/agentflow-cron.sh >> /tmp/agentflow-orchestrate.log 2>&1

# Sprint mode (every 5 min, use during active dev only):
# */5 * * * * ~/.claude/sdlc/agentflow-cron.sh >> /tmp/agentflow-orchestrate.log 2>&1
```

## Setup

1. Read conventions: `conventions.md`
2. Read all prompt templates for reference (don't execute them — that's the workers' job)

## Sweep Process

### Step 0: Acquire Sweep Lock

Check the Status task for a recent `[SWEEP:RUNNING <timestamp>]` comment.
If a sweep started less than 10 minutes ago, EXIT immediately:
  "Another sweep is still running (started `<timestamp>`). Skipping this invocation."
If no recent sweep or last sweep is >10 min old:
  Post: `[SWEEP:RUNNING <current_timestamp>]`
  Continue with Step 1.
At the END of the sweep (after Step 9), post: `[SWEEP:COMPLETE <current_timestamp>]`

### Step 1: Discover Projects

```
Find all projects with names starting with "[SDLC]"
```

For each project:
- Get project details (include sections)
- Map section names to section IDs
- Get all tasks per section

Build the complete pipeline state: a map of all tasks, their stages, slots, retry counts, and costs.

**Quick check:** If ALL tasks across all projects are in Backlog (waiting on dispatch) or Done, and no tasks are in active stages (Research/Build/Review/Test/Integrate), post a minimal status update and EXIT early. This "idle sweep" costs ~$0.02 instead of ~$0.50.

### Step 2: Spec Drift Check

For each project, read the pinned Status task (in "0 - Needs Human" section).
Parse `[SPEC_HASH:<hash>]` from its description.

For each project's source SPEC.md:
- Compute SHA-256 hash of current file
- Compare to stored hash
- If changed:
  1. Post `[SPEC:CHANGED]` comment on Status task
  2. For ALL non-Done tasks, add `[NEEDS:REVALIDATION]` to description
  3. STOP dispatching for this project until user posts `[SPEC:CONTINUE]` or `[SPEC:REDECOMPOSE]`

### Step 3: Heartbeat Check

For each task in Build/Review/Test stages with an assigned slot:
- Read comments, find latest `[HEARTBEAT]` or `[BUILD:STARTED]`
- If no heartbeat for > 10 minutes:
  1. Post `[REASSIGNED] Previous worker (<old_slot>) unresponsive after 10 min. Reassigning.`
  2. Clear the slot: update `[SLOT:<old>]` → `[SLOT:--]` in task description
  3. The task will be re-dispatched in Step 6

### Step 4: Process Stage Transitions

For each task, read the LAST 10 comments per task (not all comments). The latest comment tag determines state. If the task has >20 comments, only parse the most recent 20 for transition logic. This prevents context window overflow on long-running tasks.

Check the latest comment tag and update accordingly:

| Latest Tag | Current Section | Action |
|-----------|----------------|--------|
| `[RESEARCH:COMPLETE]` or `[RESEARCH:SKIP]` | 2 - Research | Move to "3 - Build" |
| `[BUILD:COMPLETE]` + `[LINT:PASS]` | 3 - Build | Move to "4 - Review" |
| `[LINT:FAIL]` | 3 - Build | Keep in Build, clear slot for retry |
| `[REVIEW:PASS]` + `[COV:PASS]` | 4 - Review | Move to "5 - Test" |
| `[REVIEW:REJECT]` | 4 - Review | Move to "3 - Build", trigger feedback loop |
| `[COV:FAIL]` | 4 - Review | Move to "3 - Build", trigger feedback loop |
| `[TEST:PASS]` | 5 - Test | Move to "6 - Integrate" |
| `[TEST:REJECT]` | 5 - Test | Move to "3 - Build", trigger feedback loop |
| `[INTEGRATE:PASS]` | 6 - Integrate | Move to "7 - Done", mark complete |
| `[INTEGRATE:FAIL]` | 6 - Integrate | Move to "3 - Build", trigger feedback loop |
| `[BUILD:BLOCKED]` | 3 - Build | Move to "0 - Needs Human" |
| `[HOLD]` | Any | Move to "0 - Needs Human" |

**Merge lock check:** Before processing any `[TEST:PASS]` transition that would lead to merge, check the Status task for an active `[MERGE_LOCK]`. If locked by another task, do NOT transition -- leave the task in Test until the lock clears.

Batch move tasks between sections where possible.

### Step 5: Trigger Feedback Loops

For each task that was rejected/failed:

1. Increment retry counter: update `[RETRY:N]` → `[RETRY:N+1]`
2. Update cost: add stage cost to `[COST:~$X]`
3. Check cost thresholds (cost ceilings depend on model configuration -- check conventions.md for the active cost profile, Sonnet or Opus. Default to Sonnet ceilings unless the project's conventions explicitly specify Opus):
   - If > warning threshold ($3 Sonnet / $8 Opus): Post `[COST:WARNING]`
   - If > hard stop ($10 Sonnet / $20 Opus): Post `[COST:CRITICAL]`, move to "0 - Needs Human", STOP processing this task
4. Post retry context comment:

```markdown
[RETRY:<N+1>]

## Retry Context (Attempt <N+1>)

### What was tried
<Extract from the most recent [BUILD:COMPLETE] comment>

### What failed
<Extract from the rejection comment — [REVIEW:REJECT], [TEST:REJECT], etc.>

### What to do differently
<Synthesize from the rejection details — be specific>

### Accumulated learnings
<Compile ALL previous retry contexts into a summary>
```

5. Clear slot assignment: `[SLOT:T4]` → `[SLOT:--]`
6. On retry 2+: note in the retry context that a DIFFERENT worker should be assigned

### Step 6: Dispatch Tasks

For each task in Backlog ("1 - Backlog") section:

**Check dependencies:**
- Parse `## Dependencies` from task description
- For each dependency task code, find the task
- If ALL dependencies are in "7 - Done" → task is ready
- If any dependency is NOT in Done → skip

**Check file conflicts:**
- Parse `## Predicted Files` from this task
- For each task currently in Build/Review/Test/Integrate, parse their predicted files
- If ANY file appears in both lists → skip (serialize)

**Calculate priority:**
- Count how many other Backlog tasks depend on this task (directly + transitively)
- Higher count = higher priority

**Find available slot:**
- Check all slots (T2, T3, T4, T5)
- A slot is available if no incomplete task has `[SLOT:T<N>]` in its description

**Assign:**
- Pick highest-priority ready task
- Check research trigger: if triggered → move to "2 - Research", else → move to "3 - Build"
- Update task description: `[SLOT:--]` → `[SLOT:T<N>]` and `[STAGE:Backlog]` → `[STAGE:Research]` or `[STAGE:Build]`
- Move task to the correct section

**Respect role preferences:**
- Assign Build/Research tasks preferentially to T2, T3
- Assign Review tasks preferentially to T4
- Assign Test tasks preferentially to T5
- But if preferred slot is busy, use any available slot
- NEVER assign review to the same slot that built the task

### Step 7: System-Level Retrospective

Count completed tasks across ALL projects since last retrospective.

If >= 10 new completed tasks since last retrospective:
1. Read all `[REVIEW:REJECT]`, `[TEST:REJECT]`, `[LINT:FAIL]`, `[INTEGRATE:FAIL]` comments from those tasks
2. Extract common failure patterns (same type of error appearing 3+ times)
3. For each project with failures, read or create `LEARNINGS.md` in project root:

```markdown
## Pattern: <pattern name>
**Frequency:** <N>/<total> tasks
**Fix:** <What builders should do differently>
**Added:** <today's date>
```

4. After writing new patterns, check LEARNINGS.md line count. If >50 lines, remove the oldest patterns (top of file) to keep the file under 50 lines. This prevents the context window bomb on workers.
5. Post comment on Status task: `[RETROSPECTIVE] Analyzed <N> completed tasks. Added <M> patterns to LEARNINGS.md.`

### Step 8: Update Status Dashboard

Update the pinned Status task description:

```
[STATUS] [SPEC_HASH:<current_hash>]
---
## System Status — <timestamp>

Active: <N> tasks (<slot>: <stage> <task_code>, ...)
Completed: <N>/<total> tasks
Total retries: <N> (details: <task_code>: <retry_count>, ...)
Est. cost: ~$<total across all tasks>
Blocked: <N> (<task_code>: waiting on <dep_code>, ...)
Needs Human: <N> (<task_code>: <reason>, ...)
ETA: ~<hours> at current pace (<tasks_remaining> tasks / <tasks_per_hour> velocity)

### Recent Activity
- <timestamp>: <task_code> moved to <stage>
- <timestamp>: <task_code> <event>
```

Also update the Status task description with `[LAST_SWEEP:<timestamp>]`. External monitoring (setup.sh configures this) checks this timestamp. If >30 min stale, an alert fires.

Also post a status update to the project:
- Color: green (all progressing) / yellow (any retries > 2) / red (any in Needs Human)
- Title: "SDLC Sweep - <timestamp>"

### Step 9: Check for Pausing

Check if Status task has `[SYSTEM:PAUSING]` in latest comment:
- If yes: do NOT dispatch new tasks. Only process transitions for already in-progress work.

## Completion

Report sweep summary:
```
SDLC Sweep Complete — <timestamp>
Projects scanned: <N>
Tasks transitioned: <N>
Tasks dispatched: <N>
Tasks in feedback loop: <N>
Spec drift detected: <yes/no>
Dead workers reassigned: <N>
```

Exit. Wait for next crontab invocation.

## Error Handling

- If PM tool API fails mid-sweep → report what was completed, what failed
- If a task's description is malformed (can't parse metadata) → move to Needs Human with note
- If dependency resolution creates a deadlock (all Backlog tasks waiting on each other) → report as critical error
