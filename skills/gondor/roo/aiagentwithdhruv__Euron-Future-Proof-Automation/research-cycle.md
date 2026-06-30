# Workflow: Weekly Research Cycle

> **Cadence:** Weekly (cron fires, no human trigger).
> **Owner:** Atlas.
> **Agentic Loop:** Sense → Think → Decide → Act → Learn.

---

## Objective

For each competitor in `config/competitors.yaml`:
1. Pull the latest state (site + news + social).
2. Diff against last week's snapshot.
3. Classify what changed (pricing / launch / hire / partnership / press).
4. Rank findings by business relevance.
5. Write one report covering all competitors.
6. Deliver the report to Slack + Email + Telegram.
7. Save new snapshots (source of truth for next week's diff).
8. Log the run.

---

## Inputs

| Input | Type | Required | Default |
|-------|------|----------|---------|
| competitors_config | path | Yes | `config/competitors.yaml` |
| dry_run | bool | No | `false` (skip delivery, write preview) |
| cost_cap_usd | float | No | `1.00` (abort if exceeded) |
| rate_limit_sec | int | No | `3` (seconds between requests per domain) |
| delivery_channels | list | No | `[slack, email, telegram]` (skip any missing creds) |

---

## Tools (in order)

1. `tools/fetch_competitor.py` — scrape competitor site (homepage + pricing + /about + /blog)
2. `tools/fetch_news.py` — pull news mentions per competitor keyword (NewsAPI + RSS + Tavily)
3. `tools/fetch_social.py` — pull social signals (Tavily-based; LinkedIn/X scraping is out of free tier)
4. `tools/snapshot_diff.py` — diff current vs previous snapshot per competitor
5. `tools/analyze_changes.py` — LLM classifies and ranks diffs
6. `tools/write_report.py` — generate markdown report from ranked findings
7. `tools/deliver_report.py` — send to Slack + Email + Telegram (best-effort; skip missing channels)
8. `tools/run_research.py` — orchestrator (Steps 1→8)

All tools respect the shared budget (`shared/cost_tracker.py`, $1 run cap, $5 daily).

---

## Steps

### Step 1 — Load competitor list
```bash
# Implicit inside run_research.py
```
Reads `config/competitors.yaml`. Expected schema:
```yaml
competitors:
  - name: "n8n"
    homepage: "https://n8n.io"
    pricing: "https://n8n.io/pricing"
    blog: "https://blog.n8n.io"
    news_keywords: ["n8n", "n8n.io"]
    social:
      twitter: "n8n_io"
      linkedin: "n8n-io"
business_context: "AI automation / agent platforms"
```

### Step 2 — Fetch per competitor
For each competitor:
```bash
python tools/fetch_competitor.py --name "n8n" --urls homepage,pricing,blog --rate-limit 3
python tools/fetch_news.py   --keywords "n8n,n8n.io" --days 7 --limit 15
python tools/fetch_social.py --name "n8n" --handles "twitter:n8n_io,linkedin:n8n-io" --days 7
```
- Outputs: `.tmp/fetch/{name}_site.json`, `.tmp/fetch/{name}_news.json`, `.tmp/fetch/{name}_social.json`
- Respects `robots.txt` (via `shared/robots_check.py`).
- Rate-limits 3s between requests to the same domain.
- Strips PII (emails, phones) from stored content.

### Step 3 — Build current snapshot + diff vs previous
```bash
python tools/snapshot_diff.py \
  --name "n8n" \
  --current-files .tmp/fetch/n8n_site.json,.tmp/fetch/n8n_news.json,.tmp/fetch/n8n_social.json \
  --previous-snapshot data/snapshots/n8n.json
```
- Output: `.tmp/diff/{name}.json`
- First run (no previous snapshot): everything is marked `added`, small subset flagged for analysis.
- **Snapshot diff is the source of truth.** Step 4 only consumes the diff, never the full content.

### Step 4 — Classify changes (LLM)
```bash
python tools/analyze_changes.py \
  --diffs .tmp/diff/n8n.json,.tmp/diff/lindy.json \
  --business-context "AI automation / agent platforms"
```
- LLM tags each change: `pricing | launch | hire | partnership | press | site | other`
- LLM ranks findings 1–5 by business relevance.
- Output: `.tmp/insights.json` (merged, ranked, cross-competitor)
- Uses prompts: `prompts/classify_change_v1.md`, `prompts/rank_findings_v1.md`
- Cost per run: ~$0.02 (free on Euri).

### Step 5 — Write report
```bash
python tools/write_report.py --insights .tmp/insights.json --output .tmp/report.md
```
- Sections: Executive Summary → Top Findings → Per-Competitor Changes → Sources.
- Uses prompt: `prompts/write_report_v1.md`.

### Step 6 — Deliver report
```bash
python tools/deliver_report.py --report .tmp/report.md --channels slack,email,telegram
```
- **Slack:** incoming webhook (`SLACK_WEBHOOK_URL`), posts markdown.
- **Email:** Resend API (`RESEND_API_KEY`), subject "Competitor Digest — {date}".
- **Telegram:** Bot API (`TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`), MarkdownV2.
- Missing credentials → skip that channel, log warning, don't crash.
- Receipts collected into `runs/{date}-research-cycle.md`.

### Step 7 — Save new snapshots
- Write `data/snapshots/{name}.json` per competitor (overwrite).
- Each snapshot is small (key hashes + page summaries + metadata), commitable.
- PII-stripped.

### Step 8 — Log run
- `runs/YYYY-MM-DD-research-cycle.md` with: competitors, step statuses, findings count, delivery receipts, total cost.

---

## Outputs

| Output | Location | Format |
|--------|----------|--------|
| Raw fetches | `.tmp/fetch/*.json` | JSON (disposable) |
| Diffs | `.tmp/diff/*.json` | JSON |
| Insights | `.tmp/insights.json` | JSON |
| Report | `.tmp/report.md` | Markdown |
| Snapshots | `data/snapshots/{name}.json` | JSON (persistent) |
| Run log | `runs/YYYY-MM-DD-research-cycle.md` | Markdown |

---

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| robots.txt disallow | URL blocked | Skip that URL, log WARN, continue |
| HTTP 429 | Rate limit hit | Backoff 60s once, then skip domain for this run |
| HTTP 403 / WAF | Anti-bot block | Skip URL, log, don't retry (respect the block) |
| NewsAPI 401 | Bad key | Skip news source, keep going |
| LLM failure | Euri/OpenRouter down | Fall back to rule-based classification (keyword heuristics) |
| Cost cap hit | `BudgetExceededError` | Abort run immediately, write partial log, exit non-zero |
| Missing delivery key | e.g. no `SLACK_WEBHOOK_URL` | Skip channel, continue with others |
| Empty diff | First run or no changes | Report says "No meaningful changes this week" + send |
| Missing previous snapshot | First ever run for this competitor | Mark entire snapshot as "initial baseline", skip analysis to save cost |

---

## Cost Estimate

| Component | Cost / run |
|-----------|-----------|
| Competitor scraping | $0 (requests + bs4) |
| NewsAPI | $0 (100/day free) |
| Tavily | $0 (1000/mo free) |
| Euri LLM (classify + rank + report) | $0 (200K tokens/day free) |
| OpenRouter fallback | ~$0.02–0.05 |
| Slack / Resend / Telegram | $0 |
| **Total (typical)** | **$0–0.05** |
| **Hard cap** | **$1.00** (abort on breach) |

---

## Guardrails (Non-Negotiable)

1. **robots.txt:** check every URL before GET. Skip disallowed.
2. **Rate limit:** 3s minimum between requests to the same domain.
3. **PII strip:** regex-scrub emails, phone numbers, SSN-like patterns before saving.
4. **Snapshot diff = source of truth:** Step 4 never re-analyzes full content.
5. **Cost cap $1/run:** `check_budget()` before every paid call; abort on breach.
6. **User-Agent:** identify as `Angelina-OS-Research-Agent/1.0 (+contact)`.
7. **No login-gated content:** free/public pages only.
8. **Receipts, not claims:** every delivery logged with message_id or response.
9. **Dry-run:** `--dry-run` writes `.tmp/report.md` preview and skips delivery.
10. **Fail open, fail loud:** one competitor failing doesn't block others; all failures are logged.

---

## Test Procedure (Local, 2 Competitors, DO NOT Deploy)

```bash
cd Autonomous_Research_Agent
cp .env.example .env                      # fill the keys you have
python tools/run_research.py --competitors config/competitors.yaml --dry-run
# verify: .tmp/report.md preview, .tmp/insights.json sanity, runs/*.md log
```

Success criteria:
- [ ] Fetches at least 1 URL per competitor (or logs skip reason).
- [ ] `robots.txt` check ran and is logged.
- [ ] 3s delay observed between same-domain requests.
- [ ] Snapshot written to `data/snapshots/{name}.json`.
- [ ] `.tmp/report.md` is coherent markdown.
- [ ] `runs/*.md` log exists with per-step status + total cost.
- [ ] Cost cap not exceeded.
- [ ] No PII in stored snapshots.

Do **not** wire GitHub Actions cron until Angelina dispatches the deploy step.
