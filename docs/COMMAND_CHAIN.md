# Цепочка команд

Каждая строка — запуск `python3 cli/mazu.py`. Чат `/opsx:*` идёт через `chat`, тот вызывает ту же функцию, что и прямая команда.

- Шагов: 25
- Совпало: 25
- Не совпало: 0

| Чат | CLI | Функция | Код | Ожидали | Итог |
|---|---|---|---:|---:|---|
| `/opsx:explore gate-visible` | `chat /opsx:explore gate-visible Оператор видит отказ гейта` | `openspec_flow.explore` | 0 | 0 | ok |
| `/opsx:propose gate-visible` | `chat /opsx:propose gate-visible Оператор видит отказ гейта` | `openspec_flow.propose` | 0 | 0 | ok |
| `validate` | `openspec validate gate-visible` | `openspec_flow.validate` | 0 | 0 | ok |
| `propose again` | `openspec propose gate-visible --intent Оператор видит отказ гейта` | `openspec_flow.propose` | 1 | 1 | ok |
| `/opsx:apply` | `chat /opsx:apply gate-visible` | `openspec_flow.link_task` | 0 | 0 | ok |
| `tasks still open` | `read tasks.md` | `openspec_flow.tasks` | 0 | 0 | ok |
| `complete without evidence` | `openspec complete gate-visible --task 1.1 --evidence ` | `openspec_flow.complete` | 1 | 1 | ok |
| `complete 1.1` | `openspec complete gate-visible --task 1.1 --evidence отказ напечатан` | `openspec_flow.complete` | 0 | 0 | ok |
| `archive too early` | `openspec archive gate-visible` | `openspec_flow.archive` | 1 | 1 | ok |
| `complete 1.2` | `openspec complete gate-visible --task 1.2 --evidence пустая улика отклонена` | `openspec_flow.complete` | 0 | 0 | ok |
| `/opsx:archive` | `chat /opsx:archive gate-visible` | `openspec_flow.archive` | 0 | 0 | ok |
| `archive files` | `filesystem` | `openspec_flow.archive` | 0 | 0 | ok |
| `bdd pass` | `check bdd US-001` | `bdd.acceptance_issues` | 0 | 0 | ok |
| `add vague story` | `add story Плохо --points 3 --acceptance Given a When b Then works well --never Commit secrets` | `bdd.acceptance_issues` | 0 | 0 | ok |
| `bdd fail` | `check bdd US-003` | `bdd.acceptance_issues` | 1 | 1 | ok |
| `sdd refuse` | `check guard commit secrets --never commit secrets` | `sdd.guard` | 1 | 1 | ok |
| `bmad block` | `check phase implementation` | `bmad.phase_issues` | 1 | 1 | ok |
| `bmad pass` | `check phase implementation --outcome Оператор видит отказ гейта --has-boundaries --has-check` | `bmad.phase_issues` | 0 | 0 | ok |
| `adr create` | `add adr One JSON file --description One writer` | `adr.write` | 0 | 0 | ok |
| `adr empty` | `check adr ADR-001` | `adr.issues` | 1 | 1 | ok |
| `adr filled` | `check adr ADR-001` | `adr.issues` | 0 | 0 | ok |
| `sysl` | `check sysl /tmp/bmad-repo/diagrams/sysl/backlog.sysl` | `sysl_check.issues` | 0 | 0 | ok |
| `calm` | `check calm /tmp/bmad-repo/diagrams/calm/backlog.calm.json` | `calm_check.issues` | 0 | 0 | ok |
| `sysl svg` | `diagram sysl /tmp/bmad-repo/diagrams/sysl/backlog.sysl -o /tmp/pytest-of-root/pytest-28/test_command_chain0/chain/sysl.svg` | `sysl_draw.draw` | 0 | 0 | ok |
| `calm svg` | `diagram calm /tmp/bmad-repo/diagrams/calm/backlog.calm.json -o /tmp/pytest-of-root/pytest-28/test_command_chain0/chain/calm.svg` | `calm_draw.draw` | 0 | 0 | ok |

## Ответы

### /opsx:explore gate-visible

```
chat: /opsx:explore gate-visible Оператор видит отказ гейта
cli: openspec explore gate-visible
function: mazu_method.openspec_flow.explore
/tmp/pytest-of-root/pytest-28/test_command_chain0/chain/openspec/explore/gate-visible.md
```

### /opsx:propose gate-visible

```
chat: /opsx:propose gate-visible Оператор видит отказ гейта
cli: openspec propose gate-visible
function: mazu_method.openspec_flow.propose
/tmp/pytest-of-root/pytest-28/test_command_chain0/chain/openspec/changes/gate-visible
PASS propose
```

### validate

```
PASS validate
```

### propose again

```
OPENSPEC-4 change already exists: /tmp/pytest-of-root/pytest-28/test_command_chain0/chain/openspec/changes/gate-visible
```

### /opsx:apply

```
chat: /opsx:apply gate-visible
cli: openspec apply gate-visible
function: mazu_method.openspec_flow.apply
initialized /tmp/pytest-of-root/pytest-28/test_command_chain0/chain/mazu-data
US-001
US-002
PASS apply
1.1 -> US-001
1.2 -> US-002
```

### tasks still open

```
boxes open and story ids linked
```

### complete without evidence

```
OPENSPEC-5 evidence is required
```

### complete 1.1

```
PASS complete 1.1
```

### archive too early

```
OPENSPEC-6 not ready: 1.2
```

### complete 1.2

```
PASS complete 1.2
```

### /opsx:archive

```
chat: /opsx:archive gate-visible
cli: openspec archive gate-visible
function: mazu_method.openspec_flow.archive
/tmp/pytest-of-root/pytest-28/test_command_chain0/chain/openspec/changes/archive/2026-10-22-gate-visible
PASS archive
```

### archive files

```
/tmp/pytest-of-root/pytest-28/test_command_chain0/chain/openspec/changes/archive/2026-10-22-gate-visible
```

### bdd pass

```
PASS
```

### add vague story

```
US-003
```

### bdd fail

```
FAIL BDD-1 Then is not observable (scenario 1)
```

### sdd refuse

```
BOUND-3 refuse: commit secrets
```

### bmad block

```
FAIL BMAD-1 outcome is missing
FAIL BMAD-1 boundaries are missing
FAIL BMAD-1 the check is missing
```

### bmad pass

```
PASS
```

### adr create

```
ADR-001
```

### adr empty

```
FAIL ADR-2 decision is empty
```

### adr filled

```
PASS
```

### sysl

```
PASS
```

### calm

```
PASS
```

### sysl svg

```
/tmp/pytest-of-root/pytest-28/test_command_chain0/chain/sysl.svg
```

### calm svg

```
/tmp/pytest-of-root/pytest-28/test_command_chain0/chain/calm.svg
```
