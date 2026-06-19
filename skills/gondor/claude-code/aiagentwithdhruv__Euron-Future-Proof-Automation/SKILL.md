---
name: ghost-browser
description: AI-powered browser automation with human-like behavior — LinkedIn, Twitter, Indeed, GMaps, GitHub, HackerNews, MonkeyType
argument-hint: --agents linkedin,indeed --visible
---

# Ghost Browser — AI-Powered Browser Automation

> The browser moves on its own. No human needed.

**GitHub:** https://github.com/aiagentwithdhruv/ghost-browser
**Path:** `Social-Media-Agent-1.0/browser-automation/`
**Stack:** Python 3, Playwright, OpenAI API

---

## What It Does

Automates any browser action with human-like behavior — LinkedIn posting, engagement, job applications, web scraping, stats tracking, and visual demos.

---

## Schema

### Inputs

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `LINKEDIN_LI_AT` | string | For LinkedIn | LinkedIn `li_at` cookie from DevTools |
| `TWITTER_AUTH_TOKEN` | string | For Twitter | Twitter auth_token cookie |
| `TWITTER_CT0` | string | For Twitter | Twitter ct0 cookie |
| `YOUTUBE_API_KEY` | string | For YouTube | Google Cloud API key (free) |
| `OPENAI_API_KEY` | string | For AI comments | GPT-4o-mini for comment/cover letter generation |

### Outputs

| Name | Type | Description |
|------|------|-------------|
| LinkedIn post | Action | Published post with optional image |
| Feed data | JSON | Posts from LinkedIn feed with author, content, URN |
| Job listings | JSON | Jobs from LinkedIn/Indeed with title, company, description |
| Scraped data | JSON/CSV | Data from any website (smart/full/selector modes) |
| Stats | JSON + MD | Followers, views, connections across all platforms |
| Screenshots | PNG | Any URL, full page or element |

### Credentials

| Service | How to Get |
|---------|-----------|
| LinkedIn li_at | DevTools → Application → Cookies → linkedin.com |
| Twitter auth_token + ct0 | DevTools → Application → Cookies → x.com |
| YouTube API | Google Cloud Console → YouTube Data API v3 (FREE) |
| OpenAI | platform.openai.com → API Keys |

### Cost

| Component | Cost |
|-----------|------|
| Playwright/Chromium | Free |
| YouTube API | Free (10K units/day) |
| OpenAI (comments) | ~$0.01 per comment |
| LinkedIn/Twitter | Free (cookie auth) |

---

## Scripts Reference

| Script | What It Does | Example Command |
|--------|-------------|----------------|
| `orchestrator.py` | Multi-agent orchestrator (8 agents, 5 combos) | `python3 orchestrator.py --demo --visible` |
| `ghost_mcp.py` | MCP server (10 tools for any AI agent) | `python3 ghost_mcp.py` (stdio transport) |
| `multi_context.py` | Isolated browser session manager | Used by orchestrator |
| `linkedin_engage.py` | LinkedIn CLI — post, feed, engage, apply, connect | `python3 linkedin_engage.py post --text "Hello" --image photo.jpg --visible` |
| `universal_scraper.py` | Scrape any website with 6 presets | `python3 universal_scraper.py indeed --query "AI engineer" --output jobs.json` |
| `stats_tracker.py` | Pull stats from all platforms | `python3 stats_tracker.py --notify` |
| `demo_wow.py` | 6-stage visual demo (viral) | `python3 demo_wow.py` |
| `monkeytype_flex.py` | Speed typing demo (412 WPM) | `python3 monkeytype_flex.py` |
| `job_research.py` | Browse AI jobs on LinkedIn + Indeed | `python3 job_research.py` |
| `screenshot_tool.py` | Screenshot any URL | `python3 screenshot_tool.py --url "https://example.com"` |

---

## Architecture (v2.0)

```
human_behavior.py          ← Anti-detection layer (mouse drift, idle, warmup)
    ↓
base_browser.py            ← Playwright wrapper (cookie auth, context manager)
multi_context.py           ← Isolated browser sessions (multiple contexts, 1 process)
    ↓
orchestrator.py            ← 8 agents, 5 combos, CLI
    ├── agent_linkedin_feed / agent_linkedin_engage
    ├── agent_scrape_indeed / agent_scrape_gmaps
    ├── agent_twitter_trending (cookie auth: TWITTER_AUTH_TOKEN + TWITTER_CT0)
    ├── agent_monkeytype / agent_github_trending / agent_hacker_news
    └── run_orchestrator() → parallel execution in isolated contexts
    ↓
ghost_mcp.py               ← MCP server (10 tools) for Claude/Cursor/Codex
    ↓
├── linkedin_browser.py    ← LinkedIn: post, like, comment, apply, connect
├── linkedin_scraper.py    ← LinkedIn: followers, connections, analytics
├── twitter_scraper.py     ← Twitter: followers, impressions
├── youtube_stats.py       ← YouTube API (no browser)
├── universal_scraper.py   ← Any website (6 presets)
└── screenshot_tool.py     ← Screenshots
    ↓
├── linkedin_engage.py     ← CLI for LinkedIn
├── stats_tracker.py       ← Stats + Telegram notifications
├── demo_wow.py            ← Viral demo
└── job_research.py        ← Job market research
```

### Agents & Combos (v2.0)

| Agent | Description |
|-------|-------------|
| `linkedin-feed` | Scroll feed, extract posts |
| `linkedin-engage` | Like posts with human behavior |
| `indeed` | Scrape Indeed job listings |
| `gmaps` | Scrape Google Maps businesses |
| `monkeytype` | Speed typing demo (~400 WPM) |
| `github` | Browse GitHub trending repos |
| `hackernews` | Read top Hacker News stories |
| `twitter` | Scrape X.com trending/search (cookie auth) |

| Combo | Agents |
|-------|--------|
| `demo` | monkeytype, github, hackernews |
| `research` | linkedin-feed, indeed, github, twitter |
| `lead-gen` | linkedin-feed, gmaps, indeed |
| `social` | linkedin-feed, twitter, hackernews |
| `full` | all 6 non-demo agents |

### MCP Server (10 tools)

```json
{
    "mcpServers": {
        "ghost-browser": {
            "command": "python3",
            "args": ["/path/to/ghost_mcp.py"],
            "env": { "LINKEDIN_LI_AT": "...", "OPENAI_API_KEY": "sk-..." }
        }
    }
}
```

Tools: linkedin_feed, linkedin_post, linkedin_engage, scrape_url, scrape_indeed, scrape_gmaps, scrape_twitter, typing_demo, screenshot, multi_run

---

## Human-Like Behavior Rules

| Behavior | Implementation |
|----------|---------------|
| Typing | 40-55 WPM, char-by-char, 3-5% typo rate with backspace correction |
| Delays | Gaussian distribution (not uniform) — clusters around midpoint |
| Scrolling | Sinusoidal speed curve — slow start, fast middle, slow end |
| Clicking | Random offset from center (not dead-center like bots) |
| Reading | Wait time proportional to word count |
| Breaks | 30-120 sec pause every 15-25 actions |
| Viewport | Random from pool: 1440x900, 1920x1080, 1536x864, etc. |

---

## LinkedIn Post Flow

```
1. Navigate to feed
2. Click "Start a post"
3. Find Quill editor (contenteditable div)
4. Short posts (<200 chars) → human_type with typos
   Long posts (>200 chars) → insert_text (paste)
5. Attach image → file input upload
6. Click "Next" (LinkedIn image editor step)
7. Click "Post" → confirmed
```

---

## Composable With

| Skill | How |
|-------|-----|
| `scrape-leads` | Scrape → enrich with ghost-browser LinkedIn data |
| `instantly-campaigns` | Scrape leads → cold email |
| `gmaps-leads` | Google Maps preset in universal_scraper |
| `cross-niche-outliers` | Research content → auto-post to LinkedIn |
| `upwork-apply` | Job research data feeds Upwork proposals |
| `send-telegram` | Stats tracker sends notifications |

---

## Revenue Use Cases

| Use Case | Revenue |
|----------|---------|
| LinkedIn automation service | $500-2000/mo per client |
| Web scraping gigs (Fiverr/Upwork) | $200-1000 per project |
| LinkedIn ghostwriting + auto-post | $500-1500/mo per client |
| AI job application bot | $50-200 per person |
| Lead generation (scrape → email) | $500-2000/mo per client |

---

## Quick Start

```bash
cd Social-Media-Agent-1.0/browser-automation
pip install -r requirements.txt
playwright install chromium
cp .env.example .env  # Add your cookies

# Run the viral demo
python3 demo_wow.py

# Post to LinkedIn
python3 linkedin_engage.py post --text "Hello world" --visible

# Scrape Indeed jobs
python3 universal_scraper.py indeed --query "AI engineer" --output jobs.json
```
