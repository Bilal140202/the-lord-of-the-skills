---
description: Aggregate TokenWise routing data over a time window (default: last 7 days). Shows trend, top task classes, and cumulative savings. Use when the user asks "show me my weekly/monthly savings", "how am I doing on tokenwise", or runs /tokenwise:summary.
---

# /tokenwise:summary — Multi-session trend report

Aggregate `.tokenwise/log.ndjson` over a time window.

## Parse $ARGUMENTS

- `--week` (default) — last 7 days
- `--month` — last 30 days
- `--all` — entire log
- `--days <N>` — last N days
- `--out <path>` — write the report to a markdown file instead of stdout
- `--json` — output JSON instead of text

## Steps

1. **Read** `./.tokenwise/log.ndjson` (or the path the user provides)

2. **Filter** entries to the time window:
   - Compute cutoff: `now - <days>*86400`
   - Keep entries where `ts > cutoff`

3. **Aggregate:**
   - **Total:** sessions (unique session_id), tasks, total cost, baseline cost, savings
   - **Per model:** task count, cost, % of total
   - **Per task_class:** task count, avg cost, dominant model
   - **Trend** (only for `--week` or `--days <≤14>`): per-day cost + savings bar chart in plain text

4. **Print:**

```
TokenWise Summary — last <N> days
==================================

Sessions:        <count>
Tasks routed:    <count>
Total spent:     $<total>
Baseline:        $<baseline>
Savings:         $<savings> (<pct>%)

Per model:
  Haiku    <count> tasks  $<cost>  (<pct>%)
  Sonnet   <count> tasks  $<cost>  (<pct>%)
  Opus     <count> tasks  $<cost>  (<pct>%)

Top task classes:
  <class>          <count> tasks   avg cost $<avg>   model: <dominant>
  ...

Daily trend (cost):
  Mon  ███████░░░ $4.21
  Tue  ███░░░░░░░ $1.82
  Wed  ████████░░ $5.04
  ...
```

5. **If `--out <path>`** was provided, write the markdown version of the report to that path. Use a proper markdown table for the trend section.

6. **If `--json`**, dump the aggregated data structure as pretty-printed JSON.

## Notes on small log files

- If <2 sessions in the window: print the report but add `Note: too few sessions for meaningful trend data.`
- If log file is empty/missing: print the same "No TokenWise log found" message that `/tokenwise:report` uses.

## Tools

Read, Bash (for jq aggregation if helpful), Write (for `--out`).
