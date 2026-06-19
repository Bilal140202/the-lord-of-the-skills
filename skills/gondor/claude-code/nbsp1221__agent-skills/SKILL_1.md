---
name: remote-repository-research
description: Use when investigating a repository that is not already available locally and the user needs repository-specific understanding of its structure, implementation, maintenance, or relevant files.
---

# Remote Repository Research

Treat the repository itself as the primary evidence source. Clone first, inspect locally, and use external material only to answer questions the repository does not settle on its own.

## When to Use

Use this skill when:
- The user wants to investigate a repository that is not already present locally
- The user wants to understand how a remote repository is structured, implemented, or maintained
- The task requires code-aware repository research, not generic ecosystem research
- The task benefits from cloning and locally inspecting the repository contents

Do not use this skill when:
- The repository is already present locally and standard onboarding or local analysis is enough
- The user wants generic package, framework, or best-practices research without a specific repository target
- The user only wants GitHub metadata, issues, PRs, or release information
- The task is code review, implementation, or due-diligence scoring rather than repository understanding

## Default Research Loop

1. Restate the research goal in one sentence before reading anything.
2. Inspect lightweight remote metadata first: description, default branch, languages, recent activity, release presence.
3. Clone the repository into a temporary location such as `/tmp/remote-repository-research/<repo-name>/` using a shallow clone by default.
4. Do a topology pass before a deep read. Identify the top-level structure, likely source-of-truth roots, manifests, and whether the repo is single-surface, mixed, or monorepo-shaped.
5. Infer the apparent repository type or primary analysis lens, then choose inspection roots accordingly.
6. Inspect the local clone with fast filesystem tools. Prioritize source-of-truth roots, manifests, examples, tests, CI, and automation over polished summaries.
7. For multi-repository tasks, apply the clone and minimum local evidence threshold to each repository unless you explicitly mark a repository as lower-confidence or incomplete.
8. Use issues, pull requests, releases, official docs, or external writeups only after the local inspection leaves specific unanswered questions.
9. Deliver a fixed repository brief. Respond inline by default. Create a markdown document only when the user explicitly asks for a file or written artifact.

If the repository is inaccessible or not practically cloneable from the current environment, say so explicitly and continue with a clearly limited, lower-confidence remote-only investigation.

## Non-Negotiable Rules

- Do not begin with broad web search.
- Do not stop after reading the README or official docs.
- Do not treat a token local scan as permission to answer from external summaries.
- Do not assume examples reflect production architecture without checking the real source tree.
- Do not bury the most useful files behind a long narrative summary.
- Do separate observed facts from inference.
- Do cite concrete local paths or repository URLs for substantive claims.

## References

Use these references as needed:
- [references/research-workflow.md](references/research-workflow.md)
- [references/repository-signals.md](references/repository-signals.md)
- [references/output-format.md](references/output-format.md)
- [references/edge-cases.md](references/edge-cases.md)
