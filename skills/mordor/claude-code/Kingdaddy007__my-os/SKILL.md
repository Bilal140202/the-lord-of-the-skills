---
name: APPLICATION SECURITY & THREAT MODELING
description: >
  Use this skill when the work involves authentication, authorization, trust
  boundaries, sensitive data, input validation, or vulnerability assessment.
  Activated when designing or modifying AuthN/AuthZ flows; handling or storing
  PII, financial, or health data; processing user input or file uploads;
  integrating with third-party APIs; designing system boundaries; reviewing
  pull requests (implicitly always active); or when the user mentions security
  concerns, vulnerabilities, or asks for a security audit. Examples: "is this
  secure?", "audit this for vulnerabilities", "how should I handle auth?",
  "is this input validation sufficient?", "what are the security risks here?",
  mentions of XSS, CSRF, SQLi, IDOR. Security is ALWAYS active as a secondary
  lens during code review and architecture design — never skip it.
---

# APPLICATION SECURITY & THREAT MODELING

## WHEN TO USE THIS

- Designing or modifying Authentication (AuthN) or Authorization (AuthZ) flows
- Handling, storing, or transmitting sensitive data (PII, financial, health)
- Processing user input or file uploads
- Integrating with third-party APIs or external systems
- Designing system boundaries and network architecture
- Reviewing pull requests (implicitly always active)
- User asks for a security audit or mentions specific vulnerabilities

## NEVER DO

- Trust client-side validation as a primary defense mechanism
- Store secrets or API keys in code, plaintext files, or environment variables committed to version control
- Use blocklists (denylist) to filter input — use allowlists
- Build custom cryptography or hashing algorithms
- Grant wildcard (`*`) IAM or database permissions to bypass blockers
- Fail open — when in doubt, deny access
- Trust data from internal microservices without validation

---

## MINDSET — ASSUME BREACH

The staff-level security mental model operates on one core assumption: **Assume Breach.**

Do not trust the network, the user, the internal microservices, the database, or the third-party API. Perimeter defense (firewalls) is insufficient because threats often originate from inside the perimeter or bypass it via application logic flaws.

Security is never an afterthought, a final audit, or a compliance checklist. It is integrated directly into the architectural design phase ("Shift Left") to prevent flaws before implementation begins.

View the system through the eyes of a malicious actor: *"How can I break this? How can I bypass this? How can I use this feature in a way the developer never intended?"* Do not rely on obscurity. Rely on mathematically proven cryptographic standards and robust, centralized authorization mechanisms.

---

## DECISION FRAMEWORK — STRIDE

| Threat | What the Attacker Does | Primary Mitigation | Security Property |
| --- | --- | --- | --- |
| **S**poofing | Pretending to be someone else | Strong AuthN, MFA, robust session management | Authentication |
| **T**ampering | Modifying data in transit or at rest | Input validation, parameterized queries, TLS | Integrity |
| **R**epudiation | Claiming they didn't perform an action | Non-repudiable audit logging, digital signatures | Non-repudiation |
| **I**nformation Disclosure | Accessing data they shouldn't see | TLS, encryption at rest, strict AuthZ rules | Confidentiality |
| **D**enial of Service | Crashing or exhausting the system | Rate limiting, WAFs, load shedding, pagination | Availability |
| **E**levation of Privilege | Gaining admin rights without authorization | RBAC, Least Privilege | Authorization |

---

## SECURITY LENSES

Apply all ten before and during security work:

**1. Trust Boundaries** — Where does untrusted input enter? Where do identities change context? Which systems, users, or services should not automatically trust each other?

**2. Authentication** — How is identity established? Is the method appropriate? Are session/token lifecycles, expiration, refresh, and invalidation handled safely?

**3. Authorization** — Who is allowed to do what? Is access control enforced server-side? Are permissions scoped narrowly and explicitly? Is object-level access checked, not just route-level access?

**4. Input and Output Safety** — Are inputs validated at the correct boundaries? Are outputs encoded safely for their context? Could user-controlled data trigger injection, script execution, or unsafe rendering?

**5. Sensitive Data Handling** — What data is sensitive? Is it encrypted in transit and at rest? Is retention minimized? Is exposure limited to the minimum required surface?

**6. Secret and Credential Handling** — Where are secrets stored? Are they hardcoded, logged, copied into configs, or otherwise handled unsafely? Are privileged credentials rotated and scoped appropriately?

**7. Abuse and Misuse Cases** — How could a malicious actor misuse this feature? What is the worst credible abuse path? What controls limit spam, enumeration, privilege escalation, or automated abuse?

**8. Blast Radius** — If this component is compromised, what else is reachable? What can the attacker do next? Are privileges and trust relationships too broad?

**9. Auditability and Detection** — Would we know if this were abused? Are there logs or signals for auth events, denied access, unusual access patterns, or suspicious failures? Are those logs safe and non-leaky?

**10. Safe Defaults** — Does the design fail closed or fail open? Are protections on by default? Would a rushed implementation accidentally deploy an unsafe configuration?

---

## SECURITY HEURISTICS

Prefer:

- Explicit authorization checks over implied assumptions
- Allowlists over permissive acceptance where appropriate
- Narrow access scopes over broad permissions
- Short-lived and well-scoped credentials where possible
- Safe framework defaults over custom risky logic
- Server-side enforcement over client-side trust
- Degrading safely over failing open
- Visibility into auth events and suspicious activity
- Standard vetted cryptographic libraries over custom implementations
- Least-privilege IAM and database roles over wildcard grants

---

## BEHAVIORAL WORKFLOW

### Step 1 — Map the Trust Boundaries

Draw a box around the components you control. Everything outside is untrusted. Identify every point where data crosses a boundary (APIs, UI forms, file uploads, database queries). Data loses its "trusted" status the moment it crosses a boundary.

### Step 2 — Identify Sensitive Assets

What data, if leaked, would cause catastrophic business or user harm? Where does this data live? How does it move? Who needs access to it?

### Step 3 — Apply Threat Modeling (STRIDE)

Look at the trust boundaries and assets. Apply STRIDE categories. Ask: "How could someone spoof an identity here? How could they tamper with this payload?"

### Step 4 — Design Input Validation

Define a strict **Allowlist** for all incoming data (type, length, format, range). Never use blocklists — they always fail. Sanitize and escape data right before it is used (parameterized queries for SQL, HTML escaping for UI).

### Step 5 — Enforce Access Control

Do not rely on UI hiding. The API must verify authorization on *every single request*. Check both vertical privilege (is this user an admin?) and horizontal privilege (is this User A's document, or User B's document?).

### Step 6 — Secure the Secrets

Ensure no API keys, passwords, or salts are in the code. Ensure logging mechanisms strip PII, passwords, and tokens before writing to disk.

### Step 7 — Define the Failure State

If the authentication service goes down, does the application default to letting everyone in, or locking everyone out? It must lock everyone out. Ensure error messages do not leak internal system details ("Invalid password" not "User found, but password incorrect").

### Step 8 — Before Finalizing, Re-check

- Are trust boundaries correctly enforced?
- Is access control logic verified at both route and object level?
- Is input and output safety verified?
- Is secret handling and data exposure verified?
- Does security logging leak sensitive data?
- Is observability sufficient for incident response?
- If uncertainty remains, state confidence and investigation gaps explicitly.

---

## BEHAVIORAL SECTIONS

### A. Designing roles and permissions

1. Define roles by capability, not vague status labels.
2. Scope permissions narrowly.
3. Verify checks at the server or authoritative boundary.
4. Avoid broad admin-like bypasses unless absolutely necessary.
5. Check object ownership, tenant boundaries, and row-level access assumptions.

### B. Handling secrets and tokens

1. Never hardcode secrets.
2. Never log secrets, credentials, or sensitive tokens.
3. Scope and rotate credentials appropriately.
4. Set expiration and invalidation behavior deliberately.
5. Prefer external secret management or controlled environment injection over ad hoc handling.

### C. Designing against abuse

1. Consider enumeration, replay, brute-force, spam, mass access, and privilege escalation.
2. Add rate limiting, throttling, or challenge mechanisms where appropriate.
3. Distinguish between normal errors and attacker-useful feedback.
4. Ensure the system does not reveal more than necessary through error messages or timing differences.

### D. Reviewing existing code for security

1. Walk the flow like an attacker or abusive user would.
2. Ask what happens if an untrusted caller manipulates identity, input, resource identifiers, volume, or timing.
3. Check whether access control is enforced at the right layer.
4. Check for unsafe logging, leaking errors, or insecure defaults.
5. Check whether missing monitoring would make security incidents invisible.

### E. Integrating with external systems

1. Treat all third-party data as untrusted until validated.
2. Verify webhook signatures and API response integrity.
3. Scope API credentials to only the operations needed.
4. Define failure behavior when the external system is unavailable or returns unexpected data.

---

## KEY DIAGNOSTIC QUESTIONS

- **Boundary Question:** Where exactly does untrusted input enter the system, and is it validated *immediately* upon entry?
- **Privilege Question:** Does this service/function run with more database or cloud permissions than it strictly needs?
- **Lateral Movement Question:** If this specific container/service is completely compromised, what prevents the attacker from accessing the billing service next door?
- **Abuse Case Question:** How could a user manipulate this perfectly functioning feature (password reset, file upload) to harm the system or other users?
- **Log Question:** If I search the production logs right now, will I find session tokens or plaintext user data?

---

## ANTI-PATTERNS

| Anti-Pattern | What It Looks Like | Why It's Harmful | Fix |
| --- | --- | --- | --- |
| **Client-Side Security** | JavaScript validation or hidden UI buttons as the only access control | An attacker can bypass the browser entirely via cURL or Postman | Client-side checks are for UX. Backend must validate everything independently. |
| **Blocklist / Denylist** | Regexes filtering out `<script>` or `OR 1=1` | Attackers use encoded payloads, mixed casing, or alternative syntax your blocklist didn't anticipate | Use Allowlists. Define exactly what *is* allowed and reject everything else. |
| **Security by Obscurity** | Assuming an endpoint is safe because it's not documented | Attackers decompile apps, monitor network traffic, and reverse-engineer logic. Once the secret is found, the system falls. | A system must remain secure even if the attacker has the entire source code (Kerckhoffs's principle). |
| **Wildcard Permissions** | `AmazonS3FullAccess` or `GRANT ALL PRIVILEGES` to get things working quickly | If that service is breached, the attacker gains god-mode access to infrastructure | Apply Least Privilege. Grant only the specific permissions the service actually needs. |

---

## OUTPUT SHAPE

```markdown

## Security Scope

What components/flows are being evaluated.

## Trust Boundaries

Where data crosses from untrusted to trusted zones.

## Threat Assessment (STRIDE)

| Threat | Component | Vulnerability | Severity |
| --- | --- | --- | --- |
| Spoofing | Auth API | Missing rate limiting | High |
| Tampering | DB Layer | String concat in SQL | Critical |

## Identified Vulnerabilities (Prioritized)

### 🔴 Critical / High

- **Vulnerability:** [Description]
- **Exploit Path:** [How an attacker uses it]
- **Blast Radius:** [What happens when exploited]
- **Remediation:** [Exact code/arch change needed]

### 🟡 Medium / Low

- [Lower priority hardening steps]

## Hardening Recommendations

General architectural or process changes to improve defense in depth.
```

---

## NON-NEGOTIABLE CHECKLIST

- [ ] **Authentication:** All endpoints (except explicit public ones) require verified identity
- [ ] **Authorization:** Every request verifies user has permission to access the *specific resource* requested (IDOR prevention)
- [ ] **Input Validation:** All input validated against a strict allowlist
- [ ] **SQLi Prevention:** Parameterized queries or ORMs used exclusively — no string concatenation for SQL
- [ ] **XSS Prevention:** Output contextually escaped before rendering in a browser
- [ ] **Secret Management:** Secrets injected via environment variables or secret managers — never committed to repo
- [ ] **Cryptography:** Standard, vetted libraries used for hashing (Argon2, bcrypt) and encryption (AES-GCM) — no custom crypto
- [ ] **Transit:** All communication happens over HTTPS/TLS

---

**Final Rule:** Security is about controlling trust, capability, and blast radius under imperfect conditions. A strong security result makes clear: what is being protected, where the trust boundary is, what could go wrong, how the system reduces that risk, and what still needs verification before trust is justified.
