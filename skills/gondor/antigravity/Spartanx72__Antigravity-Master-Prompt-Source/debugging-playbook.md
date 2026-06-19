# Playbook: Debugging

Use this workflow for bug triage and resolution.

## 1. Reproduce
- Define exact reproduction steps.
- Capture environment and version details.
- Identify expected vs observed behavior.
- Identify what surfaces must remain unchanged while fixing the bug.

## 2. Isolate
- Narrow problem surface to smallest component.
- Inspect recent changes and dependencies.
- Add temporary instrumentation/logging if required.

## 3. Diagnose
- Form one or more root-cause hypotheses.
- Validate hypotheses with targeted checks.
- Record evidence for accepted/rejected hypotheses.

## 4. Fix
- Implement minimal, low-risk correction.
- Preserve existing behavior outside bug scope.
- Add regression checks where possible.
- Avoid unrelated cleanup unless it is required to make the fix safe.

## 5. Validate
- Re-run reproduction path and regression checks.
- Confirm no UI or security regressions.
- Document final root cause, fix summary, and any new prevention rule or follow-up.
