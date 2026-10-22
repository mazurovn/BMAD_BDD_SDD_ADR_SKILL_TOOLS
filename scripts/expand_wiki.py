#!/usr/bin/env python3
"""Fill the thin wiki pages from the operating procedures, without external URLs."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def body(skill: str) -> str:
    text = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
    return "\n".join(text.splitlines()[5:]).strip()


def write(name: str, intro: str, skills: list[str]) -> None:
    parts = [f"# {name}", "", intro, ""]
    for skill in skills:
        parts.append(body(skill))
        parts.append("")
    path = ROOT / "wiki" / f"{name}.md"
    path.write_text("\n".join(parts).strip() + "\n", encoding="utf-8")
    print(name, len(path.read_text(encoding="utf-8").splitlines()))


def main() -> None:
    write("BDD", "Страница самодостаточна. Код проверки — src/mazu_method/bdd.py. Команда `python3 cli/mazu.py check bdd ID`.", ["bdd"])
    write("ADR", "Страница самодостаточна. Код — src/mazu_method/adr.py. Пустой Decision не проходит проверку.", ["adr"])
    write("Agile", "Страница самодостаточна. Код — src/mazu_method/agile.py. Scrum и Kanban используют одни колонки.", ["agile-delivery"])
    write("SDD-boundaries", "Страница самодостаточна. Always проходит, Ask First останавливает, Never отказывает. Код — src/mazu_method/sdd.py.", ["sdd"])
    write("Estimation", "Страница самодостаточна. Points и часы — разные поля. Код — src/mazu_method/estimation.py.", ["estimation"])
    write("Sysl", "Страница самодостаточна. Примеры diagrams/sysl/example.sysl и diagrams/sysl/backlog.sysl уже проходят check.", ["sysl"])
    write("CALM", "Страница самодостаточна. Примеры diagrams/calm/example.calm.json и diagrams/calm/backlog.calm.json уже проходят check.", ["calm"])
    write("Projects", "Страница самодостаточна. Данные проекта живут в mazu-data и не коммитятся.", ["projects"])
    write("Workflows", "Два именованных потока BMAD v6. Код обоих — src/mazu_method/workflows.py. Фазы вокруг них описаны следом.", ["create-epics-and-stories", "sprint-planning", "bmad"])
    write("BMAD-v6", "Фазы и нарезка. Пропуск фазы без факта — ошибка check phase.", ["bmad", "create-epics-and-stories", "sprint-planning"])
    harness = """# Harnesses

Агент читает эту страницу, затем скилл целиком, затем выполняет CLI. Второй бэклог в переписке не ведут.

Какой файл открыть:

| Вопрос | Скилл | Код |
|---|---|---|
| Какая фаза | skills/bmad/SKILL.md | src/mazu_method/bmad.py |
| Нарезка | skills/create-epics-and-stories/SKILL.md | src/mazu_method/workflows.py |
| Спринт | skills/sprint-planning/SKILL.md | src/mazu_method/workflows.py |
| Границы | skills/sdd/SKILL.md | src/mazu_method/sdd.py |
| Сценарии | skills/bdd/SKILL.md | src/mazu_method/bdd.py |
| Решение | skills/adr/SKILL.md | src/mazu_method/adr.py |
| Доска | skills/agile-delivery/SKILL.md | src/mazu_method/agile.py |
| Points и часы | skills/estimation/SKILL.md | src/mazu_method/estimation.py |
| Поведение | skills/sysl/SKILL.md | src/mazu_method/sysl_check.py |
| Состав | skills/calm/SKILL.md | src/mazu_method/calm_check.py |
| Три слоя | skills/architecture/SKILL.md | председательство, без своего хранилища |
| Импорт | skills/backlog-connectors/SKILL.md | cli/mazu.py |
| Вызов функций | skills/tool-calling/SKILL.md | tools/openai.json и tools/gigachat.json |

Файлы старта harness лежат в репозитории: AGENTS.md, CLAUDE.md, QWEN.md, opencode.json, configs/. В каждый вставлен один и тот же блок standards/PROMPT_BLOCK.md. Блок приказывает читать скилл целиком и не объявлять PASS без stdout.

Проверка набора: `python3 cli/mazu.py doctor`, затем `python3 scripts/audit.py`, затем `python3 -m pytest -q tests`.

"""
    (ROOT / "wiki" / "Harnesses.md").write_text(harness + "\n" + body("tool-calling") + "\n", encoding="utf-8")
    print("Harnesses", len((ROOT / "wiki" / "Harnesses.md").read_text().splitlines()))


if __name__ == "__main__":
    main()
