---
name: agile-delivery
description: Shape a backlog, split stories, plan a sprint, track a Kanban board, separate story points from hours.
---

# Agile delivery

Practices aligned with packs such as agile-delivery-skills (backlog grooming, story splitting, sprint goals, blockers, definition of done). Implemented here as CLI commands plus this checklist.

## Hierarchy

`idea → epic → story → task`

- Epic: outcome, not a task list.
- Story: one user-visible or one independently testable slice. Points required. Prefer 1–8. 13 means split. 21 means not ready.
- Task: optional step under a story. No points.

## Splitting

Split by workflow step, business rule, or data variation. Do not split by technical layer (all-UI then all-API) unless an ADR says the slice cannot be vertical.

## Scrum and Kanban

Both use the same statuses: `backlog`, `ready`, `in-progress`, `review`, `done`.

- Scrum: `sprint new --goal "..."`, then `sprint add --id US-001 --sprint S1`. A sprint goal is one sentence.
- Kanban: skip sprint assignment and read `python3 cli/mazu.py board`. Limit work in `in-progress` by agreement (default suggestion: 2 stories).

## Points vs time

| | Story points | Hours |
|---|---|---|
| Question | how big / how uncertain | how long it actually took |
| Command | `--points` | `log US-001 1.5 --note "..."` |
| Use | planning, velocity | cost, retro |

Velocity = sum of points of stories in that sprint with status `done`. The dashboard prints it. Do not convert points to hours.

## Definition of ready

Parent set, points set, at least one acceptance scenario, boundaries set.

## Definition of done

Acceptance evidence recorded, status `done`, hours logged if someone wants cost (optional), dashboard regenerated.

## Retro prompt

After a sprint, read `dashboard` and answer: what blocked movement to done, which 13+ stories should have been split, whether hours and points diverged in a way that changes the next goal. Do not invent metrics that are not in `store.json`.

## Rules
Operate under wiki/Rules.md. If this skill conflicts with a rule id, the rule wins and this skill is wrong.
