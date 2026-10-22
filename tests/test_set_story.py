"""Public set/edit story command."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, str(ROOT / "cli" / "mazu.py")]


def _run(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(CLI + list(args), cwd=cwd, text=True, capture_output=True)


def _story(tmp_path: Path) -> None:
    _run(tmp_path, "init").check_returncode()
    _run(tmp_path, "add", "idea", "Outcome").check_returncode()
    _run(tmp_path, "add", "epic", "Slice", "--parent", "IDEA-001").check_returncode()
    r = _run(
        tmp_path,
        "add",
        "story",
        "Attach later",
        "--parent",
        "EPIC-001",
        "--points",
        "3",
        "--acceptance",
        "Given a When b Then c exists",
        "--always",
        "Keep store valid",
        "--never",
        "Commit secrets",
    )
    r.check_returncode()


def test_set_acceptance_and_merge_never(tmp_path):
    _story(tmp_path)
    r = _run(
        tmp_path,
        "set",
        "story",
        "US-001",
        "--acceptance",
        "Given backlog When set --acceptance Then show lists new lines | Given Never When set --never Then union keeps old",
        "--never",
        "Commit mazu-data into the method repo",
    )
    assert r.returncode == 0, r.stderr + r.stdout
    assert "US-001" in r.stdout
    assert "role hint" in r.stderr
    item = json.loads(_run(tmp_path, "show", "US-001").stdout)
    assert len(item["acceptance"]) == 2
    assert "Commit secrets" in item["boundaries"]["never"]
    assert "Commit mazu-data into the method repo" in item["boundaries"]["never"]
    assert _run(tmp_path, "check", "bdd", "US-001").returncode == 0
    assert _run(tmp_path, "check", "boundaries", "US-001").returncode == 0


def test_empty_never_is_noop_and_edit_alias(tmp_path):
    _story(tmp_path)
    before = json.loads(_run(tmp_path, "show", "US-001").stdout)["boundaries"]["never"]
    r = _run(tmp_path, "edit", "story", "US-001", "--never", "")
    assert r.returncode == 0, r.stderr + r.stdout
    after = json.loads(_run(tmp_path, "show", "US-001").stdout)["boundaries"]["never"]
    assert after == before


def test_refuse_acceptance_on_done(tmp_path):
    _story(tmp_path)
    # Force status done in store to exercise EDIT-1 without full QA path.
    store = tmp_path / "mazu-data" / "store.json"
    data = json.loads(store.read_text(encoding="utf-8"))
    for item in data["items"]:
        if item["id"] == "US-001":
            item["status"] = "done"
    store.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    r = _run(tmp_path, "set", "story", "US-001", "--acceptance", "Given x When y Then z")
    assert r.returncode != 0
    assert "EDIT-1" in (r.stderr + r.stdout)


def test_replace_never_still_unions(tmp_path):
    _story(tmp_path)
    r = _run(
        tmp_path,
        "set",
        "story",
        "US-001",
        "--boundaries-mode",
        "replace",
        "--always",
        "Only this always",
        "--never",
        "Delete a check to go green",
    )
    assert r.returncode == 0, r.stderr + r.stdout
    item = json.loads(_run(tmp_path, "show", "US-001").stdout)
    assert item["boundaries"]["always"] == ["Only this always"]
    assert "Commit secrets" in item["boundaries"]["never"]
    assert "Delete a check to go green" in item["boundaries"]["never"]
