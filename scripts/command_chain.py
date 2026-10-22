#!/usr/bin/env python3
"""Chat command -> CLI -> framework function -> artifact. Exit 1 on a mismatch."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, str(ROOT / "cli" / "mazu.py")]


def main() -> int:
    demo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/mazu-command-chain")
    if demo.exists():
        shutil.rmtree(demo)
    demo.mkdir()
    rows: list[dict] = []
    failed = False

    def step(chat: str, args: list[str], expect: int, function: str, proof: str) -> str:
        nonlocal failed
        proc = subprocess.run(CLI + args, cwd=demo, text=True, capture_output=True)
        text = (proc.stdout or "") + (proc.stderr or "")
        ok = proc.returncode == expect and proof in text
        if not ok:
            failed = True
        rows.append({
            "chat": chat,
            "cli": " ".join(args),
            "function": function,
            "exit": proc.returncode,
            "expect": expect,
            "ok": ok,
            "out": text.strip()[:400],
        })
        return text

    intent = "Оператор видит отказ гейта"
    step("/opsx:explore gate-visible", ["chat", f"/opsx:explore gate-visible {intent}"], 0, "openspec_flow.explore", "openspec/explore")
    step("/opsx:propose gate-visible", ["chat", f"/opsx:propose gate-visible {intent}"], 0, "openspec_flow.propose", "PASS propose")
    step("validate", ["openspec", "validate", "gate-visible"], 0, "openspec_flow.validate", "PASS validate")
    step("propose again", ["openspec", "propose", "gate-visible", "--intent", intent], 1, "openspec_flow.propose", "OPENSPEC-4")
    step("/opsx:apply", ["chat", "/opsx:apply gate-visible"], 0, "openspec_flow.link_task", "PASS apply")
    tasks = (demo / "openspec/changes/gate-visible/tasks.md").read_text(encoding="utf-8")
    if "- [ ]" not in tasks or "story:US-" not in tasks:
        failed = True
        rows.append({"chat": "tasks still open", "cli": "read tasks.md", "function": "openspec_flow.tasks", "exit": 1, "expect": 0, "ok": False, "out": tasks[:300]})
    else:
        rows.append({"chat": "tasks still open", "cli": "read tasks.md", "function": "openspec_flow.tasks", "exit": 0, "expect": 0, "ok": True, "out": "boxes open and story ids linked"})
    step("complete without evidence", ["openspec", "complete", "gate-visible", "--task", "1.1", "--evidence", ""], 1, "openspec_flow.complete", "OPENSPEC-5")
    step("complete 1.1", ["openspec", "complete", "gate-visible", "--task", "1.1", "--evidence", "отказ напечатан"], 0, "openspec_flow.complete", "PASS complete")
    step("archive too early", ["openspec", "archive", "gate-visible"], 1, "openspec_flow.archive", "OPENSPEC-6")
    step("complete 1.2", ["openspec", "complete", "gate-visible", "--task", "1.2", "--evidence", "пустая улика отклонена"], 0, "openspec_flow.complete", "PASS complete")
    step("/opsx:archive", ["chat", "/opsx:archive gate-visible"], 0, "openspec_flow.archive", "PASS archive")
    spec = demo / "openspec/specs/gate-visible/spec.md"
    archived = list((demo / "openspec/changes/archive").glob("*-gate-visible"))
    if not spec.exists() or not archived or (demo / "openspec/changes/gate-visible").exists():
        failed = True
        rows.append({"chat": "archive files", "cli": "filesystem", "function": "openspec_flow.archive", "exit": 1, "expect": 0, "ok": False, "out": "missing spec or archive"})
    else:
        rows.append({"chat": "archive files", "cli": "filesystem", "function": "openspec_flow.archive", "exit": 0, "expect": 0, "ok": True, "out": str(archived[0])})

    step("bdd pass", ["check", "bdd", "US-001"], 0, "bdd.acceptance_issues", "PASS")
    step("add vague story", ["add", "story", "Плохо", "--points", "3", "--acceptance", "Given a When b Then works well", "--never", "Commit secrets"], 0, "bdd.acceptance_issues", "US-")
    vague = step("bdd fail", ["check", "bdd", "US-003"], 1, "bdd.acceptance_issues", "not observable")
    if "US-" not in vague and "not observable" not in vague:
        pass
    step("sdd refuse", ["check", "guard", "commit secrets", "--never", "commit secrets"], 1, "sdd.guard", "BOUND-3")
    step("bmad block", ["check", "phase", "implementation"], 1, "bmad.phase_issues", "BMAD-1")
    step("bmad pass", ["check", "phase", "implementation", "--outcome", intent, "--has-boundaries", "--has-check"], 0, "bmad.phase_issues", "PASS")
    step("adr create", ["add", "adr", "One JSON file", "--description", "One writer"], 0, "adr.write", "ADR-")
    step("adr empty", ["check", "adr", "ADR-001"], 1, "adr.issues", "ADR-2")
    adr = demo / "mazu-data/adr/ADR-001.md"
    adr.write_text(adr.read_text(encoding="utf-8").replace("## Decision\n_fill in_", "## Decision\nKeep one JSON file."), encoding="utf-8")
    step("adr filled", ["check", "adr", "ADR-001"], 0, "adr.issues", "PASS")
    step("sysl", ["check", "sysl", str(ROOT / "diagrams/sysl/backlog.sysl")], 0, "sysl_check.issues", "PASS")
    step("calm", ["check", "calm", str(ROOT / "diagrams/calm/backlog.calm.json")], 0, "calm_check.issues", "PASS")
    step("sysl svg", ["diagram", "sysl", str(ROOT / "diagrams/sysl/backlog.sysl"), "-o", str(demo / "sysl.svg")], 0, "sysl_draw.draw", "sysl.svg")
    step("calm svg", ["diagram", "calm", str(ROOT / "diagrams/calm/backlog.calm.json"), "-o", str(demo / "calm.svg")], 0, "calm_draw.draw", "calm.svg")

    passed = sum(1 for row in rows if row["ok"])
    lines = [
        "# Цепочка команд",
        "",
        "Каждая строка — запуск `python3 cli/mazu.py`. Чат `/opsx:*` идёт через `chat`, тот вызывает ту же функцию, что и прямая команда.",
        "",
        f"- Шагов: {len(rows)}",
        f"- Совпало: {passed}",
        f"- Не совпало: {len(rows) - passed}",
        "",
        "| Чат | CLI | Функция | Код | Ожидали | Итог |",
        "|---|---|---|---:|---:|---|",
    ]
    for row in rows:
        lines.append(f"| `{row['chat']}` | `{row['cli']}` | `{row['function']}` | {row['exit']} | {row['expect']} | {'ok' if row['ok'] else 'FAIL'} |")
    lines += ["", "## Ответы", ""]
    for row in rows:
        lines += [f"### {row['chat']}", "", "```", row["out"], "```", ""]
    report = ROOT / "docs" / "COMMAND_CHAIN.md"
    report.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"steps {len(rows)} matched {passed} failed {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
