# mcp-multi-agents

Shared context MCP server for multi-IDE continuity. Eliminates cold-start when switching between VS Code + Claude Code and Antigravity (Gemini IDE).

## What It Does

Both IDEs connect to two MCP servers simultaneously:
1. **claude-mem** (existing) — persistent memory observations at `~/.claude-mem/claude-mem.db`
2. **mcp-multi-agents** (this project) — handoff checkpoints, CLAUDE.md injection, task persistence

## MCP Tools

| Tool | Purpose |
|------|---------|
| `session_start` | Call at session start — returns handoff + recent memory + tasks + CLAUDE.md |
| `handoff_save` | Checkpoint state before switching IDEs |
| `handoff_load` | Restore last checkpoint in new IDE |
| `read_project_context` | Read all CLAUDE.md files for a project path |
| `list_tasks` | List persistent tasks for a project |
| `create_task` | Create a task (persists across IDEs) |
| `update_task` | Update task title/description/status |

## Storage

- Handoffs: `~/.mcp-agents/handoffs.json` + claude-mem observation
- Tasks: `~/.mcp-agents/tasks.json`
- Memory: `~/.claude-mem/claude-mem.db` (claude-mem, shared)

## Build & Run

```bash
npm install
npm run build       # compiles src/ → dist/
node dist/index.js  # start server (stdio MCP)
```

## IDE Setup

**VS Code + Claude Code:** `.mcp.json` in project root auto-registers the server.

**Antigravity:** Add entries from `antigravity-mcp.json` to Antigravity's MCP config settings.

## Session Workflow

```
Start new session in any IDE:
  → call session_start({ project_path: "/home/konsing/myproject" })
  → receive: last handoff + recent memory + tasks + CLAUDE.md

Before switching IDEs:
  → call handoff_save({ project_path, current_task, next_steps, ... })
  → state is checkpointed and immediately available in the new IDE
```
