# 👁 Mordor

> *"One audit to rule them all."*

---

**Domain:** Security & Auditing

**Keyword signatures:** `security, vuln, owasp, xss, crypto, pentest`


## 📊 Statistics

| Metric | Count |
|:---|---:|
| Total artifacts | 272 |
| Source repositories | 22 |
| Canonical (⭐) | 5 |
| Frameworks represented | 5 |

## ⚙ Frameworks

| Framework | Artifacts |
|:---|---:|
| claude-code | 226 |
| general | 38 |
| cursor | 6 |
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