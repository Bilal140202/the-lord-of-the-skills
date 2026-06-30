---
description: Full autonomous execution mode - ultrawork
---

# /ultrawork (or /ulw)

## What It Does

Activates **full autonomous mode** with:
- Parallel agent execution
- Background task processing
- Deep code exploration
- Relentless task completion (Ralph Loop)
- Auto-delegation

## Usage

```
/ultrawork migrate the database to PostgreSQL
/ulw add user authentication with JWT
ralph ulw: refactor the payment system
```

## What Happens

1. **Task Analysis**: Sisyphus analyzes the request
2. **Planning**: Prometheus creates execution plan
3. **Parallel Execution**: Multiple agents work simultaneously
4. **Background Tasks**: Long-running tasks don't block
5. **Ralph Loop**: Ensures all TODOs are completed
6. **Auto-Commit**: Git Master commits atomically

## Example Flow

**User**: `/ulw build a REST API for user management`

**System**:
```
[Sisyphus] Analyzing request...
[Sisyphus] Delegating to Prometheus for planning

[Prometheus] Plan created:
  Stage 1: Oracle - Design API architecture
  Stage 2: CodeSmith - Implement endpoints
  Stage 3: Tester - Write tests
  Stage 4: SecurityGuard - Security audit
  Stage 5: Scribe - API documentation

[Parallel Execution]
  → Oracle (designing...)
  → [COMPLETE] Architecture ready

  → CodeSmith (implementing...)
  → SecurityGuard (auditing in background...)
  → [COMPLETE] 5 endpoints implemented

  → Tester (testing...)
  → [COMPLETE] 15 tests passing

[Ralph Loop] Checking for incomplete tasks...
  → Found TODO in UserController
  → CodeSmith fixing...
  → [COMPLETE] All TODOs resolved

[Git Master] Creating atomic commits...
  ✓ feat(api): add user CRUD endpoints
  ✓ test(api): add endpoint tests
  ✓ docs(api): add API documentation

[Sisyphus] Task complete! 🎉
```

## Differences from Normal Mode

| Feature | Normal | Ultrawork |
|---------|--------|-----------|
| Agent Execution | Sequential | Parallel |
| Task Completion | Manual check | Ralph Loop |
| Code Review | Manual | Automatic |
| Git Commits | Manual | Atomic auto-commits |
| Documentation | On request | Automatic |

## Magic Combinations

```
ralph ulw: <task>     # Ralph Loop + Ultrawork
ralplan: <task>       # Ralph + Planning mode
plan ulw: <task>      # Planning + Ultrawork
autopilot ulw: <task> # Full autonomous
```

## When to Use

✅ **Use ultrawork when:**
- Complex multi-step tasks
- Time-sensitive deliverables
- Want hands-off experience
- Need parallel execution

❌ **Don't use for:**
- Learning/exploration
- Highly experimental changes
- When you want full control

---

*"Work smarter, not harder."*
