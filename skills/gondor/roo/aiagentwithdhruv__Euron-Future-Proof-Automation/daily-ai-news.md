# Workflow: Daily AI News Digest

## Objective
Fetch today's AI news from multiple sources, rank the top 5, and send a formatted digest to Telegram.

## Inputs
| Input | Type | Required | Default |
|-------|------|----------|---------|
| sources | string | No | `newsapi,rss` |
| top_n | int | No | `5` |
| format | string | No | `markdown` |

## Tools (in order)
1. `tools/fetch_news.py` — Fetch raw articles
2. `tools/rank_news.py` — Rank and summarize top 5
3. `tools/format_message.py` — Format for Telegram
4. `tools/send_telegram.py` — Send to Telegram

## Steps

### Step 1: Fetch news
```bash
python tools/fetch_news.py --sources newsapi,rss --limit 20
```
- Output: `.tmp/raw_news.json`
- Expected: 15-30 articles

### Step 2: Rank and summarize
```bash
python tools/rank_news.py --input .tmp/raw_news.json --top 5
```
- Output: `.tmp/ranked_news.json`
- Uses Euri LLM if available, otherwise keyword scoring
- Expected: 5 articles with summaries

### Step 3: Format message
```bash
python tools/format_message.py --input .tmp/ranked_news.json --format markdown
```
- Output: `.tmp/telegram_message.txt`
- MarkdownV2 with escaped special chars

### Step 4: Send to Telegram
```bash
python tools/send_telegram.py --input .tmp/telegram_message.txt
```
- Sends to configured chat/channel
- Auto-falls back to plain text if markdown parsing fails

## Outputs
| Output | Location | Format |
|--------|----------|--------|
| Raw articles | `.tmp/raw_news.json` | JSON array |
| Ranked articles | `.tmp/ranked_news.json` | JSON array (top 5) |
| Telegram message | `.tmp/telegram_message.txt` | MarkdownV2 text |
| Run log | `runs/YYYY-MM-DD-daily-ai-news.md` | Markdown |

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| NewsAPI 401 | Invalid/expired API key | Check .env, regenerate key at newsapi.org |
| NewsAPI 429 | Rate limit (100/day) | Wait 24h or use RSS-only mode |
| LLM timeout | Euri/OpenRouter down | Fall back to `--no-llm` keyword ranking |
| Telegram 400 | Markdown parse error | Auto-retries as plain text |
| Telegram 403 | Bot blocked or wrong chat_id | User must /start the bot and verify chat_id |
| Empty results | No articles found | Log warning, send "No AI news found today" |

## Cost Estimate
| Component | Cost per run |
|-----------|-------------|
| NewsAPI | $0 (free tier) |
| RSS feeds | $0 (free) |
| Euri LLM ranking | $0 (free 200K tokens/day) |
| Telegram Bot API | $0 (free) |
| **Total** | **$0** |
