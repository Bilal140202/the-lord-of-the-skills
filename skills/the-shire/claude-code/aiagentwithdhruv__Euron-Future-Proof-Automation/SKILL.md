---
name: gamma-presentation
description: Create AI-generated presentations, documents, webpages, and social posts via Gamma MCP. Use when user asks to create slides, make a presentation, generate a deck, build a document, or create a webpage.
disable-model-invocation: true
argument-hint: "[topic]"
---

# Gamma Presentation Skill

> **Version:** 1.1.0 | **Updated:** 2026-03-03 | **Category:** Presentations & Docs

---

## ⚠️ CRITICAL — How to Call Gamma

**NEVER** look for `GAMMA_API_KEY` in .env files.
**NEVER** call Gamma REST API directly with fetch/requests.
**NEVER** search for credentials — there are none to find.

**ONLY correct way → call the MCP tool directly:**
```
mcp__claude_ai_Gamma__generate(inputText, format, themeId, ...)
```
Auth is handled transparently by the MCP connector. Works in Claude Code (VSCode) and claude.ai web. If you see "key empty" or "API key not found" — wrong approach. Stop and use the MCP tool.

---

## What It Does

Creates AI-generated presentations, documents, webpages, and social posts via Gamma MCP.
**No API key needed. No setup. Fully live via MCP.**

Use for:
- YouTube class slides (Euron bootcamp)
- Client pitch decks (QuotaHit, Onsite, agency)
- Social media carousels
- Portfolio / "about me" decks
- Product landing pages (Gamma webpage format)
- LinkedIn documents

---

## How to Trigger

Say any of these:
- "Create a Gamma presentation about X"
- "Make a deck for X"
- "Build a Gamma doc / webpage / social post"
- "Create slides for today's class"
- "Make a pitch deck for QuotaHit"

---

## MCP Tools Available

| Tool | Use When |
|------|----------|
| `generate` | Create new presentation/doc/webpage/social post |
| `get_themes` | Browse all 100+ available themes |
| `get_folders` | List saved Gamma folders |
| `get_generation_status` | Check if generation is complete |

---

## Format Options

| Format | Use When |
|--------|----------|
| `presentation` | Slides (default — use for most things) |
| `document` | Long-form doc, guide, course notes |
| `webpage` | Single-page website / landing page |
| `social` | LinkedIn carousel / social post |

---

## Best Themes for AiwithDhruv Brand

| Theme ID | Name | Best For |
|----------|------|----------|
| `nebulae` | Nebulae | **Default brand theme** — dark, purple/blue, futuristic, high-tech |
| `stratos` | Stratos | Investor decks, serious tech — deep navy, bold, dramatic |
| `aurora` | Aurora | Creative content, YouTube — dark gradient, fuchsia to purple |
| `gamma-dark` | Gamma Dark | Bold content — dark purple + salmon, playful futuristic |
| `founder` | Founder | Minimalist dark — startup pitches, professional |
| `velvet-tides` | Velvet Tides | Luxury/agency feel — dark black + purple gradient |
| `default-dark` | Basic Dark | Clean professional — dark, blue/purple, simple |

**Always default to `nebulae` unless user asks for something different.**

---

## Key Parameters

```
format: presentation | document | webpage | social
themeId: nebulae (default)
numCards: 6-10 (presentations), omit for docs/webpages
textMode: preserve (use exact content) | generate (expand from outline) | condense (shorten long content)
textOptions.amount: brief | medium | detailed | extensive
textOptions.tone: bold, futuristic, professional
textOptions.language: en (default)
exportAs: pptx | pdf (only when user asks)

# Dimensions (cardOptions.dimensions) — 9 options:
16x9         → YouTube, standard widescreen (default)
4x3          → Classic slides
fluid        → Responsive, no fixed ratio
letter       → US Letter (8.5x11) for print
a4           → A4 for print/PDF
pageless     → Infinite scroll document
1x1          → Square (Instagram)
4x5          → Portrait (Instagram feed)
9x16         → Vertical (Instagram Reels, TikTok, Shorts)

# AI Image Models (imageOptions.model) — use for better visuals:
flux-1-quick        → Fast, good quality (default)
flux-kontext-fast   → Context-aware, faster
flux-kontext-max    → Context-aware, max quality
flux-1-pro          → Pro quality
imagen-3-pro        → Google Imagen 3 Pro (photorealistic)
imagen-4-pro        → Google Imagen 4 Pro (best photorealism)
ideogram-v3         → Best for text-in-image
leonardo-phoenix    → Artistic/creative style
recraft-v3          → Vector/design style
recraft-v3-svg      → SVG output

# Sharing (sharingOptions) — set on generation:
workspaceAccess: edit | comment | view | noAccess
externalAccess: edit | comment | view | noAccess
emailOptions: { recipients: [...], access: 'view' }

# Header/Footer (cardOptions.headerFooter):
Add slide numbers, logo, or text to every slide
topLeft/topRight/bottomLeft/bottomCenter/bottomRight
type: cardNumber | image | text
```

---

## Workflow

1. **Get context** — What is the presentation for? Who's the audience?
2. **Pick theme** — Default `nebulae`. Use `get_themes` if user wants something specific.
3. **Write content** — Full slide content in `inputText` (use `preserve` mode for exact content)
4. **Generate** — Call `generate` → get `generationId`
5. **Poll status** — Call `get_generation_status` every 5-10s until `status: completed`
6. **Return URL** — Share `gammaUrl` with user

---

## Prompt Template (inputText structure)

```
Slide 1 — [Title Slide]
Title: [Main title]
Subtitle: [Subtitle or tagline]
Tagline: [Optional quote]

Slide 2 — [Section Name]
[Bullet points or paragraph content]

Slide 3 — [Section Name]
[Content...]
```

---

## Example Calls

### Quick deck
```
"Make a 6-slide Gamma presentation about MCP servers for my Euron class"
→ format: presentation, themeId: nebulae, numCards: 6
```

### Client pitch
```
"Create a QuotaHit pitch deck for investors — 10 slides, professional theme"
→ format: presentation, themeId: stratos, numCards: 10
```

### Course doc
```
"Create a Gamma document with all the class notes from today's session"
→ format: document, themeId: nebulae, textMode: preserve
```

### Export
```
"Create a presentation and export as PPTX"
→ exportAs: pptx
```

---

## Schema

### Inputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `inputText` | string | Yes | Full content (slides, outline, or paste) |
| `format` | enum | No | presentation / document / webpage / social |
| `themeId` | string | No | Default: nebulae |
| `numCards` | number | No | Number of slides |
| `textMode` | enum | No | preserve / generate / condense |
| `exportAs` | enum | No | pptx / pdf |

### Outputs
| Output | Description |
|--------|-------------|
| `gammaUrl` | Shareable link to the finished presentation |
| `generationId` | ID to check status |
| `credits.remaining` | How many Gamma credits left |

### Credentials
| Credential | Where | Notes |
|------------|-------|-------|
| Gamma MCP | Already connected via Claude MCP | No setup needed |

### Composable With
- `thumbnail-generator` → Create image prompt after building slides
- `image-to-video` → Animate slides into short video
- `ghost-browser` → Auto-post deck to LinkedIn
- `send-telegram` → Notify when deck is ready

### Input Pipelines (Content Sources → Gamma)
| Source | How | Use When |
|--------|-----|----------|
| YouTube video | Fetch transcript → feed as inputText | Turn a class recording into a deck |
| Web article | Extract article text → feed as inputText + textMode: condense | Research-to-deck |
| n8n workflow | Trigger Gamma generation from n8n HTTP node | Auto-generate weekly reports |
| Raw text/notes | Paste directly + textMode: preserve | Class notes → student deck |
| CSV/data | Summarize data → narrative slides | Sales report decks |

### Dimensions by Use Case
| Use Case | Dimension |
|----------|-----------|
| YouTube thumbnail / standard deck | `16x9` |
| Instagram carousel | `4x5` |
| Instagram/TikTok/Shorts | `9x16` |
| Print handout | `letter` or `a4` |
| LinkedIn document | `fluid` |
| Instagram square | `1x1` |

### Image Model by Use Case
| Use Case | Model |
|----------|-------|
| Fast deck (default) | `flux-1-quick` |
| Tech/realistic visuals | `imagen-4-pro` |
| Slides with text in images | `ideogram-v3` |
| Creative/artistic | `leonardo-phoenix` |
| Design/brand assets | `recraft-v3` |

### Cost
- **Free:** Gamma MCP is included in your plan (3,309 credits remaining as of Mar 3, 2026)
- ~34 credits per 8-slide deck

---

## Sub-Skills

| Sub-Skill | File | Use When |
|-----------|------|----------|
| Social Media Presentations | See `Social-Media-Agent-1.0/` | LinkedIn carousels, YouTube slides, content decks |
| Onsite Sales Presentations | See `Onsite/presentations/` | Client decks, sales proposals, onboarding slides |
