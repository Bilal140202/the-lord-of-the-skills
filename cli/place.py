#!/usr/bin/env python3
"""
lotr place — Smart per-framework skill placer.

Drops fetched skill files in the exact right location for each framework.
Handles:
  - Directory creation (mkdir -p)
  - File-append mode for convention files (CONVENTIONS.md, AGENTS.md)
  - Home-dir expansion (~/.claude/skills/)
  - Conflict resolution (don't overwrite existing files)
"""
from __future__ import annotations
import os
from pathlib import Path
from typing import Optional

# Per-framework destination rules.
# - "dir" → copy file into this directory
# - "append" → append file content to this single file
# - "stdout" → print to stdout (don't write to disk)
DESTINATIONS: dict[str, dict] = {
    "antigravity": {"mode": "dir",    "path": ".antigravity/skills/"},
    "cursor":      {"mode": "dir",    "path": ".cursor/rules/"},
    "claude-code": {"mode": "dir",    "path": "~/.claude/skills/"},
    "cline":       {"mode": "dir",    "path": ".clinerules/"},
    "roo":         {"mode": "dir",    "path": ".roo/rules/"},
    "continue":    {"mode": "dir",    "path": ".continue/rules/"},
    "goose":       {"mode": "dir",    "path": ".goose/extensions/"},
    "aider":       {"mode": "append", "path": "CONVENTIONS.md"},
    "codex":       {"mode": "append", "path": "AGENTS.md"},
    "copilot":     {"mode": "append", "path": ".github/copilot-instructions.md"},
}

def resolve_destination(framework: str, project_root: Path | str = ".") -> Path:
    """Resolve the destination path for a framework, given a project root.

    For "dir" mode: returns the directory path (created if needed).
    For "append" mode: returns the file path (parent dir created if needed).

    Args:
        framework: e.g., "claude-code", "cursor"
        project_root: Project directory (for relative paths)

    Returns:
        Absolute Path to the destination (dir or file).
    """
    if framework not in DESTINATIONS:
        raise ValueError(f"Unknown framework: {framework}. Known: {list(DESTINATIONS)}")
    rule = DESTINATIONS[framework]
    raw_path = rule["path"]
    # Expand ~
    if raw_path.startswith("~"):
        dest = Path(raw_path).expanduser()
    else:
        dest = Path(project_root) / raw_path
    # Resolve to absolute
    dest = dest.resolve()
    # Create parent dirs
    if rule["mode"] == "dir":
        dest.mkdir(parents=True, exist_ok=True)
    else:  # append
        dest.parent.mkdir(parents=True, exist_ok=True)
    return dest

def place_skill(framework: str, content: str, filename: str,
                project_root: Path | str = ".",
                overwrite: bool = False) -> Path:
    """Place a single skill file in the right location.

    Args:
        framework: Target framework
        content: File content (string)
        filename: Original filename (used for "dir" mode)
        project_root: Project directory
        overwrite: If True, overwrite existing files. Default False (suffix _1, _2, etc.)

    Returns:
        Path to the written file.
    """
    if framework not in DESTINATIONS:
        raise ValueError(f"Unknown framework: {framework}")
    rule = DESTINATIONS[framework]
    dest = resolve_destination(framework, project_root)
    if rule["mode"] == "dir":
        # Write to dest/filename
        target = dest / filename
        # Strip canonical__ prefix for cleaner install
        if target.name.startswith("canonical__"):
            target = dest / target.name[len("canonical__"):]
        # Conflict resolution
        if target.exists() and not overwrite:
            stem = Path(target.name).stem
            suffix = Path(target.name).suffix
            n = 1
            while target.exists():
                target = dest / f"{stem}_{n}{suffix}"
                n += 1
        target.write_text(content, encoding="utf-8")
        return target
    elif rule["mode"] == "append":
        # Append to existing file (with separator if non-empty)
        if dest.exists() and dest.stat().st_size > 0:
            existing = dest.read_text(encoding="utf-8")
            separator = "\n\n---\n\n<!-- Appended by lotr CLI -->\n\n"
            content = existing.rstrip() + separator + content
        dest.write_text(content, encoding="utf-8")
        return dest
    else:
        raise ValueError(f"Unknown mode: {rule['mode']}")

def list_installed(framework: str, project_root: Path | str = ".") -> list[Path]:
    """List skill files already installed for a framework.

    Args:
        framework: Target framework
        project_root: Project directory

    Returns:
        List of paths to installed skill files.
    """
    if framework not in DESTINATIONS:
        raise ValueError(f"Unknown framework: {framework}")
    rule = DESTINATIONS[framework]
    raw_path = rule["path"]
    if raw_path.startswith("~"):
        dest = Path(raw_path).expanduser()
    else:
        dest = Path(project_root) / raw_path
    dest = dest.resolve()
    if rule["mode"] == "dir":
        if not dest.is_dir():
            return []
        # List .md, .mdc, .cursorrules, .yaml files
        results = []
        for ext in ["*.md", "*.mdc", "*.cursorrules", "*.yaml", "*.yml", "*.json"]:
            results.extend(dest.glob(ext))
        return sorted(results)
    else:  # append
        if dest.is_file():
            return [dest]
        return []

if __name__ == "__main__":
    import sys
    fw = sys.argv[1] if len(sys.argv) > 1 else "claude-code"
    root = sys.argv[2] if len(sys.argv) > 2 else "."
    dest = resolve_destination(fw, root)
    print(f"Framework: {fw}")
    print(f"Mode:      {DESTINATIONS[fw]['mode']}")
    print(f"Path:      {dest}")
    installed = list_installed(fw, root)
    print(f"Installed: {len(installed)} files")
    for f in installed[:5]:
        print(f"  - {f.name}")
