# rldyour Antigravity CLI Context

You are operating inside the `rldyour-antigravity-cli` adapter repository (now
Antigravity CLI-targeted). This adapter configures Antigravity CLI with
native surfaces for the rldyour AI CLI control plane.

## Current Facts

- Adapter version: `1.5.1`.
- Runtime: Antigravity CLI `1.0.8` (primary), Gemini CLI `0.46.0` (enterprise legacy).
- Install: `curl -fsSL https://antigravity.google/cli/install.sh | bash`
- Config path: `~/.gemini/antigravity-cli/settings.json`
- MCP config: `~/.gemini/antigravity-cli/mcp_config.json`
- Hooks: `~/.gemini/config/hooks.json` (shared with Gemini CLI)
- Binary: `agy` (not `gemini`)
- Supported access target: enterprise, paid API-key, Vertex AI, Google Cloud, or
  explicitly owner-approved authenticated environments.
- Consumer OAuth availability after June 18, 2026 is not promised because Google
  transitioned unpaid and Google One users to Antigravity CLI.

## Operating Rules

- Use Antigravity CLI-native configuration files: `GEMINI.md`,
  `.gemini/antigravity-cli/settings.json`, `.gemini/antigravity-cli/mcp_config.json`,
  `gemini-extension.json`, TOML commands, skills, agents, hooks, and policies.
- Configure only providers listed in the approved active inventory; removed or
  historical tools require an explicit inventory and release-policy update.
- Keep browser routing split: Webwright for long-horizon workflows, Playwright
  CLI for screenshots/flows/visual evidence, Chrome DevTools MCP for debugging.
- Gemini built-in `browser_agent` is disabled for this release; do not enable it
  unless it is modeled as a separate explicit provider with validators.
- In standard mode, the owner/user remains the orchestration layer.
- In cmux mode, orchestration exists only as visible terminal sessions.
- Gemini subagents are internal Antigravity CLI delegation, not cmux workers.
- Headless `antigravity-cli -p` is allowed for smoke, doctor, and CI checks only.
- Never commit secrets, OAuth state, service-account files, browser artifacts,
  runtime caches, or temporary evidence.

## Required Report Shape

When reporting work, include exact files changed, commands run, pass/fail
results, and any `NOT PROVEN` gaps. Do not claim release certification unless
the root control plane and all adapter gates pass.
