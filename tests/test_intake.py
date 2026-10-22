import json
from pathlib import Path

import pytest

from test_mazu import CLI, ROOT, load_cli


def test_intake_builds_a_ready_sprint(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    mod = load_cli()
    mod.main(["init"])
    mod.main(["intake", "--file", str(ROOT / "examples" / "intake.md")])
    store = json.loads((tmp_path / "mazu-data" / "store.json").read_text(encoding="utf-8"))
    kinds = {item["kind"] for item in store["items"]}
    assert {"idea", "epic", "story", "requirement"} <= kinds
    stories = [item for item in store["items"] if item["kind"] == "story"]
    assert stories
    assert all(item.get("sprint") for item in stories)
    assert all(item["parent"] for item in stories)
    epic = next(item for item in store["items"] if item["kind"] == "epic")
    assert (tmp_path / "mazu-data" / "specs" / f"{epic['id']}.md").exists()
    assert (tmp_path / "mazu-data" / "calm.json").exists()
    assert "GET:" in (tmp_path / "mazu-data" / "system.sysl").read_text(encoding="utf-8")
    mod.main(["trace", "IDEA-001"])
    mod.main(["gate", "ready", stories[0]["id"]])


def test_intake_rejects_unlabeled_text(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    mod = load_cli()
    mod.main(["init"])
    with pytest.raises(SystemExit):
        mod.main(["intake", "--text", "просто абзац без метки"])


def test_cli_help_lists_intake():
    import subprocess
    import sys

    proc = subprocess.run([sys.executable, str(CLI), "--help"], text=True, capture_output=True, check=True)
    assert "intake" in proc.stdout
    assert "trace" in proc.stdout
    assert Path(ROOT / "src" / "mazu_method" / "intake.py").exists()
