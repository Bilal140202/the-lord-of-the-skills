---
description: OWASP-based security audit — secrets, database, auth, HTTP headers, vulnerability scan.
---

# /check-security

Full security audit of the current project.

## Scope

1. Environment and secrets
   - Check for .env files in git staging.
   - Scan source for hardcoded credentials, tokens, API keys.
   - Validate NEXT_PUBLIC_ conventions.

2. Database (Supabase/Postgres)
   - Run Security Advisor via MCP.
   - Verify RLS is active on all sensitive tables with explicit policies.
   - Check stored procedures for secured search_path.
   - Verify no excessive privileges on public roles.

3. Authentication and sessions
   - Review middleware for zero-trust pattern on private routes.
   - Verify cookie/session destruction.
   - Evaluate OAuth flows for session hijacking vectors.

4. HTTP headers (next.config.ts)
   - Content-Security-Policy
   - Strict-Transport-Security
   - X-Frame-Options
   - X-Content-Type-Options
   - CORS configuration.

5. Vulnerability checklist
   Injections: SQLi, NoSQL, OS command, XXE, SSTI.
   Client: XSS (reflected, stored, DOM), SSRF, CSRF, clickjacking, open redirects.
   Access control: IDOR, broken access control, path traversal, LFI, RFI, mass assignment.
   Auth: brute force, session fixation, session hijacking, JWT vulnerabilities.
   Data: insecure deserialization, race conditions, sensitive data exposure.
   Config: missing headers, weak ciphers, outdated dependencies (npm audit).

## Output format

CRITICAL: Deployment blocker. Fix before any push.
WARNING: Moderate risk. Fix before release.
IMPROVEMENT: Minor optimization.
SECURE: Check passed.
