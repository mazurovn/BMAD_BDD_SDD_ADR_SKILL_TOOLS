"""Draw a CALM document as SVG. The JSON remains the source. The picture is a view."""

from __future__ import annotations

import html
import json


def draw(text: str) -> str:
    data = json.loads(text or "{}")
    nodes = data.get("nodes") or []
    width = max(240, 180 * max(len(nodes), 1) + 40)
    height = 220
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f7f1e8"/>',
    ]
    positions = {}
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            continue
        unique = str(node.get("unique-id") or f"n{index}")
        x = 30 + index * 180
        y = 40
        positions[unique] = (x, y)
        label = html.escape(str(node.get("name") or unique))
        kind = html.escape(str(node.get("node-type") or ""))
        parts.append(f'<rect x="{x}" y="{y}" width="140" height="64" rx="14" fill="#fffaf6" stroke="#e4d9cc"/>')
        parts.append(f'<text x="{x + 12}" y="{y + 28}" font-size="14" fill="#2c2830">{label}</text>')
        parts.append(f'<text x="{x + 12}" y="{y + 48}" font-size="11" fill="#6f6676">{kind} · {html.escape(unique)}</text>')
    for rel in data.get("relationships") or []:
        if not isinstance(rel, dict):
            continue
        pairs = []
        typed = rel.get("relationship-type")
        if isinstance(typed, dict):
            pairs.extend(typed.items())
        for name, body in rel.items():
            if name in {"unique-id", "description", "relationship-type", "protocol", "metadata", "controls"}:
                continue
            if isinstance(body, dict):
                pairs.append((name, body))
        for name, body in pairs:
            if not isinstance(body, dict):
                continue
            edges = []
            if body.get("source") and body.get("destination"):
                edges.append((body.get("source"), body.get("destination")))
            if body.get("actor") and body.get("nodes"):
                for node in body["nodes"]:
                    edges.append((body.get("actor"), node))
            for left, right in edges:
                source = positions.get(left)
                dest = positions.get(right)
                if not source or not dest:
                    continue
                x1, y1 = source[0] + 140, source[1] + 32
                x2, y2 = dest[0], dest[1] + 32
                parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#b9a99a" stroke-width="2"/>')
                parts.append(f'<text x="{(x1 + x2) / 2}" y="{y1 - 6}" font-size="11" fill="#6f6676">{html.escape(str(name))}</text>')
    parts.append("</svg>")
    return "".join(parts)
