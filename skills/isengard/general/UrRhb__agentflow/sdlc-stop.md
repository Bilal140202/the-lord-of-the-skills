---
name: sdlc-stop
description: Gracefully shut down the AgentFlow pipeline. Lets active workers finish, moves unstarted tasks back to Backlog, posts system paused status.
---

# /sdlc-stop

Gracefully shut down the AgentFlow pipeline.

## Process

### Step 1: Signal pausing

Find the pinned Status task across all `[SDLC]` projects.

Post comment: `[SYSTEM:PAUSING] Graceful shutdown initiated. Active workers will finish their current stage. No new tasks will be dispatched.`

### Step 2: Drain active work

Check all tasks in Research/Build/Review/Test/Integrate stages:

**For tasks with `[BUILD:STARTED]` and recent heartbeat (< 10 min):**
- Leave them alone — the worker is still active
- Report: "Waiting for <task_code> to finish <stage> (worker <slot>)"

**For tasks in Research or Build WITHOUT `[BUILD:STARTED]` (not started yet):**
- Move back to "1 - Backlog"
- Clear slot: `[SLOT:T<N>]` → `[SLOT:--]`
- Reset stage: `[STAGE:X]` → `[STAGE:Backlog]`
- Clean up git worktree if it exists: `git worktree remove feat/<task-code>-<slug> --force`

**For tasks in Review/Test that are waiting (no worker actively processing):**
- Move back to "1 - Backlog"
- Clear slot
- Reset stage
- Clean up git worktree if it exists: `git worktree remove feat/<task-code>-<slug> --force`

### Step 3: Wait for active workers

Report which tasks are still being worked on.

Tell the user: "Active workers are finishing. The system will be fully paused when all active work completes. You can check your Kanban board for current status."

### Step 4: Post paused status

Update the Status task:

```
[SYSTEM:PAUSED]

Graceful shutdown complete — <timestamp>
Tasks returned to Backlog: <N>
Tasks still completing: <N> (if any workers were mid-build)

To resume: run /sdlc-orchestrate
```

### Step 5: Disable crontab (instruct user)

Tell the user:

```
To fully stop the orchestrator, comment out or remove the crontab entry:

  crontab -e
  # Comment out: */15 * * * * /usr/local/bin/claude -p "Run /sdlc-orchestrate" ...

To resume later, uncomment it and run /sdlc-orchestrate once to kick things off.
```

## Notes

- This does NOT kill running Claude Code sessions — it only signals via the Kanban board
- Workers will see the `[SYSTEM:PAUSING]` status on their next board read and should stop picking up new work
- If a worker finishes mid-shutdown, its task will remain in the completed stage (Review-Complete, Test, etc.) and the orchestrator will process it on resume
- `/sdlc-stop` is idempotent — running it twice is harmless
