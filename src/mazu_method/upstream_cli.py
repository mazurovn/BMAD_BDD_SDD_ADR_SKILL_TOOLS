"""Run a published CLI from upstream/node_modules. Missing install is an error."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BIN = ROOT / "upstream" / "node_modules" / ".bin"
INSTALL = "npm ci --prefix upstream"
TOOLS = {
    "openspec": "openspec",
    "calm": "calm",
    "bmad": "bmad",
    "bmad-method": "bmad-method",
}


def binary(tool: str) -> Path:
    name = TOOLS.get(tool)
    if not name:
        known = ", ".join(sorted(TOOLS))
        raise SystemExit(f"UPSTREAM-1 unknown tool {tool}. Known: {known}")
    path = BIN / name
    if not path.exists():
        raise SystemExit(f"UPSTREAM-1 {tool} is not installed. Run: {INSTALL}")
    return path


def execute(tool: str, args: list[str]) -> int:
    proc = subprocess.run([str(binary(tool)), *args])
    return proc.returncode
