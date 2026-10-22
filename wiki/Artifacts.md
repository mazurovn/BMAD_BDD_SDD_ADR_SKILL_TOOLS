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
