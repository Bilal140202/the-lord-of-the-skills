# ✎ The Shire

> *"Quiet writing, deep roots."*

---

**Domain:** Writing & Content

**Keyword signatures:** `writing, blog, docs, readme, marketing`


## 📊 Statistics

| Metric | Count |
|:---|---:|
| Total artifacts | 1272 |
| Source repositories | 168 |
| Canonical (⭐) | 22 |
| Frameworks represented | 10 |

## ⚙ Frameworks

| Framework | Artifacts |
|:---|---:|
| claude-code | 691 |
| antigravity | 263 |
| general | 261 |
| cursor | 26 |
| roo | 14 |
| continue | 7 |
| codex | 4 |
| cline | 4 |
| goose | 1 |
| copilot | 1 |

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