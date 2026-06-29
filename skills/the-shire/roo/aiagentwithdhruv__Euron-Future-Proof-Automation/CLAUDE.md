# Social-Media-Automations — Automation Rules

> Inherits from the parent `CLAUDE.md` at project root.

---

## Project

- **Name:** Social-Media-Automations
- **Objective:** Post to LinkedIn, X, Instagram, and YouTube with AI content generation, media support, and draft-approve-post workflow
- **Phase:** 6 (Industry Playbooks — Marketing Automation)
- **Status:** In Progress

---

## Architecture

```
User Input (text / topic / URL + media)
  |
  v
Content Engine -----> AI generates platform-optimized content (optional)
  |                   OR user provides raw content
  v
Platform Adapter ---> Formats text/media per platform rules
  |                   (char limits, hashtags, image sizes, etc.)
  v
Draft Storage ------> Saves draft to .tmp/drafts/ for review
  |
  v
Approval ----------> User reviews, edits, approves
  |
  v
Platform Connectors -> Posts via direct APIs
  |                    LinkedIn API v2
  |                    X/Twitter API v2
  |                    Instagram Graph API (Meta)
  |                    YouTube Data API v3
  v
Post Log -----------> Logs to runs/ with post IDs, timestamps, status
```

### Agentic Loop
1. **Sense:** User provides content/topic + media
2. **Think:** AI generates platform-optimized posts (if auto mode)
3. **Decide:** User reviews drafts and approves
4. **Act:** Post to selected platforms via direct APIs
5. **Learn:** Log results, track engagement (Phase 2)

---

## Platform Details

### LinkedIn (Direct API v2)
- **Auth:** OAuth 2.0 (3-legged)
- **Can post:** Text, images, articles, documents
- **Char limit:** 3,000 characters
- **Image:** JPG/PNG, max 10MB, recommended 1200x627

### X / Twitter (Direct API v2)
- **Auth:** OAuth 1.0a (user context)
- **Can post:** Text, images (up to 4), videos
- **Char limit:** 280 characters
- **Image:** JPG/PNG/GIF, max 5MB, recommended 1600x900
- **Free tier:** 1,500 tweets/month

### Instagram (Meta Graph API)
- **Auth:** OAuth 2.0 via Meta (Facebook Business Page + IG Professional account)
- **Can post:** Single image, carousel (up to 10), reels (video up to 90s)
- **Image:** JPG, max 8MB, 1080x1080 or 1080x1350
- **Complexity:** HIGH — Facebook Page + IG Business/Creator account required

### YouTube (Data API v3)
- **Auth:** OAuth 2.0 (Google Cloud Console)
- **Can upload:** Videos with title, description, tags, thumbnail
- **Quota:** 10,000 units/day (~6 uploads/day)
- **Shorts:** Vertical video under 60 seconds

---

## Tech

| Layer | Choice |
|-------|--------|
| **Backend** | Python 3.11+ |
| **AI Model** | OpenRouter (Claude Sonnet) or Euri (free) |
| **Media** | Local files + AI generation (FLUX/Gemini) |
| **Storage** | Local JSON drafts in `.tmp/drafts/` |
| **Deploy** | Local CLI first, then GitHub Actions for scheduling |

---

## File Structure

```
Social-Media-Automations/
├── CLAUDE.md
├── PROMPTS.md
├── README.md
├── .env.example
├── config/
│   └── platforms.yaml      # Platform settings, char limits, image sizes
├── tools/
│   ├── content_engine.py   # AI content generation (topic -> posts)
│   ├── media_handler.py    # Image/video handling + AI generation
│   ├── draft_manager.py    # Save, list, edit, approve drafts
│   ├── linkedin_poster.py  # LinkedIn API v2 connector
│   ├── x_poster.py         # X/Twitter API v2 connector
│   ├── instagram_poster.py # Instagram Graph API connector
│   └── youtube_uploader.py # YouTube Data API v3 connector
├── workflows/
│   ├── post-to-all.md      # Full multi-platform posting workflow
│   └── generate-content.md # AI content generation workflow
├── runs/                   # Post logs
└── .tmp/
    ├── drafts/             # Draft posts awaiting approval
    └── media/              # Processed media files
```

---

## Workflow: Draft -> Approve -> Post

1. **Create:** `python tools/content_engine.py --topic "AI agents" --platforms linkedin,x,instagram`
2. **Review:** `python tools/draft_manager.py --list`
3. **Approve:** `python tools/draft_manager.py --approve <draft_id> --platforms linkedin,x`
4. **Post:** Approved drafts get posted via platform connectors
5. **Log:** Results saved to `runs/YYYY-MM-DD-post.md`

---

## Phase 2: NotebookLM Integration

After core posting works:
- Connect NotebookLM MCP for research/content sourcing
- Generate posts from NotebookLM research summaries

---

## Inherited Rules

All rules from parent CLAUDE.md apply:
- 3-layer separation (Agent -> Workflows -> Tools)
- Security guardrails (14 non-negotiable)
- Budget protection ($2/run, $5/day)
- Self-improvement loop
- Tool-first execution
