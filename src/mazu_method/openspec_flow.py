"""OpenSpec change flow. Files are the result. A checked task requires evidence."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

_SLUG = re.compile(r"[^a-z0-9-]+")
_TASK = re.compile(r"^- \[( |x)\]\s+(\S+)\s+(.*)$")


def slug(name: str) -> str:
    cleaned = _SLUG.sub("-", (name or "").strip().lower()).strip("-")
    if not cleaned:
        raise ValueError("OPENSPEC-0 change name is empty")
    return cleaned


def change_dir(root: Path, name: str) -> Path:
    return root / "openspec" / "changes" / slug(name)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def propose(root: Path, name: str, intent: str) -> Path:
    intent = (intent or "").strip()
    if len(intent) < 8:
        raise ValueError("OPENSPEC-0 intent is too short")
    path = change_dir(root, name)
    if path.exists():
        raise FileExistsError(f"OPENSPEC-4 change already exists: {path}")
    key = slug(name)
    _write(path / "proposal.md", f"""
# Proposal: {key}

## Why
{intent}

## What Changes
The first slice makes this observable: {intent}

## Impact
Stories that cannot show this outcome stay out of a sprint.
""")
    _write(path / "specs" / key / "spec.md", f"""
# {key} delta spec

## ADDED Requirements

### Requirement: {intent}
The change is done only when the outcome can be observed.

#### Scenario: success
- GIVEN the change {key} is proposed
- WHEN the operator finishes the slice
- THEN {intent}

#### Scenario: refusal
- GIVEN a task has no evidence
- WHEN archive is requested
- THEN the command exits non-zero and the change stays active
""")
    _write(path / "design.md", f"""
## Context
{intent}

## Goals / Non-Goals
Goal: one observable slice. Non-goal: a second product.

## Decisions
Keep the change as files under openspec/changes/{key}/. Do not mark a task done without evidence.

## Risks
A vague Then would pass a human reading and fail the checker. The scenario above names the outcome.
""")
    _write(path / "tasks.md", f"""
## 1. {key}

- [ ] 1.1 Record the outcome: {intent}
- [ ] 1.2 Reject a task that has no evidence
""")
    return path


def validate(path: Path) -> list[str]:
    issues: list[str] = []
    for name in ("proposal.md", "design.md", "tasks.md"):
        file = path / name
        if not file.exists() or len(file.read_text(encoding="utf-8").strip()) < 40:
            issues.append(f"OPENSPEC-1 missing {name}")
    specs = list(path.glob("specs/*/spec.md"))
    if not specs:
        issues.append("OPENSPEC-1 missing specs/*/spec.md")
    else:
        text = specs[0].read_text(encoding="utf-8")
        if "#### Scenario:" not in text or "GIVEN" not in text or "THEN" not in text:
            issues.append("OPENSPEC-2 scenario is missing")
    if not tasks(path):
        issues.append("OPENSPEC-3 no tasks")
    return issues


def tasks(path: Path) -> list[dict]:
    rows = []
    file = path / "tasks.md"
    if not file.exists():
        return rows
    for line in file.read_text(encoding="utf-8").splitlines():
        match = _TASK.match(line.strip())
        if match:
            rows.append({"done": match.group(1) == "x", "id": match.group(2), "title": match.group(3)})
    return rows


def link_task(path: Path, task_id: str, story_id: str) -> None:
    file = path / "tasks.md"
    lines = []
    for line in file.read_text(encoding="utf-8").splitlines():
        match = _TASK.match(line.strip())
        if match and match.group(2) == task_id and f"story:{story_id}" not in line:
            line = f"{line} story:{story_id}"
        lines.append(line)
    file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def complete(path: Path, task_id: str, evidence: str) -> None:
    evidence = (evidence or "").strip()
    if len(evidence) < 3:
        raise ValueError("OPENSPEC-5 evidence is required")
    file = path / "tasks.md"
    found = False
    lines = []
    for line in file.read_text(encoding="utf-8").splitlines():
        match = _TASK.match(line.strip())
        if match and match.group(2) == task_id:
            found = True
            if match.group(1) == "x":
                raise ValueError(f"OPENSPEC-5 task {task_id} is already done")
            line = line.replace("- [ ]", "- [x]", 1)
        lines.append(line)
    if not found:
        raise ValueError(f"OPENSPEC-5 unknown task {task_id}")
    file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    log = path / "evidence.md"
    previous = log.read_text(encoding="utf-8") if log.exists() else "# Evidence\n"
    log.write_text(previous.rstrip() + f"\n- {task_id}: {evidence}\n", encoding="utf-8")


def sync(root: Path, name: str) -> Path:
    path = change_dir(root, name)
    specs = list(path.glob("specs/*/spec.md"))
    if not specs:
        raise FileNotFoundError("OPENSPEC-1 missing specs/*/spec.md")
    target = root / "openspec" / "specs" / specs[0].parent.name / "spec.md"
    _write(target, specs[0].read_text(encoding="utf-8"))
    return target


def archive(root: Path, name: str, today: str) -> Path:
    path = change_dir(root, name)
    issues = validate(path)
    open_tasks = [task["id"] for task in tasks(path) if not task["done"]]
    if issues or open_tasks:
        raise RuntimeError("OPENSPEC-6 not ready: " + ", ".join(issues + open_tasks))
    if not (path / "evidence.md").exists():
        raise RuntimeError("OPENSPEC-6 evidence.md is missing")
    dest = root / "openspec" / "changes" / "archive" / f"{today}-{slug(name)}"
    if dest.exists():
        raise FileExistsError(f"OPENSPEC-4 archive exists: {dest}")
    sync(root, name)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(path), dest)
    return dest


def explore(root: Path, name: str, intent: str) -> Path:
    path = root / "openspec" / "explore" / f"{slug(name)}.md"
    _write(path, f"# Explore {slug(name)}\n\n{intent.strip()}\n\nNo change was created.\n")
    return path


def update(root: Path, name: str, revision: str) -> Path:
    path = change_dir(root, name) / "proposal.md"
    if not path.exists():
        raise FileNotFoundError("OPENSPEC-4 no proposal to update")
    text = path.read_text(encoding="utf-8").rstrip()
    path.write_text(text + f"\n\n## Revision\n{revision.strip()}\n", encoding="utf-8")
    return path
