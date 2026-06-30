---
name: prompt-decorators
description: >
  Activates a structured decorator framework that modifies how Claude reasons, responds,
  and formats output. Trigger this skill whenever a prompt contains one or more markers
  prefixed with +++, such as +++Reasoning, +++StepByStep, +++Tone(style=formal), or any
  other +++ marker, regardless of what follows in the prompt. Also trigger when the user
  asks to activate, list, or clear decorators, references the prompt decorator framework,
  or uses phrases like "use decorator", "apply +++", or "what decorators are available".
  This skill must be active for any +++ marker to take effect.
---

# Prompt Decorators

Lightweight control markers that modify reasoning, style, structure, and session behavior.
Activated by the `+++` prefix. Multiple decorators can be combined in a single prompt.
Each decorator's full definition lives in its own file under `references/`. Load only the file(s) you need.
The Quick Reference table below maps every decorator to its file.

---

## Parsing Decorators from a Prompt

When a prompt contains `+++` markers:

1. Extract all decorator names and parameters from the prompt (they appear before the main content)
2. For each decorator, load its definition from `references/<DecoratorName>.md` (e.g. `+++Reasoning` → `references/Reasoning.md`, `+++StepByStep` → `references/StepByStep.md`). Use the Quick Reference table in this file to map decorator names to file paths.
3. Apply all active decorators simultaneously to the response
4. Parameters are passed in parentheses, for example: `+++Tone(style=formal)`, `+++Refine(iterations=3)`

If an unrecognized decorator is used, note it and proceed with the rest.

---

## Scope Rules

Decorators operate in one of two scopes:

| Scope | Behavior |
|-------|----------|
| **Message scope** (default) | Decorator applies only to the current prompt |
| **Chat scope** | Decorator persists across all subsequent messages until cleared |

- `+++ChatScope`: switches all decorators in the same message to chat scope; they auto-apply to every future prompt
- `+++MessageScope`: pauses chat-scoped decorators for the current message only (does not erase them)
- `+++Clear`: removes all active chat-scoped decorators; `+++Clear(+++Reasoning, +++Tone)` removes only the named ones
- `+++ActiveDecs`: lists all currently active chat-scoped decorators
- `+++AvailableDecs`: lists all available decorators with name, description, and current status

Track active chat-scoped decorators across the conversation and apply them automatically even when the user does not re-specify them.

---

## Combining Decorators

All decorators in a prompt apply simultaneously and in order. They do not conflict, each governs a different dimension of the response (reasoning process, tone, format, verification, etc.). When decorators overlap in effect, use judgment to satisfy both.

Example:
```
+++Reasoning
+++StepByStep
+++Tone(style=formal)

Explain how transformer models handle attention.
```
→ Begin with explicit reasoning, structure the body as labeled steps, maintain formal tone throughout.

---

## Quick Reference

| Category | Decorator | Definition File |
|----------|-----------|----------------|
| Reasoning & structure | `+++Reasoning` | `references/Reasoning.md` |
| Reasoning & structure | `+++StepByStep` | `references/StepByStep.md` |
| Reasoning & structure | `+++Socratic` | `references/Socratic.md` |
| Reasoning & structure | `+++Debate` | `references/Debate.md` |
| Evaluation & refinement | `+++Critique` | `references/Critique.md` |
| Evaluation & refinement | `+++Refine(iterations=N)` | `references/Refine.md` |
| Evaluation & refinement | `+++Candor(level=L)` | `references/Candor.md` |
| Exploration & planning | `+++Brainstorm` | `references/Brainstorm.md` |
| Exploration & planning | `+++Planning` | `references/Planning.md` |
| Exploration & planning | `+++Interactive` | `references/Interactive.md` |
| Exploration & planning | `+++Import(topic=T)` | `references/Import.md` |
| Rewriting & clarification | `+++Rewrite` | `references/Rewrite.md` |
| Output control | `+++OutputFormat(format=F)` | `references/OutputFormat.md` |
| Output control | `+++Tone(style=S)` | `references/Tone.md` |
| Verification | `+++FactCheck` | `references/FactCheck.md` |
| Verification | `+++CiteSources` | `references/CiteSources.md` |
| Verification | `+++Validate` | `references/Validate.md` |
| Session management | `+++ChatScope` | `references/ChatScope.md` |
| Session management | `+++MessageScope` | `references/MessageScope.md` |
| Session management | `+++Clear` | `references/Clear.md` |
| Session management | `+++ActiveDecs` | `references/ActiveDecs.md` |
| Session management | `+++AvailableDecs` | `references/AvailableDecs.md` |
| Export | `+++Export(format=F)` | `references/Export.md` |
| Export | `+++Dump` | `references/Dump.md` |
