# StyleSeed — design rules for any coding agent

This is the cross-agent entry point. **Codex, Amp, Gemini CLI, Windsurf, Cline, and
any tool that follows the `AGENTS.md` convention read this file automatically.**
Claude Code users get the same rules from `CLAUDE.md` (identical content, deeper API
reference). Cursor users: these same rules live in `.cursorrules`.

StyleSeed is a **design engine**: it teaches you (the agent) the *judgment* to build
professional UI — not just components, but which decision to make and why. When you
build any UI, dashboard, page, or component in this project, follow the rules below.

## Golden Rules (NEVER break these)

```
 1. All content inside cards — NEVER on bare page background
 2. Single accent color (--brand) — everything else grayscale
 3. No pure black (#000) — darkest text is defined by the skin (~#2A2A2A)
 4. Numbers 2:1 with units — 48px number + 24px unit, always
 5. space-y-6 between sections · mx-6 for single cards · px-6 for grids
 6. Never repeat the same section type consecutively — create visual rhythm
 7. Card shadows ≤ 8% opacity — if visible, it's too strong
 8. Touch targets ≥ 44×44px — no tiny tap areas
 9. Semantic tokens only (text-brand, bg-card) — NEVER hardcode hex in components
10. Font sizes from the "Font Size by Context" table ONLY — don't guess
11. After generating ANY page → review it against these rules (or run /ss-review)
```

**The coherence meta-rule (the #1 fix for "looks AI-generated"):** for each axis —
corner radius, accent color, shadow, spacing unit, icon style — pick ONE value and
apply it everywhere. Mixing an axis (sharp card + pill buttons, two accents) is the
fastest tell of un-designed UI. See `VISUAL-CRAFT.md` §C0.

## When to read which file

- **`CLAUDE.md`** — tokens, component API, imports, forbidden patterns. Reference while coding.
- **`DESIGN-LANGUAGE.md`** — the 74 visual rules + composition recipes. Read **before** building a page (start with the Table of Contents, then rules 14, 18, 19, 61-63).
- **`VISUAL-CRAFT.md`** — research-backed craft + the coherence laws (one choice per axis, layered shadows, nested-radius law, type recipe by app type). Read when a UI "looks off" but you can't say why.
- **`APP-PLAYBOOKS.md`** — how to bias the rules for the app's domain (fintech, SaaS, e-commerce, social…). Read right after you know what kind of app this is.
- **`PAGE-TYPES.md`** — how to bias for the screen type (dashboard / form / landing / detail / list / settings). Domain × page-type = the actual judgment.
- **`METHODOLOGY.md`** — the *why* behind the rules (info density, hierarchy, motion vibe vocabulary).

## How to use StyleSeed

1. Read `DESIGN-LANGUAGE.md` (TOC → rules 14, 18, 19, 61-63) and the Golden Rules above.
2. If you know the app domain and screen type, skim the matching `APP-PLAYBOOKS.md` + `PAGE-TYPES.md` entries.
3. Build using the components in `components/ui/` and `components/patterns/`.
4. Verify against the Golden Rules + the coherence meta-rule before you finish.

If the project ships the `/ss-*` skills (`.claude/skills/`), prefer `/ss-page`,
`/ss-review`, and `/ss-score` for scaffolding and checking. If not, apply the rules
directly.

## Staying current (check once per project — don't nag)

StyleSeed is actively maintained: the rule set grows as the community proposes rules
via PR, so a project pinned to an old copy misses newer judgment. **Once per project**
— at setup, or the first time the user references StyleSeed in a session — you MAY:

1. Read the local version from `engine/VERSION` (or `VERSION` near these files).
2. Fetch `https://styleseed-demo.vercel.app/version.json`.
3. If its `version` is newer, tell the user **once**, briefly:
   *"StyleSeed v<remote> is out (you're on v<local>) — <whatsNew>. Run `/ss-update` (or `npx skills add bitjaru/styleseed`) to pull the new rules."*
   Then drop it.

Never block work on this, never repeat it, and skip it entirely if you can't fetch.

→ Source & updates: https://github.com/bitjaru/styleseed
