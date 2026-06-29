---
name: sdlc-health
description: Diagnostic health check for the AgentFlow pipeline. Verifies prerequisites, checks connectivity, reports pipeline status.
---

# /sdlc-health

Run a comprehensive health check on the AgentFlow pipeline. Report status for every subsystem and provide actionable fix instructions for any issues found.

## Execution

Run all checks below in order. Collect results, then print the summary at the end.

## Checks

### 1. Prerequisites

Verify each of these exists and is functional:

- [ ] **Claude Code CLI** -- run `claude --version` to confirm it is accessible
- [ ] **git** -- run `git --version`
- [ ] **gh (GitHub CLI)** -- run `gh --version`, then `gh auth status` to confirm authentication
- [ ] **Node.js** -- run `node --version`
- [ ] **npm** -- run `npm --version`
- [ ] **Conventions file** -- check `~/.claude/sdlc/conventions.md` exists
- [ ] **Skill files** -- check `~/.claude/skills/` contains: `spec-to-asana.md`, `sdlc-worker.md`, `sdlc-orchestrate.md`, `sdlc-stop.md`, `sdlc-health.md`, `sdlc-demo.md`
- [ ] **Prompt files** -- check `~/.claude/sdlc/prompts/` contains: `decompose.md`, `research.md`, `build.md`, `review.md`, `test.md`

For any missing file, report exactly which file is missing and suggest running `./setup.sh` from the agentflow repo.

### 2. PM Tool Connectivity

Test the Asana MCP connection:

- [ ] **MCP responding** -- call the Asana MCP `get_me` tool. If it responds with user info, the connection is live.
- [ ] **Can list projects** -- call `get_projects` and confirm at least one project is returned
- [ ] **Can read tasks** -- pick any project, call `get_tasks` for it
- [ ] **Can post comments** -- do NOT actually post a comment; just confirm the `add_comment` tool is available in the MCP toolset

If MCP is not responding, report: "Asana MCP server not connected. Check your MCP configuration in Claude Code settings."

### 3. Pipeline Status

Search for projects with `[SDLC]` in the name. For each one found:

- Count tasks per stage: Backlog, Research, Build, Review, Test, Integrate, Done, Needs Human
- List active workers: which slots (T2-T5) have assigned tasks, and which tasks
- Find the Status task (pinned task with `[LAST_SWEEP:]` in description)
  - Extract the last sweep timestamp
  - Calculate time since last sweep
  - Classify: HEALTHY (<20 min), WARNING (20-60 min), CRITICAL (>60 min)
- List any tasks in "Needs Human" (task name and code)
- Report total estimated cost across all active tasks (sum `[COST:~$N]` values)
- Check for active merge locks (`[MERGE_LOCK:]` in Status task)
- Check for active sweep locks (`[SWEEP:RUNNING]` in Status task)

If no `[SDLC]` projects found, report: "No AgentFlow projects found. Create one with: /spec-to-asana"

### 4. Crontab Status

- [ ] **Crontab entry** -- run `crontab -l` and check for a line containing `agentflow-cron.sh`
- [ ] **Cron wrapper exists** -- check `~/.claude/sdlc/agentflow-cron.sh` exists and is executable
- [ ] **Log file exists** -- check `/tmp/agentflow-orchestrate.log` exists
- [ ] **Recent log entry** -- if log exists, read the last 5 lines. Check if the most recent entry is less than 30 minutes old.
- [ ] **Last entry successful** -- check that the last log entry does NOT contain "ERROR"

If crontab is not configured: "Crontab not set up. Run: ./setup.sh --with-cron"

### 5. Git Status

Run these in the current working directory:

- [ ] **Not on main** -- `git branch --show-current` should NOT be `main` or `master` (workers should be on feature branches)
- [ ] **Clean working tree** -- `git status --porcelain` should be empty (uncommitted changes block worktree creation)
- [ ] **Remote configured** -- `git remote get-url origin` should return a valid URL
- [ ] **Remote accessible** -- `git ls-remote --exit-code origin HEAD` should succeed

### 6. LEARNINGS.md Status

If a LEARNINGS.md file exists in the current project:

- Count the number of lines
- If approaching 50 lines: report as INFO
- If over 50 lines: report as WARNING ("LEARNINGS.md is over the 50-line cap. Consider archiving old entries.")

## Output Format

Print a clean summary:

```
AgentFlow Health Check
======================
Prerequisites:  [OK] All 12 checks passed (or [FAIL] Missing: <list>)
PM Tool:        [OK] Connected as <username> (or [FAIL] <error>)
Pipeline:       N project(s), M active tasks, K in Needs Human
Orchestrator:   [OK] Last sweep 5 min ago (or [FAIL] No sweep in 60 min!)
Crontab:        [OK] Configured, last run 12 min ago (or [FAIL] Not set up)
Git:            [OK] Clean, on branch feature/xyz (or [WARN] Uncommitted changes)
LEARNINGS.md:   [OK] 23 lines (or [WARN] 52 lines -- over 50-line cap)
```

Then list any issues, sorted by severity:

```
Issues Found:
  [CRITICAL] No orchestrator sweep in 65 minutes -- check crontab and /tmp/agentflow-orchestrate.log
  [CRITICAL] Asana MCP not responding -- check MCP server configuration
  [WARNING]  2 tasks in Needs Human: APP-003, APP-007
  [WARNING]  GitHub CLI not authenticated -- run: gh auth login
  [INFO]     LEARNINGS.md is 48 lines (approaching 50-line cap)
  [INFO]     No AgentFlow projects found -- create one with /spec-to-asana
```

If zero issues found, print:

```
No issues found. Pipeline is healthy.
```

## Fix Instructions

For every issue reported, include a one-line fix command or instruction:

| Issue | Fix |
|-------|-----|
| Claude CLI not found | Install from https://claude.ai/code |
| git not found | Install git for your platform |
| gh not installed | Install from https://cli.github.com/ |
| gh not authenticated | Run: `gh auth login` |
| Missing skill/prompt files | Run: `cd /path/to/agentflow && ./setup.sh` |
| Asana MCP not responding | Check MCP server config in Claude Code settings |
| No SDLC projects | Run: `/spec-to-asana` with a SPEC.md in your project |
| Crontab not configured | Run: `./setup.sh --with-cron` |
| No recent sweep | Check: `tail -20 /tmp/agentflow-orchestrate.log` |
| Sweep errors in log | Check: `grep ERROR /tmp/agentflow-orchestrate.log \| tail -5` |
| On main branch | Create a feature branch: `git checkout -b feature/your-feature` |
| Uncommitted changes | Commit or stash: `git stash` |
| LEARNINGS.md over cap | Archive old entries to LEARNINGS-archive.md |
