"""
Tests for crawler.dedup — canonical deduplication
"""
import sys
from pathlib import Path

# Add crawler to path
CRAWLER_DIR = Path(__file__).parent.parent / "crawler"
sys.path.insert(0, str(CRAWLER_DIR))

import pytest
from dedup import (
    normalize_title, tokenize, jaccard, canonical_score,
    FRAMEWORK_PRIORITY, SKILL_TYPE_PRIORITY,
)


class TestNormalizeTitle:
    """Test title normalization."""

    @pytest.mark.parametrize("input,expected", [
        ("Git Commit", "git commit"),
        ("git-commit", "git commit"),
        ("Git_Commit", "git commit"),
        ("  Git   Commit  ", "git commit"),
        ("Git Commit!", "git commit"),
        ("GIT COMMIT", "git commit"),
        ("Git-Commit_Skill", "git commit skill"),
        ("", ""),
    ])
    def test_normalize(self, input, expected):
        assert normalize_title(input) == expected


class TestTokenize:
    """Test tokenization for Jaccard similarity."""

    def test_basic_tokenize(self):
        tokens = tokenize("hello world")
        assert "hello" in tokens
        assert "world" in tokens

    def test_strips_punctuation(self):
        tokens = tokenize("hello, world!")
        assert "hello" in tokens
        assert "world" in tokens

    def test_removes_stopwords(self):
        tokens = tokenize("the cat is on the mat")
        assert "the" not in tokens
        assert "is" not in tokens
        assert "on" not in tokens
        assert "cat" in tokens
        assert "mat" in tokens

    def test_lowercase(self):
        tokens = tokenize("HELLO World")
        assert "hello" in tokens
        assert "world" in tokens

    def test_empty_string(self):
        assert tokenize("") == set()


class TestJaccard:
    """Test Jaccard similarity."""

    def test_identical_sets(self):
        assert jaccard({"a", "b"}, {"a", "b"}) == 1.0

    def test_disjoint_sets(self):
        assert jaccard({"a"}, {"b"}) == 0.0

    def test_partial_overlap(self):
        result = jaccard({"a", "b"}, {"b", "c"})
        assert abs(result - 1/3) < 0.001

    def test_empty_sets(self):
        assert jaccard(set(), set()) == 0.0
        assert jaccard(set(), {"a"}) == 0.0
        assert jaccard({"a"}, set()) == 0.0

    def test_subset(self):
        assert jaccard({"a"}, {"a", "b"}) == 0.5


class TestCanonicalScore:
    """Test canonical score calculation."""

    def test_basic_record(self):
        rec = {
            "framework": "claude-code",
            "skill_type": "execution",
            "size_bytes": 5000,
            "filename": "SKILL.md",
        }
        score = canonical_score(rec)
        assert score > 0

    def test_framework_priority(self):
        base = {"skill_type": "execution", "size_bytes": 5000, "filename": "SKILL.md"}
        claude_score = canonical_score({**base, "framework": "claude-code"})
        cursor_score = canonical_score({**base, "framework": "cursor"})
        general_score = canonical_score({**base, "framework": "general"})
        assert claude_score > cursor_score > general_score

    def test_skill_type_priority(self):
        base = {"framework": "claude-code", "size_bytes": 5000, "filename": "SKILL.md"}
        conventions_score = canonical_score({**base, "skill_type": "conventions"})
        execution_score = canonical_score({**base, "skill_type": "execution"})
        other_score = canonical_score({**base, "skill_type": "other"})
        assert conventions_score > execution_score > other_score

    def test_canonical_filename_bonus(self):
        base = {"framework": "claude-code", "skill_type": "execution", "size_bytes": 5000}
        with_bonus = canonical_score({**base, "filename": "SKILL.md"})
        without = canonical_score({**base, "filename": "random.md"})
        assert with_bonus > without

    def test_size_bonus_capped(self):
        base = {"framework": "claude-code", "skill_type": "execution", "filename": "SKILL.md"}
        small = canonical_score({**base, "size_bytes": 1024})
        medium = canonical_score({**base, "size_bytes": 30 * 1024})
        large = canonical_score({**base, "size_bytes": 100 * 1024})
        assert small < medium
        assert medium < large
        sixty_kb = canonical_score({**base, "size_bytes": 60 * 1024})
        assert abs(large - sixty_kb) < 0.01


class TestFrameworkPriority:
    """Test framework priority mapping."""

    def test_claude_code_highest(self):
        assert FRAMEWORK_PRIORITY["claude-code"] == max(FRAMEWORK_PRIORITY.values())

    def test_codex_second(self):
        assert FRAMEWORK_PRIORITY["codex"] == 9

    def test_all_frameworks_represented(self):
        expected_frameworks = {
            "claude-code", "cursor", "cline", "roo", "aider", "openhands",
            "swe-agent", "codex", "continue", "goose", "copilot",
            "autogen", "crewai", "langgraph", "general",
        }
        for fw in expected_frameworks:
            assert fw in FRAMEWORK_PRIORITY, f"Missing: {fw}"


class TestSkillTypePriority:
    """Test skill type priority mapping."""

    def test_conventions_highest(self):
        assert SKILL_TYPE_PRIORITY["conventions"] == max(SKILL_TYPE_PRIORITY.values())

    def test_other_lowest(self):
        assert SKILL_TYPE_PRIORITY["other"] == min(SKILL_TYPE_PRIORITY.values())

    def test_all_types_represented(self):
        expected_types = {
            "planning", "execution", "verification", "memory",
            "tools", "prompts", "orchestration", "conventions", "other",
        }
        assert set(SKILL_TYPE_PRIORITY.keys()) == expected_types


class TestDedupIntegration:
    """Integration test for the dedup process."""

    def test_two_files_same_title_cluster_together(self):
        title1 = "Git Commit"
        title2 = "git-commit"
        assert normalize_title(title1) == normalize_title(title2)

    def test_canonical_selection_prefers_better_framework(self):
        rec1 = {
            "framework": "claude-code",
            "skill_type": "execution",
            "size_bytes": 5000,
            "filename": "SKILL.md",
        }
        rec2 = {
            "framework": "general",
            "skill_type": "execution",
            "size_bytes": 5000,
            "filename": "SKILL.md",
        }
        assert canonical_score(rec1) > canonical_score(rec2)
