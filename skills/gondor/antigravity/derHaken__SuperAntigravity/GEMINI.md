# SuperAntigravity Skills

You have superantigravity installed — a complete workflow and specialist skills framework.

## MANDATORY: Check Skills Before Acting

Before taking ANY action — including asking clarifying questions, exploring files,
writing code, or debugging — you MUST check whether a skill applies.

Even a 1% chance a skill might apply = you MUST check it.

This is not optional. This is not negotiable.

## How Skills Work in Antigravity

Skills are loaded automatically when your task matches the skill's description.
The agent reads skill descriptions for all installed skills and loads the full
content of matching ones before acting.

Skills live in: ~/.gemini/antigravity/skills/

## Skill Priority

1. **Process skills first** (brainstorming, systematic-debugging) — determine HOW to approach
2. **Implementation skills second** (architecture-design, deep-research) — guide execution

"Let's build X" → brainstorming first.
"Fix this bug" → systematic-debugging first.

## Red Flags — You Are Rationalizing

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Let Antigravity load the current version. |
| "This doesn't count as a task" | Action = task. Check for skills. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |

## Available Slash Commands

Type `/` followed by any of these names to trigger explicit workflows:

| Command | Purpose |
|---------|---------|
| /brainstorm | Design before code — requirements discovery |
| /plan | Write implementation plan |
| /implement | Feature implementation |
| /research | Deep research with parallel search |
| /build | Build, compile, package |
| /test | Run tests with coverage |
| /git | Git operations with smart commits |
| /analyze | Code quality, security, performance analysis |
| /design | Architecture and API design |
| /troubleshoot | Debug issues systematically |
| /explain | Explain code or concepts |
| /improve | Apply improvements to code |
| /review | Code review |
| /cleanup | Remove dead code, optimize structure |
| /document | Generate documentation |
| /estimate | Development estimates |

## Specialist Skills

| Skill | When to use |
|-------|-------------|
| `deep-research` | Task needs external information before proceeding |
| `performance-optimization` | Code needs profiling and optimization |
| `security-review` | Code touches auth, input handling, or sensitive data |
| `architecture-design` | Designing systems, APIs, or significant features |
| `confidence-check` | About to implement — verifies readiness |
| `browser-agent` | Interacting with web browser, testing UI flows, verifying web app behavior |
| `dependency-management` | Adding, updating, auditing, or evaluating project dependencies |
