import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, str(ROOT / "cli" / "mazu.py"), "upstream"]


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(CLI + args, cwd=ROOT, text=True, capture_output=True, check=False)


def test_every_shipped_cli_runs():
    expected = {
        "openspec": "1.14.3",
        "bmad": "6.12.4",
        "cucumber": "13.3.0",
        "sysl": "0.792.0",
        "specify": "1.2.3",
    }
    for tool, marker in expected.items():
        args = ["--version"] if tool != "specify" else ["version"]
        if tool == "sysl":
            args = ["--version"]
        proc = run([tool, "--", *args])
        blob = proc.stdout + proc.stderr
        assert proc.returncode == 0, blob
        assert marker in blob, blob
    calm = run(["calm", "--", "validate", "--architecture", "diagrams/calm/example.calm.json", "--format", "json"])
    assert calm.returncode == 0 and '"hasErrors": false' in calm.stdout
    sysl = run(["sysl", "--", "validate", "diagrams/sysl/example.sysl"])
    assert sysl.returncode == 0, sysl.stderr
    adr = run(["adr", "--", "help"])
    assert adr.returncode == 0 and "init" in adr.stdout
    feature = run(["cucumber", "--", "examples/bdd/gate.feature", "--require", "examples/bdd/steps.js"])
    assert feature.returncode == 0, feature.stdout + feature.stderr
    page = (ROOT / "wiki" / "Commands.md").read_text(encoding="utf-8")
    assert "http://" not in page and "https://" not in page
    assert "OpenSpec" in page and "Sysl" in page and "Specify" in page
