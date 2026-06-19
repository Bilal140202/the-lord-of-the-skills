# ⚙ Isengard

> *"Industry wakes the deep."*

---

**Domain:** Agents & Orchestration

**Keyword signatures:** `agent, subagent, orchestrat, workflow, delegation`


## 📊 Statistics

| Metric | Count |
|:---|---:|
| Total artifacts | 968 |
| Source repositories | 40 |
| Canonical (⭐) | 19 |
| Frameworks represented | 6 |

## ⚙ Frameworks

| Framework | Artifacts |
|:---|---:|
| claude-code | 920 |
| general | 37 |
| openhands | 4 |
| goose | 3 |
| continue | 2 |
| cline | 2 |

## 📁 Directory Layout

```
isengard/
├── <framework>/              ← e.g. claude-code, cursor, cline, aider
│   └── <source-repo>/        ← e.g. anthropics__skills
│       ├── SKILL.md          ← original skill file
│       ├── canonical__*.md   ← ⭐ canonical representative
│       └── ...               ← all variants preserved
└── ...
```

## 🚀 Usage

```bash
# Copy all Isengard skills for Claude Code
cp -r isengard/claude-code/*/* ~/.claude/skills/

# Copy only canonical ⭐ representatives
find isengard/ -name 'canonical__*' -exec cp {} ~/.claude/skills/ \;
```

---
*Part of [The Lord of the Skills](../README.md)*