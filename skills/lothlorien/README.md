# ✿ Lothlórien

> *"Where data roots run deep."*

---

**Domain:** Data & Analysis

**Keyword signatures:** `data, etl, pandas, ml, statistics, visualization`


## 📊 Statistics

| Metric | Count |
|:---|---:|
| Total artifacts | 496 |
| Source repositories | 91 |
| Canonical (⭐) | 13 |
| Frameworks represented | 9 |

## ⚙ Frameworks

| Framework | Artifacts |
|:---|---:|
| claude-code | 293 |
| general | 99 |
| antigravity | 84 |
| cursor | 12 |
| roo | 3 |
| continue | 2 |
| goose | 1 |
| copilot | 1 |
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