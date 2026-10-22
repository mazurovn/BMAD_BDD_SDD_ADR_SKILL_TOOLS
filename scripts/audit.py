#!/usr/bin/env python3
"""Cascade check. Walk the kit, then run a throwaway backlog. Exit 1 on any gap."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, str(ROOT / "cli" / "mazu.py")]
REQUIRED = [
    "cli/mazu.py",
    "cli/mazu",
    "methodology/MAZU-ADGILE.md",
    "methodology/MAZU-ADGILE.ru.md",
    "ONBOARDING.md",
    "AGENTS.md",
    "CLAUDE.md",
    "QWEN.md",
    "opencode.json",
    "schemas/store.schema.json",
    "tools/openai.json",
    "tools/gigachat.json",
    "examples/jira.csv",
    "examples/youtrack.csv",
    "diagrams/sysl/backlog.sysl",
    "diagrams/calm/backlog.calm.json",
    "templates/adr.md",
    "templates/spec.md",
    "templates/user-story.md",
    "templates/boundaries.md",
    "configs/gpt/PROMPT.md",
    "configs/codex/PROMPT.md",
    "configs/deepseek/PROMPT.md",
    "configs/kimi/PROMPT.md",
    "configs/gigachat/PROMPT.md",
    "configs/gigacode/PROMPT.md",
    "configs/grok/prompt.md",
    "configs/grok-bot/PROMPT.md",
    ".opencode/agent/mazu.md",
    "wiki/Manual.md",
    "src/mazu_method/bmad.py",
    "src/mazu_method/sdd.py",
    "src/mazu_method/bdd.py",
    "src/mazu_method/adr.py",
    "src/mazu_method/agile.py",
    "src/mazu_method/estimation.py",
    "src/mazu_method/workflows.py",
    "src/mazu_method/sysl_check.py",
    "src/mazu_method/calm_check.py",
]
SKILLS = [
    "bmad", "sdd", "bdd", "adr", "agile-delivery", "product-ideas",
    "requirements", "sysl", "calm", "skill-creator", "backlog-connectors",
    "tool-calling", "projects", "create-epics-and-stories", "sprint-planning",
    "lazy-senior", "architecture", "estimation",
]
ROLES = [
    "analyst.md", "po.md", "bmad-lead.md", "architect.md",
    "business-architect.md", "enterprise-architect.md", "solution-architect.md",
    "adr-keeper.md", "sdd-author.md", "bdd-author.md", "sysl-modeler.md",
    "calm-modeler.md", "scrum-master.md", "dev.md", "lazy-senior.md", "qa.md",
    "integrator.md", "skill-creator.md", "researcher.md", "writer.md", "release.md",
]
HELP_WORDS = ["project", "import", "export", "pull", "connectors", "skill", "dashboard", "serve", "check", "workflow", "gate"]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)
    print(f"GAP {message}")


def main() -> int:
    errors: list[str] = []
    print("1. files")
    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            fail(errors, f"missing {rel}")
    print("2. skills")
    for name in SKILLS:
        path = ROOT / "skills" / name / "SKILL.md"
        if not path.exists():
            fail(errors, f"missing skill {name}")
            continue
        text = path.read_text(encoding="utf-8")
        if "name:" not in text or "description:" not in text:
            fail(errors, f"skill {name} has no frontmatter")
    print("2b. wiki has no external urls")
    for page in (ROOT / "wiki").glob("*.md"):
        text = page.read_text(encoding="utf-8")
        if "http://" in text or "https://" in text:
            fail(errors, f"external url in {page.name}")
    print("3. roles")
    for name in ROLES:
        if not (ROOT / "agents" / name).exists():
            fail(errors, f"missing role {name}")
    catalog = json.loads((ROOT / "agents" / "catalog.json").read_text(encoding="utf-8"))
    if len(catalog.get("subagents", [])) < len(ROLES):
        fail(errors, "catalog has fewer subagents than role files")
    print("4. tool schemas")
    for rel in ("tools/openai.json", "tools/gigachat.json", "opencode.json", "diagrams/calm/backlog.calm.json"):
        try:
            json.loads((ROOT / rel).read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(errors, f"bad json {rel}: {exc}")
    print("5. cli help")
    help_text = subprocess.check_output(CLI + ["--help"], text=True)
    for word in HELP_WORDS:
        if word not in help_text:
            fail(errors, f"help missing {word}")
    print("6. throwaway backlog")
    with tempfile.TemporaryDirectory() as tmp:
        env = os.environ.copy()
        for key in ("JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_TOKEN", "YOUTRACK_URL", "YOUTRACK_TOKEN"):
            env.pop(key, None)

        def run(*args: str) -> subprocess.CompletedProcess[str]:
            return subprocess.run(CLI + list(args), cwd=tmp, env=env, text=True, capture_output=True)

        steps = [
            ["init"],
            ["project", "new", "audit-demo"],
            ["import", "jira-csv", str(ROOT / "examples" / "jira.csv")],
            ["import", "youtrack-csv", str(ROOT / "examples" / "youtrack.csv")],
            ["export", "xlsx", "out.xlsx"],
            ["import", "xlsx", "out.xlsx"],
            ["dashboard"],
            ["connectors"],
        ]
        for step in steps:
            result = run(*step)
            if result.returncode != 0:
                fail(errors, f"{' '.join(step)} -> {result.returncode} {result.stderr}")
        store = json.loads(Path(tmp, "mazu-data/projects/audit-demo/store.json").read_text(encoding="utf-8"))
        keys = {item.get("external_id") for item in store["items"]}
        if "ABC-2" not in keys or "YT-2" not in keys:
            fail(errors, f"external ids missing: {keys}")
        bug = next(item for item in store["items"] if item.get("external_id") == "ABC-3")
        if bug.get("points") is not None:
            fail(errors, "non-fibonacci points were kept")
        pull = run("pull", "jira")
        if pull.returncode == 0:
            fail(errors, "pull jira succeeded without tokens")
        if "not connected" not in (pull.stderr + pull.stdout):
            fail(errors, "pull jira did not say not connected")
        skill = run("skill", "new", "audit-temp", "--description", "temporary")
        if skill.returncode != 0:
            fail(errors, skill.stderr)
        created = ROOT / "skills" / "audit-temp"
        if created.exists():
            for child in created.glob("*"):
                child.unlink()
            created.rmdir()
        else:
            fail(errors, "skill new did not write a skeleton")
    print("7. result")
    if errors:
        print(f"FAIL {len(errors)}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
