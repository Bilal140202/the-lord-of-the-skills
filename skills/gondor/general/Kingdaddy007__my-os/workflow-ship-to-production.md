# WORKFLOW: SHIP TO PRODUCTION

**Version:** Gold v1.1 (Master Merge)
**Layer:** 8 — Execution Workflow
**Tier:** 2 — Loaded by task
**File:** workflows/workflow-ship-to-production.md
**Primary Mode:** Reviewer then DevOps/Infra then Builder
**Secondary Modes:** Security, Performance, Architect, Debugger
**Purpose:** The systematic pre-deployment and deployment sequence for shipping code to production safely — from release scope definition through staged rollout to post-deployment monitoring and stabilization. The final safety gate between staging and production.
**Loaded When:** Preparing to deploy to production, releasing a feature, performing a production deployment, planning a release, or executing a hotfix for a production incident.
**Inherits From:** execution-workflow.md (universal process)

***

## WHAT THIS WORKFLOW DOES

This workflow is the final safety gate between staging and production. It ensures code reaching users has been verified, the deployment process is followed, and post-deployment monitoring catches issues before users do.

Without this workflow, deployments happen with unchecked assumptions, missing verification steps, and no post-deployment monitoring — turning every deploy into a gamble.

***

## ACTIVATION

### Use When

- "Deploy to production"
- "Ship this feature"
- "Release [feature or version]"
- "Is this ready to deploy?"
- "What is the release plan?"
- "What should we check before deploy?"
- "What is the rollback plan?"
- Planning a production release
- Hotfix deployment for a production incident

### Do NOT Use When

- Deploying to staging — automatic on merge per `infra-context.md`
- Building features → use `workflow-build-feature.md`
- Debugging a production issue with no release pending → use `workflow-debug-issue.md`
- Designing architecture only
- Implementing unfinished features

This workflow assumes something is close enough to release that readiness must be judged. Do not start this workflow if the feature is not yet functionally complete.

***

## REQUIRED FILES

### Skills — Always Load

| Priority | Skill | Why |
| :--- | :--- | :--- |
| Primary | `skill-devops-infra` | Deployment process, monitoring, rollback |
| Secondary | `skill-review-audit` | Final quality check before release |
| Secondary | `skill-security` | Security verification before release |
| Secondary | `skill-testing` | Verification completeness assessment |

### Skills — Load When Relevant

| Condition | Skill | Why IT Matters |
| :--- | :--- | :--- |
| Test gaps need addressing before deploy | `skill-testing` (deep load) | Ensuring coverage |
| Performance risk in the release | `skill-performance` | Latency safety |
| Unresolved risk remains after review | `skill-debugging` | Stability |
| API contract changes | `skill-api-design` | Consumer safety |
| Database migration or data risk | `skill-database` | Data integrity |

### Contexts — Always Load

- `infra-context.md`
- `stack-context.md`
- `architecture-context.md`
- `testing-standards.md`
- `security-baselines.md`
- `business-priorities.md`

### Contexts — Load When Relevant

| Condition | Context |
| :--- | :--- |
| API or contract changes | `api-conventions.md` |
| Database migrations | `database-context.md` |
| Domain or business rule changes | `domain-rules.md` |

***

## REQUIRED INPUTS

At minimum, Anti-Gravity should have or establish before proceeding:

1. A defined release candidate or change set.
2. A clear understanding of what is changing.
3. Verification evidence from prior testing and review.
4. Impact and blast-radius assessment.
5. Known compatibility, migration, or data risks.
6. Known rollback or mitigation options.

### If inputs are incomplete (Ship to Production)

Do NOT default to release optimism. Instead:

1. State what is still unknown.
2. Identify whether the unknown affects release safety materially.
3. Reduce scope or strengthen rollout caution where certainty is weak.
4. Ask clarification only when missing information changes the go/no-go judgment materially.

***

## RELEASE RISK CLASSIFICATION

Before choosing rollout strategy, classify the release:

| Risk Level | Signals | Rollout Posture |
| :--- | :--- | :--- |
| Low | Additive change, no schema change, no auth change, easy rollback | Direct release with standard monitoring |
| Moderate | New behavior, config change, limited blast radius | Staged rollout or feature flag, extended monitoring |
| High | Auth change, schema migration, payment logic, API contract change, broad blast radius | Canary or feature-flag, second engineer on call, extended monitoring, rollback rehearsal |
| Critical | Data integrity risk, irreversible change, broad system-sensitive path | Expand-contract migration, blue-green or shadow, formal approval required |

***

## EXECUTION SEQUENCE

***

### STEP 1 — DEFINE THE RELEASE CANDIDATE

**Mode:** Reviewer
**Goal:** Know exactly what is being shipped. If the release scope is fuzzy, tighten it before planning rollout.

#### Actions (Define Release Candidate)

- Identify the specific feature, fix, configuration, migration, or contract change being released.
- Define what user or system behavior should change after release.
- Separate the release candidate from unrelated pending changes.
- Identify whether the release is additive, behavioral, breaking, or partially reversible.
- Identify whether the change includes:
  - Schema changes or migrations.
  - New or changed API contracts.
  - Auth or permission changes.
  - Infrastructure changes.
  - Feature flags.
  - Background job or async changes.
  - Configuration changes.

#### Output (Define Release Candidate)

```markdown
Release candidate: [what is shipping]
Expected production change: [what changes for users or the system]
Change type: [additive / behavioral / breaking / migration]
Risk classification: [low / moderate / high / critical]
Included surfaces: [list — schema, auth, API, infra, flags, etc]
```

***

### STEP 2 — ASSESS IMPACT AND BLAST RADIUS

**Mode:** Reviewer
**Goal:** Understand how much can go wrong if the release is wrong. Do not use the same rollout posture for low-risk and high-risk changes.

#### Actions (Assess Impact)

- Identify affected users, services, and critical paths.
- Identify whether the change touches authentication, payments, data integrity, APIs, migrations, or high-volume paths.
- Identify whether the release is global, phased, scoped to an environment, or tenant-scoped.
- Estimate how quickly bad effects would appear and how wide they would spread.
- Identify whether effects are reversible or could cause persistent data damage.

#### Output (Assess Impact)

```markdown
Affected surface: [list]
Blast radius: [narrow / moderate / broad / critical]
High-risk areas: [list]
Time to impact if wrong: [immediate / minutes / hours]
Reversibility: [fully reversible / partially / irreversible]
```

***

### STEP 3 — VERIFY PRE-RELEASE READINESS

**Mode:** Reviewer
**Goal:** Confirm the release candidate has enough pre-release confidence to justify production promotion.

#### Code Verification (Step 3)

- [ ] All features intended for this release are merged.
- [ ] No work-in-progress code included — no partial features, no TODO stubs.
- [ ] All PRs reviewed and approved.
- [ ] No known critical or high-severity bugs in release scope.
- [ ] Code review findings addressed, not just acknowledged.

#### CI/CD Pipeline Verification (Step 3)

- [ ] All CI checks pass on main branch:
  - [ ] Type checking.
  - [ ] Linting.
  - [ ] Unit and integration tests.
  - [ ] Build succeeds.
  - [ ] E2E tests pass.
- [ ] No flaky tests suppressed without a fix ticket.
- [ ] Build artifacts are identical to what was tested in staging.

#### Staging Verification (Step 3)

- [ ] Changes have been deployed to staging.
- [ ] Staging tested manually or via smoke tests.
- [ ] Staging uses same configuration as production except secrets.
- [ ] No errors observed in staging monitoring since deployment.
- [ ] Important flows verified in staging.

#### Database Verification (Step 3)

- [ ] Migrations tested against production-volume data.
- [ ] Migrations follow Expand-Contract pattern for breaking changes.
- [ ] Rollback path exists for each migration.
- [ ] No long-running table locks expected.
- [ ] Database backups are current.

#### Security Verification (Step 3)

- [ ] No new security vulnerabilities introduced.
- [ ] Auth changes reviewed by a second engineer.
- [ ] No secrets committed to repository.
- [ ] Environment variables verified for production values.
- [ ] Security headers unchanged or changes are intentional.

#### Readiness Summary (Step 3)

```markdown
Verified before release:

- [item]
- [item]

Open concerns (accepted or deferred):

- [item with reason]

```

#### Gate (Step 3 — Readiness Verification)

If confidence is weak and blast radius is high, the answer may be "not yet." Do not ship because the code is done. Ship when the change is sufficiently verified, observable, and recoverable for its real production risk.

***

### STEP 4 — CHOOSE THE ROLLOUT STRATEGY

**Mode:** DevOps/Infra
**Goal:** Select a delivery approach that matches the risk profile of the change. Avoid sophisticated rollout theater if monitoring and rollback posture cannot support it.

#### Rollout Options (Step 4)

| Strategy | When to Use | Rollback Speed |
| :--- | :--- | :--- |
| Direct release | Low-risk additive change, easy rollback | Instant — redeploy previous |
| Feature-flag controlled | Behavioral change, want gradual exposure | Instant — toggle flag |
| Staged rollout | Moderate risk, want incremental user exposure | Minutes |
| Canary | High risk, want small percentage first | Minutes |
| Blue-green or cutover | High risk, need instant full swap | Seconds |
| Migration-first then app | Schema or data change required before code | Depends on migration |

#### Decision (Step 4 — Rollout Strategy)

- Match rollout style to reversibility, observability, and blast radius.
- If rollback requires database reversal, the rollout must be more cautious.
- If monitoring cannot distinguish success from failure, the release is not ready to go live.

#### Output (Step 4 — Rollout Strategy)

```markdown
Rollout strategy: [choice]
Reason: [why this matches the risk profile]
Exposure order: [who sees it first, then next]
Checkpoint before full exposure: [yes / no — what triggers go/no-go]
```

***

### STEP 5 — DEFINE ROLLBACK AND MITIGATION PATHS

**Mode:** DevOps/Infra
**Goal:** Know what happens if the release is wrong. If rollback is weak or impossible, release caution must increase sharply.

#### Actions (Step 5 — Rollback & Mitigation)

- Define how to reverse or contain the change if production behavior degrades.
- Distinguish rollback from partial mitigation.
- Identify whether rollback is code-only, config-only, traffic-shift, flag-based, or blocked by data changes.
- Identify any one-way migration or compatibility hazards.
- Define when to stop rollout versus when to revert fully.
- Verify previous production deployment is still available.

#### Rollback Decision Framework (Step 5)

```markdown
Is the issue affecting users RIGHT NOW?
  YES → Is it a data integrity issue?
    YES → Rollback IMMEDIATELY. Assess data damage.
    NO  → Can it be fixed in under 15 minutes?
      YES → Fix forward. Deploy hotfix.
      NO  → Rollback. Fix in next deployment.
  NO → Monitor. Fix in next deployment if needed.
```

#### Output (Step 5 — Rollback & Mitigation)

```markdown
Primary rollback path: [how to revert]
Time to rollback: [estimated]
Rollback blockers: [what cannot be undone]
Partial mitigation if full rollback is unavailable: [approach]
Kill switch if feature-flagged: [flag name and how to toggle]
```

***

### STEP 6 — CONFIRM DEPLOYMENT ENVIRONMENT READINESS

**Mode:** DevOps/Infra
**Goal:** Confirm the deployment environment is healthy and the timing is appropriate before executing.

#### Timing (Step 6)

- [ ] Deployment during approved hours — check `infra-context.md`.
- [ ] If outside approved hours: is this a critical hotfix?
- [ ] On-call engineer is available and aware.
- [ ] No scheduled events making this a bad time — high traffic, demos, end-of-month billing.

#### Infrastructure Health (Step 6)

- [ ] Production systems healthy — check monitoring dashboards.
- [ ] Database load normal.
- [ ] Error rate at baseline.
- [ ] No ongoing incidents.
- [ ] External dependencies healthy — APIs, services, queues.

#### Communication (Step 6)

- [ ] Team notified of deployment.
- [ ] User-facing changes documented for support team if applicable.
- [ ] Product manager aware if it is a feature release.

***

### STEP 7 — EXECUTE THE DEPLOYMENT

**Mode:** DevOps/Infra
**Goal:** Deploy using the established process. Keep rollout disciplined. Do not add undocumented improvisation.

#### Actions (Step 7 — Execute Deployment)

1. Follow `infra-context.md` deployment procedure exactly.
2. Trigger the production deployment workflow.
3. Approve when prompted.
4. Wait for deployment to complete.

#### Immediate Post-Deploy Smoke Tests (Step 7)

- [ ] Deployment completed successfully.
- [ ] Application is responding — uptime monitor shows healthy.
- [ ] No immediate error spikes in error tracking.
- [ ] Application loads correctly.
- [ ] Authentication works.
- [ ] Core feature works — primary user action completes.
- [ ] Data loads correctly — no empty pages, no stale data.

#### Gate (Step 7 — Smoke Tests)

If smoke tests fail immediately after deployment, initiate rollback before investigating. Do not continue rollout on failed smoke tests.

***

### STEP 8 — POST-DEPLOYMENT MONITORING

**Mode:** DevOps/Infra
**Goal:** Watch for issues that only appear under real production conditions. Confirm the release stabilized before declaring success.

Stay alert and monitor actively:

- [ ] Error rate — any new errors? Compare to pre-deployment baseline.
- [ ] Response times — any degradation?
- [ ] Database performance — any slow query spikes?
- [ ] User-facing functionality — spot-check key flows.
- [ ] Background jobs processing normally if applicable.

#### First Hour — Background Watch (Step 8)

Check periodically:

- [ ] Error rate trend stable — not increasing.
- [ ] Performance metrics stable.
- [ ] No user-reported issues in support channels.
- [ ] Memory and resource usage normal.

#### Issue Response During Monitoring (Step 8)

| Objective | Action | Why It Matters |
| :--- | :--- | :--- |
| Error rate more than 2x baseline | Investigate immediately. Prepare rollback. | System instability |
| Core feature broken | Rollback immediately. Investigate after rollback. | User blocking |
| Performance degraded more than 50% | Investigate. Rollback if not quickly fixable. | Scalability risk |
| Minor cosmetic issue | Note it. Fix in next deployment. Do NOT rollback. | Low impact |
| Database migration issue | Assess data impact. If data corruption risk: rollback immediately. | Integrity safety |

#### Gate (Step 8 — Monitoring Stabilization)

Do not continue rollout just because the sequence says "next" if production signals say otherwise. Do not declare the release complete without honoring the observation window.

***

### STEP 9 — CONFIRM STABILIZATION AND DELIVER SUMMARY

**Mode:** Communicator
**Goal:** Close the release responsibly. Record what was shipped, what was observed, and what follow-up is needed.

#### Stabilization Confirmation (Step 9)

- Confirm the release stabilized within the expected observation window.
- Record what was verified in production.
- Note anomalies, residual risk, or follow-up cleanup needed.
- Identify whether additional regression guardrails or observability improvements are needed.
- Record lessons if the rollout exposed a process weakness.

#### Delivery Structure (Step 9 — Deployment Record)

```markdown

## Deployment Record

### Date and Time

[When the deployment occurred]

### What Was Deployed

[Features, fixes, changes included in this release]

### Deployment Type

[Regular release / Hotfix / Infrastructure change]

### Risk Classification

[Low / Moderate / High / Critical — and why]

### Pre-Deployment Checks

[All passed / Note any concerns that were accepted and why]

### Rollout Strategy Used

[Direct / Feature-flag / Staged / Canary / Blue-green]

### Post-Deployment Status

[Healthy / Issues detected — describe]

### Monitoring Observations

- Error rate: [normal / elevated — details]
- Performance: [normal / degraded — details]
- User reports: [none / describe]
- Background jobs: [normal / issues — details]

### Rollback Required?

[No / Yes — describe what happened]

### Action Items

[Follow-up work triggered by this deployment]

### Follow-Up Needed

[Observability gaps, regression tests, cleanup, post-mortem]
```

#### After Delivery (Step 9)

- [ ] Notify team that deployment is complete and healthy.
- [ ] If feature release: confirm with product manager.
- [ ] Update memory files if significant decisions were made.
- [ ] If deployment surfaced issues: create follow-up tickets.

***

## HOTFIX VARIANT

When deploying a hotfix for an active P1 or P2 production incident:

### Modified Process (Hotfix)

1. **Expedited review:** One reviewer — not the author — must approve.
2. **Skip staging soak time:** Deploy to staging, quick smoke test, promote to production.
3. **Narrowest possible fix:** Fix ONLY the incident — no other changes.
4. **Extended monitoring:** Active watch for 30 minutes post-deployment.
5. **Follow-up required:** Full post-mortem within 48 hours.
6. **Regression test required:** Add test that catches this incident, deployed in next regular release.

### Hotfix Rules

- Still requires: CI passing, one review, staging verification even if quick.
- Does NOT require: full pre-deployment checklist, business-hours restriction.
- MUST be followed by: root cause analysis and permanent fix if the hotfix is temporary.

***

## CHECKPOINTS AND QUALITY GATES

| Gate | Condition | Action |
| :--- | :--- | :--- |
| Gate 1 — Release scope unclear | Cannot say exactly what is being shipped | Not ready — tighten scope first |
| Gate 2 — Readiness evidence too weak for blast radius | Verification incomplete, important paths at risk | Strengthen evidence or reduce exposure |
| Gate 3 — Rollback path weak or unknown | Rollback is unclear, untested, or blocked by data | Release strategy must become more conservative |
| Gate 4 — Monitoring cannot distinguish success from failure | Cannot tell if the release is healthy | Not ready to go live — improve observability first |
| Gate 5 — Production signals disagree with rollout | Post-release evidence is bad | Stop or reverse — do not rationalize warning signs |
| Gate 6 — Smoke tests fail immediately | Core paths broken right after deployment | Rollback before investigating |

***

## QUALITY GATE CHECKLIST

Before calling a production deployment complete:

- [ ] Release scope defined — exactly what is shipping.
- [ ] Risk classified and rollout strategy matched to risk.
- [ ] All CI checks pass on main.
- [ ] Staging tested and stable.
- [ ] Database migrations verified if applicable.
- [ ] Security verification complete.
- [ ] Deployment timing appropriate or exception justified.
- [ ] Infrastructure healthy before deployment.
- [ ] Rollback path confirmed and documented.
- [ ] Team notified.
- [ ] Deployment completed successfully.
- [ ] Smoke tests pass on production.
- [ ] 15-minute active monitoring complete — no issues.
- [ ] 1-hour background monitoring complete — stable.
- [ ] Deployment record documented.
- [ ] Follow-up tickets created for any issues surfaced.

***

## WORKFLOW ANTI-PATTERNS

### Deploy-and-Pray

**What it looks like:** Running the release mechanically with little explicit blast-radius thinking, weak monitoring, and no serious rollback posture.
**Why it is harmful:** The team discovers risk only after users absorb it.
**What to do instead:** Define rollout, rollback, and production verification before release execution begins.

### One-Size-Fits-All Rollout

**What it looks like:** Using the same release strategy for tiny low-risk changes and high-risk system-sensitive changes.
**Why it is harmful:** Release posture becomes disconnected from actual danger.
**What to do instead:** Match rollout style to risk, reversibility, and observability using the risk classification table.

### Rollback Fantasy

**What it looks like:** Claiming a rollback exists when it is incomplete, untested, blocked by data changes, or not realistically fast enough.
**Why it is harmful:** False recovery confidence increases production risk.
**What to do instead:** State the rollback path honestly, including what it cannot undo.

### Release Completion Illusion

**What it looks like:** Treating deployment success as production success without an observation window or signal review.
**Why it is harmful:** Problems surface after the team has mentally moved on.
**What to do instead:** Define and honor stabilization checks before calling the release complete.

### Shipping on Code Completion Alone

**What it looks like:** Declaring readiness based only on "the feature is done" without checking verification, staging, security, and rollback.
**Why it is harmful:** Code done and safe to ship are not the same thing.
**What to do instead:** Complete the full pre-deployment checklist at Step 3 before proceeding.

***

## FAILURE MODES AND ESCALATION PATHS

| Failure Mode | What It Looks Like | Escalation |
| :--- | :--- | :--- |
| Change is not actually release-ready | Feature incomplete, tests failing, review outstanding | Return to feature build, review, or testing work |
| Release touches irreversible or data-sensitive changes | Migration cannot be rolled back, data may be affected | Strengthen rollback and migration reasoning with database context |
| Main problem is observability weakness | Cannot monitor the release meaningfully | Pause and improve visibility before pretending control exists |
| Release is actually multiple changes with different risk profiles | One rollout strategy cannot cover the whole changeset | Split the release by risk profile |
| Rollout problem is really a product or communication problem | Staged exposure requires expectation management | Bring in product reasoning for user communication |

***

## FINAL RULE

Do not ship because the code is done.

Ship when the change is sufficiently verified, observable, and recoverable for its real production risk. Every deploy is a bet — this workflow exists to make that bet as informed and reversible as possible.
