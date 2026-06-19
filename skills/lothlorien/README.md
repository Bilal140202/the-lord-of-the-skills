# ✿ Lothlórien

> *"Where data roots run deep."*

---

**Domain:** Data & Analysis

**Keyword signatures:** `data, etl, pandas, ml, statistics, visualization`


## 📊 Statistics

| Metric | Count |
|:---|---:|
| Total artifacts | 305 |
| Source repositories | 23 |
| Canonical (⭐) | 5 |
| Frameworks represented | 6 |

## ⚙ Frameworks

| Framework | Artifacts |
|:---|---:|
| claude-code | 259 |
| general | 36 |
| cursor | 7 |
| goose | 1 |
| continue | 1 |
| cline | 1 |

## 📁 Directory Layout

```
lothlorien/
├── <framework>/              ← e.g. claude-code, cursor, cline, aider
│   └── <source-repo>/        ← e.g. anthropics__skills
│       ├── SKILL.md          ← original skill file
│       ├── canonical__*.md   ← ⭐ canonical representative
│       └── ...               ← all variants preserved
└── ...
```

## 🚀 Usage

```bash
# Copy all Lothlórien skills for Claude Code
cp -r lothlorien/claude-code/*/* ~/.claude/skills/

# Copy only canonical ⭐ representatives
find lothlorien/ -name 'canonical__*' -exec cp {} ~/.claude/skills/ \;
```

---
*Part of [The Lord of the Skills](../README.md)*