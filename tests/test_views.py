import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
CLI = [sys.executable, str(ROOT / "cli" / "mazu.py")]

from mazu_method.calm_draw import draw as draw_calm
from mazu_method.openspec import issues as spec_issues
from mazu_method.sysl_draw import draw as draw_sysl


def test_diagrams_are_svg():
    calm = draw_calm((ROOT / "diagrams/calm/backlog.calm.json").read_text(encoding="utf-8"))
    sysl = draw_sysl((ROOT / "diagrams/sysl/backlog.sysl").read_text(encoding="utf-8"))
    assert calm.startswith("<svg") and "mazu-cli" in calm
    assert sysl.startswith("<svg") and "MazuCli" in sysl
    page = (ROOT / "cli/dashboard.html").read_text(encoding="utf-8")
    assert "&" in page
    assert "view-scrum" in page and "view-backlog" in page and "data-open" in page


def test_sprint_refuses_unready_story(tmp_path):
    subprocess.run(CLI + ["init"], cwd=tmp_path, check=True)
    subprocess.run(CLI + ["add", "story", "Bare", "--points", "3"], cwd=tmp_path, check=True)
    subprocess.run(CLI + ["sprint", "new", "--goal", "Only ready stories"], cwd=tmp_path, check=True)
    refused = subprocess.run(CLI + ["sprint", "add", "--id", "US-001", "--sprint", "S1"], cwd=tmp_path, text=True, capture_output=True)
    assert refused.returncode == 1
    assert "FAIL" in refused.stdout
    filled = tmp_path / "spec.md"
    filled.write_text("# Spec\n\n## Goal\nShip\n\n## Requirements\nWhen saved, the row exists.\n\n## Acceptance\nGiven a user When they save Then the row exists.\n\n## Plan\nUse the store.\n\n## Tasks\n- [ ] write the row\n\n## Boundaries\nNever: commit secrets.\n", encoding="utf-8")
    subprocess.run(CLI + ["check", "spec", str(filled)], cwd=tmp_path, check=True)
    assert spec_issues("# Spec\n\n## Goal\n\n") 
    svg = tmp_path / "calm.svg"
    subprocess.run(CLI + ["diagram", "calm", str(ROOT / "diagrams/calm/example.calm.json"), "-o", str(svg)], cwd=tmp_path, check=True)
    assert svg.read_text(encoding="utf-8").startswith("<svg")
