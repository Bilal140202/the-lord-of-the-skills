# WORKFLOW: TASK DISPATCH (ORCHESTRATION)

**Version:** Gold v1.2
**Layer:** 7 — Orchestration Workflow
**Tier:** 2 — Loaded by task
**Primary Mode:** Architect / Orchestrator
**Purpose:** Handles the safe handoff of isolated micro-tasks to separate chat sessions or subagents.

## WHEN TO USE

Use this workflow when you have broken down an implementation plan into micro-tasks, and one or more of those tasks is highly isolated, tedious, or time-consuming.

Instead of doing it all in one long, sequential, context-bloating session, you act as the Orchestrator and dispatch the work.

## THE DISPATCH PROCESS

### 1. Identify Dispatchable Tasks

A task is dispatchable if:

- It is highly isolated (e.g., writing tests for a pure function, styling a simple component, writing documentation).
- It does not require deep knowledge of the entire system architecture.
- Its inputs and expected outputs are clear.

### 2. Prepare the Task Brief

For each task you intend to dispatch, generate a clear, self-contained brief for the user to hand to a new agent session.

### Format

```

## Task Brief: [Task Name]

**Goal:** [What needs to be achieved]
**Inputs:** [Specific files to read or APIs to use]
**Expected Outputs:** [Specific files to write or changes to make]
**Constraints:** [Formatting rules, performance needs, etc.]
**Verification:** [How the new agent should prove it works]
**Context Needed:** [A 1-2 sentence summary of what the agent needs to know]
```

### 3. Handoff

Present the brief(s) to the user. Say:
"Here are the tasks that can be dispatched to separate sessions. Copy each brief into a new chat window. I will wait here for you to bring back the results or confirm completion."

### 4. Re-integration

When the user returns from a sub-session:

1. Review the changes made (using git status/diff or by reading the touched files).
2. Verify the subagent followed the brief and didn't break adjacent behavior.
3. Mark the task as complete in your master checklist.
4. Proceed to the next task.

## WHY WE DO THIS

- **Context Protection:** Complex tasks bloat context windows. Splitting them saves tokens and prevents hallucination.
- **Parallelization:** The user can have multiple agents working on isolated tasks simultaneously.
- **Focus:** The master agent (you) stays focused on the big picture, architecture, and integration.
