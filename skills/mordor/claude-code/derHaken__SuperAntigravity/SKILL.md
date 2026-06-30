---
name: security-review
description: Use when reviewing code for vulnerabilities, implementing authentication or authorization, handling user input, storing sensitive data, or before any feature that touches security boundaries goes to production
---

# Security Review

## Overview

Security is not a feature — it's a property of the entire system.
Review security boundaries systematically, not ad-hoc.

## When to Use

- Authentication, authorization, session management code
- Any user input that touches storage, commands, or rendering
- Secrets, credentials, API keys in code or config
- Before a security-sensitive feature ships
- After any change to auth flows or data access controls

## OWASP Top 10 Checklist

Work through these for every security-relevant code change:

**A01 - Broken Access Control**
- [ ] Every endpoint checks authorization, not just authentication
  - Search: `grep -r 'router\.\|app\.\(get\|post\|put\|delete\|patch\)' --include='*.js' --include='*.ts' | grep -v 'auth\|authorize\|permission\|role'`
- [ ] Users can only access their own data
  - Search: `grep -rn 'req\.params\.id\|req\.query\.id' --include='*.js' --include='*.ts'` — verify each result checks ownership
- [ ] Admin functions require explicit admin role check
  - Search: `grep -rn 'admin' --include='*.js' --include='*.ts' | grep -v 'isAdmin\|requireAdmin\|role.*admin\|admin.*role'`

**A02 - Cryptographic Failures**
- [ ] No secrets in source code or env files committed to git
  - Search: `grep -rn 'password\s*=\s*["\x27][^"\x27]\|api_key\s*=\s*["\x27][^"\x27]\|secret\s*=\s*["\x27][^"\x27]' --include='*.js' --include='*.py' --include='*.ts'`
- [ ] Passwords hashed with bcrypt/argon2 (not MD5/SHA1)
  - Search: `grep -r 'password' --include='*.js' --include='*.ts' --include='*.py' | grep -v 'bcrypt\|argon2\|hash'`
  - Also check: `grep -rn 'md5\|sha1\|sha256' --include='*.js' --include='*.ts' --include='*.py' | grep -i 'password'`
- [ ] Data in transit uses TLS
  - Search: `grep -rn 'http://' --include='*.js' --include='*.ts' --include='*.py' | grep -v 'localhost\|127\.0\.0\.1\|test\|spec\|comment'`
- [ ] Sensitive data not logged
  - Search: `grep -rn 'console\.log\|logger\.' --include='*.js' --include='*.ts' | grep -i 'password\|token\|secret\|key\|ssn\|credit'`

**A03 - Injection**
- [ ] All database queries use parameterized queries / ORM (never string concat)
  - Search: `grep -rn 'query\s*[+\`].*\(req\.\|user\.\|input\|params\)' --include='*.js' --include='*.ts' --include='*.py'`
  - Also: `grep -rn '"SELECT\|"INSERT\|"UPDATE\|"DELETE' --include='*.js' --include='*.ts' | grep '\+'`
- [ ] All shell commands use safe exec (never `eval` with user input)
  - Search: `grep -rn 'eval(\|exec(\|system(\|spawn(' --include='*.js' --include='*.ts' --include='*.py'`
- [ ] All HTML output is escaped or uses safe template engine
  - Search: `grep -rn 'innerHTML\s*=' --include='*.js' --include='*.ts' | grep -v '//.*innerHTML'`

**A04 - Insecure Design**
- [ ] Authentication flows validated against known-good patterns
- [ ] Rate limiting on authentication endpoints
  - Search: `grep -rn 'login\|signin\|auth' --include='*.js' --include='*.ts' | grep -v 'rateLimit\|rate_limit\|throttle'`
- [ ] Account enumeration prevented (same response for unknown user vs wrong password)
  - Search: `grep -rn '"User not found"\|"Invalid username"\|"No account"' --include='*.js' --include='*.ts' --include='*.py'`

**A05 - Security Misconfiguration**
- [ ] Debug mode disabled in production
  - Search: `grep -rn 'debug\s*=\s*true\|DEBUG\s*=\s*True\|NODE_ENV.*development' --include='*.js' --include='*.ts' --include='*.py' --include='*.env'`
- [ ] Default credentials changed
  - Search: `grep -rn 'admin.*admin\|root.*root\|password.*password\|default.*password' --include='*.js' --include='*.ts' --include='*.py'`
- [ ] Unnecessary features/endpoints disabled
- [ ] Error messages don't expose stack traces to users
  - Search: `grep -rn 'err\.stack\|error\.stack\|traceback' --include='*.js' --include='*.ts' --include='*.py' | grep -v 'log\|console\|logger'`

**A06 - Vulnerable and Outdated Components**
- [ ] Dependencies checked against known CVE databases (npm audit, pip-audit, snyk)
  - Run: `npm audit` or `pip-audit` or `snyk test`
- [ ] No dependencies with known critical/high CVEs in production
  - Run: `npm audit --audit-level=high` (exits non-zero if high/critical found)
- [ ] Lock files committed (package-lock.json, poetry.lock, etc.)
  - Search: `git ls-files | grep -E 'package-lock\.json|yarn\.lock|poetry\.lock|Pipfile\.lock|Gemfile\.lock'`
- [ ] Direct dependencies pinned to specific versions
  - Search: `grep -E '"\^|"~|">=|">' package.json` — each result is a non-pinned dependency

**A07 - Authentication Failures**
- [ ] Session tokens invalidated on logout
  - Search: `grep -rn 'logout\|signout\|sign_out' --include='*.js' --include='*.ts' --include='*.py' | grep -v 'destroy\|invalidate\|clear\|delete\|revoke'`
- [ ] Password reset tokens expire and are single-use
  - Search: `grep -rn 'reset.*token\|token.*reset' --include='*.js' --include='*.ts' --include='*.py'` — verify expiry and single-use enforcement
- [ ] Brute force protection on login
  - Search: `grep -rn 'login\|signin' --include='*.js' --include='*.ts' | grep -v 'attempts\|lockout\|rateLimit\|throttle'`

**A08 - Software and Data Integrity**
- [ ] Dependencies pinned to verified versions
- [ ] No eval() or dynamic code execution with user input
  - Search: `grep -rn 'eval(' --include='*.js' --include='*.ts' --include='*.py'`
  - Also: `grep -rn 'new Function(' --include='*.js' --include='*.ts'`

**A09 - Logging and Monitoring**
- [ ] Authentication events logged (success and failure)
  - Search: `grep -rn 'login\|signin\|authenticate' --include='*.js' --include='*.ts' --include='*.py' | grep -v 'log\|audit\|event\|monitor'`
- [ ] Sensitive operations audited
- [ ] Logs don't contain secrets or PII
  - Search: `grep -rn 'log\.' --include='*.js' --include='*.ts' | grep -i 'password\|token\|secret\|ssn\|credit_card\|cvv'`

## Common Vulnerabilities to Check

| Vulnerability | Check |
|---------------|-------|
| SQL Injection | All queries parameterized? |
| XSS | All user content escaped before rendering? |
| CSRF | State-changing requests have CSRF protection? |
| Path traversal | File paths sanitized and validated? |
| Secret exposure | No hardcoded keys/tokens in code? |
| Mass assignment | Only allowed fields accepted from user input? |

## Red Flags in Code

These patterns require immediate review:
- `eval()`, `exec()`, `system()` with any user-influenced input
- String concatenation in SQL: `"SELECT * FROM users WHERE id = " + userId`
- `innerHTML = userContent` (XSS)
- `require(userInput)` or dynamic imports with user data
- Secrets in `.env` files committed to git
- MD5 or SHA1 for password hashing

## Output

For each finding, document:
1. **Vulnerability type** (OWASP category)
2. **Severity** (Critical/High/Medium/Low)
3. **Location** (file:line)
4. **Description** (what's wrong and why)
5. **Fix** (specific code change or pattern to use)

If no vulnerabilities found: output "Security Review: PASS. No issues found in [scope]. Reviewed: [list of OWASP categories checked]. Verified: [date and reviewer]."
