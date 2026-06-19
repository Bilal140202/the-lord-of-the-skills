# 🐴 Rohan

> *"Ride now, ride to verify."*

---

**Domain:** Testing & Verification

**Keyword signatures:** `test, verify, assert, coverage, lint, typecheck`


## 📊 Statistics

| Metric | Count |
|:---|---:|
| Total artifacts | 450 |
| Source repositories | 35 |
| Canonical (⭐) | 4 |
| Frameworks represented | 6 |

## ⚙ Frameworks

| Framework | Artifacts |
|:---|---:|
| claude-code | 362 |
| general | 64 |
| cursor | 21 |
| continue | 1 |
| cline | 1 |
| roo | 1 |

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