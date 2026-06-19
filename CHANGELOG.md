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
- Broader crawler coverage (target 500+ repos)
- Per-kingdom dedicated READMEs
- Star-based ranking of canonical skills
- Weekly auto-refresh option (in addition to monthly)
- Star-fetcher for upstream repo stars to improve canonical scoring
- Docker image for one-command refresh
- VSCode extension for browsing skills in-editor
