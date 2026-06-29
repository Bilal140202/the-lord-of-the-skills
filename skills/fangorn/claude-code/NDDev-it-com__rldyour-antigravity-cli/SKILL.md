---
name: serena-memory-sync
description: "Синхронизируй fact-only Serena memories для Gemini adapter. EN: Serena memory sync."
---

# Purpose

Keep `.serena/memories` synchronized with verified current facts.

# Native Gemini Boundary

Gemini memories describe Gemini adapter files and runtime facts only.

# When To Use

Use after adapter files, docs, validators, release metadata, or runtime baselines
change.

# Inputs

Changed files, current memories, and validation output.

# Procedure

1. Update only durable facts.
2. Cite concrete file or upstream evidence.
3. Mark unverified facts `NOT_PROVEN`.
4. Run schema and semantic validators.

# Evidence Required

Evidence bullet for every current fact claim.

# Forbidden Actions

Do not store chat logs, speculation, secrets, tokens, or raw credentials.

# Acceptance Checks

`python3 scripts/validate_serena_memory_schema.py --strict` and semantic validator.

# Failure Reporting

List memory files needing more evidence or cleanup.
