import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, str(ROOT / "cli" / "mazu.py"), "upstream"]


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(CLI + args, cwd=ROOT, text=True, capture_output=True, check=False)


def test_official_clis_answer():
    openspec = run(["openspec", "--", "version"])
    assert openspec.returncode == 0, openspec.stderr
    assert "1.14.3" in openspec.stdout
    calm = run(["calm", "--", "validate", "--architecture", "diagrams/calm/example.calm.json", "--format", "json"])
    assert calm.returncode == 0, calm.stdout + calm.stderr
    payload = json.loads(calm.stdout)
    assert payload["hasErrors"] is False
    bmad = run(["bmad", "--", "--version"])
    assert bmad.returncode == 0, bmad.stderr
    assert "6.12.4" in bmad.stdout
    change = run(["openspec", "--", "validate", "bind-upstreams", "--strict"])
    assert change.returncode == 0, change.stdout + change.stderr
    assert (ROOT / ".agents/skills/openspec-propose/SKILL.md").exists()
    assert (ROOT / "upstream/packages/openspec/package.json").exists()
    assert (ROOT / "upstream/packages/adr-tools/src/_adr_help").exists()
