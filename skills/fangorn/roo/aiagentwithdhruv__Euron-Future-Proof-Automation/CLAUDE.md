# RAG_Knowledge_Chatbot — Rules

> Inherits from `../CLAUDE.md`.

---

## Project

- **Name:** RAG_Knowledge_Chatbot
- **Objective:** One AI brain knows YOUR product → answers on website + WhatsApp with citations
- **Phase:** 4 — AI-Powered Autonomous Systems (Week 9: RAG & Knowledge Bases)
- **Status:** In Progress
- **Owner:** Atlas

---

## Agentic Loop

1. **Sense:** User question (web/WhatsApp)
2. **Think:** Embed → retrieve top-k
3. **Decide:** Answer / clarify / escalate
4. **Act:** Reply with citations
5. **Learn:** Feedback loop tunes retrieval

---

## Tech

| Layer | Choice |
|-------|--------|
| LLM | euri/gpt-4o (answers), euri/gpt-4o-mini (classify) |
| Embeddings | Gemini Embedding 2 |
| Vector DB | Supabase pgvector |
| Backend | FastAPI |
| Channels | Web widget + WhatsApp Cloud |
| Deploy | **n8n** ✅ LIVE at `n8n.aiwithdhruv.cloud/webhook/aiwithdhruv-chat/chat` |

---

## Project-Specific Rules

- **RAG separation non-negotiable** (rule 50): ingestion/retrieval/generation are 3 separate layers.
- **Every answer must cite sources** — no cite = no send.
- **Confidence threshold** — below 0.6 → escalate to human.
- **Re-ingest weekly** for updated content.
- **Chunk metadata mandatory** — source_id, section, updated_at.
