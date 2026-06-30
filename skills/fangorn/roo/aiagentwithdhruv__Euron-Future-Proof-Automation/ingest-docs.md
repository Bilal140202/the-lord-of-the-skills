# Workflow — Ingest Docs

> How to add new knowledge to the RAG brain.
> Rule 50: ingestion stages are strictly sequential and never cross into retrieval or generation.

---

## Objective

Take a directory of docs (`.md`, `.txt`, `.pdf`) → produce chunked, embedded rows in Supabase `knowledge_chunks`.

## Inputs

| Input | Type | Notes |
|-------|------|-------|
| `--path` | directory | The knowledge root (e.g. `./knowledge`) |
| `--type` | md \| txt \| pdf \| all | File filter |

## Tools (in order)

1. `tools/ingestion/load_docs.py` — directory → `.tmp/docs.jsonl`
2. `tools/ingestion/chunk_docs.py` — docs → `.tmp/chunks.jsonl`
3. `tools/ingestion/embed_chunks.py` — chunks → Supabase `knowledge_chunks`

## Steps

```bash
# From project root
python tools/ingestion/load_docs.py   --path ./knowledge --type md
python tools/ingestion/chunk_docs.py  --chunk-size 800 --overlap 100
python tools/ingestion/embed_chunks.py --batch 20
```

## Outputs

- `.tmp/docs.jsonl` — one record per document (disposable)
- `.tmp/chunks.jsonl` — one record per chunk (disposable)
- `knowledge_chunks` table in Supabase — permanent store

## Metadata Preserved per Chunk

- `chunk_id` (unique, deterministic from `source_id::index`)
- `source_id`, `source_path`, `section`, `chunk_index`
- `metadata.title`, `metadata.type`, `metadata.updated_at`, `metadata.char_offset`

## Error Handling

| Failure | Fix |
|---------|-----|
| `FileNotFoundError` on load | Check `--path` is a real directory |
| PDF parsing needs `pypdf` | `pip install pypdf` or use `.md` |
| Gemini 429 | Embedder retries with backoff; otherwise wait |
| Supabase 400 on upsert | Verify schema was applied from `db/supabase_schema.sql` |
| Embedding dim mismatch | `vector(768)` must match your embedding model |

## Cost Estimate

| Step | Cost |
|------|------|
| Load + chunk | Free (local) |
| Embed | Gemini free tier ~1500 RPM; 100 chunks ≈ seconds |
| Store | Supabase free tier, negligible |

## Re-ingestion

Upserts on `chunk_id`, so re-running is idempotent. To fully rebuild, drop rows
for a given `source_id` first:

```sql
delete from knowledge_chunks where source_id = 'refund-policy';
```
