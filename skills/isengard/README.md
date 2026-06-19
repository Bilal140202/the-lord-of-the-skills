# ⚙ Isengard

> *"Industry wakes the deep."*

---

**Domain:** Agents & Orchestration

**Keyword signatures:** `agent, subagent, orchestrat, workflow, delegation`


## 📊 Statistics

| Metric | Count |
|:---|---:|
| Total artifacts | 1630 |
| Source repositories | 173 |
| Canonical (⭐) | 19 |
| Frameworks represented | 10 |

## ⚙ Frameworks

| Framework | Artifacts |
|:---|---:|
| claude-code | 1090 |
| antigravity | 307 |
| general | 215 |
| openhands | 4 |
| codex | 4 |
| goose | 3 |
| continue | 2 |
| cline | 2 |
| roo | 2 |
| cursor | 1 |

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