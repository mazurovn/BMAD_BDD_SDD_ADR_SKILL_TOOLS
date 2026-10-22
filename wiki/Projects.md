# Проекты

Один каталог `mazu-data/` может держать несколько бэклогов.

```bash
python3 cli/mazu.py project new alpha
python3 cli/mazu.py project list
python3 cli/mazu.py project use alpha
```

Активное имя лежит в `mazu-data/active-project`. Данные проекта: `mazu-data/projects/alpha/store.json`, рядом его ADR, спеки и дашборд.

`project new` не удаляет уже существующий store. `project use` на неизвестное имя завершается ошибкой.

Импорт, спринт, часы и `serve` всегда касаются только активного проекта. Чтобы не смешать два бэклога, перед импортом выполняют `project use`.

Каталог `mazu-data/` не коммитят. Это рабочее состояние, не метод.
