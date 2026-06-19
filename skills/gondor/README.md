# ⚔ Gondor

> *"Gondor sees, Gondor codes."*

---

**Domain:** Coding & Software Engineering

**Keyword signatures:** `coding, refactor, debug, git, typescript, react, api, build`


## 📊 Statistics

| Metric | Count |
|:---|---:|
| Total artifacts | 5631 |
| Source repositories | 126 |
| Canonical (⭐) | 188 |
| Frameworks represented | 13 |

## ⚙ Frameworks

| Framework | Artifacts |
|:---|---:|
| claude-code | 4352 |
| general | 654 |
| cursor | 475 |
| codex | 71 |
| continue | 28 |
| openhands | 18 |
| cline | 16 |
| roo | 5 |
| goose | 4 |
| copilot | 3 |
| aider | 2 |
| crewai | 2 |
| langgraph | 1 |

## 📁 Directory Layout

```
gondor/
├── <framework>/              ← e.g. claude-code, cursor, cline, aider
│   └── <source-repo>/        ← e.g. anthropics__skills
│       ├── SKILL.md          ← original skill file
│       ├── canonical__*.md   ← ⭐ canonical representative
│       └── ...               ← all variants preserved
└── ...
```

## 🚀 Usage

```bash
# Copy all Gondor skills for Claude Code
cp -r gondor/claude-code/*/* ~/.claude/skills/

# Copy only canonical ⭐ representatives
find gondor/ -name 'canonical__*' -exec cp {} ~/.claude/skills/ \;
```

---
*Part of [The Lord of the Skills](../README.md)*