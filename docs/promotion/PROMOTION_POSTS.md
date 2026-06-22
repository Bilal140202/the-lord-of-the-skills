# 📣 Promotion Posts — *Spreading the Word of the Kingdom*

Ready-to-post templates for sharing The Lord of the Skills across platforms. Each is tailored to the platform's audience and format.

---

## 🟠 Reddit — r/MachineLearning

**Title:** [Project] I built "The Lord of the Skills" — 18,142+ AI agent skills from 14 frameworks, organized into 10 LOTR-themed kingdoms

**Body:**

Hi r/MachineLearning,

I've been frustrated by how scattered AI agent skills are across GitHub. Claude Code skills here, Cursor rules there, Cline memory banks somewhere else. So I built a crawler to spider all of GitHub and compile them into one organized library.

**The result: [The Lord of the Skills](https://github.com/Bilal140202/the-lord-of-the-skills)**

Stats:
- 18,142+ artifacts extracted
- 307+ source repositories spidered
- 14 frameworks covered (Claude Code, Cursor, Cline, Roo, Aider, OpenHands, Codex, Continue, Goose, Copilot, AutoGen, CrewAI, LangGraph, Google Antigravity)
- 357 canonical ⭐ representatives (deduplicated)
- Organized into 10 LOTR-themed kingdoms:
  - ⚔ Gondor = Coding (10,141 skills)
  - ✦ Rivendell = Research (1,776)
  - ⚙ Isengard = Agents (1,630)
  - ✎ The Shire = Writing (1,272)
  - ⛏ Moria = DevOps (914)
  - 🐴 Rohan = Testing (718)
  - 🌳 Fangorn = Memory (708)
  - ✿ Lothlórien = Data (496)
  - 👁 Mordor = Security (406)
  - 🕸 Mirkwood = Specialized (81)

**Key features:**
- Reusable Python crawler (5-phase, resumable) — run it yourself to build a custom kingdom
- Canonical deduplication: one best representative per concept across all frameworks
- Monthly auto-refresh via cron
- 33-page themed PDF catalog + 6-sheet Excel index
- Drop-in ready: `cp -r skills/gondor/claude-code/* ~/.claude/skills/`

The crawler is open-source MIT. The skills themselves retain their original upstream licenses (see CREDITS.md).

I'd love feedback on:
1. The LOTR theme — fun or distracting?
2. The kingdom taxonomy — does it make sense? Should I add/remove kingdoms?
3. The canonical dedup algorithm — currently uses Jaccard similarity on summaries + framework priority scoring. Should I upgrade to embeddings?
4. What framework should I add next? (Windsurf? Codeium? Devin? Gemini?)

Star if it's useful: https://github.com/Bilal140202/the-lord-of-the-skills

---

## 🟠 Reddit — r/artificial

**Title:** Built an open-source crawler that spiders GitHub for every AI agent skill file (SKILL.md, AGENTS.md, .cursorrules, .clinerules, etc.) — 18,000+ skills compiled

**Body:**

Hey r/artificial — I open-sourced a Python crawler that spiders GitHub for agentic AI skill files and compiles them into one organized library. It covers 14 frameworks including Claude Code, Cursor, Cline, Aider, OpenHands, and Google's new Antigravity IDE.

GitHub: https://github.com/Bilal140202/the-lord-of-the-skills

What it does:
- 5-phase resumable crawler (seeds → BFS expansion → GitHub Search API → bulk clone → extract)
- Classifies each skill into 10 LOTR-themed kingdoms by keyword voting
- Deduplicates with canonical ⭐ marking (one best version per concept)
- Generates themed PDF catalog + Excel index
- Monthly cron auto-refresh

Total: 18,142 skills from 307+ repos, 357 canonical representatives.

Drop-in ready for your agent:
```bash
cp -r skills/gondor/claude-code/* ~/.claude/skills/   # Claude Code
cp -r skills/gondor/cursor/*     .cursor/rules/        # Cursor
cp -r skills/gondor/cline/*      .clinerules/          # Cline
```

The crawler is reusable — clone it and build your own kingdom. MIT licensed.

Feedback welcome!

---

## 🟧 Hacker News

**Title:** Show HN: The Lord of the Skills – Open-source crawler that compiled 18k+ AI agent skills from GitHub

**Body:**

Hi HN,

I built a Python crawler that spiders GitHub for AI agent skill files (SKILL.md, AGENTS.md, .cursorrules, .clinerules, CONVENTIONS.md, etc.) and compiles them into one organized library.

The motivation: AI agent skills are scattered across hundreds of GitHub repos with no unified index. If you use Claude Code, you have to find Claude skills. If you use Cursor, you hunt for cursorrules. If you switch to Cline, you start over. I wanted one catalog to rule them all.

The crawler is 5-phase and resumable:
1. Clone seed repos (248 hand-curated)
2. BFS-expand from READMEs (discovers ~2000 more repos)
3. GitHub Search API expansion (56 queries)
4. Bulk clone all discovered repos
5. Extract skill files using 24 regex patterns

Then a classifier tags each file into one of 10 LOTR-themed kingdoms (Gondor=Coding, Rivendell=Research, Mordor=Security, etc.) using weighted keyword voting. A dedup pass clusters similar skills and marks one canonical ⭐ per concept.

Results: 18,142 skills from 307+ repos across 14 frameworks. 357 canonical representatives.

The LOTR theme is partly for fun, partly for navigation — it's easier to remember "I need a Mordor skill for security" than "I need a skill tagged with security/audit/vulnerability keywords".

Tech: Python, requests, openpyxl, ReportLab. No external services. Runs in ~2 hours. ~5 GB disk for cached repos.

Repo (MIT): https://github.com/Bilal140202/the-lord-of-the-skills

I'd love feedback on:
- The dedup algorithm (currently Jaccard on tokenized summaries — should I use embeddings?)
- The kingdom taxonomy (10 kingdoms — too many? too few?)
- The crawler architecture (BFS from awesome-lists is the main discovery mechanism — better approaches?)

Thanks!

---

## 🐦 Twitter/X (thread)

**Tweet 1:**
⚔ Built "The Lord of the Skills" — the largest open-source compilation of AI agent skills on GitHub.

18,142+ skills · 14 frameworks · 307+ repos · 10 LOTR-themed kingdoms

One catalog to rule them all ↓

https://github.com/Bilal140202/the-lord-of-the-skills

**Tweet 2:**
The problem: AI agent skills are scattered across hundreds of GitHub repos. Claude Code skills here, Cursor rules there, Cline memory banks somewhere else.

The solution: a Python crawler that spiders all of GitHub and compiles them into one library.

**Tweet 3:**
The 10 kingdoms:

⚔ Gondor = Coding (10,141)
✦ Rivendell = Research (1,776)
⚙ Isengard = Agents (1,630)
✎ The Shire = Writing (1,272)
⛏ Moria = DevOps (914)
🐴 Rohan = Testing (718)
🌳 Fangorn = Memory (708)
✿ Lothlórien = Data (496)
👁 Mordor = Security (406)
🕸 Mirkwood = Specialized (81)

**Tweet 4:**
14 frameworks covered:

🟠 Claude Code
🟣 Cursor
🔵 Cline
⚫ Roo
🟢 Aider
🟡 OpenHands
⚫ Codex
🟤 Continue
⚪ Goose
🔵 Copilot
🟣 CrewAI
🟢 LangGraph
🟪 Google Antigravity (new!)
⚪ General

**Tweet 5:**
Drop-in ready for your agent:

```bash
# Claude Code
cp -r skills/gondor/claude-code/* ~/.claude/skills/

# Cursor
cp -r skills/gondor/cursor/* .cursor/rules/

# Cline
cp -r skills/gondor/cline/* .clinerules/
```

Or canonical ⭐ only (357 best skills):
```bash
find skills/ -name 'canonical__*' -exec cp {} ~/.claude/skills/ \;
```

**Tweet 6:**
The crawler is reusable and MIT-licensed.

5-phase resumable:
1. Clone seeds
2. BFS-expand
3. GitHub Search API
4. Bulk clone
5. Extract + classify + dedup

Run it yourself to build a custom kingdom:
```bash
cd crawler/
pip install -r requirements.txt
python3 crawler.py
```

**Tweet 7:**
Includes:
- 33-page themed PDF catalog
- 6-sheet Excel index (filterable)
- Monthly cron auto-refresh
- pytest tests + GitHub Actions CI
- Per-kingdom READMEs with stats

Star if useful: https://github.com/Bilal140202/the-lord-of-the-skills

May your agents be wise, your prompts be sharp, and your skills be many. ⚔

---

## 💼 LinkedIn

**Post:**

Excited to share a project I've been working on: **The Lord of the Skills** — an open-source compilation of 18,000+ AI agent skills from 307+ GitHub repositories, organized into 10 Lord of the Rings-themed kingdoms.

The problem I kept hitting: every AI agent framework (Claude Code, Cursor, Cline, Aider, OpenHands, etc.) has its own skill format scattered across hundreds of repos. There's no unified index. Switching frameworks means starting over.

So I built a Python crawler that:
- Spiders GitHub using 5-phase resumable architecture
- Extracts skills, agents, rules, and conventions from 14 framework formats
- Classifies each into 10 LOTR-themed kingdoms (Gondor=Coding, Rivendell=Research, Mordor=Security, etc.)
- Deduplicates with canonical ⭐ marking (one best version per concept)
- Generates themed PDF catalog + Excel index
- Auto-refreshes monthly via cron

Results: 18,142 skills, 357 canonical representatives, 14 frameworks including Google's new Antigravity IDE.

The crawler is fully reusable and MIT-licensed — clone it and build your own kingdom.

GitHub: https://github.com/Bilal140202/the-lord-of-the-skills

#AI #AgenticAI #OpenSource #Python #ClaudeCode #Cursor #LLM #AIAgents

---

## 📘 Dev.to / Medium (blog post outline)

**Title:** How I Built "The Lord of the Skills" — An Open-Source Crawler for 18,000+ AI Agent Skills

**Outline:**

1. **The Problem** — AI agent skills are scattered across hundreds of GitHub repos with no unified index
2. **The Solution** — A 5-phase Python crawler that spiders GitHub and compiles skills into a themed library
3. **Architecture Deep Dive**
   - Phase 1: Seed curation (248 hand-picked repos)
   - Phase 2: BFS expansion from READMEs (discovers 2000+ more)
   - Phase 3: GitHub Search API (56 queries)
   - Phase 4: Bulk git clone (disk-aware, resumable)
   - Phase 5: File extraction (24 regex patterns)
4. **Classification** — Weighted keyword voting into 10 LOTR kingdoms
5. **Deduplication** — Jaccard similarity + framework priority scoring for canonical ⭐ selection
6. **The LOTR Theme** — Why domain naming matters for navigation
7. **Results** — 18,142 skills, 357 canonical, 14 frameworks
8. **Lessons Learned** — Disk management, rate limiting, filename safety, BFS cap tuning
9. **What's Next** — Embeddings-based search, web UI, MCP server
10. **Call to Action** — Star the repo, contribute skills, run the crawler yourself

---

## 📌 Awesome-List Submissions

Submit to these awesome-lists (open PRs adding the repo):

1. **awesome-ai-agents** (`e2b-dev/awesome-ai-agents`)
   ```markdown
   - [The Lord of the Skills](https://github.com/Bilal140202/the-lord-of-the-skills) - 18,142+ AI agent skills from 14 frameworks, organized into 10 LOTR-themed kingdoms. Includes reusable crawler.
   ```

2. **awesome-claude-code** (`hesreallyhim/awesome-claude-code`)
   ```markdown
   - [The Lord of the Skills](https://github.com/Bilal140202/the-lord-of-the-skills) - Compilation of 8,100+ Claude Code skills (plus 13 other frameworks) organized by domain.
   ```

3. **awesome-cursorrules** (`biuo/awesome-cursorrules`)
   ```markdown
   - [The Lord of the Skills](https://github.com/Bilal140202/the-lord-of-the-skills) - 1,400+ Cursor rules compiled from across GitHub, organized by domain kingdom.
   ```

4. **awesome-mcp-servers** (`punkpeye/awesome-mcp-servers`)
   - Submit only if we add an MCP server (planned for v2.0.0)

---

## 📊 Promotion Checklist

- [ ] Post to r/MachineLearning
- [ ] Post to r/artificial
- [ ] Submit to Hacker News (Show HN)
- [ ] Post Twitter/X thread
- [ ] Post on LinkedIn
- [ ] Write Dev.to/Medium blog post
- [ ] Submit PR to awesome-ai-agents
- [ ] Submit PR to awesome-claude-code
- [ ] Submit PR to awesome-cursorrules
- [ ] Share in Discord/Slack AI communities
- [ ] Email AI newsletters (TLDR AI, Import AI, etc.)

---

<div align="center">

*The word of the kingdom spreads across the lands.*

</div>
