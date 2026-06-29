# 📋 MANIFEST.md — *The Record of Artifacts*

> Documentation for `_manifest.json` — the machine-readable heart of the compilation.

---

## 📄 What is `_manifest.json`?

`_manifest.json` is the **machine-readable manifest** of every artifact in the compilation. It's the single source of truth used by:
- The Excel index generator
- The PDF catalog generator
- The package builder
- External tools that want to query the compilation programmatically

---

## 🗂 Location

The full manifest lives at:
- **In this repo**: `docs/_manifest.json` (truncated, sample only)
- **In the source build**: `/home/z/my-project/the-lord-of-the-skills/_cache/manifest_final.json` (full)

> **Note**: The full manifest is **~70 MB** (18,142 entries with metadata) and is NOT committed to git. To get the full manifest, either:
> 1. Run the crawler yourself: `python3 crawler/crawler.py`
> 2. Download it from the [latest release artifacts](https://github.com/Bilal140202/the-lord-of-the-skills/releases)

---

## 📐 Schema

The manifest is a JSON object with this top-level structure:

```json
{
  "generated_at": "2026-06-19T07:08:40Z",
  "classified_at": "2026-06-19T07:09:00Z",
  "dedup_at": "2026-06-19T07:09:30Z",
  "total_discovered_repos": 2928,
  "total_cloned_repos": 307,
  "total_extracted_files": 18142,
  "frameworks_detected": ["aider", "antigravity", "claude-code", ...],
  "kingdom_distribution": {"gondor": 10141, "rivendell": 1776, ...},
  "skill_type_distribution": {"execution": 6944, "verification": 1393, ...},
  "dedup_stats": {
    "total_clusters": 1880,
    "multi_clusters": 1880,
    "canonical_count": 357,
    "cluster_size_distribution": {"2": 362, "3": 865, ...}
  },
  "files": [
    {
      "source_repo": "anthropics/skills",
      "framework": "claude-code",
      "kingdom": "gondor",
      "kingdom_label": "Coding & Software Engineering",
      "kingdom_motto": "Gondor sees, Gondor codes.",
      "skill_type": "execution",
      "original_path": "skill-creator/SKILL.md",
      "filename": "SKILL.md",
      "extracted_path": "_raw/claude-code/anthropics__skills/skill-creator__SKILL.md",
      "title": "Skill Creator",
      "summary": "A skill for creating new skills and iteratively improving them...",
      "size_bytes": 4523,
      "line_count": 187,
      "cluster_id": "cluster_0042",
      "cluster_size": 5,
      "canonical": true,
      "see_also": [
        "_raw/claude-code/wshobson__agents/SKILL.md",
        "_raw/claude-code/davepoon__buildwithclaude/SKILL.md",
        ...
      ],
      "retrieved_at": "2026-06-19T05:01:42Z"
    },
    ...
  ]
}
```

---

## 📊 Field Reference

### Top-Level Fields

| Field | Type | Description |
|:---|:---|:---|
| `generated_at` | string (ISO 8601) | When the crawler ran |
| `classified_at` | string (ISO 8601) | When the classifier ran |
| `dedup_at` | string (ISO 8601) | When the dedup pass ran |
| `total_discovered_repos` | integer | Total repos found via seeds + BFS + search |
| `total_cloned_repos` | integer | Repos successfully cloned |
| `total_extracted_files` | integer | Total skill files extracted |
| `frameworks_detected` | string[] | List of frameworks present |
| `kingdom_distribution` | object | Map of kingdom → file count |
| `skill_type_distribution` | object | Map of skill type → file count |
| `dedup_stats` | object | Deduplication statistics |
| `files` | object[] | Array of file records (see below) |

### Per-File Fields

| Field | Type | Description |
|:---|:---|:---|
| `source_repo` | string | `owner/repo` of source GitHub repository |
| `framework` | string | Detected framework (claude-code, cursor, cline, etc.) |
| `kingdom` | string | LOTR kingdom (gondor, rivendell, moria, etc.) |
| `kingdom_label` | string | Human-readable kingdom domain |
| `kingdom_motto` | string | LOTR-themed kingdom motto |
| `skill_type` | string | Functional type (planning, execution, verification, etc.) |
| `original_path` | string | Path of the file within the source repo |
| `filename` | string | Just the filename |
| `extracted_path` | string | Where the file lives in the local build (not in repo) |
| `title` | string | Extracted from frontmatter or first H1 |
| `summary` | string | First substantive paragraph (max 220 chars) |
| `size_bytes` | integer | File size in bytes |
| `line_count` | integer | Number of lines |
| `cluster_id` | string | ID of the dedup cluster this file belongs to |
| `cluster_size` | integer | Number of files in this cluster |
| `canonical` | boolean | `true` if this is the ⭐ canonical representative |
| `see_also` | string[] | Paths of other files in the same cluster |
| `retrieved_at` | string (ISO 8601) | When this file was extracted |

---

## 🛠 Programmatic Usage

### Python

```python
import json

with open("_manifest.json") as f:
    manifest = json.load(f)

# Get all canonical skills
canonical = [f for f in manifest["files"] if f["canonical"]]
print(f"Canonical skills: {len(canonical)}")

# Get all Claude Code skills in Gondor
gondor_cc = [f for f in manifest["files"]
             if f["kingdom"] == "gondor"
             and f["framework"] == "claude-code"]
print(f"Gondor Claude Code skills: {len(gondor_cc)}")

# Get all skills from a specific source repo
anthropics = [f for f in manifest["files"]
              if f["source_repo"] == "anthropics/skills"]
print(f"anthropics/skills files: {len(anthropics)}")

# Get kingdom distribution
for kingdom, count in sorted(manifest["kingdom_distribution"].items(),
                              key=lambda x: -x[1]):
    print(f"  {kingdom:12s}: {count}")
```

### JavaScript / Node.js

```javascript
const manifest = require('./_manifest.json');

// All canonical skills
const canonical = manifest.files.filter(f => f.canonical);
console.log(`Canonical skills: ${canonical.length}`);

// All Cursor rules in Mordor (security)
const mordorCursor = manifest.files.filter(f =>
  f.kingdom === 'mordor' && f.framework === 'cursor'
);
console.log(`Mordor Cursor rules: ${mordorCursor.length}`);
```

### jq (Command Line)

```bash
# All canonical skills (titles only)
jq '.files[] | select(.canonical) | .title' _manifest.json

# Count of skills per kingdom
jq '.kingdom_distribution' _manifest.json

# All skills from anthropics/skills
jq '.files[] | select(.source_repo == "anthropics/skills") | {title, kingdom, framework}' _manifest.json

# Top 10 source repos by file count
jq -r '.files | group_by(.source_repo) | map({repo: .[0].source_repo, count: length}) | sort_by(-.count) | .[:10] | .[] | "\(.count)\t\(.repo)"' _manifest.json
```

---

## 🔄 Updating the Manifest

The manifest is regenerated every time the crawler runs. To update:

```bash
cd crawler/
python3 crawler.py           # Re-spider GitHub
python3 classify.py          # Re-classify
python3 dedup.py             # Re-dedup
# manifest_final.json now contains the updated manifest
```

For a one-shot refresh:

```bash
bash crawler/refresh_lord_of_skills.sh
```

---

## 📈 Manifest Size

| Version | Files | Manifest Size |
|:---|---:|---:|
| v1.0.0 | 10,888 | ~42 MB |
| v1.1.0 | 10,888 | ~42 MB |
| v1.2.0 | 18,142 | ~70 MB |

---

<div align="center">

*The manifest knows all, sees all, binds all.*

</div>
