---
name: vedix-slide-presenter
description: Generates Beamer PDF + python-pptx editable slide deck + speaker notes from a compiled manuscript. Vendored from AI-Research-SKILLs presenting-conference-talks. Runs after Phase 7 (reviewer accepts).
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

# Slide Presenter

Generate `manuscript-slides.pdf` (Beamer) + `manuscript-slides.pptx` (python-pptx) + speaker notes from a compiled manuscript.

## Inputs

- `<input name="manuscript_pdf">` — path to compiled `manuscript.pdf`
- `<input name="manuscript_tex">` — path to source LaTeX
- `<input name="figures_dir">` — path to figures/

## Steps

1. Read the manuscript LaTeX to identify abstract, key results, conclusions.
2. Generate a 12-slide Beamer outline:
   - Title slide
   - Motivation
   - Related Work
   - Methodology (1–2 slides)
   - Experimental setup
   - Results (3–4 slides; one per main finding)
   - Discussion
   - Limitations
   - Future work
   - Q&A
3. Write `<output_dir>/manuscript-slides.tex`. Compile via `pdflatex` ×2.
4. Generate `<output_dir>/manuscript-slides.pptx` via `python-pptx` with the same content + speaker notes per slide.

## Output

```
<output name="paths">
{
  "pdf": "<output_dir>/manuscript-slides.pdf",
  "pptx": "<output_dir>/manuscript-slides.pptx"
}
</output>
```
