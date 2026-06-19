# 🌳 Fangorn

> *"The old forest remembers."*

---

**Domain:** Documentation & Memory

**Keyword signatures:** `memory, context, rag, embedding, knowledge base`


## 📊 Statistics

| Metric | Count |
|:---|---:|
| Total artifacts | 708 |
| Source repositories | 148 |
| Canonical (⭐) | 15 |
| Frameworks represented | 8 |

## ⚙ Frameworks

| Framework | Artifacts |
|:---|---:|
| claude-code | 304 |
| general | 206 |
| antigravity | 156 |
| cursor | 17 |
| codex | 10 |
| roo | 10 |
| goose | 3 |
| openhands | 2 |

## 📁 Directory Layout

```
fangorn/
├── <framework>/              ← e.g. claude-code, cursor, cline, aider
│   └── <source-repo>/        ← e.g. anthropics__skills
│       ├── SKILL.md          ← original skill file
│       ├── canonical__*.md   ← ⭐ canonical representative
│       └── ...               ← all variants preserved
└── ...
```

## 🚀 Usage

```bash
# Copy all Fangorn skills for Claude Code
cp -r fangorn/claude-code/*/* ~/.claude/skills/

# Copy only canonical ⭐ representatives
find fangorn/ -name 'canonical__*' -exec cp {} ~/.claude/skills/ \;
```

---
*Part of [The Lord of the Skills](../README.md)*