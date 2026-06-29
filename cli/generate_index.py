#!/usr/bin/env python3
"""
Generate skills/index.json — machine-readable manifest for the lotr CLI.

Walks the skills/<kingdom>/<framework>/<repo>/ tree and builds an index of
all canonical__ skills with: title, kingdom, frameworks, tags, path, filename,
canonical flag, summary (first 200 chars).

Output: skills/index.json
"""
from __future__ import annotations
import json
import re
import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone

REPO_ROOT = Path("/home/z/my-project/repo-push")
SKILLS_DIR = REPO_ROOT / "skills"
OUT_PATH = SKILLS_DIR / "index.json"

KINGDOM_DOMAINS = {
    "gondor": "Coding & Software Engineering",
    "rivendell": "Research & Knowledge",
    "moria": "DevOps & Infrastructure",
    "lothlorien": "Data & Analysis",
    "mordor": "Security & Auditing",
    "the-shire": "Writing & Content",
    "isengard": "Agents & Orchestration",
    "rohan": "Testing & Verification",
    "fangorn": "Documentation & Memory",
    "mirkwood": "Specialized & Niche",
}

# Tag-extraction keywords per kingdom
KINGDOM_TAGS = {
    "gondor": ["coding", "refactor", "debug", "git", "typescript", "react", "api", "build",
               "code-review", "frontend", "backend", "nextjs", "node", "database"],
    "rivendell": ["research", "analyze", "literature", "methodology", "synthesis", "citation"],
    "moria": ["devops", "kubernetes", "docker", "terraform", "aws", "ci-cd", "deploy",
              "cloud", "monitoring", "nginx"],
    "lothlorien": ["data", "etl", "pandas", "numpy", "ml", "statistics", "visualization",
                   "jupyter", "eda"],
    "mordor": ["security", "vulnerability", "owasp", "xss", "csrf", "crypto", "pentest",
               "audit", "auth"],
    "the-shire": ["writing", "blog", "docs", "readme", "marketing", "content", "tutorial"],
    "isengard": ["agent", "subagent", "orchestration", "workflow", "multi-agent", "delegation"],
    "rohan": ["test", "verify", "assert", "coverage", "lint", "typecheck", "tdd", "e2e"],
    "fangorn": ["memory", "context", "rag", "embedding", "knowledge-base", "session"],
    "mirkwood": ["specialized", "niche", "experimental"],
}

def extract_title(content: str, filename: str) -> str:
    """Title from frontmatter, H1, or filename."""
    m = re.search(r"^title:\s*(.+)$", content, re.MULTILINE)
    if m:
        return m.group(1).strip().strip("\"'")[:120]
    m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if m:
        return m.group(1).strip()[:120]
    name = filename
    if name.startswith("canonical__"):
        name = name[len("canonical__"):]
    return name.rsplit(".", 1)[0].replace("-", " ").replace("_", " ").title()[:120]

def extract_summary(content: str, max_len: int = 200) -> str:
    """First substantive paragraph."""
    text = content
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4:]
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", "```", "---", "|", ">", "- ", "* ")):
            continue
        return s[:max_len] + ("..." if len(s) > max_len else "")
    return ""

def extract_tags(content: str, kingdom: str, framework: str) -> list[str]:
    """Extract tags from content + kingdom + framework."""
    text_lower = (content + " " + kingdom + " " + framework).lower()
    tags = set()
    # Kingdom tags
    for tag in KINGDOM_TAGS.get(kingdom, []):
        if tag in text_lower or tag.replace("-", " ") in text_lower:
            tags.add(tag)
    # Framework tag
    tags.add(framework)
    # Always add kingdom
    tags.add(kingdom)
    # Detect common tech
    for tech, pattern in [("typescript", r"\btypescript\b"), ("python", r"\bpython\b"),
                          ("react", r"\breact\b"), ("next", r"\bnext\.?js\b"),
                          ("rust", r"\brust\b"), ("go", r"\bgo lang\b"),
                          ("docker", r"\bdocker\b"), ("k8s", r"\bkubernetes\b"),
                          ("api", r"\bapi\b"), ("database", r"\b(database|sql|postgres)\b")]:
        if re.search(pattern, text_lower):
            tags.add(tech)
    return sorted(tags)[:15]

def main():
    print(f"Generating skills/index.json from {SKILLS_DIR}...")
    skills = []
    kingdom_counts = defaultdict(int)
    framework_counts = defaultdict(int)
    canonical_count = 0
    seen_paths = set()

    # Walk skills/<kingdom>/<framework>/<repo>/<file>
    for kingdom_dir in sorted(SKILLS_DIR.iterdir()):
        if not kingdom_dir.is_dir() or kingdom_dir.name.startswith("."):
            continue
        kingdom = kingdom_dir.name
        if kingdom not in KINGDOM_DOMAINS:
            continue
        for framework_dir in sorted(kingdom_dir.iterdir()):
            if not framework_dir.is_dir():
                continue
            framework = framework_dir.name
            for repo_dir in sorted(framework_dir.iterdir()):
                if not repo_dir.is_dir():
                    continue
                repo_name = repo_dir.name.replace("__", "/")
                for skill_file in sorted(repo_dir.iterdir()):
                    if not skill_file.is_file():
                        continue
                    # Skip READMEs (kingdom-level docs, not skills)
                    if skill_file.name == "README.md":
                        continue
                    # Skip non-text files
                    if skill_file.suffix not in {".md", ".mdc", ".yaml", ".yml",
                                                  ".json", ".cursorrules", ".clinerules",
                                                  ".toml", ".txt"}:
                        continue
                    rel_path = skill_file.relative_to(REPO_ROOT).as_posix()
                    if rel_path in seen_paths:
                        continue
                    seen_paths.add(rel_path)
                    is_canonical = skill_file.name.startswith("canonical__")
                    if is_canonical:
                        canonical_count += 1
                    try:
                        content = skill_file.read_text(encoding="utf-8", errors="ignore")
                    except Exception:
                        content = ""
                    title = extract_title(content, skill_file.name)
                    summary = extract_summary(content)
                    tags = extract_tags(content, kingdom, framework)
                    # The "frameworks" field lists which frameworks this skill is available for.
                    # For canonical skills, we try to find all frameworks that have the same title.
                    # For simplicity, just list the current framework.
                    skills.append({
                        "id": f"{kingdom}/{framework}/{repo_dir.name}/{skill_file.name}",
                        "title": title,
                        "kingdom": kingdom,
                        "kingdom_label": KINGDOM_DOMAINS[kingdom],
                        "frameworks": [framework],
                        "canonical": is_canonical,
                        "tags": tags,
                        "source_repo": repo_name,
                        "filename": skill_file.name,
                        "path": rel_path,
                        "summary": summary,
                        "size_bytes": len(content.encode("utf-8")),
                    })
                    kingdom_counts[kingdom] += 1
                    framework_counts[framework] += 1

    # Build index
    index = {
        "version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "repo": "Bilal140202/the-lord-of-the-skills",
        "raw_base": "https://raw.githubusercontent.com/Bilal140202/the-lord-of-the-skills/main",
        "total_skills": len(skills),
        "canonical_count": canonical_count,
        "kingdoms": dict(kingdom_counts),
        "frameworks": dict(framework_counts),
        "skills": skills,
    }

    OUT_PATH.write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"✓ Wrote {OUT_PATH}")
    print(f"  Total skills: {len(skills)}")
    print(f"  Canonical ⭐: {canonical_count}")
    print(f"  Kingdoms: {dict(kingdom_counts)}")
    print(f"  Frameworks: {dict(framework_counts)}")
    print(f"  Size: {OUT_PATH.stat().st_size // 1024} KB")

if __name__ == "__main__":
    main()
