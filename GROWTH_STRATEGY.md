# 🚀 Growth Strategy — Making The Lord of the Skills Popular & Discoverable

> *How to make this repo rank on Google, get recommended by LLMs, and attract stars, forks, and contributors.*

---

## 📊 Current State (July 2026)

| Metric | Value |
|:---|:---|
| GitHub stars | ~1 |
| PyPI downloads | New (v1.3.5) |
| Google search presence | Low (only GitHub + PyPI pages indexed) |
| LLM awareness | Zero (not in training data yet) |
| Community | 1 external contributor (manavsep) |

**Goal:** 500+ stars in 30 days, 2000+ in 90 days, recommended by ChatGPT/Claude when users ask about AI agent skills.

---

## 🎯 Strategy 1: GitHub SEO (Do This Week)

Google indexes GitHub repos with high domain authority. Your README.md IS your SEO landing page.

### 1.1 Optimize the Repo Description (DONE — verify current)

**Current:** `⚔ 17,000+ AI agent skills from 307+ GitHub repos across 14 frameworks... pip install lotr-skills`

**Checklist:**
- [x] Contains primary keyword ("AI agent skills")
- [x] Contains install command ("pip install lotr-skills")
- [x] Under 350 chars (GitHub limit)
- [ ] Add "cursor rules" and "claude code" — these are the #1 searched terms
- [ ] Add "lotr" for brand recognition

**Suggested update:**
```
⚔ AI agent skills installer — 17,000+ skills for Claude Code, Cursor, Cline, Aider, Codex & Antigravity. pip install lotr-skills. LOTR-themed. cursor rules, claude code skills, agent rules.
```

### 1.2 Optimize GitHub Topics (20 max — we have 20)

**Current topics:** `agentic-ai`, `ai-agents`, `aider`, `antigravity`, `awesome-list`, `claude-code`, `cline`, `codex`, `compilation`, `crewai`, `cursor`, `cursor-rules`, `cursorrules`, `langgraph`, `llm`, `lotr`, `mcp`, `openhands`, `prompt-engineering`, `rules`, `skills`

**Missing high-search topics to consider swapping in:**
- `ai-coding` (trending)
- `developer-tools` (broad reach)
- `skill-md` (was removed — consider re-adding)
- `cursor-ai` (alternative to "cursor")
- `ai-agent-framework` (broad)

### 1.3 README Keyword Optimization

Google indexes your README.md. The first 200 words are critical.

**Keywords users search for that should appear in README:**
- "AI agent skills" ✅ (in title + description)
- "cursor rules" ✅ (in topics + body)
- "claude code skills" ✅ (in body)
- "SKILL.md" ✅ (in body)
- "AGENTS.md" ✅ (in body)
- "ai coding assistant" — **ADD THIS**
- "skill installer" — **ADD THIS**
- "agent rules" — **ADD THIS**
- "cursorrules collection" — **ADD THIS**

**Action:** Add a "Keywords" section at the bottom of README (hidden in `<details>` tag) with all search terms.

### 1.4 Custom Social Preview (DONE)

- [x] Generated 1280×640 social preview at `assets/social/social-preview.png`
- [ ] **Manual step:** Upload via Settings → Social preview

This affects every Twitter/X, LinkedIn, Reddit, and Slack share.

---

## 🤖 Strategy 2: LLM Discoverability (Do This Month)

LLMs (ChatGPT, Claude, Perplexity, GitHub Copilot) discover tools through 3 channels:

### 2.1 Training Data (Long-term)

LLMs are trained on web crawls. To get into the next training cycle:
- Get mentioned on high-traffic sites (Reddit, HN, Dev.to, Medium)
- Get added to awesome-lists (these are crawled heavily)
- Have a PyPI page (pypi.org is crawled — ✅ done)
- Get backlinks from popular repos

**Timeline:** Next LLM training cycle (3-6 months). Content created now will be in the next GPT/Claude training data.

### 2.2 Web Search (Immediate — for Perplexity, ChatGPT Search, Google AI)

When users ask "what's the best AI skills installer?", LLMs with web search look for:
1. **PyPI page** — `pypi.org/project/lotr-skills/` ✅ (done)
2. **GitHub repo** — indexed by Google ✅ (done)
3. **Blog posts** mentioning the tool — **NONE YET** ❌
4. **Reddit threads** mentioning the tool — **NONE YET** ❌
5. **Awesome-list entries** — **NONE YET** ❌

**Action items:**
- [ ] Write a Dev.to article: "How I built an AI skills installer for 14 frameworks"
- [ ] Write a Medium article: "The Lord of the Skills — a LOTR-themed AI agent skills catalog"
- [ ] Submit PRs to: `awesome-ai-agents`, `awesome-claude-code`, `awesome-cursorrules`, `awesome-mcp-servers`
- [ ] Post on Reddit (see Strategy 4)

### 2.3 AI-Citable Documentation

LLMs cite sources that are:
- **Structured** (clear headings, tables, code blocks)
- **Factual** (specific numbers, not vague claims)
- **Self-contained** (answer is complete on one page)
- **Recent** (date stamps matter)

**Our docs are already good at this.** To improve:
- [ ] Add a `## What is lotr-skills?` section at the very top of README with a 2-sentence factual answer
- [ ] Add schema.org `SoftwareApplication` markup to a GitHub Pages landing page
- [ ] Add a `## Quick Facts` table with: name, version, license, PyPI URL, GitHub URL, install command

### 2.4 The "Cassidoo Trick"

Ask ChatGPT/Claude/Perplexity: *"What tools exist for installing AI agent skills?"*

If they don't mention lotr-skills:
1. Create content that fills the gap (blog post, Dev.to)
2. Get that content cited by other sites
3. Re-ask in 2 weeks — LLMs with web search will pick it up

---

## 🔍 Strategy 3: Google Search Optimization

### 3.1 What Google Indexes from GitHub

| Element | Indexed? | Optimization |
|:---|:---:|:---|
| Repo name | ✅ | `the-lord-of-the-skills` — good, unique |
| Description | ✅ | Already optimized with keywords |
| Topics | ✅ | 20 topics, well-chosen |
| README.md | ✅ | **Most important** — this IS your landing page |
| Releases page | ✅ | 9 releases — good signal |
| PyPI page | ✅ | `pypi.org/project/lotr-skills/` — separate domain, ranks independently |
| Issues/Discussions | ✅ | 5 issues, 3 discussions — activity signal |

### 3.2 Backlink Strategy

Google ranks based on backlinks. Each backlink from a high-DA site is worth gold:

| Source | Domain Authority | Action |
|:---|---:|:---|
| PyPI.org | 92 | ✅ Done (pypi.org/project/lotr-skills/) |
| GitHub.com | 96 | ✅ Done (repo page) |
| Dev.to | 89 | ❌ Write article |
| Medium.com | 95 | ❌ Write article |
| Reddit.com | 91 | ❌ Post on r/MachineLearning |
| Hacker News | 90 | ❌ Submit Show HN |
| Awesome-lists (GitHub) | 96 | ❌ Submit 4 PRs |
| npmjs.com | 89 | ❌ Consider npm package (JS port) |
| Product Hunt | 88 | ❌ Launch when ready |

**Target:** 10+ backlinks from DA 85+ sites in 30 days.

### 3.3 GitHub Pages Landing Page (High Impact)

Create a GitHub Pages site at `https://bilal140202.github.io/the-lord-of-the-skills/` with:
- Landing page with install command, demo GIF, and structured data
- `schema.org/SoftwareApplication` markup
- Open Graph tags for social sharing
- A sitemap.xml for Google Search Console

This gives you a **second indexed page** (separate from the repo) that you fully control.

### 3.4 Google Search Console

- [ ] Verify the GitHub Pages site in Google Search Console
- [ ] Submit sitemap.xml
- [ ] Monitor which queries bring traffic
- [ ] Track impressions + clicks over time

---

## 📣 Strategy 4: Social Distribution (Do This Week)

### 4.1 Reddit (Highest ROI)

| Subreddit | Subscribers | Best Post Type | Timing |
|:---|---:|:---|:---|
| r/ClaudeAI | 150k+ | "I built a CLI that installs Claude Code skills in 1 command" | Tuesday 9am EST |
| r/LocalLLaMA | 200k+ | "18k+ AI agent skills organized into 11 LOTR kingdoms" | Wednesday 10am EST |
| r/cursor | 50k+ | "5,600+ cursor rules + automatic installer CLI" | Thursday 9am EST |
| r/MachineLearning | 2M+ | Technical deep-dive on the crawler architecture | Friday 8am EST |
| r/artificial | 500k+ | "pip install lotr-skills — one command for all your AI agent skills" | Saturday 10am EST |
| r/LocalLLaMA | 200k+ | Cross-post from r/ClaudeAI if it performs well | Same day |

**Reddit posting rules:**
- Post title ≤ 100 chars
- Body: show, don't tell (code blocks, output screenshots)
- Always link to GitHub + PyPI
- Respond to every comment within 1 hour
- Don't cross-post the same day — wait 2 days between subreddits

### 4.2 Hacker News (Show HN)

**Title:** `Show HN: The Lord of the Skills – CLI that installs AI agent skills for 14 frameworks`

**Body:** 3-4 sentences about what it does, why you built it, and a link. Don't over-explain — HN readers are technical.

**Timing:** Tuesday-Thursday, 8-9am PST (US morning).

### 4.3 Twitter/X Thread

7-tweet thread (templates already in `docs/promotion/` — sent to your Telegram):
1. Hook: "I built a CLI that installs AI agent skills in 1 command"
2. Problem: skills are scattered across 300+ GitHub repos
3. Solution: lotr detects your framework + downloads only what you need
4. Demo: `lotr "write unit tests"` → 3 skills in 1 second
5. Stats: 17k skills, 14 frameworks, 11 kingdoms
6. Install: `pip install lotr-skills`
7. CTA: star the repo

### 4.4 Dev.to Article

**Title:** "How I built an AI skills installer for 14 frameworks (LOTR-themed)"

**Structure:**
1. The problem (skills are scattered)
2. The architecture (crawler → classifier → dedup → CLI)
3. The LOTR theme (why it matters for navigation)
4. Live demo with screenshots
5. `pip install lotr-skills` call to action

### 4.5 Discord Communities

| Server | Action |
|:---|:---|
| Cursor Discord | Share in #showcase or #community |
| Claude Code community | Share in relevant channel |
| Cline Discord | Share as "Cline-compatible skill installer" |
| Antigravity community | Share as "the only skills catalog covering Antigravity" |

---

## 📋 Strategy 5: Awesome-List Submissions

Submit PRs to these lists (each is a permanent backlink from a DA 96 domain):

| Awesome List | PR Title | Status |
|:---|:---|:---|
| `e2b-dev/awesome-ai-agents` | Add lotr-skills — 17k+ skills across 14 frameworks | ❌ Pending |
| `hesreallyhim/awesome-claude-code` | Add lotr-skills — CLI installer for Claude Code skills | ❌ Pending |
| `biuo/awesome-cursorrules` | Add lotr-skills — 1,400+ cursor rules + installer | ❌ Pending |
| `punkpeye/awesome-mcp-servers` | Add lotr-skills — MCP server (when built) | ❌ Deferred |
| `shobro/awesome-aider` | Add lotr-skills — Aider CONVENTIONS.md installer | ❌ Pending |

**PR template:**
```markdown
- [The Lord of the Skills](https://github.com/Bilal140202/the-lord-of-the-skills) — CLI installer for 17,000+ AI agent skills across 14 frameworks. `pip install lotr-skills`. LOTR-themed.
```

---

## 📈 Strategy 6: Analytics & Measurement

### 6.1 Track These Metrics Weekly

| Metric | Tool | Target (30 days) |
|:---|:---|:---|
| GitHub stars | GitHub Insights | 500+ |
| PyPI downloads | pypistats.org | 1,000+ |
| Google impressions | Search Console | 1,000+ |
| Reddit upvotes | Manual | 100+ total |
| Backlinks | Google Search Console | 10+ |
| npm/package installs | pip stats | 500+ unique |

### 6.2 Tools to Set Up

- [ ] Google Search Console (verify GitHub Pages site)
- [ ] pypistats.org tracking (automatic for PyPI packages)
- [ ] GitHub traffic insights (automatic — Settings → Insights)
- [ ] Star-history.com tracking (already embedded in README)

---

## 🏗 Strategy 7: Technical SEO Actions

### 7.1 GitHub Pages Landing Page

```yaml
# .github/workflows/pages.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

Landing page at `site/index.html` with:
- `SoftwareApplication` schema.org markup
- Open Graph + Twitter Card meta tags
- Install command prominently displayed
- Demo GIF
- Link to GitHub repo + PyPI

### 7.2 Structured Data (Schema.org)

Add to GitHub Pages landing page:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "The Lord of the Skills",
  "applicationCategory": "DeveloperTool",
  "operatingSystem": "Cross-platform",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "description": "CLI installer for 17,000+ AI agent skills across 14 frameworks",
  "url": "https://github.com/Bilal140202/the-lord-of-the-skills",
  "installUrl": "https://pypi.org/project/lotr-skills/",
  "softwareVersion": "1.3.5",
  "license": "https://github.com/Bilal140202/the-lord-of-the-skills/blob/main/LICENSE"
}
</script>
```

### 7.3 PyPI Page Optimization

The PyPI page (`pypi.org/project/lotr-skills/`) is a separate indexed page. Optimize:
- [x] Good description in pyproject.toml
- [x] Keywords in pyproject.toml
- [x] Links to GitHub repo
- [ ] Add long_description (renders as PyPI page content) — currently using README.md
- [ ] Add classifiers for discoverability (already have 15 classifiers)

---

## 📅 30-Day Action Plan

### Week 1: Foundation (Do Now)
1. ✅ Update GitHub description with all keywords
2. ✅ Verify 20 topics are optimal
3. ❌ Upload social preview image (Settings → Social preview)
4. ❌ Submit PRs to 5 awesome-lists
5. ❌ Post on r/ClaudeAI

### Week 2: Content
6. ❌ Write Dev.to article
7. ❌ Post on r/cursor
8. ❌ Submit Show HN
9. ❌ Create GitHub Pages landing page with schema.org markup
10. ❌ Verify site in Google Search Console

### Week 3: Amplification
11. ❌ Post on r/LocalLLaMA
12. ❌ Post Twitter/X thread
13. ❌ Post on LinkedIn
14. ❌ Reach out to Antigravity community (antigravity-ide.com)
15. ❌ Share in Discord servers (Cursor, Claude, Cline)

### Week 4: Measure & Iterate
16. ❌ Check Google Search Console for impressions
17. ❌ Check pypistats.org for download trends
18. ❌ Ask ChatGPT/Claude "what tools exist for AI agent skills?" — see if we appear
19. ❌ Write follow-up Dev.to article based on feedback
20. ❌ Plan v2.0 features based on user requests

---

## 🎯 Success Metrics (90-Day Targets)

| Metric | 30 Days | 60 Days | 90 Days |
|:---|---:|---:|---:|
| GitHub stars | 500 | 1,500 | 3,000 |
| PyPI downloads | 1,000 | 5,000 | 15,000 |
| Google impressions | 1,000 | 10,000 | 50,000 |
| Backlinks | 10 | 30 | 75 |
| LLM mentions | 0 | 1-2 | 5+ |
| Contributors | 2 | 5 | 10 |
| Awesome-list entries | 3 | 5 | 8 |

---

## 🔑 Key Insight

**The #1 thing that will make this repo popular is the `lotr design` command.** The Taste Skill (59k stars) proves that the design-skills community is actively looking for tools like this. Post on r/webdev and r/Frontend about "a CLI that installs design skills for your AI agent" — that community is hungry for this.

**The #2 thing is the Antigravity angle.** We're the ONLY skills catalog covering Google Antigravity. That's a defensible, unique claim. Post in Antigravity communities — they're starved for tooling.

---

*This strategy document is a living document. Update it as metrics come in.*
