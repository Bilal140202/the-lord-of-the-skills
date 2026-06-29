---
name: notion-sync
description: Use when syncing research documents to Notion. Handles Notion synchronization operations including state management and encoding validation.
metadata:
  version: "1.0.0"
---

# Notion Sync Skill

This skill provides standardized procedures for synchronizing research documents to Notion, ensuring data integrity and avoiding common pitfalls.

## When to use this skill

- After completing `/daily-routine` workflow
- After updating ticker analyses
- When user explicitly requests Notion sync
- When troubleshooting sync issues

## Sync Architecture

### State Management
**File**: `.notion_sync_state.json`

**Purpose**: Tracks which files have been synced to avoid duplicates

**Structure**:
```json
{
  "research/daily_briefs/Multi_Target_Analysis_20260117.md": {
    "page_id": "abc123...",
    "last_synced": "2026-01-17T10:30:00Z"
  }
}
```

### Sync Scripts

| Script | Purpose | Use Case |
|--------|---------|----------|
| `ops/sync_full_research.py` | Full repository sync | Initial setup, major updates |
| `scripts/sync_to_notion.py` | Incremental sync | Daily updates |
| `scripts/sync_vault.py` | Vault-specific sync | Knowledge base updates |

## Standard Sync Flow

### 1. Pre-sync Validation
```powershell
# Ensure documents are clean
.bin\python\python.exe ops/lint_reports.py
```

**Why**: Notion API rejects malformed Markdown or encoding issues

### 2. Execute Sync
```powershell
# Full sync (use sparingly)
.bin\python\python.exe ops/sync_full_research.py

# Incremental sync (recommended)
.bin\python\python.exe scripts/sync_to_notion.py
```

### 3. Verify Completion
- Check console output for errors
- Verify `.notion_sync_state.json` updated
- Spot-check Notion pages for correct rendering

## Common Issues & Solutions

### Issue 1: Encoding Errors
**Symptom**: Notion pages show garbled text

**Root cause**: File not UTF-8 encoded

**Solution**:
```powershell
# Fix encoding first
.bin\python\python.exe ops/lint_reports.py

# Then retry sync
.bin\python\python.exe scripts/sync_to_notion.py
```

### Issue 2: Duplicate Pages
**Symptom**: Same report appears multiple times in Notion

**Root cause**: Sync state file corrupted or missing

**Solution**:
```powershell
# Check sync state
cat .notion_sync_state.json

# If corrupted, backup and regenerate
Copy-Item .notion_sync_state.json .notion_sync_state.json.backup
# Then run full sync
```

### Issue 3: Rate Limiting
**Symptom**: `429 Too Many Requests` error

**Root cause**: Notion API rate limits exceeded

**Solution**:
- Wait 60 seconds between sync attempts
- Use incremental sync instead of full sync
- Batch updates when possible

### Issue 4: Authentication Failure
**Symptom**: `401 Unauthorized` error

**Root cause**: Invalid or expired Notion API token

**Solution**:
- Verify `NOTION_API_KEY` environment variable
- Check token permissions in Notion integration settings
- Regenerate token if necessary

## Decision Tree

**Q: Should I run full sync or incremental sync?**
- **Full sync**: Initial setup, major restructuring, state file corrupted
- **Incremental sync**: Daily updates, new reports only

**Q: When should I sync?**
- **Automatic**: After `/daily-routine` completion (Phase 6)
- **Manual**: After major research updates
- **Never**: During development/testing (avoid polluting Notion)

**Q: What if sync fails?**
1. Check error message in console
2. Run `lint_reports.py` to fix encoding
3. Verify Notion API credentials
4. Check `.notion_sync_state.json` integrity
5. Retry with incremental sync first
6. If persistent, run full sync as last resort

## Best Practices

### 1. Validate Before Sync
Always run quality checks before syncing:
```powershell
.bin\python\python.exe ops/lint_reports.py
```

### 2. Use Incremental Sync
Prefer incremental over full sync to:
- Reduce API calls
- Avoid rate limiting
- Faster execution

### 3. Monitor Sync State
Periodically check `.notion_sync_state.json`:
- Verify file paths are correct
- Check for orphaned entries
- Backup before major operations

### 4. Respect Rate Limits
- Wait 60s between sync attempts
- Don't run multiple syncs in parallel
- Use batch operations when available

### 5. Handle Failures Gracefully
- Log errors for debugging
- Don't retry indefinitely
- Notify user of persistent failures

## Integration with Workflows

### /daily-routine
- **Phase 6**: Notion Sync
- Automatically syncs daily reports
- Uses incremental sync for efficiency

### /sync-research
- Dedicated sync workflow
- Allows manual trigger
- Supports both full and incremental modes

## Troubleshooting Guide

### Diagnostic Script
```powershell
.bin\python\python.exe ops/diagnose_notion.py
```

**What it checks**:
- API credentials validity
- Sync state file integrity
- Network connectivity
- Recent sync history

### Manual Verification
1. Open Notion workspace
2. Navigate to Research Hub
3. Check latest synced pages
4. Verify content rendering
5. Confirm timestamps match

### Recovery Procedures

**Scenario 1: Sync state corrupted**
```powershell
# Backup current state
Copy-Item .notion_sync_state.json .notion_sync_state.json.backup

# Clear state (forces full resync)
Remove-Item .notion_sync_state.json

# Run full sync
.bin\python\python.exe ops/sync_full_research.py
```

**Scenario 2: Partial sync failure**
```powershell
# Identify failed files from error log
# Manually fix those files
# Retry incremental sync
.bin\python\python.exe scripts/sync_to_notion.py
```
