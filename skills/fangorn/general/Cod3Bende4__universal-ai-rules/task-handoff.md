# TASK-HANDOFF.md
# PURPOSE: How to preserve and restore context between AI sessions without losing information
# LOAD WHEN: Ending a session, starting a continuation session, or switching between tasks

---

## Session End: Saving Context

At the END of every session, create or update a handoff document:

### Handoff Document Location
- File: `dev-log.md` in the project root
- Format: Append a new entry — never overwrite previous entries
- If `dev-log.md` doesn't exist, create it

### Handoff Entry Template
```markdown
---
## Session: [date] [time]
### Task
[One-sentence description of what was worked on]

### Completed
- [x] [Specific thing completed 1]
- [x] [Specific thing completed 2]
- [x] [Specific thing completed 3]

### In Progress
- [ ] [Thing started but not finished 1]
  - Current state: [describe exactly where you stopped]
  - Next step: [the exact next action to take]
- [ ] [Thing started but not finished 2]
  - Current state: [describe exactly where you stopped]
  - Next step: [the exact next action to take]

### Not Started (Planned)
- [ ] [Thing that was planned but not reached]

### Decisions Made
- [ADR or decision description] — [reason]

### Known Issues
- [Issue 1] — [impact and workaround if any]

### Files Changed
- `path/to/file1.ts` — [what changed and why]
- `path/to/file2.ts` — [what changed and why]

### Environment / Setup Notes
- [Any environment changes, new dependencies, config updates]

### Blockers
- [Anything blocking progress — needs user input, external dependency, etc.]
---
```

### Rules for Session End
- [ ] Always create a handoff entry — even for short sessions
- [ ] Be specific about "where you stopped" — file, line, function, state
- [ ] List exact files changed — not "some files in the auth module"
- [ ] Document any decisions, even small ones — future you doesn't know why
- [ ] Note any environment changes — new deps, config changes, DB migrations
- [ ] Commit the dev-log.md — it's part of the project history

---

## Session Start: Restoring Context

### Step 1: Read the Handoff Document
- [ ] Read the latest entry in `dev-log.md` — understand what was done last
- [ ] Check all "In Progress" items — these are the immediate priorities
- [ ] Check "Blockers" — address or ask about them before continuing
- [ ] Check "Known Issues" — don't reintroduce fixed issues

### Step 2: Verify the State
- [ ] Run `git status` — see uncommitted changes
- [ ] Run `git log --oneline -5` — see recent commits
- [ ] Run `git diff --stat` — see what changed but isn't committed
- [ ] Run the test suite — verify current state is working
- [ ] Verify the app runs locally — `npm run dev` or equivalent

### Step 3: Confirm with the User
```
📋 Picking up from last session ([date]):

Last completed: [brief summary]
In progress: [list from handoff]
Blockers: [list from handoff]

I plan to continue with: [next task from handoff]
Is that correct, or would you like to work on something else?
```

### Step 4: Resume Work
- [ ] Start with the exact "Next step" from the handoff — don't restart
- [ ] Verify any partially completed work — don't duplicate or overwrite
- [ ] Load the appropriate rule files — based on the task type

---

## Multi-Task Context Switching

When switching between tasks within a session:

### Before Switching
- [ ] Document current task state in dev-log.md — where you stopped, what's next
- [ ] Commit any work in progress — or stash with a descriptive message
- [ ] Note which rule files were loaded — for the current task

### After Switching
- [ ] Load rule files for the new task — via MASTER.md
- [ ] Read any existing context for the new task — from dev-log.md
- [ ] Confirm the new task's scope with the user — don't assume
- [ ] Create a clear boundary in dev-log.md — separate tasks visually

---

## Cross-Editor State Transfer

If the user is switching from one AI Editor (like Claude Code) to another (like Cursor, Windsurf, or Antigravity):
- [ ] Export the complete current mental model using the Handoff Entry Template to `dev-log.md`.
- [ ] Explicitly state: "I have saved the session state to `dev-log.md`. You can open your other editor and instruct the AI to read the latest entry to instantly resume."

---

## Long-Running Feature Handoff

For features spanning multiple sessions:

### Feature Tracking Template
```markdown
## Feature: [Feature Name]
### Status: [Not Started | In Progress | Review | Done]
### Started: [date]
### Estimated Sessions: [number]

### Sub-tasks
- [x] Task 1 — completed [date]
- [/] Task 2 — in progress
  - Sub-task 2a ✅
  - Sub-task 2b — working on this
  - Sub-task 2c — not started
- [ ] Task 3 — not started
- [ ] Task 4 — not started

### Architecture/Design Decisions
- [Decision 1] — [rationale]
- [Decision 2] — [rationale]

### Test Coverage
- [What has tests] ✅
- [What needs tests] ⚠️

### Integration Points
- [Other features/modules this interacts with]
```

---

## Handoff Quality Rules

- [ ] Handoff document is understandable by a different AI model — not just the one that wrote it
- [ ] No abbreviations without explanation — spell it out
- [ ] File paths are absolute or relative to project root — no ambiguity
- [ ] Code state is described, not assumed — "the function exists but has no error handling" is better than "partially done"
- [ ] Next steps are actionable — "add validation to createUser in UserService.ts" not "finish the feature"
- [ ] Blockers include the question to ask the user — not just "needs input"

⚠️ WARNING: A vague handoff wastes the first 30 minutes of the next session figuring out where things stand. Be specific.

---

## 🛑 STOP: Handoff Gate

Before ending a session:

1. [ ] Has dev-log.md been updated with the handoff entry?
2. [ ] Are all "In Progress" items described with current state and next step?
3. [ ] Are all files changed listed with what was changed?
4. [ ] Are all decisions documented with rationale?
5. [ ] Are all blockers clearly described with specific questions?
6. [ ] Is the work committed (or stashed with a descriptive message)?
7. [ ] Can a new AI model read this handoff and continue without asking "what were you doing?"
