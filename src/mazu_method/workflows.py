"""BMAD v6 local workflows: create-epics-and-stories and sprint-planning."""

from __future__ import annotations

from mazu_method.agile import ready_issues


def epic_tree_issues(idea: dict | None, epic: dict | None, stories: list[dict]) -> list[str]:
    issues: list[str] = []
    if idea is None or not (idea.get("title") or "").strip():
        issues.append("EPIC-1 idea is missing")
    elif idea.get("kind") != "idea":
        issues.append("EPIC-1 parent of the epic must be an idea")
    if epic is None or not (epic.get("title") or "").strip():
        issues.append("EPIC-1 epic is missing")
    elif epic.get("kind") != "epic":
        issues.append("EPIC-1 epic has the wrong kind")
    elif idea and epic.get("parent") != idea.get("id"):
        issues.append("EPIC-1 epic is not attached to the idea")
    if not stories:
        issues.append("EPIC-2 epic has no stories")
    for story in stories:
        if story.get("kind") != "story":
            issues.append(f"EPIC-2 {story.get('id')} is not a story")
            continue
        if epic and story.get("parent") != epic.get("id"):
            issues.append(f"EPIC-2 {story.get('id')} parent is not the epic")
        for issue in ready_issues(story):
            issues.append(f"{story.get('id')} {issue}")
    return issues


def sprint_plan_issues(goal: str, stories: list[dict]) -> list[str]:
    issues: list[str] = []
    if not (goal or "").strip():
        issues.append("SPRINT-1 goal is empty")
    if not stories:
        issues.append("SPRINT-1 sprint has no stories")
    for story in stories:
        for issue in ready_issues(story):
            issues.append(f"{story.get('id')} {issue}")
    return issues
