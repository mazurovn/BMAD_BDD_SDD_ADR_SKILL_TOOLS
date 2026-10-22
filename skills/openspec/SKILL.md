---
name: openspec
description: Команды /opsx:propose, apply, archive и остальные. Каждая пишет файл и проверяет его.
---

# OpenSpec

`/opsx:propose` в чате — это не обещание. Команда `chat` вызывает `openspec propose`, функция `mazu_method.openspec_flow.propose` пишет четыре артефакта, `validate` читает их обратно. Нет файла — нет предложения.

## Ответственность

Владелец: SDD author.
Код: `src/mazu_method/openspec_flow.py`.
Команда не пишет код продукта и не ставит `[x]` сама.

## Когда открывать

- Человек написал `/opsx:propose`, `/opsx:apply`, `/opsx:archive`, `/opsx:explore`, `/opsx:update`, `/opsx:sync`.
- Нужно изменение с proposal, delta spec, design и tasks до кода.

## Когда не открывать

- Нужна только проверка одного Then у уже существующей истории. Это BDD.
- Нужен дорогой выбор без изменения. Это ADR.

## Входы, без которых процедуру не начинают

- Имя изменения латиницей.
- Исход одной фразой длиннее семи символов. Короткий отказ — `OPENSPEC-0`.

## Процедура

1. Разобрать чат: `python3 cli/mazu.py chat "/opsx:propose имя исход"`.
2. Прочитать stdout. Первые строки — chat, cli, function. Дальше путь каталога и `PASS propose`.
3. Повторить проверку прямой командой: `python3 cli/mazu.py openspec validate имя`.
4. `python3 cli/mazu.py openspec apply имя` создаёт историю на каждую открытую задачу и дописывает `story:US-00N` в tasks.md. Квадрат остаётся `[ ]`.
5. Закрыть задачу только с уликой: `python3 cli/mazu.py openspec complete имя --task 1.1 --evidence "что наблюдали"`.
6. `archive` переносит каталог в `openspec/changes/archive/ГГГГ-ММ-ДД-имя/` и копирует spec в `openspec/specs/`. Пока есть `[ ]` или нет evidence.md, команда завершается с `OPENSPEC-6`.

## Гейты и гардрейлы

- Повторный propose в тот же каталог — `OPENSPEC-4`, файлы не затираются.
- Пустой evidence на complete — `OPENSPEC-5`.
- Archive без закрытых задач — отказ. В оригинальном OpenSpec это предупреждение. Здесь это блок, потому что иначе «закрыто» ничего не значит.
- Apply не отмечает задачи сделанными. Это и есть защита от фейковой реализации.

## Делать

- Сверять, что в proposal.md есть исход человека, а не общая фраза.
- После archive проверять, что активный каталог исчез, а архивный и основной spec на месте.

## Не делать

- Не ставить `[x]` руками, чтобы archive прошёл.
- Не называть apply написанным кодом продукта. Он создаёт карточки.
- Не архивировать чужое изменение, не прочитав tasks.md.

## Контроль качества

- `validate` печатает PASS.
- В specs есть `#### Scenario:` и строки GIVEN / THEN.
- Число строк в evidence.md не меньше числа закрытых задач.

## Как выглядит провал

- OPENSPEC-1 missing proposal.md, design.md, tasks.md или spec.
- OPENSPEC-2 scenario is missing.
- OPENSPEC-6 not ready.

## Передача

После propose spec читает BDD author. Истории из apply забирает PO: у них ещё нет родителя-эпика, поэтому в спринт они сами не попадут. Archive делает SDD author, не разработчик.

## Пример команд

```bash
python3 cli/mazu.py chat "/opsx:propose gate-visible Оператор видит отказ гейта"
python3 cli/mazu.py openspec validate gate-visible
python3 cli/mazu.py openspec apply gate-visible
python3 cli/mazu.py openspec complete gate-visible --task 1.1 --evidence "отказ напечатан"
```

## Применение инструментов

Функция в `tools/openai.json` называется `mazu_openspec`. Она не заменяет чтение stdout.

Боевой бинарник-скрипт: `bin/openspec`. Версия в этом дереве 1.14.3. Строгая проверка: `bin/openspec validate ИМЯ --strict`. Наш propose пишет MUST, иначе официальный валидатор отклоняет спеку.
