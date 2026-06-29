# ⛏ Moria

> *"Speak, friend, and enter the deploy."*

---

**Domain:** DevOps & Infrastructure

**Keyword signatures:** `devops, kubernetes, docker, terraform, aws, ci/cd`


## 📊 Statistics

| Metric | Count |
|:---|---:|
| Total artifacts | 914 |
| Source repositories | 107 |
| Canonical (⭐) | 40 |
| Frameworks represented | 10 |

## ⚙ Frameworks

| Framework | Artifacts |
|:---|---:|
| claude-code | 564 |
| general | 226 |
| antigravity | 83 |
| cursor | 29 |
| codex | 3 |
| roo | 3 |
| openhands | 2 |
| continue | 2 |
| copilot | 1 |
| cline | 1 |

## 📁 Directory Layout

```
moria/
├── <framework>/              ← e.g. claude-code, cursor, cline, aider
│   └── <source-repo>/        ← e.g. anthropics__skills
│       ├── SKILL.md          ← original skill file
│       ├── canonical__*.md   ← ⭐ canonical representative
│       └── ...               ← all variants preserved
└── ...
```

## 🚀 Usage

```bash
# Copy all Moria skills for Claude Code
cp -r moria/claude-code/*/* ~/.claude/skills/

# Copy only canonical ⭐ representatives
find moria/ -name 'canonical__*' -exec cp {} ~/.claude/skills/ \;
```

---
*Part of [The Lord of the Skills](../README.md)*