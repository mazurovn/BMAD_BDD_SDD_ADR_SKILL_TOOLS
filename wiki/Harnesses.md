# Как агенту стартовать

Агент читает эту вики, затем скилл под задачу, затем выполняет CLI. Второй бэклог в переписке не ведут.

Какой скилл открыть:

| Задача | Скилл |
|---|---|
| Фазы | skills/bmad |
| Нарезка эпиков и историй | skills/create-epics-and-stories |
| Спринт или канбан | skills/sprint-planning |
| Спека и границы | skills/sdd |
| Сценарии | skills/bdd |
| Решение | skills/adr |
| Доска, points, часы, дробление | skills/agile-delivery |
| Идея и эпик | skills/product-ideas |
| Формулировка требования | skills/requirements |
| Поведение | skills/sysl |
| Состав | skills/calm |
| Несколько проектов | skills/projects |
| Jira, YouTrack, CSV, Excel | skills/backlog-connectors |
| Вызов функций | skills/tool-calling |
| Новый скилл | skills/skill-creator |

Файлы старта в репозитории, без внешней документации: `AGENTS.md`, `CLAUDE.md`, `QWEN.md`, `opencode.json`, `.opencode/agent/mazu.md`, каталог `configs/` для GPT, Codex, DeepSeek, Kimi, GigaChat, GigaCode, Grok и Grok-бота.

Схемы вызова, которые агент отдаёт модели, а не придумывает: `tools/openai.json` и `tools/gigachat.json`. Имя функции из схемы исполняют через CLI. Пока stdout не получен, агент не отвечает так, будто команда уже прошла.

Для GigaChat после `finish_reason` равного `function_call` ответ функции возвращают отдельным сообщением роли function.

Проверка, что метод ещё целый: `python3 scripts/audit.py`. Ненулевой код означает, что работать «как будто всё на месте» нельзя.
