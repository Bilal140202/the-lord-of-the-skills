#!/usr/bin/env python3
"""
The Lord of the Skills — Dedup + Canonical Marking
===================================================
Reads _cache/manifest_classified.json.
Clusters skills by:
  - normalized title (lowercased, punctuation stripped)
  - similarity of summary (Jaccard on word sets, threshold 0.6)
Within each cluster of size > 1, picks one "canonical" file using a score:
  + repo stars (when known)
  + file size (longer = richer = preferred)
  + skill_type clarity (prefer conventions / orchestration over 'other')
  + framework preference (claude-code > cursor > others, as canonical reference)
Writes _cache/manifest_final.json with each record augmented:
  {canonical: bool, cluster_id: str, cluster_size: int,
   canonical_for_cluster: bool, see_also: [paths]}
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime, timezone

ROOT = Path("/home/z/my-project/the-lord-of-the-skills")
IN_PATH = ROOT / "_cache" / "manifest_classified.json"
OUT_PATH = ROOT / "_cache" / "manifest_final.json"

def normalize_title(t: str) -> str:
    t = t.lower()
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def tokenize(s: str) -> set[str]:
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return set(s.split()) - {"the", "a", "an", "of", "for", "and", "to", "in",
                            "on", "with", "your", "is", "are", "this", "that"}

def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)

# Framework preference for "canonical reference implementation"
FRAMEWORK_PRIORITY = {
    "claude-code": 10,
    "codex": 9,
    "openhands": 8,
    "cursor": 7,
    "cline": 6,
    "roo": 6,
    "aider": 5,
    "general": 4,
    "continue": 3,
    "goose": 3,
    "copilot": 3,
    "autogen": 5,
    "crewai": 5,
    "langgraph": 5,
    "swe-agent": 5,
}

SKILL_TYPE_PRIORITY = {
    "conventions": 10,
    "orchestration": 9,
    "planning": 8,
    "execution": 7,
    "tools": 6,
    "verification": 6,
    "memory": 5,
    "prompts": 4,
    "other": 1,
}

def canonical_score(rec: dict) -> float:
    """Higher is better."""
    score = 0.0
    score += FRAMEWORK_PRIORITY.get(rec["framework"], 0) * 10
    score += SKILL_TYPE_PRIORITY.get(rec["skill_type"], 0) * 5
    # size in KB, capped
    size_kb = rec.get("size_bytes", 0) / 1024
    score += min(size_kb, 50)  # cap at 50 points
    # filename bonus: well-known canonical filenames
    fn = rec.get("filename", "").lower()
    if fn in {"skill.md", "agents.md", "conventions.md", ".cursorrules",
              "copilot-instructions.md", "claude.md"}:
        score += 20
    return score

def main():
    if not IN_PATH.exists():
        print(f"ERROR: {IN_PATH} not found. Run classify.py first.")
        return
    manifest = json.loads(IN_PATH.read_text())
    files = manifest.get("files", [])
    print(f"Deduping {len(files)} files...")

    # ---- Step 1: cluster by normalized title ----
    by_title: dict[str, list[int]] = defaultdict(list)
    for i, rec in enumerate(files):
        nt = normalize_title(rec.get("title", ""))
        if nt:
            by_title[nt].append(i)

    # ---- Step 2: for unclustered (singletons), try summary similarity ----
    clusters: list[list[int]] = []
    assigned: set[int] = set()
    for nt, idxs in by_title.items():
        if len(idxs) > 1:
            clusters.append(idxs)
            for i in idxs:
                assigned.add(i)
    # remaining singletons — try Jaccard similarity on summaries
    singletons = [i for i in range(len(files)) if i not in assigned]
    summaries_tok = {i: tokenize(files[i].get("summary", "")) for i in singletons}
    used: set[int] = set()
    for i in singletons:
        if i in used:
            continue
        cluster = [i]
        used.add(i)
        for j in singletons:
            if j in used or j == i:
                continue
            if jaccard(summaries_tok[i], summaries_tok[j]) >= 0.7:
                cluster.append(j)
                used.add(j)
        if len(cluster) > 1:
            clusters.append(cluster)

    # ---- Step 3: within each cluster, pick canonical ----
    canonical_by_cluster: dict[int, int] = {}
    for cid, cluster in enumerate(clusters):
        best_i = max(cluster, key=lambda i: canonical_score(files[i]))
        canonical_by_cluster[cid] = best_i

    # ---- Step 4: also process singletons as 1-element clusters ----
    singleton_clusters: list[list[int]] = [[i] for i in range(len(files)) if i not in assigned and i not in used]
    for sc in singleton_clusters:
        clusters.append(sc)
        canonical_by_cluster[len(clusters) - 1] = sc[0]

    # ---- Step 5: augment records ----
    for cid, cluster in enumerate(clusters):
        canon_i = canonical_by_cluster[cid]
        cluster_size = len(cluster)
        for i in cluster:
            files[i]["cluster_id"] = f"cluster_{cid:04d}"
            files[i]["cluster_size"] = cluster_size
            files[i]["canonical"] = (i == canon_i)
            files[i]["see_also"] = [
                files[j]["extracted_path"]
                for j in cluster if j != i
            ]

    cluster_size_dist = Counter(len(c) for c in clusters)
    multi_clusters = sum(1 for c in clusters if len(c) > 1)
    canonical_count = sum(1 for f in files if f.get("canonical"))

    manifest["files"] = files
    manifest["dedup_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    manifest["dedup_stats"] = {
        "total_clusters": len(clusters),
        "multi_clusters": multi_clusters,
        "canonical_count": canonical_count,
        "cluster_size_distribution": dict(cluster_size_dist),
    }

    OUT_PATH.write_text(json.dumps(manifest, indent=2))
    print(f"\nDedup complete.")
    print(f"  Total clusters: {len(clusters)}")
    print(f"  Multi-file clusters: {multi_clusters}")
    print(f"  Canonical (⭐) entries: {canonical_count}")
    print(f"  Cluster size distribution: {dict(cluster_size_dist)}")
    print(f"\nWrote: {OUT_PATH}")

if __name__ == "__main__":
    main()
