from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_skills_and_agents_are_procedures():
    skills = list((ROOT / "skills").glob("*/SKILL.md"))
    assert len(skills) >= 17
    for path in skills:
        text = path.read_text(encoding="utf-8")
        assert len(text.splitlines()) >= 70, path
        assert "Не делать" in text
        assert "python3 cli/mazu.py" in text
        assert "Гейты" in text or "Гейт" in text
    for path in (ROOT / "agents").glob("*.md"):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        assert len(text.splitlines()) >= 70, path
        assert "Не делать" in text
        assert "Гардрейлы" in text
        assert "python3 cli/mazu.py" in text or "scripts/audit.py" in text
