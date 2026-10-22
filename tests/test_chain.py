import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_command_chain(tmp_path):
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "command_chain.py"), str(tmp_path / "chain")],
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = (ROOT / "docs" / "COMMAND_CHAIN.md").read_text(encoding="utf-8")
    assert "Не совпало: 0" in report
    for name in ("openspec_flow.propose", "bdd.acceptance_issues", "sdd.guard", "bmad.phase_issues", "adr.issues", "sysl_check.issues", "calm_check.issues"):
        assert name in report
    archived = list((tmp_path / "chain" / "openspec" / "changes" / "archive").glob("*-gate-visible"))
    assert archived
    assert (tmp_path / "chain" / "openspec" / "specs" / "gate-visible" / "spec.md").exists()
    assert not (tmp_path / "chain" / "openspec" / "changes" / "gate-visible").exists()
