"""Initial verification tests for AI NEWS FACTORY project setup."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def test_core_documentation_and_rules():
    assert (ROOT / "AI_NEWS_FACTORY_RULES.md").exists()
    assert (ROOT / "AI_NEWS_VISUAL_STYLE_BIBLE_v1.0.md").exists()
    assert (ROOT / "START_HERE.md").exists()
    assert (ROOT / "RUNBOOK.md").exists()
    assert (ROOT / "config" / "factory.yaml").exists()

def test_schemas_exist():
    schemas = [
        "news_candidates.schema.json",
        "verified_news.schema.json",
        "script.schema.json",
        "visual_plan.schema.json",
        "qa_report.schema.json",
    ]
    for s in schemas:
        schema_file = ROOT / "schemas" / s
        assert schema_file.exists(), f"Missing schema: {s}"
        with open(schema_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert isinstance(data, dict)

def test_data_directories_exist():
    dirs = [
        "data/inbox",
        "data/verified",
        "data/scripts",
        "data/visuals",
        "data/qa",
        "data/rendered",
    ]
    for d in dirs:
        dir_path = ROOT / d
        assert dir_path.is_dir(), f"Missing data directory: {d}"

def test_agents_and_skills_exist():
    agents = [
        "news-hunter.md",
        "fact-checker.md",
        "storyteller.md",
        "visual-storyteller.md",
        "qa-publisher.md",
        "orchestrator.md",
    ]
    for a in agents:
        agent_file = ROOT / ".agents" / "agents" / a
        assert agent_file.exists(), f"Missing agent definition: {a}"

    skills = [
        "ai-news-research",
        "ai-news-qa",
        "ai-news-storytelling",
        "ai-news-visuals",
    ]
    for sk in skills:
        skill_dir = ROOT / ".agents" / "skills" / sk
        assert skill_dir.is_dir(), f"Missing skill directory: {sk}"
        assert (skill_dir / "SKILL.md").exists(), f"Missing SKILL.md in {sk}"
