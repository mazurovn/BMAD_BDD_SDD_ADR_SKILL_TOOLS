# Онбординг

Релиз собирается из ветки `main`. Архив — тот же набор файлов, что в коммите. Сырые заметки: `python3 cli/mazu.py intake --file examples/intake.md`. Команда сама собирает беклог, спеку, CALM, Sysl и спринт из историй, которые проходят ready. Доска: `dashboard`, вкладка «цикл».

## Что открыть первым

1. Этот файл.
2. `wiki/Kit.md` — где лежит каждый CLI и чем он отличается от нашего гейта.
3. `wiki/Commands.md` — текст `--help`, снятый с установленных программ.
4. `wiki/Manual.md` — гейты беклога.
5. Роль в `agents/`, затем скилл в `skills/<имя>/SKILL.md`.

## Проверка, что архив живой

Из корня репозитория, без сети и без установки пакетов:

```
bin/openspec --version
bin/calm --version
bin/bmad --version
bin/cucumber --version
bin/sysl --version
bin/specify version
bin/adr help
python3 cli/mazu.py doctor
sh scripts/self-demo.sh
```

Ожидание: OpenSpec `1.14.3`, CALM `1.65.0`, BMAD `6.12.4`, Cucumber `13.3.0`, Sysl `v0.792.0`, Specify `1.2.3`. `doctor` перечисляет обязательные файлы. `self-demo.sh` создаёт проект `kit-self` и пишет `docs/demo/self-dashboard.html`.

## Как устроено

Наш CLI — `python3 cli/mazu.py`. Он хранит беклог в `mazu-data/` и не скачивает трекеры. Команда `upstream` и скрипты `bin/` запускают чужие программы, которые уже лежат в дереве.

| Вопрос | Куда смотреть | Команда |
|---|---|---|
| Что меняем и зачем | OpenSpec | `bin/openspec validate ИМЯ --strict` |
| Кто с кем связан | CALM | `bin/calm validate --architecture ФАЙЛ --format json` |
| Поведение эндпоинтов | Sysl | `bin/sysl validate ФАЙЛ` |
| Сценарий словами клиента | BDD | `bin/cucumber ФАЙЛ.feature --require ШАГИ` |
| Границы агента | SDD | `python3 cli/mazu.py check boundaries ID` |
| Спека до кода | Specify | `bin/specify version` |
| Решение, которое нельзя молча отменить | ADR | `bin/adr help` и `python3 cli/mazu.py check adr ID` |
| Фазы и нарезка | BMAD | `bin/bmad --version` и `python3 cli/mazu.py workflow epics` |
| Спринт и доска | Agile | `python3 cli/mazu.py gate sprint S1` и `dashboard` |

Чужой CLI не подменяется нашим текстом. Если `bin/calm` вернул ошибку, запись в беклоге не становится принятой.

## Цикл от идеи до улики

1. `project new ИМЯ` и `project use ИМЯ`.
2. `add idea`, затем эпик с `--parent`.
3. Истории: родитель, points из 1 2 3 5 8, одна строка `Given ... When ... Then ...`, границы `--always`, `--ask-first`, `--never`.
4. `gate ready ID`. Отказ означает, что карточка ещё не готова. Её не кладут в спринт.
5. `sprint new --goal "..."` и `sprint add --id ID --sprint S1`.
6. Работа: `move ID in-progress`, `log ID ЧАСЫ --note "..."`.
7. Улика — прогон команды: `evidence ID --run КОМАНДА` (exit 0). Пересказ «тесты прошли» `gate done` не примет.
8. `gate done ID`, затем `move ID done`.
9. Изменение спеки: `openspec propose ИМЯ --intent "..."`, потом `bin/openspec validate ИМЯ --strict`. В требовании должно быть MUST или SHALL.

## Что в архиве и зачем

- `bin/` — команды, с которых начинают.
- `upstream/packages/` — исходники OpenSpec, CALM, BMAD и adr-tools.
- `upstream/node_modules/` — их зависимости, уже установлены. `npm install` не нужен.
- `upstream/py` и `upstream/cpython` — Specify и его Python 3.12 (оба в git; размер и лицензии в `wiki/SETUP.md`). Системный Python 3.10 для Specify недостаточен.
- `bin/sysl` — бинарник Sysl. Компилятор Go в архив не входит и не требуется.
- `skills/`, `agents/`, `wiki/` — как работать.
- `src/mazu_method/` и `cli/mazu.py` — гейты.
- `openspec/` — изменения, включая `self-demo` и `bind-upstreams`.
- `diagrams/` — примеры, которые проходят официальные `calm validate` и `sysl validate`.

Node в архив как программу ставить не надо. Запасной `upstream/node/node.xz` можно не трогать, пока `node --version` отвечает.

## Чего агент не делает

Не ставит пакеты. Не пишет PASS без кода выхода. Не закрывает историю без улики на каждый Then. Не архивирует изменение OpenSpec, пока в `tasks.md` есть открытый пункт. Не путает story points и часы.
