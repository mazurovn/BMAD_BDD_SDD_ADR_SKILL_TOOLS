"""Story points are complexity. Hours are time already spent. They are not convertible."""

from __future__ import annotations

FIBONACCI = (1, 2, 3, 5, 8, 13, 21)
READY_MAX = 8


def classify_points(points) -> str:
    if points is None or points == "":
        return "missing"
    try:
        value = int(points)
    except (TypeError, ValueError):
        return "invalid"
    if value not in FIBONACCI:
        return "invalid"
    if value >= 13:
        return "split"
    return "ok"


def points_issue(points) -> str | None:
    kind = classify_points(points)
    if kind == "missing":
        return "EST-2 points are missing"
    if kind == "invalid":
        return "EST-2 points must be 1, 2, 3, 5, 8, 13, or 21"
    if kind == "split":
        return "EPIC-2 points are too large to be ready"
    return None


def hours_total(logs: list[dict], item_id: str) -> float:
    total = 0.0
    for entry in logs:
        if entry.get("item") == item_id:
            total += float(entry.get("hours") or 0)
    return round(total, 2)


def reject_hours_as_points(points, hours) -> str | None:
    """A number in both fields is allowed. Treating one as the other is not."""
    if points is None or hours in (None, "", 0):
        return None
    try:
        if float(points) == float(hours):
            return "EST-1 do not copy hours into points or points into hours"
    except (TypeError, ValueError):
        return None
    return None
