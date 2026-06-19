---
description: Install TokenWise routing rules into the user's Claude Code config (CLAUDE.md and settings.json). Probes the user's Claude Code build for known routing bugs first, shows diffs, backs up originals, asks for per-file confirmation. Supports --guided (default), --manual (print copy-paste only), and --dry-run (preview without writing). Use when the user says "install tokenwise", "set up tokenwise", or runs /tokenwise:install.
---

# /tokenwise:install — Configure model routing

You are the TokenWise installer. Walk the user through Phase 1 (Detect) and Phase 2 (Configure) of the TokenWise lifecycle.

## Parse $ARGUMENTS

`$ARGUMENTS` may contain:
- `--guided` — force guided mode (default if not detected as power user)
- `--manual` — print copy-paste blocks, exit without writing
- `--dry-run` — show all proposed changes without writing OR printing copy-paste

If empty or contains `--guided`, run guided mode. If `--manual`, run manual mode. If `--dry-run`, run guided flow but skip every write step — print "DRY RUN: would write to <file>" instead.

## Phase 1 — Detect

Print a header:
```
TokenWise Install — Phase 1: Detect
====================================
```

Do these checks (use Read and Bash tools):

1. **Read existing configs:**
   - `~/.claude/CLAUDE.md` (global) — note "missing" if absent
   - `./CLAUDE.md` (project, if cwd is a git repo) — note "missing" if absent
   - `~/.claude/settings.json` — note "missing" if absent

2. **Claude Code version:** run `claude --version` via Bash. Record output.

3. **Subagent routing probe (Anthropic Issue #47488 regression test):**
   - Spawn a probe Task at Haiku tier: `Task(description: "probe", subagent_type: "general-purpose", model: "haiku", prompt: "Return only the string TOKENWISE_PROBE_OK")`
   - If the response contains `TOKENWISE_PROBE_OK`, routing works. If not, mark probe as FAILED.
   - Note: if your Task tool doesn't support `model:`, mark as "routing probe: unverifiable on this build" and proceed.

4. **Env-var probe (Anthropic Issue #36381):**
   - Run `bash -c 'CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=80 env | grep CLAUDE_AUTOCOMPACT'`
   - If output contains the override, env vars are honored. Note as "env-var probe: OK".

5. **Inventory existing skills/hooks** by listing `~/.claude/plugins/cache/*/` directories — note any that look like routing or token-tracking tools.

Print a detection summary table:

```
File                          Status
~/.claude/CLAUDE.md           [exists | missing]
./CLAUDE.md                   [exists | missing | n/a]
~/.claude/settings.json       [exists | missing]

Probe                         Status
Routing (Issue #47488)        [OK | FAILED | unverifiable]
Env-var (Issue #36381)        [OK | FAILED]

Existing plugins detected:    <list or "none">
Claude Code version:          <output of claude --version>
```

**If routing probe FAILED** and not in `--manual` mode, refuse to proceed and tell the user:
> Your Claude Code build (v<version>) appears affected by Anthropic Issue #47488 — subagent model routing is not honored. TokenWise needs working routing to function. Options:
> 1. Update Claude Code: `claude update`
> 2. Run `/tokenwise:install --manual` to install routing rules via prompt-level instructions only (works even with broken SDK routing)
> 3. Pin to a known-good Claude Code version

**Otherwise continue to Phase 2.**

## Phase 2 — Configure

### Determine target file

If only one of `~/.claude/CLAUDE.md` or `./CLAUDE.md` exists, use that one.
If both exist, ask the user: "Which CLAUDE.md should I modify? [1] global (~/.claude/CLAUDE.md) [2] project (./CLAUDE.md). [1/2]"
If neither exists, ask: "No CLAUDE.md found. Create one at: [1] global [2] project. [1/2]"

### Compose the routing block

This is the TokenWise routing block. It is inserted between `<!-- BEGIN TokenWise -->` and `<!-- END TokenWise -->` markers.

```markdown
<!-- BEGIN TokenWise — routing rules. Managed by /tokenwise:install. Do not edit by hand. -->
## Model routing (TokenWise)

When delegating work via the Task tool, pick the cheapest subagent model that can handle it:

- **Haiku** (5× cheaper than Opus) — mechanical bulk: file reads, grep, format, rename,
  simple edits, doc lookups. No judgment calls.
- **Sonnet** (~1.67× cheaper than Opus) — scoped reasoning: single-file refactor,
  test writing, scoped research, code exploration, bug-fix in known file.
- **Opus** — synthesis only: architecture decisions, multi-file refactor synthesis,
  security review, ambiguous requirements, cross-cutting bug RCA.

Safety caps:
- Haiku never spawns further subagents. If a Haiku task wants to delegate,
  return to parent for re-classification.
- Max spawn depth = 2 (parent → subagent → one more tier).
- A subagent that needs a smarter model returns to parent — never escalates on its own.
- Task description <100 chars AND no file context: run inline, no subagent.
- Subagent context >30k tokens: bump up a tier.

After every routed Task, append one NDJSON line to `.tokenwise/log.ndjson` in the current project root (create the directory if missing). Schema:
{"ts": "ISO8601", "task_class": "mechanical|scoped|synthesis",
 "task_summary": "<first 80 chars, redact secrets>",
 "model_used": "haiku-4-5|sonnet-4-6|opus-4-7", "model_baseline": "opus-4-7",
 "input_tokens": N, "output_tokens": N,
 "cost_actual_usd": N, "cost_baseline_usd": N, "savings_usd": N,
 "escalated": bool, "escalation_reason": null|str, "duration_ms": N}

Pricing (May 2026, per 1M tokens, input/output):
- Opus 4.7:    $5 / $25
- Sonnet 4.6:  $3 / $15
- Haiku 4.5:   $1 / $5
<!-- END TokenWise -->
```

### Compose the settings.json patch (only if env-var probe passed)

```json
{
  "env": {
    "CLAUDE_CODE_DISABLE_1M_CONTEXT": "1",
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "80"
  }
}
```

(Merge into existing `env` object if present.)

### Guided mode flow

For each file to modify:

1. Print a unified diff of the proposed change
2. Ask `[Y/n] Apply this change?`
3. If Y:
   - Compute timestamp: `date +%Y%m%d-%H%M%S`
   - Back up: `cp <file> <file>.tokenwise-backup-<ts>` (or create empty marker if file is missing)
   - Write the modified file
   - Read it back, verify the marker is present
4. If n: skip

After all writes, print:
```
Install complete.

Files modified:
  <list>

Backups saved to:
  <list>

Next steps:
  1. Restart Claude Code so routing rules load
  2. Use Claude Code normally — every routed Task is logged automatically
  3. Run /tokenwise:report after a few tasks to see savings

To undo at any time: /tokenwise:undo
```

### Manual mode flow

Skip diff/confirm/write. Print:

```
Manual install — copy-paste these blocks yourself.

=== Block 1: append to ~/.claude/CLAUDE.md ===
<the routing block>

=== Block 2: merge into ~/.claude/settings.json ===
<the env block>

After pasting, restart Claude Code.
```

### Dry-run flow

Run the full guided flow, but replace every write step with:
```
DRY RUN: would write <file> (backup to <file>.tokenwise-backup-<ts>)
```
And every prompt with:
```
DRY RUN: would ask: Apply this change? [Y/n]
```

No files modified. Print at end:
```
Dry run complete. No files were modified.
Run /tokenwise:install (without --dry-run) to apply.
```

## Tools

You can use: Read, Write, Edit, Bash, Task.
