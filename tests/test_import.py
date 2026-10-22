import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, str(ROOT / "cli" / "mazu.py")]


def run(tmp_path, *args):
    return subprocess.run(CLI + list(args), cwd=tmp_path, text=True, capture_output=True, check=True)


def test_jira_csv_and_project(tmp_path):
    run(tmp_path, "project", "new", "demo")
    run(tmp_path, "import", "jira-csv", str(ROOT / "examples" / "jira.csv"))
    store = json.loads((tmp_path / "mazu-data" / "projects" / "demo" / "store.json").read_text())
    by_key = {item["external_id"]: item for item in store["items"]}
    assert by_key["ABC-1"]["kind"] == "epic"
    assert by_key["ABC-1"]["status"] == "backlog"
    assert by_key["ABC-2"]["points"] == 3
    assert by_key["ABC-2"]["status"] == "in-progress"
    assert by_key["ABC-3"]["points"] is None
    assert by_key["ABC-3"]["kind"] == "task"


def test_xlsx_roundtrip(tmp_path):
    run(tmp_path, "init")
    run(tmp_path, "add", "story", "Roundtrip", "--points", "2")
    run(tmp_path, "export", "xlsx", "board.xlsx")
    run(tmp_path, "import", "xlsx", "board.xlsx")
    data = json.loads((tmp_path / "mazu-data" / "store.json").read_text())
    titles = [item["title"] for item in data["items"]]
    assert titles.count("Roundtrip") == 2


def test_pull_without_tokens(tmp_path, monkeypatch):
    monkeypatch.delenv("JIRA_BASE_URL", raising=False)
    monkeypatch.delenv("JIRA_EMAIL", raising=False)
    monkeypatch.delenv("JIRA_TOKEN", raising=False)
    result = subprocess.run(CLI + ["pull", "jira"], cwd=tmp_path, text=True, capture_output=True)
    assert result.returncode != 0
    assert "not connected" in result.stderr + result.stdout
