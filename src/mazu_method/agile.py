"""Backlog rules: ready, done, split, and the unfinished-work limit."""

from __future__ import annotations

from mazu_method.bdd import acceptance_issues
from mazu_method.estimation import hours_total, points_issue
from mazu_method.sdd import boundary_issues

WIP_LIMIT = 2


def ready_issues(item: dict) -> list[str]:
    if item.get("kind") != "story":
        return ["ready gate applies to a story"]
    issues: list[str] = []
    if not item.get("parent"):
        issues.append("EPIC-2 parent is missing")
    point_issue = points_issue(item.get("points"))
    if point_issue:
        issues.append(point_issue)
    issues.extend(acceptance_issues(item.get("acceptance") or []))
    issues.extend(boundary_issues(item.get("boundaries")))
    return issues


def evidence_verified(entry: dict | str) -> bool:
    """Natural-language claims are not proof. Only command-verified evidence counts."""
    if not isinstance(entry, dict):
        return False
    if entry.get("verified") is True and int(entry.get("exit", 1)) == 0:
        return True
    return False


def done_issues(item: dict) -> list[str]:
    issues = ready_issues(item)
    acceptance = [line for line in item.get("acceptance") or [] if str(line).strip()]
    evidence = item.get("evidence") or []
    if not evidence:
        issues.append("BDD-4 no evidence")
    elif len(evidence) < len(acceptance):
        issues.append("BDD-4 fewer evidence notes than acceptance lines")
    else:
        unverified = [i for i, row in enumerate(evidence, 1) if not evidence_verified(row)]
        if unverified:
            issues.append(
                "BDD-4 evidence is not command-verified (use: evidence ID --run COMMAND); "
                f"bad lines {unverified}"
            )
    return issues


def wip_issues(items: list[dict]) -> list[str]:
    active = [item for item in items if item.get("kind") == "story" and item.get("status") == "in-progress"]
    if len(active) > WIP_LIMIT:
        return [f"AGILE-6 {len(active)} stories in progress, limit {WIP_LIMIT}"]
    return []


def velocity(items: list[dict], sprint_id: str) -> int:
    total = 0
    for item in items:
        if item.get("kind") == "story" and item.get("sprint") == sprint_id and item.get("status") == "done":
            total += int(item.get("points") or 0)
    return total


def hours_for(logs: list[dict], item_id: str) -> float:
    return hours_total(logs, item_id)
