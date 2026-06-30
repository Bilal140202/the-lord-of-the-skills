---
name: vedix-plotter
description: "Generates publication-grade figures via 3-cycle iterative refinement. Two output paths: matplotlib/seaborn scripting and LaTeX-native TikZ/pgfplots. Per-cycle artifacts in figures_draft1/, figures_draft2/, figures_final/. Auto-applies Okabe-Ito palette and journal-specific rcParams. Uses VLM critique on a 10-point rubric for Cycle 2."
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
  - Read
  - Write
  - Bash
  - mcp__mempalace__wake_up
  - mcp__mempalace__mine
---

# Plotter

Iterative publication-grade figure generation. Three cycles, each independently re-runnable.

## Inputs

- `<input name="output_dir">` — job output directory containing `results.csv` and any `*.npy` files
- `<input name="article_type">` — `experimental` | `review` | `benchmark`
- `<input name="journal_style">` — `nature` | `cell` | `ieee` | `springer` | `auto`
- `<input name="mode">` — `scripting` (matplotlib) | `latex_native` (TikZ/pgfplots) | `both`
- `<input name="cycle">` — `1` | `2` | `3` | `all`
- `<input name="figure_specs">` — JSON list of `{figure_id, kind, x, y, title, facets}`

## Cycle 1 — Inspect & Draft

For each spec:
1. Sniff the schema of `results.csv` — column dtypes, row count, missing %, ranges.
2. Justify the chosen plot kind in one sentence (e.g. "violin over bar because n=847 and Shapiro-Wilk rejects normality at p<0.001").
3. Render a draft PNG at 2× target DPI (high enough to evaluate legibility, not final).
4. Write `figures_draft1/<id>.png` and `figures_draft1/manifest.json`.

Article-type defaults:
- **review** → bibliometric figures: timeline, taxonomy tree, co-citation cluster heatmap, journal/year heatmap. Booktabs summary tables in LaTeX. Prefer `latex_native` mode for font consistency with manuscript.
- **experimental** → headline result with paired comparison + 95 % bootstrap CI; ablation table; Pareto front.
- **benchmark** → score-vs-method bars (sorted by median, not alphabetically), per-task heatmap, compute-vs-quality scatter, Bradley-Terry Elo bars with symmetric CI.

Mandatory: every figure has axis labels with units, error bars (with description in caption), and a one-sentence rationale logged in `manifest.json`.

## Cycle 2 — VLM Critique

For each figure, ask the VLM (per host: GPT-4o / Claude w/ vision / Gemini) the 10-point rubric:

1. Is the primary message legible at thumbnail size?
2. Is the color palette colorblind-safe (Okabe-Ito or Wong)?
3. Are all axes labeled with units?
4. Are error bars present and described in the caption?
5. Is the legend placement optimal (inside or direct labels)?
6. Is the font size legible at journal column width?
7. Is the figure free of chartjunk (3D/gradient/shadow)?
8. Are statistical annotations (p-values, n, CI) complete?
9. Does the figure match the caption claim?
10. Is the data-ink ratio maximized?

Score each item 1 (fails) to 4 (excellent). Write `figures_draft2/vlm_rubric.json` with per-figure scores + actionable edits. Edit the draft based on VLM feedback. **Run sequentially per figure** — VLM critique accuracy degrades for batch >2 figures per context.

## Cycle 3 — Polish & Export

1. Apply journal-specific `rcParams`: column widths from `JOURNAL_STYLES[journal_style]`, font family (Arial for Nature/Cell, Times for IEEE/Springer), font sizes 7–8 pt for axis labels.
2. Default categorical palette: **Okabe-Ito** (`['#E69F00','#56B4E9','#009E73','#F0E442','#0072B2','#D55E00','#CC79A7','#000000']`). For sequential / heatmaps: **viridis**. For diverging: **PuOr** or **PRGn** (CVD-safe).
3. Export PDF (vector primary) + TIFF 300 dpi (raster backup).
4. Verify font embedding via `pdffonts manuscript.pdf` if available; warn if any font is "no" embedded.
5. Emit `figures_final/figure_metadata.csv` (figure_id, title, kind, journal_style, aggregate_score, mode) and `figures_final/figures.tex` with `\includegraphics` calls at the correct width.

LaTeX-native mode (`mode=latex_native`): for each figure, emit a `figures_final/<id>.tex` with a `\begin{tikzpicture}...\end{tikzpicture}` snippet using `pgfplots` (bar/scatter/heatmap), `pgf-pie` (category breakdown), or pure TikZ (taxonomy/flowchart/architecture). Use `\usetikzlibrary{external}` so each figure compiles to a cached PDF on first run.

## Polish checklist (applied in Cycle 3)

- No 3D / gradient / shadow effects
- Gridlines: light gray (`#CCCCCC`), 0.5 pt, major only; often omit
- Axes: y-axis at zero for bars; non-zero allowed for line trends
- Ticks: inside or none
- Legend: inside plot or direct labeling; avoid floating outside
- Whitespace: 10–15 % padding around content
- Line weight: minimum 1 pt at single-column width
- Marker size: minimum 4 pt at print size

## Output

```
<output name="cycle3_summary">
{
  "cycle": 3,
  "mode": "scripting|latex_native",
  "journal_style": "nature",
  "figures_count": 6,
  "metadata_csv": "figures_final/figure_metadata.csv"
}
</output>
```
