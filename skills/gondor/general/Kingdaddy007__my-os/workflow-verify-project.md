---
description: The systematic sequence for running automated project verification checks — security scan, code quality, accessibility, and performance profiling before deployment.
---

# WORKFLOW: VERIFY PROJECT (MASTER)

> **[CONTEXT AMNESIA FAILSAFE]**
> YOU MUST USE TOOL CALLS TO READ THE FULL SOURCE FILE AND THE REQUIRED SKILLS/CONTEXTS BEFORE EXECUTING THIS.
> Verify silently in your internal reasoning that you have done this.

> **IMPORTANT [REQUIRED]:** This workflow runs the Antigravity Gold verification scripts against the current project. The scripts are located in `{{GLOBAL_CONFIG_URI}}\scripts\`.

## WHAT THIS WORKFLOW DOES

Runs automated quality checks against the project to catch security issues, code quality problems, accessibility violations, and performance concerns BEFORE deployment. This adds executable teeth to our rubric-based quality bar.

---

## WHEN TO USE

- Before any deployment or push to production
- After completing a major feature build
- During Phase 6 (Verify) of the execution workflow
- When the user says "verify", "check", or "is this ready to ship?"
- Anti-Gravity should SUGGEST (not force) running this before deployments

## WHEN NOT TO USE

- During active development (too noisy — wait for a natural checkpoint)
- For tiny changes (single line fix, comment update)

---

## EXECUTION

### Quick Check (Most Common)

```bash
python {{GLOBAL_CONFIG_URI}}\scripts\verify.py <project_path>
```

This runs all 4 checks in priority order:

1. **P0: Security Scan** — Hardcoded secrets, dangerous code, env exposure
2. **P1: Code Quality** — Console.log, empty catch, unhandled fetch
3. **P2: Accessibility** — WCAG basics on HTML files
4. **P3: Performance** — File sizes, bundle analysis

### Targeted Check

```bash
python {{GLOBAL_CONFIG_URI}}\scripts\verify.py <project_path> --only security
python {{GLOBAL_CONFIG_URI}}\scripts\verify.py <project_path> --only quality
python {{GLOBAL_CONFIG_URI}}\scripts\verify.py <project_path> --only accessibility
python {{GLOBAL_CONFIG_URI}}\scripts\verify.py <project_path> --only performance
```

### Skip Specific Checks

```bash
python {{GLOBAL_CONFIG_URI}}\scripts\verify.py <project_path> --skip performance
```

---

## INTERPRETING RESULTS

| Exit Code | Meaning | Action |
| :--- | :--- | :--- |
| 0 | All checks passed | Ready to deploy |
| 1 | Issues found | Review output, fix critical/high issues before deployment |

### Severity Levels

| Severity | Meaning | Must Fix Before Deploy? |
| :--- | :--- | :--- |
| CRITICAL | Security vulnerability or data exposure | ✅ YES — stop everything |
| HIGH | Significant issue that could cause problems | ✅ YES |
| MEDIUM | Quality issue worth addressing | ⚠️ Recommended |
| LOW | Minor issue or style concern | ❌ Optional |
| INFO | Observation, no action needed | ❌ No |

---

## QUALITY GATES

- **G1 (Security):** CRITICAL security findings = deployment blocked
- **G2 (Quality):** More than 10 MEDIUM code quality issues = review before deployment
- **G3 (Accessibility):** More than 5 HIGH accessibility issues = fix before deployment
