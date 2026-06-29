# ❓ FAQ — *Answers from the Wise*

> *"He that breaks a thing to find out what it is has left the path of wisdom."*

Common questions about The Lord of the Skills.

---

## 📚 General

### Q: What is The Lord of the Skills?

**A:** A compilation of **18,142+ AI agent skills, rules, and conventions** from **307+ GitHub repositories** across **15 frameworks** (Claude Code, Cursor, Cline, Roo, Aider, OpenHands, Codex, Continue, Goose, Copilot, AutoGen, CrewAI, LangGraph, Antigravity and General), organized into **10 LOTR-themed kingdoms** by domain.

### Q: Why LOTR theme?

**A:** Because boring folder structures are boring. The LOTR theme makes the repo memorable, fun to navigate, and gives a strong identity. Plus, "One Catalog to Rule Them All" is genuinely what this is.

### Q: Is this free to use?

**A:** The compilation scripts are MIT-licensed. The skill artifacts themselves retain their original upstream licenses — see [`docs/CREDITS.md`](docs/CREDITS.md). For commercial use, audit the licenses of the specific skills you use.

### Q: How is this different from awesome-claude-code or awesome-cursorrules?

**A:** Three key differences:
1. **Multi-framework** — We cover 14 frameworks, not just one.
2. **Canonical deduplication** — We identify one best representative per concept across all frameworks.
3. **Reusable crawler** — You can run our spider yourself to build a custom kingdom (domain).

---

## 🚀 Usage

### Q: How do I add a skill to my agent?

**A:** See [`QUICKSTART.md`](QUICKSTART.md) for the 60-second guide. Short version:
```bash
# Claude Code
cp -r skills/gondor/claude-code/* ~/.claude/skills/

# Cursor
cp -r skills/gondor/cursor/* .cursor/rules/
```

### Q: My agent doesn't see the new skills. What's wrong?

**A:** Most agents scan the skills directory at startup. **Restart your agent** (Claude Code, Cursor, Cline) after copying files.

### Q: What does the `canonical__` prefix mean?

**A:** It marks the **⭐ canonical representative** of a concept cluster. For example, `canonical__SKILL.md` is the best version of `SKILL.md` across all 307+ source repos. See [`DEDUP.md`](DEDUP.md) for how canonical skills are chosen.

### Q: Can I rename the `canonical__` files?

**A:** Yes — the prefix is just a marker. Strip it:
```bash
find ~/.claude/skills/ -name 'canonical__*' | while read f; do
  mv "$f" "$(echo "$f" | sed 's/canonical__//')"
done
```

### Q: How do I find a specific skill?

**A:** Three options:
1. **Excel index** — open `catalogs/Lord_of_the_Skills_Index.xlsx`, use the filter on the Artifacts sheet
2. **`git grep`** — `git grep -l "code-review" skills/`
3. **GitHub code search** — use the search box at the top of the repo page

### Q: Can I use just one kingdom?

**A:** Yes! Each kingdom is independent:
```bash
# Only security skills
cp -r skills/mordor/claude-code/* ~/.claude/skills/

# Only testing skills
cp -r skills/rohan/claude-code/* ~/.claude/skills/
```

### Q: Can I use just one framework?

**A:** Yes — copy just that framework's subdirectory:
```bash
# Only Cursor rules
cp -r skills/gondor/cursor/* .cursor/rules/

# Only Aider conventions
cp skills/gondor/aider/CONVENTIONS.md ./CONVENTIONS.md
```

---

## 🕷 Crawler

### Q: How long does the crawler take to run?

**A:** Approximately 1-2 hours for the full pipeline, depending on:
- Network speed (cloning 300+ repos)
- Disk speed (extracting 18,000+ files)
- GitHub API rate limits (we sleep between search queries)

The crawler is **resumable** — if it crashes or you kill it, just run again and it picks up where it left off.

### Q: Do I need a GitHub token?

**A:** No, but it helps. Without a token: 60 API req/hr (very slow). With a token: 5,000 req/hr (fast).

```bash
cd crawler/
export GITHUB_TOKEN=ghp_xxx
python3 crawler.py
```

### Q: The crawler says "No space left on device". What do I do?

**A:** The crawler clones 300+ repos (~5-10 GB). Either:
1. Free up disk space (each cached repo can be deleted after extraction).
2. Use the `cleanup_repo_cache()` function (built into v1.2.0+).
3. Run on a machine with 20+ GB free.

### Q: How do I add my own seed repos?

**A:** Edit `crawler/crawler.py` and add to the `SEEDS` list:
```python
SEEDS = [
    ...
    "yourusername/your-skills-repo",
]
```

### Q: Can I run just the antigravity crawler?

**A:** Yes:
```bash
cd crawler/
python3 crawler_antigravity.py
```

This is faster (~20-30 min) and only targets antigravity-specific repos.

---

## 🏰 Kingdoms

### Q: How are skills assigned to kingdoms?

**A:** By weighted keyword voting. Each kingdom has a list of domain keywords (e.g., Gondor = "coding, refactor, debug, git, typescript, react"). The classifier counts keyword matches in each skill file's content + path, and assigns the kingdom with the most matches. See [`crawler/classify.py`](crawler/classify.py) for the implementation.

### Q: What if a skill fits multiple kingdoms?

**A:** It's assigned to the kingdom with the most keyword matches. We don't duplicate files across kingdoms (would inflate counts). If you think a skill is misclassified, [open an issue](https://github.com/Bilal140202/the-lord-of-the-skills/issues/new).

### Q: Can I propose a new kingdom?

**A:** Yes! Open an issue with:
- Proposed kingdom name (LOTR-themed)
- Domain it covers
- Example skills that would belong there
- Why the existing 10 kingdoms don't cover it

### Q: Why is Mirkwood so small (only 81 files)?

**A:** Mirkwood is the "Specialized & Niche" bucket — it only catches files that don't match any other kingdom's keywords. Most skills fit into one of the other 9 kingdoms. If you have specialized skills (esoteric, experimental, one-off), they'll land here.

---

## ⚖ Licensing

### Q: Can I use this commercially?

**A:** The compilation scripts are MIT-licensed — yes. The skill artifacts retain their original upstream licenses — **you must check each skill's source license**. See [`docs/CREDITS.md`](docs/CREDITS.md) for the list of source repos.

### Q: I'm an upstream maintainer and want my skills removed.

**A:** No problem — [open an issue](https://github.com/Bilal140202/the-lord-of-the-skills/issues/new) with "Removal request: <repo-name>" and we'll remove them within 24 hours.

### Q: Can I redistribute this package?

**A:** For personal/internal use: yes. For commercial redistribution: you must audit [`docs/CREDITS.md`](docs/CREDITS.md) and respect each upstream license. We do NOT re-license any upstream artifact.

---

## 🤝 Contributing

### Q: How do I add a new skill?

**A:** See [`CONTRIBUTING.md`](CONTRIBUTING.md). Short version:
1. Fork the repo
2. Add your skill to `skills/<kingdom>/<framework>/<your-repo>/SKILL.md`
3. Open a PR

### Q: Do you accept skills in any language?

**A:** Yes — we accept skills in English, Spanish, French, German, Chinese, Japanese and any other language. The classifier works on keyword matching so non-English skills may end up in `general` or `mirkwood` — that's fine.

### Q: How do I become a maintainer?

**A:** Consistently contribute high-quality PRs (skills, code, docs) for 3+ months. Reach out via an issue tagged `maintainer-request`.

---

## 🐛 Troubleshooting

### Q: The PDF won't open.

**A:** Try a different PDF viewer (Adobe Reader, Preview, Chrome). If it still fails, [open an issue](https://github.com/Bilal140202/the-lord-of-the-skills/issues/new) — we'll regenerate it.

### Q: The Excel file is too big for my spreadsheet program.

**A:** The Excel file is ~1.3 MB with 18,000+ rows. Use Excel, Google Sheets, or LibreOffice Calc. For very old spreadsheet software, use the PDF catalog instead.

### Q: `git clone` is slow.

**A:** The repo is ~20 MB (skills folder is large). Use `--depth=1` for a shallow clone:
```bash
git clone --depth=1 https://github.com/Bilal140202/the-lord-of-the-skills.git
```

### Q: I'm getting rate-limited by GitHub when running the crawler.

**A:** Get a GitHub token (free at https://github.com/settings/tokens) and set it:
```bash
cd crawler/
export GITHUB_TOKEN=ghp_xxx
python3 crawler.py
```

This raises your limit from 60 req/hr to 5,000 req/hr.

---

## 💬 Still Have Questions?

[Open an issue](https://github.com/Bilal140202/the-lord-of-the-skills/issues/new) — we respond within 24 hours.

Or [start a discussion](https://github.com/Bilal140202/the-lord-of-the-skills/discussions) for longer-form conversations.

---

<div align="center">

*"Not all those who wander are lost"*

</div>
