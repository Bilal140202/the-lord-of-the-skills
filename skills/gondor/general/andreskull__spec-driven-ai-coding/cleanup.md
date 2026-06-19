# Cleanup Command

Clean up temporary, investigative, and other files created during feature implementation. **ALWAYS runs in DRY RUN mode by default** - lists files without deleting.

## Safety Requirements

⚠️ **CRITICAL SAFETY RULES:**

1. **MUST default to DRY RUN mode** - lists files that would be deleted without actually deleting
2. **REQUIRES explicit user confirmation** before any deletion (cannot proceed without user approval)
3. Shows file count and total size before deletion
4. Provides option to review individual files before confirming
5. Never runs `rm -rf` or destructive commands without explicit user confirmation

## File Patterns Identified

The cleanup command identifies and can remove:

### Temporary Test Files
- `*_test_temp.py`
- `test_*.tmp`
- `*.test.tmp`

### Investigative Scripts
- `investigate_*.py`
- `debug_*.py`
- `scratch_*.py`
- `explore_*.py`
- `test_*.py` (in root or temp directories)

### Temporary Markdown Files
- `notes.md` (in root)
- `temp.md`
- `scratch.md`
- `TODO.md` (if marked as temporary)

### Backup Files
- `*.bak`
- `*.backup`
- `*~`
- `*.swp`
- `*.swo`

### Log Files
- `*.log` (development logs)
- `debug.log`
- `*.local.log`

## Process

1. **Scan** - Identify files matching patterns
2. **Dry Run** - List all files that would be deleted (DEFAULT)
3. **Review** - Show file count, total size, and file list
4. **Confirm** - Ask for explicit user confirmation
5. **Delete** - Only delete after confirmation

## Configuration

Can be configured with project-specific ignore patterns via `.cleanupignore` file:

```
# .cleanupignore
*.important.log
custom_temp_pattern_*
```

## Usage Examples

```bash
# Dry run (default) - just lists files
/cleanup

# Explicit dry run
/cleanup --dry-run

# Actually delete (requires confirmation)
/cleanup --confirm
```

## Best Practices

- Always review the dry run output first
- Check file sizes before confirming
- Verify important files aren't included
- Use `.cleanupignore` for project-specific patterns
- Commit important work before cleanup
