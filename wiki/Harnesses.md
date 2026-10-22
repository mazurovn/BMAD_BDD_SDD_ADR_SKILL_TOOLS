# Harnesses

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


# Вызов инструментов

Имя функции берут из `tools/openai.json` или `tools/gigachat.json`. Рядом нет скрытого сервера: функция означает команду `python3 cli/mazu.py`. Пока stdout не прочитан, агент не знает, что получилось.

## Ответственность

Владелец: Любая роль, которая трогает store.
Код, который проверяет результат: `tools/openai.json`.
Если вопрос принадлежит другой роли, этот скилл останавливается и называет её. Он не закрывает чужой гейт и не подменяет чужое решение.

## Когда открывать

- Модель в harness умеет function call.
- Надо объяснить, почему нельзя просто пообещать запись в бэклог.

## Когда не открывать

- Человек явно просит только объяснить правило и не трогать store.

## Входы, без которых процедуру не начинают

- Схема из файла tools, не из памяти модели.
- Аргументы, которые есть у соответствующей команды `--help`.

## Процедура

1. Найти функцию в схеме. Если имени нет, не вызывать выдуманное.
2. Собрать команду CLI с теми же аргументами.
3. Выполнить её в каталоге набора или проекта.
4. Для GigaChat после finish_reason function_call вернуть результат отдельным сообщением роли function.
5. В ответе человеку привести id и строку PASS или FAIL, если был гейт.

## Гейты и гардрейлы

- Нет схемы — нет вызова.
- Ненулевой код не превращают в успех перефразированием.

Ненулевой код выхода — это отказ. Агент не пишет, что шаг пройден, пока в stdout нет `PASS`.

## Делать

- Повторять команду в ответе, чтобы её можно было проверить.
- Передавать только те поля, которые команда принимает.

## Не делать

- Не печатать токены, которые команда connectors скрывает.
- Не вызывать pull повторно «на всякий случай», если первый завершился ошибкой из-за отсутствия токена.

## Контроль качества

- Каждому утверждению «записано» соответствует id из stdout.
- Имя функции есть в JSON схемы.

## Как выглядит провал

- Ответ «добавил US-010», а `list` его не показывает.
- Вызвана функция, которой нет в tools.

## Передача

Дальше работает скилл той роли, чью команду вызвали. Tool-calling сам работу не делает.

## Пример команд

```bash
python3 cli/mazu.py tools
python3 cli/mazu.py --help
```

## Применение инструментов

Каждая команда выше — это `python3 cli/mazu.py ...` из корня набора. Схему вызова для модели берут из `tools/openai.json` или `tools/gigachat.json` и не выдумывают имя функции. Результат известен только после stdout.
