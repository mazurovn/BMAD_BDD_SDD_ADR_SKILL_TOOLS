---
name: create-epics-and-stories
description: Slice an idea into one epic and checkable stories with points, acceptance, and boundaries.
---

# Create epics and stories

This is the local form of the BMAD workflow create-epics-and-stories.

## Procedure

1. One idea with a one-sentence outcome: `python3 cli/mazu.py add idea "..." --description "..."`.
2. One epic for the first outcome, not for a department: `add epic "..." --parent IDEA-001`.
3. Stories are vertical slices. Each story gets:
   - `--parent EPIC-001`
   - `--points` of 1, 2, 3, 5, or 8. Use 13 only to mark a split. Do not leave 21 in a sprint.
   - `--acceptance` with at least one Given / When / Then. Separate scenarios with `|`.
   - `--always`, `--ask-first`, `--never` when the story has a rule of its own.
4. Tasks are optional steps under a story: `add task "..." --parent US-001`. Tasks do not get points.
5. A story is not ready until parent, points, and acceptance exist. `move US-001 ready` is the SM's action after that check.

## Do not

Do not write hours into `--points`. Hours are `log` after work starts.
Do not create an epic per technical layer.

## Rules
Operate under wiki/Rules.md. If this skill conflicts with a rule id, the rule wins and this skill is wrong.
