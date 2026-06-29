#!/usr/bin/env python3
"""
lotr — The Lord of the Skills CLI

One-command smart skills installer for any agentic AI framework.

Usage:
  lotr "update the UI to be more modern"     # Natural language (auto-detects everything)
  lotr install --task "add authentication"   # Explicit install
  lotr preview "write unit tests"            # Dry-run: show what would be installed
  lotr list                                  # List available skills for detected stack
  lotr update                                # Update all installed skills to latest
  lotr detect                                # Show detected framework + stack
  lotr kingdoms                              # List all 10 kingdoms
  lotr search "code review"                  # Search the index by keyword

Examples:
  $ cd my-react-project/
  $ lotr "write unit tests for the API"
  [detect] framework=claude-code  language=typescript  stack=[react, next]
  [match]  intent="write unit tests for the API" → rohan (score=3, kws=[test, unit, tests])
  [fetch]  3 canonical skills found for rohan/claude-code
  [place]  ~/.claude/skills/canonical__test-coverage.md
  [place]  ~/.claude/skills/canonical__unit-test-writer.md
  [place]  ~/.claude/skills/canonical__assertion-helper.md
  ✓ Installed 3 skills in 2.1s
"""
from __future__ import annotations
import argparse
import json
import sys
import time
from pathlib import Path
from typing import Optional

# Add cli/ to path so we can import sibling modules
CLI_DIR = Path(__file__).parent.resolve()
if str(CLI_DIR) not in sys.path:
    sys.path.insert(0, str(CLI_DIR))

from detect import detect as detect_stack
from match import match as match_intent, match_kingdoms
from fetch import fetch_index, fetch_skills_by_index, fetch_and_save
from place import resolve_destination, place_skill, list_installed, DESTINATIONS

# Kingdom data (for `lotr kingdoms` command)
KINGDOMS = {
    "gondor":      {"name": "Gondor",       "domain": "Coding & Software Engineering",  "symbol": "⚔"},
    "rivendell":   {"name": "Rivendell",    "domain": "Research & Knowledge",           "symbol": "✦"},
    "moria":       {"name": "Moria",        "domain": "DevOps & Infrastructure",        "symbol": "⛏"},
    "lothlorien":  {"name": "Lothlórien",   "domain": "Data & Analysis",                "symbol": "✿"},
    "mordor":      {"name": "Mordor",       "domain": "Security & Auditing",            "symbol": "👁"},
    "the-shire":   {"name": "The Shire",    "domain": "Writing & Content",              "symbol": "✎"},
    "isengard":    {"name": "Isengard",     "domain": "Agents & Orchestration",         "symbol": "⚙"},
    "rohan":       {"name": "Rohan",        "domain": "Testing & Verification",         "symbol": "🐴"},
    "fangorn":     {"name": "Fangorn",      "domain": "Documentation & Memory",         "symbol": "🌳"},
    "mirkwood":    {"name": "Mirkwood",     "domain": "Specialized & Niche",            "symbol": "🕸"},
}

# ANSI colors (auto-disabled if not a TTY)
_USE_COLOR = sys.stdout.isatty()
_COLORS = {"gold": "\033[33m", "green": "\033[32m", "red": "\033[31m",
           "blue": "\033[34m", "gray": "\033[90m", "bold": "\033[1m",
           "reset": "\033[0m"}
def c(text: str, color: str) -> str:
    if not _USE_COLOR:
        return text
    return f"{_COLORS.get(color, '')}{text}{_COLORS['reset']}"

def banner():
    print(c("⚔ THE LORD OF THE SKILLS — CLI v1.0", "gold"))
    print(c("  One command. Any framework. Any kingdom.", "gray"))
    print()

def cmd_detect(args):
    """Detect and print framework + stack for the current project."""
    banner()
    print(c("[detect]", "bold"), "Scanning project...")
    result = detect_stack(args.project_root)
    print(f"  Framework:  {c(result['framework'] or '(none detected)', 'gold')}")
    print(f"  Language:   {c(result['language'], 'blue')}")
    print(f"  Stack:      {c(str(result['stack']), 'blue')}")
    print(f"  Project:    {c(result['project_root'], 'gray')}")
    if not result['framework']:
        print()
        print(c("  ⚠ No agent framework detected.", "red"))
        print(c("    Install one of: .cursor/, .claude/, .clinerules/, .roo/, AGENTS.md, etc.", "gray"))
    return 0

def cmd_kingdoms(args):
    """List all 10 kingdoms."""
    banner()
    print(c("The Ten Kingdoms:", "bold"))
    print()
    for k, info in KINGDOMS.items():
        print(f"  {c(info['symbol'], 'gold')} {c(info['name'], 'bold'):14s} "
              f"{c(info['domain'], 'blue')}")
    return 0

def cmd_search(args):
    """Search the index by keyword."""
    banner()
    query = args.query.lower()
    print(c(f"[search] {query!r}", "bold"))
    try:
        idx = fetch_index()
    except Exception as e:
        print(c(f"  ✗ Failed to fetch index: {e}", "red"))
        return 1
    skills = idx.get("skills", [])
    matches = []
    for s in skills:
        title = (s.get("title") or "").lower()
        summary = (s.get("summary") or "").lower()
        tags = [t.lower() for t in s.get("tags", [])]
        if query in title or query in summary or query in tags:
            matches.append(s)
    print(f"  Found {c(str(len(matches)), 'green')} matching skills")
    for s in matches[:20]:
        title = s.get("title", "(untitled)")[:60]
        kingdom = s.get("kingdom", "?")
        fws = ", ".join(s.get("frameworks", []))[:30]
        canon = "⭐" if s.get("canonical") else " "
        print(f"  {canon} {c(title, 'bold'):62s} [{c(kingdom, 'blue')}] {c(fws, 'gray')}")
    if len(matches) > 20:
        print(f"  ... and {len(matches) - 20} more (refine your query)")
    return 0

def cmd_list(args):
    """List available skills for the detected stack."""
    banner()
    print(c("[detect]", "bold"), "Scanning project...")
    result = detect_stack(args.project_root)
    framework = result["framework"]
    print(f"  Framework: {c(framework or '(none)', 'gold')}  Language: {c(result['language'], 'blue')}  Stack: {c(str(result['stack']), 'blue')}")
    if not framework:
        print(c("  ✗ No agent framework detected. Run `lotr detect` for details.", "red"))
        return 1
    print()
    print(c("[list]", "bold"), f"Fetching skills index...")
    try:
        idx = fetch_index()
    except Exception as e:
        print(c(f"  ✗ Failed to fetch index: {e}", "red"))
        return 1
    skills = fetch_skills_by_index(idx, framework=framework, canonical_only=not args.all)
    print(f"  {c(str(len(skills)), 'green')} skills available for {c(framework, 'gold')}")
    print()
    # Group by kingdom
    by_kingdom = {}
    for s in skills:
        k = s.get("kingdom", "unknown")
        by_kingdom.setdefault(k, []).append(s)
    for k in sorted(by_kingdom.keys()):
        info = KINGDOMS.get(k, {"symbol": "?", "name": k.title()})
        print(f"  {c(info['symbol'], 'gold')} {c(info['name'], 'bold')} ({len(by_kingdom[k])})")
        for s in by_kingdom[k][:5]:
            title = (s.get("title") or "(untitled)")[:55]
            canon = "⭐" if s.get("canonical") else " "
            print(f"      {canon} {title}")
        if len(by_kingdom[k]) > 5:
            print(f"      ... and {len(by_kingdom[k]) - 5} more")
    return 0

def cmd_preview(args):
    """Dry-run: show what would be installed for a given intent."""
    banner()
    intent = args.intent
    if not intent:
        print(c("  ✗ No intent provided. Usage: lotr preview \"write unit tests\"", "red"))
        return 1
    print(c("[detect]", "bold"), "Scanning project...")
    result = detect_stack(args.project_root)
    framework = result["framework"] or args.framework
    if not framework:
        print(c("  ✗ No agent framework detected. Pass --framework to override.", "red"))
        return 1
    print(f"  Framework: {c(framework, 'gold')}  Language: {c(result['language'], 'blue')}")
    print()
    print(c("[match]", "bold"), f"Intent: {c(intent, 'gold')!r}")
    matches = match_intent(intent, top_n=3)
    if not matches:
        print(c("  ✗ No kingdoms matched. Try rephrasing.", "red"))
        return 1
    for kingdom, score, kws in matches:
        info = KINGDOMS.get(kingdom, {"symbol": "?", "name": kingdom.title()})
        print(f"  {c(info['symbol'], 'gold')} {c(kingdom, 'bold'):12s} (score={score}, keywords={kws})")
    print()
    print(c("[fetch]", "bold"), "Querying skills index...")
    try:
        idx = fetch_index()
    except Exception as e:
        print(c(f"  ✗ Failed to fetch index: {e}", "red"))
        return 1
    top_kingdom = matches[0][0]
    skills = fetch_skills_by_index(idx, kingdom=top_kingdom, framework=framework,
                                    canonical_only=not args.all, limit=args.limit or 10)
    print(f"  Would install {c(str(len(skills)), 'green')} skills to {c(str(resolve_destination(framework, args.project_root)), 'blue')}")
    for s in skills:
        title = (s.get("title") or "(untitled)")[:60]
        canon = "⭐" if s.get("canonical") else " "
        print(f"    {canon} {title}")
    print()
    print(c("  (dry-run — no files written. Run `lotr install` to actually install.)", "gray"))
    return 0

def cmd_install(args):
    """Install skills for a given intent (or explicit kingdom/framework)."""
    banner()
    intent = args.intent
    if not intent and not (args.kingdom and args.framework):
        print(c("  ✗ Provide an intent OR both --kingdom and --framework.", "red"))
        print(c("  Usage: lotr install \"write unit tests\"", "gray"))
        print(c("  Usage: lotr install --kingdom mordor --framework cursor", "gray"))
        return 1
    t0 = time.time()
    # Detect
    print(c("[detect]", "bold"), "Scanning project...")
    result = detect_stack(args.project_root)
    framework = args.framework or result["framework"]
    if not framework:
        print(c("  ✗ No agent framework detected. Pass --framework to override.", "red"))
        return 1
    print(f"  Framework: {c(framework, 'gold')}  Language: {c(result['language'], 'blue')}  Stack: {c(str(result['stack']), 'blue')}")
    # Match
    kingdom = args.kingdom
    if not kingdom and intent:
        print()
        print(c("[match]", "bold"), f"Intent: {c(intent, 'gold')!r}")
        matches = match_intent(intent, top_n=1)
        if not matches:
            print(c("  ✗ No kingdoms matched. Try rephrasing or use --kingdom.", "red"))
            return 1
        kingdom = matches[0][0]
        score, kws = matches[0][1], matches[0][2]
        info = KINGDOMS.get(kingdom, {"symbol": "?"})
        print(f"  {c(info['symbol'], 'gold')} {c(kingdom, 'bold'):12s} (score={score}, keywords={kws})")
    # Fetch
    print()
    print(c("[fetch]", "bold"), "Querying skills index...")
    try:
        idx = fetch_index()
    except Exception as e:
        print(c(f"  ✗ Failed to fetch index: {e}", "red"))
        return 1
    skills = fetch_skills_by_index(idx, kingdom=kingdom, framework=framework,
                                    canonical_only=not args.all, limit=args.limit or 10)
    if not skills:
        print(c(f"  ✗ No skills found for kingdom={kingdom}, framework={framework}", "red"))
        print(c("  Try: lotr list  to see what's available, or --all to include non-canonical.", "gray"))
        return 1
    print(f"  Found {c(str(len(skills)), 'green')} skills")
    # Place
    print()
    print(c("[place]", "bold"), f"Installing to {c(str(resolve_destination(framework, args.project_root)), 'blue')}")
    installed = []
    for s in skills:
        try:
            path = fetch_and_save(s, resolve_destination(framework, args.project_root))
            installed.append(path)
            title = (s.get("title") or s.get("filename") or "(untitled)")[:60]
            canon = "⭐" if s.get("canonical") else " "
            print(f"  {c('✓', 'green')} {canon} {c(str(path.name), 'bold')}")
        except Exception as e:
            print(f"  {c('✗', 'red')} {s.get('filename', '?')}: {e}")
    elapsed = time.time() - t0
    print()
    print(c(f"✓ Installed {len(installed)} skills in {elapsed:.1f}s", "green"))
    print(c(f"  Next: restart your agent ({framework}) to pick up the new skills.", "gray"))
    return 0

def cmd_update(args):
    """Update installed skills to latest."""
    banner()
    print(c("[detect]", "bold"), "Scanning project...")
    result = detect_stack(args.project_root)
    framework = result["framework"]
    if not framework:
        print(c("  ✗ No agent framework detected.", "red"))
        return 1
    print(f"  Framework: {c(framework, 'gold')}")
    installed = list_installed(framework, args.project_root)
    print(f"  Installed: {c(str(len(installed)), 'green')} skill files")
    if not installed:
        print(c("  Nothing to update.", "gray"))
        return 0
    print()
    print(c("[update]", "bold"), "Force-refreshing index...")
    try:
        idx = fetch_index(force_refresh=True)
    except Exception as e:
        print(c(f"  ✗ Failed to refresh index: {e}", "red"))
        return 1
    print(f"  Index refreshed: {len(idx.get('skills', []))} skills total")
    # For each installed file, try to find a matching index entry and re-download
    updated = 0
    for f in installed:
        # Match by filename
        fname = f.name
        # Strip canonical__ if present
        lookup_name = fname
        if not lookup_name.startswith("canonical__"):
            lookup_name = "canonical__" + lookup_name
        for s in idx.get("skills", []):
            if s.get("filename") == lookup_name and s.get("kingdom") in KINGDOMS:
                # Re-fetch
                try:
                    fetch_and_save(s, resolve_destination(framework, args.project_root))
                    print(f"  {c('✓', 'green')} Updated {fname}")
                    updated += 1
                    break
                except Exception:
                    pass
    print()
    print(c(f"✓ Updated {updated}/{len(installed)} skills", "green"))
    return 0

def main():
    parser = argparse.ArgumentParser(
        prog="lotr",
        description="⚔ The Lord of the Skills — smart skills installer for any agentic AI framework",
        epilog="One catalog to rule them all. Docs: https://github.com/Bilal140202/the-lord-of-the-skills",
    )
    parser.add_argument("--version", action="version", version="lotr 1.0.0")

    subparsers = parser.add_subparsers(dest="command", help="Subcommand")

    # detect
    p_detect = subparsers.add_parser("detect", help="Show detected framework + stack")
    p_detect.add_argument("--project-root", default=".")

    # kingdoms
    subparsers.add_parser("kingdoms", help="List all 10 kingdoms")

    # search
    p_search = subparsers.add_parser("search", help="Search the skills index by keyword")
    p_search.add_argument("query", help="Search query")

    # list
    p_list = subparsers.add_parser("list", help="List available skills for detected stack")
    p_list.add_argument("--project-root", default=".")
    p_list.add_argument("--framework")
    p_list.add_argument("--all", action="store_true")

    # preview
    p_preview = subparsers.add_parser("preview", help="Dry-run: show what would be installed")
    p_preview.add_argument("intent", help="Natural-language task")
    p_preview.add_argument("--project-root", default=".")
    p_preview.add_argument("--framework")
    p_preview.add_argument("--all", action="store_true")
    p_preview.add_argument("--limit", type=int, default=10)

    # install
    p_install = subparsers.add_parser("install", help="Install skills for a task")
    p_install.add_argument("intent", nargs="?", help="Natural-language task (omit for --kingdom+--framework)")
    p_install.add_argument("--project-root", default=".")
    p_install.add_argument("--framework")
    p_install.add_argument("--kingdom")
    p_install.add_argument("--all", action="store_true")
    p_install.add_argument("--limit", type=int, default=10)

    # update
    p_update = subparsers.add_parser("update", help="Update installed skills to latest")
    p_update.add_argument("--project-root", default=".")

    # Shorthand: `lotr "do something"` = `lotr install "do something"`
    # We detect this by checking if argv[1] is not a known subcommand
    known_commands = {"detect", "kingdoms", "search", "list", "preview", "install", "update",
                      "-h", "--help", "--version"}
    argv = sys.argv[1:]
    if argv and argv[0] not in known_commands and not argv[0].startswith("-"):
        # Treat as `lotr install "<intent>"`
        argv = ["install"] + argv
    args = parser.parse_args(argv)

    # Common args (apply to install shorthand)
    if args.command is None:
        # No subcommand — check if there's an intent from shorthand
        parser.print_help()
        return 0

    if args.command == "detect":
        return cmd_detect(args)
    elif args.command == "kingdoms":
        return cmd_kingdoms(args)
    elif args.command == "search":
        return cmd_search(args)
    elif args.command == "list":
        return cmd_list(args)
    elif args.command == "preview":
        return cmd_preview(args)
    elif args.command == "install":
        return cmd_install(args)
    elif args.command == "update":
        return cmd_update(args)
    else:
        parser.print_help()
        return 0

if __name__ == "__main__":
    sys.exit(main())
