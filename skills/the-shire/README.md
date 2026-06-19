# ✎ The Shire

> *"Quiet writing, deep roots."*

---

**Domain:** Writing & Content

**Keyword signatures:** `writing, blog, docs, readme, marketing`


## 📊 Statistics

| Metric | Count |
|:---|---:|
| Total artifacts | 712 |
| Source repositories | 41 |
| Canonical (⭐) | 22 |
| Frameworks represented | 8 |

## ⚙ Frameworks

| Framework | Artifacts |
|:---|---:|
| claude-code | 619 |
| general | 67 |
| cursor | 17 |
| continue | 5 |
| codex | 1 |
| goose | 1 |
| cline | 1 |
| roo | 1 |

## 📁 Directory Layout

```
the-shire/
├── <framework>/              ← e.g. claude-code, cursor, cline, aider
│   └── <source-repo>/        ← e.g. anthropics__skills
│       ├── SKILL.md          ← original skill file
│       ├── canonical__*.md   ← ⭐ canonical representative
│       └── ...               ← all variants preserved
└── ...
```

## 🚀 Usage

```bash
# Copy all The Shire skills for Claude Code
cp -r the-shire/claude-code/*/* ~/.claude/skills/

# Copy only canonical ⭐ representatives
find the-shire/ -name 'canonical__*' -exec cp {} ~/.claude/skills/ \;
```

---
*Part of [The Lord of the Skills](../README.md)*