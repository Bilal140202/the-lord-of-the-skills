# ⚔ Gondor

> *"Gondor sees, Gondor codes."*

---

**Domain:** Coding & Software Engineering

**Keyword signatures:** `coding, refactor, debug, git, typescript, react, api, build`


## 📊 Statistics

| Metric | Count |
|:---|---:|
| Total artifacts | 10141 |
| Source repositories | 544 |
| Canonical (⭐) | 188 |
| Frameworks represented | 14 |

## ⚙ Frameworks

| Framework | Artifacts |
|:---|---:|
| claude-code | 4798 |
| general | 2464 |
| antigravity | 2007 |
| cursor | 566 |
| codex | 144 |
| roo | 59 |
| continue | 35 |
| cline | 24 |
| openhands | 18 |
| copilot | 11 |
| aider | 8 |
| goose | 4 |
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