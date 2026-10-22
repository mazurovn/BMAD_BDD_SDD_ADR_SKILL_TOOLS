"""ADR files: context, decision, consequences. Supersede by a new file. Never delete."""

from __future__ import annotations

REQUIRED = ("status", "context", "decision", "consequences")


def render(
    item_id: str,
    title: str,
    status: str,
    context: str,
    decision: str | None = None,
    consequences: str | None = None,
) -> str:
    body = context.strip() or "_fill in_"
    decision_body = (decision or "").strip() or "_fill in_"
    if consequences and consequences.strip():
        consequences_body = consequences.strip()
    else:
        consequences_body = "- Positive:\n- Negative:"
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
            decision_body,
            "",
            "## Consequences",
            consequences_body,
            "",
        ]
    )


def fill_sections(
    text: str,
    *,
    context: str | None = None,
    decision: str | None = None,
    consequences: str | None = None,
) -> str:
    """Replace named ADR sections. Leaves unspecified sections unchanged."""
    found = section_map(text or "")
    if context is not None and context.strip():
        found["context"] = context.strip()
    if decision is not None and decision.strip():
        found["decision"] = decision.strip()
    if consequences is not None and consequences.strip():
        found["consequences"] = consequences.strip()
    # Rebuild from original heading order when possible
    lines = (text or "").splitlines()
    if not lines:
        return text
    title = lines[0]
    status = found.get("status") or "backlog"
    return "\n".join(
        [
            title,
            "",
            "## Status",
            status,
            "",
            "## Context",
            found.get("context") or "_fill in_",
            "",
            "## Decision",
            found.get("decision") or "_fill in_",
            "",
            "## Consequences",
            found.get("consequences") or "- Positive:\n- Negative:",
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
