"""Draw a Sysl file as labeled boxes. The .sysl text remains the source."""

from __future__ import annotations

import html


def apps(text: str) -> list[tuple[str, list[str]]]:
    current = None
    found: list[tuple[str, list[str]]] = []
    endpoints: list[str] = []
    for raw in (text or "").splitlines():
        if not raw.strip() or raw.startswith("#"):
            continue
        if not raw[:1].isspace() and raw.rstrip().endswith(":"):
            if current:
                found.append((current, endpoints))
            current = raw.strip()[:-1]
            endpoints = []
            continue
        stripped = raw.strip()
        if stripped.startswith("/") and current:
            endpoints.append(stripped.rstrip(":"))
    if current:
        found.append((current, endpoints))
    return found


def draw(text: str) -> str:
    blocks = apps(text)
    height = 80 + 36 * sum(max(len(eps), 1) for _, eps in blocks)
    width = 420
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{max(height, 120)}" viewBox="0 0 {width} {max(height, 120)}">',
        '<rect width="100%" height="100%" fill="#f7f1e8"/>',
    ]
    y = 24
    for name, endpoints in blocks:
        rows = endpoints or ["(нет эндпоинта)"]
        box_h = 36 + 22 * len(rows)
        parts.append(f'<rect x="24" y="{y}" width="360" height="{box_h}" rx="14" fill="#fffaf6" stroke="#e4d9cc"/>')
        parts.append(f'<text x="40" y="{y + 22}" font-size="14" fill="#2c2830">{html.escape(name)}</text>')
        for index, endpoint in enumerate(rows):
            parts.append(f'<text x="40" y="{y + 44 + index * 22}" font-size="12" fill="#6f6676">{html.escape(endpoint)}</text>')
        y += box_h + 16
    parts.append("</svg>")
    return "".join(parts)
