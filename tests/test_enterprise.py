import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_enterprise_demo(tmp_path):
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "enterprise_demo.py"), str(tmp_path / "demo")],
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = (ROOT / "docs" / "BATTLE_REPORT.md").read_text(encoding="utf-8")
    assert "Не совпало: 0" in report
    assert "works well" in report or "Плохой сценарий" in report
    html = (ROOT / "docs" / "demo" / "dashboard.html").read_text(encoding="utf-8")
    assert "Сохранить карточку" in html
    assert "MAZU-ADGILE" in html
