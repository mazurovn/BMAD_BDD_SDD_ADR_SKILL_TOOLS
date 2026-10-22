# Боевой отчёт

Отчёт собран скриптом `scripts/enterprise_demo.py`. Каждая строка — реальный запуск `python3 cli/mazu.py`. Числа не выдуманы.

- Команд: 49
- Совпало с ожидаемым кодом выхода: 49
- Не совпало: 0
- Сумма времени CLI, мс: 2991.2
- Карточек в store: 11
- Спринтов: 1
- Записей времени: 1

| Команда | Код | Ожидали | мс | Итог |
|---|---:|---:|---:|---|
| `init` | 0 | 0 | 62.1 | ok |
| `project new enterprise-demo` | 0 | 0 | 61.0 | ok |
| `add idea Оператор видит отказ гейта до того, как история попала в спринт` | 0 | 0 | 61.2 | ok |
| `add epic Гейт ready обязателен --parent IDEA-001` | 0 | 0 | 61.1 | ok |
| `add requirement Когда Then нельзя проверить, gate ready завершается с ошибкой --parent EPIC-001` | 0 | 0 | 61.4 | ok |
| `add story Плохой сценарий --parent EPIC-001 --points 3 --acceptance Given a user When they save Then works well --never Commit secrets` | 0 | 0 | 61.6 | ok |
| `gate ready US-001` | 1 | 1 | 61.6 | ok |
| `add story Сохранить карточку --parent EPIC-001 --points 5 --acceptance Given a user When they save Then the store has the story | Given an empty title When they save Then the command exits non-zero --always Keep the store valid --ask-first new dependency --never Commit secrets` | 0 | 0 | 63.3 | ok |
| `add story Показать отказ --parent EPIC-001 --points 3 --acceptance Given a failed check When the operator opens the board Then the story is not in the sprint --never Commit secrets` | 0 | 0 | 81.7 | ok |
| `check bdd US-002` | 0 | 0 | 61.5 | ok |
| `check boundaries US-002` | 0 | 0 | 61.4 | ok |
| `check points US-002` | 0 | 0 | 63.9 | ok |
| `gate ready US-002` | 0 | 0 | 61.5 | ok |
| `gate ready US-003` | 0 | 0 | 61.7 | ok |
| `workflow epics --idea IDEA-001 --epic EPIC-001` | 1 | 1 | 63.5 | ok |
| `add story Слишком крупная --parent EPIC-001 --points 13 --acceptance Given a slice When it is still 13 Then it stays out of ready --never Commit secrets` | 0 | 0 | 69.2 | ok |
| `gate ready US-004` | 1 | 1 | 76.1 | ok |
| `add story Чужая шкала --parent EPIC-001 --points 4` | 1 | 1 | 65.5 | ok |
| `add adr Store is one JSON file --description One operator and no concurrent writers` | 0 | 0 | 64.4 | ok |
| `check adr ADR-001` | 1 | 1 | 62.8 | ok |
| `edit ADR-001 Decision by the ADR procedure` | 0 | 0 | 0 | ok |
| `check adr ADR-001` | 0 | 0 | 63.3 | ok |
| `sprint new --goal В спринт попадают только истории, прошедшие ready` | 0 | 0 | 70.5 | ok |
| `sprint add --id US-002 --sprint S1` | 0 | 0 | 65.7 | ok |
| `sprint add --id US-003 --sprint S1` | 0 | 0 | 63.5 | ok |
| `workflow sprint --sprint S1` | 0 | 0 | 62.1 | ok |
| `gate sprint S1` | 0 | 0 | 62.5 | ok |
| `move US-002 in-progress` | 0 | 0 | 62.3 | ok |
| `log US-002 1.5 --note saved the row` | 0 | 0 | 62.0 | ok |
| `move US-002 review` | 0 | 0 | 62.4 | ok |
| `gate done US-002` | 1 | 1 | 62.6 | ok |
| `evidence US-002 store contained the story` | 0 | 0 | 64.0 | ok |
| `evidence US-002 empty title exited non-zero` | 0 | 0 | 63.2 | ok |
| `gate done US-002` | 0 | 0 | 63.0 | ok |
| `move US-002 done` | 0 | 0 | 63.2 | ok |
| `check wip board` | 0 | 0 | 62.6 | ok |
| `check phase implementation --outcome Оператор видит отказ гейта` | 1 | 1 | 61.4 | ok |
| `check phase implementation --outcome Оператор видит отказ гейта --has-boundaries --has-check` | 0 | 0 | 62.4 | ok |
| `check guard commit secrets --never commit secrets` | 1 | 1 | 62.5 | ok |
| `check guard keep store valid --always keep store valid` | 0 | 0 | 62.3 | ok |
| `check sysl /tmp/bmad-repo/diagrams/sysl/example.sysl` | 0 | 0 | 62.5 | ok |
| `check sysl /tmp/bmad-repo/diagrams/sysl/backlog.sysl` | 0 | 0 | 62.2 | ok |
| `check calm /tmp/bmad-repo/diagrams/calm/example.calm.json` | 0 | 0 | 61.4 | ok |
| `check calm /tmp/bmad-repo/diagrams/calm/backlog.calm.json` | 0 | 0 | 61.4 | ok |
| `import jira-csv /tmp/bmad-repo/examples/jira.csv` | 0 | 0 | 67.6 | ok |
| `dashboard` | 0 | 0 | 63.3 | ok |
| `connectors` | 0 | 0 | 63.0 | ok |
| `pull jira --jql project = DEMO` | 1 | 1 | 61.8 | ok |
| `GET http://127.0.0.1:8767/` | 0 | 0 | 0 | ok |

## Что команды ответили

### init

```
initialized /tmp/pytest-of-root/pytest-23/test_enterprise_demo0/demo/mazu-data
```

### project new enterprise-demo

```
enterprise-demo
```

### add idea Оператор видит отказ гейта до того, как история попала в спринт

```
IDEA-001
```

### add epic Гейт ready обязателен --parent IDEA-001

```
EPIC-001
```

### add requirement Когда Then нельзя проверить, gate ready завершается с ошибкой --parent EPIC-001

```
REQ-001
```

### add story Плохой сценарий --parent EPIC-001 --points 3 --acceptance Given a user When they save Then works well --never Commit secrets

```
US-001
```

### gate ready US-001

```
FAIL US-001 BDD-1 Then is not observable (scenario 1)
```

### add story Сохранить карточку --parent EPIC-001 --points 5 --acceptance Given a user When they save Then the store has the story | Given an empty title When they save Then the command exits non-zero --always Keep the store valid --ask-first new dependency --never Commit secrets

```
US-002
```

### add story Показать отказ --parent EPIC-001 --points 3 --acceptance Given a failed check When the operator opens the board Then the story is not in the sprint --never Commit secrets

```
US-003
```

### check bdd US-002

```
PASS
```

### check boundaries US-002

```
PASS
```

### check points US-002

```
points=5 hours=0.0
PASS
```

### gate ready US-002

```
PASS ready US-002
```

### gate ready US-003

```
PASS ready US-003
```

### workflow epics --idea IDEA-001 --epic EPIC-001

```
FAIL US-001 BDD-1 Then is not observable (scenario 1)
```

### add story Слишком крупная --parent EPIC-001 --points 13 --acceptance Given a slice When it is still 13 Then it stays out of ready --never Commit secrets

```
US-004
```

### gate ready US-004

```
FAIL US-004 EPIC-2 points are too large to be ready
```

### add story Чужая шкала --parent EPIC-001 --points 4

```
points must be one of (1, 2, 3, 5, 8, 13, 21)
```

### add adr Store is one JSON file --description One operator and no concurrent writers

```
ADR-001
```

### check adr ADR-001

```
FAIL ADR-2 decision is empty
```

### edit ADR-001 Decision by the ADR procedure

```
replaced empty Decision
```

### check adr ADR-001

```
PASS
```

### sprint new --goal В спринт попадают только истории, прошедшие ready

```
S1
```

### sprint add --id US-002 --sprint S1

```
US-002 in S1
```

### sprint add --id US-003 --sprint S1

```
US-003 in S1
```

### workflow sprint --sprint S1

```
PASS
velocity 0
```

### gate sprint S1

```
PASS sprint S1
```

### move US-002 in-progress

```
US-002 -> in-progress
```

### log US-002 1.5 --note saved the row

```
logged 1.5h on US-002
```

### move US-002 review

```
US-002 -> review
```

### gate done US-002

```
FAIL US-002 BDD-4 no evidence
```

### evidence US-002 store contained the story

```
evidence 1 on US-002
```

### evidence US-002 empty title exited non-zero

```
evidence 2 on US-002
```

### gate done US-002

```
PASS done US-002
```

### move US-002 done

```
US-002 -> done
```

### check wip board

```
PASS
```

### check phase implementation --outcome Оператор видит отказ гейта

```
FAIL BMAD-1 boundaries are missing
FAIL BMAD-1 the check is missing
```

### check phase implementation --outcome Оператор видит отказ гейта --has-boundaries --has-check

```
PASS
```

### check guard commit secrets --never commit secrets

```
BOUND-3 refuse: commit secrets
```

### check guard keep store valid --always keep store valid

```
PASS proceed
```

### check sysl /tmp/bmad-repo/diagrams/sysl/example.sysl

```
PASS
```

### check sysl /tmp/bmad-repo/diagrams/sysl/backlog.sysl

```
PASS
```

### check calm /tmp/bmad-repo/diagrams/calm/example.calm.json

```
PASS
```

### check calm /tmp/bmad-repo/diagrams/calm/backlog.calm.json

```
PASS
```

### import jira-csv /tmp/bmad-repo/examples/jira.csv

```
imported 3 from jira-csv
```

### dashboard

```
# MAZU dashboard

Generated: 2026-10-22T15:03:18Z

## By status
- backlog: 7
- ready: 1
- in-progress: 1
- review: 0
- done: 2

## By kind
- idea: 1
- epic: 2
- story: 5
- task: 1
- requirement: 1
- adr: 1

## Estimation
- story points open: 22
- story points done: 5
- hours logged: 1.5

## Sprints
- S1 [planned] velocity=5 goal: В спринт попадают только истории, прошедшие ready

## Board

| ID | Kind | Status | SP | Hours | Sprint | Title |
|---|---|---|---|---|---|---|
| IDEA-001 | idea | back
```

### connectors

```
jira: not connected, missing JIRA_BASE_URL, JIRA_EMAIL, JIRA_TOKEN
youtrack: not connected, missing YOUTRACK_URL, YOUTRACK_TOKEN
csv: ready
xlsx: ready
live pull is optional. Without tokens use: import jira-csv | import youtrack-csv | import xlsx
```

### pull jira --jql project = DEMO

```
Jira is not connected. Set JIRA_BASE_URL, JIRA_EMAIL, JIRA_TOKEN or export a CSV and run: mazu import jira-csv FILE
```

### GET http://127.0.0.1:8767/

```
dashboard http 200
```
