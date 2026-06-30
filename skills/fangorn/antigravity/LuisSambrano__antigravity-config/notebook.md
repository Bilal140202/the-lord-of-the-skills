---
description: NotebookLM project memory management. Create, sync, log, and audit project notebooks.
---

# /notebook

Manages project notebooks in NotebookLM via the nlm CLI.

## Prerequisites

nlm CLI installed and authenticated. Verify with: nlm auth status

## Commands

### /notebook init [name]

Creates a new project notebook with initial architecture documents.

Steps:
1. nlm notebook create "[name]"
2. Generate base documents locally in /tmp/nlm_[project]/: brief, UX, architecture, features, infrastructure.
3. Upload each document: nlm source add <notebook-id> --file /tmp/nlm_[project]/NN-file.md --title "NN - Title" --wait
4. Start deep research: nlm research start <notebook-id> "Research market, recommended stacks, and similar projects described in source 01."
5. Return notebook ID. Notify that research is running.

### /notebook sync [name]

Synchronizes the notebook with the current codebase state.

Steps:
1. nlm notebook list to find the target notebook.
2. Download current sources to /tmp/nlm_sync/.
3. Compare against actual code (package.json, DB schemas, deploy URLs).
4. Rewrite stale sources where discrepancies exist.
5. Replace atomically: nlm source delete <old-id> -y && nlm source add <notebook-id> --file updated.md --wait
6. Report which sources were updated and why.

### /notebook log [name]

Appends a session log or architecture decision record.

Steps:
1. Determine next sequence number from existing sources.
2. Create log file with: session context, architectural decisions (decision / reason / long-term consequence), next steps.
3. Upload: nlm source add <notebook-id> --file log.md --title "NN - Log: YYYY-MM-DD [topic]" --wait
4. If the decision invalidates an existing architecture or feature source, run a sync on those sources.

### /notebook audit [name]

Reviews notebook content for quality and accuracy.

Steps:
1. Download all sources to /tmp/.
2. Tone check: find superlatives, absolute promises, marketing adjectives.
3. State check: for every feature marked as operational, verify a commit or URL exists. Degrade to "in progress" if not verifiable.
4. Report violations. Rewrite and re-upload if auto mode is confirmed.
