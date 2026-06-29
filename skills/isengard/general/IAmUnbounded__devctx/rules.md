# Agent Rules

1. **Always Save Context**: Before you finish a task or hand control back to the user (via `notify_user`), you MUST run `devctx save --auto` to persist the session intent, approaches, and decisions.
2. **Use Auto-Extraction**: Do not assume you know the context better than the `devctx` CLI. Use the `--auto` flag to let it extract structured data from your own artifacts (`task.md`, `implementation_plan.md`, `walkthrough.md`).
