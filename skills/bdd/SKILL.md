---
name: bdd-acceptance
description: Write acceptance as Given / When / Then and attach it to a story.
---

# BDD acceptance

## Format

One scenario per line group, stored in the story `acceptance` array. Separate scenarios with `|` on the CLI.

```
Given <context>
When <action>
Then <observable result>
```

## Rules

- The Then line is something a person or a test can check. No "works well".
- Cover the happy path and one failure or empty case before calling the story ready.
- Do not hide implementation steps ("call function X") unless the story is a technical enabler. Say so in the title.
- Points measure complexity. They are not the Then clause.

## CLI

```bash
python3 cli/mazu.py add story "Sign in" --parent EPIC-001 --points 3 \
  --acceptance "Given a known user | When they submit valid credentials | Then the session starts | Given unknown credentials | When they submit | Then no session starts and the reason is generic"
```

## Review

QA does not move a story to `done` until each acceptance line has evidence: a command output, a test name, or an explicit human check recorded in the description.
