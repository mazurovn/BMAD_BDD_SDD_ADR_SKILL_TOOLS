import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, str(ROOT / "cli" / "mazu.py")]


def test_board_renders_ten_checks(tmp_path):
    subprocess.run(CLI + ["init"], cwd=tmp_path, check=True)
    subprocess.run(CLI + ["intake", "--file", str(ROOT / "examples" / "intake.md")], cwd=tmp_path, check=True)
    subprocess.run(CLI + ["dashboard"], cwd=tmp_path, check=True)
    page = tmp_path / "mazu-data" / "dashboard.html"
    proc = subprocess.run(["node", str(ROOT / "tests" / "board_check.js"), str(page)], text=True, capture_output=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert proc.stdout.count("PASS ") == 10
