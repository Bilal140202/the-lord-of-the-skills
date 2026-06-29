# WORKFLOW: DEBUG ISSUE (FULL SOURCE)

**Version:** Gold v1.1 (Master Merge)
**Layer:** 8 — Execution Workflow
**Tier:** 2 — Loaded by task
**File:** workflows/workflow-debug-issue-SOURCE.md
**Primary Mode:** Debugger
**Secondary Modes:** Reviewer, Builder, Security, Testing
**Purpose:** The systematic sequence for diagnosing and fixing bugs — from symptom observation through root cause identification to verified fix with regression prevention. Prevents the most common debugging mistake: guessing at the cause and changing code before understanding the problem.
**Loaded When:** Something is broken, unexpected behavior is observed, error reports received, production incidents occur, regressions detected, or flaky behavior investigated.
**Inherits From:** execution-workflow.md (universal process)

---

## WHAT THIS WORKFLOW DOES

This workflow enforces evidence-based diagnosis, root cause analysis, and verified fixes with regression prevention.

Without this workflow, debugging degenerates into shotgun debugging — random changes, print statements everywhere, and symptom-masking fixes that create new bugs while leaving the real cause intact.

---

## ACTIVATION

### Use When

- "This is broken"
- "I am getting an error"
- "Why is this happening?"
- "This started failing"
- "We have a regression"
- "This test is flaky"
- "The service keeps timing out"
- "Users are seeing inconsistent behavior"
- Stack traces, error messages, or unexpected behavior
- Production incident response

### Do NOT Use When

- Code works but needs improvement → use `workflow-refactor-module.md`
- Code works but is slow → use `workflow-optimize-performance.md`
- Building new functionality → use `workflow-build-feature.md`
- Reviewing code for quality → use `workflow-review-code.md`
- Feature planning without a failure symptom
- Pure research or comparison questions

---

## REQUIRED FILES

### Skills — Always Load

| Priority | Skill | Why |
| :--- | :--- | :--- |
| Primary | `skill-debugging` | Systematic diagnosis methodology |
| Secondary | `skill-review-audit` | Code quality assessment around the fix |
| Secondary | `skill-testing` | Regression test for the fix |

### Skills — Load When Relevant

| Condition | Skill |
| :--- | :--- |
| Bug has security implications | `skill-security` |
| Bug is performance-related | `skill-performance` |
| Bug reveals structural debt | `skill-refactoring` |

### Contexts — Always Load

- `stack-context.md`
- `architecture-context.md`
- `domain-rules.md`

### Contexts — Load When Relevant

| Condition | Context |
| :--- | :--- |
| Data-related bug | `database-context.md` |
| Business logic bug | `domain-rules.md` |
| Deployment or infrastructure bug | `infra-context.md` |
| Auth or trust boundary involved | `security-baselines.md` |
| API contract suspected | `api-conventions.md` |

---

## REQUIRED INPUTS

At minimum, Anti-Gravity should have or establish before proceeding:

- a described symptom or observed failure
- expected versus actual behavior, even if incomplete
- enough surrounding context to identify the likely system area
- environment where the issue occurs
- urgency and severity classification

### Strongly preferred inputs

- reproduction steps or known triggering conditions
- logs, traces, metrics, screenshots, stack traces, or test output
- recent changes in code, config, infra, dependencies, or data
- impact information: who is affected and how broadly

### If inputs are incomplete

Do NOT jump straight to a fix. Instead:

1. Restate the symptom as precisely as possible
2. Separate the symptom from guessed causes
3. Gather the strongest available evidence before code changes
4. Ask clarification only if missing information would materially change the diagnosis path

---

## SEVERITY-BASED PROCESS ADJUSTMENT

| Severity | Definition | Process Modification |
| :--- | :--- | :--- |
| P1 — Critical | Service down or data integrity at risk | Steps 1 and 2 compressed. Rollback immediately if possible. Apply full process after mitigation. |
| P2 — Major | Major feature broken, many users affected | Full process but expedited. Skip extensive hypothesis ranking if cause is already obvious from evidence. |
| P3 — Minor | Minor bug, workaround exists | Full process. No shortcuts. |
| P4 — Cosmetic | Visual issue, no functional impact | Simplified: identify → fix → verify. Full hypothesis formation not required. |

---

## EXECUTION SEQUENCE

---

### MANDATORY STOP-AND-VERIFY GATE

>
> **[CONTEXT AMNESIA FAILSAFE]**
> Do NOT proceed to Step 1 until you have SILENTLY verified that all required context files and skill files have been read using tool calls.

### STEP 1 — UNDERSTAND THE SYMPTOM

**Mode:** Debugger
**Goal:** Establish exactly what is broken — not what you think is broken.

**CRITICAL RULE:** Do NOT touch any code until Step 1 is complete. The symptom is NOT the cause. Resist the urge to jump to a fix.

#### Actions (Step 1)

1. **Restate the symptom precisely:**
   - What is the exact observed behavior?
   - What is the expected behavior?
   - What is the difference between them?

2. **Gather basic context:**
   - When did this start? What changed recently?
   - Does it happen consistently or intermittently?
   - Who is affected — all users, some users, specific conditions?
   - What environment: local, staging, production?

3. **Reproduce the issue:**
   - Can it be reproduced locally?
   - What is the minimum set of steps to trigger it?
   - If not reproducible: what evidence exists — logs, error tracking, user reports?

4. **Classify severity and blast radius:**
   - Determine user impact, operational impact, data integrity risk
   - Decide whether rollback, feature flag disable, or traffic mitigation is needed immediately
   - Distinguish emergency containment from root-cause resolution

5. **CHECK MEMORY (MANDATORY — workspace first, then global):**
   - Scan `.agents/memory/mistakes-to-avoid.md` then `antigravity/memory/mistakes-to-avoid.md` — has this bug type been seen before?
   - Scan `.agents/memory/common-patterns.md` then `antigravity/memory/common-patterns.md` — does a proven fix pattern exist?
   - Scan `.agents/memory/postmortems.md` then `antigravity/memory/postmortems.md` — is this related to a past incident?

#### Output (Step 1)

```text
Symptom: [observed behavior] when [conditions]
Expected: [correct behavior]
Reproducible: [yes / no / intermittent]
Severity: [P1 / P2 / P3 / P4]
Immediate mitigation needed: [yes / no]
```

#### Gate (Step 1)

If the symptom is still vague, tighten the definition before proceeding. Do not move to evidence gathering against an unclear symptom statement.

---

### STEP 2 — GATHER EVIDENCE

**Mode:** Debugger
**Goal:** Collect the data that will point to the cause. Never compensate for weak evidence with stronger guessing.

#### Actions (Step 2)

1. **Read the actual error completely:**
   - Full error message, not just the first line
   - Full stack trace, read from the TOP
   - Error codes and HTTP status codes

2. **Check logs:**
   - Application logs around the time of failure
   - Database logs for slow queries or connection errors
   - External service logs for API responses or webhook deliveries

3. **Check recent changes:**
   - What code was deployed recently?
   - Were any configuration changes made?
   - Were any dependencies updated?
   - Were any infrastructure changes made?

4. **Check the data:**
   - Is the data in the state we expect?
   - Is there corrupted, missing, or unexpected data?
   - Is the data different between environments?

5. **Check the environment:**
   - Is this environment-specific?
   - Are external dependencies healthy — APIs, databases, services?
   - Are there resource constraints — memory, connections, CPU?

6. **Identify what evidence is strong, weak, missing, or misleading**
7. **Note any contradictions between evidence sources**

#### Output (Step 2)

```text
Evidence gathered:

- [item]
- [item]

Evidence still missing:

- [item]

What the evidence suggests:

- [summary]

```

#### Gate (Step 2)

If the issue is not reproducible, evidence quality matters even more. Do not compensate for weak evidence with stronger guessing.

---

### STEP 3 — FORM HYPOTHESES

**Mode:** Debugger
**Goal:** Generate plausible explanations ranked by likelihood. Avoid emotionally attaching to the first story that sounds right.

**CRITICAL RULE:** Do NOT assume your first hypothesis is correct. The goal is to ELIMINATE hypotheses through evidence, not to confirm your favorite guess.

#### Actions (Step 3)

1. Generate at least three plausible root-cause hypotheses when ambiguity exists
2. Rank by probability — most likely first
3. Rank by blast radius — which cause would be most severe if true
4. Classify the type of issue:
   - logic issue
   - data issue
   - contract mismatch
   - config issue
   - timing or race condition
   - infrastructure issue
   - security boundary issue
5. For each hypothesis identify:
   - What evidence supports it?
   - What evidence contradicts it?
   - How can it be tested — confirmed or eliminated?

#### Output (Step 3)

```text
Hypothesis 1 (most likely): [description]
  Evidence for: [...]
  Evidence against: [...]
  Test: [how to confirm or eliminate]

Hypothesis 2: [description]
  Evidence for: [...]
  Evidence against: [...]
  Test: [how to confirm or eliminate]

Hypothesis 3: [description]
  Evidence for: [...]
  Evidence against: [...]
  Test: [how to confirm or eliminate]
```

#### Gate (Step 3)

If there is only one hypothesis, ask whether that is because the evidence is overwhelming or because alternatives were not considered seriously.

---

### STEP 4 — ISOLATE AND CONFIRM ROOT CAUSE

**Mode:** Debugger
**Goal:** Narrow down to the actual root cause with evidence. Change one variable at a time.

**Gate:** Do NOT write a fix until the root cause is confirmed with evidence.

#### Actions (Step 4)

1. Test the most likely hypothesis first

2. **Isolate one variable at a time:**
   - Change ONE thing, observe the result
   - If behavior changes: contributing factor found
   - If behavior does not change: eliminate this hypothesis

3. **Use binary search when the problem area is large:**
   - Isolate half the suspect code path
   - If bug disappears: problem is in that half
   - Repeat until isolated to specific lines

4. **Apply the Five Whys once the failing point is found:**

   ```text
   Why did it fail?        → [immediate cause]
   Why did that happen?    → [deeper cause]
   Why did THAT happen?    → [structural cause]
   Continue until reaching a systemic root cause
   ```

5. **Confirm root cause with evidence:**
   - Can you explain ALL the observed symptoms from this root cause?
   - Does the evidence unambiguously support this conclusion?
   - Could there be multiple contributing causes?

6. Separate root cause from contributing factors

#### Output (Step 4)

```text
Root cause: [specific, evidence-backed explanation]
Evidence: [what proves this]
Contributing factors: [if any]
```

#### Gate (Step 4)

Do not call a hypothesis confirmed because it sounds coherent. Tie confirmation to actual evidence. If confidence remains low and impact is high, do not overstate certainty.

---

### STEP 5 — FIX

**Mode:** Builder
**Goal:** Implement a targeted fix that addresses the root cause, not the symptom.

**CRITICAL RULE:** A fix without a regression test is a temporary patch, not a solution.

#### Actions (Step 5)

1. **Design the fix:**
   - Does this fix the ROOT CAUSE or just mask the symptom?
   - What is the MINIMUM change that fixes the issue?
   - Could this fix introduce new problems?
   - Does this fix match existing code patterns and conventions?
   - Should the fix be immediate, staged, behind a flag, or paired with mitigation?

2. **Implement the fix:**
   - Follow `coding-standards.md` conventions
   - Make the smallest effective change
   - Preserve existing behavior everywhere else
   - Avoid bundling unrelated cleanup into urgent fixes
   - Add comments explaining WHY the fix works for future maintainers

3. **Write a regression test:**
   - The test MUST fail BEFORE the fix is applied
   - The test MUST pass AFTER the fix is applied
   - The test covers the exact conditions that triggered the original bug
   - The test prevents this specific bug from returning

#### Gate (Step 5)

Code must pass the `skill-coding` Non-Negotiable Checklist before proceeding to verification.

---

### STEP 6 — VERIFY

**Mode:** Reviewer
**Goal:** Confirm the fix works completely without side effects.

**Gate:** ALL verification checks must pass before delivery.

#### Actions (Step 6)

1. **Verify the original symptom is resolved:**
   - Re-run the exact reproduction steps from Step 1
   - Confirm the expected behavior now occurs

2. **Check for regressions:**
   - Run the full test suite
   - Manually verify adjacent functionality
   - Check edge cases around the fix

3. **Check for side effects:**
   - Does this change affect other code paths?
   - Are there other callers of the modified code?
   - Could this change affect performance?

4. **Verify in the appropriate environment:**
   - If the bug was environment-specific, verify in that environment
   - If a production bug: verify in staging with the same conditions

5. **Confirm observability:**
   - Do metrics, logs, and traces now reflect the intended outcome?
   - Note what is verified versus not yet verified

#### Output (Step 6)

```text
Verified:

- [item]
- [item]

Not yet verified:

- [item]

```

#### Gate (Step 6)

Do not treat "it stopped happening once" as sufficient proof for meaningful issues. Do not call the feature done until adjacent behavior and failure paths are checked.

---

### STEP 7 — ADD REGRESSION DEFENSE AND DELIVER

**Mode:** Communicator
**Goal:** Reduce recurrence risk and communicate the result clearly with full context.

#### Actions (Step 7) — Regression Defense

- Add or recommend a regression test, alert, validation rule, log improvement, or instrumentation
- Note if broader structural debt still exists beyond the immediate fix
- If the bug exposed a monitoring gap: flag it for observability improvement
- If the bug exposed a missing test category: consider broader test coverage improvement

#### Load Template (Step 7)

- [REQUIRED] Load [debug-report.md]({{GLOBAL_CONFIG_URI}}/global_templates/debug-report.md)
- Follow the structure and guidance in the template exactly to record the bug investigation.

---

### STEP 8 — POST-FIX & MEMORY CAPTURE (MANDATORY FOR SIGNIFICANT BUGS)

1. If the bug was P1 or P2: conduct a post-mortem within 48 hours
2. Post-mortem format: Timeline, Impact, Root Cause using Five Whys, Contributing Factors, Action Items with owners and deadlines
3. Blameless culture — focus on systems, not individuals

#### Memory Capture (write to workspace `.agents/memory/` first, global only for cross-project lessons)

- [ ] **Mistakes:** Log to `.agents/memory/mistakes-to-avoid.md` if this bug class could recur
- [ ] **Patterns:** Log to `.agents/memory/common-patterns.md` if the fix reveals a reusable pattern
- [ ] **Postmortem:** Log to `.agents/memory/postmortems.md` if P1/P2 severity
- [ ] **Contexts:** Update relevant context files if the bug reveals a gap in documented conventions

If workspace memory files do not exist, create them (copy format from global templates).

---

## CHECKPOINTS AND QUALITY GATES

| Gate | Condition | Action |
| :--- | :--- | :--- |
| Gate 1 — Symptom vague | Expected vs actual still ambiguous | Tighten symptom definition before evidence gathering |
| Gate 2 — No evidence, only guesses | Diagnosis is mostly intuition | Gather stronger evidence before changing code |
| Gate 3 — Structural issue, not local bug | Problem reveals architecture or ownership failure | Escalate to architecture or refactoring planning |
| Gate 4 — Fix is only containment | Change reduces impact but does not address cause | Label it mitigation, keep diagnosis open |
| Gate 5 — Low confidence, high impact | Certainty remains low for a severe issue | Do not overstate certainty, maintain mitigation, escalate verification |

---

## QUALITY GATE CHECKLIST

Before marking a bug fix as complete:

- [ ] Symptom clearly documented with expected versus actual behavior
- [ ] Severity classified and immediate mitigation assessed
- [ ] Evidence gathered before code was changed
- [ ] At least two to three hypotheses generated before fixing
- [ ] Root cause identified with evidence, not guessed
- [ ] Five Whys applied to reach structural cause
- [ ] Fix addresses root cause, not just symptom
- [ ] Minimum effective change implemented
- [ ] Regression test written — fails before fix, passes after
- [ ] Full test suite passes
- [ ] Adjacent functionality checked for regressions
- [ ] Fix follows `coding-standards.md`
- [ ] No unnecessary changes beyond the fix
- [ ] Delivery summary written with root cause explanation
- [ ] Remaining uncertainty stated honestly

---

## WORKFLOW ANTI-PATTERNS

| Anti-Pattern | Why It Is Harmful | How This Workflow Prevents It |
| :--- | :--- | :--- |
| Shotgun debugging | Random changes produce accidental behavior changes and leave the true cause untouched | Step 1 forces understanding before touching code |
| Assumption-based fixes | Guessing narrows the search space too early and produces false confidence | Steps 2 through 4 require evidence before fixing |
| Symptom suppression | Reducing visible failure while leaving the real mechanism intact keeps recurrence risk high | Step 4 requires root cause via Five Whys |
| Fix without regression test | The same problem returns and the team learns nothing durable | Step 5 requires regression test before completion |
| Scope creep during debugging | Refactoring unrelated code during diagnosis creates new risk | Step 5 requires minimum effective change |
| Incomplete verification | Fixing one thing while breaking another | Step 6 requires regression and side-effect checks |
| First-coherent-story bias | Treating the first plausible explanation as truth | Step 3 requires multiple ranked hypotheses |
| Declaring success too early | Treating one successful run as proof | Step 6 gate requires full verification before delivery |

---

## FAILURE MODES AND ESCALATION PATHS

| Failure Mode | What It Looks Like | Escalation |
| :--- | :--- | :--- |
| Monitoring Gap | Cannot diagnose because signals do not exist | Improve visibility before claiming diagnosis is complete |
| Logic Conflict | Bug is actually a feature misunderstanding | Switch to product or feature-build reasoning |
| Structural Debt | Local fix is unsafe or insufficient | Load `skill-refactoring.md`, decide whether to refactor first or isolate around the debt |
| Trust Breach | Issue crosses security or data boundaries | Load security and database skills, strengthen investigation |
| Multi-Incident | Multiple unrelated failures are bundled together | Split into separate investigations |

---

## RECOVERY RECIPES

> When debugging itself goes wrong, DO NOT spiral. Check this section first.

### Can't Reproduce the Bug

```

1. Check if the bug is environment-specific (prod vs local vs staging)
2. Check if it's timing-dependent (race condition, async order)
3. Ask: "Under what conditions does this NEVER happen?" — the inverse helps isolate
4. Add targeted logging at the suspect code path and wait for next occurrence
5. If truly unreproducible after 3 attempts → classify as intermittent, add monitoring, document
6. Do NOT guess-fix an unreproducible bug — you can't verify the fix
```

### All Hypotheses Eliminated

```

1. STOP — you're looking in the wrong area
2. Widen the search: check infra, config, data, and external dependencies
3. Check git log for recent changes in adjacent systems
4. Ask: "What ELSE changed around the time this started?"
5. Check memory/mistakes-to-avoid.md — a past pattern might match
6. If still stuck → rubber-duck the problem statement aloud: restate symptom + evidence
7. If still stuck after 30 min → take a break, come back fresh
```

### Fix Breaks Something Else

```

1. REVERT the fix immediately — don't layer fix-on-fix
2. The fix addressed a symptom, not the root cause — go back to Step 4
3. Check: who else calls the code you changed?
4. Check: what assumptions did the adjacent code make about the old behavior?
5. Design a fix that is compatible with ALL callers, not just the broken one
6. If impossible → the fix requires a broader refactor, escalate scope
```

### Bug is Actually a Feature Misunderstanding

```

1. STOP debugging — this isn't a bug, it's a requirements gap
2. Clarify: "Is this working as intended but not as expected?"
3. If yes → switch to /workflow-build-feature to change the behavior
4. If no → continue debugging with refined symptom definition
5. Document the misunderstanding so it doesn't waste time again
```

### Session Interrupted Mid-Debug

```

1. Read task.md for current phase and completed steps
2. Announce: "Resuming debug workflow from Phase [N]"
3. Re-read the symptom statement and evidence gathered so far from task.md notes
4. Check if new evidence appeared since last session (logs, user reports)
5. Resume from current phase — do NOT restart from symptom observation
```

### Pressure to Ship Incomplete Fix

```

1. If P1/P2: ship a MITIGATION (feature flag, rollback) immediately
2. Label it clearly: "This is mitigation, not a fix"
3. Keep the debug workflow OPEN — do not close the investigation
4. Schedule the root-cause fix for the next available slot
5. NEVER mark an incomplete fix as "done" — it will come back
```

---

## WORKFLOW STATE TRACKING

This workflow integrates with `task.md`.

**On activation:** Check `task.md` for existing state or create a new checklist.
**After each step:** Update `task.md` with current phase, status, and notes.
**On interruption:** task.md preserves progress for next session.

Phase map for state tracking:

```
1_understand_symptom → 2_gather_evidence → 3_form_hypotheses → 4_isolate_root_cause →
5_fix → 6_verify → 7_regression_defense → 8_post_fix_memory
```

---

## FINAL RULE

Do not debug by trying random fixes until the symptom disappears.

Debug by reducing uncertainty until the cause becomes explainable — then fix that cause precisely, verify it completely, and leave a regression test so it cannot return silently.

---

## VERSION HISTORY

| Version | Date | Changes |
| :--- | :--- | :--- |
| Gold v1.1 | Initial | Established the systematic sequence for diagnosing and fixing bugs |
| Gold v1.2 | 2026-04-10 | Added Recovery Recipes and Workflow State Tracking integration |
