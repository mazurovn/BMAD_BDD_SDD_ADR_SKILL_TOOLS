# MAZU-ADGILE

Метод, которым ведут изменение от идеи до проверки. Этот репозиторий — сам метод. Бэклог клиента сюда не кладут: он живёт в локальном `mazu-data/`.

## Одна петля

BMAD даёт фазы и роли. SDD запрещает реализацию, пока нет спецификации и границ Always / Ask First / Never. BDD делает приёмку наблюдаемой: Given / When / Then. ADR фиксирует дорогой выбор. Agile-delivery режет работу на эпик, историю и задачу и отдельно считает сложность (story points) и время (часы). Sysl описывает поведение, CALM — состав системы. Jira, YouTrack, Excel и CSV — источники строк. После импорта источник правды — локальный store, пока вы явно не выгрузите его обратно.

## Роли

| Роль | Файл | Делает | Не делает |
|---|---|---|---|
| Analyst | agents/analyst.md | формулирует проблему и исход | не выбирает архитектуру |
| PO | agents/po.md | эпик, приоритет, ценность | не подменяет points часами |
| Architect | agents/architect.md | ADR, границы, Sysl, CALM | не придумывает ценность |
| SM | agents/scrum-master.md | спринт или канбан, дробление | не меняет принятый ADR |
| Dev | agents/dev.md | одна история, пишет часы через `log` | не ставит `done` |
| QA | agents/qa.md | сверяет каждый Then с уликой | не закрывает без улики |
| Integrator | agents/integrator.md | CSV, xlsx, Jira, YouTrack | не говорит «синхронизировано», если токена нет |
| Skill creator | agents/skill-creator.md | новый скилл по шаблону | не плодит дубли |
| Researcher | agents/researcher.md | проверяет формат harness по источнику | не выдумывает имя конфига |
| Writer | agents/writer.md | документация совпадает с `--help` | не описывает команду, которой нет |
| Release | agents/release.md | зелёный `scripts/audit.py` | не называет план сдачей |

Четыре Grok-бота (BMAD, SDD, ADR, BDD) — эксперты. Идентификаторы в `agents/catalog.json`. Остальные роли — промпты в `agents/`, не отдельные процессы.

## Практика

```bash
python3 cli/mazu.py project new demo
python3 cli/mazu.py add idea "Собрать бэклог из выгрузки"
python3 cli/mazu.py add epic "Импорт без живого Jira" --parent IDEA-001
python3 cli/mazu.py add story "Прочитать CSV" --parent EPIC-001 --points 3 \
  --acceptance "Given a Jira CSV | When I import jira-csv | Then the issue key is kept" \
  --always "store stays valid JSON" --ask-first "change the schema" --never "commit the client backlog"
python3 cli/mazu.py import jira-csv examples/jira.csv
python3 cli/mazu.py sprint new --goal "Импорт виден на доске"
python3 cli/mazu.py dashboard
```

Points — только 1, 2, 3, 5, 8, 13, 21. Историю на 13 режут. 21 означает, что история не готова. Часы пишут командой `log`. Velocity — сумма points историй спринта в статусе `done`. Час не равен поинту.

Статусы одни и для Scrum, и для Kanban: `backlog`, `ready`, `in-progress`, `review`, `done`. Scrum назначает спринт. Kanban смотрит `board` без спринта.

## Трекеры

Без аккаунта работают файлы: `import csv`, `import jira-csv`, `import youtrack-csv`, `import xlsx`. Обратно: `export csv`, `export xlsx`. Колонки описаны в `skills/backlog-connectors/SKILL.md`.

С аккаунтом: `connectors`, затем `pull jira` или `pull youtrack`. Если переменных окружения нет, команда завершается с ошибкой и называет CSV-путь. Это не успешный импорт.

Другие трекеры заходят через их выгрузку CSV или xlsx. Отдельного плагина на каждый продукт нет, пока нет проверенного ответа API.

## Harness

Сами читают файл в репозитории:

- Claude Code — `CLAUDE.md`
- Codex, Kimi CLI, Qwen Code, OpenCode — `AGENTS.md`
- Qwen Code — ещё и `QWEN.md`
- OpenCode — ещё `opencode.json` и `.opencode/agent/`

Промпт, который вставляют руками, потому что отдельный проектный файл здесь не подтверждён:

- GPT, DeepSeek, GigaChat, GigaCode, Grok, Grok-бот — файлы в `configs/`

Схемы вызова: `tools/openai.json` и `tools/gigachat.json`. Для GigaChat цикл такой: `finish_reason = function_call`, выполнить CLI, вернуть сообщение с ролью `function`.

## Готовность

`python3 scripts/audit.py` обходит манифест, проверяет frontmatter скиллов, JSON инструментов, импорт примера Jira CSV, Excel туда-обратно и отказ `pull` без токена. Ненулевой код значит, что метод не готов. Текст в документе не заменяет этот прогон.
