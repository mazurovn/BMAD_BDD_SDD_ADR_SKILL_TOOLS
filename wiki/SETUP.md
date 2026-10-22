# SETUP

Страница самодостаточна. Свежий clone должен пройти `doctor`, `probe`, примеры Sysl/CALM и `release` без скрытого `pip install` для Specify.

## Что нужно

- Системный Python 3.11+ для `cli/mazu.py` и pytest.
- Внутри репозитория уже лежат: `bin/*`, `upstream/node_modules`, `upstream/packages`, `upstream/cpython`, **`upstream/py`** (Specify).

## Первый запуск

```bash
python3 -m pip install -r requirements-dev.txt   # только pytest для тестов/релиза
python3 cli/mazu.py doctor
python3 cli/mazu.py init
bin/specify version
bin/sysl validate diagrams/sysl/example.sysl
bin/calm validate --architecture diagrams/calm/example.calm.json --format json
```

`doctor` печатает `ok`, `pytest: available|missing`, `specify: upstream/py present`. Если `upstream/py` нет — код выхода 1.

## `upstream/py` (размер и лицензии)

| | |
|---|---|
| Назначение | site-packages для `bin/specify` / Spec Kit |
| Объём | ≈138 MiB, ≈2170 файлов (как в zip v1.3.0) |
| Главный пакет | specify-cli 1.2.3, **MIT** (GitHub Spec Kit) |
| Остальное | транзитивные колёса; лицензии в `upstream/py/lib/python3.12/site-packages/*/…dist-info` |
| Откуда | зафиксировано в git; при необходимости восстановить из опубликованного zip `mazu-adgile-1.3.0.zip` каталог `mazu-adgile/upstream/py/` (см. GitHub Releases tag v1.3.0; URL в вики не кладём — audit) |

Не ставить specify через pip «сбоку»: метод ожидает дерево в `upstream/py`.

## Релизные гейты (валидаторы)

`python3 cli/mazu.py release --version X` гоняет по порядку audit → pytest → doctor → in-house `check sysl` / `check calm` → **`bin/sysl validate`** → **`bin/calm validate`** → `scripts/self-demo.sh`. Любой ненулевой код останавливает архив.

Клиентский бэклог остаётся в `mazu-data/` и в репозиторий метода не коммитится.
