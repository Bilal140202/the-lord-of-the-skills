---
description: Run the Vedix research pipeline. Full or partial based on flags.
argument-hint: "<topic> [--domain ml|optimization|statistical|mathematical|computational_biology|software_engineering] [--codebase <path>] [--output <dir>] [--full] [--only <agent>] [--no-word-export] [--reviewer-model opus|sonnet]"
---

Invoke the vedix skill with the user's full command line as the topic + flags. The skill handles argument parsing.

If `--full` is present, force the full 12-phase pipeline regardless of phrasing.
If `--only <agent>` is present, dispatch only that single agent.
Otherwise, the skill's Phase −1 classifier picks the agent subset based on the topic phrasing.
