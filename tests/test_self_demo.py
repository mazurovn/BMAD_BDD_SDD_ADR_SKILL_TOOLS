"""self-demo.sh (run by release) leaves the operator's active project as it found it."""
from __future__ import annotations

import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _kit_without_bin(tmp_path: Path) -> Path:
    """cli, src and scripts only: the demo switches to kit-self, then fails at the first bin/ call."""
    kit = tmp_path / "kit"
    for name in ("cli", "src", "scripts"):
        shutil.copytree(ROOT / name, kit / name, ignore=shutil.ignore_patterns("__pycache__"))
    return kit


def _demo(kit: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["sh", "scripts/self-demo.sh"], cwd=kit, text=True, capture_output=True)


def test_failed_demo_restores_previous_project(tmp_path):
    kit = _kit_without_bin(tmp_path)
    cli = [sys.executable, "cli/mazu.py"]
    subprocess.run(cli + ["project", "new", "mine"], cwd=kit, check=True, capture_output=True)
    proc = _demo(kit)
    assert proc.returncode != 0
    assert (kit / "mazu-data" / "projects" / "kit-self" / "store.json").exists()
    assert (kit / "mazu-data" / "active-project").read_text(encoding="utf-8").strip() == "mine"
    listing = subprocess.run(cli + ["project", "list"], cwd=kit, text=True, capture_output=True, check=True)
    assert "* mine" in listing.stdout


def test_terminated_demo_restores_previous_project(tmp_path):
    kit = _kit_without_bin(tmp_path)
    subprocess.run([sys.executable, "cli/mazu.py", "project", "new", "mine"], cwd=kit, check=True, capture_output=True)
    pointer = kit / "mazu-data" / "active-project"
    proc = subprocess.Popen(["sh", "scripts/self-demo.sh"], cwd=kit, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline = time.monotonic() + 30
    while pointer.read_text(encoding="utf-8").strip() != "kit-self":
        assert proc.poll() is None and time.monotonic() < deadline
        time.sleep(0.05)
    proc.send_signal(signal.SIGTERM)
    assert proc.wait(timeout=30) != 0
    assert pointer.read_text(encoding="utf-8").strip() == "mine"


def test_demo_without_previous_project_leaves_no_pointer(tmp_path):
    kit = _kit_without_bin(tmp_path)
    proc = _demo(kit)
    assert proc.returncode != 0
    assert (kit / "mazu-data" / "projects" / "kit-self" / "store.json").exists()
    assert not (kit / "mazu-data" / "active-project").exists()
