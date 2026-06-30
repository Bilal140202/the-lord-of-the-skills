# 🐴 Rohan

> *"Ride now, ride to verify."*

---

**Domain:** Testing & Verification

**Keyword signatures:** `test, verify, assert, coverage, lint, typecheck`


## 📊 Statistics

| Metric | Count |
|:---|---:|
| Total artifacts | 718 |
| Source repositories | 129 |
| Canonical (⭐) | 20 |
| Frameworks represented | 8 |

## ⚙ Frameworks

| Framework | Artifacts |
|:---|---:|
| claude-code | 399 |
| general | 191 |
| antigravity | 79 |
| cursor | 40 |
| codex | 4 |
| roo | 3 |
| continue | 1 |
| cline | 1 |

## 📁 Directory Layout

```
rohan/
├── <framework>/              ← e.g. claude-code, cursor, cline, aider
│   └── <source-repo>/        ← e.g. anthropics__skills
│       ├── SKILL.md          ← original skill file
│       ├── canonical__*.md   ← ⭐ canonical representative
│       └── ...               ← all variants preserved
└── ...
```

## 🚀 Usage

```bash
# Copy all Rohan skills for Claude Code
cp -r rohan/claude-code/*/* ~/.claude/skills/

# Copy only canonical ⭐ representatives
find rohan/ -name 'canonical__*' -exec cp {} ~/.claude/skills/ \;
```

---
*Part of [The Lord of the Skills](../README.md)*