# ✨ DEDUP.md — *The Canonical Quest*

> How The Lord of the Skills identifies the **one best representative** of each concept across 18,000+ files.

---

## 🎯 Why Dedup?

Many skills overlap across frameworks. For example, the concept of "git-commit" exists as:
- `SKILL.md` in 12 different Claude Code repos
- `.cursorrules` in 8 Cursor repos
- `.clinerules/git-commit.md` in 5 Cline repos
- `CONVENTIONS.md` (mentioning git commits) in 3 Aider repos

That's **28 files for one concept**. Without dedup, your `~/.claude/skills/` directory would be flooded with duplicates.

The Lord of the Skills identifies these clusters and marks **one file as canonical ⭐** — the best representative of the concept.

---

## 📊 Stats

| Metric | Count |
|:---|---:|
| Total artifacts | 18,142 |
| Total clusters | 1,880 |
| Multi-file clusters | 1,880 |
| Canonical ⭐ representatives | 357 |
| Largest cluster | 671 files (all `SKILL.md` with no distinguishing title) |
| Median cluster size | 3 files |

---

## 🔄 The Dedup Process

The dedup pass runs in `crawler/dedup.py` and has 4 steps:

### Step 1: Normalize Titles

Each file's title (extracted from frontmatter or first H1) is normalized:
- Lowercased
- Punctuation stripped
- Whitespace normalized

Normalization is performed before any clustering occurs to ensure we aren't splitting identical concepts due to case or punctuation differences.

```python
"Git Commit Skill" → "git commit skill"
"git-commit-skill" → "git commit skill"
"Git Commit Skill!" → "git commit skill"
```

### Step 2: Cluster by Exact Title Match

Files with the same normalized title are grouped into a cluster:

```
Cluster "skill":
  - anthropics/skills:SKILL.md
  - wshobson/agents:SKILL.md
  - davepoon/buildwithclaude:SKILL.md
  - ... (8 more)

Cluster "git commit":
  - repo-A:skills/git-commit.md
  - repo-B:skills/git-commit.md
  - repo-C:.clinerules/git-commit.md
  - ...
```

### Step 3: Jaccard Similarity for Singletons

Files that didn't match by exact title are compared by **summary similarity**:
- Tokenize each file's summary (first substantive paragraph). A and B represent the set of words in the summaries.
- Compute Jaccard similarity: `|A ∩ B| / |A ∪ B|`
- If similarity ≥ 0.7, group them into a cluster

```python
def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)
```

### Step 4: Pick the Canonical ⭐

Within each cluster, the canonical file is chosen by a **score**:

```python
def canonical_score(rec: dict) -> float:
    score = 0.0
    # Framework priority (Claude Code > Codex > OpenHands > ...)
    score += FRAMEWORK_PRIORITY[rec["framework"]] * 10
    # Skill type priority (conventions > orchestration > planning > ...)
    score += SKILL_TYPE_PRIORITY[rec["skill_type"]] * 5
    # File size (longer = richer = preferred, capped at 50KB)
    score += min(rec["size_bytes"] / 1024, 50)
    # Well-known filename bonus
    if rec["filename"] in {"SKILL.md", "AGENTS.md", "CONVENTIONS.md", ...}:
        score += 20
    return score
```

The file with the highest score wins ⭐.

---

## 🏆 Framework Priority

```
1. claude-code   (10 points × 10 = 100)
2. codex         ( 9 points × 10 =  90)
3. openhands     ( 8 points × 10 =  80)
4. cursor        ( 7 points × 10 =  70)
5. cline         ( 6 points × 10 =  60)
6. roo           ( 6 points × 10 =  60)
7. aider         ( 5 points × 10 =  50)
8. autogen       ( 5 points × 10 =  50)
9. crewai        ( 5 points × 10 =  50)
10. langgraph    ( 5 points × 10 =  50)
11. general      ( 4 points × 10 =  40)
12. continue     ( 3 points × 10 =  30)
13. goose        ( 3 points × 10 =  30)
14. copilot      ( 3 points × 10 =  30)
```

**Rationale**: Claude Code skills are the most structured and well-documented format, so they're preferred as canonical references. Codex `AGENTS.md` is the emerging industry standard. OpenHands is well-curated. The rest follow.

---

## 🎯 Skill Type Priority

```
1. conventions    (10 points × 5 = 50)  — Coding standards, best practices
2. orchestration  ( 9 points × 5 = 45)  — Multi-agent orchestration
3. planning       ( 8 points × 5 = 40)  — Task planning, decomposition
4. execution      ( 7 points × 5 = 35)  — Task execution
5. tools          ( 6 points × 5 = 30)  — Tool usage, MCP
6. verification   ( 6 points × 5 = 30)  — Testing, verification
7. memory         ( 5 points × 5 = 25)  — Memory, context, RAG
8. prompts        ( 4 points × 5 = 20)  — Prompt templates
9. other          ( 1 point  × 5 =  5)  — Unclassified
```

**Rationale**: Conventions and orchestration skills are the most reusable. "Other" skills are often one-off or experimental.

---

## 📁 Filename Bonus

These canonical filenames get **+20 bonus points**:
- `SKILL.md`
- `AGENTS.md`
- `CONVENTIONS.md`
- `.cursorrules`
- `copilot-instructions.md`
- `CLAUDE.md`

**Rationale**: Files with these names are by definition the "main" file of their repo, so they're more likely to be high-quality.

---

## 📊 Cluster Size Distribution

| Cluster Size | Count | Interpretation |
|:---|---:|:---|
| 2 | 362 | Two very similar files |
| 3 | 865 | Three variants of one concept |
| 4 | 389 | Four variants |
| 5 | 90 | Five variants |
| 6 | 96 | Six variants |
| 7 | 25 | Seven variants |
| 8 | 24 | Eight variants |
| 9 | 10 | Nine variants |
| 10+ | 11 | Many variants |
| 671 | 1 | All `SKILL.md` files with no distinguishing title |

---

## 🛠 Using Canonical Skills

### Copy only canonical skills

```bash
# All canonical skills (357 files)
find skills/ -name 'canonical__*' -exec cp {} ~/.claude/skills/ \;
```

### Per-kingdom canonical skills

```bash
# Only canonical Gondor (coding) skills
find skills/gondor/ -name 'canonical__*' -exec cp {} ~/.claude/skills/ \;

# Only canonical Mordor (security) skills
find skills/mordor/ -name 'canonical__*' -exec cp {} ~/.claude/skills/ \;
```

### Programmatic access

```python
import json
manifest = json.load(open("_manifest.json"))
canonical = [f for f in manifest["files"] if f["canonical"]]
print(f"Canonical skills: {len(canonical)}")
for f in canonical[:10]:
    print(f"  ⭐ {f['title']} ({f['kingdom']}/{f['framework']})")
```

---

## 🐛 Known Limitations

1. **Title-based clustering is conservative** — Files with different titles but similar content won't cluster. The Jaccard pass catches some of these, but not all.

2. **The 671-file "skill" cluster** — Many repos have `SKILL.md` without a frontmatter title or H1. They all get the title "skill" and cluster together. The canonical is the largest Claude Code SKILL.md.

3. **Framework priority bias** — Claude Code skills are preferred as canonical. If a Cursor rule is genuinely better, it won't be chosen as canonical. This is intentional (Claude Code format is the most structured) but worth knowing.

4. **No semantic similarity** — We use Jaccard on word sets, not embeddings. Two skills saying the same thing in different words won't cluster. Future work: add sentence-transformer embeddings.

---

## 🚀 Future Improvements

- [ ] **Embeddings-based similarity** — Use sentence-transformers for semantic clustering
- [ ] **Quality scoring** — Incorporate upstream repo stars, recency, license clarity
- [ ] **Multi-canonical** — Allow 2-3 canonicals per cluster (one per framework)
- [ ] **Manual curation** — Allow maintainers to override canonical selection

---

## 📖 See Also

- [`crawler/dedup.py`](crawler/dedup.py) — The implementation
- [`MANIFEST.md`](MANIFEST.md) — Full manifest schema (including `canonical`, `cluster_id`, `cluster_size` fields)
- [`FAQ.md`](FAQ.md) — Common questions about dedup

---

<div align="center">

*One skill to rule them all, one skill to find them, one skill to bring them all, and in the darkness bind them.*

</div>
