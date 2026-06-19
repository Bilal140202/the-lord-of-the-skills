---
name: release-review
description: "Проверь release readiness Gemini adapter и public CI policy. EN: release review."
---

# Purpose

Validate that current release surfaces, CI, tags, metadata, and archives are
coherent.

# Native Gemini Boundary

Release review validates Gemini-native config and public adapter policy.

# When To Use

Use before tagging, publishing, or integrating this adapter into the root tuple.

# Inputs

Version files, changelog, workflows, validators, tests, and release artifacts.

# Procedure

1. Check version parity.
2. Check native Gemini surfaces.
3. Check workflows and release metadata.
4. Check archive hygiene.
5. Verify GitHub Release evidence when credentials allow.

# Evidence Required

Command results, tag/release URL, commit SHA, and artifact validation output.

# Forbidden Actions

Do not certify release with `NOT_PROVEN` runtime, GitHub, or archive evidence.

# Acceptance Checks

All local validators, pytest, and release/archive hygiene checks pass.

# Failure Reporting

State exact non-green gates and whether they are blockers or `NOT_PROVEN`.
