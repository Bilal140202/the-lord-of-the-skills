# Objective
Run a strict two-layer validation sweep against `/Users/Shared/antigravity/testing_folder/.env` and do not stop until every configured provider credential has been classified correctly and every active primary tier has been proven live.

# Context
- Target testing directory: `/Users/Shared/antigravity/testing_folder`
- Environment file: `/Users/Shared/antigravity/testing_folder/.env`
- Source repository: `/Users/Shared/antigravity/3-tier-multi-agent-architecture-work`

# Execution Directives

## Phase 1: Structural Runtime Audit
1. Change directory to `/Users/Shared/antigravity/testing_folder`.
2. Activate the repo-local virtual environment: `source .venv/bin/activate`.
3. Run the structural audit:
   ```bash
   PYTHONPATH=src ./.venv/bin/python scripts/validate_runtime_env.py \
     --workspace . \
     --project-root .
   ```
4. Capture the effective tier matrix, fallback topology, configured provider inventory, active provider env keys, and runtime warnings.

## Phase 2: Active Matrix Live Probe
1. Run the active-tier live probe:
   ```bash
   PYTHONPATH=src ./.venv/bin/python scripts/validate_runtime_env.py \
     --workspace . \
     --project-root . \
     --live
   ```
2. Confirm the currently selected primary tiers can answer a minimal prompt through CrewAI/LiteLLM.
3. Treat this pass as validation of the active runtime only. Do not use it as proof that inactive credentials in `.env` are healthy.

## Phase 3: Configured Provider Healthchecks
1. Run the configured-provider probe and emit the machine-readable report:
   ```bash
   PYTHONPATH=src ./.venv/bin/python scripts/validate_runtime_env.py \
     --workspace . \
     --project-root . \
     --probe-configured-providers \
     --report-path docs/reports/validation_report.json
   ```
2. Probe every configured provider credential found in `.env`, including inactive providers and accepted aliases such as `GEMINI_API_KEY`, `KIMIK_API_KEY`, and `KIMIK_BASE_URL`.
3. Use these canonical healthcheck models and official REST surfaces:
   - OpenAI: `gpt-4o-mini`
   - Gemini: `models:list` and `gemini-3.1-pro-preview:generateContent`
   - MiniMax: `MiniMax-M2.5`
   - GLM: `glm-5`
   - Kimi: `moonshot-v1-auto`
   - DeepSeek: `deepseek-chat`
4. Capture HTTP status, latency, endpoint used, failure classification, and a redacted response preview for every provider probe.

## Phase 4: Self-Correction Loop
1. If the active matrix fails but the underlying credential is valid, patch the source repository, wipe `/Users/Shared/antigravity/testing_folder`, recopy the repo, and rerun Phases 1 through 3.
2. If a provider probe fails with `auth_invalid`, treat the credential itself as dead and report exactly which env var must be replaced.
3. If a provider probe fails with `model_unavailable` or `endpoint_misconfigured`, diagnose the model ID or base URL against the official provider docs, patch the source repository, and rerun the full loop.
4. If a provider probe times out, retry after fixing the timeout cause or provider endpoint selection.

## Success Criteria
- SC1: The structural audit resolves the tier matrix from `.env` without placeholder fallbacks or duplicate-key conflicts.
- SC2: `--live` proves every active primary tier can answer successfully through CrewAI/LiteLLM.
- SC3: `--probe-configured-providers` makes a live outgoing request for every configured provider credential present in `.env`, including inactive providers and alias-backed credentials.
- SC4: Every provider probe either returns `200 OK` or is explicitly classified with a precise failure category and exact env var ownership.
- SC5: `docs/reports/validation_report.json` is regenerated from the current run and is safe to publish because it contains no raw secrets.
