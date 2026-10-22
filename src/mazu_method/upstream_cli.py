"""Run a CLI that is stored in this repo. A missing file is an error, not a pass."""

from __future__ import annotations

import lzma
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def node_binary() -> Path:
    binary = ROOT / "upstream" / "node" / "node"
    if binary.exists():
        return binary
    packed = ROOT / "upstream" / "node" / "node.xz"
    if not packed.exists():
        raise SystemExit("UPSTREAM-1 upstream/node/node.xz is missing")
    binary.write_bytes(lzma.open(packed, "rb").read())
    binary.chmod(0o755)
    return binary


def resolve(tool: str) -> list[str]:
    node = str(node_binary())
    if tool == "openspec":
        return [node, str(ROOT / "upstream/node_modules/@fission-ai/openspec/bin/openspec.js")]
    if tool == "calm":
        return [node, str(ROOT / "upstream/node_modules/@finos/calm-cli/dist/index.js")]
    if tool in {"bmad", "bmad-method"}:
        return [node, str(ROOT / "upstream/node_modules/bmad-method/tools/installer/bmad-cli.js")]
    if tool == "cucumber":
        return [node, str(ROOT / "upstream/node_modules/@cucumber/cucumber/bin/cucumber.js")]
    if tool == "adr":
        return [str(ROOT / "upstream/packages/adr-tools/src/adr")]
    if tool == "sysl":
        return [str(ROOT / "bin/sysl")]
    if tool == "specify":
        return [str(ROOT / "bin/specify")]
    raise SystemExit(
        "UPSTREAM-1 unknown tool "
        + tool
        + ". Known: openspec, calm, bmad, bmad-method, cucumber, adr, sysl, specify"
    )


def execute(tool: str, args: list[str]) -> int:
    command = resolve(tool)
    if not Path(command[-1]).exists() and not Path(command[0]).exists():
        raise SystemExit(f"UPSTREAM-1 {tool} is not in the repo at {command[-1]}")
    env = dict(os.environ)
    node_path = str(ROOT / "upstream" / "node_modules")
    env["NODE_PATH"] = node_path if not env.get("NODE_PATH") else node_path + ":" + env["NODE_PATH"]
    if tool == "adr":
        env["PATH"] = str(ROOT / "upstream/packages/adr-tools/src") + os.pathsep + env.get("PATH", "")
    return subprocess.run(command + args, env=env).returncode
