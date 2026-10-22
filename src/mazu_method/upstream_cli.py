"""Run a published CLI that ships with this repo. A missing binary is an error."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BIN = ROOT / "upstream" / "node_modules" / ".bin"


def resolve(tool: str) -> list[str]:
    if tool == "openspec":
        return [str(BIN / "openspec")]
    if tool == "calm":
        return [str(BIN / "calm")]
    if tool in {"bmad", "bmad-method"}:
        return [str(BIN / tool)]
    if tool == "cucumber":
        return [str(BIN / "cucumber-js")]
    if tool == "adr":
        return [str(ROOT / "upstream" / "packages" / "adr-tools" / "src" / "adr")]
    if tool == "sysl":
        return [str(ROOT / "upstream" / "bin" / "sysl")]
    if tool == "specify":
        return [str(ROOT / "upstream" / "bin" / "specify")]
    known = "openspec, calm, bmad, bmad-method, cucumber, adr, sysl, specify"
    raise SystemExit(f"UPSTREAM-1 unknown tool {tool}. Known: {known}")


def execute(tool: str, args: list[str]) -> int:
    command = resolve(tool)
    if not Path(command[0]).exists():
        raise SystemExit(f"UPSTREAM-1 {tool} is not in the repo at {command[0]}")
    env = dict(**subprocess.os.environ)
    node_path = str(ROOT / "upstream" / "node_modules")
    env["NODE_PATH"] = node_path if not env.get("NODE_PATH") else node_path + ":" + env["NODE_PATH"]
    return subprocess.run(command + args, env=env).returncode
