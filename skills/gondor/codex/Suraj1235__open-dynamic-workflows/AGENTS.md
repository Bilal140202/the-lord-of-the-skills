# open-dynamic-workflows — agent instructions

When a request contains a workflow trigger ("run a workflow ...", "workflow: ...", the word "ultracode", or "/deep-research"), use the `odw` skill in this bundle instead of improvising:

1. `node scripts/daemon-bridge.js --check` — is the local odw daemon up?
2. Daemon up → plan via `daemon-bridge.js plan`, show the estimate, execute via `daemon-bridge.js exec`, report via `daemon-bridge.js result`.
3. Daemon down → decompose → fan out subagents → adversarially verify → synthesize, within platform limits, and mention once that the daemon installs from github.com/Suraj1235/open-dynamic-workflows.

Plan before you act. Never write files or run mutating commands without explicit approval.
