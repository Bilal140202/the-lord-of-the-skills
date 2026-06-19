# SESSION-START.md
# PURPOSE: Step-by-step instructions for what the AI does at the start of every session
# LOAD WHEN: Always — this is the boot sequence for every new AI coding session

---

## Session Start Sequence

Execute these steps IN ORDER at the beginning of every session:

### Step 1: Read Project State
- [ ] **Temporal Awareness**: Explicitly resolve and state today's real-world current date. Do not rely on training cutoff dates for `CHANGELOG.md`, copyright headers, or timestamps.
- [ ] Check if `dev-log.md` or `CHANGELOG.md` exists — read the last 5 entries
- [ ] Check if `docs/roadmap.md` or `TODO.md` exists — understand current priorities
- [ ] Run or review `git log --oneline -10` — see recent changes
- [ ] Check for open PR branches — `git branch -a` to see active work
- [ ] Check for uncommitted changes — `git status` to see work in progress
- [ ] Read `README.md` — understand project setup and conventions

### Step 2: Assess the Project
- [ ] Identify the language(s) and framework(s) — read package.json, requirements.txt, go.mod, etc.
- [ ] Identify the test framework — how to run tests
- [ ] Identify the build system — how to build and run the project
- [ ] Identify the deployment target — where this project runs
- [ ] Note any linters/formatters configured — respect existing code style

### Step 3: Load Relevant Rule Files
Based on what the user says in their FIRST message, load files from MASTER.md:
- [ ] Always load `core/security.md` — non-negotiable
- [ ] Match the user's task to a task type in MASTER.md — load corresponding files
- [ ] If task is unclear, ask the user to clarify before loading — don't guess

### Step 4: Confirm Scope with the User
Before writing ANY code, confirm:
- [ ] What is the specific task? — get a clear, bounded statement
- [ ] What are the acceptance criteria? — how will we know it's done?
- [ ] Are there any constraints? — timeline, tech stack, dependencies
- [ ] What files or modules are affected? — narrow the scope
- [ ] What is NOT in scope? — prevent scope creep

### Step 5: Surface Project State
Present a brief summary to the user:

```
📋 Project Status Summary:
- Last change: [latest commit message and date]
- Active branch: [current branch name]
- Uncommitted changes: [yes/no — list if yes]
- Open items: [from TODO/roadmap, top 3]
- Test status: [last known result if available]

Ready to work on: [description of what the user asked for]
Scope: [what we will and won't do]
```

---

## Greeting Template

Use this as a starting point — adapt to the specific project:

```
👋 Hi! I've reviewed the project state. Here's where we are:

📦 Project: [name] ([framework/language])
🌿 Branch: [current branch]
📝 Last commit: [message] ([date])
⚠️ Uncommitted changes: [none / brief list]

Based on your request, I'll be working on:
✅ [Specific task]
🚫 Not in scope: [explicit exclusions]

Before I start, can you confirm:
1. [Any clarifying question]
2. [Any scope question]
```

---

## File Loading Decision Tree

```
User says "start a new project" or "init" or "scaffold"
→ Load: 01-project-init.md + session-start.md

User says "design" or "architect" or "plan"
→ Load: 03-system-design.md + code-quality.md

User says "database" or "schema" or "migration" or "model"
→ Load: 04-database.md + error-handling.md

User says "API" or "endpoint" or "route" or "REST"
→ Load: 05-api-design.md + error-handling.md + code-quality.md

User says "frontend" or "UI" or "component" or "page" or "React"
→ Load: 06-frontend.md + code-quality.md

User says "backend" or "service" or "server" or "logic"
→ Load: 07-backend.md + code-quality.md + error-handling.md

User says "test" or "spec" or "coverage" or "TDD"
→ Load: 08-testing.md

User says "deploy" or "CI" or "CD" or "pipeline"
→ Load: 09-cicd.md

User says "monitor" or "log" or "alert" or "trace"
→ Load: 10-observability.md + error-handling.md

User says "performance" or "optimize" or "slow" or "cache"
→ Load: 11-performance.md

User says "refactor" or "clean up" or "tech debt" or "upgrade"
→ Load: 12-maintenance.md + code-quality.md

User says "docs" or "document" or "readme" or "onboard"
→ Load: 13-documentation.md

User says "review" or "PR" or "merge" or "commit"
→ Load: review-gate.md + code-quality.md

User says "fix" or "bug" or "error" or "debug" or "broken"
→ Load: error-handling.md + code-quality.md

User says "continue" or "resume" or "pick up where we left off"
→ Load: task-handoff.md + session-start.md
```

✅ DEFAULT: When in doubt, load more files rather than fewer. Context is cheap compared to missing a critical rule.

---

## Session Rules

- [ ] Never start writing code without confirming scope — saves rework
- [ ] Never skip security.md — no exceptions, no matter how trivial the task seems
- [ ] Summarize what you understood before coding — let the user correct misunderstandings
- [ ] If the session is a continuation, check task-handoff.md — don't lose context
- [ ] If the user's task is unclear, ask ONE clarifying question — then proceed
- [ ] **Context Budgeting**: In long sessions spanning multiple tasks, actively summarize your progress and discard irrelevant file context to keep your working memory lean and focused.

⚠️ WARNING: Starting to code without understanding the task is the most expensive mistake. 5 minutes of clarification saves hours of rework.
