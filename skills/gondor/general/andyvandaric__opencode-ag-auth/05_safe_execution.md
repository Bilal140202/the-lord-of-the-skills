## 🛡️ Safe Execution Rules

> [!CAUTION]
> **MANDATORY: Minimize risk during execution!**

### Pre-Implementation Checklist

1. ✅ **Run tests BEFORE making changes** (baseline)
2. ✅ **Use dry-run when available** (preview changes)
3. ✅ **Create backup before destructive operations**
4. ✅ **Start with smallest scope** (single file → module → system)
5. ✅ **VERIFY every command result** (never skip verification)

### Command Verification Rule

> [!CAUTION]
> **MANDATORY: After EVERY CLI command, VERIFY the result!**
> - Check output/status matches expected outcome
> - Use `--json` and parse to confirm data changes
> - Never assume success from "no output" - verify explicitly

```powershell
# ❌ WRONG: Execute and move on
flowcrate time log bug-1234 10

# ✅ CORRECT: Execute and verify
flowcrate time log bug-1234 10
flowcrate show bug-1234 --json | ConvertFrom-Json | Select-Object totalTimeMinutes
# Verify: totalTimeMinutes = 10
```

### Dry-Run First Policy

**If command has --dry-run, USE IT FIRST:**

```bash
# ❌ WRONG: Execute directly
flowcrate push-workspace "Main" "Server"

# ✅ CORRECT: Dry-run first, then execute
flowcrate push-workspace "Main" "Server" --dry-run
# Review output, then:
flowcrate push-workspace "Main" "Server"
```

### Test Script Priority

| Change Type | Verification Order |
|-------------|-------------------|
| Any code change | 1. `cargo test --lib` 2. Manual verify |
| DB changes | 1. Backup 2. Dry-run 3. Execute 4. Verify |
| File operations | 1. List files 2. Dry-run 3. Execute |
| Destructive | 1. Backup 2. Dry-run 3. User confirm 4. Execute |

### Rollback Plan

**For every phase, document rollback:**

```markdown
## Rollback Plan
💡 To undo: `flowcrate backup import .flowcrate/backups/push_*.json --mode replace`
```
