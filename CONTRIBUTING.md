# 🤝 Contributing to The Lord of the Skills

> *"Yet it is not our part to master all the tides of the world, but to do what is in us for the succor of those years wherein we are set, uprooting the evil in the fields that we know."*

Thank you for considering contributing to the kingdom! This document explains how.

## 🏰 Ways to Contribute

### 1. Add a New Skill
Have a skill file (SKILL.md, AGENTS.md, .cursorrules, etc.) that should be in the compilation?

**Option A — Add directly to source repo:**
1. Place your skill in `skills/<kingdom>/<framework>/<your-repo>/`
2. Filename should match the original convention (e.g., `SKILL.md`, `.cursorrules`)
3. If it's the canonical representative, prefix with `canonical__` (e.g., `canonical__SKILL.md`). See [DEDUP.md](DEDUP.md) for how canonical skills are chosen.
4. Open a PR

**Option B — Add a source repo:**
1. Edit `crawler/crawler.py` and add the repo to `SEEDS`
2. Run the crawler to extract: `python3 crawler/crawler.py`
3. Re-run the pipeline:
   ```bash
   python3 crawler/classify.py
   python3 crawler/dedup.py
   python3 crawler/build_package.py
   python3 crawler/generate_excel.py
   python3 crawler/generate_pdf.py
   ```
4. Open a PR with the new artifacts + updated manifest

### 2. Propose a New Kingdom
Have an idea for an 11th kingdom? Open an issue with:
- Kingdom name (LOTR-themed)
- Domain it covers
- Example skills that would belong there
- Why the existing 10 kingdoms don't cover it

### 3. Improve the Crawler
The crawler is in `crawler/crawler.py`. Common improvements:
- **Broader file detection**: Add new patterns to `SKILL_FILE_PATTERNS`
- **Better BFS**: Improve `discover_repos_from_readme()` regex
- **Smarter classification**: Tweak `KINGDOM_KEYWORDS` in `classify.py`
- **Better dedup**: Adjust `jaccard` threshold in `dedup.py`

### 4. Improve Documentation
- Fix typos in README.md
- Add usage examples for new frameworks
- Translate docs to other languages
- Improve the PDF catalog design

## 🛠 Development Setup

```bash
git clone https://github.com/Bilal140202/the-lord-of-the-skills.git
cd the-lord-of-the-skills

# Install Python deps (pinned in requirements.txt)
pip install -r crawler/requirements.txt

# Run the full pipeline
python3 crawler/crawler.py
python3 crawler/classify.py
python3 crawler/dedup.py
python3 crawler/build_package.py
python3 crawler/generate_excel.py
python3 crawler/generate_pdf.py

# Run tests
pytest tests/ -v
```

## 📋 Pull Request Checklist

- [ ] Code follows existing style
- [ ] If adding files to `skills/`, the file is genuine and not a duplicate
- [ ] If modifying crawler, the crawler still runs to completion
- [ ] README.md is updated if needed
- [ ] CHANGELOG.md is updated
- [ ] No secrets/tokens in commits

## 🐛 Reporting Issues

When reporting an issue, please include:
- What you expected
- What actually happened
- Steps to reproduce
- Your OS + Python version
- Relevant log output (from `_cache/crawler.log`)

## ⚖ Licensing

By contributing, you agree that your contributions will be licensed under the MIT license for the compilation scripts. Skill artifacts you submit retain whatever license you specify (default: same as the source repo).

## 🌟 Recognition

All contributors are listed in the README's Contributors section (auto-generated from GitHub). Top contributors get a mention in the CHANGELOG.

---

<div align="center">

*May your contributions flow like the Anduin — strong, steady, and far-reaching.*

</div>
