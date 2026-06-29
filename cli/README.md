# ⚔ lotr — The Lord of the Skills CLI

> *One command. Any framework. Any kingdom.*

`lotr` is a smart skills installer that detects your project's AI agent framework, maps your natural-language task to the right LOTR kingdom, fetches canonical skills from [The Lord of the Skills](https://github.com/Bilal140202/the-lord-of-the-skills), and drops them in the exact right location — in under 3 seconds.

## 🚀 Install

```bash
# From source (for now; PyPI package coming in v1.6.0)
git clone https://github.com/Bilal140202/the-lord-of-the-skills.git
cd the-lord-of-the-skills/cli
pip install -r requirements.txt  # just `requests` for now

# Add to PATH (optional)
echo 'alias lotr="python3 /path/to/the-lord-of-the-skills/cli/lotr.py"' >> ~/.bashrc
```

## 🎯 Quick Start

```bash
# cd into any project that uses an AI agent
cd my-react-project/

# Install skills for a task — auto-detects everything
lotr "write unit tests for the API"

# That's it. The CLI:
# 1. Detects → cursor + typescript + react
# 2. Maps    → "write unit tests" → rohan (testing)
# 3. Fetches → canonical ⭐ testing skills for cursor
# 4. Places  → .cursor/rules/jest-cursor-rules.mdc, testing-rules.mdc, ...
```

## 📋 Commands

### `lotr "<intent>"` (auto-detects install vs kickoff)
Natural-language install. Auto-detects framework, matches intent to kingdom, fetches + places skills.

The CLI auto-detects whether you want a **single task** (install mode) or a **project kickoff** (multi-kingdom setup) based on your phrasing:

```bash
# Single-task mode (auto-detected):
lotr "update the UI to be more modern"      # → gondor (coding)
lotr "deploy to kubernetes"                  # → moria (devops)
lotr "audit for OWASP vulnerabilities"       # → mordor (security)
lotr "write a blog post about our launch"    # → the-shire (writing)
lotr "set up memory bank for context"        # → fangorn (memory)

# Project kickoff mode (auto-detected):
lotr "building a tauri app"                  # → 5 kingdoms (gondor, rohan, moria, fangorn, isengard)
lotr "starting a nextjs SaaS dashboard"      # → 5+ kingdoms
lotr "setting up a full-stack react platform" # → 5+ kingdoms
```

### `lotr kickoff` (explicit kickoff mode)
Multi-kingdom project setup. Install skills across all relevant kingdoms for a new project.

```bash
lotr kickoff "building a tauri app"
lotr kickoff "starting a nextjs SaaS dashboard" --top-kingdoms 4 --skills-per-kingdom 3
```

### `lotr install`
Explicit install with optional overrides.

```bash
lotr install "add authentication"            # auto-detect + match
lotr install --kingdom mordor --framework cursor   # explicit
lotr install "write tests" --limit 5         # max 5 skills
lotr install "refactor" --all                # include non-canonical
```

### `lotr preview`
Dry-run: shows what would be installed without writing any files.

```bash
lotr preview "write unit tests"
# [detect] framework=cursor  language=typescript  stack=[react, next]
# [match]  intent="write unit tests" → rohan (score=2, kws=[unit tests])
# [fetch]  3 canonical skills found for rohan/cursor
# [place]  Would install to .cursor/rules/
#   ⭐ jest-cursor-rules.mdc
#   ⭐ testing-rules.mdc
#   ⭐ ruby-on-rails-cursor-rules.mdc
# (dry-run — no files written)
```

### `lotr list`
List all available skills for your detected framework.

```bash
lotr list                  # canonical ⭐ only
lotr list --all            # include non-canonical
lotr list --framework claude-code   # override
```

### `lotr search`
Search the entire skills index by keyword.

```bash
lotr search "code review"
lotr search "react"
lotr search "kubernetes"
```

### `lotr detect`
Show what the CLI detected for your project.

```bash
$ lotr detect
[detect] Scanning project...
  Framework:  cursor
  Language:   typescript
  Stack:      ['react', 'next', 'typescript']
  Project:    /home/user/my-react-project
```

### `lotr kingdoms`
List all 10 LOTR kingdoms.

```bash
$ lotr kingdoms
The Ten Kingdoms:
  ⚔ Gondor         Coding & Software Engineering
  ✦ Rivendell      Research & Knowledge
  ⛏ Moria          DevOps & Infrastructure
  ✿ Lothlórien     Data & Analysis
  👁 Mordor         Security & Auditing
  ✎ The Shire      Writing & Content
  ⚙ Isengard       Agents & Orchestration
  🐴 Rohan          Testing & Verification
  🌳 Fangorn       Documentation & Memory
  🕸 Mirkwood       Specialized & Niche
```

### `lotr update`
Update all installed skills to the latest version from the index.

```bash
lotr update
```

## 🏗 Architecture

```
cli/
├── lotr.py           ← entry point (argparse + subcommands)
├── detect.py         ← stack + framework detector
├── match.py          ← intent → kingdom mapper (weighted keyword voting)
├── fetch.py          ← GitHub raw downloader (with local fallback + caching)
├── place.py          ← smart per-framework placement
└── generate_index.py ← builds skills/index.json from the skills tree
```

### How it works (the 4-phase pipeline)

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ detect  │ -> │  match  │ -> │  fetch  │ -> │  place  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
   |              |              |              |
   |              |              |              |
   v              v              v              v
.antigravity/  "write unit   GitHub raw   .cursor/rules/
.cursor/       tests" →       CDN          ~/.claude/skills/
.claude/       rohan          (instant)    .clinerules/
.clinerules/                                .roo/rules/
```

### The `skills/index.json` manifest

The CLI queries a machine-readable manifest at `skills/index.json` (generated by `generate_index.py`). This is what makes skill lookup instant — no git clone needed.

```json
{
  "version": "1.0.0",
  "total_skills": 16760,
  "canonical_count": 354,
  "skills": [
    {
      "id": "rohan/cursor/nedcodes-ok__cursorrules-collection/canonical__eest.mdc",
      "title": "Jest Cursor Rules",
      "kingdom": "rohan",
      "frameworks": ["cursor"],
      "canonical": true,
      "tags": ["test", "cursor", "rohan"],
      "source_repo": "nedcodes-ok/cursorrules-collection",
      "filename": "canonical__eest.mdc",
      "path": "skills/rohan/cursor/nedcodes-ok__cursorrules-collection/canonical__eest.mdc"
    }
  ]
}
```

## 🎨 Per-Framework Placement

The CLI knows exactly where each framework expects its skills:

| Framework | Mode | Destination |
|:---|:---|:---|
| antigravity | dir | `.antigravity/skills/` |
| cursor | dir | `.cursor/rules/` |
| claude-code | dir | `~/.claude/skills/` |
| cline | dir | `.clinerules/` |
| roo | dir | `.roo/rules/` |
| continue | dir | `.continue/rules/` |
| goose | dir | `.goose/extensions/` |
| aider | append | `CONVENTIONS.md` |
| codex | append | `AGENTS.md` |
| copilot | append | `.github/copilot-instructions.md` |

## 🧪 Tests

```bash
cd tests/
pytest test_cli.py -v
```

## 🛠 Development

```bash
# Regenerate the index after adding skills
python3 cli/generate_index.py

# Run the CLI in dev mode (uses local skills/ as fallback if remote fetch fails)
python3 cli/lotr.py detect --project-root /path/to/project
```

## 📦 PyPI Package (coming in v1.6.0)

```bash
pip install lotr-skills   # not yet published
```

## 🗺 Roadmap

- [x] `detect` — framework + stack detection
- [x] `match` — intent → kingdom mapping
- [x] `fetch` — GitHub raw downloader
- [x] `place` — smart per-framework placement
- [x] `install` / `preview` / `list` / `search` / `kingdoms` / `detect` / `update`
- [x] `skills/index.json` manifest
- [ ] PyPI package (`pip install lotr-skills`)
- [ ] Fuzzy search (typos, synonyms)
- [ ] AI-powered intent matching (embeddings)
- [ ] `lotr init` — bootstrap a new project with recommended skills

## 📄 License

MIT — see [LICENSE](../LICENSE)

## 🙏 Credits

Built on top of [The Lord of the Skills](https://github.com/Bilal140202/the-lord-of-the-skills) compilation.

---

<div align="center">

*One command to rule them all.*

</div>
