---
description: Technical feasibility evaluation for a new feature or technology concept.
---

# /idea

Evaluates the technical viability of a concept within the current stack.

## Steps

1. Define the core concept and technical requirements.
2. Identify underlying technologies and dependencies.
3. Assess stack compatibility: Next.js, Supabase, Vercel.
4. Estimate effort.
5. Identify security, performance, or architectural risks.
6. Issue verdict.

## Verdict format

YES: Provide an actionable implementation plan.
PARTIAL: List supported vs unsupported components and propose workarounds.
NO: State blocking reasons and propose viable alternatives.

## Example

Input: /idea implement passkey authentication

Output:
```
Concept: Passwordless authentication via device biometrics.

Stack compatibility:
- Next.js: supported
- Supabase: indirect (workarounds needed)
- Vercel: supported

Verdict: PARTIAL

Supported path: integrate WebAuthn via @simplewebauthn as secondary MFA.
Blocking path: exclusive passkey auth has device compatibility limits.
Estimated effort: 4-6 hours.
Alternative: magic links (native Supabase support).
```
