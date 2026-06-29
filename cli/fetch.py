#!/usr/bin/env python3
"""
lotr fetch — GitHub raw skill downloader.

Fetches skill files from the Lord of the Skills GitHub repo via raw URLs.
No git clone needed — instant download via HTTPS.

Uses the skills/index.json manifest for lookups when available;
falls back to constructing raw URLs from kingdom/framework/skill name.
"""
from __future__ import annotations
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, List, Dict

# Base URL for raw file fetches
RAW_BASE = "https://raw.githubusercontent.com/Bilal140202/the-lord-of-the-skills/main"
INDEX_URL = f"{RAW_BASE}/skills/index.json"

# Local cache for the index (avoids re-downloading on every command)
_CACHE_DIR = Path.home() / ".lotr" / "cache"
_CACHE_INDEX = _CACHE_DIR / "index.json"
_CACHE_TTL_SECONDS = 3600  # 1 hour

def _http_get(url: str, timeout: int = 30) -> bytes:
    """Simple HTTP GET with User-Agent. Returns bytes."""
    req = urllib.request.Request(url, headers={
        "User-Agent": "lotr-cli/1.0 (+https://github.com/Bilal140202/the-lord-of-the-skills)",
        "Accept": "*/*",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def fetch_index(force_refresh: bool = False) -> Dict:
    """Fetch the skills/index.json manifest (with caching).

    Falls back to a local copy in the repo if the remote fetch fails
    (useful during development and pre-push testing).

    Args:
        force_refresh: If True, bypass cache and download fresh.

    Returns:
        Parsed JSON manifest dict.
    """
    import time
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    # Check cache
    if not force_refresh and _CACHE_INDEX.exists():
        age = time.time() - _CACHE_INDEX.stat().st_mtime
        if age < _CACHE_TTL_SECONDS:
            try:
                return json.loads(_CACHE_INDEX.read_text(encoding="utf-8"))
            except Exception:
                pass  # cache corrupt, re-download
    # Download fresh
    try:
        data = _http_get(INDEX_URL)
        manifest = json.loads(data)
        _CACHE_INDEX.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return manifest
    except Exception as e:
        # Fall back to cache even if stale
        if _CACHE_INDEX.exists():
            try:
                return json.loads(_CACHE_INDEX.read_text(encoding="utf-8"))
            except Exception:
                pass
        # Last resort: look for a local copy in the repo (dev mode)
        # Walk up from cli/ to find skills/index.json
        local_index = Path(__file__).parent.parent / "skills" / "index.json"
        if local_index.exists():
            try:
                return json.loads(local_index.read_text(encoding="utf-8"))
            except Exception:
                pass
        raise RuntimeError(f"Failed to fetch skills index from {INDEX_URL}: {e}")

def fetch_skill(kingdom: str, framework: str, skill_path: str, timeout: int = 30) -> str:
    """Fetch a single skill file's content from GitHub raw.

    Falls back to local repo copy if remote fetch fails (dev mode).

    Args:
        kingdom: e.g., "gondor"
        framework: e.g., "claude-code"
        skill_path: path relative to skills/<kingdom>/<framework>/ (e.g., "anthropics__skills/canonical__SKILL.md")
        timeout: HTTP timeout in seconds

    Returns:
        File content as string.
    """
    url = f"{RAW_BASE}/skills/{kingdom}/{framework}/{skill_path}"
    try:
        return _http_get(url, timeout=timeout).decode("utf-8")
    except Exception:
        # Fall back to local copy (dev mode)
        local = Path(__file__).parent.parent / "skills" / kingdom / framework / skill_path
        if local.exists():
            return local.read_text(encoding="utf-8")
        raise FileNotFoundError(f"Skill not found at {url} (and no local copy at {local})")

def fetch_skills_by_index(index: Dict, kingdom: Optional[str] = None,
                           framework: Optional[str] = None,
                           canonical_only: bool = True,
                           tags: Optional[List[str]] = None,
                           limit: Optional[int] = None) -> List[Dict]:
    """Query the index for matching skills.

    Args:
        index: The parsed index.json manifest
        kingdom: Filter by kingdom (None = all)
        framework: Filter by framework (None = all)
        canonical_only: Only return canonical ⭐ skills
        tags: Filter by tags (any match)
        limit: Max results to return

    Returns:
        List of skill dicts from the index.
    """
    skills = index.get("skills", [])
    results = []
    for skill in skills:
        if kingdom and skill.get("kingdom") != kingdom:
            continue
        if framework and framework not in skill.get("frameworks", []):
            continue
        if canonical_only and not skill.get("canonical", False):
            continue
        if tags:
            skill_tags = set(skill.get("tags", []))
            if not skill_tags.intersection(tags):
                continue
        results.append(skill)
    if limit:
        results = results[:limit]
    return results

def fetch_and_save(skill: Dict, dest_dir: Path, timeout: int = 30) -> Path:
    """Fetch a skill (from index entry) and save to dest_dir.

    Uses the skill's title (slugified) as the filename for readability.
    Falls back to the original filename if no title.

    Args:
        skill: Index entry with at least {kingdom, frameworks[0], path, filename}
        dest_dir: Where to save the file
        timeout: HTTP timeout

    Returns:
        Path to the saved file.
    """
    kingdom = skill["kingdom"]
    framework = skill.get("frameworks", ["general"])[0]
    path = skill["path"]
    # Strip "skills/kingdom/framework/" prefix to get the relative path
    rel_path = path
    for prefix in [f"skills/{kingdom}/{framework}/", f"skills/{kingdom}/"]:
        if rel_path.startswith(prefix):
            rel_path = rel_path[len(prefix):]
            break
    content = fetch_skill(kingdom, framework, rel_path, timeout=timeout)
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Prefer title-based filename (cleaner than mangled canonical__ names)
    title = skill.get("title")
    original_filename = skill.get("filename") or Path(rel_path).name
    # Determine extension from original
    ext = Path(original_filename).suffix or ".md"
    if title and title != "(untitled)":
        # Slugify the title
        import re
        slug = re.sub(r"[^A-Za-z0-9._-]+", "-", title.lower()).strip("-")
        slug = re.sub(r"-+", "-", slug)[:60]  # cap length
        filename = f"{slug}{ext}"
    else:
        # Fall back to original filename, strip canonical__ prefix
        filename = original_filename
        if filename.startswith("canonical__"):
            filename = filename[len("canonical__"):]

    dest = dest_dir / filename
    # Avoid overwriting existing files
    n = 1
    while dest.exists():
        stem = Path(filename).stem
        suffix = Path(filename).suffix
        dest = dest_dir / f"{stem}_{n}{suffix}"
        n += 1
    dest.write_text(content, encoding="utf-8")
    return dest

if __name__ == "__main__":
    # Demo: fetch the index and print stats
    print("Fetching skills index...")
    idx = fetch_index()
    print(f"Total skills in index: {len(idx.get('skills', []))}")
    print(f"Index version: {idx.get('version', 'unknown')}")
    print(f"Generated at: {idx.get('generated_at', 'unknown')}")
    # Sample
    for s in idx.get("skills", [])[:3]:
        print(f"  - {s.get('title')}: {s.get('kingdom')}/{s.get('frameworks')}")
