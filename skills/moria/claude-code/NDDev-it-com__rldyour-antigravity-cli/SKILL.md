---
name: ry-deploy
description: "Подготовь Gemini deploy/release handoff. EN: prepare Gemini deploy or release handoff."
---

# Purpose

Prepare and verify deployment, release, or publication work for Gemini adapter
changes.

# Native Gemini Boundary

Gemini headless prompts are allowed for smoke/doctor/CI checks only. Persistent
orchestration remains cmux visible-terminal-only.

# When To Use

Use when a request includes deploy, release, publish, rollout, server, or
production handoff.

# Inputs

- Target environment or release repository.
- Branch, tag, artifact, credential, health-check, and rollback requirements.
- Current validator and GitHub release evidence.

# Procedure

1. Confirm target, credentials policy, and rollback path.
2. Run required validators and artifact hygiene checks.
3. Confirm GitHub release/CI evidence where applicable.
4. Execute only explicitly authorized deploy/release steps.
5. Report artifact paths, run URLs, health checks, and rollback criteria.

# Evidence Required

Commands, artifact paths, release tags, GitHub run URLs, health check output,
and explicit `NOT_PROVEN` gaps.

# Forbidden Actions

Do not invent credentials, servers, release tags, CI proof, or background
orchestrators.

# Acceptance Checks

Release/deploy state is reproducible from source-of-truth commands and clean
artifacts.

# Failure Reporting

Lead with blockers that prevent safe deploy or release.

