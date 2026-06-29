"""
Tests for the lotr CLI — detect, match, fetch, place modules.
"""
import sys
import json
import os
import tempfile
from pathlib import Path

# Add cli/ to path
CLI_DIR = Path(__file__).parent.parent / "cli"
sys.path.insert(0, str(CLI_DIR))

import pytest
from detect import detect, detect_framework, detect_stack
from match import match, match_kingdoms, _phrase_kingdom
from place import resolve_destination, place_skill, list_installed, DESTINATIONS


# ============================================================
# detect.py
# ============================================================

class TestDetect:
    """Test framework + stack detection."""

    def _make_project(self, files: dict) -> Path:
        """Create a temp project with the given files. files = {path: content}."""
        tmp = tempfile.mkdtemp()
        for relpath, content in files.items():
            full = Path(tmp) / relpath
            full.parent.mkdir(parents=True, exist_ok=True)
            full.write_text(content)
        return Path(tmp)

    def test_detect_cursor(self):
        root = self._make_project({".cursor/rules/dummy.mdc": "# test"})
        result = detect(root)
        assert result["framework"] == "cursor"

    def test_detect_claude_code(self):
        root = self._make_project({".claude/settings.json": "{}"})
        result = detect(root)
        assert result["framework"] == "claude-code"

    def test_detect_cline(self):
        root = self._make_project({".clinerules/dummy.md": "# test"})
        result = detect(root)
        assert result["framework"] == "cline"

    def test_detect_codex(self):
        root = self._make_project({"AGENTS.md": "# agents"})
        result = detect(root)
        assert result["framework"] == "codex"

    def test_detect_aider(self):
        root = self._make_project({"CONVENTIONS.md": "# conventions"})
        result = detect(root)
        assert result["framework"] == "aider"

    def test_detect_copilot(self):
        root = self._make_project({".github/copilot-instructions.md": "# copilot"})
        result = detect(root)
        assert result["framework"] == "copilot"

    def test_detect_no_framework(self):
        root = self._make_project({"README.md": "# project"})
        result = detect(root)
        assert result["framework"] is None

    def test_detect_react_stack(self):
        pkg = '{"dependencies": {"react": "^18", "next": "^14", "typescript": "^5"}}'
        root = self._make_project({"package.json": pkg})
        result = detect(root)
        assert result["language"] == "typescript"
        assert "react" in result["stack"]
        assert "next" in result["stack"]

    def test_detect_python_fastapi(self):
        root = self._make_project({"requirements.txt": "fastapi==0.104.0\npydantic==2.0"})
        result = detect(root)
        assert result["language"] == "python"
        assert "fastapi" in result["stack"]
        assert "pydantic" in result["stack"]

    def test_detect_python_django(self):
        root = self._make_project({"requirements.txt": "django==4.2"})
        result = detect(root)
        assert "django" in result["stack"]

    def test_detect_ruby_rails(self):
        root = self._make_project({"Gemfile": 'gem "rails", "~> 7.0"'})
        result = detect(root)
        assert result["language"] == "ruby"
        assert "rails" in result["stack"]

    def test_detect_go(self):
        root = self._make_project({"go.mod": "module test\n\ngo 1.21\n\nrequire github.com/gin-gonic/gin v1.9"})
        result = detect(root)
        assert result["language"] == "go"
        assert "gin" in result["stack"]

    def test_detect_rust(self):
        root = self._make_project({"Cargo.toml": '[dependencies]\ntokio = "1"\naxum = "0.7"'})
        result = detect(root)
        assert result["language"] == "rust"
        assert "tokio" in result["stack"]

    def test_detect_nonexistent_dir(self):
        with pytest.raises(FileNotFoundError):
            detect("/nonexistent/path/that/does/not/exist")


# ============================================================
# match.py
# ============================================================

class TestMatch:
    """Test intent → kingdom matching."""

    @pytest.mark.parametrize("intent,expected_top", [
        ("write unit tests for the API", "rohan"),
        ("deploy to kubernetes", "moria"),
        ("update the UI to be more modern", "gondor"),
        ("audit for OWASP vulnerabilities", "mordor"),
        ("research the literature on transformers", "rivendell"),
        ("write a blog post about our launch", "the-shire"),
        ("set up memory bank for context", "fangorn"),
        ("orchestrate multi-agent workflow", "isengard"),
        ("analyze the dataset with pandas", "lothlorien"),
    ])
    def test_match_top_kingdom(self, intent, expected_top):
        matches = match(intent, top_n=1)
        assert len(matches) >= 1
        assert matches[0][0] == expected_top, f"Intent {intent!r}: expected {expected_top}, got {matches[0][0]}"

    def test_match_empty_intent(self):
        assert match("") == []
        assert match("   ") == []

    def test_match_no_keywords(self):
        matches = match("xyz abc defghi jklmno")
        # Should either return empty or return mirkwood (fallback)
        # The actual behavior depends on whether any keywords match
        # "defghi" doesn't match anything, so this should be empty
        if matches:
            # If something matched, it should be low score
            assert matches[0][1] <= 1

    def test_match_returns_scores(self):
        matches = match("audit for OWASP vulnerabilities", top_n=3)
        assert len(matches) >= 1
        for kingdom, score, kws in matches:
            assert isinstance(score, int)
            assert score >= 1
            assert isinstance(kws, list)

    def test_match_compound_phrase_scoring(self):
        # "unit tests" is a compound phrase worth 2 points
        matches = match("write unit tests", top_n=3)
        rohan_match = [m for m in matches if m[0] == "rohan"]
        assert rohan_match, "rohan should match 'unit tests'"
        assert rohan_match[0][1] >= 2, "compound phrase should score >= 2"

    def test_match_kingdoms_helper(self):
        kingdoms = match_kingdoms("write unit tests", top_n=3)
        assert isinstance(kingdoms, list)
        assert "rohan" in kingdoms

    def test_phrase_kingdom_mapping(self):
        assert _phrase_kingdom("unit test") == "rohan"
        assert _phrase_kingdom("machine learning") == "lothlorien"
        assert _phrase_kingdom("multi-agent") == "isengard"
        assert _phrase_kingdom("ci/cd") == "moria"
        assert _phrase_kingdom("code review") == "gondor"
        assert _phrase_kingdom("owasp") == "mordor"


# ============================================================
# place.py
# ============================================================

class TestPlace:
    """Test per-framework skill placement."""

    def test_resolve_destination_cursor(self, tmp_path):
        dest = resolve_destination("cursor", tmp_path)
        assert dest.is_dir()
        assert dest.name == "rules"
        assert dest.parent.name == ".cursor"

    def test_resolve_destination_claude_code(self, tmp_path):
        # claude-code uses ~/.claude/skills/ (home dir)
        dest = resolve_destination("claude-code", tmp_path)
        assert dest.is_dir()
        assert "skills" in str(dest)

    def test_resolve_destination_cline(self, tmp_path):
        dest = resolve_destination("cline", tmp_path)
        assert dest.is_dir()
        assert dest.name == ".clinerules"

    def test_resolve_destination_aider_append(self, tmp_path):
        dest = resolve_destination("aider", tmp_path)
        assert dest.is_file() or dest == (tmp_path / "CONVENTIONS.md").resolve()

    def test_resolve_destination_unknown_framework(self, tmp_path):
        with pytest.raises(ValueError):
            resolve_destination("unknown-framework", tmp_path)

    def test_place_skill_cursor(self, tmp_path):
        path = place_skill("cursor", "# Test Skill\ncontent here", "test-skill.md", tmp_path)
        assert path.exists()
        assert path.name == "test-skill.md"
        assert "Test Skill" in path.read_text()

    def test_place_skill_strips_canonical_prefix(self, tmp_path):
        path = place_skill("cursor", "# Test", "canonical__test-skill.md", tmp_path)
        assert path.name == "test-skill.md"  # canonical__ stripped

    def test_place_skill_conflict_resolution(self, tmp_path):
        # Place same file twice — second should get _1 suffix
        place_skill("cursor", "# Test", "test.md", tmp_path)
        path2 = place_skill("cursor", "# Test", "test.md", tmp_path)
        assert path2.name == "test_1.md"

    def test_place_skill_aider_append(self, tmp_path):
        # First append creates the file
        path1 = place_skill("aider", "# Convention 1\nrule 1", "conv.md", tmp_path)
        assert path1.exists()
        content1 = path1.read_text()
        assert "Convention 1" in content1
        # Second append adds to the file
        path2 = place_skill("aider", "# Convention 2\nrule 2", "conv.md", tmp_path)
        content2 = path2.read_text()
        assert "Convention 1" in content2
        assert "Convention 2" in content2

    def test_list_installed_empty(self, tmp_path):
        result = list_installed("cursor", tmp_path)
        assert result == []

    def test_list_installed_after_place(self, tmp_path):
        place_skill("cursor", "# Test", "skill.md", tmp_path)
        installed = list_installed("cursor", tmp_path)
        assert len(installed) >= 1
        assert any(p.name == "skill.md" for p in installed)

    def test_all_frameworks_have_destinations(self):
        expected = {"antigravity", "cursor", "claude-code", "cline", "roo",
                    "continue", "goose", "aider", "codex", "copilot"}
        assert set(DESTINATIONS.keys()) == expected


# ============================================================
# fetch.py (smoke tests — don't hit network)
# ============================================================

class TestFetch:
    """Smoke tests for fetch module (no network calls)."""

    def test_fetch_index_falls_back_to_local(self, tmp_path, monkeypatch):
        # Point the cache dir to tmp so we don't use real cache
        import fetch
        monkeypatch.setattr(fetch, "_CACHE_DIR", tmp_path / "cache")
        monkeypatch.setattr(fetch, "_CACHE_INDEX", tmp_path / "cache" / "index.json")
        # The fetch should fail remotely but fall back to local skills/index.json
        # (which exists in the repo)
        try:
            idx = fetch.fetch_index()
            assert "skills" in idx
            assert "total_skills" in idx
        except RuntimeError:
            # If no local index exists (e.g., running outside repo), skip
            pytest.skip("No local skills/index.json available")

    def test_fetch_skills_by_index_filters(self):
        # Test the filtering logic without network
        fake_index = {
            "skills": [
                {"kingdom": "gondor", "frameworks": ["cursor"], "canonical": True, "tags": ["test"]},
                {"kingdom": "mordor", "frameworks": ["cursor"], "canonical": True, "tags": ["security"]},
                {"kingdom": "gondor", "frameworks": ["claude-code"], "canonical": False, "tags": ["test"]},
            ]
        }
        from fetch import fetch_skills_by_index
        # Filter by kingdom (canonical only by default → 1 gondor canonical)
        result = fetch_skills_by_index(fake_index, kingdom="gondor")
        assert len(result) == 1
        # Filter by kingdom (include non-canonical → 2 gondor)
        result = fetch_skills_by_index(fake_index, kingdom="gondor", canonical_only=False)
        assert len(result) == 2
        # Filter by framework
        result = fetch_skills_by_index(fake_index, framework="cursor")
        assert len(result) == 2
        # Filter canonical only (default)
        result = fetch_skills_by_index(fake_index, canonical_only=True)
        assert len(result) == 2
        # Filter by tag
        result = fetch_skills_by_index(fake_index, tags=["security"])
        assert len(result) == 1
        assert result[0]["kingdom"] == "mordor"


# ============================================================
# Kickoff mode tests
# ============================================================

class TestKickoffDetection:
    """Test is_kickoff_intent() heuristic."""

    @pytest.mark.parametrize("intent,expected", [
        # Kickoff intents (project descriptions)
        ("building a tauri app", True),
        ("starting a nextjs SaaS dashboard", True),
        ("creating a microservice", True),
        ("setting up a full-stack react platform", True),
        ("building a python fastapi backend", True),
        ("bootstrapping a new project", True),
        ("scaffolding a vue app", True),
        # Single-task intents (NOT kickoff)
        ("update the UI to be more modern", False),
        ("write unit tests for the API", False),
        ("deploy to kubernetes", False),
        ("audit for OWASP vulnerabilities", False),
        ("refactor the authentication module", False),
        ("write a blog post about our launch", False),
        ("research the literature on transformers", False),
        ("set up memory bank for context", False),
    ])
    def test_kickoff_detection(self, intent, expected):
        from match import is_kickoff_intent
        result = is_kickoff_intent(intent)
        assert result == expected, f"Intent {intent!r}: expected kickoff={expected}, got {result}"

    def test_empty_intent_not_kickoff(self):
        from match import is_kickoff_intent
        assert is_kickoff_intent("") == False
        assert is_kickoff_intent("   ") == False


class TestMatchMulti:
    """Test match_multi() for project kickoff mode."""

    def test_returns_multiple_kingdoms(self):
        from match import match_multi
        results = match_multi("building a react app with tests and deployment")
        assert len(results) >= 3, f"Expected 3+ kingdoms, got {len(results)}"

    def test_pads_with_defaults(self):
        """Even if only 1 kingdom matches keywords, match_multi should
        return at least 5 kingdoms for kickoff mode."""
        from match import match_multi
        # "tauri" only matches gondor, but kickoff should still return 5+
        results = match_multi("building a tauri app")
        assert len(results) >= 5, f"Expected 5+ kingdoms (padded), got {len(results)}"
        kingdoms = [r[0] for r in results]
        assert "gondor" in kingdoms  # matched from "tauri"
        assert "rohan" in kingdoms   # padded default
        assert "moria" in kingdoms   # padded default

    def test_respects_top_n(self):
        from match import match_multi
        results = match_multi("building a react app", top_n=3)
        assert len(results) <= 3

    def test_returns_scores_and_keywords(self):
        from match import match_multi
        results = match_multi("building a react app with tests")
        for kingdom, score, kws in results:
            assert isinstance(kingdom, str)
            assert isinstance(score, int)
            assert isinstance(kws, list)

    def test_sorts_by_score_desc(self):
        from match import match_multi
        results = match_multi("building a react app with tests and deployment and docs")
        scores = [r[1] for r in results]
        assert scores == sorted(scores, reverse=True)


# ============================================================
# Starter + guide + init tests
# ============================================================

class TestStarterPack:
    """Test starter pack configuration."""

    def test_all_frameworks_have_starter_kingdoms(self):
        """Every supported framework should have a starter pack defined."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "cli"))
        from lotr import STARTER_KINGDOMS
        expected_frameworks = {"antigravity", "cursor", "claude-code", "codex",
                                "cline", "roo", "aider", "general"}
        for fw in expected_frameworks:
            assert fw in STARTER_KINGDOMS, f"Missing starter pack for {fw}"

    def test_starter_kingdoms_are_valid(self):
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "cli"))
        from lotr import STARTER_KINGDOMS, KINGDOMS
        for fw, kingdoms in STARTER_KINGDOMS.items():
            for k in kingdoms:
                assert k in KINGDOMS, f"Invalid kingdom {k} in starter pack for {fw}"

    def test_starter_kingdoms_include_gondor(self):
        """Every starter pack should include gondor (coding basics)."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "cli"))
        from lotr import STARTER_KINGDOMS
        for fw, kingdoms in STARTER_KINGDOMS.items():
            assert "gondor" in kingdoms, f"Starter pack for {fw} missing gondor"

    def test_general_fallback_exists(self):
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "cli"))
        from lotr import STARTER_KINGDOMS
        assert "general" in STARTER_KINGDOMS


class TestInitCommand:
    """Test lotr init command."""

    def test_init_creates_bootstrap_files(self, tmp_path):
        """lotr init should create .lotr/AGENTS.md and .lotr/config.json."""
        import sys, json
        sys.path.insert(0, str(Path(__file__).parent.parent / "cli"))
        from lotr import cmd_init

        # Create a mock project with .cursor/
        (tmp_path / ".cursor").mkdir()
        (tmp_path / "package.json").write_text('{"dependencies": {"react": "^18"}}')

        # Mock args
        class Args:
            project_root = str(tmp_path)
        cmd_init(Args())

        # Verify files created
        assert (tmp_path / ".lotr" / "AGENTS.md").exists()
        assert (tmp_path / ".lotr" / "config.json").exists()

        # Verify config.json has detected framework
        config = json.loads((tmp_path / ".lotr" / "config.json").read_text())
        assert config["framework"] == "cursor"
        assert config["language"] in ["javascript", "typescript"]

    def test_init_agents_md_has_commands(self, tmp_path):
        """The AGENTS.md bootstrap file should mention lotr commands."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "cli"))
        from lotr import cmd_init

        (tmp_path / ".cursor").mkdir()

        class Args:
            project_root = str(tmp_path)
        cmd_init(Args())

        content = (tmp_path / ".lotr" / "AGENTS.md").read_text()
        assert "lotr install" in content
        assert "lotr kickoff" in content
        assert "lotr starter" in content
        assert "Gondor" in content
