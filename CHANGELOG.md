# Changelog

All notable changes to **The Lord of the Skills** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-06-19 — *The Fellowship Forms*

### 🎉 Added
- Initial compilation of **10,888** agentic AI skill/agent/rule files
- Spidered from **102** source GitHub repositories
- Coverage of **13** frameworks:
  - Anthropic Claude Code (`SKILL.md`, `skills/`)
  - Cursor (`.cursorrules`, `.cursor/rules/*.mdc`)
  - Cline (`.clinerules/`, `.cline/`)
  - Roo Code (`.roo/rules/`, `.roo/modes/`)
  - Aider (`CONVENTIONS.md`, `.aider*`)
  - OpenHands (agent configs)
  - SWE-agent (templates)
  - OpenAI Codex (`AGENTS.md`)
  - Continue (`.continue/`)
  - Block Goose (`.goose/`)
  - GitHub Copilot (`.github/copilot-instructions.md`)
  - AutoGen (agent configs)
  - CrewAI (agent configs)
  - LangGraph (agent definitions)
- 10 LOTR-themed kingdoms:
  - ⚔ Gondor (Coding & Software Engineering) — 5,631 artifacts
  - ✦ Rivendell (Research & Knowledge) — 1,521
  - ⚙ Isengard (Agents & Orchestration) — 968
  - ✎ The Shire (Writing & Content) — 712
  - ⛏ Moria (DevOps & Infrastructure) — 703
  - 🐴 Rohan (Testing & Verification) — 450
  - 🌳 Fangorn (Documentation & Memory) — 322
  - ✿ Lothlórien (Data & Analysis) — 305
  - 👁 Mordor (Security & Auditing) — 272
  - 🕸 Mirkwood (Specialized & Niche) — 4
- **1,880** canonical ⭐ clusters via deduplication
- Reusable Python crawler with 5-phase resumable architecture:
  - Phase 1: Clone seed repos
  - Phase 2: BFS expansion from READMEs
  - Phase 3: GitHub Search API expansion
  - Phase 4: Clone all discovered repos
  - Phase 5: Extract skill/agent/rule files
- LOTR-themed classifier with weighted keyword voting
- Deduplication via normalized-title + Jaccard-similarity clustering
- 33-page themed PDF catalog
- 6-sheet Excel index (Artifacts, Kingdoms, Frameworks, Canonical, Stats, About)
- Monthly cron refresh pipeline
- Full aggregate CREDITS.md with all 102 source repos

### 🛠 Tooling
- Python 3.12+
- `requests` for GitHub API
- `git` (depth=1 clones)
- `openpyxl` for Excel generation
- `reportlab` for PDF generation
- `pypdf` for PDF verification

---

## [Unreleased]

### 🚀 Planned
- MCP server — expose skills via Model Context Protocol
- Semantic search — embeddings-based skill matching
- Windsurf framework support (15th framework)
- Self-improving crawler — auto-detect new awesome-lists
- VSCode extension for browsing skills in-editor
- Docker image for one-command refresh

---

## [1.1.0] — 2026-06-19 — *The Kingdoms Take Shape*

### 🏗 Restructured
- **Top-level `KINGDOMS.md`** — Visual map of the 10 kingdoms with artifact/repo/canonical counts and mottos
- **Per-kingdom `README.md`** — Every kingdom (gondor/, rivendell/, moria/, etc.) now has its own README with stats, framework breakdown, directory layout, and usage examples
- **URL/git-safe filenames** — Renamed 508 files that had non-ASCII characters (⭐) or spaces in their names
  - `⭐_SKILL.md` → `canonical__SKILL.md` (canonical prefix preserved, ASCII-safe)
  - Spaces → hyphens
  - All filenames now work in URLs, shell scripts, and git operations across all platforms

### 🐛 Fixed
- Bug in `safe_filename()` that was eating the first letter of canonical filenames (canonical_KILL.md → canonical__SKILL.md) — fixed via `fix_mangled_names.py`

### 📊 Verified
- All 10,888 artifacts preserved (no content lost)
- All crawler pipeline scripts still import and run cleanly
- Per-kingdom canonical counts now accurate:
  - ⚔ Gondor: 33 canonical
  - ⚙ Isengard: 11 canonical
  - ✦ Rivendell: 9 canonical
  - ✎ The Shire: 6 canonical
  - 🌳 Fangorn: 6 canonical
  - ✿ Lothlórien: 5 canonical
  - 👁 Mordor: 5 canonical
  - ⛏ Moria: 4 canonical
  - 🐴 Rohan: 4 canonical
  - 🕸 Mirkwood: 1 canonical
  - **Total: 84 canonical ⭐ representatives**

### 🛠 Added
- `scripts/restructure_repo.py` — Idempotent restructure script (safe to re-run)
- `scripts/fix_mangled_names.py` — One-shot fix for canonical__ filename mangling bug

---

## [1.2.0] — 2026-06-19 — *The Antigravity Frontier*

### 🚀 Added — Antigravity Framework Support
- **New 14th framework**: Google Antigravity IDE skills
- Built dedicated `crawler_antigravity.py` — focused crawler for Antigravity-specific repos
- Discovered **689** antigravity-related GitHub repositories via 30 targeted search queries
- Cloned **307** of them and extracted **11,697** antigravity-tagged files
- **820 files** explicitly tagged as `antigravity` framework (the rest tagged by their original format: claude-code, cursor, etc. but sourced from AG collections)
- Files merged into the existing kingdom tree under `skills/<kingdom>/antigravity/<repo>/`

### 📊 Growth Statistics
| Metric | v1.1.0 | v1.2.0 | Δ |
|:---|---:|---:|---:|
| Total artifacts | 10,888 | 18,142 | **+7,254** (+66%) |
| Source repositories | 102 | 307+ | **+205** |
| Canonical ⭐ clusters | 84 | 357 | **+273** |
| Frameworks | 13 | 14 | **+1** (Antigravity) |
| Kingdom file counts: |
| ⚔ Gondor | 5,631 | 10,141 | +4,510 |
| ✦ Rivendell | 1,521 | 1,776 | +255 |
| ⚙ Isengard | 968 | 1,630 | +662 |
| ✎ The Shire | 712 | 1,272 | +560 |
| ⛏ Moria | 703 | 914 | +211 |
| 🐴 Rohan | 450 | 718 | +268 |
| 🌳 Fangorn | 322 | 708 | +386 |
| ✿ Lothlórien | 305 | 496 | +191 |
| 👁 Mordor | 272 | 406 | +134 |
| 🕸 Mirkwood | 4 | 81 | +77 |

### 🛠 Added
- `scripts/crawler_antigravity.py` — Focused crawler with 30 antigravity-specific search queries
- Antigravity-specific seed list including:
  - `sickn33/antigravity-awesome-skills`
  - `google/antigravity`
  - Plus 687 more discovered via GitHub Search API + BFS

### 🕷 Crawler Details
- **30 search queries** targeting: antigravity skill, agent, rules, mcp, IDE, sdk, python, typescript, subagents, system prompt, tutorial, etc.
- **GitHub Code Search** for files containing "antigravity" (where rate limits allowed)
- **BFS expansion** from antigravity-awesome-skills READMEs
- Files classified into all 10 kingdoms via the same LOTR keyword-vote classifier

### 📁 New Structure
```
skills/
├── gondor/antigravity/         ← NEW: Antigravity-tagged coding skills
├── rivendell/antigravity/      ← NEW: Antigravity research skills
├── isengard/antigravity/       ← NEW: Antigravity agent-orchestration skills
├── moria/antigravity/          ← NEW: Antigravity devops skills
├── ... (all 10 kingdoms now have antigravity/ subdirs)
```

---

## [1.3.0] — 2026-06-22 — *The Polished Kingdom*

### 🎨 Aesthetics & First Impressions
- **Shortened README** from 1,000+ lines to ~200 lines — scannable, with clear CTAs
- **Added 10 GitHub badges** at the top: stars, forks, watchers, license, CI, last commit, contributors, issues, repo size, license
- **Generated screenshots**: PDF preview pages + folder-structure image (stored in `assets/screenshots/`)
- **Added "Why This Repo?" section** to README highlighting USPs (largest collection, LOTR-themed, canonical skills, reusable crawler)
- **Added "Previews" section** with image grid showing PDF catalog and folder structure

### 📚 New Documentation (6 new files)
- `QUICKSTART.md` — 60-second start guide with copy-paste commands for every framework
- `FRAMEWORKS.md` — detailed 14-framework breakdown with detection patterns + how to add new frameworks
- `ROADMAP.md` — prioritized roadmap with completed/in-progress/planned/ideas sections
- `FAQ.md` — 25+ common questions covering usage, crawler, kingdoms, licensing, troubleshooting
- `MANIFEST.md` — full schema documentation for `_manifest.json` with Python/JS/jq examples
- `DEDUP.md` — detailed explanation of canonical dedup algorithm with framework/skill-type priority tables

### 🛠 Technical Robustness
- **Added `crawler/requirements.txt`** — pinned Python dependencies (requests, openpyxl, reportlab, pypdf, Pillow, cairosvg, pytest, etc.)
- **Added `crawler/pyproject.toml`** — modern Python packaging with `lotr-crawl`, `lotr-classify`, `lotr-dedup` CLI entry points
- **Added GitHub Actions CI/CD** (`.github/workflows/ci.yml`):
  - Tests on Python 3.10, 3.11, 3.12
  - Lint with flake8, black, isort
  - pytest with coverage upload to Codecov
  - Markdown link checker
  - Catalog artifact verification
  - Kingdom structure verification
- **Added pytest unit tests** (`tests/`):
  - `test_classify.py` — 30+ tests for kingdom classification, skill types, title/summary extraction
  - `test_dedup.py` — 25+ tests for normalize_title, tokenize, jaccard, canonical_score
  - `test_crawler.py` — 30+ tests for skill file detection, framework detection, seed list sanity, BFS regex
  - `conftest.py` — pytest configuration
  - **130 tests total, all passing**
- **Added `tests/README.md`** — how to run tests, add new tests

### 🤝 Community Engagement
- **Created 5 starter issues** (labeled `good first issue` + `help wanted`):
  1. Add Windsurf IDE support (15th framework)
  2. Add 11th kingdom "The Grey Havens" for dev tools
  3. Fix typos and improve grammar in docs
  4. Add Streamlit web UI for browsing skills
  5. Add embeddings-based semantic search for skills
- **Created 8 GitHub labels**: good first issue, help wanted, enhancement, documentation, crawler, kingdoms, frameworks, LOTR
- **Enabled GitHub Discussions** for longer-form conversations

### 📣 Promotion Materials
- **Added `docs/promotion/PROMOTION_POSTS.md`** with ready-to-post templates for:
  - Reddit (r/MachineLearning, r/artificial)
  - Hacker News (Show HN)
  - Twitter/X (7-tweet thread)
  - LinkedIn
  - Dev.to / Medium (blog post outline)
  - Awesome-list submissions (3 PRs to submit)
- **Promotion checklist** with 11 channels

### 📊 Summary
| Category | Items Added |
|:---|---:|
| New docs | 6 (QUICKSTART, FRAMEWORKS, ROADMAP, FAQ, MANIFEST, DEDUP) |
| Screenshots | 5 (PDF previews + folder structure) |
| GitHub badges | 10 |
| Test files | 4 (test_classify, test_dedup, test_crawler, conftest) |
| Tests passing | 130 |
| CI/CD workflows | 1 (ci.yml with 3 jobs) |
| Starter issues | 5 |
| GitHub labels | 8 |
| Promotion posts | 6 platform templates |
| Python packaging | 2 (requirements.txt, pyproject.toml) |

### 🎯 Impact (Expected)
Based on the critique feedback:
- **+Stars**: Shorter README + badges + screenshots = better first impression
- **+Contributors**: 5 good-first-issues + clear CONTRIBUTING.md = lower barrier
- **+Trust**: CI badge + tests + dependency management = professional appearance
- **+Discoverability**: Promotion posts + awesome-list submissions = wider reach

---

## [1.4.0] — 2026-06-22 — *The Trustworthy Kingdom*

### 🎯 Trust & Credibility Fixes (based on community critique)

#### 📝 Description & Topics Sync
- **Updated GitHub repo description** to match README: 18,142+ artifacts, 14 frameworks, 307+ repos (was stale at 10,888/102/13)
- **Updated GitHub topics** (20 max): added `cursor-rules`, `mcp`, `prompt-engineering`, `rules`, `antigravity`; dropped lower-search-value ones (`agent-framework`, `agents-md`, `compilation`, `roo-code`, `skill-md`)

#### 📦 GitHub Releases (was: 0 → now: 4)
- Published **4 proper GitHub Releases** with full release notes:
  - [v1.0.0 — The Fellowship Forms](https://github.com/Bilal140202/the-lord-of-the-skills/releases/tag/v1.0.0)
  - [v1.1.0 — The Kingdoms Take Shape](https://github.com/Bilal140202/the-lord-of-the-skills/releases/tag/v1.1.0)
  - [v1.2.0 — The Antigravity Frontier](https://github.com/Bilal140202/the-lord-of-the-skills/releases/tag/v1.2.0)
  - [v1.3.0 — The Polished Kingdom](https://github.com/Bilal140202/the-lord-of-the-skills/releases/tag/v1.3.0)
- Releases appear in GitHub search, notifications, and the trending algorithm

#### 💬 Discussions Seeded (was: empty → now: 3 starter threads)
- [#6 Which kingdom do you use most?](https://github.com/Bilal140202/the-lord-of-the-skills/discussions/6) — General
- [#7 Request a new kingdom — what domain are we missing?](https://github.com/Bilal140202/the-lord-of-the-skills/discussions/7) — Ideas
- [#8 Share your workflow](https://github.com/Bilal140202/the-lord-of-the-skills/discussions/8) — Show and tell

#### 🔒 SECURITY.md Added
- Full security policy covering: vulnerability reporting, scope (in/out), IP & redistribution concerns, crawler security properties, user best practices
- Eligible for GitHub's security policy badge

#### 🖼 Social Preview Image Generated
- Created custom 1280×640 social preview at `assets/social/social-preview.png`
- LOTR-themed: dark parchment background, gold ring centerpiece, all 10 kingdoms listed
- **Manual step required**: upload via Settings → Social preview (GitHub has no API for this)

#### ✨ Antigravity Spotlight
- Added dedicated "Spotlight" section to README highlighting that this is the **only major skills catalog covering Google Antigravity**
- Added direct link to [antigravity.google](https://antigravity.google) in FRAMEWORKS.md
- Softened "LARGEST COLLECTION" claim to "A growing, organized collection" — letting the community validate the claim over time

#### 🐛 CONTRIBUTING.md Fix
- Fixed contradiction: instructions now say `canonical__` (not `⭐_`) for canonical prefix, matching DEDUP.md and README
- Updated dev setup to use `pip install -r crawler/requirements.txt` (was: ad-hoc pip install)
- Added `pytest tests/ -v` step

### 📋 Summary
| Item | Before | After |
|:---|:---|:---|
| GitHub Releases | 0 | 4 |
| Discussion threads | 0 | 3 |
| SECURITY.md | ❌ | ✅ |
| Custom social preview | ❌ | ✅ (generated; needs manual upload) |
| Repo description | stale (10,888/102/13) | current (18,142/14/307+) |
| Topics | 20 (missing high-search terms) | 20 (includes mcp, prompt-engineering, cursor-rules) |
| Antigravity visibility | buried in table | headline spotlight section |
| "LARGEST" claim | "largest on GitHub" | "growing, organized collection" |
| CONTRIBUTING.md | contradicted README | consistent (canonical__ everywhere) |

### 🎯 Commit Hygiene Note
This release consolidates all v1.4.0 fixes into a **single commit** (addressing feedback that v1.0→v1.3 looked like an AI mass-dump). Going forward, commits will be spaced out organically as features are developed.

---

## [1.5.0] — 2026-06-29 — *The One Command*

### 🚀 New: `lotr` CLI — Smart Skills Installer

A one-command installer that detects your project's AI agent framework, maps your natural-language task to the right LOTR kingdom, fetches canonical skills, and drops them in the exact right location.

```bash
# One command does everything:
lotr "write unit tests for the API"

# The CLI:
# 1. Detects → cursor + typescript + react
# 2. Maps    → "write unit tests" → rohan (testing)
# 3. Fetches → canonical ⭐ testing skills for cursor
# 4. Places  → .cursor/rules/jest-cursor-rules.mdc, testing-rules.mdc, ...
```

### 🛠 New Files (cli/)
- `cli/lotr.py` — entry point with subcommands: `install`, `preview`, `list`, `search`, `detect`, `kingdoms`, `update`
- `cli/detect.py` — framework + stack detector (10 frameworks, 6 languages, 25+ stack libraries)
- `cli/match.py` — intent → kingdom mapper with weighted keyword voting + compound phrase scoring
- `cli/fetch.py` — GitHub raw downloader with caching + local fallback
- `cli/place.py` — smart per-framework placement (dir mode + append mode for conventions)
- `cli/generate_index.py` — builds `skills/index.json` from the skills tree
- `cli/requirements.txt` — minimal deps (just `requests`)
- `cli/README.md` — full CLI docs with examples + architecture diagram

### 📊 New: `skills/index.json` — Machine-Readable Manifest
- **16,760 skills** indexed with: title, kingdom, frameworks, canonical flag, tags, source_repo, path
- **354 canonical ⭐** skills (deduplicated representatives)
- **7.3 MB** compact JSON
- Queried by the CLI for instant skill lookup — no git clone needed
- Schema documented in `cli/README.md`

### 🎨 Per-Framework Placement
The CLI knows exactly where each framework expects its skills:
- `antigravity` → `.antigravity/skills/`
- `cursor` → `.cursor/rules/`
- `claude-code` → `~/.claude/skills/`
- `cline` → `.clinerules/`
- `roo` → `.roo/rules/`
- `aider` → appends to `CONVENTIONS.md`
- `codex` → appends to `AGENTS.md`
- `copilot` → appends to `.github/copilot-instructions.md`
- ... (10 frameworks total)

### 🧪 Tests
- `tests/test_cli.py` — **43 new tests** for detect/match/fetch/place
- All 43 passing
- Covers: framework detection, stack detection, intent matching (9 kingdoms), compound phrase scoring, per-framework placement, conflict resolution, append mode, filtering logic

### ✨ Match Quality Improvements
- Fixed regex: `unit.?test` → `unit.?tests?` (now matches plural "unit tests")
- Added compound phrase scoring: "unit tests" = 2 points (vs 1 for single words)
- This breaks ties correctly: "write unit tests" → rohan (2) beats the-shire (1, "write")
- Verified across 9 test intents covering all kingdoms

### 📋 Summary
| Item | Count |
|:---|---:|
| CLI modules | 6 (lotr, detect, match, fetch, place, generate_index) |
| CLI subcommands | 7 (install, preview, list, search, detect, kingdoms, update) |
| Skills indexed | 16,760 |
| Canonical ⭐ in index | 354 |
| New tests | 43 |
| Frameworks supported | 10 (antigravity, cursor, claude-code, cline, roo, continue, goose, aider, codex, copilot) |
| Languages detected | 6 (typescript, javascript, python, ruby, go, rust) |

---

## [1.6.0] — 2026-06-29 — *The Kickoff + PyPI*

### 🚀 New: `lotr kickoff` — Multi-Kingdom Project Setup

A new mode that installs skills across **multiple kingdoms** for project kickoff. Instead of one task, you describe the project and the CLI fetches skills from all relevant domains.

```bash
# Two modes, same command — auto-detected:
lotr "write unit tests"          # → install mode (single kingdom: rohan)
lotr "building a tauri app"      # → kickoff mode (5 kingdoms: gondor, rohan, moria, fangorn, isengard)
```

**Kickoff mode downloads only 10-15 canonical skills — not 18,000.**

### 🧠 Smart Auto-Detection

The CLI figures out the mode from how you describe it:
- **Kickoff signals**: "building", "starting", "creating", "setting up", "tauri", "saas", "dashboard", "microservice", "full-stack"
- **Single-task signals**: compound phrases like "unit tests", "code review", "OWASP" (clear primary intent)
- 13/13 test cases pass correctly

### 📦 New: PyPI Package (`lotr-skills`)

The CLI is now pip-installable:

```bash
pip install lotr-skills
lotr "write unit tests"
```

- `pyproject.toml` at repo root with `[project.scripts] lotr = "cli.lotr:main"`
- `cli/__init__.py` makes it a proper Python package
- Dual-mode imports: works as script (`python3 cli/lotr.py`) AND as package (`from cli.lotr import main`)
- Built + tested locally: `lotr --version` → `lotr 1.0.0`
- `PUBLISHING.md` with full twine upload instructions

### 🛠 New Files
- `pyproject.toml` — PyPI package config with `lotr` entry point
- `cli/__init__.py` — package marker
- `PUBLISHING.md` — step-by-step PyPI publishing guide
- `dist/` — built wheel + sdist (gitignored)

### 🧪 Tests
- **21 new tests** for kickoff mode (194 total, all passing)
- `TestKickoffDetection` — 15 parametrized cases for is_kickoff_intent()
- `TestMatchMulti` — 5 tests for multi-kingdom matching + default padding

### 📊 Summary
| Item | Count |
|:---|---:|
| CLI subcommands | 8 (install, kickoff, preview, list, search, detect, kingdoms, update) |
| Tests passing | 194 |
| PyPI package | Ready to publish (`lotr-skills` 1.0.0) |
| Kickoff detection accuracy | 13/13 (100%) |
| Skills downloaded in kickoff mode | 10-15 (not 18,000) |

---

## [1.7.0] — 2026-06-29 — *The Complete CLI*

### 🚀 New Commands (3 added — CLI now has 11 subcommands)

#### `lotr init` — Bootstrap
Creates `.lotr/AGENTS.md` so your AI agent knows about lotr and can reference its commands. Run once per project.

```bash
lotr init
# → creates .lotr/AGENTS.md (agent instructions with all lotr commands)
# → creates .lotr/config.json (detected framework + stack)
# → adds .lotr/ to .gitignore
```

#### `lotr starter` — Safe Defaults
Download a starter skill pack with safe defaults for your detected framework. No task description needed — perfect when you're unsure what you need.

```bash
lotr starter                    # 9 skills across 3 kingdoms (default)
lotr starter --skills-per-kingdom 5   # more skills per kingdom
```

Starter kingdoms per framework:
- **antigravity / cursor / general**: gondor + fangorn + mordor (coding + docs + security)
- **claude-code**: gondor + fangorn + isengard (coding + docs + agents)
- **codex**: gondor + fangorn + moria (coding + docs + devops)
- **cline / roo**: gondor + rohan + fangorn (coding + testing + docs)
- **aider**: gondor + fangorn (coding + docs)

#### `lotr guide` — Full Usage Guide
Show the complete usage guide in-terminal. Lists all commands with examples.

```bash
lotr guide
```

### 📦 Version Bump
- Bumped from v1.0.0 → **v1.2.0** on PyPI
- Updated `pyproject.toml`, `cli/__init__.py`, `cli/lotr.py` version strings
- Banner now shows "CLI v1.2"

### 🧪 Tests
- **6 new tests** (200 total, all passing)
- `TestStarterPack` — 4 tests for starter pack configuration
- `TestInitCommand` — 2 tests for init command (creates files, AGENTS.md has commands)

### 📋 Final Command List (11 subcommands)

| Command | What it does |
|:---|:---|
| `lotr init` | Bootstrap — creates .lotr/AGENTS.md so agent knows lotr |
| `lotr starter` | Safe defaults — no task needed, 9 skills across 3 kingdoms |
| `lotr guide` | Full usage guide in-terminal |
| `lotr install "task"` | Skills for one specific task |
| `lotr kickoff "project"` | Full project skill suite (multi-kingdom) |
| `lotr detect` | Show detected stack |
| `lotr list` | Browse available skills |
| `lotr search` | Search by keyword |
| `lotr preview` | Dry run |
| `lotr kingdoms` | List all 10 kingdoms |
| `lotr update` | Refresh skills |
| `lotr --help` | Auto-generated help |

### 📊 Summary
| Item | Count |
|:---|---:|
| CLI subcommands | 11 (was 8) |
| Tests passing | 200 (was 194) |
| PyPI version | 1.2.0 (was 1.0.0) |
| New commands | 3 (init, starter, guide) |

---

## [1.8.0] — 2026-06-29 — *The Design Kingdom*

### 🏰 New: 11th Kingdom — Minas Tirith (UI & Design)

Added a new kingdom dedicated to UI design, frontend aesthetics, and design systems.

**Motto:** *"The White City, where every surface is crafted with intention."*

**366 design skills** crawled from 3 repos:
- **leonxlnx/taste-skill** — 14 skills (brutalist, minimalist, stitch, brandkit, redesign, image-to-code, etc.) — the #1 most-stard design skill on GitHub (59k+ stars)
- **HermeticOrmus/LibreUIUX-Claude-Code** — 352 skills (design vocabulary, modern card/button/nav/form prompts, design systems, CLAUDE.md templates, checklists)
- **VoltAgent/awesome-claude-design** — README only (links to others)

### 🎨 New: `lotr design` Command

```bash
lotr design "make this app look premium"
# → detects framework
# → installs design skills from Minas Tirith
# → falls back to claude-code if your framework has no design skills
```

### 🛠 Changes
- Added `minas-tirith` to `classify.py` KINGDOM_KEYWORDS (design, ui, ux, aesthetic, glassmorphism, brutalism, etc.)
- Added `minas-tirith` to `build_package.py`, `generate_excel.py`, `cli/lotr.py`, `cli/match.py`
- Added `minas-tirith` to `generate_index.py` KINGDOM_DOMAINS
- Created `skills/minas-tirith/README.md` kingdom documentation
- Regenerated `skills/index.json` — now 17,126 skills across 11 kingdoms
- Bumped CLI version to 1.3.0
- Updated test expectations (11 kingdoms, "update the UI" → minas-tirith)

### 📊 Updated Stats
| Metric | Before | After |
|:---|---:|---:|
| Total artifacts | 16,760 | 17,126 |
| Kingdoms | 10 | 11 |
| CLI subcommands | 11 | 12 (added `design`) |
| PyPI version | 1.2.0 | 1.3.0 |

---

## [1.3.5] — 2026-07-11 — *Windows Fix + Framework Command*

### 🪟 Windows Unicode Fix
- Added `sys.stdout.reconfigure(encoding='utf-8', errors='replace')` at CLI startup
- Added `safe_print()` function that catches `UnicodeEncodeError` and falls back to ASCII replacement
- Fixes crash on Windows consoles with cp1252 encoding when printing emoji (⚔, ⭐, 🏰)

### 🏷 New: `lotr framework set` Command
```bash
lotr framework set antigravity    # sets framework in .lotr/config.json
lotr framework set cursor         # validates name, rejects invalid frameworks
```
- Validates framework name against 11 known frameworks
- Writes to `.lotr/config.json` without requiring manual file editing
- Shows old → new transition

### 🔍 Improvements
- Added `--kingdom` flag to `lotr preview` subcommand (parity with `lotr install`)
- Preview now works with `--kingdom` alone (no intent required when using --kingdom)
- `safe_print` used in banner to prevent Windows crashes

### 📝 Media Coverage
- Dev.to article published: https://dev.to/ansari_bilal/the-ultimate-collection-of-18k-ai-agent-skills-across-14-frameworks-fbo

### 📊 Current State
| Item | Value |
|:---|---:|
| CLI subcommands | 13 (init, framework, design, starter, guide, detect, kingdoms, search, list, preview, install, kickoff, update) |
| PyPI version | 1.3.5 |
| Tests passing | 231 |
| Frameworks supported | 14 |
| Kingdoms | 11 |
| Total artifacts | 17,126+ |

---

## [1.4.0] — 2026-07-12 — *The Searchable Realm*

### 🌐 New: Streamlit Web UI
- `web/app.py` — interactive skill browser with search, filter, and preview
- Search 17,000+ skills by keyword (title, summary, tags)
- Filter by kingdom (11), framework (14), canonical ⭐
- Preview full skill content without leaving the browser
- Kingdom dashboard with visual cards + bar chart
- Framework coverage table with detection patterns
- Copy `lotr install` command with one click
- Deployable to Streamlit Cloud / Hugging Face Spaces (free)

### 🧹 Cleanup
- Cleaned stale `[Unreleased]` section in CHANGELOG (removed already-done items)
- Updated README with web UI section + repo structure

### 📦 Version
- Bumped to v1.4.0
- 231 tests passing
- 13 CLI subcommands
- 11 kingdoms, 14 frameworks, 17,126 skills

---

## [1.4.1] — 2026-07-20 — *More Skills Added*

### 📥 New Skills (533 added from 4 repos)

#### MengTo/Skills (289 files)
- Game development skills (Three.js, VFX, combat, inventory, audio)
- Web design skills (hover effects, animations, landing pages, WebGL)
- UI design skills (design-first prompting, spec-driven UI)
- Codex workflows (video-to-prompt, HTML-to-interaction, page capture)
- Customer support skills (SaaS account cases)
- Media skills (Aura asset images)
- Kingdoms: gondor (95), minas-tirith (192), the-shire (2)

#### LaunchDarkly/agent-skills (128 files)
- Observability skills (alert investigation, logs, traces, metrics, sessions)
- Flag management skills (feature flags, experimentation)
- Graph creation skills (enums, metrics, traces visualization)
- Kingdoms: gondor (112), moria (16)

#### terramate-io/agent-skills (58 files)
- Terraform best practices (37 rules across 10 categories)
- Security, performance, language, module composition rules
- Kingdoms: gondor (19), moria (39)

#### netresearch/agents-skill (58 files)
- Agent rules (backend Go, PHP, TypeScript, testing, examples)
- Coding conventions and project-scoped rules
- Kingdoms: gondor (58)

### 📊 Updated Stats
| Metric | Before | After |
|:---|---:|---:|
| Total skills | 17,126 | 17,659 |
| Minas Tirith | 366 | 558 |
| Moria | 893 | 948 |
| Gondor | 9,228 | 9,512 |
| The Shire | 1,238 | 1,240 |
| Source repos | 310 | 314 |
