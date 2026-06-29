# Playbook: Deployment Checklist

Use this checklist before releasing changes.

## Pre-Deployment
- [ ] Confirm scope and changelog summary.
- [ ] Verify tests/lint/build checks are green.
- [ ] Verify secrets/config are externalized.
- [ ] Review security-sensitive changes.
- [ ] Confirm ports, protocols, and exposure level (local, LAN, or internet-facing).
- [ ] Confirm least-exposure network posture and reverse proxy or TLS needs.

## Release Readiness
- [ ] Confirm migration or rollout requirements.
- [ ] Confirm rollback strategy.
- [ ] Confirm monitoring/alerts for changed components.
- [ ] Confirm public exposure, credential handling, and paid-service implications are understood.

## Post-Deployment
- [ ] Smoke test critical paths.
- [ ] Check logs/metrics for anomalies.
- [ ] Record release notes and follow-up actions.
