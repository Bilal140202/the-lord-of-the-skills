---
name: test
description: name: test
---
# Test

Run tests with coverage analysis.

Load test-driven-development skill for the full RED-GREEN-REFACTOR process.

## Running Tests
1. Run full test suite first to establish baseline
2. Report: total tests, passed, failed, skipped, coverage %
3. For failures: show exact error messages, not summaries

## On Test Failure
Load systematic-debugging skill — investigate root cause before fixing.
Load verification-before-completion skill before declaring tests fixed.

## Coverage

80% is the minimum floor for shipping. It is not a target — high-risk code (auth, payments, data mutations) should be 95%+. Do not write coverage-padding tests.

- Report overall coverage %
- Flag files below 80% coverage
- Do NOT write tests purely to increase coverage numbers

## Mass Failure Guidance

If >20 tests fail simultaneously (e.g., major dependency upgrade): do NOT fix test-by-test. First, understand the failure pattern — are they all failing for the same root cause? Fix the root cause, then re-run. Load systematic-debugging skill.

## Before Declaring Done
Load verification-before-completion skill.
Actually run the tests. Do not claim they pass without running them.

## Example Test Report

```
Test run: 2026-02-25 18:30 UTC
Command: pytest tests/ -v --cov=src --cov-report=term

Results: 47 passed | 0 failed | 2 skipped
Coverage: 84.3% overall
  src/auth.py: 97.2% ✓
  src/user.py: 81.4% ✓
  src/notifications.py: 61.0% ⚠ BELOW THRESHOLD

Action required: notifications.py below 80% — add tests before shipping
```
