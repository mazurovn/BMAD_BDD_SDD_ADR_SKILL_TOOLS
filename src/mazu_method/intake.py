"""Turn raw notes into a backlog plan. The plan is data. The CLI writes it."""

from __future__ import annotations

import json
import re

MARKERS = {
    "pain": "pain",
    "боль": "pain",
    "interview": "interview",
    "интервью": "interview",
    "idea": "idea",
    "идея": "idea",
    "task": "task",
    "задача": "task",
    "research": "research",
    "исследование": "research",
}

_HEAD = re.compile(r"^\s*(?:#{1,3}\s*)?([A-Za-zА-Яа-я]+)\s*:\s*(.*)$")


def parse_notes(text: str) -> list[dict]:
    notes: list[dict] = []
    kind = ""
    buf: list[str] = []

    def flush() -> None:
        body = " ".join(part.strip() for part in buf if part.strip()).strip()
        if kind and body:
            notes.append({"kind": kind, "text": body})

    for raw in (text or "").splitlines():
        match = _HEAD.match(raw.strip())
        word = match.group(1).lower() if match else ""
        if word in MARKERS:
            flush()
            kind = MARKERS[word]
            buf = [match.group(2)]
            continue
        if kind:
            buf.append(raw)
    flush()
    return notes


def _quote(text: str, limit: int = 90) -> str:
    flat = " ".join(text.split())
    if len(flat) <= limit:
        return flat
    return flat[: limit - 1].rstrip() + "…"


def acceptance_for(text: str) -> str:
    return (
        "Given the source note is stored "
        f"When the operator opens the card "
        f"Then the card shows: {_quote(text, 80)}"
    )


def boundaries() -> dict[str, list[str]]:
    return {
        "always": ["keep the source quote on the card"],
        "ask_first": ["merge two notes into one story"],
        "never": ["invent a customer quote"],
    }


def plan(text: str) -> dict:
    notes = parse_notes(text)
    if not notes:
        raise ValueError("INTAKE-1 no labeled notes")
    groups: list[dict] = []
    current: dict | None = None

    def ensure() -> dict:
        nonlocal current
        if current is None:
            current = {"idea": "Собрать беклог из сырых заметок", "notes": []}
            groups.append(current)
        return current

    for note in notes:
        if note["kind"] == "idea":
            current = {"idea": _quote(note["text"], 120), "notes": [note]}
            groups.append(current)
            continue
        ensure()["notes"].append(note)
    slices = []
    for group in groups:
        stories = []
        requirements = []
        for note in group["notes"]:
            if note["kind"] == "idea":
                continue
            if note["kind"] in {"pain", "task"}:
                stories.append(
                    {
                        "title": _quote(note["text"], 90),
                        "source": note["kind"],
                        "points": 3 if note["kind"] == "pain" else 2,
                        "acceptance": acceptance_for(note["text"]),
                        "boundaries": boundaries(),
                        "description": note["text"],
                    }
                )
            else:
                requirements.append(
                    {
                        "title": _quote(note["text"], 90),
                        "source": note["kind"],
                        "description": note["text"],
                    }
                )
        slices.append({"idea": group["idea"], "stories": stories, "requirements": requirements})
    return {"slices": slices}


def calm_document(epics: list[dict]) -> str:
    nodes = [
        {
            "unique-id": "client",
            "node-type": "webclient",
            "name": "Operator",
            "description": "Person who dropped the raw notes",
        }
    ]
    rels = []
    for index, epic in enumerate(epics, start=1):
        unique = f"epic-{index}"
        nodes.append(
            {
                "unique-id": unique,
                "node-type": "service",
                "name": epic["id"],
                "description": epic["title"][:80],
            }
        )
        rels.append(
            {
                "unique-id": f"rel-{index}",
                "description": "Operator reviews the slice",
                "relationship-type": {"interacts": {"actor": "client", "nodes": [unique]}},
            }
        )
    return json.dumps(
        {"$schema": "https://calm.finos.org/release/1.2/meta/calm.json", "nodes": nodes, "relationships": rels},
        ensure_ascii=False,
        indent=2,
    )


def sysl_document(stories: list[dict]) -> str:
    lines = ["Backlog:"]
    if not stories:
        lines += ["    /empty:", "        GET:", "            return ok <: string"]
        return "\n".join(lines) + "\n"
    for index, story in enumerate(stories, start=1):
        lines += [f"    /story{index}:", "        GET:", "            return ok <: string"]
    return "\n".join(lines) + "\n"


def spec_document(epic_id: str, idea: str, stories: list[dict]) -> str:
    parts = [
        f"# Spec {epic_id}",
        "",
        "## ADDED Requirements",
        "",
        "### Requirement: Source stays visible",
        f"The system MUST show the source of this slice: {idea}",
        "",
        "#### Scenario: card opened",
        "- **WHEN** the operator opens a story card",
        "- **THEN** the card shows the source quote",
        "- GIVEN the note was taken in by intake",
        "",
    ]
    for story in stories:
        parts.append(f"- {story['id']}: {story['title']}")
    return "\n".join(parts) + "\n"
