# /check

Verify the current implementation against the active spec — tests, code review, and regression check.

**Steps:**
1. Read the active spec from `docs/specs/` and the active plan from `docs/plans/`
2. Run the full test suite and report results
3. Review all changed files against the spec's acceptance criteria — flag any gaps
4. Check for regressions by reviewing changed files for unintended side effects
5. Produce a structured report:
   - ✅ Acceptance criteria met
   - ❌ Acceptance criteria not met (with details)
   - ⚠️ Potential regressions (with details)
   - 📋 Suggested fixes
6. If all criteria are met and no regressions are found, prompt the user to run `/ship`
