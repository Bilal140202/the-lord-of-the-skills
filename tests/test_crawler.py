"""
Tests for crawler.crawler — skill file detection + framework detection
"""
import sys
import re
from pathlib import Path

# Add crawler to path
CRAWLER_DIR = Path(__file__).parent.parent / "crawler"
sys.path.insert(0, str(CRAWLER_DIR))

import pytest
from crawler import (
    SKILL_FILE_PATTERNS, SKIP_PATTERNS, is_skill_file, detect_framework,
    SEEDS, GITHUB_LINK_RE,
)


class TestSkillFileDetection:
    """Test SKILL_FILE_PATTERNS regex."""

    @pytest.mark.parametrize("path,expected", [
        ("SKILL.md", True),
        ("skills/my-skill.md", True),
        ("agents/my-agent.md", True),
        ("AGENTS.md", True),
        ("CONVENTIONS.md", True),
        (".cursorrules", True),
        (".cursor/rules/my-rule.mdc", True),
        (".clinerules/my-rule.md", True),
        (".roo/rules/my-rule.md", True),
        (".continue/config.yaml", True),
        (".goose/recipe.yaml", True),
        (".github/copilot-instructions.md", True),
        ("prompts/code-review.md", True),
        ("my-skill.prompt.md", True),
        ("my-rule.mdc", True),
        ("README.md", False),
        ("CHANGELOG.md", False),
        ("LICENSE", False),
        ("package.json", False),
        # NOTE: node_modules/ and vendor/ are pruned at the directory level
        # in extract_files_from_repo(), not by is_skill_file(). is_skill_file()
        # only checks SKIP_PATTERNS which require a leading slash.
        # So /node_modules/foo/SKILL.md (with leading /) IS skipped:
        ("/node_modules/something/SKILL.md", False),
        ("/.git/config", False),
        ("/vendor/lib/SKILL.md", False),
    ])
    def test_skill_file_detection(self, path, expected):
        assert is_skill_file(path) == expected, f"Path {path!r}: expected {expected}"

    def test_all_patterns_are_compiled_regex(self):
        for pattern in SKILL_FILE_PATTERNS:
            assert isinstance(pattern, re.Pattern), f"Pattern not compiled: {pattern}"

    def test_skip_patterns_cover_common_noise(self):
        # SKIP_PATTERNS use leading-slash regex, so paths must have leading /
        # to be skipped by is_skill_file(). The crawler's extract_files_from_repo()
        # also prunes these directories at the os.walk level.
        skip_paths = [
            "/node_modules/foo/SKILL.md",       # leading / required by regex
            "/.git/config",
            "/vendor/lib/SKILL.md",
            "/dist/build/SKILL.md",
            "/__pycache__/foo.md",
            "/path/to/package-lock.json",
            "/path/to/yarn.lock",
            "/path/to/CHANGELOG.md",
            "/path/to/LICENSE",
            "/path/to/image.png",
            "/path/to/archive.zip",
        ]
        for path in skip_paths:
            assert not is_skill_file(path), f"Should skip: {path}"


class TestFrameworkDetection:
    """Test detect_framework function."""

    @pytest.mark.parametrize("path,repo,expected", [
        (".cursorrules", "my-repo", "cursor"),
        (".cursor/rules/foo.mdc", "my-repo", "cursor"),
        (".clinerules/foo.md", "my-repo", "cline"),
        (".cline/foo.md", "my-repo", "cline"),
        (".roo/rules/foo.md", "my-repo", "roo"),
        (".continue/config.yaml", "my-repo", "continue"),
        (".goose/recipe.yaml", "my-repo", "goose"),
        (".github/copilot-instructions.md", "my-repo", "copilot"),
        ("CONVENTIONS.md", "my-repo", "aider"),
        ("AGENTS.md", "my-repo", "codex"),
        ("SKILL.md", "my-repo", "claude-code"),
        # NOTE: detect_framework() checks '/skills/' (with leading slash).
        # A bare 'skills/foo.md' (no leading /) doesn't match, falls to general.
        # In practice, paths from os.walk always have a leading dir, so this works.
        ("/skills/foo.md", "my-repo", "claude-code"),
        ("random.md", "my-cursor-rules", "cursor"),
        ("random.md", "my-cline-tools", "cline"),
        ("random.md", "my-aider-config", "aider"),
        ("random.md", "my-openhands", "openhands"),
        ("random.md", "my-random-repo", "general"),
    ])
    def test_framework_detection(self, path, repo, expected):
        assert detect_framework(path, repo) == expected, f"Path={path!r} repo={repo!r}: expected {expected}"


class TestSeeds:
    """Sanity checks on SEED list."""

    def test_seeds_not_empty(self):
        assert len(SEEDS) > 0
        assert len(SEEDS) >= 80, "Should have at least 80 seed repos"

    def test_all_seeds_have_owner_repo_format(self):
        for seed in SEEDS:
            assert "/" in seed, f"Invalid seed format: {seed}"
            parts = seed.split("/")
            assert len(parts) == 2, f"Seed should be owner/repo: {seed}"
            assert parts[0], f"Empty owner: {seed}"
            assert parts[1], f"Empty repo: {seed}"

    def test_no_duplicate_seeds(self):
        assert len(SEEDS) == len(set(SEEDS)), "Duplicate seeds found"

    def test_anthropic_official_in_seeds(self):
        anthropic_seeds = [s for s in SEEDS if s.startswith("anthropics/")]
        assert len(anthropic_seeds) >= 3, "Should include multiple anthropic/* repos"

    def test_claude_code_community_in_seeds(self):
        community = [s for s in SEEDS if "awesome-claude-code" in s or "claude-code" in s]
        assert len(community) >= 5, "Should include multiple claude-code community repos"

    def test_cursor_rules_in_seeds(self):
        cursor = [s for s in SEEDS if "cursor" in s.lower()]
        assert len(cursor) >= 5, "Should include multiple cursor repos"

    def test_cline_roo_in_seeds(self):
        cline_roo = [s for s in SEEDS if "cline" in s.lower() or "roo" in s.lower()]
        assert len(cline_roo) >= 3, "Should include cline/roo repos"

    def test_aider_in_seeds(self):
        aider = [s for s in SEEDS if "aider" in s.lower()]
        assert len(aider) >= 2, "Should include aider repos"

    def test_openhands_in_seeds(self):
        oh = [s for s in SEEDS if "openhands" in s.lower() or "open-hands" in s.lower()]
        assert len(oh) >= 1, "Should include OpenHands repos"


class TestBFSRegex:
    """Test GitHub link extraction for BFS."""

    @pytest.mark.parametrize("text,should_match", [
        ("Check out https://github.com/anthropics/skills", True),
        ("See [this repo](https://github.com/wshobson/agents) for more", True),
        ("github.com/Aider-AI/aider is great", True),
        ("Visit github.com/cline/cline today", True),
        ("no links here", False),
        ("example.com is not github", False),
    ])
    def test_github_link_regex(self, text, should_match):
        matches = GITHUB_LINK_RE.findall(text)
        if should_match:
            assert len(matches) > 0, f"Should match: {text}"
        else:
            assert len(matches) == 0, f"Should not match: {text}"


class TestCrawlerSanity:
    """Sanity checks on crawler module."""

    def test_skill_file_patterns_not_empty(self):
        assert len(SKILL_FILE_PATTERNS) >= 20, f"Should have at least 20 skill file patterns, got {len(SKILL_FILE_PATTERNS)}"

    def test_skip_patterns_not_empty(self):
        assert len(SKIP_PATTERNS) >= 10, f"Should have skip patterns, got {len(SKIP_PATTERNS)}"

    def test_patterns_are_case_insensitive(self):
        for pattern in SKILL_FILE_PATTERNS:
            assert pattern.flags & re.IGNORECASE, f"Pattern not case-insensitive: {pattern.pattern}"

    def test_skip_patterns_are_case_insensitive(self):
        for pattern in SKIP_PATTERNS:
            assert pattern.flags & re.IGNORECASE, f"Skip pattern not case-insensitive: {pattern.pattern}"
