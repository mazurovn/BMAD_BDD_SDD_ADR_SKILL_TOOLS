# MAZU-ADGILE

Method for running BMAD, SDD, BDD, ADR, Sysl, CALM, and agile delivery as one loop.
Russian walkthrough: [MAZU-ADGILE.ru.md](MAZU-ADGILE.ru.md).
This repository is the method. It does not contain a product backlog.

## What you produce

| Artifact | Command | File |
|---|---|---|
| Idea | `add idea` | store |
| Epic | `add epic --parent IDEA-00N` | store |
| Requirement | `add requirement` | store |
| Spec | copy templates/spec.md | `mazu-data/specs/` |
| Story | `add story --points N --acceptance "..."` | store |
| Task | `add task --parent US-00N` | store |
| ADR | `add adr` | `mazu-data/adr/ADR-00N.md` |
| Sprint | `sprint new` / `sprint add` | store |
| Hours | `log ID 1.5` | store `time_logs` |
| Board | `board` | stdout |
| Dashboard | `dashboard` | `mazu-data/dashboard.md` and `.html` |
| System behavior | edit | `diagrams/sysl/*.sysl` |
| System shape | edit | `diagrams/calm/*.calm.json` |

## Loop

1. Analyst writes an idea. If the outcome is not one sentence, stop.
2. PO writes an epic and requirements. Spec file uses `templates/spec.md`.
3. Architect writes an ADR for any expensive choice and sets boundaries:
   - Always — do it
   - Ask First — stop and ask
   - Never — do not do it
4. PO and SM slice stories. Points are Fibonacci only: 1, 2, 3, 5, 8, 13, 21. A 13 is a split candidate. A 21 is not ready.
5. Each story has at least one Given/When/Then scenario.
6. SM opens a sprint (`sprint new --goal`) or runs Kanban (`board` with no sprint).
7. Dev moves `ready → in-progress → review` and logs hours. Hours are not points.
8. QA moves to `done` only with evidence for every scenario.
9. `dashboard` shows counts, open points, done points, hours, and per-sprint velocity (done story points).

## BMAD v6 names, local actions

| Workflow | Do this |
|---|---|
| create-epics-and-stories | `add epic`, then `add story --parent` |
| sprint-planning | `sprint new`, `sprint add` |
| sprint-status | `board`, `dashboard` |
| readiness | story has parent, points, acceptance, boundaries |

## Scrum and Kanban

Same statuses: `backlog`, `ready`, `in-progress`, `review`, `done`.

- Scrum assigns a sprint id.
- Kanban does not. Suggested limit: two stories in `in-progress`.

## What this repo refuses

- Product or customer data.
- Vendored copies of BMAD, Spec Kit, Sysl, or CALM. Those stay upstream (MIT / Apache-2.0). This repo is the operational layer that runs without them.
- Treating a written plan as proof the work is done.

## Apply it

```bash
python3 cli/mazu.py init
python3 cli/mazu.py add idea "Describe the change"
python3 cli/mazu.py add epic "First outcome" --parent IDEA-001
python3 cli/mazu.py add story "Smallest checkable slice" --parent EPIC-001 --points 3 \
  --acceptance "Given an empty store | When I add a story | Then list shows it" \
  --always "keep JSON valid" --ask-first "change the schema" --never "commit secrets"
python3 cli/mazu.py sprint new --goal "One slice is visible on the dashboard"
python3 cli/mazu.py sprint add --id US-001 --sprint S1
python3 cli/mazu.py dashboard
```

Open `mazu-data/dashboard.html`.
