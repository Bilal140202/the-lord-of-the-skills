#!/usr/bin/env python3
"""
lotr match — Intent → kingdom mapper.

Maps a natural-language task string to one or more LOTR kingdoms
using weighted keyword voting. Returns the matched kingdoms (ranked)
plus the keywords that triggered the match.

Examples:
  "update the UI to be more modern"  →  ["gondor", "lothlorien"]
  "write unit tests for the API"      →  ["rohan"]
  "deploy to kubernetes"              →  ["moria"]
  "audit for OWASP vulnerabilities"   →  ["mordor"]
"""
from __future__ import annotations
import re
from typing import List, Tuple

# Kingdom → list of regex patterns (case-insensitive)
INTENT_MAP: dict[str, list[str]] = {
    "gondor": [
        r"\b(code|coding|refactor|debug|implement|function|class|method|api|endpoint|"
        r"git|commit|branch|merge|codebase|module|package|build|compile|typescript|"
        r"javascript|python|rust|go|java|react|vue|svelte|next\.?js|node|database|"
        r"sql|schema|migration|orm)\b",
        r"\b(ui|ux|interface|component|frontend|front-end|style|css|tailwind|"
        r"layout|design|theme|button|form|page)\b",
    ],
    "rivendell": [
        r"\b(research|study|investigate|analyze|analysis|knowledge|learn|understand|"
        r"explore|discover|paper|academic|literature|survey|review|summarize|"
        r"synthesis|insight|theory|concept|methodology|hypothesis|citation)\b",
    ],
    "moria": [
        r"\b(devops|infrastructure|deploy|deployment|kubernetes|docker|container|"
        r"terraform|ansible|ci/?cd|ci |cd |pipeline|cloud|aws|gcp|azure|server|nginx|"
        r"load.?balancer|monitoring|observability|metrics|alert|incident|sre|helm|"
        r"operator|config|environment)\b",
    ],
    "lothlorien": [
        r"\b(data|dataset|etl|dataframe|pandas|numpy|visualization|chart|graph|"
        r"plot|statistics|statistical|ml|machine.?learning|model|training|feature|"
        r"feature.?engineering|notebook|jupyter|eda|cleaning)\b",
    ],
    "mordor": [
        r"\b(security|secure|vulnerability|vuln|audit|pentest|pen.?test|exploit|cve|"
        r"owasp|injection|xss|csrf|ssrf|authentication|authorization|auth|crypto|"
        r"encryption|secret|credentials|hardening|firewall|compliance|gdpr|privacy|"
        r"threat|malware|reverse.?engineer)\b",
    ],
    "the-shire": [
        r"\b(writing|write|content|blog|article|essay|story|narrative|copy|"
        r"copywriting|documentation|docs|readme|guide|tutorial|explain|explanation|"
        r"edit|proofread|grammar|style|tone|voice|newsletter|marketing|social.?media|"
        r"tweet|post)\b",
    ],
    "isengard": [
        r"\b(agent|subagent|orchestrat|multi.?agent|workflow|pipeline|task|"
        r"scheduler|orchestrator|coordinator|delegation|decompose|sub.?task|subtask|"
        r"plan|planning|strategy|supervisor|manager|fellowship|swarm|team.?of.?agents)\b",
    ],
    "rohan": [
        r"\b(tests?|testing|verify|verification|validate|validation|assertion|assert|"
        r"unit.?tests?|integration.?tests?|e2e|tdd|bdd|coverage|mocks?|stubs?|fixtures?|"
        r"snapshots?|regression|qa|quality|lints?|linters?|typechecks?|type.?checks?|"
        r"static.?analysis)\b",
    ],
    "fangorn": [
        r"\b(memory|remember|recall|context|history|documentation|doc|knowledge.?base|"
        r"kb|note|notes|journal|log|diary|embedding|vector|rag|retrieval|index|"
        r"searchable|trace|audit.?log|session|conversation.?history)\b",
    ],
    "mirkwood": [
        r"\b(specialized|niche|domain.?specific|custom|esoteric|unusual|advanced|"
        r"experimental|prototype|research.?grade|hack|trick|one.?off|specific)\b",
    ],
}

# Compile patterns once
_COMPILED: dict[str, list[re.Pattern]] = {
    kingdom: [re.compile(p, re.IGNORECASE) for p in patterns]
    for kingdom, patterns in INTENT_MAP.items()
}

def match(intent: str, top_n: int = 3, min_score: int = 1) -> List[Tuple[str, int, list[str]]]:
    """Map an intent string to ranked kingdoms.

    Args:
        intent: Natural-language task string (e.g., "update the UI to be more modern")
        top_n: Max number of kingdoms to return
        min_score: Minimum score threshold (default 1 = at least one keyword match)

    Returns:
        List of (kingdom, score, matched_keywords) tuples, highest score first.
        Empty list if no matches.

    Scoring:
        - Each unique keyword match = 1 point
        - Compound phrases (e.g., "unit test", "ci/cd", "machine learning") = 2 points
          (they're stronger intent signals than single words)
        - This helps break ties: "write unit tests" → rohan (2, "unit tests")
          beats the-shire (1, "write")
    """
    if not intent or not intent.strip():
        return []
    # Compound phrases worth 2 points (stronger intent signal)
    COMPOUND_PHRASES = {
        "unit test", "unit tests", "integration test", "integration tests",
        "e2e test", "type check", "type checking", "static analysis",
        "machine learning", "knowledge base", "multi-agent", "sub-agent",
        "ci/cd", "ci cd", "continuous integration", "continuous deployment",
        "code review", "code reviewer", "git commit", "pull request",
        "owasp", "pen test", "pen-test", "penetration test",
        "reverse engineer", "social media",
    }
    intent_lower = intent.lower()
    results: list[tuple[str, int, list[str]]] = []
    for kingdom, patterns in _COMPILED.items():
        matched_keywords: list[str] = []
        score = 0
        for pattern in patterns:
            matches = pattern.findall(intent)
            for m in matches:
                if isinstance(m, tuple):
                    m = m[0]
                if m.lower() not in [k.lower() for k in matched_keywords]:
                    matched_keywords.append(m)
                # Compound phrases get 2 points, single words get 1
                if m.lower() in COMPOUND_PHRASES:
                    score += 2
                else:
                    score += 1
        # Also check for compound phrases directly in the intent (catches multi-word phrases
        # that the regex might have split)
        for phrase in COMPOUND_PHRASES:
            if phrase in intent_lower:
                # Only count if not already counted via regex
                already = any(phrase in mk.lower() for mk in matched_keywords)
                if not already and kingdom == _phrase_kingdom(phrase):
                    matched_keywords.append(phrase)
                    score += 2
        if score >= min_score:
            results.append((kingdom, score, matched_keywords))
    # Sort by score desc, then alphabetical for stability
    results.sort(key=lambda x: (-x[1], x[0]))
    return results[:top_n]

def _phrase_kingdom(phrase: str) -> str:
    """Map a compound phrase to its kingdom (for bonus scoring)."""
    p = phrase.lower()
    if any(w in p for w in ["test", "assert", "coverage", "lint", "type check", "static analysis"]):
        return "rohan"
    if any(w in p for w in ["machine learning", "knowledge base"]):
        return "lothlorien"
    if any(w in p for w in ["multi-agent", "sub-agent", "agent"]):
        return "isengard"
    if any(w in p for w in ["ci/cd", "ci cd", "continuous", "deploy"]):
        return "moria"
    if any(w in p for w in ["code review", "git commit", "pull request"]):
        return "gondor"
    if any(w in p for w in ["owasp", "pen test", "penetration", "reverse engineer"]):
        return "mordor"
    if any(w in p for w in ["social media"]):
        return "the-shire"
    return ""

def match_kingdoms(intent: str, top_n: int = 3) -> List[str]:
    """Convenience: return just the kingdom names (no scores/keywords)."""
    return [k for k, _, _ in match(intent, top_n=top_n)]

if __name__ == "__main__":
    import sys
    intent = " ".join(sys.argv[1:]) or "update the UI to be more modern"
    print(f"Intent: {intent!r}")
    print(f"Matches:")
    for kingdom, score, kws in match(intent):
        print(f"  {kingdom:12s} (score={score}, keywords={kws})")
