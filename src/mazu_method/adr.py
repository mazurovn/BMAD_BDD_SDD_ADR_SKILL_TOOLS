"""ADR files: context, decision, consequences. Supersede by a new file. Never delete."""

from __future__ import annotations

REQUIRED = ("status", "context", "decision", "consequences")


def render(item_id: str, title: str, status: str, context: str) -> str:
    body = context.strip() or "_fill in_"
    return "\n".join(
        [
            f"# {item_id}: {title}",
            "",
            "## Status",
            status,
            "",
            "## Context",
            body,
            "",
            "## Decision",
            "_fill in_",
            "",
            "## Consequences",
            "- Positive:",
            "- Negative:",
            "",
        ]
    )


def section_map(text: str) -> dict[str, str]:
    current = ""
    chunks: dict[str, list[str]] = {}
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip().lower()
            chunks.setdefault(current, [])
            continue
        if current:
            chunks[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in chunks.items()}


def issues(text: str) -> list[str]:
    found = section_map(text or "")
    missing = [name for name in REQUIRED if not found.get(name)]
    out = [f"ADR-2 missing {name}" for name in missing]
    decision = found.get("decision", "")
    if decision.strip() in {"", "_fill in_"}:
        out.append("ADR-2 decision is empty")
    context = found.get("context", "")
    if context.strip() in {"", "_fill in_"}:
        out.append("ADR-2 context is empty")
    return out


def supersede_note(old_id: str, new_id: str) -> str:
    return f"Superseded by {new_id}. Keep {old_id}. Do not delete it."
