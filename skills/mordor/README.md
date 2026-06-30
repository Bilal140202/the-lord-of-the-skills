# 👁 Mordor

> *"One audit to rule them all."*

---

**Domain:** Security & Auditing

**Keyword signatures:** `security, vuln, owasp, xss, crypto, pentest`


## 📊 Statistics

| Metric | Count |
|:---|---:|
| Total artifacts | 406 |
| Source repositories | 94 |
| Canonical (⭐) | 9 |
| Frameworks represented | 7 |

## ⚙ Frameworks

| Framework | Artifacts |
|:---|---:|
| claude-code | 259 |
| general | 95 |
| antigravity | 36 |
| cursor | 11 |
| roo | 3 |
| openhands | 1 |
| continue | 1 |

## 📁 Directory Layout

```
mordor/
├── <framework>/              ← e.g. claude-code, cursor, cline, aider
│   └── <source-repo>/        ← e.g. anthropics__skills
│       ├── SKILL.md          ← original skill file
│       ├── canonical__*.md   ← ⭐ canonical representative
│       └── ...               ← all variants preserved
└── ...
```

## 🚀 Usage

```bash
# Copy all Mordor skills for Claude Code
cp -r mordor/claude-code/*/* ~/.claude/skills/

# Copy only canonical ⭐ representatives
find mordor/ -name 'canonical__*' -exec cp {} ~/.claude/skills/ \;
```

---
*Part of [The Lord of the Skills](../README.md)*