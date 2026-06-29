---
description:  The systematic sequence for cleanly wrapping up a long conversation, securing all state and memory to disk, and preparing the workspace for a fresh context window
---

# Workflow: Context Hygiene

**Description:** The systematic sequence for cleanly wrapping up a long conversation, securing all state and memory to disk, and preparing the workspace for a fresh context window.

## Phase 1: Secure Long-Term Knowledge

- Identify any architectural decisions made in this session and log them to `.agents/memory/decisions-log.md`.
- Identify any mistakes, failed approaches, or dead-ends, and log them to `.agents/memory/mistakes-to-avoid.md`.
- Identify any new conventions or reusable code patterns and log them to `.agents/memory/common-patterns.md`.

## Phase 2: Secure Immediate State

- Read the current `.agents/workflow-state.json` file.
- Update the `workflow`, `current_phase`, and `completion_pct`.
- Write a clear, concise summary in the `notes` field detailing exactly what was just finished and exactly what the next session must focus on.
- Update `key_decisions` and `blockers` based on the session's events.
- Write the updated JSON back to disk.

## Phase 3: Verification & Handoff

- Verify that both the `.agents/memory/` markdown files and `.agents/workflow-state.json` have been successfully updated.
- Output a final summary to the user detailing exactly what was saved.
- Formally advise the user to close this chat and open a new window to continue the sprint with maximum sharpness.
