---
name: koyeb-deploy
description: DEPRECATED. Koyeb removed its free tier. Use github-actions-deploy or n8n-workflow-deploy instead.
disable-model-invocation: true
---

# Koyeb — DEPRECATED (as of April 2026)

## Why This Skill Was Removed

Koyeb killed the free always-on tier. The "Pro plan" now requires a credit card upfront at **$30/month** with only $10 included credit — not acceptable for a student bootcamp focused on free infrastructure.

## What To Use Instead

| Your use case | Use this skill |
|---------------|----------------|
| Scheduled / cron / batch | **`github-actions-deploy`** |
| Webhook / chat / event-driven | **`n8n-workflow-deploy`** |
| Always-on API server | **`n8n-workflow-deploy`** (webhook node) OR self-host n8n on Oracle Cloud free tier |
| Telegram/Discord bot | **`n8n-workflow-deploy`** (polling trigger) |
| Full-stack web app (for later phases) | Self-hosted VPS — Hostinger ($5/mo) OR Oracle Cloud free |

## Bootcamp Decision

```
Schedule?  → GitHub Actions
Reacts?    → n8n
Unsure?    → n8n
```

See [`DEPLOY.md`](../../../DEPLOY.md) at the repo root for the full deployment guide.

## Historical Note

This file is kept as a reference so students understand **why** the recommendation changed, not to delete the decision trail. The free hosting landscape shifts — expect to re-evaluate every 6 months.
