#!/usr/bin/env python3
"""
The Lord of the Skills — Antigravity Focused Crawler
=====================================================
Google Antigravity is the new agentic IDE (2025). This crawler specifically
targets Antigravity skill, agent, and rule repos.

Strategy:
  Phase 1: Use GitHub Search API to find Antigravity-specific repos
           (queries: "antigravity skill", "antigravity agent", "antigravity rules",
            "google antigravity", "antigravity IDE", "antigravity mcp")
  Phase 2: Also scan the existing sickn33/antigravity-awesome-skills repo for links
  Phase 3: Clone all discovered repos, extract skill/agent/rule files using
           the same SKILL_FILE_PATTERNS as the main crawler
  Phase 4: Merge results into the existing skills/ tree, classifying each
           file into the appropriate LOTR kingdom

Outputs:
  - New skill files in /home/z/my-project/repo-push/skills/<kingdom>/antigravity/<repo>/
  - Updated manifest_fragment_antigravity.json
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter, defaultdict

import requests

# Reuse main crawler utilities
import sys
sys.path.insert(0, "/home/z/my-project/scripts")
from crawler import (
    SKILL_FILE_PATTERNS, SKIP_PATTERNS, is_skill_file,
    detect_framework, SESSION, GITHUB_TOKEN
)
from classify import KINGDOM_KEYWORDS

ROOT = Path("/home/z/my-project/the-lord-of-the-skills")
AG_CACHE_DIR = ROOT / "_cache" / "ag_repos"   # antigravity-specific cache
AG_RAW_DIR = ROOT / "_raw_antigravity"        # extracted files
AG_MANIFEST = ROOT / "_cache" / "manifest_antigravity.json"
AG_LOG = ROOT / "_cache" / "antigravity_crawler.log"

REPO_PUSH_SKILLS = Path("/home/z/my-project/repo-push/skills")

AG_CACHE_DIR.mkdir(parents=True, exist_ok=True)
AG_RAW_DIR.mkdir(parents=True, exist_ok=True)
( ROOT / "_cache").mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------
# Antigravity-specific seeds + search queries
# ----------------------------------------------------------------------
AG_SEED_REPOS = [
    "sickn33/antigravity-awesome-skills",     # already in main tree but re-spider
    "google/antigravity",                     # if it exists
    "antigravity-team/antigravity",
    "AntigravityOfficial/antigravity",
]

AG_SEARCH_QUERIES = [
    "antigravity skill",
    "antigravity agent",
    "antigravity rules",
    "antigravity mcp",
    "antigravity IDE",
    "google antigravity",
    "antigravity skills",
    "antigravity agents",
    "antigravity-skills",
    "antigravity-agents",
    "antigravity-rules",
    "antigravity awesome",
    "awesome antigravity",
    "antigravity cursorrules",
    "antigravity prompts",
    "antigravity conventions",
    "antigravity config",
    "antigravity extensions",
    "antigravity plugins",
    "antigravity-tools",
    "antigravity-dev",
    "antigravity-cli",
    "antigravity sdk",
    "antigravity python",
    "antigravity typescript",
    "antigravity javascript",
    "agentic IDE antigravity",
    "antigravity subagents",
    "antigravity system prompt",
    "antigravity tutorial",
]

# ----------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------
def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(AG_LOG, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")

# ----------------------------------------------------------------------
# GitHub Search (rate-limited)
# ----------------------------------------------------------------------
def github_search_repos(query: str, per_page: int = 30) -> list[str]:
    """Use GitHub Search API to find repos matching the query."""
    url = "https://api.github.com/search/repositories"
    headers = {"Accept": "application/vnd.github+json",
               "X-GitHub-Api-Version": "2022-11-28"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    try:
        r = SESSION.get(url, params={"q": query, "sort": "stars",
                                      "order": "desc", "per_page": per_page},
                        timeout=20, headers=headers)
        if r.status_code == 403:
            log(f"  RATE LIMITED on search")
            return []
        if r.status_code != 200:
            log(f"  search HTTP {r.status_code}: {r.text[:100]}")
            return []
        items = r.json().get("items", [])
        return [f"{it['owner']['login']}/{it['name']}" for it in items]
    except Exception as e:
        log(f"  search error: {e}")
        return []

def github_search_code(query: str, per_page: int = 30) -> list[dict]:
    """Search code for files matching the query (requires token)."""
    url = "https://api.github.com/search/code"
    headers = {"Accept": "application/vnd.github+json",
               "X-GitHub-Api-Version": "2022-11-28"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    try:
        r = SESSION.get(url, params={"q": query, "per_page": per_page},
                        timeout=20, headers=headers)
        if r.status_code == 403:
            log(f"  RATE LIMITED on code search")
            return []
        if r.status_code != 200:
            log(f"  code search HTTP {r.status_code}")
            return []
        items = r.json().get("items", [])
        return items
    except Exception as e:
        log(f"  code search error: {e}")
        return []

# ----------------------------------------------------------------------
# Git clone
# ----------------------------------------------------------------------
def ag_clone_repo(repo: str, depth: int = 1) -> bool:
    """Clone repo into antigravity cache dir."""
    safe_name = repo.replace("/", "__")
    local = AG_CACHE_DIR / safe_name
    if local.exists() and (local / ".git").exists():
        return True
    if local.exists():
        shutil.rmtree(local, ignore_errors=True)
    local.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://github.com/{repo}.git"
    try:
        result = subprocess.run(
            ["git", "clone", "--depth", str(depth), "--quiet",
             "--filter=blob:none", "--no-tags", url, str(local)],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            log(f"  CLONE FAIL {repo}: {result.stderr.strip()[:200]}")
            return False
        return True
    except subprocess.TimeoutExpired:
        log(f"  CLONE TIMEOUT {repo}")
        return False
    except Exception as e:
        log(f"  CLONE ERROR {repo}: {e}")
        return False

# ----------------------------------------------------------------------
# Extract skill files from a cloned repo
# ----------------------------------------------------------------------
def safe_filename(name: str) -> str:
    """URL/git-safe filename (reuse main restructure logic)."""
    if name.startswith("⭐_"):
        name = "canonical__" + name[3:]
    elif name.startswith("⭐"):
        name = "canonical__" + name[1:]
    import unicodedata
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.replace(" ", "-")
    name = re.sub(r"[-_]{2,}", "_", name) if not name.startswith("canonical_") else name
    name = re.sub(r"[-]+", "-", name)
    name = re.sub(r"[^A-Za-z0-9._-]", "", name)
    return name.lstrip(".-") or "unnamed"

def classify_kingdom(content: str, framework: str, original_path: str) -> str:
    """Same classifier as main crawler."""
    text = (content + " " + original_path).lower()
    scores = Counter()
    for kingdom, spec in KINGDOM_KEYWORDS.items():
        for kw in spec["keywords"]:
            if kw in text:
                scores[kingdom] += 1
    if framework in {"claude-code", "autogen", "crewai", "langgraph", "openhands"}:
        scores["isengard"] += 2
    if not scores:
        return "mirkwood"
    return scores.most_common(1)[0][0]

def extract_files_from_repo(repo: str) -> list[dict]:
    """Walk repo and extract skill/agent/rule files."""
    safe_name = repo.replace("/", "__")
    local = AG_CACHE_DIR / safe_name
    if not local.exists():
        return []
    records = []
    for root, dirs, files in os.walk(local):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules",
                   "__pycache__", ".venv", "venv", "dist", "build", "vendor",
                   ".next", "target", "site-packages"}]
        for fn in files:
            full = Path(root) / fn
            rel = str(full.relative_to(local))
            if not is_skill_file(rel):
                continue
            try:
                content = full.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if not content.strip():
                continue
            framework = detect_framework(rel, repo)
            # Override framework to 'antigravity' for files from AG repos
            # (unless it's clearly a different framework like .cursorrules)
            if "antigravity" in repo.lower() and framework == "general":
                framework = "antigravity"
            kingdom = classify_kingdom(content, framework, rel)
            filename = Path(rel).name
            # Write to AG raw dir
            safe_rel = rel.replace("/", "__").lstrip(".")
            target_raw = AG_RAW_DIR / framework / safe_name / safe_filename(safe_rel)
            target_raw.parent.mkdir(parents=True, exist_ok=True)
            target_raw.write_text(content)
            # Also write to repo-push skills tree
            target_skills = REPO_PUSH_SKILLS / kingdom / framework / safe_name / safe_filename(filename)
            target_skills.parent.mkdir(parents=True, exist_ok=True)
            if not target_skills.exists():
                target_skills.write_text(content)
            records.append({
                "source_repo": repo,
                "framework": framework,
                "kingdom": kingdom,
                "original_path": rel,
                "filename": filename,
                "extracted_path": str(target_raw.relative_to(ROOT)),
                "skills_path": str(target_skills.relative_to("/home/z/my-project/repo-push")),
                "size_bytes": len(content.encode("utf-8")),
                "line_count": content.count("\n") + 1,
                "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            })
    return records

# ----------------------------------------------------------------------
# BFS: scan README for github links
# ----------------------------------------------------------------------
GITHUB_LINK_RE = re.compile(
    r"github\.com/([A-Za-z0-9](?:[A-Za-z0-9\-]{0,38}[A-Za-z0-9]?))/([A-Za-z0-9][A-Za-z0-9._\-]{0,99})",
    re.IGNORECASE,
)
NON_REPO_NAMES = {
    "github", "about", "features", "pricing", "login", "signup", "topics",
    "trending", "collections", "events", "sponsors", "settings",
    "notifications", "explore", "marketplace", "search", "new", "orgs",
    "organizations", "profile", "dashboard", "session", "sessions",
    "pulls", "issues", "codespaces", "actions", "projects", "packages",
    "stars", "watchers", "forks", "blob", "tree", "commit", "releases",
    "tags", "branches", "compare", "wiki", "graphs", "network",
    "security", "policy", "insights", "pulse", "community", "discussions",
    "wiki", "settings", "account", "apps", "marketplace", "sponsors",
    "feature_request", "bug_report", "issues", "pull", "pulls",
    "settings", "billing", "emails", "notifications", "keys",
}

def discover_ag_repos_from_readme(repo_path: Path) -> list[str]:
    """Scan README for github links that might be antigravity-related."""
    found = []
    scan_files = []
    for name in ["README.md", "readme.md", "README.rst", "README", "OVERVIEW.md", "INDEX.md"]:
        p = repo_path / name
        if p.exists():
            scan_files.append(p)
    for d in ["docs", "doc", "awesomes", "lists", "skills", "agents", "prompts"]:
        dpath = repo_path / d
        if dpath.is_dir():
            scan_files.extend(dpath.rglob("*.md"))
    for p in repo_path.glob("*.md"):
        if p not in scan_files:
            scan_files.append(p)
    scan_files = scan_files[:50]
    for f in scan_files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        # Only collect links from files that mention antigravity
        if "antigravity" not in text.lower():
            continue
        for m in GITHUB_LINK_RE.finditer(text):
            owner, name = m.group(1), m.group(2)
            name = name.rstrip("/.!?")
            if "/" in name:
                name = name.split("/")[0]
            if name.lower() in NON_REPO_NAMES:
                continue
            if "." in name and not name.endswith((".git", ".md")):
                if not re.match(r"^[A-Za-z0-9][A-Za-z0-9._\-]*$", name):
                    continue
            if len(name) < 2 or len(name) > 60:
                continue
            found.append(f"{owner}/{name}")
    return list(dict.fromkeys(found))

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    log("=" * 70)
    log("THE LORD OF THE SKILLS — Antigravity Focused Crawler")
    log(f"Seeds: {len(AG_SEED_REPOS)} | Search queries: {len(AG_SEARCH_QUERIES)}")
    log("=" * 70)

    discovered: set[str] = set()
    discovered.update(AG_SEED_REPOS)

    # ---- Phase 1: GitHub Search API ----
    log(f"\n[Phase 1] GitHub Search API expansion ({len(AG_SEARCH_QUERIES)} queries)")
    for i, q in enumerate(AG_SEARCH_QUERIES, 1):
        log(f"  [{i}/{len(AG_SEARCH_QUERIES)}] searching: {q}")
        repos = github_search_repos(q, per_page=30)
        for r in repos:
            discovered.add(r)
        # Also do a code search for files mentioning antigravity
        if GITHUB_TOKEN:
            code_results = github_search_code(f"antigravity in:file extension:md", per_page=20)
            for item in code_results:
                repo_full = item.get("repository", {}).get("full_name")
                if repo_full:
                    discovered.add(repo_full)
        time.sleep(2 if GITHUB_TOKEN else 7)
    log(f"  Discovered: {len(discovered)} unique repos")

    # ---- Phase 2: BFS expansion from any cloned AG seeds ----
    log(f"\n[Phase 2] BFS expansion from AG seed repos")
    for repo in AG_SEED_REPOS:
        if not ag_clone_repo(repo):
            continue
        new_repos = discover_ag_repos_from_readme(AG_CACHE_DIR / repo.replace("/", "__"))
        for nr in new_repos:
            discovered.add(nr)
    log(f"  After BFS: {len(discovered)} repos discovered")

    # ---- Phase 3: Clone all discovered repos + extract ----
    log(f"\n[Phase 3] Clone + extract from {len(discovered)} repos")
    all_records = []
    cloned = set()
    for i, repo in enumerate(sorted(discovered), 1):
        log(f"  [{i}/{len(discovered)}] cloning {repo}")
        if not ag_clone_repo(repo):
            continue
        cloned.add(repo)
        records = extract_files_from_repo(repo)
        all_records.extend(records)
        log(f"    → {len(records)} files extracted")
        # Free disk after each AG repo (small repos)
        # Don't delete cache since we might re-spider

    # ---- Write manifest ----
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "crawler_type": "antigravity-focused",
        "total_discovered_repos": len(discovered),
        "total_cloned_repos": len(cloned),
        "total_extracted_files": len(all_records),
        "frameworks_detected": sorted({r["framework"] for r in all_records}),
        "kingdoms_detected": sorted({r["kingdom"] for r in all_records}),
        "files": all_records,
    }
    AG_MANIFEST.write_text(json.dumps(manifest, indent=2))

    # ---- Summary ----
    kingdom_counter = Counter(r["kingdom"] for r in all_records)
    framework_counter = Counter(r["framework"] for r in all_records)
    log("\n" + "=" * 70)
    log("ANTIGRAVITY CRAWL COMPLETE")
    log("=" * 70)
    log(f"  Discovered: {len(discovered)} AG-related repos")
    log(f"  Cloned:     {len(cloned)} repos")
    log(f"  Extracted:  {len(all_records)} files")
    log(f"  Kingdoms: {dict(kingdom_counter)}")
    log(f"  Frameworks: {dict(framework_counter)}")
    log(f"  Manifest: {AG_MANIFEST}")

if __name__ == "__main__":
    main()
