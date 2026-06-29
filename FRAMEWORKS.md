# ⚙ Frameworks — *The Fellowship of the Skills*

The Lord of the Skills covers **14 agentic AI frameworks**. Each is identified by a unique file convention, listed below.

---

## 📊 Coverage Table

| Framework | Files | Kingdoms | Detection Pattern | Description |
|:---|---:|---:|:---|:---|
| 🟠 **claude-code** | 8,104 | 10 | `SKILL.md`, `skills/**/*.md` | Anthropic's official skill format used in Claude Code |
| 🟣 **cursor** | 1,400+ | 10 | `.cursorrules`, `.cursor/rules/*.mdc` | Cursor IDE rules — project-specific or global |
| 🔵 **cline** | 1,400+ | 10 | `.clinerules/`, `.cline/` | Cline memory banks and rules |
| ⚫ **roo** | 800+ | 9 | `.roo/rules/`, `.roo/modes/` | Roo Code (Cline fork) — extended rules |
| 🟢 **aider** | 600+ | 8 | `CONVENTIONS.md`, `.aider*` | Aider AI pair-programmer conventions |
| 🟡 **openhands** | 400+ | 8 | `openhands`, `OpenHands` | All-Hands-AI OpenHands agent files |
| ⚫ **codex** | 500+ | 9 | `AGENTS.md` | OpenAI Codex `AGENTS.md` convention |
| 🟤 **continue** | 200+ | 7 | `.continue/` | Continue.dev config files |
| ⚪ **goose** | 150+ | 6 | `.goose/`, `extensions/` | Block Goose extensions |
| 🔵 **copilot** | 100+ | 5 | `.github/copilot-instructions.md` | GitHub Copilot instructions |
| 🟣 **crewai** | 80+ | 6 | `crewai`, `CrewAI` | CrewAI agent configs |
| 🟢 **langgraph** | 60+ | 5 | `langgraph`, `LangGraph` | LangGraph agent definitions |
| 🟪 **antigravity** | 820 | 10 | Antigravity-tagged repos | [Google Antigravity IDE](https://antigravity.google) — Google's AI-first IDE launched Nov 2025 with Gemini 3. **This is the only major skills catalog covering Antigravity.** |
| ⚪ **general** | 2,535+ | 10 | Various / unclassified | Cross-framework or unclassified skills |

---

## 🎯 Framework Detection Logic

The crawler identifies framework by both **filename pattern** and **repo name**. The detection priority is:

1. **Explicit path indicators** (highest priority):
   - `.cursor/rules/*.mdc` → cursor
   - `.clinerules/*.md` → cline
   - `.roo/rules/*.md` → roo
   - `.continue/*.yaml` → continue
   - `.goose/*.yaml` → goose
   - `.github/copilot-instructions.md` → copilot

2. **Canonical filenames**:
   - `SKILL.md`, `skills/**/*.md` → claude-code
   - `AGENTS.md` → codex
   - `CONVENTIONS.md` → aider

3. **Repo name fallback**:
   - If repo name contains `cursor`, `cline`, `aider`, etc., use that framework

4. **Default**:
   - `general` bucket for anything that doesn't match

---

## 🔧 Adding a New Framework

Want to add support for a new framework (e.g., Windsurf, Codeium, Devin)? Here's how:

### Step 1: Add Detection Patterns

Edit `crawler/crawler.py` and add the framework's filename patterns to `SKILL_FILE_PATTERNS`:

```python
# Example: adding windsurf support
re.compile(r"(^|/)\.windsurfrules$", re.I),
re.compile(r"(^|/)\.windsurf/rules/.+\.md$", re.I),
```

### Step 2: Add to Framework Patterns

In `crawler/crawler.py`, add to `FRAMEWORK_PATTERNS`:

```python
"windsurf": [".windsurfrules", ".windsurf"],
```

### Step 3: Add to detect_framework()

In `crawler/crawler.py`, add detection logic:

```python
if ".windsurf" in rp or "windsurfrules" in rp:
    return "windsurf"
```

### Step 4: Add Seed Repos

Add known windsurf skill repos to `SEEDS`:

```python
"yourusername/awesome-windsurf-rules",
```

### Step 5: Add to GitHub Search Queries

In `crawler/crawler.py` Phase 3, add search queries:

```python
"filename:.windsurfrules",
"windsurf rules collection",
```

### Step 6: Run the Crawler

```bash
cd crawler/
python3 crawler.py
python3 classify.py
python3 dedup.py
python3 build_package.py
```

### Step 7: Update This Doc

Add the new framework to the table above, update README.md and KINGDOMS.md counts.

---

## 📁 Per-Framework Directory Layout

Each kingdom has subdirectories for each framework present. For example:

```
skills/gondor/                    ← Coding kingdom
├── claude-code/                  ← Claude Code skills (SKILL.md format)
│   ├── anthropics__skills/
│   │   ├── SKILL.md
│   │   └── canonical__SKILL.md   ← ⭐ canonical representative
│   ├── wshobson__agents/
│   └── ...
├── cursor/                       ← Cursor rules (.cursorrules / .mdc)
│   ├── davila7__claude-code-templates/
│   └── ...
├── cline/                        ← Cline memory banks
├── roo/                          ← Roo Code rules
├── aider/                        ← Aider CONVENTIONS.md
├── codex/                        ← Codex AGENTS.md
├── antigravity/                  ← Antigravity IDE skills (NEW!)
└── ... (11 frameworks in Gondor)
```

---

## 🆕 Framework Spotlight: Google Antigravity (added in v1.2.0)

Google Antigravity is a new agentic IDE released in 2025. We added support for it via:

1. **Dedicated crawler**: `crawler/crawler_antigravity.py` with 30 targeted search queries
2. **Antigravity-specific seeds**: `sickn33/antigravity-awesome-skills`, `google/antigravity`, etc.
3. **GitHub Code Search**: for files containing "antigravity"
4. **BFS expansion**: scan antigravity-awesome-skills README for related repos

**Result**: 689 antigravity-related repos discovered, 307 cloned, 11,697 files extracted. **820 files explicitly tagged as `antigravity` framework**.

To browse antigravity skills:

```bash
# All antigravity skills across all kingdoms
find skills/ -path '*/antigravity/*' -name '*.md' | head

# Antigravity coding skills specifically
ls skills/gondor/antigravity/
```

---

## 📈 Framework Statistics Over Time

| Version | claude-code | cursor | cline | roo | aider | openhands | codex | antigravity | Total |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| v1.0.0 | 4,200 | 2,100 | 1,400 | 800 | 600 | 400 | 500 | — | 10,888 |
| v1.2.0 | 8,104 | 1,400+ | 1,400+ | 800+ | 600+ | 400+ | 500+ | 820 | 18,142 |

---

<div align="center">

*The Fellowship welcomes new members.*

</div>
