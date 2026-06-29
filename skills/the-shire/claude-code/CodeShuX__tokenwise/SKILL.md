---
description: Restore TokenWise config backups. Lists all .tokenwise-backup-* files found, lets the user pick one to restore in place. Use when the user wants to roll back TokenWise's changes to CLAUDE.md or settings.json, or runs /tokenwise:undo.
---

# /tokenwise:undo — Restore from backup

Find TokenWise backups and restore one.

## Steps

1. **Find backups** with Bash:
   ```bash
   find ~/.claude -maxdepth 3 -name "*.tokenwise-backup-*" 2>/dev/null
   find . -maxdepth 3 -name "*.tokenwise-backup-*" 2>/dev/null
   ```

2. **If none found:**
   ```
   No TokenWise backups found.

   Backups are created automatically by /tokenwise:install before any file modification.
   If you've never run /tokenwise:install, there's nothing to undo.

   If you removed the backups manually, you'll need to restore from version control or recreate config by hand.
   ```

3. **If found, print a numbered list:**
   ```
   TokenWise backups found:

     1. ~/.claude/CLAUDE.md.tokenwise-backup-20260511-143218
        (target: ~/.claude/CLAUDE.md, created <relative time>)
     2. ~/.claude/settings.json.tokenwise-backup-20260511-143219
        (target: ~/.claude/settings.json, created <relative time>)

   Restore which? (1-N, or 'all', or 'cancel'):
   ```

4. **Parse user response:**
   - Single number → restore that one
   - `all` → restore all backups
   - `cancel` (or empty) → exit with `No changes made.`

5. **For each backup to restore:**
   - Derive target path: strip the `.tokenwise-backup-<ts>` suffix
   - Confirm: `Restore <target> from <backup>? This will overwrite <target>. [Y/n]`
   - If Y:
     - Read current target file (if exists), back it up to `<target>.tokenwise-pre-undo-<ts>` (so undo is reversible)
     - Copy backup over target: `cp <backup> <target>`
     - Verify by reading target — confirm content matches backup
   - If n: skip

6. **Optionally delete the consumed backup:**
   `Delete the backup file <backup> now that it has been restored? [Y/n]`

7. **Print summary:**
   ```
   Undo complete.

   Restored:
     <list>

   Pre-undo backups (in case you want to redo):
     <list>
   ```

8. **Remind user:** "Restart Claude Code so the original CLAUDE.md / settings.json take effect."

## Edge cases

- **Multiple backups for the same target file:** the user should pick which one. Print them sorted by timestamp descending (newest first).
- **Backup file is empty:** warn before restoring (`Backup is empty. Restoring will leave <target> empty. Continue?`).
- **Target file no longer exists:** that's fine — restore creates it.

## Tools

Read, Write, Bash.
