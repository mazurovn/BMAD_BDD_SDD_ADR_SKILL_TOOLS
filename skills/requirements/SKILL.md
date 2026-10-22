---
name: requirements
description: Write a requirement that a story can trace to. Use EARS-style wording when a rule must be unambiguous.
---

# Requirements

## Forms

User story (value):

```
As a <role>
I want <capability>
so that <outcome>
```

EARS (rule):

```
When <trigger>, the system shall <response>.
While <state>, the system shall <response>.
If <unwanted event>, then the system shall <response>.
```

## Trace

```bash
python3 cli/mazu.py add requirement "Dashboard shows points and hours separately" \
  --parent EPIC-001 \
  --description "When the dashboard renders, the system shall show story points and logged hours in different fields."
```

Stories reference the requirement id in `--description` or as `--parent` when the parent is the requirement instead of an epic. Prefer epic as parent and name the requirement id in the description so the tree stays epic → story.

## Quality bar

A requirement is not ready if the reader cannot tell whether a build meets it. Rewrite until a Then line is possible.

## Rules
Operate under wiki/Rules.md. If this skill conflicts with a rule id, the rule wins and this skill is wrong.
