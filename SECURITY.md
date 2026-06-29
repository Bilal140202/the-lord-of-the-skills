# 🔒 Security Policy

> *"I am a servant of the Secret Fire, wielder of the flame of Anor. You cannot pass."*

## 🛡 Supported Versions

The Lord of the Skills is actively maintained on the `main` branch. We publish security-relevant fixes as new GitHub Releases.

| Version | Supported |
|:---|:---|
| `main` (latest) | ✅ |
| v1.3.0+ | ✅ |
| < v1.3.0 | ❌ (please update) |

## 🐛 Reporting a Vulnerability

If you discover a security vulnerability in this repository, **please do NOT open a public issue**. Instead:

1. **Email**: [Bilal140202@users.noreply.github.com](mailto:Bilal140202@users.noreply.github.com) (or use GitHub's private vulnerability reporting at the Security tab)
2. **Subject**: `[SECURITY] The Lord of the Skills — <brief description>`
3. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Affected files/components
   - Suggested fix (if any)

**Response time**: within 48 hours.
**Disclosure**: We follow responsible disclosure — we'll credit you in the fix release unless you prefer to remain anonymous.

## 🌍 Scope

### In Scope
- **Crawler scripts** (`crawler/*.py`) — security bugs in the Python code (e.g., unsafe deserialization, command injection, path traversal)
- **CI/CD pipeline** (`.github/workflows/*.yml`) — secrets exposure, malicious PR workflows
- **GitHub Actions** — malicious actions, secret exfiltration
- **Documentation** — security-related misinformation

### Out of Scope
- **Skill artifacts** (`skills/**`) — these are reproduced from upstream repos under their original licenses. Vulnerabilities in skill content (e.g., a SKILL.md suggesting an insecure coding pattern) should be reported to the **upstream repo**, not here. We will, however, remove skills on request from upstream maintainers (see [docs/CREDITS.md](docs/CREDITS.md)).
- **Third-party dependencies** — report to the upstream package maintainer (e.g., `requests`, `reportlab`). We pin all versions in [crawler/requirements.txt](crawler/requirements.txt) for traceability.
- **Vulnerabilities in agents** that consume these skills (Claude Code, Cursor, Cline, etc.) — report to those vendors.

## ⚖ Intellectual Property & Redistribution Concerns

This repository crawls public GitHub repositories and redistributes their skill/agent/rule files. We take IP seriously:

### For Upstream Maintainers
If you are an upstream maintainer and:
- **Want your skills removed** → [open an issue](https://github.com/Bilal140202/the-lord-of-the-skills/issues/new) with title `Removal request: <your-repo>`. We comply within 24 hours.
- **Want attribution corrected** → see [docs/CREDITS.md](docs/CREDITS.md); open a PR or issue.
- **Want a license notice added** → open a PR adding it to `docs/CREDITS.md`.
- **Believe your code is misused** → email us privately (above).

### What We Do NOT Do
- ❌ We do NOT re-license upstream artifacts. Every file in `skills/` retains its original license.
- ❌ We do NOT modify the content of upstream artifacts (except for filename normalization for URL/git safety — see [DEDUP.md](DEDUP.md)).
- ❌ We do NOT sell or commercialize this compilation. The compilation scripts are MIT; the artifacts retain upstream licenses.

## 🔐 Security Best Practices for Users

When using skills from this compilation:

1. **Audit before use** — Review any skill file before copying it into your agent's directory. Skills can contain arbitrary instructions that your agent may execute.
2. **Check the source** — Every skill has a `source_repo` field in [`_manifest.json`](MANIFEST.md). Verify the upstream repo's reputation before trusting a skill.
3. **Prefer canonical ⭐** — Canonical representatives have been vetted by the dedup algorithm (see [DEDUP.md](DEDUP.md)). They're not guaranteed safe, but they're the best version we found.
4. **Don't run as root** — Run your agent with minimal permissions. Skills that suggest filesystem writes, network calls, or shell execution should be sandboxed.
5. **Review CI workflows** — If you fork this repo and enable GitHub Actions, review `.github/workflows/ci.yml` first. It runs on every push and PR.

## 🛠 Crawler Security

The crawler is designed with these safety properties:

- **No code execution** — The crawler only clones repos and reads files. It never executes Python, shell, or any other code from crawled repos.
- **Path traversal protection** — Extracted files are written to a sandboxed `_raw/` directory with sanitized filenames (see `safe_filename()` in `crawler/crawler.py`).
- **No secrets in code** — The crawler reads `GITHUB_TOKEN` from environment variable only. No hardcoded credentials.
- **Rate limiting** — Respects GitHub API rate limits (60 req/hr unauthenticated, 5000 req/hr with token).
- **Disk-aware** — Built-in disk space monitoring and cache pruning to avoid filling the disk.

If you find a violation of any of these properties, please report it privately.

## 📜 License

This security policy is part of The Lord of the Skills project, licensed under MIT. See [LICENSE](LICENSE).

---

<div align="center">

*The dark fire will not avail you, flame of Udûn. Go back to the shadow!*

</div>
