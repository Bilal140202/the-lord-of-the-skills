"""
Tests for crawler.classify — LOTR kingdom classifier
"""
import sys
from pathlib import Path

# Add crawler to path
CRAWLER_DIR = Path(__file__).parent.parent / "crawler"
sys.path.insert(0, str(CRAWLER_DIR))

import pytest
from classify import (
    KINGDOM_KEYWORDS, classify_kingdom, classify_skill_type,
    extract_title, extract_summary,
)
from dedup import (
    canonical_score, jaccard, normalize_title,
    FRAMEWORK_PRIORITY, SKILL_TYPE_PRIORITY,
)


class TestKingdomClassification:
    """Test LOTR kingdom assignment."""

    def test_gondor_coding(self):
        content = "This skill helps with coding, refactoring TypeScript React components and debugging git commits."
        kingdom = classify_kingdom(content, "claude-code", "skills/coding/SKILL.md")
        assert kingdom == "gondor"

    def test_rivendell_research(self):
        content = "Research methodology for analyzing academic papers and synthesizing literature reviews."
        kingdom = classify_kingdom(content, "claude-code", "skills/research/SKILL.md")
        assert kingdom == "rivendell"

    def test_moria_devops(self):
        content = "Deploy to Kubernetes with Docker containers via Terraform on AWS. CI/CD pipeline included."
        kingdom = classify_kingdom(content, "claude-code", "skills/devops/SKILL.md")
        assert kingdom == "moria"

    def test_mordor_security(self):
        content = "Security audit for OWASP top 10 vulnerabilities including XSS, CSRF, SSRF, and SQL injection."
        kingdom = classify_kingdom(content, "claude-code", "skills/security/SKILL.md")
        assert kingdom == "mordor"

    def test_isengard_agents(self):
        content = "Multi-agent orchestration workflow with subagents for task delegation."
        kingdom = classify_kingdom(content, "claude-code", "skills/agents/SKILL.md")
        assert kingdom == "isengard"

    def test_rohan_testing(self):
        content = "Run unit tests, integration tests, and e2e tests with coverage reports and lint checks."
        kingdom = classify_kingdom(content, "claude-code", "skills/testing/SKILL.md")
        assert kingdom == "rohan"

    def test_fangorn_memory(self):
        content = "Memory bank for preserving context across agent sessions using embeddings and RAG."
        kingdom = classify_kingdom(content, "claude-code", "skills/memory/SKILL.md")
        assert kingdom == "fangorn"

    def test_lothlorien_data(self):
        content = "Data analysis with pandas, numpy, and matplotlib for statistical visualization."
        kingdom = classify_kingdom(content, "claude-code", "skills/data/SKILL.md")
        assert kingdom == "lothlorien"

    def test_the_shire_writing(self):
        content = "Writing blog posts, documentation, and marketing copy with proper grammar and tone."
        kingdom = classify_kingdom(content, "claude-code", "skills/writing/SKILL.md")
        assert kingdom == "the-shire"

    def test_mirkwood_fallback(self):
        # Truly neutral content with no kingdom keywords at all
        content = "xyz abc def ghi jkl mno pqr stu vwx zzz."
        kingdom = classify_kingdom(content, "general", "random/xyz.md")
        assert kingdom == "mirkwood"

    def test_all_kingdoms_have_keywords(self):
        for kingdom, spec in KINGDOM_KEYWORDS.items():
            assert "keywords" in spec, f"{kingdom} missing keywords"
            assert len(spec["keywords"]) > 0, f"{kingdom} has no keywords"
            assert "domain_label" in spec, f"{kingdom} missing domain_label"
            assert "motto" in spec, f"{kingdom} missing motto"

    def test_framework_bias_for_agent_repos(self):
        content = "agent subagent workflow"
        kingdom = classify_kingdom(content, "claude-code", "skills/agent.md")
        assert kingdom == "isengard"


class TestSkillTypeClassification:
    """Test skill type assignment."""

    def test_planning(self):
        content = "Plan the task by decomposing it into steps with a clear strategy."
        skill_type = classify_skill_type(content, "skills/plan.md", "plan.md")
        assert skill_type == "planning"

    def test_execution(self):
        content = "Execute the task by running the implementation and carrying out the operation."
        skill_type = classify_skill_type(content, "skills/execute.md", "execute.md")
        assert skill_type == "execution"

    def test_verification(self):
        content = "Verify the output by validating assertions and running tests."
        skill_type = classify_skill_type(content, "skills/verify.md", "verify.md")
        assert skill_type == "verification"

    def test_conventions_from_filename(self):
        # CONVENTIONS.md filename + neutral content (no skill-type keywords)
        # should default to conventions via filename heuristic
        content = "xyz abc def ghi jkl mno."
        skill_type = classify_skill_type(content, "CONVENTIONS.md", "CONVENTIONS.md")
        assert skill_type == "conventions"

    def test_prompts_from_filename(self):
        # .prompt.md filename + neutral content should default to prompts
        content = "xyz abc def ghi jkl mno."
        skill_type = classify_skill_type(content, "my-prompt.prompt.md", "my-prompt.prompt.md")
        assert skill_type == "prompts"


class TestTitleExtraction:
    """Test title extraction from markdown files."""

    def test_from_frontmatter(self):
        content = "---\ntitle: My Awesome Skill\ndescription: A skill\n---\n\n# Body"
        assert extract_title(content, "SKILL.md") == "My Awesome Skill"

    def test_from_h1(self):
        content = "# My Awesome Skill\n\nBody text here."
        assert extract_title(content, "SKILL.md") == "My Awesome Skill"

    def test_from_filename_fallback(self):
        content = "Just body text, no title."
        assert extract_title(content, "my-skill.md") == "My Skill"

    def test_frontmatter_with_quotes(self):
        content = '---\ntitle: "Quoted Title"\n---\n\nBody'
        assert extract_title(content, "SKILL.md") == "Quoted Title"


class TestSummaryExtraction:
    """Test summary extraction from markdown files."""

    def test_basic_summary(self):
        content = "# Title\n\nThis is the first paragraph of the skill. It has multiple sentences.\n\nSecond paragraph."
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

    def test_max_length(self):
        content = "# Title\n\n" + "A" * 500
        summary = extract_summary(content, max_len=100)
        assert len(summary) <= 103


class TestNormalizeTitle:
    """Test title normalization for dedup."""

    def test_lowercase(self):
        assert normalize_title("Git Commit") == "git commit"

    def test_strip_punctuation(self):
        assert normalize_title("Git-Commit!") == "git commit"

    def test_whitespace(self):
        assert normalize_title("  Git   Commit  ") == "git commit"


class TestJaccardSimilarity:
    """Test Jaccard similarity for dedup."""

    def test_identical(self):
        a = {"a", "b", "c"}
        assert jaccard(a, a) == 1.0

    def test_disjoint(self):
        assert jaccard({"a"}, {"b"}) == 0.0

    def test_partial(self):
        assert jaccard({"a", "b", "c"}, {"a", "b", "d"}) == 0.5

    def test_empty(self):
        assert jaccard(set(), {"a"}) == 0.0
        assert jaccard(set(), set()) == 0.0


class TestCanonicalScore:
    """Test canonical score calculation."""

    def test_claude_code_higher_than_general(self):
        claude_rec = {"framework": "claude-code", "skill_type": "execution", "size_bytes": 5000, "filename": "SKILL.md"}
        general_rec = {"framework": "general", "skill_type": "execution", "size_bytes": 5000, "filename": "SKILL.md"}
        assert canonical_score(claude_rec) > canonical_score(general_rec)

    def test_canonical_filename_bonus(self):
        with_bonus = {"framework": "claude-code", "skill_type": "conventions", "size_bytes": 5000, "filename": "SKILL.md"}
        without = {"framework": "claude-code", "skill_type": "conventions", "size_bytes": 5000, "filename": "random.md"}
        assert canonical_score(with_bonus) > canonical_score(without)

    def test_all_frameworks_have_priority(self):
        for fw in ["claude-code", "cursor", "cline", "roo", "aider", "openhands",
                   "codex", "continue", "goose", "copilot", "autogen", "crewai",
                   "langgraph", "general"]:
            assert fw in FRAMEWORK_PRIORITY, f"Missing framework priority: {fw}"

    def test_all_skill_types_have_priority(self):
        for st in ["planning", "execution", "verification", "memory", "tools",
                   "prompts", "orchestration", "conventions", "other"]:
            assert st in SKILL_TYPE_PRIORITY, f"Missing skill type priority: {st}"


class TestKingdomData:
    """Sanity checks on kingdom data structures."""

    def test_all_10_kingdoms_present(self):
        expected = {"gondor", "rivendell", "moria", "lothlorien", "mordor",
                    "the-shire", "isengard", "rohan", "fangorn", "mirkwood"}
        assert set(KINGDOM_KEYWORDS.keys()) == expected

    def test_every_kingdom_has_motto(self):
        for kingdom, spec in KINGDOM_KEYWORDS.items():
            assert spec["motto"], f"{kingdom} has empty motto"
            assert isinstance(spec["motto"], str)
            assert len(spec["motto"]) > 10

    def test_every_kingdom_has_keywords(self):
        for kingdom, spec in KINGDOM_KEYWORDS.items():
            assert len(spec["keywords"]) >= 5, f"{kingdom} has too few keywords"
