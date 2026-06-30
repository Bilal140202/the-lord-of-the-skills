# Workflow: Post to All Platforms

> Full multi-platform social media posting workflow.
> Draft -> Approve -> Post pattern.

---

## Objective
Post content to LinkedIn, X, Instagram, and/or YouTube with platform-optimized formatting.

## Inputs
- **Content:** Topic (AI mode) OR raw text (manual mode) OR URL to adapt
- **Media:** Local image/video path OR AI-generated
- **Platforms:** Which platforms to target (default: linkedin, x)

## Steps

### Step 1: Generate Content
```bash
# AI mode — give a topic, AI creates platform-optimized posts
python tools/content_engine.py --topic "Your topic here" --platforms linkedin,x,instagram

# Manual mode — adapt your text for each platform
python tools/content_engine.py --text "Your raw content" --platforms linkedin,x

# With extra instructions
python tools/content_engine.py --topic "AI agents" --platforms linkedin,x --instructions "Be controversial"
```

### Step 2: Review Draft
```bash
# List all drafts
python tools/draft_manager.py --list

# Show specific draft with full content
python tools/draft_manager.py --show <draft_id>
```

### Step 3: Edit (if needed)
Open `.tmp/drafts/<draft_id>.json` and edit the text directly.

### Step 4: Add Media (if needed)
Edit the draft JSON to add image/video paths:
```json
{
  "posts": {
    "linkedin": {
      "text": "...",
      "media": ["/path/to/image.jpg"]
    }
  }
}
```

### Step 5: Approve
```bash
# Approve for all platforms
python tools/draft_manager.py --approve <draft_id>

# Approve for specific platforms only
python tools/draft_manager.py --approve <draft_id> --platforms linkedin,x
```

### Step 6: Post
```bash
python tools/draft_manager.py --post <draft_id>
```

### Step 7: Verify
Check the run log: `runs/YYYY-MM-DD-social-post.md`

---

## Direct Posting (Skip Draft Flow)

For quick posts without the draft flow:

```bash
# LinkedIn
python tools/linkedin_poster.py --text "Hello LinkedIn!" --image /path/to/image.jpg

# X / Twitter
python tools/x_poster.py --text "Hello X!" --image /path/to/image.jpg

# Instagram (requires public URL for image)
python tools/instagram_poster.py --caption "Hello Instagram!" --image "https://example.com/photo.jpg"

# YouTube
python tools/youtube_uploader.py --video /path/to/video.mp4 --title "My Video" --description "..."
```

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Token expired | Refresh OAuth tokens |
| 403 Forbidden | Missing scopes/permissions | Check app permissions |
| 429 Rate Limited | Too many requests | Wait and retry |
| Instagram: needs public URL | Local file won't work | Upload image to hosting first |
| YouTube: quota exceeded | 10K units/day used | Wait 24h or use different project |

---

## Cost
- LLM calls (content generation): ~$0.001-0.01 per post via Euri (free) or OpenRouter
- API calls: Free (within platform rate limits)
- Total: Effectively $0 per post
