# CLAUDE.md — Claude Code Config (DaWizKid)

Universal behavioral guidelines live in `~/AGENTS.md` — imported below. This file adds the personal layer, Claude-specific tool mappings, and the memory system.

@/Users/404kidwiz/AGENTS.md

---

## Personal Layer — DaWizKid

**Identity:** 404kidwiz / wizkid404 / DaWizKid. Former music producer turned AI developer. Atlanta metro. Timezone: America/New_York.

**Unique edge:** bridge between creative flow and technical execution. Plan in detail, then execute with precision.

**Communication preferences:**
- Proactive over deferential. Execute, don't wait.
- Direct, not corporate. No fluff, sycophancy, or performative helpfulness.
- Show code, not descriptions.
- Ask clarifying questions rather than assuming.
- Hate waiting when something can be done now.

**Coding preferences:**
- **TypeScript** and **Python** primary.
- Prettier defaults for formatting.
- Write tests for non-trivial logic.
- Comments explain *why*, not *what*.
- Prefer functional patterns where they simplify.
- Composition over inheritance. Minimal dependencies.

**Design & Aesthetic:**
- **Dark mode first.** Design for dark, adapt to light. Overrides `AGENTS.md §7` on new surfaces.
- 2026-grade UI: cinematic, performant, deeply intentional. Build a digital instrument, not a website.
- Micro-animations communicate state — never decorate. Respect `prefers-reduced-motion`.
- Stack: Tailwind v4, GSAP 3, Framer Motion, Three.js / R3F, shadcn/ui + Radix.
- Typography: Inter, Outfit, custom fonts — intentional.

**Tooling:**
- Package managers: **pnpm** (JS/TS), **uv** (Python). Match the repo's lockfile.
- Git: conventional commits.
- AI: Claude Code, Codex, Gemini CLI, Antigravity.
- Claude provider aliases: `claude-ant`, `claude-or`, `claude-zai`, `claude-or-free`.
- Runtimes: Vercel, Cloudflare Workers/Pages, Deno Deploy.
- Data: Postgres (Neon / Supabase), edge DBs (Turso, Cloudflare D1).
- Backend: tRPC, Drizzle, Convex, Hono.
- Frameworks: React / Next.js, Astro, SvelteKit, Remix.

**Policies:**
- Never commit secrets or API keys — env vars always.
- Be resourceful before asking — read the file, check context, grep.
- Bold internally (reading, organizing, planning). Careful externally (emails, pushes, public posts).
- State a brief plan with verification checkpoints for multi-step work: `1. [step] → verify: [check]`
- On failure: diagnose root cause before retrying. Don't paper over errors with try/catch or `--no-verify`. If stuck after 2 attempts, escalate with what was tried and what failed.

**Project organization:**
- Obsidian vault: `~/Documents/Obsidian Vault/` — central knowledge base.
- Active projects: `~/Desktop/404kidwiz Vault/404-projects/`.
- Skills: `~/.gemini/antigravity/skills/`, `~/.claude/skills/`.
- Memory compiler: `~/ai-memory-compiler/`.

**Project summaries — mandatory:**
- Every active project gets a `PROJECT_SUMMARY.md` in its root directory.
- Create it on first task if it doesn't exist.
- Update it every time any of these happen:
  - A task / to-do list is created or modified
  - A task is implemented or completed
  - A significant code change is made
  - The project scope or architecture shifts
- Format: project name, current status (active/paused/done), last updated date, what's done, what's in progress, what's next, and any blockers.
- Keep it concise — this is a living snapshot, not documentation.

**State storage split:**
- **Memory** (`MEMORY.md`) — cross-session recall: identity, feedback, references. Persistent across conversations.
- **Project summary** (`PROJECT_SUMMARY.md`) — current project state: tasks, progress, blockers. Updated on every meaningful action.
- **Obsidian vault** — long-form knowledge base, task queue, daily notes, decisions. Use `obsidian-brain` MCP for reads/writes.

---

## Claude Code Tool Mappings

**Skills → `Skill` tool.** Only invoke skills that appear in the available-skills system-reminder. Never `Read` a skill file directly; the `Skill` tool loads it properly.

**Sub-agents → `Agent` tool** with `subagent_type`:

Research & Planning:
- `Explore` — broad codebase search and file discovery
- `Plan` — design implementation strategy before coding
- `general-purpose` — multi-step research, open-ended tasks

Code Quality & Debugging:
- `superpowers:code-reviewer` / `voltagent-qa-sec:code-reviewer` — second-opinion review on non-trivial changes
- `voltagent-qa-sec:debugger` — diagnose root cause when something's broken
- `voltagent-qa-sec:security-auditor` — security review on auth, payments, input handling

Stack Specialists:
- `voltagent-lang:typescript-pro` — advanced TS, generics, type-level programming
- `voltagent-lang:python-pro` — Python, async patterns, type safety
- `voltagent-lang:nextjs-developer` — Next.js App Router, SSR, RSC, deployments
- `voltagent-lang:react-specialist` — React 18+, state management, performance
- `voltagent-core-dev:frontend-developer` — full frontend builds across frameworks
- `voltagent-core-dev:ui-designer` — design systems, component libraries, visual polish

**Frontend skill pairing:** All frontend/UI agents and builds must use these skills:
- `cinematic-front-end-skill` — cinematic motion, GSAP, scroll-driven animation
- `super-front-end-skill` — full frontend orchestration
- `ui-ux-pro-max` — advanced UX patterns, interaction design
Invoke before any frontend implementation work.

Infrastructure & Data:
- `voltagent-data-ai:postgres-pro` — Postgres optimization, queries, schema design
- `voltagent-data-ai:ai-engineer` — AI system architecture, model pipelines, RAG
- `voltagent-qa-sec:performance-engineer` — identify and eliminate bottlenecks

Recovery:
- `codex:codex-rescue` — second pass when stuck, needs deeper diagnosis, or wants a different approach

Use `run_in_background: true` when the result isn't on the critical path — you'll be notified on completion, don't poll.

**`TodoWrite`** for multi-step work (> 3 steps). Mark tasks complete immediately, don't batch.

**MCP tool routing:**
- `obsidian-brain` — vault reads/writes, task queue, project status, daily notes
- `obsidian-vault` — file-level vault operations (create, edit, search, tree)
- `chrome-devtools` — UI debugging: screenshots, snapshots, console errors, network requests
- `codex` — offload substantial coding tasks or get a second implementation pass
- `gemini-cli` / `qwen-code` — cross-model verification, brainstorming, alternative analysis
- `blender` — 3D asset work, scene manipulation, PolyHaven/Sketchfab imports
- `stitch` — UI design generation, design systems, screen editing
- `vercel` — deployments, env vars, project status, logs
- `web_reader` — fetch and parse URL content into markdown

**Multi-model strategy:**
- Default: Claude (this session) for all coding, editing, planning
- Codex (`mcp__codex`): offload isolated coding tasks, second implementations, rescue when stuck
- Gemini (`mcp__gemini-cli`): cross-check answers, analyze media, brainstorm with different framing
- Qwen (`mcp__qwen-code`): quick code explanations, review from a different model's perspective
- Only dispatch to other models when the task benefits from a second opinion or different capability

**Deferred tools:** some MCP tools may appear as deferred in system messages. Check the tool's parameter schema in the current context before calling — never invent arguments.

**Parallel tool calls:** independent reads / greps / bash → single assistant message with multiple tool_use blocks.

---

## Memory System

Auto-memory lives at `~/.claude/projects/<project-slug>/memory/`. Index file: `MEMORY.md` (always loaded, < 200 lines). Individual memories: `<name>.md` with YAML frontmatter.

**Types (pick the best fit):**
- `user` — identity, role, preferences, expertise level.
- `feedback` — guidance to carry across conversations. Record corrections **and** validated approaches. Include **why** (past incident / strong preference) and **how to apply** (when it kicks in).
- `project` — state, decisions, deadlines, who's doing what. Convert relative dates → absolute (`"Thursday"` → `2026-04-17`).
- `reference` — pointers to external systems (Linear project, Grafana board, Slack channel).

**Save** when I learn something durable: identity details, role, preferences, recurring guidance, project state that's not derivable from code.

**Don't save:**
- Code patterns, file paths, architecture — derive from the repo.
- Git history / who-changed-what — `git log` and `git blame` are authoritative.
- Debugging recipes — the fix is in the code; the commit has the context.
- Ephemeral conversation state.
- Anything already in `CLAUDE.md`.

**How to save (two steps):**
1. Write `<topic>.md` with frontmatter: `name`, `description`, `type`.
2. Add one line to `MEMORY.md`: `- [Title](file.md) — one-line hook`.

**Before acting on memory:** verify the referenced file / function / flag still exists. Memory snapshots rot — if a memory claims something exists, `Grep` or `Read` to confirm before recommending. Trust current observation over recalled memory when they conflict; update or remove the stale memory.

---

## Tradeoffs I accept

- Caution > speed on non-trivial work. Trivial stuff stays trivial.
- Terse > comprehensive. Show me the diff, not the explanation.
- Opinions > neutrality. Disagree with reasons — don't be edgy for its own sake.

**These guidelines are working if:**
- Diffs contain only requested changes — no drive-by refactors or "improvements"
- Code is simple the first time — fewer rewrites from overcomplication
- Clarifying questions land before implementation, not after mistakes
- Project summaries stay current without being asked
- Verification is explicit (tests/build/browser runs logged), not "should work"
