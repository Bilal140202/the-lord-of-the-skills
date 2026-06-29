---
created: 2026-04-17
updated: 2026-04-17
---

# AGENTS — Terraform Reference Lab

## Read order

1. [README.md](README.md) — scaffold story, maturity, tooling, workflows  
2. [lab.yaml](lab.yaml) — `labId`, `maturityStage`, governance, `requiredChecks`  
3. [.lab/reality/IMPLEMENTATION_MAP.md](.lab/reality/IMPLEMENTATION_MAP.md) — path index for code ↔ docs  
4. The environment you are changing — `environments/dev` or `environments/prod` — and the [`modules/*`](modules/) it calls  

## Lab OS contract files (required for `validate`)

These five paths are enforced by Lab OS `validate-lab.mjs`; they anchor the pillars and link to deeper docs:

| Pillar | File |
| --- | --- |
| intent | [.lab/intent/ARCHITECTURE_TARGET.md](.lab/intent/ARCHITECTURE_TARGET.md) |
| reality | [.lab/reality/IMPLEMENTATION_MAP.md](.lab/reality/IMPLEMENTATION_MAP.md) |
| delta | [.lab/delta/GAP_MAP.md](.lab/delta/GAP_MAP.md) |
| behavior | [.lab/behavior/GOVERNANCE_POLICY.md](.lab/behavior/GOVERNANCE_POLICY.md) |
| evidence | [.lab/evidence/READINESS_CHECKS.md](.lab/evidence/READINESS_CHECKS.md) |

Do not delete or rename these; add detail in sibling files (`PURPOSE.md`, `DESIGN_DECISIONS.md`, etc.) instead. In this repo they live under **`.lab/`**; Lab OS also supports a root **`lab/`** tree but **not both at once**.

## Rules of thumb

- Prefer **module boundaries** over growing environment `main.tf` without bound.  
- **Never** commit real secrets. For DB password use `TF_VAR_db_password`, CI secrets, or Secrets Manager—not long-lived values in `terraform.tfvars` for production.  
- After Terraform edits: `terraform fmt` and `terraform validate` (or [pre-commit](.pre-commit-config.yaml)).  
- **Apply** to shared or production accounts only with explicit human approval (`lab.yaml` governance).  
- **`queue_url`:** messaging module output is surfaced at environment level ([`environments/dev/aws/outputs.tf`](environments/dev/aws/outputs.tf)); wire into Kubernetes workloads per [.lab/behavior/FAILOVER_POLICY.md](.lab/behavior/FAILOVER_POLICY.md).  
- **`GAP_MAP.md`:** avoid the substring `high` in severity prose when possible—the Lab OS `promote-stage` script treats any `high` in that file as a pilot promotion blocker (false positives on words like “highlight”).

## Lab OS toolkit (parent repo)

From **lab-os-lab** (adjust `--target` if you moved this folder):

```bash
npm run validate -- --target .tmp/terraform-reference-lab
```

Avoid `npm run lab:init -- .tmp/terraform-reference-lab` unless you want **automatic promotion to `poc`**. To bump stage intentionally:

```bash
npm run promote -- --target .tmp/terraform-reference-lab --to poc
```

(Only after evidence and `GAP_MAP.md` are clean for that stage.)

## LocalStack

Default `use_localstack = true` in [`environments/dev/aws/terraform.tfvars`](environments/dev/aws/terraform.tfvars) (and sibling `terraform.tfvars` per cloud). Start [tests/localstack/docker-compose.yml](tests/localstack/docker-compose.yml). EKS/RDS behavior may diverge from AWS; see [.lab/delta/GAP_MAP.md](.lab/delta/GAP_MAP.md) and [.lab/reality/ARCHITECTURE.md](.lab/reality/ARCHITECTURE.md).

## Terratest

[tests/terratest/](tests/terratest/) is stubbed with `t.Skip` at `experiment`. Align unskipping with [.lab/evidence/VALIDATION_MATRIX.md](.lab/evidence/VALIDATION_MATRIX.md).
