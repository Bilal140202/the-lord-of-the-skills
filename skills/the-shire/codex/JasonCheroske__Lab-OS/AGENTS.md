---
created: 2026-04-17
updated: 2026-04-17
---

# Agents: working in this Lab OS workspace

## Load order

1. **[README.md](README.md)** — startup arc, validate/promote hints, links to the Lab OS seed runbooks.
2. **[docs/README.md](docs/README.md)** — pillar index for `.lab/*`.
3. **[.lab/intent/ARCHITECTURE_TARGET.md](.lab/intent/ARCHITECTURE_TARGET.md)** — target direction.
4. **[.lab/reality/IMPLEMENTATION_MAP.md](.lab/reality/IMPLEMENTATION_MAP.md)** — what exists.
5. **[.lab/delta/GAP_MAP.md](.lab/delta/GAP_MAP.md)** — gaps and planned work.
6. **[.lab/behavior/GOVERNANCE_POLICY.md](.lab/behavior/GOVERNANCE_POLICY.md)** — protected areas and sign-off expectations.

Prefer **editing existing pillars** over inventing parallel doc trees. Keep `docs/project-structure.md` consistent with the real folder layout as code appears.

## Rules of thumb

- Treat `lab.yaml` and the required `.lab/*` files as **source of truth** for governance and stage; optional `docs/*`, this file, and root `README.md` are companions (they may be removed without failing validation—see Lab OS `LAB_CONTRACT`).
- Propose **ADRs** under `.lab/evidence/adrs/` when decisions are durable.
- After substantive edits, remind the human to run **validate** (and **promote** only when evidence supports it).

## Optional: Cursor

If this repo is opened in Cursor, a conversation-first `/lab-init` workflow can precede deep implementation; scaffolding commands still come from the Lab OS toolkit or `lab-os` CLI.

## Reference

- [Seed startup runbook](https://github.com/JasonCheroske/Lab-OS/blob/main/docs/30-runbooks/SEED_STARTUP_RUNBOOK.md)
- [Adoption guide](https://github.com/JasonCheroske/Lab-OS/blob/main/docs/30-runbooks/ADOPTION_GUIDE.md)

## Change history

| Date | Change summary | Editor |
| --- | --- | --- |
| 2026-03-27 | Initial AGENTS.md for template root copy. | Lab OS seed |
