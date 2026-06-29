---
description: Audit a live web page to find mock data, hardcoded values, LLM-fabricated metrics, and broken endpoints. Opens the URL in Playwright, clicks every interactive element, traces every visible value to its actual source (DB/API/mock/LLM/hardcoded), and produces a markdown report. Use when the user wants a reality check on a vibe-coded app, AI-generated UI, or any web app where data provenance is uncertain.
---

# MockHunter — Live Page Reality Check

Audit a web page in five phases. For every value visible on screen, classify its source as one of: **REAL / MOCK / LLM / HARDCODED / BROKEN / UNKNOWN**.

Output: a markdown report the user can read in two minutes.

> **Philosophy:** A rendered value is not verified until you've traced it to its source. "It looks like a number" is not evidence that a number was computed.

---

## Quickstart

User invokes `/mockhunter:mockhunter`. Skill collects inputs, runs all five phases, writes `mockhunter-report.md` to the current directory.

If the user provides only a URL, ask the smart questions (Phase 1). If the user provides full config upfront, skip directly to Phase 2.

---

## Inputs

Collect these in Phase 1. Required unless marked optional.

| Input | Required | Default |
|---|---|---|
| Target URL | Yes | — |
| Auth mode | Yes | `skip` (one of: `public`, `localhost`, `form`, `skip`) |
| Auth credentials | If `form` | — |
| Has database? | Yes | `N` |
| DB connection (string OR shell command) | If has DB | — |
| Stack hint (optional) | No | autodetect from URL |
| Suspicions (optional) | No | — |
| Money page (optional) | No | target URL |

Auto-detect stack from URL pattern when not provided:
- `*.lovable.app` → Lovable
- `*.bolt.new`, `*.stackblitz.io` → Bolt
- `*.v0.app`, `*.v0.dev` → v0
- `*.replit.app`, `*.repl.co` → Replit
- `aistudio.google.com/*` → Google AI Studio
- everything else → Custom

---

## The Five Phases

### Phase 1 — Setup & Smart Questions

1. Greet the user in one line: *"MockHunter — I'll audit a page and tell you what's real, what's mocked, and what's broken."*
2. Ask for the target URL if not supplied.
3. Ask up to 5 smart questions, picked from this pool based on context:
   - *"What is this page supposed to do for the user?"* (frames audit)
   - *"Which numbers, badges, or sections do you most suspect are mocked?"* (focuses scrutiny)
   - *"Do you have a way to query the database directly? If yes, paste the command (e.g., `psql ...`, `docker exec ...`, Supabase SQL link)."* (enables deep trace)
   - *"What stack is this built with?"* (skip if auto-detected)
   - *"Are any sections intentionally AI-generated content (so I don't false-flag them)?"*
4. Ask about auth mode if URL looks like it might require login (presence of `/login`, `/auth`, `/dashboard` in path; or stack hint suggests authenticated app).
5. Confirm the audit plan with one short summary, then proceed.

**Don't ask all 5 questions if 2 are enough.** Read the user's first message carefully — if they say "audit my Lovable dashboard, no auth, here's the URL," that already answers most questions.

### Phase 2 — Navigate & Catalog

Use Playwright MCP tools.

1. `browser_navigate` to the target URL.
2. Handle auth:
   - `public` / `skip` / `localhost`: nothing
   - `form`: navigate to login URL, fill email + password fields, click submit, wait for navigation
3. Wait for page to settle: `browser_wait_for` on network idle, max 10s.
4. `browser_take_screenshot` → save to `mockhunter-screenshots/01-initial.png` (full page).
5. `browser_snapshot` → capture accessibility tree.
6. From the snapshot, build an element inventory:
   - Headings (h1–h6) with text
   - Buttons with label, ref, disabled state
   - Links with href and visible text
   - Form inputs with type, name, current value
   - Tabs / nav regions
   - Data displays: text content of every card, badge, stat, list item, table cell
   - Empty state messages ("No data", "—", "Coming soon")
   - Images with src, alt, loaded status
7. `browser_console_messages` → capture initial console errors.
8. `browser_network_requests` → capture initial network log.
9. Detect tab/section structure. Record list of tabs.

**Output of phase:** Element inventory, console log, network log, screenshot path.

### Phase 3 — Test Interactivity

For every tab and every button found in Phase 2:

**Tabs (highest priority — switch context first):**
1. For each tab not yet visited:
   - `browser_click` the tab
   - `browser_wait_for` network idle, 5s max
   - `browser_take_screenshot` → `mockhunter-screenshots/tab-{name}.png`
   - `browser_snapshot` → re-catalog elements visible in this tab
   - Append to console log + network log
   - Scroll to bottom: `browser_evaluate` with `window.scrollTo(0, document.body.scrollHeight)`, snapshot again
   - Note any new elements revealed below the fold

**Buttons (after all tabs covered):**

For each button (excluding nav, excluding any matching destructive patterns — see safety rules below):

1. Note button label and current page state (URL, modal-open?)
2. `browser_click` the button
3. Wait 2s, snapshot
4. Classify outcome:
   - Modal opened? → record modal contents, then close it
   - Toast/notification appeared? → record text
   - Navigation occurred? → note new URL, return with `browser_navigate_back`
   - Network request fired? → record the request (URL, method, status)
   - Nothing happened? → flag as **NO-OP** (likely unwired button)
5. If a modal opened, also: snapshot modal, record any form fields, attempt to close (Escape key or close button)

**Forms:**

For each form on the page:
1. Identify required fields (asterisk, `required` attribute, label cues)
2. Try **empty submit** first → check for client-side validation
3. If validation present and submit is non-destructive: try a valid submit with throwaway data
4. Record API call triggered, response status, success/error UX

**Safety rules (CRITICAL — never bypass):**
- **Skip any button matching** `/delete|remove|cancel|deactivate|terminate|destroy|drop|wipe|clear|reset|logout|sign out|transfer|pay|purchase|charge|send (email|message|invoice)|publish|deploy/i` — log as "skipped (destructive)"
- **Skip any link** with `target="_blank"` to an external domain (don't follow)
- **Never type real credentials** into forms during the audit (use `mockhunter@example.com` / `MockHunterTest123!` for throwaway form tests)
- **If a button label is ambiguous (`Apply`, `Continue`, `Confirm`)** and the surrounding context suggests a state-changing operation, ask the user before clicking
- **Stop and ask** if a clicked button initiates payment, OAuth grant, or external API write

**Output of phase:** Behavior log — every interactive element with its observed outcome, expanded inventory, expanded network log.

### Phase 4 — Trace Provenance (the heart)

For every visible value on the page (from the inventories built in Phases 2 + 3), determine its source.

**Run this decision tree per value:**

```
Visible value V (e.g., "73% engagement", "$4,231", "EMERGING")

Step 1: Did any network request return this value (or its component)?
  ├── Search response bodies in network log for V (string match, fuzzy numeric match)
  ├── If found in response from /api/* (own backend):
  │   ├── HTTP status 4xx/5xx → BROKEN (with status code)
  │   ├── HTTP 2xx with V present:
  │   │   ├── Endpoint path matches /ai|openai|generate|llm|chat|completion → LLM
  │   │   ├── Response shape has prompt/completion/model/tokens keys → LLM
  │   │   ├── Response has known mock-library shape (faker, mockoon, MSW) → MOCK
  │   │   ├── Apply uniformity heuristics (see below) → MOCK or LLM (flag for review)
  │   │   ├── DB connection provided?
  │   │   │   ├── Yes → run query, check if V exists in expected table
  │   │   │   │   ├── Match found → REAL (cite table.column)
  │   │   │   │   ├── No match → MOCK (likely seeded or hardcoded server-side)
  │   │   │   │   └── Table doesn't exist → MOCK or BROKEN
  │   │   │   └── No DB → UNKNOWN (best-guess based on heuristics)
  ├── If found in response from external API (Stripe, Supabase, third party):
  │   └── REAL (note: external dependency)
  └── If NOT found in any network response:
      ├── Step 2: Inspect DOM source for V
      │   ├── browser_evaluate: find element, walk up to component source if available
      │   ├── V appears as string literal in inline HTML / JSX serialized to client → HARDCODED
      │   ├── V is computed from Math.random / Date.now / faker / static array → MOCK
      │   ├── V is a static badge (TRENDING, NEW, EMERGING, HOT) without data backing → HARDCODED (or LLM if AI-generated label)
      │   └── Cannot determine → UNKNOWN
```

**Uniformity heuristics — flag as suspicious:**
1. All items in a list have identical numeric value (e.g., every row "2 mentions") — variance < 1 unit
2. All percentages are round numbers (50%, 75%, 90%) — no values like 73.4%
3. All timestamps cluster within a single minute (batch-seeded, not organic)
4. All strings in a "data" column have identical structure (template-generated)
5. Numeric series has < 3 unique values across 10+ items

**Detection rule:** If any column shows uniformity by 2+ of the above signals → likely seeded/templated/LLM, flag as MOCK or LLM.

**LLM-specific signals (additional checks):**
- Response field names like `summary`, `analysis`, `insight`, `recommendation`, `suggestion` with prose values
- Endpoint paths ending in `/explain`, `/summarize`, `/recommend`, `/predict`, `/score`
- Values that are too well-formed prose for a typical data field (full sentences in a "type" or "category" column)
- Numeric "scores" (probability, confidence, viral, engagement) without a backing table

**HARDCODED-specific signals:**
- String literals in DOM that match common placeholder patterns: "Lorem ipsum", "John Doe", "user@example.com", "Acme Inc"
- Round-number percentages or scores not present in any network response
- Timestamps formatted as "2 hours ago", "yesterday" but no actual datetime in DOM/state
- Counts/badges (5 new, 3 unread) that never change after refresh

**For each value, record:**
```
{
  value: "73% engagement",
  location: "Dashboard > Top Card > Engagement Metric",
  verdict: "HARDCODED",
  evidence: "String literal in <Badge>73%</Badge>, no /api/engagement call observed",
  severity: "P1",
  recommended_action: "Add API endpoint or label as 'Sample data'"
}
```

**DB verification (if user provided DB access):**

Use the user's provided shell command. Examples of how it can look:
- `psql "$DB_URL" -c "SELECT ..."` — direct Postgres
- `docker exec my-app-db psql -U user -d db -c "..."` — dockerized
- A Supabase HTTP endpoint with service role key (use `curl`)
- `mysql -h ... -e "..."` — MySQL

For each REAL candidate, run a verification query. **Never run destructive queries (no UPDATE, DELETE, DROP, TRUNCATE, INSERT).** Read-only SELECTs only. If user's command uses an interactive shell, embed the SELECT directly.

If a query fails, note "DB verification failed: {error}" but continue — don't fail the audit.

**Output of phase:** Provenance map — every visible value labeled.

### Phase 5 — Report

Generate `mockhunter-report.md` in current working directory (or path specified).

**Report structure:**

```markdown
# MockHunter Report

**URL:** {url}
**Audit completed:** {timestamp}
**Stack detected:** {stack}
**Auth mode:** {mode}
**DB verification:** {enabled|disabled}

## Summary

| Verdict | Count |
|---|---|
| REAL | N |
| MOCK | N |
| LLM | N |
| HARDCODED | N |
| BROKEN | N |
| UNKNOWN | N |

**Total elements scanned:** N
**Console errors:** N
**Failed network requests:** N

## Findings

### {Section/Tab Name}

| # | Element | Value | Verdict | Source | Severity | Action |
|---|---------|-------|---------|--------|----------|--------|
| 1 | "Engagement" badge (Dashboard top card) | 73% | HARDCODED | String literal in JSX | P1 | Wire to GET /api/metrics/engagement |
| 2 | "Recent Activity" list | (empty) | BROKEN | GET /api/activity → 404 | P0 | Implement endpoint or remove section |
| 3 | "Total Revenue" stat | $4,231 | REAL | Stripe API → DB invoices.amount_total | — | None |
| 4 | "Viral score" badge | 75% | LLM | POST /api/ai/score → GPT-4 response | P1 | Label as "AI estimate" or remove |
| 5 | "Trending Up" indicator | ↑23% | MOCK | Math.random()*100 in components/Trend.tsx | P2 | Replace with real time-series math |

### {Next Section/Tab}
...

## Console Errors

```
[error] Failed to load resource: 404 — /api/activity (DashboardPage.tsx:42)
[warn] React: missing key prop in list ...
```

## Network Failures

| Method | URL | Status | Triggered by |
|---|---|---|---|
| GET | /api/activity | 404 | Dashboard mount |
| POST | /api/comments | 500 | "Add comment" button |

## NO-OP Buttons (clicked, nothing happened)

- "Refresh data" — Dashboard top right
- "Export" — Reports page
- "Settings" — Sidebar gear icon

## Suspicious Patterns

- All 5 items in "Top Performers" have engagement = 73% (uniformity flag — likely seeded)
- All timestamps in "Recent Activity" cluster within 60 seconds of deploy time
- "Insights" cards have prose summaries with no underlying data — likely LLM-generated

## Smart Questions for the User

1. The dashboard makes 8 parallel API calls on mount — is that intentional, or should some be combined?
2. "Viral score" is LLM-generated. Is that the intended UX, or should it be a real calculation?
3. "Refresh data" button is a NO-OP. Did it lose its handler, or was it never wired up?
4. Cold-start (zero data): what should this page show? Currently it shows hardcoded mock values.

## Methodology

- Phases run: 1, 2, 3, 4, 5
- Auth mode: {mode}
- DB verification: {enabled|disabled}
- Stack: {stack}
- Audit duration: {duration}
- Total network requests captured: N
- Total interactive elements tested: N

## Severity Reference

- **P0** — Broken endpoints, data integrity failures, fabricated metrics presented as real data
- **P1** — Hardcoded values masquerading as dynamic, unlabeled LLM data, misleading empty states
- **P2** — Mock data clearly intentional but unlabeled, suspicious uniformity in real data
- **P3** — Cosmetic, expected mock data (placeholder avatars, lorem ipsum in early-stage UI)

---

*Generated by MockHunter v0.1.0 — https://github.com/CodeShuX/mockhunter*
```

**Final step in Phase 5:** Print a one-screen summary to the user:

```
✅ MockHunter audit complete

URL: {url}
Verdict counts: REAL: X | MOCK: X | LLM: X | HARDCODED: X | BROKEN: X

🚨 Top issues (P0):
  1. {issue}
  2. {issue}

📄 Full report: ./mockhunter-report.md
📸 Screenshots: ./mockhunter-screenshots/
🔍 Raw trace: ./mockhunter-trace.json

Next: ask me to dive deeper on any finding, or run on another page.
```

---

## Tools Used

| Tool | Purpose |
|---|---|
| Playwright MCP (`browser_navigate`, `browser_snapshot`, `browser_take_screenshot`, `browser_click`, `browser_type`, `browser_fill_form`, `browser_evaluate`, `browser_wait_for`, `browser_console_messages`, `browser_network_requests`, `browser_navigate_back`, `browser_press_key`) | Live browser control, element inventory, screenshots, network/console capture |
| Bash | DB queries (read-only SELECTs only), shell commands user provides |
| Write | Generate `mockhunter-report.md`, save trace.json |
| Read | Re-read partial outputs as needed |
| AskUserQuestion (when available) | Smart questions in Phase 1 |

---

## Key Principles

### Provenance over presence
A rendered value is not verified until you've traced it to its source. "It looks correct" is not evidence.

### Honest UNKNOWN
If you can't determine the source within the audit's reach, label it **UNKNOWN** — never guess REAL. UNKNOWN with explanation is more useful than false certainty.

### Conservative interactivity
Never click destructive-sounding buttons. Never submit forms with real-looking data unless explicitly safe. The audit must not mutate the user's app.

### Cold-start awareness
Test what the page looks like when data is empty. If most sections are empty, that's a P1 UX issue (the page doesn't guide the user).

### Cite specifically
Every finding must cite either: (a) a specific network request (URL + status), (b) a specific DOM source (component file:line if available), or (c) a specific DB query result. "I think it's mock" is not a valid finding.

### Stop and ask, don't guess
When in doubt — destructive button, ambiguous form, payment flow — stop and ask the user. The audit's job is to inform, not to break.

### Stack-aware heuristics
Lovable apps mock differently than Bolt apps. v0 apps are usually frontend-only. Use stack detection to tune classification (e.g., a v0 app with no backend should expect HARDCODED, not flag everything as broken).

### No false equivalence
A clearly-labeled "Sample data" section is fine. An unlabeled fabricated metric presented as analytics is P1. The skill must distinguish honest placeholders from misleading ones.

---

## Edge Cases & Limitations

| Case | Behavior |
|---|---|
| App requires 2FA / magic-link / OAuth | Document workaround: user logs in manually first; skill detects existing auth state. v0.1.0 doesn't auto-handle these. |
| App is a SPA with heavy lazy-loading | Wait for network idle up to 10s, then proceed. Document limitation. |
| Frontend-only app (no backend at all) | Expected. Most values will be HARDCODED or MOCK. Report frames this honestly: "Detected: frontend-only app. All visible data is local; no backend was contacted." |
| User provides invalid DB connection | Audit continues without DB verification, all REAL candidates downgrade to UNKNOWN. Report notes "DB verification skipped due to connection error." |
| Audit runs >10 minutes | Acceptable. Report progress per phase. v0.2 may add streaming. |
| Page returns 500 on initial load | Report this as P0 in summary, attempt one retry, then write a partial report and stop. |
| Auth fails | Stop after one retry, ask user to verify credentials, do not continue blindly. |
| Page has 100+ buttons | Cap at 30 most-prominent buttons (by visual area / viewport position) for v0.1.0. Note the cap in the report. |

---

## What this skill does NOT do

- Visual regression / pixel diffing — use Applitools, Percy
- Performance audit — use Lighthouse
- A11y audit — use Axe (could be added in v0.2)
- SEO audit — use Lighthouse, Screaming Frog
- Multi-page crawl — v0.1.0 audits one page per run
- Auto-fix code — produces recommendations, not patches
- Continuous CI runs — interactive only in v0.1.0
- Test generation — use LaVague QA

---

## Versioning

This is `mockhunter` v0.1.0. Spec at https://github.com/CodeShuX/mockhunter/blob/main/SPEC.md.

If you change phase semantics or input format, bump the minor version and update SPEC.md in the same PR.
