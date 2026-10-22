"""Spec boundaries. Always proceeds, Ask First stops, Never refuses."""

from __future__ import annotations

LEVELS = ("always", "ask_first", "never")


def normalize(boundaries: dict | None) -> dict[str, list[str]]:
    source = boundaries or {}
    out = {}
    for level in LEVELS:
        values = source.get(level) or []
        if isinstance(values, str):
            values = [values]
        out[level] = [str(item).strip() for item in values if str(item).strip()]
    return out


def boundary_issues(boundaries: dict | None) -> list[str]:
    data = normalize(boundaries)
    if not any(data.values()):
        return ["BOUND-5 boundaries are missing"]
    return []


def decide(action: str, boundaries: dict | None) -> str:
    """Return always, ask_first, never, or unspecified.

    A Never hit wins over Ask First. Ask First wins over Always.
    Matching is a case-insensitive substring either way.
    """
    text = (action or "").strip().lower()
    data = normalize(boundaries)
    if not text:
        return "unspecified"
    for level in ("never", "ask_first", "always"):
        for rule in data[level]:
            rule_l = rule.lower()
            # One-way substring: the rule must appear in the action.
            # Reverse match ("e" inside "commit secrets") fails open and is refused.
            if rule_l and rule_l in text:
                return level
    return "unspecified"


def guard(action: str, boundaries: dict | None) -> str | None:
    """None means proceed. A string is the stop or refuse reason."""
    level = decide(action, boundaries)
    if level == "never":
        return "BOUND-3 refuse: " + action
    if level == "ask_first":
        return "BOUND-2 stop and ask: " + action
    return None


def merge(base: dict | None, extra: dict | None) -> dict[str, list[str]]:
    """Story rules add to the spec. They never delete a Never."""
    left = normalize(base)
    right = normalize(extra)
    return {level: left[level] + [item for item in right[level] if item not in left[level]] for level in LEVELS}
