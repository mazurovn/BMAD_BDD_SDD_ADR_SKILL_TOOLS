"""Minimal CALM check: nodes, stable ids, and relationships that point at those ids."""

from __future__ import annotations

import json
import re

_SECRET = re.compile(r"(password|secret|api[_-]?key|AKIA[0-9A-Z]{8})", re.IGNORECASE)


def issues(text: str) -> list[str]:
    try:
        data = json.loads(text or "")
    except json.JSONDecodeError as exc:
        return [f"CALM-3 not json: {exc.msg}"]
    if not isinstance(data, dict):
        return ["CALM-3 document is not an object"]
    found: list[str] = []
    blob = json.dumps(data)
    if _SECRET.search(blob):
        found.append("CALM-4 secret-like text")
    nodes = data.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        return found + ["CALM-2 nodes are missing"]
    ids: list[str] = []
    for node in nodes:
        if not isinstance(node, dict):
            found.append("CALM-2 node is not an object")
            continue
        unique = str(node.get("unique-id") or "").strip()
        if not unique:
            found.append("CALM-2 node has no unique-id")
        elif unique in ids:
            found.append(f"CALM-2 duplicate unique-id {unique}")
        else:
            ids.append(unique)
        if not str(node.get("node-type") or "").strip():
            found.append(f"CALM-2 {unique or '?'} has no node-type")
    relationships = data.get("relationships") or []
    if not isinstance(relationships, list):
        found.append("CALM-3 relationships is not a list")
        return found
    known = set(ids)
    for rel in relationships:
        if not isinstance(rel, dict) or not rel:
            found.append("CALM-3 empty relationship")
            continue
        ends = []
        typed = rel.get("relationship-type")
        bodies = []
        if isinstance(typed, dict):
            bodies.extend(typed.items())
        for name, body in rel.items():
            if name in {"unique-id", "description", "relationship-type", "protocol", "metadata", "controls"}:
                continue
            bodies.append((name, body))
        if not bodies:
            found.append("CALM-3 empty relationship")
            continue
        for name, body in bodies:
            if name not in ("interacts", "connects"):
                found.append(f"CALM-3 unknown relationship {name}")
                continue
            if not isinstance(body, dict):
                found.append(f"CALM-3 {name} is not an object")
                continue
            if "actor" in body or "nodes" in body:
                ends.append(body.get("actor"))
                ends.extend(body.get("nodes") or [])
            else:
                ends.extend(body.get(end) for end in ("source", "destination"))
        for ref in ends:
            if isinstance(ref, dict):
                ref = ref.get("unique-id") or ref.get("node")
            if ref not in known:
                found.append(f"CALM-3 end {ref} is not a node")
    return found
