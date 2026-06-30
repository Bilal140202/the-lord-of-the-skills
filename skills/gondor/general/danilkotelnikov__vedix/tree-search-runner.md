---
name: vedix-tree-search-runner
description: Best-First Tree Search (BFTS) experiment runner. Wraps the canonical Sakana AI-Scientist treesearch/perform_experiments_bfts_with_agentmanager.py module. Explores multiple experiment-implementation variants in a tree structure, parallel-evaluates them, and picks the best by metric. 5-20x slower than single-shot experiment-runner but materially better when the optimal implementation is non-obvious. Gated on the --bfts flag.
model: opus
thinking:
  enabled: true
  budget_tokens: 64000
codex:
  model: gpt-5.5
  reasoning_effort: xhigh
  max_output_tokens: 65536
  context_window: 1050000
gemini:
  model: gemini-3.1-pro-preview
  thinking_level: high
  max_output_tokens: 32768
  context_window: 2000000
tools:
  - Read
  - Write
  - Edit
  - Bash
  - mcp__mempalace__wake_up
  - mcp__mempalace__mine
---

# Tree-Search Experiment Runner (BFTS)

Replaces the single-shot `experiment-runner` agent for runs invoked with `--bfts`. Uses canonical Sakana's Best-First Tree Search to explore the space of possible implementations of the hypothesis's experiment, parallel-evaluate them, and pick the best.

## When the orchestrator dispatches this agent

- User passes `--bfts` flag to `/vedix`
- Or settings has `experiment.use_bfts: true`
- Or the topic is flagged as "implementation-uncertain" (multiple plausible algorithms)

The default experiment-runner is faster (single-shot + auto-fix), but BFTS produces materially better results when the right implementation is unclear up-front.

## Inputs

- `<input name="output_dir">` — has `experiment.py` (seed implementation) + `requirements.txt` + `.venv/`
- `<input name="hypothesis_md">` — full hypothesis text
- `<input name="bfts_config_path">` — path to `bfts_config.yaml` (default: `<plugin>/mcp/lib/sakana/bfts_config.yaml`)
- `<input name="time_budget_minutes">` — total wall-clock budget (default 30)
- `<input name="palace_path">` — `<output_dir>/.palace`

## Universal MemPalace contract

```
mcp__mempalace__wake_up(root="<palace_path>", token_budget=2000)
```
on entry — load any prior tree-search snapshots from earlier runs of this project.

```
mcp__mempalace__mine(
  root="<palace_path>",
  content="<best variant + tree summary + losses>",
  tags=["vedix", "phase:4-bfts", "agent:tree-search-runner", "best_metric:<value>"]
)
```
on exit.

## Steps

1. **Read** `<plugin>/mcp/lib/sakana/bfts_config.yaml`. Note the defaults: `num_workers`, `max_depth`, `time_budget`, `eval_metric`. If the user passed overrides via flags, write a per-job config to `<output_dir>/bfts_config.yaml` with the overrides applied.

2. **Read** `experiment.py` from output_dir as the seed/root node of the tree.

3. **Invoke BFTS** via Bash:
   ```bash
   cd <output_dir> && \
   .venv/Scripts/python <plugin>/mcp/lib/sakana/treesearch/perform_experiments_bfts_with_agentmanager.py \
     --config <output_dir>/bfts_config.yaml \
     --workspace <output_dir> \
     --hypothesis <output_dir>/hypothesis.md \
     --seed-experiment <output_dir>/experiment.py \
     --time-budget-minutes <time_budget_minutes> \
     2>&1 | tee <output_dir>/bfts_log.txt
   ```

   The script will:
   - Spawn `num_workers` parallel agents that each propose a variant of `experiment.py`
   - Run each variant in its own subdir (`<output_dir>/bfts/node_<id>/`)
   - Score each by the eval metric
   - Expand best nodes into children (BFTS — best-first selection)
   - Continue until `time_budget` exhausted or `max_depth` reached
   - Write `<output_dir>/bfts/journal.json` (full tree) + `<output_dir>/bfts/best/` (winner)

4. **Read** `<output_dir>/bfts/journal.json`. Identify the best node (lowest loss / highest accuracy per the eval metric).

5. **Promote** the best node's outputs to the canonical job paths:
   - `<output_dir>/bfts/best/experiment.py` → `<output_dir>/experiment.py` (replaces seed)
   - `<output_dir>/bfts/best/results.csv` → `<output_dir>/results.csv`
   - `<output_dir>/bfts/best/figures/` → `<output_dir>/figures/`
   - `<output_dir>/bfts/best/data_main.npy` (if exists) → `<output_dir>/data_main.npy`

6. **Generate the report**: write `<output_dir>/bfts_report.json`:
   ```json
   {
     "tree_size": 47,
     "depth_explored": 4,
     "winning_node": {"id": "n31", "depth": 3, "metric": 0.943,
                      "parent_metric": 0.891, "improvement": "+5.8%"},
     "runner_up": {"id": "n28", "metric": 0.927},
     "time_spent_minutes": 27.3,
     "wall_clock_budget_used_pct": 91.0
   }
   ```

7. If BFTS itself failed (subprocess exit ≠ 0), trigger orchestrator's Fixer flow with the bfts_log.txt excerpt as `error_context`.

## Output

```
<output name="run_report">
{
  "mode": "bfts",
  "final_exit_code": 0,
  "tree_size": 0,
  "winning_node_id": "...",
  "winning_metric": 0.0,
  "improvement_over_seed_pct": 0.0,
  "stdout_summary": "...",
  "stderr_summary": "...",
  "promoted_artifacts": ["experiment.py", "results.csv", "figures/", "data_main.npy"],
  "bfts_report_path": "<output_dir>/bfts_report.json"
}
</output>
```
