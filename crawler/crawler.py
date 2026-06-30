#!/usr/bin/env python3
"""
The Lord of the Skills — Master Crawler
=======================================
Spiders GitHub for agentic AI skill/agent/rule files across all major ecosystems.

Strategy (no GitHub token required):
  Phase 1 — Seed expansion: clone ~60 known seed repos + awesome-lists.
            Parse their README files for links to other skill collections (BFS).
  Phase 2 — Bulk clone: git clone --depth=1 every discovered repo into _cache/repos/.
            No GitHub API rate limit applies to git clone.
  Phase 3 — Extract: walk every cloned repo, identify and copy skill/agent/rule files
            into _raw/<framework>/<repo>/<file>. Build manifest.json.
  Phase 4 — Search expansion (optional): use GitHub Search API within the
            60 req/hr unauthenticated budget to find additional repos.

File types covered (the "spider web"):
  SKILL.md, skills/**/*.md, AGENTS.md, agents/**/*.md,
  .cursorrules, .cursor/rules/*.mdc, *.cursorrules,
  .clinerules/*, .cline/*, cline-rules/*,
  .roo/rules/*, .roo/modes/*,
  CONVENTIONS.md, .aider*, aider-cmd/*,
  .continue/*, config.yaml (continue),
  .goose/*, extensions/*,
  prompts/**/*.md, system-prompts/*, *.prompt.md, *.mdc,
  .github/copilot-instructions.md,
  rules/**/*.md, awesome-* (awesome lists get their own treatment)
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import requests

# ----------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------
ROOT = Path("/home/z/my-project/the-lord-of-the-skills")
CACHE_DIR = ROOT / "_cache" / "repos"          # cloned repos live here
RAW_DIR = ROOT / "_raw"                        # extracted skill files land here
MANIFEST_PATH = ROOT / "_cache" / "manifest.json"
STATE_PATH = ROOT / "_cache" / "crawler_state.json"
LOG_PATH = ROOT / "_cache" / "crawler.log"

ROOT.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR.mkdir(parents=True, exist_ok=True)
( ROOT / "_cache").mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------
# HTTP session with caching + retry
# ----------------------------------------------------------------------
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "LordOfTheSkillsCrawler/1.0 (+research)"})

# ----------------------------------------------------------------------
# Framework taxonomy
# ----------------------------------------------------------------------
FRAMEWORK_PATTERNS = {
    "claude-code":    ["SKILL.md", "skill.md"],
    "cursor":         [".cursorrules", ".cursor/rules", ".mdc", ".cursor"],
    "cline":          [".clinerules", ".cline", "cline-rules", "cline_rules"],
    "roo":            [".roo"],
    "aider":          [".aider", "CONVENTIONS.md", "aider-cmd"],
    "openhands":      ["openhands", "OpenHands"],
    "swe-agent":      ["swe-agent", "SWE-agent"],
    "codex":          ["AGENTS.md"],   # OpenAI Codex convention
    "continue":       [".continue"],
    "goose":          [".goose", "extensions"],
    "copilot":        [".github/copilot-instructions.md"],
    "autogen":        ["autogen", "AutoGen"],
    "crewai":         ["crewai", "CrewAI"],
    "langgraph":      ["langgraph", "LangGraph"],
    "general":        [],  # fallback bucket
}

# ----------------------------------------------------------------------
# Skill file detection patterns
# ----------------------------------------------------------------------
SKILL_FILE_PATTERNS = [
    # exact filenames
    re.compile(r"(^|/)SKILL\.md$", re.I),
    re.compile(r"(^|/)AGENTS\.md$", re.I),
    re.compile(r"(^|/)CONVENTIONS\.md$", re.I),
    re.compile(r"(^|/)\.cursorrules$", re.I),
    re.compile(r"(^|/)copilot-instructions\.md$", re.I),
    re.compile(r"(^|/)CLAUDE\.md$", re.I),
    re.compile(r"(^|/)AI_GUIDELINES\.md$", re.I),
    re.compile(r"(^|/)\.windsurfrules$", re.I),
    re.compile(r"(^|/)\.codeiumrules$", re.I),
    # directories
    re.compile(r"(^|/)skills/[^/]+\.md$", re.I),
    re.compile(r"(^|/)agents/[^/]+\.md$", re.I),
    re.compile(r"(^|/)prompts/[^/]+\.md$", re.I),
    re.compile(r"(^|/)system-prompts/[^/]+\.md$", re.I),
    re.compile(r"(^|/)\.cursor/rules/.+\.(mdc|md)$", re.I),
    re.compile(r"(^|/)\.clinerules/.+\.md$", re.I),
    re.compile(r"(^|/)\.cline/.+\.md$", re.I),
    re.compile(r"(^|/)\.roo/(rules|modes)/.+\.md$", re.I),
    re.compile(r"(^|/)\.continue/.+\.(yaml|json|md)$", re.I),
    re.compile(r"(^|/)\.goose/.+\.(yaml|md)$", re.I),
    re.compile(r"(^|/)\.aider", re.I),
    # extensions
    re.compile(r"\.cursorrules$", re.I),
    re.compile(r"\.prompt\.md$", re.I),
    re.compile(r"\.mdc$", re.I),
    re.compile(r"\.prompt$", re.I),
]

# Skip patterns — common noise
SKIP_PATTERNS = [
    re.compile(r"/node_modules/", re.I),
    re.compile(r"/\.git/", re.I),
    re.compile(r"/vendor/", re.I),
    re.compile(r"/dist/", re.I),
    re.compile(r"/build/", re.I),
    re.compile(r"/\.venv/", re.I),
    re.compile(r"/__pycache__/", re.I),
    re.compile(r"/site-packages/", re.I),
    re.compile(r"\.lock$", re.I),
    re.compile(r"/package-lock\.json$", re.I),
    re.compile(r"/CHANGELOG\.md$", re.I),
    re.compile(r"/CODE_OF_CONDUCT\.md$", re.I),
    re.compile(r"/LICENSE$", re.I),
    re.compile(r"\.png$|\.jpg$|\.jpeg$|\.gif$|\.svg$|\.webp$", re.I),
    re.compile(r"\.pdf$|\.zip$|\.tar\.gz$|\.tgz$", re.I),
]

# ----------------------------------------------------------------------
# Seed list — known agentic AI skill/agent/rule repos + awesome lists
# ----------------------------------------------------------------------
SEEDS = [
    # ---- Anthropic / Claude Code official ----
    "anthropics/anthropic-cookbook",
    "anthropics/courses",
    "anthropics/claude-cookbook",
    "anthropics/skills",
    "anthropics/prompt-eng-interactive-tutorial",

    # ---- Claude Code community ----
    "hesreallyhim/awesome-claude-code",
    "VoltAgent/awesome-claude-code-subagents",
    "wshobson/agents",
    "davila7/claude-code-templates",
    "coding-with-claude/skills",
    "shobro/claude-code-skills",
    "Reaz8/claude-code-subagents",
    "XyLe-USD/claude-code-skills",
    "mgonzalezgio/claude-code-skills",
    "Njengah/claude-code-skills",
    "anthropics/agent-skills",
    "obra/superpowers",
    "shobro/agent-skills",

    # ---- Cursor rules ----
    "biuo/awesome-cursorrules",
    "Pontibus/cursor-rules",
    "alphabotsec/cursorrules",
    "elliotethan/cursor-rules",
    "Yoursnuman/CursorRulesHub",
    "kreciolin/AI-rules",
    "getcursor/cursor",
    "Mikey1369/cursor-rules-collection",
    "danielmiessler/fabric",
    "TheCommunityCave/cursor-rules",
    "PnteIneptique/cursor-rules",

    # ---- Cline / Roo Code ----
    "cline/cline",
    "RooCodeInc/Roo-Code",
    "RooCodeInc/Roo-Code-Docs",
    "greatscottmcclelland/cline-memory-bank",
    "disastrous/mac-cline-bank",
    "cline/awesome-cline-tools",
    "Guitile/cline-rules",
    "pashpashpash/cline-taskmaster",
    "Guitile/cline-Memory-Bank-Anatomy",

    # ---- Aider ----
    "Aider-AI/aider",
    "Aider-AI/aider-cmd",
    "Aider-AI/aider-bench",
    "awesome-aider/awesome-aider",
    "marjamis/aider",

    # ---- OpenHands / SWE-agent / Devin ----
    "All-Hands-AI/OpenHands",
    "All-Hands-AI/openhands-resolvers",
    "princeton-nlp/SWE-agent",
    "princeton-nlp/SWE-bench",
    "CognitionAI/devin-style-swe-bench",

    # ---- Continue / Goose / Copilot ----
    "continuedev/continue",
    "continuedev/continue-docs",
    "block/goose",
    "githubnext/copilot-workspace-user-instructions",

    # ---- AutoGen / CrewAI / LangGraph ----
    "microsoft/autogen",
    "crewAIInc/crewAI",
    "crewAIInc/crewAI-tools",
    "langchain-ai/langgraph",
    "langchain-ai/langgraph-sdk-python",

    # ---- General agent platforms ----
    "OpenInterpreter/open-interpreter",
    "smol-ai/smol-developer",
    "gpt-engineer-org/gpt-engineer",
    "e2b-dev/awesome-ai-agents",
    "humanlayer/12-factor-agents",
    "composiohq/composio",
    "crewAIInc/awesome-crewai",
    "KillianLucas/open-interpreter",

    # ---- Awesome lists / collections (BFS hubs) ----
    "e2b-dev/awesome-ai-agents",
    "punkpeye/awesome-mcp-servers",
    "wshobson/awesome-agentic-coding",
    "stas00/ml-engineering",
    "polmarti/ai-agent-tools",
    "davila7/awesome-claude-code",
    "sbensu/awesome-claude-code",
    "draeger-lat/awesome-ai-agents",
    "Fechin/reference",
    "yuheiy/awesome-cursorrules",
    "WorksApplications/awesome-claude-code-subagents",
    "SimFG/awesome-claude-code",

    # ---- MCP servers (skill-adjacent) ----
    "modelcontextprotocol/servers",
    "modelcontextprotocol/python-sdk",
    "punkpeye/awesome-mcp-servers",

    # ---- Misc skills collections ----
    "obra/superpowers",
    "Gearmate/gearmate-skills",
    "simonw/llm",
    "simonw/datasette",
    "Arindam200/awesome-agentic-workflows",
]

# Deduplicate seeds while preserving order
SEEDS = list(dict.fromkeys(SEEDS))

# ----------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------
def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_PATH, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")

# ----------------------------------------------------------------------
# State persistence (so we can resume)
# ----------------------------------------------------------------------
def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"discovered_repos": [], "cloned_repos": [], "extracted_files": 0,
            "phase_completed": []}

def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2))

# ----------------------------------------------------------------------
# Phase 1: git clone --depth=1
# ----------------------------------------------------------------------
def repo_local_path(repo: str) -> Path:
    return CACHE_DIR / repo.replace("/", "__")

def clone_repo(repo: str, depth: int = 1) -> bool:
    """Clone repo with --depth=1. Returns True on success or already exists."""
    local = repo_local_path(repo)
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
# Phase 2: BFS — parse README.md for github.com links to other repos
# ----------------------------------------------------------------------
GITHUB_LINK_RE = re.compile(
    r"github\.com/([A-Za-z0-9](?:[A-Za-z0-9\-]{0,38}[A-Za-z0-9])/([A-Za-z0-9._\-]+))",
    re.IGNORECASE,
)

def discover_repos_from_readme(repo_path: Path) -> list[str]:
    """Scan README files for github.com links to other repos."""
    found = []
    for readme_name in ["README.md", "readme.md", "README.MD", "README.rst", "README"]:
        readme = repo_path / readme_name
        if not readme.exists():
            continue
        try:
            text = readme.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for m in GITHUB_LINK_RE.finditer(text):
            owner, name = m.group(1), m.group(2)
            # filter out non-repo matches
            name = name.rstrip("/.")
            if name.lower() in {"github", "about", "features", "pricing", "login",
                                "signup", "topics", "trending", "collections",
                                "events", "sponsors", "settings", "notifications",
                                "explore", "marketplace", "search", "new",
                                "orgs", "organizations"}:
                continue
            if "." in name and not name.endswith((".git", ".md")):
                continue
            full = f"{owner}/{name}"
            found.append(full)
    return list(dict.fromkeys(found))

# ----------------------------------------------------------------------
# Phase 3: extract skill/agent/rule files from a cloned repo
# ----------------------------------------------------------------------
def is_skill_file(rel_path: str) -> bool:
    """Return True if rel_path matches any skill file pattern."""
    for skip_re in SKIP_PATTERNS:
        if skip_re.search(rel_path):
            return False
    for skill_re in SKILL_FILE_PATTERNS:
        if skill_re.search(rel_path):
            return True
    return False

def detect_framework(rel_path: str, repo_name: str) -> str:
    """Best-effort framework detection from path + repo name."""
    rp = rel_path.lower()
    rn = repo_name.lower()
    # explicit path indicators
    if ".cursor" in rp or ".cursorrules" in rp or rp.endswith(".mdc"):
        return "cursor"
    if ".cline" in rp or "clinerules" in rp or "cline-rules" in rp:
        return "cline"
    if ".roo/" in rp:
        return "roo"
    if ".aider" in rp or "conventions.md" in rp or "aider-cmd" in rp:
        return "aider"
    if ".continue" in rp:
        return "continue"
    if ".goose" in rp:
        return "goose"
    if "copilot-instructions" in rp:
        return "copilot"
    if "openhands" in rp or "open_hands" in rp:
        return "openhands"
    if "swe-agent" in rp or "swe_agent" in rp:
        return "swe-agent"
    if rp.endswith("agents.md"):
        return "codex"
    if rp.endswith("skill.md") or "/skills/" in rp:
        return "claude-code"
    # repo name fallbacks
    for fw in ["cursor", "cline", "aider", "openhands", "swe-agent",
               "continue", "goose", "autogen", "crewai", "langgraph", "roo"]:
        if fw in rn or fw.replace("-", "") in rn:
            return fw
    return "general"

def extract_files_from_repo(repo: str) -> list[dict]:
    """Walk repo and return list of extracted file records."""
    local = repo_local_path(repo)
    if not local.exists():
        return []
    records = []
    for root, dirs, files in os.walk(local):
        # prune
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
            # target path: _raw/<framework>/<repo>/<rel>
            safe_rel = rel.replace("/", "__").lstrip(".")
            target = RAW_DIR / framework / repo.replace("/", "__") / safe_rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
            records.append({
                "source_repo": repo,
                "framework": framework,
                "original_path": rel,
                "extracted_path": str(target.relative_to(ROOT)),
                "size_bytes": len(content.encode("utf-8")),
                "line_count": content.count("\n") + 1,
                "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            })
    return records

# ----------------------------------------------------------------------
# Phase 4 (optional): GitHub Search API for additional discovery
# ----------------------------------------------------------------------
def github_search_repos(query: str, per_page: int = 30) -> list[str]:
    """Use GitHub Search API. Unauthenticated = 10 req/min, 60/hr."""
    url = "https://api.github.com/search/repositories"
    try:
        r = SESSION.get(url, params={"q": query, "sort": "stars",
                                      "order": "desc", "per_page": per_page},
                        timeout=20,
                        headers={"Accept": "application/vnd.github+json"})
        if r.status_code == 403:
            log(f"  RATE LIMITED on search")
            return []
        if r.status_code != 200:
            log(f"  search HTTP {r.status_code}")
            return []
        items = r.json().get("items", [])
        return [f"{it['owner']['login']}/{it['name']}" for it in items]
    except Exception as e:
        log(f"  search error: {e}")
        return []

# ----------------------------------------------------------------------
# Main orchestration
# ----------------------------------------------------------------------
def main():
    log("=" * 70)
    log("THE LORD OF THE SKILLS — Master Crawler starting")
    log(f"Seeds: {len(SEEDS)} | Cache: {CACHE_DIR} | Raw: {RAW_DIR}")
    log("=" * 70)

    state = load_state()
    discovered = set(state["discovered_repos"])
    cloned = set(state["cloned_repos"])
    completed_phases = set(state.get("phase_completed", []))
    all_records = []

    # Always include seeds in discovered
    discovered.update(SEEDS)

    # ---- Phase 1: clone all seeds (resumable) ----
    if "phase1" not in completed_phases:
        log(f"\n[Phase 1] Cloning {len(SEEDS)} seed repos")
        for i, repo in enumerate(SEEDS, 1):
            if repo in cloned:
                continue
            log(f"    [{i}/{len(SEEDS)}] cloning {repo}")
            ok = clone_repo(repo)
            if ok:
                cloned.add(repo)
            # save state every 10 repos so we can resume
            if i % 10 == 0:
                save_state({"discovered_repos": sorted(discovered),
                           "cloned_repos": sorted(cloned),
                           "extracted_files": 0,
                           "phase_completed": []})
        completed_phases.add("phase1")
        save_state({"discovered_repos": sorted(discovered),
                   "cloned_repos": sorted(cloned),
                   "extracted_files": 0,
                   "phase_completed": sorted(completed_phases)})
        log(f"[Phase 1 complete] Cloned {len(cloned)} seed repos")
    else:
        log(f"\n[Phase 1] SKIP (already complete) — {len(cloned)} repos cloned")

    # ---- Phase 2: BFS-expand from cloned seed READMEs ----
    if "phase2" not in completed_phases:
        log(f"\n[Phase 2] BFS expansion from {len(cloned)} cloned seed READMEs")
        bfs_added = 0
        bfs_cap = 300  # hard cap on BFS discovery to keep things sane
        for i, repo in enumerate(sorted(cloned), 1):
            if i % 20 == 0:
                log(f"    progress {i}/{len(cloned)} | BFS-discovered: {len(discovered)}")
                save_state({"discovered_repos": sorted(discovered),
                           "cloned_repos": sorted(cloned),
                           "extracted_files": 0,
                           "phase_completed": sorted(completed_phases)})
            new_repos = discover_repos_from_readme(repo_local_path(repo))
            for nr in new_repos:
                if nr not in discovered and nr.count("/") == 1 and len(discovered) < bfs_cap + len(SEEDS):
                    discovered.add(nr)
                    bfs_added += 1
        log(f"  BFS added {bfs_added} new repos. Total discovered: {len(discovered)}")
        completed_phases.add("phase2")
        save_state({"discovered_repos": sorted(discovered),
                   "cloned_repos": sorted(cloned),
                   "extracted_files": 0,
                   "phase_completed": sorted(completed_phases)})
    else:
        log(f"\n[Phase 2] SKIP (already complete)")

    # ---- Phase 3: GitHub Search API expansion (rate-limited) ----
    if "phase3" not in completed_phases:
        SEARCH_QUERIES = [
            "filename:SKILL.md agentic",
            "filename:AGENTS.md agent",
            "filename:.cursorrules",
            "cursorrules collection",
            "cline rules memory bank",
            "aider CONVENTIONS.md",
            "awesome claude code skills",
            "claude code subagents",
        ]
        log(f"\n[Phase 3] GitHub Search API expansion ({len(SEARCH_QUERIES)} queries)")
        search_added = 0
        for q in SEARCH_QUERIES:
            log(f"  searching: {q}")
            repos = github_search_repos(q, per_page=20)
            for r in repos:
                if r not in discovered:
                    discovered.add(r)
                    search_added += 1
            time.sleep(7)
        log(f"  Search added {search_added} new repos. Total: {len(discovered)}")
        completed_phases.add("phase3")
        save_state({"discovered_repos": sorted(discovered),
                   "cloned_repos": sorted(cloned),
                   "extracted_files": 0,
                   "phase_completed": sorted(completed_phases)})
    else:
        log(f"\n[Phase 3] SKIP (already complete)")

    # ---- Phase 4: clone all discovered repos not yet cloned ----
    if "phase4" not in completed_phases:
        to_clone = [r for r in discovered if r not in cloned]
        log(f"\n[Phase 4] Cloning {len(to_clone)} additional discovered repos")
        for i, repo in enumerate(to_clone, 1):
            log(f"    [{i}/{len(to_clone)}] cloning {repo}")
            ok = clone_repo(repo)
            if ok:
                cloned.add(repo)
            if i % 10 == 0:
                save_state({"discovered_repos": sorted(discovered),
                           "cloned_repos": sorted(cloned),
                           "extracted_files": 0,
                           "phase_completed": sorted(completed_phases)})
        completed_phases.add("phase4")
        save_state({"discovered_repos": sorted(discovered),
                   "cloned_repos": sorted(cloned),
                   "extracted_files": 0,
                   "phase_completed": sorted(completed_phases)})
        log(f"[Phase 4 complete] Total cloned: {len(cloned)}")
    else:
        log(f"\n[Phase 4] SKIP (already complete)")

    # ---- Phase 5: extract skill files from every cloned repo ----
    log(f"\n[Phase 5] Extracting skill/agent/rule files from {len(cloned)} repos")
    for i, repo in enumerate(sorted(cloned), 1):
        if i % 25 == 0:
            log(f"    progress {i}/{len(cloned)} | files so far: {len(all_records)}")
        records = extract_files_from_repo(repo)
        all_records.extend(records)
    log(f"\n[Phase 5 complete] Extracted {len(all_records)} files total")

    # ---- Write manifest ----
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total_discovered_repos": len(discovered),
        "total_cloned_repos": len(cloned),
        "total_extracted_files": len(all_records),
        "frameworks_detected": sorted({r["framework"] for r in all_records}),
        "files": all_records,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))
    log(f"\nManifest written to {MANIFEST_PATH}")
    log(f"  - Discovered: {len(discovered)} repos")
    log(f"  - Cloned:     {len(cloned)} repos")
    log(f"  - Extracted:  {len(all_records)} skill/agent/rule files")
    log(f"  - Frameworks: {', '.join(manifest['frameworks_detected'])}")

    save_state({"discovered_repos": sorted(discovered),
               "cloned_repos": sorted(cloned),
               "extracted_files": len(all_records),
               "phase_completed": sorted(completed_phases | {"phase5"})})
    log("\nDONE.")

if __name__ == "__main__":
    main()
