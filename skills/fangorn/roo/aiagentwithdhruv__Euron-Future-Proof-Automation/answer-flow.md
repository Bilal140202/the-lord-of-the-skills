# Workflow — Answer Flow

> How a user question becomes a cited answer (or an escalation).

---

## The Agentic Loop

```
Sense    → User message (web widget | WhatsApp | /ask API)
Think    → Embed query → pgvector similarity top-k
Decide   → Confidence gate → Generate → Citation gate
Act      → Reply with answer + citations  OR  escalate to human
Learn    → /feedback logs verdict
```

## The Two Gates (rule 50 enforcement)

```
query
  │
  ▼
tools/retrieval/search.py          ← Layer 2 only
  │
  ▼
Gate 1: top_similarity >= 0.6?
  │ no                      │ yes
  ▼                         ▼
ESCALATE              tools/generation/answer.py   ← Layer 3 only
                            │
                            ▼
                      Gate 2: any valid citations?
                            │ no          │ yes
                            ▼             ▼
                      ESCALATE        ANSWER
```

Retrieval and generation live in separate modules and never import each other.
Only `tools/ask.py` wires them together.

## Steps

```bash
# CLI
python tools/ask.py --query "What's the refund window?"

# API
uvicorn api.main:app --reload
curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -H "x-api-key: $API_KEY" \
     -d '{"query":"What is the refund window?"}'
```

## Response Shape

### Answered
```json
{
  "status": "answered",
  "answer": "We offer a full refund within 14 days of delivery [1].",
  "citations": [
    {"n": 1, "chunk_id": "refund-policy::0001",
     "source_id": "refund-policy", "source_path": "refund-policy.md",
     "section": "Timeline"}
  ],
  "confidence": 0.84,
  "retrieval_top_similarity": 0.89,
  "duration_ms": 1423
}
```

### Escalated
```json
{
  "status": "escalated",
  "answer": null,
  "citations": [],
  "confidence": 0.41,
  "reason": "low_confidence (top=0.41 < 0.6)"
}
```

## Config Knobs

| Env var | Default | What it tunes |
|---------|---------|---------------|
| `TOP_K` | 5 | Chunks retrieved per query |
| `CONFIDENCE_THRESHOLD` | 0.6 | Below → escalate |
| `CHUNK_SIZE` | 800 | Ingestion-time |
| `CHUNK_OVERLAP` | 100 | Ingestion-time |
| `LLM_MODEL` | gpt-4o-mini | Euri model for generation |
| `EMBEDDING_MODEL` | text-embedding-004 | Gemini model id |

## Error Handling

| Failure | Behavior |
|---------|----------|
| Empty query | 422 from API / ValueError from CLI |
| Missing env keys | Clear error message listing what's missing |
| Gemini/Supabase 5xx | Retries with backoff; fails loudly if exhausted |
| LLM returns no citations | Escalate (citation gate) |
