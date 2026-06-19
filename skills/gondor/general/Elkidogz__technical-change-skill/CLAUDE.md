# TC Skill

Technical Change (TC) tracking skill for Claude Code. Produces structured JSON records
with accessible HTML output so AI sessions can resume seamlessly when previous sessions expire.

**Published skill** — see `SKILL.md` for the full specification, commands, and usage.

## Key Files
- `SKILL.md` — Main skill specification (commands, schemas, workflows)
- `README.md` — Public documentation
- `schemas/` — JSON Schema definitions (`tc_record.schema.json`, `tc_registry.schema.json`, etc.)
- `generators/` — Python HTML generators (`generate_tc_html.py`, `generate_dashboard.py`, `generate_retro_tcs.py`)
- `validators/validate_tc.py` — Schema validation + state machine enforcement
- `templates/` — HTML templates (`tc_record_template.html`, `tc_dashboard_template.html`, `tc_styles.css`)
- `init/` — CLAUDE.md snippet + settings template for `/tc init`
- `examples/` — Reference records + generated HTML

## Hard Rules
1. **Python stdlib only** — zero external dependencies in generators/validators
2. **CSS-only interactivity** — no JavaScript in generated HTML (CSS `:checked` filters, conic-gradient gauges)
3. **Self-contained HTML** — all CSS inlined, works from `file://` URLs
4. **WCAG AA+ accessibility** — user has low vision; use rem-based fonts, 13.2:1+ contrast, dark theme, semantic HTML, skip links
5. **State machine enforced** — validator rejects invalid status transitions
6. **Append-only revision history** — never modify past revision entries

## Version
v1.0.0 — MIT Licensed. Author: Elkidogz.

## Accessibility Requirement
User has low vision. ALL generated HTML must:
- Use rem-based typography (scales with browser font size)
- Meet WCAG AA+ contrast ratios (minimum 4.5:1 for body, 3:1 for large text)
- Default to dark theme (easier on eyes)
- Include semantic HTML with ARIA labels and skip links
- Include a print stylesheet
