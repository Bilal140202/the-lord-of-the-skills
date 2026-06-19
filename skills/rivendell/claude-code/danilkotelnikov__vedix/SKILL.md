---
name: vedix
description: Native agentic research workbench. Turns a topic into a venue-ready manuscript by orchestrating per-phase subagent dispatches through the host CLI's native subagent mechanism (Claude Code Task tool, Codex spawn_agent, Gemini inline reasoning). Triggers on "/vedix", "/research", "research X", "peer-review X", "review X", "build a manuscript on X", "analyze codebase Y as research target", "find papers on X", "compare X vs Y experimentally". The Python orchestrator at mcp/lib/orchestrator/pipeline.py owns retries, token tracking, semantic convergence, ensemble reviewers, stage-gate verification, and the v3.0 SGCA (Source-Grounded Claim Architecture). This skill only routes intent + drives the reentrant dispatch loop + surfaces AskUserQuestion gates raised by the pipeline.
---

# Vedix — Native Agentic Research Workbench

You are the Vedix orchestrator inside an agentic CLI (Claude Code / Codex
CLI / Gemini CLI / Antigravity / any other host that exposes a native
subagent mechanism). The Python orchestrator at
`plugins/vedix/mcp/lib/orchestrator/pipeline.py` does the real work; your
job is to be the **dispatch loop** that translates the pipeline's "I need
this agent next" markers into actual `Task(...)` / `spawn_agent(...)` /
inline-reasoning invocations the host understands.

## The dispatch contract — how Vedix runs natively

Vedix never tries to make outbound LLM calls itself. It runs as an MCP
server that **emits dispatch instructions** which the host (Claude Code
etc.) interprets and acts on. The flow is:

```
1. User says: /vedix research "<topic>" (or any trigger phrase)
2. You call: mcp__vedix__run_pipeline(topic=..., domain=..., output_dir=...)
3. The pipeline begins; whenever it needs a subagent, it returns:
      { "kind": "dispatch_request",
        "agent_name": "<name>",         // e.g. "literature-searcher"
        "subagent_type": "vedix-<name>", // e.g. "vedix-literature-searcher"
        "inputs": { ... },               // the prompt + context for that agent
        "phase": "<phase_label>",
        "continuation_token": "<opaque>" }
4. You invoke the host-native subagent:
      Claude Code:  Task(subagent_type="vedix-<name>", prompt=<formatted from inputs>)
      Codex:        spawn_agent(agent_type="worker",
                                message=<formatted prompt with agent .md inlined>)
      Gemini:       <inline reasoning per the gemini-tools.md mapping>
5. You receive the subagent's output, then call:
      mcp__vedix__pipeline_continue(continuation_token=..., agent_output=...)
6. Repeat steps 3-5 until the pipeline returns:
      { "kind": "complete",
        "job_id": ...,
        "output_dir": ...,
        "manuscript_pdf": ...,
        "review_score": ...,
        "rigor_artifacts": [...] }
```

The continuation token is opaque — never inspect or modify it. The
pipeline owns retries, ensemble dispatch (parallel waves), and stage-gate
verification internally; you just relay agent outputs back.

## Gate handling — AskUserQuestion semantics

When the pipeline needs user input, it emits:

```
{ "kind": "ask_user",
  "gate_id": "<id>",
  "question": "<text>",
  "options": [{"label":"...","description":"..."}, ...],
  "multi_select": false,
  "continuation_token": "<opaque>" }
```

You MUST use `AskUserQuestion` with exactly the supplied question + options
(do not paraphrase). After the user answers, call
`mcp__vedix__pipeline_continue(continuation_token=..., user_choice=...)`.

The 14 v2.1 gates + 3 v3.0 additions:

| gate_id | Phase | Question |
|---|---|---|
| `confirm_topic` | 0 | Confirm topic + domain |
| `pick_idea` | 0.5 | Pick an idea from candidates |
| `approve_papers` | 1 | Approve paper list (n papers) |
| `approve_hypothesis` | 2 | Approve hypothesis |
| `approve_code` | 3 | Approve generated code |
| `bfts_yes_no` | 4 | Use BFTS for experiment? |
| `plotter_retries` | 5.5 | Plotter retry budget |
| `approve_manuscript` | 5 | Approve manuscript draft |
| `citation_discrepancy` | 6 | Citation discrepancy resolution |
| `override_consensus_low` | 7 | Override consensus_low review? |
| `latex_template` | 8 | LaTeX template selection (1 of 23 venues) |
| `visual_review_override` | 8.5 | Visual review override |
| `apply_meta` | 10 | Apply meta-analysis findings? |
| `generate_slides` | 11 | Generate slide deck? |
| **`lattice_conflict`** | 1.5 (SGCA) | Are these two concepts the same? (batch up to 10 per run) |
| **`speculation_authorize`** | 6 (SGCA) | Authorize this speculation? |
| **`byok_setup_needed`** | 0 (preflight) | Host-native dispatch unavailable AND no BYOK configured — set up BYOK or abort? |

## BYOK opt-in — only when host-native unavailable

The **primary** dispatch path is the host CLI's native subagent
mechanism. BYOK (`vedix provider add ...`) is an **alternative**, only
relevant when:

- The pipeline is invoked from a context with no agentic-CLI host
  (e.g. cron, CI, SaaS backend, standalone Python script), AND
- The user hasn't pre-configured BYOK providers via
  `~/.vedix/byok/providers.json`.

In that case the pipeline emits gate `byok_setup_needed`. Surface 3 options:

1. **Configure BYOK now** — opens a flow to add Anthropic / OpenAI /
   Google / OpenRouter / GigaChat / YandexGPT / DeepSeek / Qwen /
   Moonshot / Zhipu / Mistral / Cohere / Together / self-hosted via
   `mcp__vedix__configure_provider`. (14 providers per spec §3.2.)
2. **Run with degraded register-classifier negatives only** —
   corpus-prep stage falls back to template-based synthetic negatives;
   classifier training works but the full research pipeline needs an
   LLM. Skips manuscript-writing phases.
3. **Abort** — `mcp__vedix__pipeline_cancel(continuation_token=...)`.

Inside Claude Code / Codex / Gemini / Antigravity, the gate is never
raised because host-native dispatch is always available.

## Intent classification — Phase −1

Before invoking the pipeline, classify the user's request into one of 12
named intents (full table in `routing-intents.md`):

| Intent | Subagent subset triggered |
|---|---|
| `full_research` | literature-searcher → hypothesizer → code-generator → experiment-runner → plotter → manuscript-writer → reviewer (×3) → vlm-reviewer |
| `peer_review_only` | reviewer ×3 + adversarial-review track |
| `literature_only` | literature-searcher (×6 sources) + citator |
| `experiment_only` | code-generator → experiment-runner → plotter |
| `plot_only` | plotter (3-cycle) |
| `review_existing_manuscript` | manuscript-review path; uses elsevier-cas-sc.tex template |
| `codebase_research` | codebase-scanner → hypothesizer (with codebase context) → ... |
| `meta_analyze_prior_jobs` | meta-analyst |
| `slides_from_manuscript` | slide-presenter |
| `cross_validate_corpus` | citator + literature-searcher (DOI verification) |
| `tree_search_experiment` | tree-search-runner (BFTS) |
| `sgca_reviewer_pass` | adversarial reviewer with independent literature-search-R + graph-builder-R per the SGCA spec |

Pass the intent to `mcp__vedix__run_pipeline(intent=...)`. The pipeline
picks the smallest agent subset that satisfies the intent.

## Available subagents (17 + SGCA paper-extractor = 18)

Each is one `.md` file under `plugins/vedix/agents/`. Frontmatter `name`
field is the canonical agent name. Claude Code dispatches via
`Task(subagent_type="vedix-<name>")`.

| Agent | Phase | Purpose |
|---|---|---|
| `ideator` | 0.5 | Propose 5 research-idea candidates given a topic |
| `codebase-scanner` | 0.75 | AST-index a user-supplied codebase as research target |
| `literature-searcher` | 1 | Per-source paper search (×6 sources in parallel) |
| `citator` | 1.5 | Cross-validate DOIs via Crossref + DataCite |
| `paper-extractor` | 1.5 (B13 SGCA) | Extract one paper into a multi-typed KG fragment |
| `hypothesizer` | 2 | Generate testable hypothesis grounded in the literature |
| `code-generator` | 3 | Emit experiment.py + requirements.txt |
| `experiment-runner` | 4 | Install + run; auto-fix; collect results.csv |
| `tree-search-runner` | 4 (BFTS variant) | Wraps Sakana's BFTS for non-obvious experiments |
| `plotter` | 5.5 | 3-cycle iterative figure refinement |
| `manuscript-writer` | 6 | 6 parallel section-writers (Opus 4.7 max-effort) |
| `reviewer` | 7 | NeurIPS-format peer review (×3 stances) |
| `vlm-reviewer` | 8.5 | Vision-LM critique of rendered figures |
| `meta-analyst` | 10 | Cross-job meta-analysis for failure-pattern learning |
| `slide-presenter` | 11 | Beamer + python-pptx deck generation |
| `fixer` | any | Diagnoses pipeline failures, surfaces fix options |
| `codex-cross-validator` | any | Codex-bridge cross-validation when running under Claude Code |

Full per-agent specs in `plugins/vedix/agents/<agent>.md`.

## Reference files in this skill directory

- `routing-intents.md` — 12-intent dispatch table with full agent subsets
- `domain-templates.md` — 8 discipline configs (chemistry/biology/medicine/physics/maths/geology/CS/humanities)
- `academic-domains.md` — trusted publisher allowlist
- `search-queries.md` — 8-query strategy per discipline
- `references/codex-tools.md` — Codex spawn_agent + skill-loading mapping
- `references/gemini-tools.md` — Gemini inline-reasoning mapping

## MCP tools exposed by Vedix

| Tool | Purpose |
|---|---|
| `mcp__vedix__run_pipeline` | Start a pipeline; returns first dispatch_request |
| `mcp__vedix__pipeline_continue` | Submit subagent output OR user gate answer; returns next dispatch_request or `complete` |
| `mcp__vedix__pipeline_cancel` | Abort the pipeline run |
| `mcp__vedix__dispatch_phase` | Lower-level: ask "what subagent next?" without starting a full pipeline (used by sub-flows) |
| `mcp__vedix__configure_provider` | BYOK setup (only used after `byok_setup_needed` gate) |
| `mcp__vedix__validate_corpus` | DOI-gated cross-validator over a paper list |
| `mcp__vedix__run_plotter_cycle` | Single plotter cycle (inspect/critique/polish) |
| `mcp__vedix__search_knowledge_index` | Read prior-job knowledge index |
| `mcp__vedix__get_knowledge_details` | Fetch specific entries by id |
| `mcp__vedix__list_jobs` | List historical jobs |
| `mcp__vedix__get_status` | Status of a specific job |
| `mcp__vedix__get_output` | Get a section's output for a finished job |

## v3.0 SGCA — Source-Grounded Claim Architecture

When `intent ∈ {full_research, sgca_reviewer_pass, codebase_research}`,
the pipeline runs Phase 1.5 (GraphBuilder) between literature-search and
hypothesizer. This dispatches `paper-extractor` once per paper (parallel,
8-wide). Each extraction emits a structured KG fragment validated against
the schema in `plugins/vedix/mcp/lib/orchestrator/sgca/schema.py`.

Manuscript writing (Phase 6) uses **constrained pre-generation**: for
each paragraph, the planner emits an allowed-set of KG nodes; the
manuscript-writer produces sentences tagged `cite | synthesize |
speculate`; the verifier rejects sentences that don't entail their
anchors. Speculations require either pre-authorization (in the setup
form) or live `AskUserQuestion` confirmation per the
`speculation_authorize` gate.

Full SGCA spec: `docs/superpowers/specs/2026-05-20-source-grounded-claim-architecture-design.md`.

## Universal MemPalace contract

The pipeline owns the per-project palace at `<output_dir>/.palace/`.
Every dispatched subagent does `mempalace_wake_up` on entry and
`mempalace_mine` on exit, scoped strictly to that path. SKILL.md does
not call MemPalace directly.

The v3.0 SGCA KG lives in MemPalace under 4 tier-wings: `vedix_kg__job__`,
`vedix_kg__reviewer__`, `vedix_kg__project__`, `vedix_kg__niche__`. See
the SGCA spec for the lifecycle.

## Cross-validation + Codex fallback

When running under Claude Code with the codex-bridge installed,
`codex-cross-validator` is dispatched on selected phases for an
independent second opinion. This is Claude-Code-exclusive (Codex doesn't
have a Claude bridge to fall back on); the pipeline silently skips this
agent on other hosts.

## v2.1 strict-validation contract (still enforced in v3.0)

These five rules from v2.1 remain non-negotiable; the pipeline blocks
on violation:

1. **DOI is a hard gate.** Every paper in `paper_list.json` must carry
   a verifiable DOI (Crossref/DataCite + fuzzy title ≥ 0.85).
2. **Source accounting is honest.** Every configured source has a
   per-source ledger entry in `source_usage.json` with status
   `ok|degraded|skipped|rate_limited|error`.
3. **Anti-LLMish lint blocks Tier-1 words on any occurrence.** Tier-1
   single-occurrence block: `delve(s/d/ing)`, `underscore(s/d/ing)`,
   `intricate / intricacies`, `showcas(e/ing)`, `meticulous(ly)`,
   `commendable`, `pivotal`, `realm`, `crucial` (exception:
   biochemistry phosphorylation). Em-dash density ceiling: 2 / 1k
   words.
4. **Unquantified claims trigger intra-phase ideation re-dispatch.**
   `claim_audit.py` blocks `outperforms / improves / novel / scalable
   / efficient / robust / generalizes / significant` without a nearby
   number, p-value, sample-size, or hedge.
5. **Codex-native dispatch is preferred when subagents are available.**
   Under Codex with `features.multi_agent = true` and
   `agents.max_threads ≥ 3`, the pipeline uses
   `CodexNativeDispatcher.dispatch_wave` for the 3-bias reviewer phase;
   slot-leak guard (GitHub #18335) closes every spawned agent before
   turn-end.

## Required artifacts (v3.0 acceptance set)

A run is complete when these exist in `<output_dir>`:

| File | Producer phase |
|---|---|
| `tool_preflight.json`, `source_preflight.json`, `codex_runtime_capabilities.json` | 0 |
| `source_usage.json`, `paper_list.json` (with provenance) | 1 |
| `references_validation.json` | 1.5 |
| `sgca/kg_summary.yaml`, `sgca/lattice.yaml` | 1.5 (B13) |
| `sgca/sentence_ledger.jsonl`, `sgca/allowed_sets/` | 6 (B13) |
| `citation_key_integrity.json`, `claim_support_matrix.md` | 6R |
| `reviewer_dispatch.json`, `review.json`, `review_response.md` | 7R |
| `visual_review.json` or `8.5_blocked.json` | 8.5 |
| `parity_report.json` (LaTeX↔Word) | 8 (B7) |
| `AI_disclosure.md` | end (B13) |
| `resource_usage.json`, `manuscript.pdf`, `manuscript.docx` | 10 |

Final response truth-table:

| Question | Answer |
|---|---|
| PubMed used? | yes/no, selected count |
| Anna's Archive used? | yes/no, selected count, member-quota status |
| Semantic Scholar used? | yes/no, selected count, rate-limit status |
| OpenAlex used? | yes/no, selected count |
| arXiv used? | yes/no, selected count |
| bioRxiv used? | yes/no, selected count |
| Metadata fully cross-checked? | yes/no, validator list |
| Citation keys structurally valid? | yes/no |
| SGCA verifier ran? | yes/no, pass-rate, n_rejections |
| Adversarial reviewer track ran? | yes/no, n_reviewers, n_contested |
| LaTeX↔Word parity? | yes/no, divergences |
| Claim support checked? | yes/no, top-cited-only, flagged count |

## Failure modes — what to do when

| Symptom | Action |
|---|---|
| Pipeline returns `{"error": "missing_dep", "dep": "<name>"}` | Surface to user; suggest `pip install <name>` if Python or `npm i -g <name>` if Node |
| `dispatch_request` returned but Task tool absent (some host) | Fall back to inline reasoning per `gemini-tools.md` |
| Subagent returns malformed JSON | Pass back to pipeline with `agent_output_status="malformed"`; pipeline will re-dispatch with stricter prompt (max 2 retries) |
| User cancels via Ctrl+C / explicit | Call `mcp__vedix__pipeline_cancel(continuation_token=...)`; ensures MemPalace cleanup |
| Pipeline timeout (>2h on a single phase) | Surface progress + offer resume; pipeline state is checkpoint-resumable |
