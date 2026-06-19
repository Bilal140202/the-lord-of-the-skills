---
name: Context Hygiene & Session Management
description: >
  Monitors conversation complexity and manages session boundaries.
  Proactively secures state and memory before advising the user to 
  split work across separate chat sessions, preventing context bloat.
trigger_patterns:
  - long implementation sessions
  - multi-step feature builds
  - debugging sessions that shift topics
  - any session exceeding ~30 back-and-forth exchanges
---

# Context Hygiene & Session Management

## Purpose

AI context windows degrade as conversations grow. After ~30+ exchanges, the AI loses track of earlier constraints, starts hallucinating details, and wastes tokens re-reading irrelevant history. 

This skill teaches Anti-Gravity to actively manage session boundaries **automatically** — securing all progress to disk before the user moves to a clean chat window.

## When to Advise a Session Split

Recommend the user open a new chat window when:

1. **The task changes significantly.** If we finished debugging and are now building a new feature, that is a new session.
2. **The conversation exceeds ~30 exchanges.** Context quality degrades. Proactively say: "We've covered a lot. I recommend starting a fresh chat for the next piece so I stay sharp."
3. **Multiple unrelated tasks are being discussed.** Each task deserves its own clean context.
4. **A micro-task sequence is complete.** After finishing a planned set of tasks, suggest: "Good stopping point. For the next batch, a fresh session will give you better results."

## How to Execute a Handoff (The Zero-Friction Method)

Never ask Beloved to manually copy-paste a "Handoff Brief." Instead, perform these two steps automatically:

### Step 1: Secure Long-Term Knowledge (Memory)
Before suggesting a split, ensure all permanent knowledge from this session is written to disk:
- Did we make an architectural choice? Write it to `.agents/memory/decisions-log.md`.
- Did we learn what *not* to do? Write it to `.agents/memory/mistakes-to-avoid.md`.
- Did we establish a new convention? Write it to `.agents/memory/common-patterns.md`.

### Step 2: Secure Immediate State (Workflow)
Update `.agents/workflow-state.json` so the next session knows exactly where to resume. 
Ensure the `notes`, `key_decisions`, and `phases` fields are perfectly up to date.

*Reference format from `GLOBAL_MEMORY.md`:*
```json
{
  "workflow": "build-feature",
  "current_phase": "IMPLEMENT",
  "completion_pct": 64,
  "notes": "Finished the UI layout. Next session must focus on wiring the submit button to the API.",
  "key_decisions": ["Used Flexbox instead of Grid for the main container"],
  "blockers": []
}
```

### Step 3: Inform the User
Once the files are updated, tell Beloved:
> *"I've secured our progress in `workflow-state.json` and logged our decisions to Memory. This chat is getting long — I recommend opening a new chat window to continue. The new session will automatically read the state file and pick up exactly where we left off."*

## When NOT to Split

- In the middle of a single atomic task (don't interrupt flow)
- When the user is in a sprint and splitting would break momentum
- When the conversation is short and focused
