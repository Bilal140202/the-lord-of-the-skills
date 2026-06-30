#!/usr/bin/env python3
"""
The Lord of the Skills — Package Builder
=========================================
Reads _cache/manifest_final.json, builds the final themed package:
  /home/z/my-project/download/the-lord-of-the-skills/
    ├── README.md              (Fellowship Manifesto, LOTR themed)
    ├── CREDITS.md             (aggregate credits — all source repos)
    ├── MAP_OF_THE_KINGDOMS.md (visual taxonomy)
    ├── SKILL_INDEX.md         (browseable index)
    ├── skills/
    │   ├── gondor/            (coding)
    │   │   ├── claude-code/
    │   │   ├── cursor/
    │   │   └── ...
    │   ├── rivendell/         (research)
    │   ├── moria/             (devops)
    │   ├── lothlorien/        (data)
    │   ├── mordor/            (security)
    │   ├── the-shire/         (writing)
    │   ├── isengard/          (agents)
    │   ├── rohan/             (testing)
    │   ├── fangorn/           (memory/docs)
    │   └── mirkwood/          (specialized)
    └── _manifest.json         (full manifest, for tooling)
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime, timezone

ROOT = Path("/home/z/my-project/the-lord-of-the-skills")
IN_PATH = ROOT / "_cache" / "manifest_final.json"
OUT_DIR = Path("/home/z/my-project/download/the-lord-of-the-skills")
SKILLS_DIR = OUT_DIR / "skills"

KINGDOMS = {
    "gondor":      {"name": "Gondor",       "domain": "Coding & Software Engineering",
                    "motto": "Gondor sees, Gondor codes.",
                    "color": "#1e3a8a",
                    "symbol": "⚔"},
    "rivendell":   {"name": "Rivendell",    "domain": "Research & Knowledge",
                    "motto": "Knowledge flows from the Last Homely House.",
                    "color": "#0f766e",
                    "symbol": "✦"},
    "moria":       {"name": "Moria",        "domain": "DevOps & Infrastructure",
                    "motto": "Speak, friend, and enter the deploy.",
                    "color": "#4b5563",
                    "symbol": "⛏"},
    "lothlorien":  {"name": "Lothlórien",   "domain": "Data & Analysis",
                    "motto": "Where data roots run deep.",
                    "color": "#15803d",
                    "symbol": "✿"},
    "mordor":      {"name": "Mordor",       "domain": "Security & Auditing",
                    "motto": "One audit to rule them all.",
                    "color": "#991b1b",
                    "symbol": "👁"},
    "the-shire":   {"name": "The Shire",    "domain": "Writing & Content",
                    "motto": "Quiet writing, deep roots.",
                    "color": "#a16207",
                    "symbol": "✎"},
    "isengard":    {"name": "Isengard",     "domain": "Agents & Orchestration",
                    "motto": "Industry wakes the deep.",
                    "color": "#52525b",
                    "symbol": "⚙"},
    "rohan":       {"name": "Rohan",        "domain": "Testing & Verification",
                    "motto": "Ride now, ride to verify.",
                    "color": "#92400e",
                    "symbol": "🐴"},
    "fangorn":     {"name": "Fangorn",      "domain": "Documentation & Memory",
                    "motto": "The old forest remembers.",
                    "color": "#166534",
                    "symbol": "🌳"},
    "mirkwood":    {"name": "Mirkwood",     "domain": "Specialized & Niche",
                    "motto": "Strange paths through the wood.",
                    "color": "#581c87",
                    "symbol": "🕸"},
}

def safe_filename(s: str) -> str:
    """Make a filesystem-safe filename."""
    keep = "-_./ "
    return "".join(c for c in s if c.isalnum() or c in keep).strip().replace(" ", "_")

def build_readme(manifest: dict) -> str:
    """The Fellowship Manifesto — README.md"""
    files = manifest["files"]
    n_repos = manifest.get("total_cloned_repos", 0)
    n_discovered = manifest.get("total_discovered_repos", 0)
    by_kingdom = Counter(f["kingdom"] for f in files)
    by_framework = Counter(f["framework"] for f in files)
    canonical_count = sum(1 for f in files if f.get("canonical"))

    lines = []
    lines.append("# ⚔ The Lord of the Skills ⚔\n")
    lines.append("> *One catalog to rule them all, one catalog to find them,")
    lines.append("> One catalog to bring them all, and in the darkness bind them.*\n")
    lines.append("---\n")
    lines.append("## 📜 The Fellowship Manifesto\n")
    lines.append(
        "Across the wide lands of GitHub, scattered among 10,000 repositories, lie the "
        "Artifacts of Agency — `SKILL.md` files that teach machines to act, `AGENTS.md` "
        "tomes that bind them to conventions, `.cursorrules` scrolls that direct their "
        "hands, `.clinerules` memory-banks that preserve their thought. For an age these "
        "artifacts lay divided: Claude Code in the West, Cursor in the East, Cline in the "
        "deep places, Aider in the libraries, OpenHands in the wild. No single hand "
        "gathered them. Until now.\n"
    )
    lines.append(
        "**The Lord of the Skills** is that gathering. A reusable Python crawler "
        f"spidered {n_discovered} GitHub repositories, cloned {n_repos} of them, and "
        f"extracted {len(files)} skill, agent, and rule files. Each artifact was sorted "
        "into one of ten kingdoms, tagged by its source framework, classified by skill "
        "type, and deduplicated with a canonical representative chosen per concept. The "
        "result is a portable library you can drop into any agentic AI tool — Claude "
        "Code, Cursor, Cline, Roo, Aider, OpenHands, Continue, Goose, Copilot, or any "
        "future fellowship.\n"
    )
    lines.append("## 🗺 The Ten Kingdoms\n")
    lines.append("| Kingdom | Domain | Artifacts | Motto |")
    lines.append("|---|---|---:|---|")
    for k, info in KINGDOMS.items():
        lines.append(f"| {info['symbol']} **{info['name']}** | {info['domain']} | {by_kingdom.get(k, 0)} | *{info['motto']}* |")
    lines.append(f"| | **TOTAL** | **{len(files)}** | |\n")

    lines.append("## ⚙ Frameworks Represented\n")
    lines.append("| Framework | Artifact count |")
    lines.append("|---|---:|")
    for fw, count in by_framework.most_common():
        lines.append(f"| {fw} | {count} |")
    lines.append("")

    lines.append("## ⭐ Canonical Artifacts\n")
    lines.append(
        f"Of {len(files)} total artifacts, **{canonical_count}** are marked **⭐ "
        "canonical** — the single best representative of each concept cluster. The rest "
        "are kept as variants, so you can compare how Claude Code, Cursor, and Cline each "
        "express the same idea (e.g. `git-commit`, `plan-task`, `verify-output`).\n"
    )

    lines.append("## 📦 What's in this package\n")
    lines.append("```")
    lines.append("the-lord-of-the-skills/")
    lines.append("├── README.md              ← you are here")
    lines.append("├── CREDITS.md             ← all source repos + licenses")
    lines.append("├── MAP_OF_THE_KINGDOMS.md ← visual taxonomy")
    lines.append("├── SKILL_INDEX.md         ← browseable flat index")
    lines.append("├── Lord_of_the_Skills_Catalog.pdf  ← master catalog (PDF)")
    lines.append("├── Lord_of_the_Skills_Index.xlsx   ← filterable spreadsheet")
    lines.append("├── _manifest.json         ← machine-readable full manifest")
    lines.append("└── skills/")
    for k, info in KINGDOMS.items():
        lines.append(f"    ├── {k}/    ← {info['name']} ({info['domain']})")
    lines.append("```\n")

    lines.append("## 🔧 Usage\n")
    lines.append("### Drop into Claude Code\n")
    lines.append("```bash")
    lines.append("cp -r skills/gondor/claude-code/* ~/.claude/skills/")
    lines.append("```\n")
    lines.append("### Drop into Cursor\n")
    lines.append("```bash")
    lines.append("cp -r skills/gondor/cursor/*  .cursor/rules/")
    lines.append("```\n")
    lines.append("### Drop into Cline / Roo Code\n")
    lines.append("```bash")
    lines.append("cp -r skills/gondor/cline/*   .clinerules/")
    lines.append("cp -r skills/gondor/roo/*     .roo/rules/")
    lines.append("```\n")
    lines.append("### Use the canonical-only subset\n")
    lines.append(
        "Every artifact's filename has a `canonical` flag in the manifest. To copy only "
        "the ⭐ canonical skill per concept:\n"
    )
    lines.append("```bash")
    lines.append("python3 -c \"import json; m=json.load(open('_manifest.json')); \\")
    lines.append("  [print(f['extracted_path']) for f in m['files'] if f.get('canonical')]\" \\")
    lines.append("  | xargs -I{} cp {} /target/dir/")
    lines.append("```\n")

    lines.append("## 🔄 Refresh\n")
    lines.append(
        "A monthly cron job re-runs `scripts/crawler.py → classify.py → dedup.py → "
        "build_package.py` to refresh this package with newly-published skills. The "
        "crawler is in `/home/z/my-project/scripts/crawler.py` and is fully reusable — "
        "run it any time to pull the latest.\n"
    )

    lines.append("## ⚖ Licensing\n")
    lines.append(
        "Every artifact in `skills/` retains its original source license. See "
        "**CREDITS.md** for the full list of source repositories, their authors, and "
        "their licenses. Where a source repo did not include a LICENSE file, the "
        "artifact is reproduced under GitHub's default terms (all rights reserved by "
        "the author) for study and reference. **Do not redistribute this package "
        "commercially without auditing CREDITS.md and respecting each upstream license.**\n"
    )

    lines.append("---\n")
    lines.append(f"*Compiled on {manifest.get('generated_at', 'unknown')}.* ")
    lines.append("*May your agents be wise, your prompts be sharp, and your skills be many.*\n")
    return "\n".join(lines)

def build_credits(manifest: dict) -> str:
    """Aggregate CREDITS.md listing every source repo."""
    files = manifest["files"]
    repos = defaultdict(lambda: {"files": [], "frameworks": set()})
    for f in files:
        repos[f["source_repo"]]["files"].append(f)
        repos[f["source_repo"]]["frameworks"].add(f["framework"])

    lines = []
    lines.append("# 🙏 CREDITS — The Source Repositories\n")
    lines.append(
        "Every artifact in The Lord of the Skills was extracted from a public GitHub "
        f"repository. This file lists all {len(repos)} source repositories, sorted "
        "alphabetically, with the artifacts pulled from each. Per our aggregate-"
        "attribution policy, individual skill files do not carry per-file attribution — "
        "this file is the single source of truth.\n"
    )
    lines.append(
        "If you are a repository maintainer and wish to have your skills removed from "
        "this compilation, please open an issue. We respect all upstream licenses and "
        "will comply promptly.\n"
    )
    lines.append("---\n")
    lines.append("| # | Repository | URL | Frameworks | Files |")
    lines.append("|---:|---|---|---|---:|")
    for i, (repo, info) in enumerate(sorted(repos.items()), 1):
        url = f"https://github.com/{repo}"
        fws = ", ".join(sorted(info["frameworks"]))
        lines.append(f"| {i} | `{repo}` | {url} | {fws} | {len(info['files'])} |")
    lines.append("")
    lines.append(f"**Total repositories: {len(repos)}**")
    lines.append(f"**Total artifacts extracted: {len(files)}**")
    lines.append("")
    lines.append("---\n")
    lines.append("## License Notes\n")
    lines.append(
        "Each upstream repository retains its own license. The Lord of the Skills "
        "compilation scripts (crawler, classifier, dedup, build) are released under MIT. "
        "The compiled skill artifacts are NOT re-licensed — they remain under their "
        "original upstream terms.\n"
    )
    return "\n".join(lines)

def build_map(manifest: dict) -> str:
    """MAP_OF_THE_KINGDOMS.md — visual taxonomy."""
    files = manifest["files"]
    by_kingdom_fw: dict[tuple[str, str], int] = Counter((f["kingdom"], f["framework"]) for f in files)
    kingdom_counts = Counter(f["kingdom"] for f in files)

    lines = []
    lines.append("# 🗺 Map of the Kingdoms\n")
    lines.append(
        "The Ten Kingdoms of the Lord of the Skills, each ruling a domain of agent "
        "capability. Below is the full taxonomy with artifact counts per kingdom and "
        "per framework.\n"
    )
    lines.append("---\n")
    for k, info in KINGDOMS.items():
        total = kingdom_counts.get(k, 0)
        lines.append(f"## {info['symbol']} {info['name']} — *{info['domain']}*\n")
        lines.append(f"> *\"{info['motto']}\"*\n")
        lines.append(f"**Artifacts:** {total}\n")
        if total > 0:
            # framework breakdown
            fw_counts = {fw: c for (kg, fw), c in by_kingdom_fw.items() if kg == k}
            sorted_fws = sorted(fw_counts.items(), key=lambda x: -x[1])
            lines.append("| Framework | Count |")
            lines.append("|---|---:|")
            for fw, c in sorted_fws:
                lines.append(f"| {fw} | {c} |")
            lines.append("")
        lines.append("---\n")
    return "\n".join(lines)

def build_index(manifest: dict) -> str:
    """SKILL_INDEX.md — browseable flat index."""
    files = sorted(manifest["files"], key=lambda f: (f["kingdom"], f["framework"],
                                                      f.get("title", "").lower()))
    lines = []
    lines.append("# 📚 Skill Index\n")
    lines.append(
        "Flat browseable index of every artifact in The Lord of the Skills. ⭐ marks "
        f"canonical representatives. Total: **{len(files)}** artifacts.\n"
    )
    lines.append("---\n")
    current_kingdom = None
    for f in files:
        if f["kingdom"] != current_kingdom:
            current_kingdom = f["kingdom"]
            info = KINGDOMS[current_kingdom]
            lines.append(f"\n## {info['symbol']} {info['name']} — *{info['domain']}*\n")
        star = "⭐ " if f.get("canonical") else "   "
        title = f.get("title", "(untitled)")
        repo = f["source_repo"]
        path = f["extracted_path"].replace("\\", "/")
        lines.append(f"- {star}**{title}** · `{f['framework']}` · `{repo}` · `{path}`")
    lines.append("")
    return "\n".join(lines)

def copy_skills(manifest: dict) -> None:
    """Copy each extracted file into skills/<kingdom>/<framework>/<file>."""
    if SKILLS_DIR.exists():
        shutil.rmtree(SKILLS_DIR)
    SKILLS_DIR.mkdir(parents=True)
    for f in manifest["files"]:
        kingdom = f["kingdom"]
        framework = f["framework"]
        target_dir = SKILLS_DIR / kingdom / framework / f["source_repo"].replace("/", "__")
        target_dir.mkdir(parents=True, exist_ok=True)
        src = ROOT / f["extracted_path"]
        if not src.exists():
            continue
        # use original filename
        target_name = Path(f["original_path"]).name
        # add canonical prefix to filename for visibility
        if f.get("canonical"):
            target_name = "⭐_" + target_name
        target = target_dir / target_name
        # avoid collisions
        n = 1
        while target.exists():
            target = target_dir / f"{Path(f['original_path']).stem}_{n}{Path(f['original_path']).suffix}"
            n += 1
        shutil.copy2(src, target)

def main():
    if not IN_PATH.exists():
        print(f"ERROR: {IN_PATH} not found. Run dedup.py first.")
        return
    manifest = json.loads(IN_PATH.read_text())
    print(f"Building package from {len(manifest['files'])} files...")

    # prepare output dir
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # write top-level files
    (OUT_DIR / "README.md").write_text(build_readme(manifest))
    print("  ✓ README.md")
    (OUT_DIR / "CREDITS.md").write_text(build_credits(manifest))
    print("  ✓ CREDITS.md")
    (OUT_DIR / "MAP_OF_THE_KINGDOMS.md").write_text(build_map(manifest))
    print("  ✓ MAP_OF_THE_KINGDOMS.md")
    (OUT_DIR / "SKILL_INDEX.md").write_text(build_index(manifest))
    print("  ✓ SKILL_INDEX.md")

    # copy skills
    copy_skills(manifest)
    print("  ✓ skills/ tree copied")

    # write manifest
    (OUT_DIR / "_manifest.json").write_text(json.dumps(manifest, indent=2))
    print("  ✓ _manifest.json")

    print(f"\nPackage built at: {OUT_DIR}")

if __name__ == "__main__":
    main()
