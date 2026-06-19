# 🕸 Mirkwood

> *"Strange paths through the wood."*

---

**Domain:** Specialized & Niche

**Keyword signatures:** `specialized, niche, experimental, esoteric`


## 📊 Statistics

| Metric | Count |
|:---|---:|
| Total artifacts | 4 |
| Source repositories | 4 |
| Canonical (⭐) | 1 |
| Frameworks represented | 4 |

## ⚙ Frameworks

| Framework | Artifacts |
|:---|---:|
| goose | 1 |
| general | 1 |
| continue | 1 |
| cline | 1 |

## 📁 Directory Layout

```
mirkwood/
├── <framework>/              ← e.g. claude-code, cursor, cline, aider
│   └── <source-repo>/        ← e.g. anthropics__skills
│       ├── SKILL.md          ← original skill file
│       ├── canonical__*.md   ← ⭐ canonical representative
│       └── ...               ← all variants preserved
└── ...
```

## 🚀 Usage

```bash
# Copy all Mirkwood skills for Claude Code
cp -r mirkwood/claude-code/*/* ~/.claude/skills/

# Copy only canonical ⭐ representatives
find mirkwood/ -name 'canonical__*' -exec cp {} ~/.claude/skills/ \;
```

---
*Part of [The Lord of the Skills](../README.md)*