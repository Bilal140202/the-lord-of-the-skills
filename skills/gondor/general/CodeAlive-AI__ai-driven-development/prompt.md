You are an independent expert assessing an OpenSearch 3.5.0 k-NN derived_source migration failure. Read the problem carefully, form your own conclusions, and answer the 6 questions below. Do not defer to the asker's hypotheses — challenge them if they seem wrong.

## Context
A backend service (CodeAlive) maintains an OpenSearch 3.5.0 index of source-code "artifacts" — one document per file/chunk in customer repositories. Each artifact has a 768-dim HNSW embedding for semantic search plus scalar fields (path, content, kind, etc.). Total ~2.9M docs, 82 GB, 4 primary shards x 1 replica, routing_partition_size=2, _routing.required=true.

A new release wants to add two denormalized scalar fields to every existing document:
- file_type (int enum) — derived in C# from path/content
- ext (string) — file extension

These two fields are not currently indexed. After migration runs, future writes will set them; they're being backfilled across all existing docs.

## Index settings (verified)
```
"engine": "lucene",
"space_type": "cosinesimil",
"name": "hnsw",
"dimension": 768,
"format": "Lucene99HnswScalarQuantizedVectorsFormat"
"knn.derived_source": { "enabled": "true" }   ← KEY POINT
"number_of_shards": 4,
"number_of_replicas": 1,
"routing_partition_size": 2,
```
OpenSearch 3.5.0 + Lucene 10.3.2, on a self-hosted 3-node cluster (Google Cloud VMs).

## What was tried (all failed)

### Attempt 1: _bulk update with Painless script
Per-batch _bulk with update actions, painless script sets ctx._source.file_type and ctx._source.ext. Failed with AlreadyClosedException: MemorySegmentIndexInput(path="..._Lucene99HnswScalarQuantizedVectorsFormat_0.vec") — HNSW segment merge race during the per-doc GET-for-update phase.

### Attempt 2: _update_by_query (server-side scroll + bulk reindex)
Rewrite using _update_by_query?routing=X with ids query, sequential per-batch. Failed with HTTP 503, search_phase_execution_exception "all shards failed", failed_shards: []. The .NET OpenSearch.Client DebugInformation dump shows full request/response but no per-shard details in the exception.

Diagnostic facts at failure time:
- Cluster green, 65/65 shards active, 0 unassigned, 0 pending tasks
- All thread pools idle, 0 rejected
- 0 ongoing merges on the index
- No exception traces in any OpenSearch node logs during the failure window
- Same request via curl (from inside the same K8s pod, same endpoint, same auth) → 200 OK in ~1.3s for IDs picked via match_all search
- Same _update_by_query for the EXACT IDs that fail from the migration → also 503 via curl

### Diagnostic finding (reproducible 100%)
For a specific routing value, deterministic split:
- GET /_search?routing=X with IdsQuery and default _source → 503
- GET /_search?routing=X with IdsQuery and _source:false, stored_fields:_none_ → 200 OK
- GET /_search without routing → 200 OK, full _source returned
- POST /_update_by_query?routing=X with IdsQuery (any script, even ctx.op='noop') → 503

Translation: when _source reconstruction is involved AND routing is scoped to the 2 shards that hold those docs, query fails. Without _source or without routing it works.

### Web research surfaced the likely mechanism
knn.derived_source.enabled=true means _source.embeddings is not stored in .fdt as a normal field — instead a 1-byte placeholder is stored and the real vector lives in .vec (Lucene99HnswScalarQuantizedVectorsFormat). At query time, OpenSearch reconstructs _source by reading the quantized vector back from .vec and injecting it into the JSON. For documents written by older indexer code (older quantile bounds, older derived-source attribute schema), the reconstruction can fail — and the exception is swallowed inside SecurityInterceptor before it reaches the transport layer's failed_shards array. Cited issues: opensearch-project/k-NN#3083, #2880, opensearch-project/OpenSearch#19330.

### Attempt 3: _source.excludes: ["embeddings"] on _update_by_query
Hypothesis: skip embeddings loading so the failing reconstruction step is skipped.

Result: request succeeds (200 OK, updated=N) for 3 previously-failing documents.

But post-update verification shows: _source is now loadable WITHOUT excludes (per-doc 503 gone), BUT _source.embeddings returns empty, AND kNN search with id-filter on those 3 docs returns 0 hits. The vectors are gone from the kNN index. The vectors are gone from those docs. Whatever segment was holding the old broken-derived-source representation got replaced by a new segment where _source excludes embeddings — and with derived_source enabled, the float array was never stored in .fdt to fall back on. So reindex with filtered _source permanently deletes the vectors from those docs.

This is a catastrophic data-loss path on ~3M docs. Cannot apply.

### Attempt 4: single-doc POST /_update/<id> with partial doc body (no script)
- On a previously-migrated doc → 200 noop. Inconclusive.
- On an untouched broken doc → 500 AlreadyClosedException on Lucene99HnswScalarQuantizedVectorsFormat_0.vec. Same HNSW merge race as Attempt 1.

## What we know about vector storage
Even for "broken" docs the vectors ARE still in the kNN index. Direct kNN search with a 768-dim vector and a routing-scoped query returns hits (tested with _source:false to bypass reconstruction). The k-NN graph is intact; only the _source reconstruction path is broken.

## The constraint that makes this hard
OpenSearch / Lucene segments are immutable. Every API that "updates" a field — _bulk update, _update_by_query, _update/<id> — under the hood reads the existing _source, mutates it, deletes the old doc, indexes a brand-new doc with the merged _source. There is no partial-field-write API on segment level. So any update API trips the broken _source reconstruction.

The only paths that DO NOT touch _source reconstruction are:
- _search with _source:false, stored_fields:_none_ (read-only)
- kNN search (read-only)
- Re-index from external source where you provide the COMPLETE new doc (overwrites — but we don't have the embedding vector outside OpenSearch)

## Options identified

1. **Skip the migration altogether**, accept that file_type/ext filters only work for new docs. The bigger problem (broken derived_source decode for old docs) is then a separate, larger issue.

2. **Side-car index**: create a second tiny index artifact_filter_metadata with (id, routing, file_type, ext) per artifact. Filter at query time via terms_lookup or client-side join. No updates to existing docs. ~2.9M small inserts.

3. **Full reindex** of the entire 82 GB index into a new index with knn.derived_source.enabled=false. Add file_type/ext during the reindex. Several hours of work, must coordinate with live traffic, but fixes the root derived_source bug for all docs not just the migration.

4. **Wait for OpenSearch upgrade** (3.6.0 mentions "Fix derived source with dynamic templates causing vectors to be incorrectly returned during bulk indexing"). Defer everything.

5. **Some other angle we haven't seen.**

## Questions (answer independently)

1. **Root cause correctness**: Is our analysis of the root cause correct? Is this really the derived_source decode failure described in k-NN #3083 etc., or is something else more likely given the symptom set? What would you do to confirm before committing to a remediation?

2. **Right path forward** given:
   - prod is healthy and stable, no incident
   - migration is "would be nice" not "must ship"
   - data loss on real customer vectors is unacceptable
   - ~3M docs and customer SLAs around chat-search latency

3. **Option framing accuracy**: Are options 1-4 framed correctly? Anything materially wrong in our characterization? Anything missing? Is there an option 5 we haven't seen?

4. **Side-car index risks**: The side-car index (option 2) seems like the lowest-risk path to us, but we're biased after spending 6 hours in this rabbit hole. What's wrong with it? What ops cost will we discover in 2 weeks?

5. **Full reindex strategy**: If pursuing full reindex (option 3), what's the right strategy? Reindex API in-place, blue-green with alias swap, or something else? What's the failure mode that breaks reindex at scale on an HNSW index this big?

6. **Research gaps**: What other GitHub issues / OpenSearch / Lucene knowledge would change the calculus here? We've cited k-NN #3083, #2880, OpenSearch #19330, neural-search #393. What did we miss?

## Output format
Structured assessment:
- **Assessment**: your overall take
- **Key Findings**: bullet points
- **Blind Spots**: what you think they're missing or wrong about
- **Alternatives**: options not listed above
- **Recommendation w/ confidence**: specific path forward with confidence level

Don't be diplomatic. If their diagnosis is wrong say so. Challenge assumptions.
