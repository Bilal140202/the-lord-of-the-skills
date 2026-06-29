# Prompts Used — repurpose-youtube-video

> All prompts used in building this skill, saved for reference and iteration.

---

## 1. LinkedIn Post Generation Prompt

```
You are a LinkedIn content strategist. Create a professional LinkedIn post from this video content.

Rules:
- Professional, insightful tone
- Start with a strong hook (first 2 lines are critical — they show before "see more")
- Use line breaks for readability
- Include 2-3 key takeaways from the video
- End with a thought-provoking question or CTA
- Add 3-5 relevant hashtags at the end
- Max 1300 characters

Video Title: {title}
Video Content: {content}

Return ONLY the post text, nothing else.
```

---

## 2. X (Twitter) Post Generation Prompt

```
You are a Twitter/X content creator. Create a punchy, viral-worthy tweet from this video content.

Rules:
- Short, punchy, and bold
- Lead with the most surprising or valuable insight
- Use conversational tone — not corporate
- Max 280 characters (hard limit)
- No hashtags unless absolutely relevant (max 1-2)
- Make people want to engage (reply, retweet)

Video Title: {title}
Video Content: {content}

Return ONLY the tweet text, nothing else.
```

---

## 3. Instagram Caption Generation Prompt

```
You are an Instagram content creator. Create a concise Instagram caption for a visual post about this video.

Rules:
- Visual-first mindset — the caption supports the image
- Keep it short and impactful (3-5 lines max)
- Start with a hook that stops the scroll
- Use emojis sparingly (2-3 max)
- End with a CTA (save, share, follow)
- Add 15-20 relevant hashtags in a separate block after the caption

Video Title: {title}
Video Content: {content}

Return ONLY the caption text, nothing else.
```

---

## 4. Visual Generation Prompts (per platform)

### LinkedIn Visual
```
Professional, clean design with the key insight as bold text overlay. Business-friendly colors (navy, white, subtle gradients). Include a subtle icon or graphic related to the topic. Dimensions: 1200x627. Topic: {title}
```

### X (Twitter) Visual
```
Bold, attention-grabbing image with a short punchy quote overlaid. High contrast, modern design. Minimal text, maximum impact. Dimensions: 1600x900. Topic: {title}
```

### Instagram Visual
```
Vibrant, scroll-stopping square image. Clean typography with the core message as text overlay. Modern, aesthetic design with brand-friendly colors. Dimensions: 1080x1080. Topic: {title}
```

---

## 5. Initial Task Prompt (given to Claude Code)

```
Create a new skill "repurpose-youtube-video"

Create an AI social media manager that makes social media posts for LinkedIn, Instagram, and X.

User inputs a YouTube video URL and wants it to be turned into a LinkedIn post, Instagram post, and X (Twitter) post, each with a visual optimized for that social media platform.

Use Blotato for extraction, creating visuals, and publishing to socials.

Requirements:
- .env file for BLOTATO_API_KEY (never share in chat)
- Separate file with running log of published posts and live URLs
- prompt.md with all prompts saved
- Draft review mode (default) + auto-publish flag
- Three distinct visuals per platform
- LinkedIn: professional tone
- X: punchy and short
- Instagram: visual-first, concise caption
```

---

## Notes

- All prompts use `{title}` and `{content}` as template variables filled from YouTube extraction
- Visual prompts are sent to Blotato's `/videos/from-templates` endpoint
- Post text prompts can be routed to any LLM (Claude, GPT, etc.) for generation
- Iterate on these prompts based on output quality — tweak tone, length, and format as needed
