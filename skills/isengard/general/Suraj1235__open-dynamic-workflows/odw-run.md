# /odw-run — plan and execute a dynamic workflow

Saved Antigravity workflow (install: copy into `~/.gemini/antigravity/global_workflows/`).

Steps:
1. Run `node ~/.gemini/skills/odw/scripts/daemon-bridge.js --check`. If it fails, tell the user how to start the daemon and stop.
2. Run `node ~/.gemini/skills/odw/scripts/daemon-bridge.js plan "{{prompt}}"` and show the user the topology, agent count, and cost estimate.
3. On confirmation, run `node ~/.gemini/skills/odw/scripts/daemon-bridge.js exec plan.json`, then `result <wf_id>`, and summarize the outcome.
