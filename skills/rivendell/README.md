# ✦ Rivendell

> *"Knowledge flows from the Last Homely House."*

---

**Domain:** Research & Knowledge

**Keyword signatures:** `research, analyze, paper, methodology, synthesis`


## 📊 Statistics

| Metric | Count |
|:---|---:|
| Total artifacts | 1521 |
| Source repositories | 29 |
| Canonical (⭐) | 9 |
| Frameworks represented | 4 |

## ⚙ Frameworks

| Framework | Artifacts |
|:---|---:|
| claude-code | 1430 |
| general | 85 |
| cursor | 5 |
| continue | 1 |

## 📁 Directory Layout

```
rivendell/
├── <framework>/              ← e.g. claude-code, cursor, cline, aider
│   └── <source-repo>/        ← e.g. anthropics__skills
│       ├── SKILL.md          ← original skill file
│       ├── canonical__*.md   ← ⭐ canonical representative
│       └── ...               ← all variants preserved
└── ...
```

## 🚀 Usage

```bash
# Copy all Rivendell skills for Claude Code
cp -r rivendell/claude-code/*/* ~/.claude/skills/

# Copy only canonical ⭐ representatives
find rivendell/ -name 'canonical__*' -exec cp {} ~/.claude/skills/ \;
```

---
*Part of [The Lord of the Skills](../README.md)*