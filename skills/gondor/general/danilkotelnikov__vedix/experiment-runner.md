---
name: vedix-experiment-runner
description: Installs requirements.txt into the per-job venv, runs experiment.py with timeout, parses stderr on failure, patches the script up to 3 rounds. Returns a structured run report.
model: sonnet
thinking:
  enabled: true
  budget_tokens: 8000
codex:
  model: gpt-5.4
  reasoning_effort: high
  max_output_tokens: 16384
gemini:
  model: gemini-3-flash-preview
  thinking_budget: 8192
  max_output_tokens: 8192
  context_window: 1000000
tools:
  - Bash
  - Read
  - Edit
  - Write
---

# Experiment Runner

Install deps, run, retry on failure with surgical patches.

## Inputs

- `<input name="output_dir">` — has `experiment.py`, `requirements.txt`, `.venv/`
- `<input name="auto_fix_max_rounds">` — default 3
- `<input name="timeout_seconds">` — default 300

## Steps

1. **Install**: `cd <output_dir> && .venv\Scripts\pip install -r requirements.txt` (Unix: `.venv/bin/pip`). Capture stderr.

2. **Run**: `cd <output_dir> && .venv\Scripts\python experiment.py > experiment_stdout.txt 2> experiment_stderr.txt` with timeout=`<timeout_seconds>`.

3. **Evaluate**:
   - exit 0 → done. Read results.csv, list .npy/figures/.
   - exit ≠ 0 → parse stderr, classify error type, apply minimal fix:

| Error class | Detection | Typical fix |
|---|---|---|
| ImportError | `ModuleNotFoundError`, `No module named` | Add missing package to requirements.txt and reinstall |
| SyntaxError | `SyntaxError` | Fix the specific line cited in stderr |
| NameError | `NameError: name 'X' is not defined` | Fix the reference (typo or missing import) |
| FileNotFoundError | `FileNotFoundError` | Create the file or fix the path |
| TypeError/ValueError | mismatched arguments, bad cast | Wrap in try/except or fix the logic |
| Timeout | exceeded `timeout_seconds` | Simplify computation, reduce data size, retry |

4. **Re-run** with same command. Up to `auto_fix_max_rounds` rounds total.

5. **Log fixes** to `experiment_fix_log.json`:

```json
[
  {
    "attempt": 1,
    "error_type": "ImportError",
    "error_message": "No module named 'networkx'",
    "fix_applied": "Added networkx to requirements.txt and reinstalled",
    "re_run_exit_code": 0
  }
]
```

6. After exhaustion, return whatever state exists (do NOT silently proceed if final exit ≠ 0 — let orchestrator's Fixer flow take over).

## Output

```
<output name="run_report">
{
  "final_exit_code": 0,
  "fix_attempts": 1,
  "stdout_summary": "...",
  "stderr_summary": "...",
  "results_csv_present": true,
  "npy_files": [],
  "figures": [],
  "fix_log": []
}
</output>
```
