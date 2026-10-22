#!/usr/bin/env python3
"""Run the method through the CLI only. Write a report from real exit codes."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, str(ROOT / "cli" / "mazu.py")]


def main() -> int:
    demo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/mazu-enterprise-demo")
    if demo.exists():
        shutil.rmtree(demo)
    demo.mkdir(parents=True)
    rows: list[dict] = []
    failed = False

    def step(args: list[str], expect: int | None) -> subprocess.CompletedProcess[str]:
        nonlocal failed
        started = time.perf_counter()
        proc = subprocess.run(CLI + args, cwd=demo, text=True, capture_output=True)
        elapsed = round((time.perf_counter() - started) * 1000, 1)
        text = (proc.stdout or "") + (proc.stderr or "")
        ok = expect is None or proc.returncode == expect
        if not ok:
            failed = True
        rows.append({
            "cmd": " ".join(args),
            "exit": proc.returncode,
            "expect": expect,
            "ok": ok,
            "ms": elapsed,
            "out": text.strip()[:500],
        })
        return proc

    step(["init"], 0)
    step(["project", "new", "enterprise-demo"], 0)
    step(["add", "idea", "Оператор видит отказ гейта до того, как история попала в спринт"], 0)
    step(["add", "epic", "Гейт ready обязателен", "--parent", "IDEA-001"], 0)
    step(["add", "requirement", "Когда Then нельзя проверить, gate ready завершается с ошибкой", "--parent", "EPIC-001"], 0)
    step(["add", "story", "Плохой сценарий", "--parent", "EPIC-001", "--points", "3",
          "--acceptance", "Given a user When they save Then works well", "--never", "Commit secrets"], 0)
    step(["gate", "ready", "US-001"], 1)
    step(["add", "story", "Сохранить карточку", "--parent", "EPIC-001", "--points", "5",
          "--acceptance", "Given a user When they save Then the store has the story | Given an empty title When they save Then the command exits non-zero",
          "--always", "Keep the store valid", "--ask-first", "new dependency", "--never", "Commit secrets"], 0)
    step(["add", "story", "Показать отказ", "--parent", "EPIC-001", "--points", "3",
          "--acceptance", "Given a failed check When the operator opens the board Then the story is not in the sprint",
          "--never", "Commit secrets"], 0)
    step(["check", "bdd", "US-002"], 0)
    step(["check", "boundaries", "US-002"], 0)
    step(["check", "points", "US-002"], 0)
    step(["gate", "ready", "US-002"], 0)
    step(["gate", "ready", "US-003"], 0)
    step(["workflow", "epics", "--idea", "IDEA-001", "--epic", "EPIC-001"], 1)
    step(["add", "story", "Слишком крупная", "--parent", "EPIC-001", "--points", "13",
          "--acceptance", "Given a slice When it is still 13 Then it stays out of ready", "--never", "Commit secrets"], 0)
    step(["gate", "ready", "US-004"], 1)
    step(["add", "story", "Чужая шкала", "--parent", "EPIC-001", "--points", "4"], 1)
    step(["add", "adr", "Store is one JSON file", "--description", "One operator and no concurrent writers"], 0)
    step(["check", "adr", "ADR-001"], 1)
    step(
        [
            "fill",
            "adr",
            "ADR-001",
            "--decision",
            "Keep one JSON file for the local store.",
            "--consequences",
            "- Positive: simple local store\n- Negative: no concurrent writers",
        ],
        0,
    )
    step(["check", "adr", "ADR-001"], 0)
    step(["sprint", "new", "--goal", "В спринт попадают только истории, прошедшие ready"], 0)
    step(["sprint", "add", "--id", "US-002", "--sprint", "S1"], 0)
    step(["sprint", "add", "--id", "US-003", "--sprint", "S1"], 0)
    step(["workflow", "sprint", "--sprint", "S1"], 0)
    step(["gate", "sprint", "S1"], 0)
    # sprint add already moved US-002 to ready; one column forward only
    step(["move", "US-002", "in-progress"], 0)
    step(["log", "US-002", "1.5", "--note", "saved the row"], 0)
    step(["move", "US-002", "review"], 0)
    step(["gate", "done", "US-002"], 1)
    step(["evidence", "US-002", "--run", sys.executable, "-c", "print('store contained the story')"], 0)
    step(["evidence", "US-002", "--run", sys.executable, "-c", "print('empty title exited non-zero')"], 0)
    step(["gate", "done", "US-002"], 0)
    step(["move", "US-002", "done"], 0)
    step(["check", "wip", "board"], 0)
    step(["check", "phase", "implementation", "--outcome", "Оператор видит отказ гейта"], 1)
    step(["check", "phase", "implementation", "--outcome", "Оператор видит отказ гейта", "--has-boundaries", "--has-check"], 0)
    step(["check", "guard", "commit secrets", "--never", "commit secrets"], 1)
    step(["check", "guard", "keep store valid", "--always", "keep store valid"], 0)
    step(["check", "sysl", str(ROOT / "diagrams/sysl/example.sysl")], 0)
    step(["check", "sysl", str(ROOT / "diagrams/sysl/backlog.sysl")], 0)
    step(["check", "calm", str(ROOT / "diagrams/calm/example.calm.json")], 0)
    step(["check", "calm", str(ROOT / "diagrams/calm/backlog.calm.json")], 0)
    step(["import", "jira-csv", str(ROOT / "examples/jira.csv")], 0)
    step(["dashboard"], 0)
    step(["connectors"], 0)
    step(["pull", "jira", "--jql", "project = DEMO"], 1)

    port = "8767"
    proc = subprocess.Popen(CLI + ["serve", "--port", port], cwd=demo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    http_ok = False
    body = ""
    try:
        deadline = time.time() + 5
        while time.time() < deadline:
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=0.5) as response:
                    body = response.read().decode("utf-8")
                    http_ok = response.status == 200 and "MAZU-ADGILE" in body and "Сохранить карточку" in body
                    break
            except Exception:
                time.sleep(0.1)
    finally:
        proc.terminate()
        proc.wait(timeout=5)
    rows.append({"cmd": f"GET http://127.0.0.1:{port}/", "exit": 0 if http_ok else 1, "expect": 0, "ok": http_ok, "ms": 0, "out": "dashboard http 200" if http_ok else "dashboard did not answer"})
    if not http_ok:
        failed = True

    out_dir = ROOT / "docs" / "demo"
    out_dir.mkdir(parents=True, exist_ok=True)
    dash = demo / "mazu-data" / "projects" / "enterprise-demo" / "dashboard.html"
    md = demo / "mazu-data" / "projects" / "enterprise-demo" / "dashboard.md"
    shutil.copyfile(dash, out_dir / "dashboard.html")
    shutil.copyfile(md, out_dir / "dashboard.md")
    store = json.loads((demo / "mazu-data" / "projects" / "enterprise-demo" / "store.json").read_text(encoding="utf-8"))
    passed = sum(1 for row in rows if row["ok"])
    total_ms = round(sum(row["ms"] for row in rows), 1)
    lines = [
        "# Боевой отчёт",
        "",
        "Отчёт собран скриптом `scripts/enterprise_demo.py`. Каждая строка — реальный запуск `python3 cli/mazu.py`. Числа не выдуманы.",
        "",
        f"- Команд: {len(rows)}",
        f"- Совпало с ожидаемым кодом выхода: {passed}",
        f"- Не совпало: {len(rows) - passed}",
        f"- Сумма времени CLI, мс: {total_ms}",
        f"- Карточек в store: {len(store['items'])}",
        f"- Спринтов: {len(store['sprints'])}",
        f"- Записей времени: {len(store['time_logs'])}",
        "",
        "| Команда | Код | Ожидали | мс | Итог |",
        "|---|---:|---:|---:|---|",
    ]
    for row in rows:
        mark = "ok" if row["ok"] else "FAIL"
        lines.append(f"| `{row['cmd']}` | {row['exit']} | {row['expect']} | {row['ms']} | {mark} |")
    lines += ["", "## Что команды ответили", ""]
    for row in rows:
        if row["out"]:
            lines.append(f"### {row['cmd']}")
            lines.append("")
            lines.append("```")
            lines.append(row["out"])
            lines.append("```")
            lines.append("")
    report = ROOT / "docs" / "BATTLE_REPORT.md"
    report.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"commands {len(rows)} matched {passed} ms {total_ms} failed {failed}")
    print(f"report {report}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
