# WORKFLOW: SECURITY AUDIT (FULL SOURCE)

**Version:** Gold v1.1 (Master Merge)
**Layer:** 8 — Execution Workflow
**Tier:** 2 — Loaded by task
**File:** workflows/workflow-security-audit-SOURCE.md
**Primary Mode:** Security
**Secondary Modes:** Reviewer, Architect, Debugger
**Purpose:** The systematic sequence for evaluating the security posture of code, features, or system components — identifying vulnerabilities, assessing risk, and recommending mitigations. Uses the STRIDE framework across trust boundaries to systematically identify vulnerabilities rather than relying on ad-hoc assessment.
**Loaded When:** Reviewing auth changes, evaluating security of a feature, assessing exposure after a dependency update, conducting periodic security review, preparing for compliance, or after a security incident.
**Inherits From:** execution-workflow.md (universal process)

---

## WHAT THIS WORKFLOW DOES

This workflow applies structured threat analysis to code and architecture. It uses the STRIDE framework across trust boundaries to systematically identify vulnerabilities.

Without this workflow, security review is either skipped entirely, done superficially with "I do not see any obvious issues," or focused narrowly on one attack vector while missing others.

---

## ACTIVATION

### Use When

- "Is this secure?"
- "Review the security of [feature]"
- "Audit this code for vulnerabilities"
- "Security audit"
- "Review auth / roles / token handling"
- "What are the security risks here?"
- "Should this be approved from a security perspective?"
- Changes to auth, permissions, or session handling
- Adding or updating third-party dependencies
- Preparing for enterprise security requirements
- After a security incident — what else might be vulnerable?
- Periodic security review — quarterly recommended

### Do NOT Use When

- General code review with security as one dimension only → use `workflow-review-code.md` which includes a security step
- Performance optimization → use `workflow-optimize-performance.md`
- Building new features → use `workflow-build-feature.md` which includes a security step
- Debugging a normal non-security bug → use `workflow-debug-issue.md`
- Active security incident already confirmed → switch to incident response and containment, not pre-release audit logic

---

## REQUIRED FILES

### Skills — Always Load

| Priority | Skill | Why |
| :--- | :--- | :--- |
| Primary | `skill-security` | STRIDE framework, trust boundaries, threat modeling |
| Secondary | `skill-review-audit` | Code quality evaluation methodology |

### Skills — Load When Relevant

| Condition | Skill |
| :--- | :--- |
| Auditing system-level security architecture | `skill-architecture` |
| Auditing API security | `skill-api-design` |
| Auditing data layer security | `skill-database` |
| Reviewing surrounding infra exposure | `skill-devops-infra` |

### Contexts — Always Load

- `security-baselines.md`
- `architecture-context.md`
- `stack-context.md`
- `domain-rules.md`

### Contexts — Load When Relevant

| Condition | Context |
| :--- | :--- |
| Auditing API endpoints | `api-conventions.md` |
| Auditing data layer | `database-context.md` |
| Auditing infrastructure exposure | `infra-context.md` |
| Business context affects risk level | `business-priorities.md` |

---

## REQUIRED INPUTS

At minimum, Anti-Gravity should have or establish before proceeding:

- the system surface, change, API, flow, or implementation target
- a stated or inferable objective for that target
- data sensitivity and trust-boundary information
- expected user roles or access model

### If inputs are incomplete

Do NOT default to broad fear-based criticism. Instead:

1. Define the likely trust boundary and risk surface
1. State assumptions explicitly
1. Identify where missing context limits certainty
1. Ask clarification only when missing information materially changes severity or remediation judgment

---

## AUDIT DEPTH CALIBRATION

| Trigger | Audit Depth |
| :--- | :--- |
| Auth or permission code change | Deep — full STRIDE analysis |
| New API endpoint | Medium — input validation, auth, data exposure |
| Dependency update | Focused — vulnerability check and permission review |
| Periodic review | Broad — surface-level across full application |
| Post-incident | Deep — focused on incident category and adjacent risks |
| Preparing for enterprise or compliance | Deep — full STRIDE plus baseline compliance |

---

## EXECUTION SEQUENCE

---

### STEP 1 — DEFINE THE AUDIT SCOPE

**Mode:** Security
**Goal:** Clearly define what is being audited, at what depth, and why it exists.

#### Actions (Step 1)

1. **Identify the audit level:**
   - Feature-level audit: one feature's code
   - Component-level audit: auth system, API layer, database
   - System-level audit: full application security posture
   - Change-level audit: security impact of a specific change

1. **Identify sensitive assets:**
   - What sensitive data flows through this scope?
   - What user actions are possible within this scope?
   - What external systems connect to this scope?
   - Reference `security-baselines.md` data classification

1. **Identify the primary function and actors:**
   - What behavior is this surface supposed to enable?
   - Who interacts with it and under what authority assumptions?
   - Which actors apply:
     - Unauthenticated external attacker
     - Authenticated user trying to access other users' data
     - Authenticated user trying to escalate privileges
     - Malicious or compromised third-party dependency
     - Insider with excessive access

1. **Set the audit depth** using the calibration table above

#### Output (Step 1)

```text
Audit target: [what is being reviewed]
Primary function: [what it does]
Expected actors: [who can interact with it]
Audit depth: [deep / medium / focused / broad]
Assets at risk: [list]
Threat actors in scope: [list]
```

#### Gate (Step 1)

If the audit surface is still vague, risk findings will likely become generic and less useful. Tighten scope before proceeding.

---

### STEP 2 — MAP TRUST BOUNDARIES

**Mode:** Security
**Goal:** Identify where data crosses security boundaries. A trust boundary exists wherever data moves between zones of different trust levels.

#### Trust Zone Diagram (Step 2)

```text
        UNTRUSTED                           TRUSTED
┌──────────────────┐              ┌──────────────────┐
│  Browser /       │──BOUNDARY───▶│  Server          │
│  Client Code     │      ▲       │  (Server Actions │
└──────────────────┘      │       │  / API Routes)   │
                          │       └────────┬─────────┘
┌──────────────────┐      │                │
│  External APIs   │──────┘       ┌────────▼─────────┐
│  (Webhooks,      │              │  Database        │
│  Third Parties)  │              │  (PostgreSQL)    │
└──────────────────┘              └──────────────────┘
                                  ┌──────────────────┐
                                  │  External        │
                                  │  Services        │
                                  │  (S3, Email)     │
                                  └──────────────────┘
```

#### Boundary Mapping (Step 2)

For Each Trust Boundary, Document:

- What data crosses this boundary?
- In which direction?
- Is the data validated at the crossing point?
- Is the data encrypted in transit?
- Who or what is on each side?
- What protections are expected at this boundary?
- Where do users cross from less-trusted to more-trusted zones?

#### Also Map

- Client → Server boundary
- Service → Service boundary
- User → Admin boundary
- Tenant → Tenant boundary
- External provider → Internal system boundary

#### Output (Step 2)

```text
Trust boundaries:

- [boundary 1]: [data flow, direction, current protection]
- [boundary 2]: [data flow, direction, current protection]

Sensitive assets / operations:

- [list]

```

#### Gate (Step 2)

If nothing important is identified as sensitive, or trust boundaries remain implicit, the audit is under-scoped.

---

### STEP 3 — APPLY STRIDE ANALYSIS

**Mode:** Security
**Goal:** Systematically check for each category of threat across every trust boundary identified in Step 2.

#### STRIDE Framework (Step 3)

For each trust boundary, evaluate all six categories:

| Threat | Question | What to Check |
| :--- | :--- | :--- |
| **S — Spoofing** | Can an attacker pretend to be someone they are not? | Auth implementation, session management, token validation, OAuth state parameter |
| **T — Tampering** | Can an attacker modify data in transit or at rest? | Input validation, parameterized queries, HTTPS enforcement, CSRF protection, data integrity checks |
| **R — Repudiation** | Can an attacker deny performing an action? | Audit logging, transaction logs, non-repudiation measures |
| **I — Information Disclosure** | Can an attacker access data they should not see? | Error messages exposing internals, verbose PII logging, overly broad API responses, broken access control |
| **D — Denial of Service** | Can an attacker make the system unavailable? | Rate limiting, resource limits, payload size limits, connection pool exhaustion |
| **E — Elevation of Privilege** | Can an attacker gain permissions they should not have? | RBAC enforcement, parameter manipulation, IDOR vulnerabilities, admin endpoint protection |

#### For Each Finding, Document

```text
Threat: [STRIDE category]
Boundary: [which trust boundary]
Description: [what the vulnerability is]
Attack Scenario: [how an attacker would exploit this]
Current Mitigation: [what protection exists, if any]
Severity: [Critical / High / Medium / Low]
Recommendation: [what to do about it]
```

#### Abuse and Misuse Path Analysis (Step 3)

In addition to STRIDE, ask:

- How might an attacker, careless client, or buggy integration misuse this surface?
- What opportunities exist for privilege escalation, bypass, leakage, spoofing, unsafe defaults, over-broad access, or weak validation?
- Consider both direct and indirect exposure routes
- Consider accidental misuse paths as well as deliberate abuse

#### Gate (Step 3)

If the audit only considers happy-path use, it is not yet a real security audit. All six STRIDE categories must be addressed per boundary.

---

### STEP 4 — CHECK AGAINST SECURITY BASELINES

**Mode:** Security
**Goal:** Verify compliance with project security standards defined in `security-baselines.md`.

#### Authentication (Step 4)

- [ ] Auth implementation matches documented approach
- [ ] Session management follows documented rules
- [ ] Rate limiting on auth endpoints is implemented
- [ ] Password handling follows documented policy
- [ ] Session invalidation triggers work correctly

#### Authorization (Step 4)

- [ ] Every protected action checks both authentication AND authorization
- [ ] Role permissions match the documented matrix
- [ ] Resource-level access control is enforced — users cannot access other users' resources
- [ ] Authorization checked server-side, not just client-side
- [ ] Privileged actions are appropriately constrained
- [ ] No authorization bypass paths exist

#### Input Validation (Step 4)

- [ ] All user input validated server-side
- [ ] File uploads validated for type, size, and content
- [ ] SQL injection prevented via parameterized queries
- [ ] XSS prevented via output escaping and CSP headers
- [ ] No trust placed in client-side validation alone

#### Data and Secret Handling (Step 4)

- [ ] Sensitive data not logged — passwords, tokens, PII
- [ ] No secrets in code or git history
- [ ] Secrets in environment variables, properly scoped
- [ ] API responses do not leak internal data
- [ ] Error messages do not expose stack traces or internal details
- [ ] Secret rotation policy followed
- [ ] Data minimization preserved where relevant

#### HTTP Security (Step 4)

- [ ] CSP header set and appropriate
- [ ] X-Frame-Options set
- [ ] X-Content-Type-Options set
- [ ] CORS policy correct — no wildcard in production
- [ ] HTTPS enforced

#### Dependencies (Step 4)

- [ ] No known critical or high vulnerabilities
- [ ] Lock file committed and reviewed
- [ ] No unnecessary dependencies with excessive permissions
- [ ] Licenses acceptable

#### Operational Exposure (Step 4)

- [ ] Logs do not over-expose sensitive information
- [ ] Admin tooling access is appropriately restricted
- [ ] Internal-only assumptions are enforced, not just conventional
- [ ] Rollback and release paths do not create new exposure

---

### STEP 5 — CLASSIFY AND PRIORITIZE FINDINGS

**Mode:** Security
**Goal:** Turn raw concerns into prioritized, actionable findings. Severity must reflect real risk, not anxiety or dramatic language.

#### Severity Classification (Step 5)

| Severity | Definition | Examples | Response Time |
| :--- | :--- | :--- | :--- |
| 🔴 Critical | Active exploitable vulnerability. Data breach or full compromise possible. | SQL injection, auth bypass, exposed secrets, unprotected admin endpoints | Fix immediately. Block deployment. |
| 🟠 High | Significant vulnerability requiring specific conditions to exploit. | Missing authorization check, IDOR vulnerability, insufficient rate limiting on sensitive endpoints | Fix within 48 hours |
| 🟡 Medium | Vulnerability with limited impact or requiring unlikely conditions. | Overly verbose error messages, missing security headers, weak defaults | Fix within one sprint |
| 🟢 Low | Minor issue or defense-in-depth improvement. | Missing Referrer-Policy header, suboptimal CORS, minor hardening | Backlog — fix when convenient |
| 💬 Informational | Useful note or caution without a strong defect claim yet | Observation, question, or emerging pattern to watch | No action required now |

#### Confidence Calibration (Step 5)

- Distinguish confirmed weakness from plausible concern from low-confidence suspicion
- Do not treat every issue as equally urgent
- Align severity with blast radius, exploitability, and asset sensitivity

#### Approval Decision (Step 5)

- **Acceptable as-is** — no blocking issues found
- **Acceptable with caveats** — minor issues noted, not blocking
- **Requires remediation before approval** — must-fix issues identified
- **Blocked** — critical issues that cannot be deferred

State blocking versus advisory clearly. Do not leave the owner guessing which findings are truly blocking.

---

### STEP 6 — DELIVER THE SECURITY AUDIT REPORT

**Mode:** Communicator
**Goal:** Communicate the audit so the next action is obvious.

#### Report Structure (Step 6)

```markdown

## Security Audit Report

### Scope

[What was audited, at what depth, and why]

### Summary

- Critical findings: [count]
- High findings: [count]
- Medium findings: [count]
- Low findings: [count]
- Approval status: [acceptable / caveats / remediate / blocked]

---

### Trust Boundary Map

[Diagram or description of trust boundaries analyzed]

---

### Findings by Severity

#### 🔴 Critical

[Each finding: description, attack scenario, evidence, recommendation]

#### 🟠 High

[Each finding]

#### 🟡 Medium

[Each finding]

#### 🟢 Low / 💬 Informational

[Each finding]

---

### Positive Observations

[Security measures that are working well — acknowledge what is right]

---

### Gaps Relative to Security Baselines

[Areas where current implementation does not meet security-baselines.md expectations]

---

### Remediation Plan (Prioritized)

1. [Most urgent action]
2. [Second most urgent]
3. [...]

### Blocking Issues for Approval

[State exactly what must change before this is acceptable]

---

### Follow-Up

[When should the next audit occur?]
[What areas need deeper investigation?]
[What monitoring or observability should be added?]
[What residual risk remains after mitigation?]
```

---

## COMMON AUDIT CHECKLISTS

### Auth Change Audit

- [ ] Session handling unchanged or improved
- [ ] Token validation covers all protected routes
- [ ] Role checks match permission matrix
- [ ] No new auth bypass paths introduced
- [ ] Session invalidation triggers still work
- [ ] OAuth state parameter validated if applicable

### New Endpoint Audit

- [ ] Authentication required unless explicitly and intentionally public
- [ ] Authorization checked for role and resource ownership
- [ ] All input validated server-side
- [ ] Error responses do not leak internal details
- [ ] Rate limiting applied if applicable
- [ ] Response does not over-expose data

### Dependency Update Audit

- [ ] No known vulnerabilities in new version
- [ ] Permissions or access have not expanded
- [ ] Breaking changes do not affect security features
- [ ] License is still acceptable

---

## CHECKPOINTS AND QUALITY GATES

| Gate | Condition | Action |
| :--- | :--- | :--- |
| Gate 1 — Scope vague | Cannot state what is being protected or from whom | Clarify boundary before proceeding |
| Gate 2 — Generic language | Findings are broad security words without concrete boundary or exploit reasoning | Tighten scope and ground findings in real paths |
| Gate 3 — Auth/authz under-specified | Protected behavior exists but authority logic is not explicit | Audit is incomplete — deepen Step 4 |
| Gate 4 — High-sensitivity surface reviewed casually | High-sensitivity behavior treated with shallow scrutiny | Raise depth and severity discipline |
| Gate 5 — Findings not prioritized | Blocking versus advisory still unclear | Classify before delivering |
| Gate 6 — Happy-path-only analysis | Abuse paths not considered | Return to Step 3 and apply STRIDE properly |

---

## QUALITY GATE CHECKLIST

Before delivering a security audit:

- [ ] Audit scope clearly defined with depth level
- [ ] Sensitive assets and threat actors identified
- [ ] Trust boundaries mapped with data flow documentation
- [ ] STRIDE analysis applied to each trust boundary
- [ ] Abuse and misuse paths considered beyond happy path
- [ ] Auth/authz logic inspected at server-side enforcement point
- [ ] Input handling, data exposure, and secret handling reviewed
- [ ] Operational and deployment exposure reviewed
- [ ] Baseline compliance checked against `security-baselines.md`
- [ ] Findings classified by severity with confidence noted
- [ ] Each finding includes attack scenario and concrete recommendation
- [ ] Positive observations acknowledged — not just problems
- [ ] Approval status stated with blocking conditions explicit
- [ ] Prioritized remediation plan provided
- [ ] Follow-up timeline and monitoring recommendations included

---

## WORKFLOW ANTI-PATTERNS

| Anti-Pattern | Why It Is Harmful | How This Workflow Prevents It |
| :--- | :--- | :--- |
| Generic Security Hand-Waving | Creates noise without useful action | Ground findings in concrete risk paths and affected assets |
| Client-Side Trust Illusion | The real authority boundary remains weak | Verify authorization where the system actually enforces power — at the server-side boundary |
| Auth Without Authz | Authenticated users can still access or modify resources they should not be able to reach | Always inspect both authentication AND authorization separately |
| All-Findings-Are-Critical | Teams lose prioritization clarity and stop trusting the audit output | Classify findings by real exploitability, blast radius, and sensitivity |
| Audit Without Approval Conditions | The next action becomes ambiguous for the owner | State remediation expectations and approval status explicitly |
| Happy-Path-Only Security Review | Real attacks do not follow intended use paths | Apply STRIDE to all trust boundaries including abuse and misuse scenarios |

---

## FAILURE MODES AND ESCALATION PATHS

| Failure Mode | What It Looks Like | Escalation |
| :--- | :--- | :--- |
| Ambiguous Surface | No clear boundary or function | Pause and clarify before continuing |
| Architectural Flaw | Weakness comes from deeper boundary or ownership design flaw | Escalate to architecture planning |
| Unset Stack Controls | Cannot judge real protection without knowing the stack | Re-anchor on baselines, note what is still open |
| Contract Collision | Mixes security with unresolved API or data-model questions | Bring in API or database reasoning first |
| Incident Active | This is not a pre-release audit anymore | Switch to incident response and containment logic |

---

## FINAL RULE

Audit the boundary, not just the code.

Most meaningful security failures happen where trust is assumed instead of enforced — at the edges where data crosses from one zone to another.

---

## VERSION HISTORY

| Version | Date | Changes |
| :--- | :--- | :--- |
| Gold v1.1 | Initial | Established the systematic sequence for security auditing and threat modeling |
