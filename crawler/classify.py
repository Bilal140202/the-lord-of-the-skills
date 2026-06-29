#!/usr/bin/env python3
"""
The Lord of the Skills — Classifier
====================================
Reads _cache/manifest.json, classifies each extracted file into:
  - LOTR kingdom (domain): gondor, rivendell, moria, lothlorien, mordor,
                           the-shire, isengard, rohan, fangorn, mirkwood
  - Skill type: planning, execution, verification, memory, tools, prompts,
                orchestration, conventions, other
  - Title + summary (extracted from file content)
Writes _cache/manifest_classified.json
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path("/home/z/my-project/the-lord-of-the-skills")
MANIFEST = ROOT / "_cache" / "manifest.json"
OUT = ROOT / "_cache" / "manifest_classified.json"

# ----------------------------------------------------------------------
# LOTR Kingdom → Domain mapping
# ----------------------------------------------------------------------
KINGDOM_KEYWORDS = {
    "gondor": {  # Coding & Software Engineering
        "keywords": ["coding", "code", "software", "engineer", "refactor",
                     "debug", "implementation", "function", "class", "method",
                     "api", "endpoint", "git", "commit", "branch", "merge",
                     "codebase", "module", "package", "build", "compile",
                     "typescript", "javascript", "python", "rust", "go ",
                     "java ", "react", "vue", "svelte", "next.js", "node",
                     "database", "sql", "schema", "migration", "orm"],
        "domain_label": "Coding & Software Engineering",
        "motto": "Gondor sees, Gondor codes.",
    },
    "rivendell": {  # Research & Knowledge
        "keywords": ["research", "study", "investigate", "analyze", "analysis",
                     "knowledge", "learn", "understand", "explore", "discover",
                     "paper", "academic", "literature", "survey", "review",
                     "summarize", "synthesis", "insight", "theory", "concept",
                     "methodology", "hypothesis", "citation", "reference"],
        "domain_label": "Research & Knowledge",
        "motto": "Knowledge flows from the Last Homely House.",
    },
    "moria": {  # DevOps & Infrastructure
        "keywords": ["devops", "infrastructure", "deploy", "deployment",
                     "kubernetes", "docker", "container", "terraform",
                     "ansible", "ci/cd", "pipeline", "ci ", "cd ",
                     "cloud", "aws", "gcp", "azure", "server", "nginx",
                     "load balancer", "monitoring", "observability",
                     "metrics", "logging", "alert", "incident", "sre",
                     "helm", "operator", "config", "environment"],
        "domain_label": "DevOps & Infrastructure",
        "motto": "Speak, friend, and enter the deploy.",
    },
    "lothlorien": {  # Data & Analysis
        "keywords": ["data", "dataset", "etl", "pipeline", "dataframe",
                     "pandas", "numpy", "analysis", "visualization",
                     "chart", "graph", "plot", "statistics", "statistical",
                     "ml", "machine learning", "model", "training",
                     "feature", "feature engineering", "notebook",
                     "jupyter", "exploration", "eda", "cleaning"],
        "domain_label": "Data & Analysis",
        "motto": "Where data roots run deep.",
    },
    "mordor": {  # Security & Auditing
        "keywords": ["security", "secure", "vulnerability", "vuln",
                     "audit", "pentest", "pen-test", "exploit", "cve",
                     "owasp", "injection", "xss", "csrf", "ssrf",
                     "authentication", "authorization", "auth", "crypto",
                     "encryption", "secret", "credentials", "sshardening",
                     "firewall", "iptables", "compliance", "gdpr",
                     "privacy", "threat", "malware", "reverse engineer"],
        "domain_label": "Security & Auditing",
        "motto": "One audit to rule them all.",
    },
    "the-shire": {  # Writing & Content
        "keywords": ["writing", "write", "content", "blog", "article",
                     "essay", "story", "narrative", "copy", "copywriting",
                     "documentation", "docs", "readme", "guide", "tutorial",
                     "explain", "explanation", "edit", "proofread",
                     "grammar", "style", "tone", "voice", "newsletter",
                     "marketing", "social media", "tweet", "post"],
        "domain_label": "Writing & Content",
        "motto": "Quiet writing, deep roots.",
    },
    "isengard": {  # Agents & Orchestration
        "keywords": ["agent", "subagent", "orchestrat", "multi-agent",
                     "workflow", "pipeline", "task", "scheduler",
                     "orchestrator", "coordinator", "delegation",
                     "decompose", "sub-task", "subtask", "plan",
                     "planning", "strategy", "supervisor", "manager",
                     "fellowship", "swarm", "team of agents"],
        "domain_label": "Agents & Orchestration",
        "motto": "Industry wakes the deep.",
    },
    "rohan": {  # Testing & Verification
        "keywords": ["test", "testing", "verify", "verification", "validate",
                     "validation", "assertion", "assert", "unit test",
                     "integration test", "e2e", "tdd", "bdd", "coverage",
                     "mock", "stub", "fixture", "snapshot", "regression",
                     "qa", "quality", "lint", "linter", "typecheck",
                     "type check", "static analysis"],
        "domain_label": "Testing & Verification",
        "motto": "Ride now, ride to verify.",
    },
    "fangorn": {  # Documentation & Memory
        "keywords": ["memory", "remember", "recall", "context", "history",
                     "documentation", "doc", "knowledge base", "kb",
                     "note", "notes", "journal", "log", "diary",
                     "embedding", "vector", "rag", "retrieval",
                     "index", "searchable", "trace", "audit log",
                     "session", "conversation history"],
        "domain_label": "Documentation & Memory",
        "motto": "The old forest remembers.",
    },
    "mirkwood": {  # Specialized / Niche
        "keywords": ["specialized", "niche", "domain-specific", "custom",
                     "esoteric", "unusual", "advanced", "experimental",
                     "prototype", "research-grade", "hack", "trick",
                     "one-off", "specific"],  # fallback bucket
        "domain_label": "Specialized & Niche",
        "motto": "Strange paths through the wood.",
    },
}

# ----------------------------------------------------------------------
# Skill-type classification
# ----------------------------------------------------------------------
SKILL_TYPE_KEYWORDS = {
    "planning":      ["plan", "planning", "decompose", "outline", "strategy",
                      "roadmap", "approach", "step", "stage", "phase"],
    "execution":     ["execute", "implement", "run", "do", "perform",
                      "action", "operation", "task", "carry out"],
    "verification":  ["verify", "validate", "check", "test", "qa", "assert",
                      "confirm", "ensure"],
    "memory":        ["memory", "context", "history", "remember", "recall",
                      "session", "state"],
    "tools":         ["tool", "mcp", "function", "calling", "api",
                      "command", "shell", "bash"],
    "prompts":       ["prompt", "system prompt", "instruction", "template"],
    "orchestration": ["orchestrat", "subagent", "delegate", "multi-agent",
                      "swarm", "team", "fellowship"],
    "conventions":   ["convention", "rule", "guideline", "standard",
                      "style", "best practice", "coding standard"],
}

# ----------------------------------------------------------------------
# Content extractors
# ----------------------------------------------------------------------
def extract_title(content: str, filename: str) -> str:
    """Try to find a human-readable title."""
    # frontmatter title
    m = re.search(r"^title:\s*(.+)$", content, re.MULTILINE)
    if m:
        return m.group(1).strip().strip("\"'")
    # first H1
    m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    # filename
    return Path(filename).stem.replace("_", " ").replace("-", " ").title()

def extract_summary(content: str, max_len: int = 220) -> str:
    """First substantive paragraph (skip frontmatter)."""
    text = content
    # strip frontmatter
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4:]
    # skip blank lines and headings
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            continue
        if s.startswith(("---", "```", ">", "- ", "* ", "|")):
            continue
        # found first body line — extend until we have enough
        summary = s
        # grab following lines until max_len
        for nxt in text.splitlines()[text.splitlines().index(line) + 1:]:
            ns = nxt.strip()
            if not ns or ns.startswith(("#", "```", "---", "|", ">")):
                break
            if len(summary) >= max_len:
                break
            summary += " " + ns
        return summary[:max_len] + ("..." if len(summary) > max_len else "")
    return "(no summary available)"

def classify_kingdom(content: str, framework: str, original_path: str) -> str:
    """Vote on kingdom via keyword matches."""
    text = (content + " " + original_path).lower()
    scores = Counter()
    for kingdom, spec in KINGDOM_KEYWORDS.items():
        for kw in spec["keywords"]:
            if kw in text:
                scores[kingdom] += 1
    # Framework bias: agent-system repos lean isengard
    if framework in {"claude-code", "autogen", "crewai", "langgraph", "openhands"}:
        scores["isengard"] += 2
    if not scores:
        return "mirkwood"
    return scores.most_common(1)[0][0]

def classify_skill_type(content: str, original_path: str, filename: str) -> str:
    text = (content + " " + original_path + " " + filename).lower()
    scores = Counter()
    for st, kws in SKILL_TYPE_KEYWORDS.items():
        for kw in kws:
            if kw in text:
                scores[st] += 1
    if not scores:
        # filename heuristics
        fn = filename.lower()
        if "convention" in fn or "rules" in fn or ".cursorrules" in fn:
            return "conventions"
        if "prompt" in fn:
            return "prompts"
        if "agent" in fn:
            return "orchestration"
        return "other"
    return scores.most_common(1)[0][0]

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    if not MANIFEST.exists():
        print(f"ERROR: {MANIFEST} not found. Run crawler.py first.")
        return
    manifest = json.loads(MANIFEST.read_text())
    files = manifest.get("files", [])
    print(f"Classifying {len(files)} files...")

    enriched = []
    kingdom_counter = Counter()
    type_counter = Counter()

    for i, rec in enumerate(files, 1):
        if i % 100 == 0:
            print(f"  progress {i}/{len(files)}")
        try:
            content = (ROOT / rec["extracted_path"]).read_text(encoding="utf-8", errors="ignore")
        except Exception:
            content = ""
        filename = Path(rec["original_path"]).name
        title = extract_title(content, filename)
        summary = extract_summary(content)
        kingdom = classify_kingdom(content, rec["framework"], rec["original_path"])
        skill_type = classify_skill_type(content, rec["original_path"], filename)
        rec.update({
            "title": title,
            "summary": summary,
            "kingdom": kingdom,
            "kingdom_label": KINGDOM_KEYWORDS[kingdom]["domain_label"],
            "kingdom_motto": KINGDOM_KEYWORDS[kingdom]["motto"],
            "skill_type": skill_type,
            "filename": filename,
        })
        enriched.append(rec)
        kingdom_counter[kingdom] += 1
        type_counter[skill_type] += 1

    manifest["files"] = enriched
    manifest["kingdom_distribution"] = dict(kingdom_counter)
    manifest["skill_type_distribution"] = dict(type_counter)
    manifest["classified_at"] = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(timespec="seconds")

    OUT.write_text(json.dumps(manifest, indent=2))
    print(f"\nClassification complete.")
    print(f"  Kingdom distribution:")
    for k, v in sorted(kingdom_counter.items(), key=lambda x: -x[1]):
        print(f"    {k:12s} : {v}")
    print(f"  Skill-type distribution:")
    for k, v in sorted(type_counter.items(), key=lambda x: -x[1]):
        print(f"    {k:14s} : {v}")
    print(f"\nWrote: {OUT}")

if __name__ == "__main__":
    main()
