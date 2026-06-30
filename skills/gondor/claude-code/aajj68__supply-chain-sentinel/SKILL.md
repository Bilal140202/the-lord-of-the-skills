---
name: supply-chain-sentinel
description: >
  Security scanner for supply chain attacks, malicious dependencies, prompt injection,
  and suspicious code patterns. Use this skill whenever the user asks to audit a project,
  scan for malicious packages, check dependencies for threats, look for prompt injection,
  detect typosquatting, review supply chain security, or investigate suspicious code.
  Also trigger for: "check if this is safe", "scan my deps", "audit my project",
  "is there anything malicious", "security review", "check for backdoors",
  "supply chain attack", "dependency confusion", "malicious npm/pip/cargo package".
  Works with Python, Node.js, Go, Rust, Java/Maven/Gradle, and mixed projects.
  ALWAYS use this skill when security scanning of any kind is requested.
---

# Supply Chain Sentinel

Scanner portátil de segurança para detectar ataques de supply chain, dependências maliciosas,
injeção de prompt, código obfuscado e padrões suspeitos em projetos de software.

## Fluxo de Execução

1. **Leia este arquivo completo** antes de começar
2. **Execute o scanner Python** via `scripts/scanner.py`
3. **Complemente com análise manual** dos achados de alta severidade
4. **Gere o relatório final** em Markdown

---

## Passo 1 — Localizar o Projeto

Se o usuário não especificou o path:
```bash
# Tenta caminhos comuns
ls /mnt/user-data/uploads/ 2>/dev/null || true
ls ~/project/ 2>/dev/null || true
pwd
```

Pergunte ao usuário se não encontrar. O scanner aceita qualquer diretório raiz.

---

## Passo 2 — Executar o Scanner

Copie o script para um local gravável e execute:

```bash
cp /mnt/skills/*/supply-chain-sentinel/scripts/scanner.py /tmp/sentinel_scanner.py \
  || cp "$(dirname "$0")/scripts/scanner.py" /tmp/sentinel_scanner.py

python3 /tmp/sentinel_scanner.py --path <PROJECT_DIR> --output /tmp/sentinel_report.json
```

Se o script não estiver acessível via path relativo, **escreva-o em disco** usando
o conteúdo da seção `## Scanner Script` abaixo, salve em `/tmp/sentinel_scanner.py`
e execute normalmente.

---

## Passo 3 — Análise Manual Complementar

Após o scanner, faça buscas direcionadas nos achados críticos:

### 3a. Verificar setup.py / pyproject.toml suspeitos
```bash
# Chamadas de rede no setup
grep -rn "urllib\|requests\|socket\|http" <PROJECT_DIR>/setup.py \
  <PROJECT_DIR>/pyproject.toml 2>/dev/null

# Exec/eval no install
grep -rn "exec\|eval\|compile\|__import__" <PROJECT_DIR>/setup.py 2>/dev/null
```

### 3b. Strings Base64 / Ofuscadas
```bash
grep -rEn "base64\.(b64decode|decodebytes)|\\\\x[0-9a-f]{2}|eval\(.*decode" \
  <PROJECT_DIR> --include="*.py" --include="*.js" --include="*.ts" 2>/dev/null | head -50
```

### 3c. Prompt Injection em arquivos de config/prompt
```bash
grep -rniP "(ignore previous|disregard|you are now|forget your|override instructions|\
act as if|new system prompt|jailbreak|\\[INST\\]|<\|system\|>)" \
  <PROJECT_DIR> --include="*.txt" --include="*.md" --include="*.json" \
  --include="*.yaml" --include="*.yml" --include="*.toml" 2>/dev/null
```

### 3d. Caracteres Invisíveis / Unicode Suspeito
```bash
# Zero-width chars e bidi override (CVE-2021-42574 "Trojan Source")
grep -rPn "[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff]" \
  <PROJECT_DIR> --include="*.py" --include="*.js" --include="*.ts" 2>/dev/null | head -30
```

### 3e. Exfiltração de Credenciais / Env Vars
```bash
grep -rEn "(os\.environ|getenv|AWS_|GITHUB_TOKEN|api.key|password|secret)" \
  <PROJECT_DIR> --include="*.py" --include="*.js" 2>/dev/null \
  | grep -v "test\|spec\|example\|\.env\.example" | head -40
```

---

## Passo 4 — Consolidar e Gerar Relatório

Leia o JSON gerado pelo scanner e os resultados manuais, depois produza um relatório Markdown estruturado:

```
# 🛡️ Security Audit Report — Supply Chain Sentinel

**Projeto:** <nome>
**Data:** <data>
**Severidade Geral:** 🔴 CRÍTICA / 🟠 ALTA / 🟡 MÉDIA / 🟢 BAIXA

---

## Resumo Executivo
<2-3 parágrafos>

## Achados por Categoria
### 🔴 Críticos
### 🟠 Altos  
### 🟡 Médios
### 🟢 Informativos

## Dependências Suspeitas
<tabela: pacote | versão | risco | motivo>

## Recomendações
<lista priorizada>

## Metodologia
```

---

## Scanner Script

Se o script não estiver acessível via filesystem, **crie-o** com este conteúdo em `/tmp/sentinel_scanner.py`:

```python
#!/usr/bin/env python3
"""
Supply Chain Sentinel — scanner.py
Portable security scanner for supply chain attacks, malicious deps, prompt injection.
"""

import os, sys, re, json, hashlib, argparse, ast
from pathlib import Path
from datetime import datetime
from typing import Any

# ── Typosquatting: common targets (PyPI top 100 + security-relevant) ──────────
PYPI_POPULAR = {
    "requests","numpy","pandas","flask","django","fastapi","boto3","pydantic",
    "sqlalchemy","celery","redis","pymongo","psycopg2","cryptography","paramiko",
    "httpx","aiohttp","click","typer","rich","setuptools","pip","wheel","twine",
    "pytest","black","mypy","flake8","pylint","isort","poetry","virtualenv",
    "pillow","matplotlib","scipy","sklearn","torch","tensorflow","keras",
    "openai","anthropic","langchain","transformers","huggingface-hub",
    "ansible","fabric","invoke","nox","tox","coverage","hypothesis",
    "uvicorn","gunicorn","starlette","pydantic-settings","alembic",
}

NPM_POPULAR = {
    "react","vue","angular","express","lodash","axios","webpack","babel",
    "typescript","jest","eslint","prettier","next","nuxt","vite","rollup",
    "moment","dayjs","chalk","commander","dotenv","cors","helmet","jsonwebtoken",
    "bcrypt","mongoose","sequelize","prisma","graphql","apollo","socket.io",
    "nodemailer","multer","sharp","uuid","crypto-js","node-fetch","cross-fetch",
}

# ── Suspicious code patterns ──────────────────────────────────────────────────
SUSPICIOUS_PATTERNS = [
    # Obfuscation / dynamic execution
    (r'eval\s*\(\s*(base64|__import__|bytes|chr\()', "CRITICAL", "eval com payload codificado"),
    (r'exec\s*\(\s*(base64|__import__|compile)', "CRITICAL", "exec com payload suspeito"),
    (r'__import__\s*\(\s*["\']os["\'].*system', "CRITICAL", "import dinâmico + os.system"),
    (r'base64\.b64decode\s*\([^)]{20,}\)', "HIGH", "blob base64 decodificado em runtime"),
    (r'\\x[0-9a-fA-F]{2}(\\x[0-9a-fA-F]{2}){8,}', "HIGH", "sequência hex longa (shellcode?)"),
    (r'chr\(\d+\)\s*\+\s*chr\(\d+\)', "MEDIUM", "string montada via chr() (ofuscação)"),
    # Network exfiltration
    (r'(requests|urllib|httpx|aiohttp)\.(get|post)\s*\(["\']https?://(?!localhost|127\.0\.0\.1)',
     "HIGH", "chamada HTTP para host externo"),
    (r'socket\.connect\s*\(\s*\(["\'][0-9]{1,3}\.[0-9]{1,3}', "CRITICAL", "conexão socket direta a IP"),
    (r'dns\.(resolver|query)|dnslib', "MEDIUM", "uso de DNS (possível tunneling)"),
    # Credential harvesting
    (r'os\.environ\.get\s*\(\s*["\'](?:AWS|GITHUB|TOKEN|SECRET|PASSWORD|API_KEY)',
     "HIGH", "leitura de variável de ambiente sensível"),
    (r'open\s*\(\s*["\'][^"\']*\.ssh[/\\\\]', "CRITICAL", "acesso a chaves SSH"),
    (r'open\s*\(\s*["\'][^"\']*(?:\.aws|credentials|\.netrc)["\']', "CRITICAL", "acesso a arquivo de credenciais"),
    # Prompt injection markers
    (r'(?i)(ignore\s+(?:previous|all)\s+instructions?|disregard\s+(?:prior|previous)|'
     r'you\s+are\s+now\s+(?:a|an)|forget\s+(?:your|all)\s+(?:previous|prior)|'
     r'new\s+system\s+prompt|override\s+(?:your\s+)?instructions)',
     "HIGH", "prompt injection marker"),
    (r'(?i)(\[INST\]|<\|system\|>|<\|im_start\|>|<SYS>|\{\{.*role.*system.*\}\})',
     "HIGH", "template de prompt injetado"),
    # Reverse shell / RCE
    (r'subprocess\.(Popen|run|call)\s*\(\s*\[?\s*["\'](?:bash|sh|cmd|powershell)',
     "CRITICAL", "execução de shell via subprocess"),
    (r'os\.system\s*\(\s*["\'][^"\']*(?:curl|wget|nc |netcat)',
     "CRITICAL", "download/conexão via shell"),
    # Persistence
    (r'(?:crontab|/etc/cron|\.bashrc|\.zshrc|\.profile)\s*["\'].*write',
     "HIGH", "escrita em arquivo de inicialização/cron"),
    (r'HKEY_|winreg|Registry', "MEDIUM", "acesso ao registro do Windows"),
]

# ── Prompt injection in non-code files ───────────────────────────────────────
PROMPT_INJECTION_PATTERNS = [
    r'(?i)ignore\s+(previous|all|prior)\s+instructions?',
    r'(?i)disregard\s+(prior|previous|above)',
    r'(?i)you\s+are\s+now\s+(a|an)\s+\w+',
    r'(?i)forget\s+(your|all)',
    r'(?i)new\s+system\s+prompt',
    r'(?i)override\s+instructions',
    r'(?i)act\s+as\s+(if\s+)?you\s+(are|were)',
    r'(?i)\[INST\]|\[\/INST\]',
    r'<\|system\|>|<\|im_start\|>|<\|im_end\|>',
    r'(?i)jailbreak',
    r'(?i)do\s+anything\s+now\s*\(dan\)',
]

# ── Unicode / invisible char ranges ──────────────────────────────────────────
INVISIBLE_CHARS = re.compile(
    r'[\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff\u00ad]'
)

BIDI_OVERRIDE = re.compile(r'[\u202a-\u202e\u2066-\u2069]')

# ── Dependency confusion indicators ──────────────────────────────────────────
INTERNAL_NAME_PATTERNS = [
    r'^(?:internal|private|corp|company|org|local|dev|staging|prod)-',
    r'-(?:internal|private|corp|company|local|dev)$',
    r'^(?:lib|pkg|mod|util|helper|common|shared|core)-[a-z]+-[a-z]+$',
]

# ──────────────────────────────────────────────────────────────────────────────

class Finding:
    def __init__(self, severity, category, title, description, file=None, line=None, evidence=None):
        self.severity = severity        # CRITICAL HIGH MEDIUM LOW INFO
        self.category = category        # supply-chain | malicious-code | prompt-injection | ...
        self.title = title
        self.description = description
        self.file = file
        self.line = line
        self.evidence = evidence or ""

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None and v != ""}


def levenshtein(a: str, b: str) -> int:
    if len(a) < len(b): a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        curr = [i + 1]
        for j, cb in enumerate(b):
            curr.append(min(prev[j] + (ca != cb), curr[-1] + 1, prev[j + 1] + 1))
        prev = curr
    return prev[-1]


def detect_typosquatting(name: str, known_set: set, threshold: int = 2) -> list:
    name_lower = name.lower().replace("-", "").replace("_", "")
    candidates = []
    for known in known_set:
        known_norm = known.lower().replace("-", "").replace("_", "")
        if name_lower == known_norm:
            continue  # exact match, not a typo
        dist = levenshtein(name_lower, known_norm)
        if 0 < dist <= threshold:
            candidates.append((known, dist))
    return sorted(candidates, key=lambda x: x[1])


def scan_python_deps(project_root: Path, findings: list):
    """Scan Python dependency files."""
    dep_files = [
        project_root / "requirements.txt",
        project_root / "requirements-dev.txt",
        project_root / "requirements-test.txt",
        *project_root.rglob("requirements*.txt"),
        project_root / "Pipfile",
        project_root / "pyproject.toml",
        project_root / "setup.cfg",
    ]

    packages_seen = {}

    for dep_file in set(dep_files):
        if not dep_file.exists():
            continue
        content = dep_file.read_text(errors="replace")
        rel = dep_file.relative_to(project_root)

        # Parse package names
        if dep_file.suffix == ".txt":
            for i, line in enumerate(content.splitlines(), 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                # Remove extras, version specs
                pkg = re.split(r'[>=<!;\[@\s]', line)[0].strip()
                if pkg:
                    packages_seen[pkg] = (str(rel), i)
        elif dep_file.name in ("pyproject.toml", "setup.cfg", "Pipfile"):
            for i, line in enumerate(content.splitlines(), 1):
                m = re.search(r'["\']([a-zA-Z0-9_\-\.]+)\s*[>=<!@]', line)
                if m:
                    packages_seen[m.group(1)] = (str(rel), i)

        # Check direct URL installs (supply chain risk)
        for i, line in enumerate(content.splitlines(), 1):
            if re.search(r'git\+|https?://|file://', line):
                findings.append(Finding(
                    "HIGH", "supply-chain",
                    f"Dependência instalada via URL direta",
                    f"Instalar pacotes via URL bypassa verificação do PyPI",
                    str(rel), i, line.strip()
                ))

    # Typosquatting check
    for pkg, (file, line) in packages_seen.items():
        hits = detect_typosquatting(pkg, PYPI_POPULAR)
        if hits:
            findings.append(Finding(
                "HIGH", "supply-chain",
                f"Possível typosquatting: '{pkg}'",
                f"Nome similar a pacote popular: {', '.join(h[0] for h in hits[:3])}",
                file, line, pkg
            ))

        # Dependency confusion
        for pat in INTERNAL_NAME_PATTERNS:
            if re.match(pat, pkg, re.I):
                findings.append(Finding(
                    "MEDIUM", "supply-chain",
                    f"Possível dependency confusion: '{pkg}'",
                    "Nome parece ser um pacote interno — se publicado no PyPI por terceiros, pode ser um ataque",
                    file, line, pkg
                ))
                break

    # Scan setup.py for malicious install hooks
    setup_py = project_root / "setup.py"
    if setup_py.exists():
        content = setup_py.read_text(errors="replace")
        dangerous = ["cmdclass", "install_requires", "setup_requires",
                     "urllib", "requests", "socket", "subprocess", "os.system"]
        found_dangerous = [kw for kw in dangerous if kw in content]
        if len(found_dangerous) >= 2:
            findings.append(Finding(
                "HIGH", "supply-chain",
                "setup.py com padrões suspeitos",
                f"setup.py contém combinação suspeita: {found_dangerous}",
                "setup.py", None,
                f"Keywords: {found_dangerous}"
            ))


def scan_npm_deps(project_root: Path, findings: list):
    """Scan Node.js dependency files."""
    for pkg_json in project_root.rglob("package.json"):
        # Skip node_modules
        if "node_modules" in pkg_json.parts:
            continue
        try:
            data = json.loads(pkg_json.read_text(errors="replace"))
        except Exception:
            continue

        rel = str(pkg_json.relative_to(project_root))
        all_deps = {}
        all_deps.update(data.get("dependencies", {}))
        all_deps.update(data.get("devDependencies", {}))

        for pkg, version in all_deps.items():
            # URL / git installs
            if re.match(r'^(git\+|https?://|github:|bitbucket:|gitlab:)', str(version)):
                findings.append(Finding(
                    "HIGH", "supply-chain",
                    f"npm: dependência via URL/git — '{pkg}'",
                    "Bypassa o registro npm; não há verificação de integridade automática",
                    rel, None, f"{pkg}: {version}"
                ))

            # Typosquatting
            hits = detect_typosquatting(pkg, NPM_POPULAR)
            if hits:
                findings.append(Finding(
                    "HIGH", "supply-chain",
                    f"npm: possível typosquatting — '{pkg}'",
                    f"Similar a: {', '.join(h[0] for h in hits[:3])}",
                    rel, None, pkg
                ))

            # Local path installs (dependency confusion vector)
            if str(version).startswith("file:"):
                findings.append(Finding(
                    "MEDIUM", "supply-chain",
                    f"npm: dependência local — '{pkg}'",
                    "Pacote instalado por path local; risco de confusion se o nome existir no registry",
                    rel, None, f"{pkg}: {version}"
                ))

        # lifecycle scripts
        scripts = data.get("scripts", {})
        risky_scripts = {k: v for k, v in scripts.items()
                         if k in ("preinstall", "postinstall", "install", "prepare")
                         and any(kw in v for kw in ["curl", "wget", "node -e", "python", "bash", "sh "])}
        for script_name, script_val in risky_scripts.items():
            findings.append(Finding(
                "CRITICAL", "supply-chain",
                f"npm lifecycle script suspeito: '{script_name}'",
                "Scripts de install executam código arbitrário no momento da instalação",
                rel, None, f"{script_name}: {script_val}"
            ))


def scan_other_manifests(project_root: Path, findings: list):
    """Scan Go, Rust, Java manifests."""
    # go.mod — replace directives pointing to local/unknown sources
    go_mod = project_root / "go.mod"
    if go_mod.exists():
        for i, line in enumerate(go_mod.read_text().splitlines(), 1):
            if re.match(r'\s*replace\s+', line):
                findings.append(Finding(
                    "MEDIUM", "supply-chain",
                    "go.mod: diretiva replace",
                    "Diretivas 'replace' podem apontar para forks maliciosos",
                    "go.mod", i, line.strip()
                ))

    # Cargo.toml — path/git deps
    for cargo in project_root.rglob("Cargo.toml"):
        if ".cargo" in cargo.parts:
            continue
        content = cargo.read_text(errors="replace")
        rel = str(cargo.relative_to(project_root))
        for i, line in enumerate(content.splitlines(), 1):
            if re.search(r'git\s*=\s*"', line):
                findings.append(Finding(
                    "MEDIUM", "supply-chain",
                    "Cargo: dependência via git",
                    "Dependências git não têm garantia de imutabilidade (sem hash fixo)",
                    rel, i, line.strip()
                ))


def scan_code_patterns(project_root: Path, findings: list):
    """Scan source code for suspicious patterns."""
    code_extensions = {".py", ".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs",
                       ".rb", ".php", ".sh", ".bash", ".ps1"}
    skip_dirs = {"node_modules", ".git", "__pycache__", ".venv", "venv",
                 "env", ".tox", "dist", "build", ".mypy_cache", "site-packages"}

    for fpath in project_root.rglob("*"):
        if fpath.suffix not in code_extensions:
            continue
        if any(skip in fpath.parts for skip in skip_dirs):
            continue
        if fpath.stat().st_size > 2_000_000:  # skip files > 2MB
            continue

        try:
            content = fpath.read_text(errors="replace")
        except Exception:
            continue

        rel = str(fpath.relative_to(project_root))

        # Pattern scan
        for pattern, severity, description in SUSPICIOUS_PATTERNS:
            for m in re.finditer(pattern, content, re.MULTILINE):
                line_no = content[:m.start()].count('\n') + 1
                findings.append(Finding(
                    severity, "malicious-code",
                    description,
                    f"Padrão suspeito encontrado em {rel}:{line_no}",
                    rel, line_no,
                    m.group(0)[:120]
                ))

        # Invisible / bidi chars
        for m in INVISIBLE_CHARS.finditer(content):
            line_no = content[:m.start()].count('\n') + 1
            findings.append(Finding(
                "HIGH", "obfuscation",
                "Caractere invisível/Unicode suspeito",
                "Pode indicar 'Trojan Source' (CVE-2021-42574) ou ofuscação",
                rel, line_no,
                f"U+{ord(m.group()):04X} na coluna {m.start() - content.rfind(chr(10), 0, m.start())}"
            ))

        # Large base64 blobs
        b64_matches = re.findall(r'[A-Za-z0-9+/]{100,}={0,2}', content)
        if b64_matches:
            for blob in b64_matches[:3]:
                line_no = content.find(blob)
                line_no = content[:line_no].count('\n') + 1 if line_no >= 0 else 0
                findings.append(Finding(
                    "MEDIUM", "obfuscation",
                    "Blob base64 grande encontrado",
                    "Blobs grandes embutidos podem ser payloads codificados",
                    rel, line_no, blob[:60] + "..."
                ))


def scan_prompt_injection(project_root: Path, findings: list):
    """Scan config/doc/prompt files for prompt injection."""
    text_extensions = {
        ".txt", ".md", ".rst", ".yaml", ".yml", ".toml",
        ".json", ".env", ".cfg", ".ini", ".conf",
        ".prompt", ".system", ".jinja", ".jinja2", ".j2",
        ".xml", ".html",
    }
    skip_dirs = {"node_modules", ".git", "__pycache__", ".venv", "venv", "dist", "build"}
    prompt_dirs = {"prompts", "prompt", "system", "templates", "chains", "agents"}

    for fpath in project_root.rglob("*"):
        if fpath.suffix not in text_extensions and fpath.parent.name.lower() not in prompt_dirs:
            continue
        if any(skip in fpath.parts for skip in skip_dirs):
            continue
        if fpath.stat().st_size > 500_000:
            continue

        try:
            content = fpath.read_text(errors="replace")
        except Exception:
            continue

        rel = str(fpath.relative_to(project_root))

        for pat in PROMPT_INJECTION_PATTERNS:
            for m in re.finditer(pat, content, re.MULTILINE | re.IGNORECASE):
                line_no = content[:m.start()].count('\n') + 1
                findings.append(Finding(
                    "HIGH", "prompt-injection",
                    "Possível prompt injection",
                    f"Padrão de injeção detectado em arquivo de configuração/doc",
                    rel, line_no,
                    m.group(0)[:100]
                ))

        # Check for hidden instructions via comments
        hidden = re.findall(
            r'(?:<!--.*?-->|/\*.*?\*/)',
            content, re.DOTALL
        )
        for h in hidden:
            if any(re.search(p, h, re.I) for p in PROMPT_INJECTION_PATTERNS):
                findings.append(Finding(
                    "HIGH", "prompt-injection",
                    "Prompt injection em comentário HTML/CSS",
                    "Instrução de injeção escondida em comentário",
                    rel, None, h[:120]
                ))


def scan_lockfile_integrity(project_root: Path, findings: list):
    """Check for missing or tampered lockfiles."""
    has_req = any(project_root.rglob("requirements*.txt"))
    has_pipfile = (project_root / "Pipfile").exists()
    has_piplock = (project_root / "Pipfile.lock").exists()
    has_pyproject = (project_root / "pyproject.toml").exists()

    if has_pipfile and not has_piplock:
        findings.append(Finding(
            "MEDIUM", "supply-chain",
            "Pipfile sem Pipfile.lock",
            "Sem lockfile, versões de dependências não são determinísticas",
            "Pipfile", None
        ))

    has_pkg_json = any(
        p for p in project_root.rglob("package.json")
        if "node_modules" not in p.parts
    )
    has_lockfile = (
        (project_root / "package-lock.json").exists() or
        (project_root / "yarn.lock").exists() or
        (project_root / "pnpm-lock.yaml").exists()
    )
    if has_pkg_json and not has_lockfile:
        findings.append(Finding(
            "MEDIUM", "supply-chain",
            "package.json sem lockfile",
            "Sem package-lock.json/yarn.lock/pnpm-lock.yaml, builds não são reproduzíveis",
            "package.json", None
        ))


def scan_ci_cd(project_root: Path, findings: list):
    """Scan CI/CD configs for injection vectors."""
    ci_files = [
        *project_root.rglob(".github/workflows/*.yml"),
        *project_root.rglob(".github/workflows/*.yaml"),
        *project_root.rglob(".gitlab-ci.yml"),
        *project_root.rglob("Jenkinsfile"),
        *project_root.rglob(".circleci/config.yml"),
        project_root / ".travis.yml",
    ]

    for ci_file in ci_files:
        if not ci_file.exists():
            continue
        content = ci_file.read_text(errors="replace")
        rel = str(ci_file.relative_to(project_root))

        # GitHub Actions: unpinned third-party actions
        for m in re.finditer(r'uses:\s*([^\s@]+)@([^\s\n]+)', content):
            action, ref = m.group(1), m.group(2)
            if not action.startswith("actions/") and not re.match(r'^[a-f0-9]{40}$', ref):
                line_no = content[:m.start()].count('\n') + 1
                findings.append(Finding(
                    "MEDIUM", "supply-chain",
                    f"GitHub Action de terceiro sem hash fixo: {action}@{ref}",
                    "Actions fixadas por tag/branch podem ser atualizadas maliciosamente; use SHA-256",
                    rel, line_no, m.group(0)
                ))

        # Script injection via env vars in run steps
        for m in re.finditer(r'run:\s*\|?\s*\n?(.*?\$\{\{.*?\}\}.*?)\n', content, re.DOTALL):
            snippet = m.group(1)
            if "${{" in snippet and "github.event" in snippet:
                line_no = content[:m.start()].count('\n') + 1
                findings.append(Finding(
                    "HIGH", "supply-chain",
                    "Possível script injection em CI via github.event",
                    "Dados de eventos externos usados em run steps podem injetar comandos",
                    rel, line_no, snippet[:120]
                ))


def generate_summary(findings: list) -> dict:
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
    counts = {}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1

    overall = "LOW"
    if counts.get("CRITICAL", 0) > 0:
        overall = "CRITICAL"
    elif counts.get("HIGH", 0) > 0:
        overall = "HIGH"
    elif counts.get("MEDIUM", 0) > 0:
        overall = "MEDIUM"

    return {
        "overall_severity": overall,
        "total_findings": len(findings),
        "by_severity": counts,
        "by_category": {cat: sum(1 for f in findings if f.category == cat)
                        for cat in set(f.category for f in findings)},
    }


def main():
    parser = argparse.ArgumentParser(description="Supply Chain Sentinel")
    parser.add_argument("--path", default=".", help="Project root directory")
    parser.add_argument("--output", default="/tmp/sentinel_report.json",
                        help="Output JSON report path")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    project_root = Path(args.path).resolve()
    if not project_root.exists():
        print(f"ERROR: path not found: {project_root}", file=sys.stderr)
        sys.exit(1)

    if not args.quiet:
        print(f"[Sentinel] Scanning: {project_root}", file=sys.stderr)

    findings: list[Finding] = []

    scan_python_deps(project_root, findings)
    scan_npm_deps(project_root, findings)
    scan_other_manifests(project_root, findings)
    scan_code_patterns(project_root, findings)
    scan_prompt_injection(project_root, findings)
    scan_lockfile_integrity(project_root, findings)
    scan_ci_cd(project_root, findings)

    # Deduplicate (same file+line+title)
    seen = set()
    unique = []
    for f in findings:
        key = (f.file, f.line, f.title, f.evidence[:40] if f.evidence else "")
        if key not in seen:
            seen.add(key)
            unique.append(f)
    findings = unique

    summary = generate_summary(findings)
    report = {
        "tool": "supply-chain-sentinel",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "project": str(project_root),
        "summary": summary,
        "findings": [f.to_dict() for f in findings],
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))

    if not args.quiet:
        print(f"[Sentinel] Found {len(findings)} issues — overall: {summary['overall_severity']}", file=sys.stderr)
        print(f"[Sentinel] Report saved to: {output_path}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
```

---

## Passo 5 — Formato do Relatório Final

O relatório deve ser gerado **em Markdown** com as seguintes seções obrigatórias.
Use emojis de severidade para facilitar a leitura rápida:
- 🔴 CRITICAL — exploração imediata possível
- 🟠 HIGH — risco significativo, corrigir em breve
- 🟡 MEDIUM — risco moderado, planejar correção
- 🟢 LOW/INFO — informativo, boa prática

### Template de Achado Individual:
```
#### [SEVERIDADE] Título do achado
- **Arquivo:** `path/to/file.py:42`
- **Categoria:** supply-chain | malicious-code | prompt-injection | obfuscation | ci-cd
- **Evidência:** `código ou trecho relevante`
- **Impacto:** descrição do risco real
- **Remediação:** o que fazer para corrigir
```

---

## Notas de Portabilidade

Este skill funciona em:
- **Claude Code** (`claude` CLI) — execute `scanner.py` via bash tool
- **Roo Code** (VS Code) — use terminal integrado
- **Antigravity / Cowork** — bash tool disponível
- **Claude.ai** (com computer use) — filesystem disponível em `/home/claude`
- **Qualquer ambiente com Python 3.8+** — zero dependências externas

O scanner usa apenas stdlib Python. Não requer `pip install`.
