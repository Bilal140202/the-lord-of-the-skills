# 🗺 Roadmap — *The Path Ahead*

> *"The road goes ever on and on, down from the door where it began."*

This document tracks the future direction of The Lord of the Skills.

---

## ✅ Completed

### v1.0.0 — *The Fellowship Forms* (2026-06-19)
- [x] Initial compilation: 10,888 artifacts from 102 source repos
- [x] 13 frameworks covered
- [x] LOTR-themed 10-kingdom taxonomy
- [x] Reusable Python crawler (5-phase, resumable)
- [x] PDF master catalog (33 pages)
- [x] 6-sheet Excel index

### v1.1.0 — *The Kingdoms Take Shape* (2026-06-19)
- [x] Restructured: per-kingdom `README.md` for all 10 kingdoms
- [x] Top-level `KINGDOMS.md` index
- [x] URL/git-safe filenames (508 files renamed)

### v1.2.0 — *The Antigravity Frontier* (2026-06-19)
- [x] Added Google Antigravity as the 14th framework (820 files)
- [x] Built `crawler_antigravity.py` focused crawler
- [x] Discovered 689 antigravity repos, cloned 307, extracted 11,697 files
- [x] Total: 18,142 artifacts (+66% from v1.0.0)

### v1.3.0 — *The Polished Kingdom* (2026-06-22)
- [x] Shortened README (under 200 lines, scannable)
- [x] Added comprehensive GitHub badges (stars, forks, CI, license, etc.)
- [x] Generated PDF + folder-structure screenshots
- [x] Added `requirements.txt` + `pyproject.toml` for crawler
- [x] Added GitHub Actions CI/CD workflow (`.github/workflows/ci.yml`)
- [x] Added pytest unit tests for crawler, classifier, dedup
- [x] Created 5 starter issues (good-first-issue labels)
- [x] Added new docs: `QUICKSTART.md`, `FRAMEWORKS.md`, `ROADMAP.md`, `FAQ.md`, `MANIFEST.md`, `DEDUP.md`
- [x] Wrote promotion post for Reddit/HN/Twitter

### v1.4.0 — *The Trustworthy Kingdom* (2026-06-22)
- [x] Fixed GitHub description to match README stats
- [x] Added `SECURITY.md` policy
- [x] Published 4 GitHub Releases (v1.0.0 – v1.3.0)
- [x] Seeded 3 Discussions
- [x] Updated topics (added mcp, prompt-engineering, cursor-rules, antigravity)
- [x] Generated custom social preview image
- [x] Antigravity spotlight in README

### v1.5.0 — *The One Command* (2026-06-29)
- [x] Built `lotr` CLI (detect, match, fetch, place, lotr entry point)
- [x] Generated `skills/index.json` (16,760 skills, 354 canonical)
- [x] 7 subcommands: install, preview, list, search, detect, kingdoms, update
- [x] 43 CLI tests (all passing)

### v1.6.0 — *The Kickoff + PyPI* (2026-06-29)
- [x] `lotr kickoff` mode — multi-kingdom project setup
- [x] Smart auto-detection (install vs kickoff from phrasing)
- [x] PyPI package (`pyproject.toml` + `cli/__init__.py` + entry point)
- [x] `PUBLISHING.md` with twine upload instructions
- [x] 21 new kickoff tests (194 total, all passing)

---

## 🚧 In Progress

### v1.7.0 — *The Searchable Realm* (target: Q3 2026)
- [x] **Publish `lotr-skills` to PyPI** — LIVE at https://pypi.org/project/lotr-skills/
- [ ] **Web search interface** — Streamlit app for browsing/searching skills by keyword, kingdom, framework
- [ ] **Semantic search** — Embeddings-based search using sentence-transformers
- [ ] **Skill preview pane** — Render SKILL.md content in-browser

---

## 📋 Planned

### v1.5.0 — *The Versioned Kingdom* (target: Q4 2026)
- [ ] **Versioned artifacts** — `skills/v1.0/`, `skills/v1.1/` etc. to track changes over time
- [ ] **Diff viewer** — Show what changed between versions
- [ ] **Skill ratings** — Community upvote/downvote on canonical skills

### v1.6.0 — *The Expanding Fellowship* (target: Q4 2026)
- [ ] **5 more frameworks** — Windsurf, Codeium, Devin, Gemini, Copilot Workspace
- [ ] **Multi-language docs** — Translate README to Spanish, French, Japanese, Chinese
- [ ] **Video walkthrough** — 5-minute YouTube demo

### v2.0.0 — *The Living Kingdom* (target: 2027)
- [ ] **REST API** — Programmatic access to skills (GET `/api/skills?kingdom=gondor&framework=claude-code`)
- [ ] **Skill install CLI** — `lotr install <skill-name>` one-command install
- [ ] **MCP server** — Expose skills via Model Context Protocol
- [ ] **Self-improving** — Crawler detects new awesome-lists and adds them automatically
- [ ] **LOTR-themed web UI** — Interactive Middle-earth map of skills

---

## 💡 Ideas (Undated)

- **Skill dependency graph** — Visualize how skills reference each other
- **Skill composition** — Combine multiple skills into a workflow
- **Skill benchmarking** — Auto-test skills against known tasks
- **Skill attribution** — Track which skill was used in which project
- **"Fellowship" teams** — Curated skill bundles for specific use cases (e.g., "The Gondor Fellowship" = all coding skills)
- **LOTR-themed commit messages** — `/quest` command to generate themed commits
- **Discord/Slack bot** — Browse skills from chat

---

## 🤝 How to Contribute to the Roadmap

1. **Suggest a feature** — [Open an issue](https://github.com/Bilal140202/the-lord-of-the-skills/issues/new) with label `enhancement`
2. **Pick an item** — Look for issues labeled `good first issue` or `help wanted`
3. **Submit a PR** — See [`CONTRIBUTING.md`](CONTRIBUTING.md)

The roadmap is a living document — items may be added, removed, or reprioritized based on community feedback.

---

## 📊 Roadmap Progress

| Status | Count |
|:---|---:|
| ✅ Completed | 25 |
| 🚧 In Progress | 3 |
| 📋 Planned | 11 |
| 💡 Ideas | 7 |

---

<div align="center">

*The quest continues — join the Fellowship.*

</div>
