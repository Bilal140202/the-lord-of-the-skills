---
description: Save full context from current AI conversation to DevContext
---

# Save Context Workflow

When the user says `/save-context`, you must introspect the **entire current conversation** and extract the following, then call `devctx save` with all of it.

## Steps

1. **Analyze the conversation** and extract:
   - **task**: What was the user working on? (one-line summary)
   - **approaches**: What approaches were tried? (include failed ones — those are valuable)
   - **decisions**: What key decisions were made? (architecture choices, library picks, design patterns)
   - **state**: Where did things end up? What's the current state?
   - **nextSteps**: What comes next? What's left to do?
   - **blockers**: Anything blocking progress?

2. **Run the save command** with ALL structured fields. Use `;;` as the separator between items:

// turbo
```bash
devctx save "TASK_SUMMARY" \
  --approaches "approach 1;; approach 2;; approach 3" \
  --decisions "decision 1;; decision 2" \
  --state "Current state description" \
  --next-steps "step 1;; step 2;; step 3" \
  --blockers "blocker 1;; blocker 2"
```

Omit any flags that don't apply (e.g., no `--blockers` if there are none).

3. **Confirm** to the user what was saved.

## Example

If the conversation was about refactoring a payment service:

```bash
devctx save "Refactoring payment service from REST to event sourcing" \
  --approaches "Tried direct DB events first, too coupled;; Switched to dedicated event store;; Considered Kafka but went with simpler in-process event bus" \
  --decisions "Using event sourcing for payment state;; In-process event bus for MVP, Kafka for scale;; Keeping REST endpoints as thin adapters over command handlers" \
  --state "Command handlers working for CreatePayment and RefundPayment. Event store persists and replays correctly. Need to wire up read-side projections." \
  --next-steps "Build read-side projections for payment queries;; Add idempotency keys to commands;; Integration tests for event replay" \
  --blockers "Need to decide on snapshotting strategy for large event streams"
```

## Important

- **Be thorough**: Include approaches that FAILED — those prevent the next session from repeating mistakes
- **Be specific**: "Using RS256 for JWT signing" is better than "configured auth"  
- **Capture reasoning**: "Chose Postgres over MongoDB because we need transactions" captures the WHY
- **Don't ask the user** to summarize — that's your job. Extract it from the conversation.
