# Набор CLI в этом репозитории

Скачивать ничего не нужно. Программы, их скрипты и зависимости уже лежат в дереве. Первый запуск Node только распаковывает `upstream/node/node.xz` своим Python из `upstream/cpython`. Сеть для этого не используется.

Проверка целиком: `sh scripts/self-demo.sh`. Скрипт создаёт проект `kit-self`, проводит истории через гейты и записывает доску в `docs/demo/self-dashboard.html`.

## Где что лежит

| Инструмент | Скрипт | Что исполняется | Зависимость в репозитории |
|---|---|---|---|
| OpenSpec 1.14.3 | `bin/openspec` | `upstream/node_modules/@fission-ai/openspec/bin/openspec.js` | `upstream/node/node.xz` и `upstream/node_modules` |
| CALM 1.65.0 | `bin/calm` | `upstream/node_modules/@finos/calm-cli/dist/index.js` | тот же Node |
| BMAD 6.12.4 | `bin/bmad` | `upstream/node_modules/bmad-method/tools/installer/bmad-cli.js` | тот же Node |
| Cucumber 13.3.0 | `bin/cucumber` | `upstream/node_modules/@cucumber/cucumber/bin/cucumber.js` | тот же Node |
| Sysl 0.792.0 | `bin/sysl` | это сам бинарник, 36 МБ | нет |
| Specify 1.2.3 | `bin/specify` | `upstream/bin/specify` | `upstream/cpython` и `upstream/py` |
| adr-tools | `bin/adr` | `upstream/packages/adr-tools/src/adr` | нет, это shell |

Исходные деревья пакетов, отдельно от `node_modules`: `upstream/packages/openspec`, `upstream/packages/calm-cli`, `upstream/packages/bmad-method`, `upstream/packages/adr-tools`.

Наш слой над ними: `python3 cli/mazu.py upstream <tool> -- <аргументы>`. Он вызывает те же файлы. Если файла нет, команда заканчивается `UPSTREAM-1`, а не выдуманным PASS.

## OpenSpec

Спеки и изменения в `openspec/`. Команды, которые отвечают в этом дереве: `init`, `new change`, `status`, `instructions`, `validate`, `show`, `archive`, `list`, `view`, `change`, `spec`, `config`, `schema`, `doctor`, `context`. Полный текст справки — в `wiki/Commands.md`.

Боевой проход: `bin/openspec --version` печатает `1.14.3`. `python3 cli/mazu.py openspec propose self-demo --intent "..."` пишет proposal, spec, design и tasks. Затем `bin/openspec validate self-demo --strict` должен сказать, что изменение действительно. Требование в спеке обязано содержать MUST или SHALL, иначе строгий валидатор официального CLI отклоняет файл.

Скиллы, которые положил сам `openspec init`, лежат в `.agents`, `.claude`, `.grok`, `.opencode`, `.qwen`, `.kimi-code`, `.gigacode`.

## CALM

`bin/calm validate --architecture diagrams/calm/example.calm.json --format json` возвращает `hasErrors: false`. Пример использует схему 1.2: у узла есть `name` и `description`, у связи есть `unique-id` и `relationship-type.interacts` с `actor` и `nodes`. Команды CLI: `generate`, `validate`, `template`, `docify`, `diff`, `timeline`, `init-ai`, `init-config`, `hub`, `workspace`.

## BMAD

`bin/bmad --version` печатает `6.12.4`. Команды установщика: `install`, `status`, `uninstall`. Модули лежат в `upstream/node_modules/bmad-method`. Наш чекер фаз и эпиков — `python3 cli/mazu.py check phase` и `workflow epics`. Это не замена `bmad install`.

## Cucumber

`bin/cucumber examples/bdd/gate.feature --require examples/bdd/steps.js` выполняет сценарий и заканчивается нулём. Версия `13.3.0`. Это BDD-исполнитель. Наш разбор Given/When/Then для гейта истории — отдельная проверка `python3 cli/mazu.py check bdd ID`.

## Sysl

`bin/sysl` — бинарник `sysl v0.792.0 linux/amd64`. `bin/sysl validate diagrams/sysl/example.sysl` заканчивается нулём. Команды: `validate`, `diagram`, `sd`, `import`, `export`, `codegen`, `datamodel`, `protobuf`, `info`, `repl`, `lsp` и другие из `bin/sysl --help`. Наш `check sysl` смотрит структуру и не заменяет этот бинарник.

## Specify

`bin/specify version` сообщает CLI Version 1.2.3 и Python 3.12.15 из `upstream/cpython`. Команды: `init`, `check`, `version`, `mcp`, `self`, `extension`, `integration`, `event`, `preset`, `artifact`. Это Spec Kit для SDD. Наши границы Always / Ask First / Never проверяет `python3 cli/mazu.py check boundaries ID`.

## adr-tools

`bin/adr help` перечисляет `init`, `new`, `list`, `generate`, `link`, `config`. Скрипты лежат в `upstream/packages/adr-tools/src`. Запись ADR в нашем беклоге: `python3 cli/mazu.py add adr "название" --description "решение"`, затем `check adr ID`. Пустое решение гейт не пропускает.

## Цикл на доске

`sh scripts/self-demo.sh` делает следующее только командами:

1. Проект `kit-self`.
2. Идея, эпик, семь историй, требование и ADR.
3. `gate ready` и спринт S1. История без родителя, очков, сценария или границ не входит.
4. Для каждой истории: запуск её CLI, улика из вывода, `gate done`, статус `done`.
5. `openspec propose self-demo` и строгая проверка официальным OpenSpec.
6. `probe` записывает код выхода каждого CLI в store.
7. `dashboard` пишет HTML. Копия: `docs/demo/self-dashboard.html`.

Полоска «Прогон CLI этого репозитория» на доске берётся из `store.probes`. Зелёная метка означает код 0 этого запуска, не ручную отметку.
