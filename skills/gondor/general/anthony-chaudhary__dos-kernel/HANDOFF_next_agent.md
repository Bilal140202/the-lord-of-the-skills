# Handoff — prove DOS natural lift on a weak model (next agent)

> **GOAL:** Prove DOS produces real, NATURAL lift on a genuinely weak/medium model on the
> ServiceNow EnterpriseOps-Gym benchmark — "as real as possible" (no synthetic injection).
> This is the docs/153 weak-model question. Everything below is grounded; verify before trusting.

## Where the program stands (read these first, in order)

- **docs/152** — the experiment that just ran. DETECT works live, FIX is inert **on a strong model**.
- **docs/153** — "Can DOS lift a weak model?" — the question this next step answers.
- **docs/149 / docs/150** — the failure distribution (~92 % premature completion) + the
  `dangling_intent` crack.
- **`benchmark/enterpriseops/RESULTS.md` + `THEORY_LADDER.md`** — the full history + the tier ladder.

### The measured result (authoritative)

100 paired natural tasks, `gemini-2.5-flash`, `--mint-rate 0`, 4 domains:

- `dangling_intent` **DETECT works live**: fired on **9/100 runs (9 %)**, **0 % false-fire** on passed runs.
- **FIX is inert at the task level**: 0/9 fired stops converted to a task pass, 0/9 derailed
  (WARN-only floor held — no run dead-ended). **+2 / −0 verifier-CHECKS** on the fired tasks.
- Whole-corpus **−1.9 pp is re-seed noise** on the 91 untouched tasks, NOT the mechanism.
- Re-run the analysis any time ($0, no API):
  ```bash
  cd benchmark/enterpriseops
  python dangling_convert.py --out live_results_natural_run --sample live_results/_sample
  ```

**Conclusion:** on a CAPABLE model the narrating stopper often stopped *because* it couldn't form
the step, so re-surfacing its own words supplies no plan → no net lift. The lift, if it exists, is
on a model weak enough to narrate steps it CAN actually execute when reminded.

## The next step (the one decisive experiment)

Run the SAME `none`-vs-`resurface` A/B (mint 0, `dangling_intent` ON) on a **genuinely weaker model**
than `gemini-2.5-flash` — one that fails MORE at premature completion but can still execute a step
when its own abandoned sentence is re-surfaced. The wiring is already built and proven; you only
need a weaker model reachable + a run + the conversion join.

The whole apparatus is shipped and committed (`df3254d`, `e41b63a`, `5c640b6` on `master`):

- **`dos_react.py`** — the `DOS_DANGLING` stop-event hook (re-surfaces the agent's own sentence once).
- **`live_ab.py`** — the `resurface` arm (`DOS_CONSULT=0`, `DOS_DANGLING=1`); UTF-8 stdout; inter-arm
  env cleanup; `dangle%` firing-rate column.
- **`score_ab.py`** — `dangling_warns` / `dangling_runs` telemetry.
- **`dangling_convert.py`** — the fire-rate + conversion-rate + net-delta join (the deliverable).
- **`replay_dangling.py`** — the $0 DETECT replay (run it on the new model's `none` trajectories first).

### The only blocker — getting a weaker model that runs

- Today ONLY `GEMINI_API_KEY` is in `.env`; the gym's `gemini.json` key is an `AQ.Ab8...` access-token
  (53 chars) — **it works** (verified live) but is access-token-shaped, may expire; smoke it first.
- The **openrouter/openai path is BLOCKED**: `langchain_openai` is NOT installed. To use a small
  Llama/Qwen/DeepSeek you must FIRST: `cd enterpriseops-gym && uv sync --extra openai` (or
  `pip install langchain-openai`), then write `conf/llm/<model>.json` + pass `--llm-config`.
  **THIS INSTALL HAS NOT BEEN DONE/TESTED** — verify it works before planning the run.
- **Cheaper alternative** if no weaker model is reachable: degrade `gemini-2.5-flash` (tighter tool
  budget / a weaker system prompt) to manufacture MORE natural premature stops — but that is
  second-best; a genuinely weaker model is the honest test.

### Run (once a weaker model is reachable, ~1 hr, ~$5–10)

```bash
cd benchmark/enterpriseops

# 0. smoke the key/model FIRST (1 task) before the batch:
python live_ab.py --tasks 1 --arms resurface --domains itsm --mint-rate 0 \
    --out /tmp/smoke --llm-config <gym>/conf/llm/<weak-model>.json

# 1. $0 DETECT replay on the weak model's natural `none` trajectories (after a `none`-only run):
python replay_dangling.py <out>/none      # expect fire-rate to RISE vs 2.5-flash's 26%

# 2. the full A/B (writes to a gitignored dir — keep the Gemini key out of git):
python live_ab.py --tasks 25 --arms none resurface --domains itsm csm email hr --mint-rate 0 \
    --out live_results_weakmodel_run --llm-config <gym>/conf/llm/<weak-model>.json

# 3. the deliverable — fire-rate, conversion rate, net delta:
python dangling_convert.py --out live_results_weakmodel_run --sample live_results/_sample
```

**SUCCESS** = on the weaker model, of the FIRED tasks a **NON-ZERO conversion rate** (fail→pass) with
the WARN-only floor still holding (≈0 derailments). That would be the first NATURAL net lift the
program has ever shown. A **null** (conversion still ~0) is ALSO publishable: it would mean even a
weak model's premature stops are "couldn't-do" not "didn't-bother," and DOS owns DETECT only.

## Traps that have already bitten (don't re-learn these)

- **Docker:** 4 MCP containers must be healthy (`eog-itsm:8006` / `eog-csm:8001` / `eog-email:8004` /
  `eog-hr:8008`). Check `docker ps`; they were up this session.
- `live_ab.py` **chdir's into the gym root** (seed_database_file paths are relative). Keep your `--out`
  **absolute**.
- Result files are named `results_oracle__<domain>__<task>.json` (the `results_` prefix); task_id is
  the last `__`-split segment. `score_ab.load_arm` already handles this.
- **Windows console is cp1252** → crashes on em-dash / Δ. `live_ab.py` now forces stdout UTF-8; if you
  add a new print script, do the same (`sys.stdout.reconfigure(encoding="utf-8")`).
- `ToolMessage` needs a `tool_call_id`; at a no-tool-call STOP there is none → use `HumanMessage` for
  the re-surface (already done; **don't regress it**).
- **CONCURRENT AGENTS edit this repo.** Stage ONLY your lane's files (`git add <specific paths>`),
  NEVER `git add -A`. The working tree this session carried another agent's `evidence.py` + docs/155/156.
- All `live_results*/` dirs are **gitignored** (they hold the Gemini key in seed configs). Keep new
  output dirs gitignored too.
- **Trust verifier-pass% / database_state integrity%** (low-variance) over success% at n ≤ 100. Arms
  are NOT verifier-paired (fresh DB per run) → ~5 pp re-seed noise; report it as a floor.

## Doctrine (don't violate)

Byte-clean only (no agent-authored satisfaction predicate); natural over injected; **WARN-only**
(BLOCK/DEFER are net-harmful safety valves, measured); DOS detects/hardens the substrate, it NEVER
supplies the plan (the +14–35 pp planner lever is forfeit by doctrine).

## Deliverable

Update docs/152 §1.5 (or a new `docs/NN`) with the weak-model fire-rate + conversion + net delta,
reporting the RUNG and the noise band, not just a headline. **Commit your lane only.**
