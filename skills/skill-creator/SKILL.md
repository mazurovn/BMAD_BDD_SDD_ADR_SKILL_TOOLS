---
name: skill-creator
description: Create a new MAZU skill skeleton with frontmatter, procedure, commands, and boundaries.
---

# Skill creator

## When

A repeated procedure is not covered by an existing skill.

## Procedure

1. Read two nearby skills so the new one matches their shape.
2. Run `python3 cli/mazu.py skill new <slug> --title "..." --description "When to use this skill."`
3. Fill When, Procedure, Commands, and Boundaries in `skills/<slug>/SKILL.md`.
4. Add a role under `agents/` only if a person would hold that job.
5. Add the file to `scripts/audit.py` only if the kit cannot run without it.
6. Run `python3 scripts/audit.py`.

## Boundaries

Always: YAML frontmatter with `name` and `description`.
Ask First: change an existing skill's public procedure.
Never: copy a third-party repository into this one. Link it from docs/SOURCES.md.

## Rules
Operate under wiki/Rules.md. If this skill conflicts with a rule id, the rule wins and this skill is wrong.
