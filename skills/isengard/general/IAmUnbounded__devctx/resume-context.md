---
description: Load saved DevContext and present it to the AI for session continuity
---

# Resume Context Workflow

When the user says `/resume-context`, load the saved DevContext for the current branch and present it so the AI understands the full history.

## Steps

// turbo
1. Run `devctx resume --stdout` to get the formatted context:

```bash
devctx resume --stdout
```

2. Read the output and **internalize it** — treat it as your briefing on:
   - What was being worked on
   - What has been tried (and what failed)
   - What decisions were already made (don't re-decide these)
   - Where things were left off
   - What the next steps are

3. Acknowledge to the user what you've loaded, e.g.:
   > "I've loaded the context from your last session. You were working on **[task]**, and left off at **[state]**. The next steps are: [next steps]. Ready to continue?"

## Important

- **Don't re-explain** what DevContext told you — just confirm you have it
- **Don't re-decide** things that were already decided — respect prior decisions unless the user explicitly wants to revisit
- **Start from where they left off** — pick up the next step, don't start from scratch
