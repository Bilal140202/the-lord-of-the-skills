"""
Tests for crawler.build_package — safe_filename + helpers
"""
import sys
from pathlib import Path

# Add crawler/ to path
CRAWLER_DIR = Path(__file__).parent.parent / "crawler"
sys.path.insert(0, str(CRAWLER_DIR))

import pytest


class TestSafeFilename:
    """Test safe_filename — filesystem-safe filename generation."""

    def test_safe_filename_spaces(self):
        # Spaces are kept during filtering, then replaced with underscores
        result = __import__('build_package').safe_filename("my skill file")
        assert result == "my_skill_file"

    def test_safe_filename_special_chars(self):
        # Colon, #, ! are stripped; space kept then replaced with _
        result = __import__('build_package').safe_filename("skill: #1!")
        assert result == "skill_1"

    def test_safe_filename_empty(self):
        # Empty string returns empty string (no "unnamed" fallback in this impl)
        result = __import__('build_package').safe_filename("")
        assert result == ""

    def test_safe_filename_already_clean(self):
        result = __import__('build_package').safe_filename("clean-name")
        assert result == "clean-name"

    def test_safe_filename_with_dots(self):
        # Dots are in the keep set
        result = __import__('build_package').safe_filename("my.skill.v2.md")
        assert result == "my.skill.v2.md"

    def test_safe_filename_with_slashes(self):
        # Slashes are in the keep set (for relative paths)
        result = __import__('build_package').safe_filename("dir/subdir/file.md")
        assert result == "dir/subdir/file.md"

    def test_safe_filename_strips_leading_trailing_space(self):
        result = __import__('build_package').safe_filename("  padded  ")
        assert result == "padded"

    def test_safe_filename_unicode_kept(self):
        # Python's isalnum() returns True for Unicode letters, so é/ü are kept
        result = __import__('build_package').safe_filename("café-münchen")
        assert result == "café-münchen"

    def test_safe_filename_emoji_stripped(self):
        # Emoji are not alphanumeric, so they're stripped
        result = __import__('build_package').safe_filename("skill⭐name")
        assert result == "skillname"

    def test_safe_filename_mixed_case_preserved(self):
        result = __import__('build_package').safe_filename("MySkillName")
        assert result == "MySkillName"

    def test_safe_filename_only_special_chars(self):
        # All chars stripped → empty string
        result = __import__('build_package').safe_filename(":::!!!###")
        assert result == ""
