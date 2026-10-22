"""Open spec check. A spec is not ready while a required section is empty.

The section names follow the specify → plan → tasks order used by Spec Kit,
plus the boundaries this kit requires before implementation.
"""

from __future__ import annotations

REQUIRED = ("goal", "requirements", "acceptance", "plan", "tasks", "boundaries")


def sections(text: str) -> dict[str, str]:
    current = ""
    chunks: dict[str, list[str]] = {}
    for line in (text or "").splitlines():
        if line.startswith("#"):
            current = line.lstrip("#").strip().lower()
            chunks.setdefault(current, [])
            continue
        if current:
            chunks[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in chunks.items()}


def issues(text: str) -> list[str]:
    found = sections(text)
    missing = []
    for name in REQUIRED:
        body = found.get(name, "")
        if not body or body in {"_fill in_", "-", "tbd"}:
            missing.append(name)
    return [f"SDD-3 spec missing {name}" for name in missing]
