# CLI

Запуск из каталога, где должен появиться `mazu-data/`. Интерпретатор: Python 3.11+.

```bash
python3 cli/mazu.py <команда>
```

`cli/mazu` делает то же самое.

## Команды

`init` создаёт store, папки `adr` и `specs`. Повторный запуск ничего не затирает.

`project new ИМЯ` создаёт `mazu-data/projects/имя` и делает его активным. `project use ИМЯ` переключает. `project list` помечает активный звёздочкой. Без активного проекта команды пишут в `mazu-data/store.json`.

`add ВИД "название"` — вид один из `idea`, `epic`, `story`, `task`, `requirement`, `adr`.

Флаги `add`:

- `--description`
- `--parent ID`
- `--points` только 1, 2, 3, 5, 8, 13, 21
- `--status` из `backlog`, `ready`, `in-progress`, `review`, `done`
- `--acceptance` сценарии через `|`
- `--always`, `--ask-first`, `--never` пункты через `|`

`list` фильтры `--kind`, `--status`, `--sprint`. `show ID` печатает JSON.

`move ID СТАТУС` переносит карточку. `log ID ЧАСЫ --note "..."` добавляет затраченное время. Часы должны быть больше нуля.

`sprint new --goal "..."`. `sprint add --id US-001 --sprint S1` пускает только историю, которая уже проходит ready. Иначе печатает FAIL и спринт не меняет. Эпик и задачу в спринт положить нельзя.

`board` печатает колонки. `--sprint S1` сужает.

`dashboard` пишет `dashboard.md` и пастельный `dashboard.html`. В снимке кнопки не меняют store.

`serve --port 8765` поднимает ту же доску на `127.0.0.1`. Кнопки влево и вправо вызывают `move`. Формы добавляют запись, пишут часы и открывают спринт. Слушает только localhost.

`import csv|jira-csv|youtrack-csv|xlsx ФАЙЛ` читает первую таблицу. `export csv|xlsx ФАЙЛ` выгружает активный store.

`connectors` говорит, заданы ли переменные Jira и YouTrack. Значения не печатает.

`pull jira --jql "..."` требует `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_TOKEN`. `pull youtrack --jql "..."` требует `YOUTRACK_URL`, `YOUTRACK_TOKEN`. Без них команда завершается с ошибкой и предлагает CSV.

`skill new имя --title --description` создаёт `skills/имя/SKILL.md`. `--force` перезаписывает.

`doctor` проверяет, что обязательные файлы метода на месте.

## Проверки, которые нельзя заменить словами

`check bdd ID` проверяет Given, When, Then.
`check boundaries ID` проверяет, что границы не пустые.
`check points ID` печатает points и часы рядом и не складывает их.
`check adr ID` читает файл решения и отвергает пустой Decision.
`check sysl ФАЙЛ` и `check calm ФАЙЛ` проверяют схемы в `diagrams/`.
`check phase ИМЯ` не пускает в фазу без факта. Для implementation нужны `--outcome`, `--has-boundaries` и `--has-check`.
`check guard "действие" --ask "..." --never "..."` останавливает Ask First и отказывает Never.
`check wip board` считает истории в `in-progress`. Больше двух — отказ.

`gate ready ID` и `gate done ID` собирают эти проверки. `move ID ready` и `move ID done` вызывают те же проверки и не двигают карточку, если есть FAIL. Промежуточные колонки `in-progress` и `review` двигаются без этого гейта: их держит лимит и ревью.

`workflow epics --idea IDEA --epic EPIC` проверяет дерево.
`workflow sprint --sprint S1` проверяет цель и каждую историю.

`tools` печатает владельца каждой команды. `guide ТЕМА` печатает раздел `wiki/Manual.md`.

## Идентификаторы

`IDEA`, `EPIC`, `US`, `TASK`, `REQ`, `ADR` плюс номер. Спринты: `S1`, `S2`. Внешний ключ трекера лежит в `external_id` и не подменяет локальный id.
