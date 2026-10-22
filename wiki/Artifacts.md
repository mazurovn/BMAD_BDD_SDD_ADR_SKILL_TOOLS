# Артефакты

Источник правды после записи — `store.json` активного проекта. Схема полей: `schemas/store.schema.json`.

У записи есть `id`, `kind`, `title`, `description`, `status`, `points`, `parent`, `sprint`, `acceptance`, `boundaries`, `created_at`, `updated_at`. После импорта ещё `source` и `external_id`.

`boundaries` — объект с тремя списками: `always`, `ask_first`, `never`.

`sprints` хранит `id`, `goal`, `status`, `created_at`.

`time_logs` хранит `item`, `hours`, `note`, `at`. Несколько записей по одной карточке суммируются.

Рядом со store:

- `adr/ADR-00N.md` — текст решения
- `specs/` — спецификации, которые агент кладёт сам из шаблона
- `dashboard.md` и `dashboard.html` — снимок

Шаблоны метода, не проекта: `templates/adr.md`, `templates/user-story.md`, `templates/spec.md`, `templates/epic.md`, `templates/boundaries.md`, `templates/sprint-status.yaml`.

Sysl и CALM метода лежат в `diagrams/`. Для клиентского описания такие же файлы кладут в каталог проекта и не коммитят в репозиторий метода.

## Кто имеет право менять поле

| Поле | Кто пишет | Чем проверяют |
|---|---|---|
| title, description, parent | автор карточки | workflow epics для дерева |
| points | PO | check points и gate ready |
| acceptance | BDD author | check bdd |
| boundaries | SDD author | check boundaries и check guard |
| evidence | QA | gate done |
| sprint | scrum master | gate sprint |
| time_logs | разработчик | log, часы больше нуля |
| status done | QA | move done после gate done |
| файл adr | ADR keeper | check adr |

Пустое поле не считается заполненным. `_fill in_` в Decision — пустое решение. Часы не заполняют points. Внешний ключ не становится локальным id.

`intake` читает заметки с метками `pain`, `idea`, `interview`, `task`, `research` (и те же слова по-русски). Из них он пишет идею, эпик, истории с приёмкой и границами, требование, файл `specs/EPIC-00N.md`, `calm.json` и `system.sysl`. Истории, которые проходят `gate ready`, попадают в новый спринт. `trace ID` печатает восемь точек цикла: источник, декомпозиция, спека, границы, гейт, улика, спринт, готово. Доска показывает те же точки во вкладке «цикл».



## Чего в store нет

Нет живой связи с Jira. Импорт копирует строки. Нет учётной записи человека. Нет секретов. Если секрет попал в описание, его удаляют из store до любого коммита, а проектный store всё равно не коммитят.

