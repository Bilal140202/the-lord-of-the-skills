# 🚀 Quickstart — *The Fellowship Sets Out*

> *"I will take the Ring, though I do not know the way."*

Welcome to The Lord of the Skills — 18,142 AI agent skills organized into 10 LOTR-themed kingdoms. This guide gets you productive in 60 seconds.

---

## ⏱ The 60-Second Path (Option A: `lotr` CLI)

### Step 1: Install the CLI

```bash
# From PyPI (live!):
pip install lotr-skills

# Or run from source (no install needed):
git clone https://github.com/Bilal140202/the-lord-of-the-skills.git
cd the-lord-of-the-skills
python3 cli/lotr.py --version
```

### Step 2: cd into your project

```bash
cd my-react-project/   # must have .cursor/, .claude/, .clinerules/, etc.
```

### Step 3: Bootstrap (once per project)

```bash
lotr init
# → creates .lotr/AGENTS.md (tells your agent about lotr)
# → creates .lotr/config.json (detected framework + stack)
```

### Step 4: Install skills

```bash
# Safe defaults (if unsure what you need):
lotr starter
# → installs 9 canonical skills across 3 kingdoms (gondor, fangorn, mordor)

# Single-task mode (auto-detected):
lotr "write unit tests for the API"
# → matches "unit tests" → rohan (testing)
# → downloads 2 canonical skills → .cursor/rules/

# Project kickoff mode (auto-detected):
lotr "building a tauri app"
# → plans 5 kingdoms (gondor, rohan, moria, fangorn, isengard)
# → downloads 4 skills across all kingdoms → .cursor/rules/

# Full usage guide:
lotr guide
```

### Step 5: Restart your agent

Restart Claude Code / Cursor / Cline — it'll scan the new skills on startup.

---

## ⏱ The 60-Second Path (Option B: Manual Copy)

### Step 1: Clone the Kingdom

```bash
git clone https://github.com/Bilal140202/the-lord-of-the-skills.git
cd the-lord-of-the-skills
```

### Step 2: Pick Your Framework

Pick the framework you use — copy-paste the right command:

```bash
# Claude Code (Anthropic)
cp -r skills/gondor/claude-code/* ~/.claude/skills/
cp -r skills/isengard/claude-code/* ~/.claude/skills/    # agents/orchestration
cp -r skills/mordor/claude-code/* ~/.claude/skills/      # security

# Cursor
mkdir -p .cursor/rules/
cp -r skills/gondor/cursor/* .cursor/rules/

# Cline / Roo Code
cp -r skills/gondor/cline/* .clinerules/
cp -r skills/gondor/roo/*   .roo/rules/

# Aider
cp skills/gondor/aider/CONVENTIONS.md ./CONVENTIONS.md

# OpenAI Codex (AGENTS.md convention)
cp skills/isengard/codex/AGENTS.md ./AGENTS.md

# Google Antigravity (NEW!)
cp -r skills/gondor/antigravity/* ~/.antigravity/skills/

# GitHub Copilot
mkdir -p .github/
cp skills/gondor/copilot/copilot-instructions.md .github/copilot-instructions.md
```

### Step 3: Verify It Worked

```bash
# Claude Code
ls ~/.claude/skills/ | head

# Cursor
ls .cursor/rules/ | head

# Cline
ls .clinerules/ | head
```

You should see skill files like `SKILL.md`, `code-review.md`, `git-commit.md`, etc.

### Step 4: Use It!

Restart your agent (Claude Code, Cursor, Cline, etc.) and try:

```
# In Claude Code:
> Use the code-review skill to review my latest commit

# In Cursor:
> Refactor this function using the refactor-typescript skill

# In Cline:
> Run the security-audit skill on this directory
```

---

## ⭐ Canonical-Only Mode (Recommended for Production)

If you want just **one best skill per concept** (357 total, deduplicated):

```bash
# Copy only the ⭐ canonical representatives
find skills/ -name 'canonical__*' -exec cp {} ~/.claude/skills/ \;
```

This gives you a clean, curated set without the duplicates. Read [`DEDUP.md`](DEDUP.md) to understand how canonical ⭐ skills are chosen.

---

## 🏰 Browse the Kingdoms

Each kingdom has its own README with stats, framework breakdown, and usage examples:

| Kingdom | Domain | Browse |
|:---|:---|:---|
| ⚔ Gondor | Coding | [`skills/gondor/README.md`](skills/gondor/README.md) |
| ✦ Rivendell | Research | [`skills/rivendell/README.md`](skills/rivendell/README.md) |
| ⚙ Isengard | Agents | [`skills/isengard/README.md`](skills/isengard/README.md) |
| ✎ The Shire | Writing | [`skills/the-shire/README.md`](skills/the-shire/README.md) |
| ⛏ Moria | DevOps | [`skills/moria/README.md`](skills/moria/README.md) |
| 🐴 Rohan | Testing | [`skills/rohan/README.md`](skills/rohan/README.md) |
| 🌳 Fangorn | Memory | [`skills/fangorn/README.md`](skills/fangorn/README.md) |
| ✿ Lothlórien | Data | [`skills/lothlorien/README.md`](skills/lothlorien/README.md) |
| 👁 Mordor | Security | [`skills/mordor/README.md`](skills/mordor/README.md) |
| 🕸 Mirkwood | Specialized | [`skills/mirkwood/README.md`](skills/mirkwood/README.md) |

---

## 📄 Browse the Catalogs

The repo ships with two pre-built catalogs:

```bash
# PDF catalog (33 pages, themed)
open catalogs/Lord_of_the_Skills_Catalog.pdf

# Excel index (6 sheets, filterable)
open catalogs/Lord_of_the_Skills_Index.xlsx
```

- **PDF**: cover, fellowship manifesto, map of kingdoms, per-kingdom sections with top canonical skills, credits
- **Excel**: About, Artifacts (10,888+ filterable rows), Kingdoms, Frameworks, Canonical ⭐, Stats

---

## 🕷 Run the Crawler Yourself

Want to build your own kingdom from scratch, or refresh this one with the latest skills?

```bash
cd crawler/
pip install -r requirements.txt

# Full pipeline (resumable)
python3 crawler.py            # 1. Spider GitHub (5-phase, ~1-2 hours)
python3 classify.py           # 2. Tag each file with kingdom + skill type
python3 dedup.py              # 3. Cluster + mark canonical ⭐
python3 build_package.py      # 4. Build themed package
python3 generate_excel.py     # 5. Generate Excel index
python3 generate_pdf.py       # 6. Generate PDF catalog

# Or — one-shot refresh script
bash refresh_lord_of_skills.sh
```

📖 Full crawler docs: [`crawler/README.md`](crawler/README.md)

---

## ❓ Common Issues

**Q: I copied the skills but my agent doesn't see them.**
A: Restart your agent (Claude Code / Cursor / Cline). Most agents only scan the skills directory at startup.

**Q: The `canonical__` files have weird names. Can I rename them?**
A: Yes! The `canonical__` prefix is just a marker. You can strip it:
```bash
find ~/.claude/skills/ -name 'canonical__*' | while read f; do
  mv "$f" "$(echo $f | sed 's/canonical__//')"
done
```

**Q: I want only skills for [specific framework].**
A: Just copy that framework's subdirectory:
```bash
cp -r skills/gondor/claude-code/* ~/.claude/skills/    # only Claude Code
```

**Q: How do I find a specific skill?**
A: Use the Excel index or `git grep`:
```bash
git grep -l "code-review" skills/
```

📖 More: [`FAQ.md`](FAQ.md)

---

## 🎯 Next Steps

1. ⭐ [Star the repo](https://github.com/Bilal140202/the-lord-of-the-skills/stargazers) — helps others discover it
2. 🍴 [Fork it](https://github.com/Bilal140202/the-lord-of-the-skills/fork) — customize for your workflow
3. 📖 Read [`KINGDOMS.md`](KINGDOMS.md) — explore the 10 kingdoms
4. 🤝 [Contribute](CONTRIBUTING.md) — add a skill, fix a bug, improve docs

---

<div align="center">

*The road goes ever on and on, down from the door where it began...*

</div>
