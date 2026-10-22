"""Minimal Sysl check. The text file is the source. A picture is optional."""

from __future__ import annotations

import re

_SECRET = re.compile(r"(password\s*=|secret\s*=|api[_-]?key\s*=|AKIA[0-9A-Z]{8})", re.IGNORECASE)


def issues(text: str) -> list[str]:
    raw = text or ""
    if not raw.strip():
        return ["SYSL-2 file is empty"]
    found: list[str] = []
    if _SECRET.search(raw):
        found.append("SYSL-2 secret-like text")
    apps = []
    for line in raw.splitlines():
        if line.startswith("#") or not line.strip():
            continue
        if line[:1].isspace():
            continue
        if line.rstrip().endswith(":"):
            apps.append(line.strip())
    if not apps:
        found.append("SYSL-2 no application block")
    if "return " not in raw:
        found.append("SYSL-2 no return")
    if "<:" not in raw:
        found.append("SYSL-2 return has no type")
    endpoints = [line.strip() for line in raw.splitlines() if line.strip().startswith("/")]
    if not endpoints:
        found.append("SYSL-2 no endpoint")
    return found
