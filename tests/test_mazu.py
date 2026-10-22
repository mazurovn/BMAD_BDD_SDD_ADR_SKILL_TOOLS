import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "cli" / "mazu.py"


def load_cli():
    spec = importlib.util.spec_from_file_location("mazu", CLI)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_flow(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    mod = load_cli()
    mod.main(["init"])
    mod.main(["add", "idea", "Ship a portable backlog"])
    mod.main(["add", "epic", "Backlog CLI", "--parent", "IDEA-001"])
    mod.main(
        [
            "add",
            "story",
            "List backlog",
            "--parent",
            "EPIC-001",
            "--points",
            "3",
            "--acceptance",
            "Given items exist When I list Then I see ids",
            "--always",
            "keep store json valid",
            "--ask-first",
            "change schema",
            "--never",
            "delete history",
        ]
    )
    mod.main(
        [
            "add",
            "adr",
            "Store JSON locally",
            "--description",
            "One operator",
            "--decision",
            "One JSON store file",
            "--consequences",
            "- Positive: simple\n- Negative: no concurrent writers",
        ]
    )
    mod.main(["sprint", "new", "--goal", "CLI works"])
    mod.main(["sprint", "add", "--id", "US-001", "--sprint", "S1"])
    mod.main(["move", "US-001", "in-progress"])
    mod.main(["log", "US-001", "1.5", "--note", "first slice"])
    mod.main(["evidence", "US-001", "--run", sys.executable, "-c", "print('list printed the ids')"])
    mod.main(["move", "US-001", "review"])
    mod.main(["move", "US-001", "done"])
    data = json.loads((tmp_path / "mazu-data" / "store.json").read_text())
    assert data["items"][2]["points"] == 3
    assert data["items"][2]["status"] == "done"
    assert data["items"][2]["sprint"] == "S1"
    assert data["time_logs"][0]["hours"] == 1.5
    assert (tmp_path / "mazu-data" / "adr" / "ADR-001.md").exists()
    mod.main(["dashboard"])
    html = (tmp_path / "mazu-data" / "dashboard.html").read_text()
    assert "MAZU-ADGILE" in html
    assert "US-001" in html


def test_rejects_bad_points(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    mod = load_cli()
    mod.main(["init"])
    try:
        mod.main(["add", "story", "Too odd", "--points", "4"])
    except SystemExit as exc:
        assert exc.code != 0
    else:
        raise AssertionError("expected exit")


def test_doctor_from_repo():
    proc = subprocess.run([sys.executable, str(CLI), "doctor"], cwd=ROOT, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "ok:" in proc.stdout
