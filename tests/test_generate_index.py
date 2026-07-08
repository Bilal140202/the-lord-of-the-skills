"""
Tests for cli.generate_index — extract_title, extract_summary, extract_tags
"""
import sys
from pathlib import Path

# Add cli/ to path
CLI_DIR = Path(__file__).parent.parent / "cli"
sys.path.insert(0, str(CLI_DIR))

import pytest
from generate_index import extract_title, extract_summary, extract_tags


class TestExtractTitle:
    """Test extract_title — title from frontmatter, H1, or filename."""

    def test_extract_title_from_h1(self):
        content = "# My Skill\nsome content"
        assert extract_title(content, "x.md") == "My Skill"

    def test_extract_title_from_frontmatter(self):
        content = "---\ntitle: Auth Skill\n---\ncontent"
        assert extract_title(content, "x.md") == "Auth Skill"

    def test_extract_title_frontmatter_with_quotes(self):
        content = '---\ntitle: "Quoted Title"\n---\ncontent'
        assert extract_title(content, "x.md") == "Quoted Title"

    def test_extract_title_fallback_to_filename(self):
        # When no frontmatter or H1, falls back to filename (title-cased)
        result = extract_title("no headers here", "my-skill.md")
        assert result == "My Skill"

    def test_extract_title_strips_canonical_prefix(self):
        # canonical__ prefix is stripped before title-casing
        result = extract_title("no headers", "canonical__code-review.md")
        assert result == "Code Review"

    def test_extract_title_empty_content_uses_filename(self):
        # Empty content with a filename falls back to filename
        result = extract_title("", "untitled.md")
        assert result == "Untitled"

    def test_extract_title_truncates_long_titles(self):
        long_title = "A" * 200
        content = f"# {long_title}\nbody"
        result = extract_title(content, "x.md")
        assert len(result) <= 120

    def test_extract_title_frontmatter_takes_precedence_over_h1(self):
        content = "---\ntitle: Frontmatter Title\n---\n# H1 Title\nbody"
        assert extract_title(content, "x.md") == "Frontmatter Title"


class TestExtractSummary:
    """Test extract_summary — first substantive paragraph."""

    def test_basic_summary(self):
        content = "# Title\n\nThis is the first paragraph of the skill.\n\nSecond paragraph."
        summary = extract_summary(content)
        assert "first paragraph" in summary

    def test_skips_frontmatter(self):
        content = "---\ntitle: Test\n---\n\nThis is the real summary content."
        summary = extract_summary(content)
        assert "real summary" in summary

    def test_skips_headings(self):
        content = "# Title\n## Subtitle\n\nThis is the actual content."
        summary = extract_summary(content)
        assert "actual content" in summary

    def test_max_length_truncation(self):
        content = "# Title\n\n" + "A" * 500
        summary = extract_summary(content, max_len=100)
        assert len(summary) <= 103  # 100 + "..."

    def test_empty_content(self):
        summary = extract_summary("")
        assert summary == ""


class TestExtractTags:
    """Test extract_tags — tag extraction from content + kingdom + framework."""

    def test_returns_list(self):
        tags = extract_tags("some content", "gondor", "cursor")
        assert isinstance(tags, list)

    def test_includes_kingdom_and_framework(self):
        tags = extract_tags("some content", "gondor", "cursor")
        assert "gondor" in tags
        assert "cursor" in tags

    def test_detects_tech_keywords(self):
        content = "This skill uses TypeScript and React for frontend development."
        tags = extract_tags(content, "gondor", "cursor")
        assert "typescript" in tags
        assert "react" in tags

    def test_detects_kingdom_keywords(self):
        content = "This skill helps with testing and verification."
        tags = extract_tags(content, "rohan", "cursor")
        assert "test" in tags

    def test_capped_at_15_tags(self):
        content = " ".join(["typescript", "python", "react", "next", "rust",
                           "docker", "k8s", "api", "database", "test",
                           "verify", "assert", "coverage", "lint", "typecheck",
                           "extra1", "extra2"])
        tags = extract_tags(content, "gondor", "cursor")
        assert len(tags) <= 15
