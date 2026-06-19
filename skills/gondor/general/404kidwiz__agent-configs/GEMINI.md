# GEMINI.md — Gemini CLI Config (DaWizKid)

Universal behavioral guidelines live in `~/AGENTS.md` — imported below. This file adds the Gemini CLI-specific layer.

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
- **Dark mode first.** Design for dark, adapt to light.
- 2026-grade UI: cinematic, performant, deeply intentional. Build a digital instrument, not a website.
- Micro-animations communicate state — never decorate. Respect `prefers-reduced-motion`.
- Stack: Tailwind v4, GSAP 3, Framer Motion, Three.js / R3F, shadcn/ui + Radix.
- Typography: Inter, Outfit, custom fonts — intentional.

**Tooling:**
- Package managers: **pnpm** (JS/TS), **uv** (Python). Match the repo's lockfile.
- Git: conventional commits.
- Runtimes: Vercel, Cloudflare Workers/Pages, Deno Deploy.
- Data: Postgres (Neon / Supabase), edge DBs (Turso, Cloudflare D1).
- Backend: tRPC, Drizzle, Convex, Hono.
- Frameworks: React / Next.js, Astro, SvelteKit, Remix.

**Policies:**
- Never commit secrets or API keys — env vars always.
- Be resourceful before asking — read the file, check context, grep.
- Bold internally (reading, organizing, planning). Careful externally (emails, pushes, public posts).
- State a brief plan with verification checkpoints for multi-step work: `1. [step] → verify: [check]`
- On failure: diagnose root cause before retrying. If stuck after 2 attempts, escalate with what was tried and what failed.

---

## Gemini CLI — Tool Mappings

**Skills:** use `activate_skill` for skill invocation. Skills live at `~/.gemini/antigravity/skills/`.

**Multi-model collaboration:**
- Default: Gemini for this session's tasks.
- Claude Code: for Claude-specific tooling, MCP servers, sub-agent dispatch.
- Codex: for isolated coding tasks or second implementation passes.
- Use Gemini's strengths: media analysis, web search with grounding, long context, brainstorming.

**MCP servers available (when configured):**
- `obsidian-brain` — vault reads/writes, task queue, daily notes
- `chrome-devtools` — UI debugging, screenshots, snapshots
- `codex` — offload coding tasks
- `stitch` — UI design generation, design systems

**Frontend skill pairing:** All frontend/UI work must use these skills:
- `cinematic-front-end-skill` — cinematic motion, GSAP, scroll-driven animation
- `super-front-end-skill` — full frontend orchestration
- `ui-ux-pro-max` — advanced UX patterns, interaction design

---

## Memory

Gemini memory lives in `~/.gemini/` paths. See `AGENTS.md` for universal memory principles.

---

## Tradeoffs I accept

- Caution > speed on non-trivial work. Trivial stuff stays trivial.
- Terse > comprehensive. Show me the diff, not the explanation.
- Opinions > neutrality. Disagree with reasons — don't be edgy for its own sake.
