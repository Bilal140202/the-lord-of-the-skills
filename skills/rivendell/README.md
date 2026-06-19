# ✦ Rivendell

> *"Knowledge flows from the Last Homely House."*

---

**Domain:** Research & Knowledge

**Keyword signatures:** `research, analyze, paper, methodology, synthesis`


## 📊 Statistics

| Metric | Count |
|:---|---:|
| Total artifacts | 1776 |
| Source repositories | 109 |
| Canonical (⭐) | 30 |
| Frameworks represented | 7 |

## ⚙ Frameworks

| Framework | Artifacts |
|:---|---:|
| claude-code | 1475 |
| general | 197 |
| antigravity | 89 |
| cursor | 6 |
| roo | 6 |
| continue | 2 |
| codex | 1 |

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