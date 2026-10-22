"""Phase order. A later phase does not erase an earlier missing fact."""

from __future__ import annotations

PHASES = ("analysis", "planning", "solutioning", "implementation")


def phase_index(name: str) -> int:
    if name not in PHASES:
        raise ValueError(f"unknown phase {name}")
    return PHASES.index(name)


def phase_issues(current: str, facts: dict) -> list[str]:
    """facts: outcome (str), boundaries (bool), check (bool)."""
    issues = []
    if current not in PHASES:
        return [f"BMAD-1 unknown phase {current}"]
    if phase_index(current) >= phase_index("planning") and not (facts.get("outcome") or "").strip():
        issues.append("BMAD-1 outcome is missing")
    if phase_index(current) >= phase_index("solutioning") and not facts.get("boundaries"):
        issues.append("BMAD-1 boundaries are missing")
    if phase_index(current) >= phase_index("implementation") and not facts.get("check"):
        issues.append("BMAD-1 the check is missing")
    return issues
