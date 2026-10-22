---
name: sprint-planning
description: Plan a sprint from ready stories, or run the same board as Kanban without a sprint.
---

# Sprint planning

This is the local form of the BMAD workflow sprint-planning.

## Scrum

1. `python3 cli/mazu.py board` and keep only stories in `ready`.
2. `sprint new --goal "one sentence"`.
3. `sprint add --id US-001 --sprint S1` for each chosen story. A backlog story becomes `ready` when added.
4. Capacity is a conversation, not a formula. Points are complexity. Do not convert them to hours during planning.
5. `dashboard` shows velocity only for stories in that sprint whose status is `done`.

## Kanban

Skip `sprint add`. Move cards with `move ID in-progress`. Suggested limit: two stories in `in-progress`.

## During the sprint

Dev moves `ready → in-progress → review` and logs hours.
QA moves `review → done` only when every acceptance line has evidence.
The interactive board is `python3 cli/mazu.py serve`.

## Rules
Operate under wiki/Rules.md. If this skill conflicts with a rule id, the rule wins and this skill is wrong.
