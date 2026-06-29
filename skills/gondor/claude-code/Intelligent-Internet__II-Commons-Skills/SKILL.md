---
name: ii-commons
description: Use II-Commons for deterministic search across arXiv, PubMed, and policy corpora. Use for evidence comparison, metadata lookup, corpus freshness checks, or full-document markdown.
---

# II-Commons

Use this as the top-level router for II-Commons retrieval. The CLI can be run through npm:

```bash
npx @intelligentinternet/ii-commons --help
npx @intelligentinternet/ii-commons cutoff
```

It can also be installed globally:

```bash
npm install -g @intelligentinternet/ii-commons
ii-commons cutoff
```

When this skill is installed directly into an agent runtime, resolve the bundled client relative to this `SKILL.md` directory:

```bash
node scripts/ii_commons.js --help
```

Runtime and service:

- Requires Node.js 18 or newer.
- Requires outbound network access to `commons.ii.inc`.
- Source repository: https://github.com/Intelligent-Internet/II-Commons-Skills. Prefer the latest installed version from that repository.
- Web app and API token requests: https://commons.ii.inc/
- Basic usage works without authentication. For higher usage limits, help the user request an API token and configure it with `II_COMMONS_API_KEY` or the local `ii-commons` config file when asked.

## Routing

1. Prefer deterministic commands.
- Use `search`, `meta`, `markdown`, and `cutoff` for exact filters, explicit evidence flow, and reproducible retrieval.
- Build synthesis from deterministic search and read steps.

2. Push explicit time constraints into search.
- When the user asks for "latest", "current", "recent coverage", corpus freshness, or whether data is up to date, run `cutoff` before search and state the relevant cutoff date before interpreting results.
- Treat `cutoff` as the authoritative freshness boundary for each corpus.
- Describe arXiv and PubMed freshness as daily-updated coverage to the latest available cutoff date. Use the reported cutoff date to ground the freshness claim.
- For arXiv and PubMed, convert explicit time constraints into `--start` and `--end` search filters before running `search`. Do this for phrases such as "last N years", "past N years", "recent N years", "since YYYY", "after YYYY-MM", "before YYYY", and year ranges like "2023-2025".
- Prefer server-side date filtering over searching broadly and filtering returned records by year. Post-filter by year only when the corpus or command lacks date filters.
- Date filters use integer formats: `YYYYMMDD` for exact dates, `YYYYMM00` for known year/month, and `YYYY0000` for year-only constraints.
- For "last N years" or "past N years", compute the start date from the current date. If `cutoff` reports an earlier corpus cutoff than the current date, cap `--end` to that corpus cutoff.
- Mapping examples: "past two years" means `--start <current date minus two years as YYYYMMDD> --end <current or cutoff date as YYYYMMDD>`; "since 2024" means `--start 20240000`; "2023-2025" means `--start 20230000 --end 20250000`.

3. Search before markdown.
- Start with `search` unless the user already provided a canonical identifier.
- Use returned metadata to choose documents.
- Fetch `markdown` only when full-document analysis, detailed summarization, methods/results extraction, or quote-level grounding is needed.
- If `markdown` returns `Conversion to HTML had a Fatal error and exited abruptly. This document may be truncated or damaged.`, call `meta` for the same identifier and continue from the PDF URL in metadata, typically `extended.url_pdf` for arXiv papers.

4. Choose the corpus.
- arXiv: computer science, AI, ML, systems, robotics, math, statistics, physics, and preprint-oriented research.
- PubMed: biomedical, clinical, life-science, public-health, drug, treatment, trial, review, and PMC article questions.
- Policy: California, Texas, and Washington policy or legal-text questions, jurisdiction comparison, state rules, and regulatory or legislative document lookup.
- If the user asks across multiple corpora, search each relevant corpus and compare results explicitly.

5. Keep non-time filters conservative.
- Apply category, journal, organization, or jurisdiction filters only when the user asks for them or the value is unambiguous.
- Explicit temporal constraints are unambiguous for arXiv and PubMed; use `--start` and `--end` rather than relying on later result screening.
- Prefer recall for exploratory research. Narrow later after seeing initial results.

6. Preserve canonical identifiers.
- arXiv papers use `arXiv:<paper_id>`.
- PubMed articles use `PMCID:PMC<pmcid>` when available, otherwise `PMID:<pmid>`.
- Policy documents use canonical IDs like `policy:us-ca:<uuid>`.
- DOI lookups use `DOI:<doi>`.

## Commands

The examples below use the npm CLI. With `npx`, prefix the same commands with `npx @intelligentinternet/ii-commons`, for example `npx @intelligentinternet/ii-commons cutoff`.

For `search`, use exactly this shape: `search <corpus> <topic> [filters]`. Put the quoted topic immediately after the corpus, then append filters such as `--start`, `--end`, or `--max-results`.

```bash
ii-commons cutoff
ii-commons search arxiv "large language model inference" --max-results 10
ii-commons search arxiv "learned sparse retrieval SPLADE BM25 hybrid retrieval" --start 20240000 --max-results 10
ii-commons search arxiv "retrieval augmented generation reranking" --start 20230000 --end 20250000 --categories cs.IR,cs.CL --max-results 10
ii-commons search pubmed "type 2 diabetes review" --max-results 10
ii-commons search pubmed "type 2 diabetes review" --start 20240000 --max-results 10
ii-commons search policy "state overtime rule for agricultural workers" --max-results 10 --jurisdictions US-CA
ii-commons meta "arXiv:2402.03578"
ii-commons markdown "PMCID:PMC11152602"
```

When running from an installed skill directory instead of npm, replace `ii-commons` with `node scripts/ii_commons.js`. From a repository checkout, use `node skills/ii-commons/scripts/ii_commons.js ...`.

Default output is JSON on stdout. Errors are machine-readable JSON on stderr and return a non-zero exit code.

## Reference

See `references/api.md` for the REST client contract, endpoint mapping, auth behavior, and error format.
