---
name: lab-init
description: >-
  Runs a conversation-first design and tailoring workflow for any project shape (single or multi-service, mixed stacks, infra), then optionally produces a paste-ready sprout handoff for the target folder. Use when the user says /lab-init or asks to bootstrap, initialize, design, or tailor a lab or project before scaffolding. Lab OS npm seed commands apply only when sprout mode is lab-os-seed in this repository.
created: 2026-04-06
updated: 2026-04-06
---

# Lab Init (`/lab-init`)

**Vocabulary:** **Phase A = Plan** (design and tailoring with the user and AI). **Phase B = Sprout execution** (materialize or run agreed steps after confirmation). **Planting** the seed at a root and **sprouting** commits that folder as a **lab workspace**—**practically irreversible** in the Lab OS model (no automated un-sprout). See [docs/60-reference/FOUNDATIONS_VOCABULARY.md](../../../../docs/60-reference/FOUNDATIONS_VOCABULARY.md).

**Default behavior:** **Phase A — Design & Tailoring (Plan)** (conversation first, **no file writes and no install/init commands** unless the user explicitly asks for execution inside Phase A).

**Optional:** **Phase B — Sprout** only after the user confirms **target path**, **sprout mode**, and **execution**.

Non-Cursor users can mirror Phase B for this repo with `npm run lab:init` / `npm run lab:verify` when sprout mode is `lab-os-seed` **here**.

## Phase A — Design & Tailoring (always start here)

### Rules

- Do **not** run `npm install`, `npm run init`, `npm run lab:init`, or write project files by default.
- If the user demands commands in Phase A, confirm intent; otherwise keep outputs as **design text** only.
- Produce a **design package** that matches project complexity: one Mermaid diagram for simple systems; **multiple** focused diagrams when boundaries, flows, or environments would be unclear in one chart.
- **Diagram hygiene:** no secrets in trees or Mermaid (use placeholders for tokens, keys, sensitive hostnames).
- **This repository only:** the living Lab OS product map ([`docs/60-reference/LAB_ARCHITECTURE_FLOWCHART.md`](../../../../docs/60-reference/LAB_ARCHITECTURE_FLOWCHART.md)) is maintained with [**`/flow-diagram`**](../flow-diagram/SKILL.md)—compact Mermaid, lookup tables, no `click`. Use **`/lab-init`** for Phase A/B design and sprout; **`/flow-diagram`** when refreshing that canonical chart after structural changes.

### Question themes (adapt order to context)

Cover what matters; skip irrelevant sections with explicit "N/A".

- **Project shape:** monolith vs multi-service vs multi-repo; teams and ownership if known.
- **Stacks / runtimes:** Node, Python, Go, etc.; infra (Terraform, OpenTofu, K8s, etc.).
- **Material and unknowns:** what docs/code exist; what is unknown or disputed.
- **Anchors:** non-negotiables, constraints, compliance, SLAs.
- **Environments:** local → dev/staging → prod; promotion and rollback posture.
- **Validation gates:** tests, CQRS read/write paths, integration points, smoke checks per service.
- **Seed placement (conceptual):** where the lab or repo root might live (folder-agnostic until Phase B).

### Required design package (content)

1. **Project profile** — domains, services, stack map (prose or table).
2. **Known / unknown inventory** — bullets.
3. **Anchor points and assumptions** — explicit; separate **risks**.
4. **Phased plan** — local → dev → prod (or your pipeline).
5. **Validation gates** — what must pass before promotion.
6. **Project structure** — ASCII tree with short per-folder annotations (Grand Exchange–style "where things live"; see [examples.md](examples.md)).
7. **Mermaid diagram set** — at least one; multiple when needed:
   - service/module boundaries
   - data or control flow (including CQRS if relevant)
   - environments and promotion / infra touchpoints
8. **Artifact layout (logical paths)** — use stable default paths so sprouting is predictable:
   - `docs/project-structure.md` — tree + annotations
   - `docs/diagrams/*.md` **or** sections in `docs/architecture.md` for diagrams
   - `docs/README.md` — mini-index linking structure, diagrams, risks, sprout handoff
9. When boundaries change later, **update the affected diagram(s)** and note the change briefly.

### Phase A output format

Use clear headings. End Phase A with:

- **Phase A complete** (summary)
- **Proceed to sprout?** (yes/no)

If no: stop with design artifacts in chat (user can save manually).

## Phase B — Sprout (opt-in; gated)

### Preconditions

- Phase A design package is accepted by the user.
- User explicitly chooses to sprout.

### Steps

1. **Target folder** — absolute or workspace-relative path where work should apply.
2. **Sprout mode** — user must pick one:
   - `docs-only` — materialize or refine **documentation only** (design package files).
   - `lab-os-seed` — apply **this repository’s** Lab OS lab scaffold (`lab.yaml`, `lab/` tree, validation/promotion scripts) in the target **when this repo is the context**; requires Node 20+ and npm here.
   - `custom` — user describes stack-specific steps; agent proposes an ordered plan; still requires confirmation before execution.
3. **Execution gate** — do not run commands or write files until the user confirms **Execute sprout**.
4. Emit a **sprout handoff** block (below) for pasting into the AI session rooted at the target folder (repeatable context).

### Sprout handoff template (copy for user)

```text
[Sprout handoff — paste into AI in <target-folder>]
Target: <path>
Mode: docs-only | lab-os-seed | custom
Summary: <one paragraph: goal, anchors, constraints>
Authoritative docs: docs/project-structure.md; docs/diagrams/... or docs/architecture.md; docs/README.md
Steps:
  1) ...
  2) ...
Do not: <paths, resources, or actions off limits>
STOP before: delete/overwrite/cloud apply/production impact — get explicit user confirmation
```

### Lab OS seed (this repo only, mode `lab-os-seed`)

If the workspace is `lab-os-lab` and the user confirms execution:

- `npm install`
- `npm run lab:init -- <target-or-default>`
- `npm run lab:verify`

Align targets with the user’s chosen folder. Do not assume every external project uses Node; **Lab OS layout is optional** and only for this mode in this seed repo.

## Output format (reporting)

- **Status:** pass / fail / blocked (waiting on user)
- **Phase:** A or B
- **Checks passed / failed** (see [checklist.md](checklist.md))
- **Next action:** concrete step

## Additional resources

- [checklist.md](checklist.md) — Phase A and Phase B checkpoints
- [examples.md](examples.md) — patterns and full examples
- [VERIFICATION.md](VERIFICATION.md) — prompt-level scenarios for acceptance checks
