"""Given / When / Then checks. A scenario that cannot fail is not acceptance."""

from __future__ import annotations

import re

_LINE = re.compile(r"^\s*(given|when|then)\b\s*(.*)$", re.IGNORECASE)
_VAGUE = re.compile(
    r"\b(works well|good enough|ok|fine|tbd|todo|работает хорошо|норм|ок)\b",
    re.IGNORECASE,
)


def split_scenarios(text: str) -> list[str]:
    return [part.strip() for part in (text or "").split("|") if part.strip()]


def parse_scenario(text: str) -> dict[str, str]:
    inline = re.search(
        r"given\s+(.*?)\s+when\s+(.*?)\s+then\s+(.*)",
        text or "",
        re.IGNORECASE | re.DOTALL,
    )
    if inline:
        return {
            "given": inline.group(1).strip(),
            "when": inline.group(2).strip(),
            "then": inline.group(3).strip(),
        }
    found = {"given": "", "when": "", "then": ""}
    for raw in (text or "").splitlines():
        match = _LINE.match(raw.strip())
        if match:
            found[match.group(1).lower()] = match.group(2).strip()
    return found


def scenario_issues(text: str) -> list[str]:
    parsed = parse_scenario(text)
    issues = []
    if not parsed["given"]:
        issues.append("BDD-1 Given is missing")
    if not parsed["when"]:
        issues.append("BDD-1 When is missing")
    if not parsed["then"]:
        issues.append("BDD-1 Then is missing")
    elif _VAGUE.search(parsed["then"]):
        issues.append("BDD-1 Then is not observable")
    return issues


def acceptance_issues(lines: list[str]) -> list[str]:
    if not lines:
        return ["BDD-2 acceptance is missing"]
    issues: list[str] = []
    for index, line in enumerate(lines, start=1):
        for issue in scenario_issues(line):
            issues.append(f"{issue} (scenario {index})")
    return issues
