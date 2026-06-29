# 🕷 Crawler — The Spider of the Skills

> *"For a fleeting moment, could one of the sleepers have seen him, they would have thought that they beheld an old weary hobbit, shrunken by the years that had carried him far beyond his time..."*

The crawler is the heart of The Lord of the Skills. It spiders GitHub for agentic AI skill/agent/rule files, extracts them, classifies them into LOTR kingdoms, deduplicates with canonical marking, and packages everything into the themed library.

## 🚀 Quick Start

```bash
# Run the full pipeline end-to-end
python3 crawler.py        # Spider GitHub, clone repos, extract skill files
python3 classify.py       # Tag each file with kingdom + skill type
python3 dedup.py          # Cluster + mark canonical ⭐
python3 build_package.py  # Build themed package
python3 generate_excel.py # Generate Excel index
python3 generate_pdf.py   # Generate PDF catalog
```

Or use the all-in-one refresh script:
```bash
bash refresh_lord_of_skills.sh
```

## 🏗 Architecture

### 5-Phase Resumable Crawler

The crawler (`crawler.py`) is fully resumable — it saves state after every 10 repos, so you can kill and restart it without losing progress.

```
Phase 1: Clone seed repos
  ↓
Phase 2: BFS-expand from cloned READMEs
  ↓
Phase 3: GitHub Search API expansion (rate-limited)
  ↓
Phase 4: Clone all discovered repos
  ↓
Phase 5: Extract skill/agent/rule files from every cloned repo
```

### File Types Detected

The crawler's `SKILL_FILE_PATTERNS` regex matches:

| Pattern | Framework |
|:---|:---|
| `SKILL.md`, `skill.md` | Claude Code |
| `AGENTS.md` | OpenAI Codex |
| `CONVENTIONS.md` | Aider |
| `.cursorrules` | Cursor |
| `.cursor/rules/*.mdc` | Cursor |
| `.clinerules/*`, `.cline/*` | Cline |
| `.roo/rules/*`, `.roo/modes/*` | Roo Code |
| `.continue/*` | Continue |
| `.goose/*` | Block Goose |
| `.aider*` | Aider |
| `.github/copilot-instructions.md` | GitHub Copilot |
| `skills/**/*.md` | Claude Code (Anthropic) |
| `agents/**/*.md` | General |
| `prompts/**/*.md` | General |
| `*.prompt.md`, `*.mdc` | General |

### LOTR Kingdom Classifier

The classifier (`classify.py`) uses weighted keyword voting to assign each file to one of 10 kingdoms:

| Kingdom | Domain | Sample Keywords |
|:---|:---|:---|
| ⚔ Gondor | Coding & Software Engineering | coding, refactor, debug, git, commit, typescript, react |
| ✦ Rivendell | Research & Knowledge | research, analyze, paper, methodology |
| ⛏ Moria | DevOps & Infrastructure | devops, kubernetes, docker, terraform, aws |
| ✿ Lothlórien | Data & Analysis | data, etl, pandas, ml, statistics |
| 👁 Mordor | Security & Auditing | security, vuln, owasp, xss, crypto |
| ✎ The Shire | Writing & Content | writing, blog, docs, readme, marketing |
| ⚙ Isengard | Agents & Orchestration | agent, subagent, orchestrat, workflow |
| 🐴 Rohan | Testing & Verification | test, verify, assert, coverage, lint |
| 🌳 Fangorn | Documentation & Memory | memory, context, rag, embedding |
| 🕸 Mirkwood | Specialized & Niche | (fallback bucket) |

### Deduplication + Canonical Marking

The dedup pass (`dedup.py`):
1. Clusters files by normalized title (exact match)
2. For unclustered files, tries Jaccard similarity ≥ 0.7 on summary tokens
3. Within each cluster, picks one canonical ⭐ via a score combining:
   - Framework priority (Claude Code > Codex > OpenHands > Cursor > Cline > ...)
   - Skill-type priority (conventions > orchestration > planning > execution > ...)
   - File size (longer = richer = preferred, capped at 50KB)
   - Well-known filename bonus (SKILL.md, AGENTS.md, CONVENTIONS.md get +20)

## 🔄 Monthly Refresh

Install the cron job for automatic monthly refresh:

```bash
crontab crawler/lord_of_the_skills.cron
```

Schedule: 1st of every month at 03:00 IST.

The refresh script (`refresh_lord_of_skills.sh`) is fully resumable — it keeps cached git clones and only re-extracts files. Old logs are auto-pruned (keeps last 12).

## 📁 Outputs

After a full run, outputs land in:
```
/home/z/my-project/the-lord-of-the-skills/
  _cache/
    manifest.json              ← Full manifest with all files
    manifest_classified.json   ← After classifier
    manifest_final.json        ← After dedup (canonical ⭐ marked)
    crawler_state.json         ← Resumable state
    crawler.log                ← Run log
    repos/                     ← Cached git clones (4-5 GB)
  _raw/
    <framework>/<repo>/<file>  ← Extracted skill files
```

The final package is built to:
```
/home/z/my-project/download/the-lord-of-the-skills/
  README.md, CREDITS.md, MAP_OF_THE_KINGDOMS.md, SKILL_INDEX.md
  Lord_of_the_Skills_Catalog.pdf
  Lord_of_the_Skills_Index.xlsx
  _manifest.json
  skills/<kingdom>/<framework>/<repo>/<file>
```

## 🐛 Troubleshooting

### "CLONE FAIL: could not read Username"
The repo is private or doesn't exist. Skipped automatically. To use a GitHub token:
```bash
export GITHUB_TOKEN=ghp_xxx
# crawler uses git clone which respects this
```

### Rate limited on GitHub Search API
Unauthenticated: 60 req/hr. With token: 5000 req/hr. The crawler sleeps 7s between searches to respect limits.

### Out of disk space
Each cloned repo is ~50MB. 300 repos = ~15GB. To clean:
```bash
rm -rf /home/z/my-project/the-lord-of-the-skills/_cache/repos/
# Re-run crawler — it will re-clone everything
```

---

<div align="center">

*The Spider of the Skills weaves its web across all of GitHub.*

</div>
