# Workflow — Re-Ingestion Schedule

> Weekly re-ingestion keeps answers fresh as policies / catalog / FAQs change.

---

## Cadence

| Source Type | Re-ingest |
|-------------|-----------|
| Refund / shipping / returns policy | On edit (event-driven) |
| Product catalog | Daily (if velocity) / weekly |
| FAQ | Weekly |
| Help-center articles | Weekly |

## Automation Options

### Option A — GitHub Actions cron (free)

`.github/workflows/reingest.yml`
```yaml
name: Weekly Re-ingest
on:
  schedule:
    - cron: "0 3 * * 1"   # Mondays 03:00 UTC
  workflow_dispatch: {}
jobs:
  reingest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r RAG_Knowledge_Chatbot/requirements.txt pypdf
      - working-directory: RAG_Knowledge_Chatbot
        env:
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_SERVICE_KEY: ${{ secrets.SUPABASE_SERVICE_KEY }}
        run: |
          python tools/ingestion/load_docs.py   --path ./knowledge --type all
          python tools/ingestion/chunk_docs.py
          python tools/ingestion/embed_chunks.py
```

> Rule: GitHub Actions workflows MUST live at repo-root `.github/workflows/`
> (see `learning-hub/ERRORS.md` — 2026-04-06 entry).

### Option B — Remote trigger via API

`POST /reingest` with the API key. Useful if the FastAPI server has mounted
storage where docs land (e.g., Notion export, S3 sync).

### Option C — On-edit event

Wire a Notion / Drive webhook → small adapter → `POST /reingest` with the
source folder. Only re-embeds changed `source_id`s because upserts are
idempotent on `chunk_id`.

## Monitoring

- Log every run to `runs/YYYY-MM-DD-reingest.md`
- Compare `chunks_out` across runs — sudden drops mean a source went missing
- Feedback `verdict=down` spikes = content drift → trigger ad-hoc reingest
