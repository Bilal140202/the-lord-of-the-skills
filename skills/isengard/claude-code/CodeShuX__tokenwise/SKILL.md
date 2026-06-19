---
description: Run an A/B test of the same task at multiple model tiers (Haiku, Sonnet, optionally Opus). Captures outputs, computes structural and semantic diffs, scores quality, writes a markdown comparison report. Use when the user wants to validate "is Haiku good enough for this task class?" or runs /tokenwise:ab "<task description>".
---

# /tokenwise:ab — A/B test a task across model tiers

Run the same task at multiple tiers and compare outputs.

## Parse $ARGUMENTS

Expected form: `<task description> [--tiers haiku,sonnet,opus]`

- The task description is everything before the first `--` flag (or the whole string if no flags)
- `--tiers haiku,sonnet` is the default (skip Opus by default — it's the baseline)
- `--tiers haiku,sonnet,opus` runs all three

If `$ARGUMENTS` is empty, ask the user:
> What task should I A/B test? Provide a task description (e.g., "rename getCwd to getCurrentWorkingDirectory across the codebase").

## Steps

1. **Confirm cost upfront:**
   ```
   A/B test will run this task <N> times (once per tier).
   Estimated cost: $<rough estimate based on task size>.
   Proceed? [Y/n]
   ```
   Estimate by treating the task as ~10k input + ~1k output per tier and summing.

2. **For each tier:**
   - Spawn a Task at that tier: `Task(description: <task>, subagent_type: "general-purpose", model: <tier>, prompt: <task>)`
   - Capture: stdout, input_tokens, output_tokens, duration_ms, errors
   - If the Task tool's `model:` param is silently overridden (Anthropic Issue #47488), warn user and abort with:
     > Cannot A/B test on this Claude Code build — subagent model routing is not honored. See `/tokenwise:install` probe results.

3. **Compute diffs:**
   - **Structural:** line count, character count, token overlap (Jaccard on word sets)
   - **File-list diff:** if outputs mention modified files, compare the lists
   - **Semantic:** spawn one more Task at Opus tier with the prompt:
     > Compare these N outputs for the task "<task>". Score each from 1-10 on (a) completeness, (b) correctness, (c) clarity. Return a JSON object: `{"<tier>": {"completeness": N, "correctness": N, "clarity": N, "overall": N, "notes": "..."}}`. Be honest — if two outputs are equivalent, give them the same score.

4. **Compute cost per tier:**
   - Use the same pricing as `/tokenwise:report`:
     - Opus 4.7: $5 input / $25 output per 1M tokens
     - Sonnet 4.6: $3 / $15
     - Haiku 4.5: $1 / $5
   - cost = (input/1M)*input_price + (output/1M)*output_price

5. **Write report to** `./tokenwise-ab-<YYYYMMDD-HHMMSS>.md`:

```markdown
# A/B Test — <first 80 chars of task>
Run: <ISO 8601 timestamp>
Task: "<full task>"
Tiers tested: <list>

## Tier comparison

| Tier   | Tokens (in/out)  | Cost     | Duration | Quality |
|--------|------------------|----------|----------|---------|
| Haiku  | <in> / <out>     | $<cost>  | <ms>     | <q>/10  |
| Sonnet | ...              | ...      | ...      | ...     |

## Semantic scores

(table with completeness/correctness/clarity per tier, plus notes from the judge)

## Recommendation

(One paragraph: which tier is sufficient for this task class, what override rule to add to CLAUDE.md if any.)

## Output diffs

(For each tier, include the full output verbatim, or a truncated version with full output in a fenced block.)
```

6. **Also log the A/B run** to `.tokenwise/log.ndjson` with `task_class: "ab-test"` so it doesn't pollute regular routing stats.

7. **Print summary to stdout:**
   ```
   A/B test complete.
   Report: tokenwise-ab-<ts>.md
   Recommendation: <one-sentence recommendation>
   ```

## Caveats to mention to the user if relevant

- **Non-deterministic tasks** (e.g., "suggest improvements") will have varying outputs across runs. The A/B is advisory in those cases.
- **Multi-step tasks** that need user input mid-flow cannot be A/B'd cleanly. Decompose first.
- **A/B costs** are not part of normal routing stats — they're tagged separately.

## Tools

Task (for spawning per-tier runs and the semantic judge), Read, Write, Bash.
