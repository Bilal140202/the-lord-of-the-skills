---
created: 2026-04-06
updated: 2026-04-17
---

# Lab templates (`template/`)

Archetypes ship under named subdirectories. `lab-os init` defaults to **`agnostic`**. Use **`--template <name>`** (or **`lab-os create`**) to select another archetype.

| Directory | Role |
| --- | --- |
| [`agnostic/`](agnostic/) | Default seed: knowledge layer, root companions, `.ai/` harness namespace. |
| [`product-starter/`](product-starter/) | Opinionated product-lab starter (domain example). |
| [`meta/`](meta/) | Meta-workshop scaffold for lab-building; may point to full source checkout. |

## Agnostic layout

```text
agnostic/
  README.md (this tree lives under agnostic/)
  root/     → README.md, AGENTS.md copied to target root
  docs/     → companion docs
  lab/      → knowledge layer (copied to `.lab/` by default; use `--knowledge-dir lab` for `lab/`)
  .ai/      → harness namespace
  lab.yaml
```

Files under **`agnostic/root/`** merge into the **target root** on init. Companion **`docs/`** and **`.ai/`** ship with every initialized lab from that archetype. Paths optional for `validate` are described in [LAB_CONTRACT](../docs/10-architecture/LAB_CONTRACT.md).

## Change history

| Date | Change summary | Editor |
| --- | --- | --- |
| 2026-04-07 | Restructure: agnostic archetype under `template/agnostic/` (ADR-0003). | — |
| 2026-04-05 | Add `.ai/` harness namespace to template output; update tree. | Lab OS seed |
| 2026-03-27 | Document `template/root/` consumer README + AGENTS.md in template output. | Lab OS seed |
| 2026-03-27 | Document optional root `docs/` in template output. | Lab OS seed |
