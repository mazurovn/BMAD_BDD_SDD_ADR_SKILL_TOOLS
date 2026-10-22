---
name: product-ideas
description: Capture an idea and promote it to an epic only when the outcome is clear.
---

# Ideas and epics

## Capture

```bash
python3 cli/mazu.py add idea "Allow agents to share one backlog format" \
  --description "Problem: each harness stores work differently. Outcome: one JSON store plus markdown specs."
```

An idea is not a commitment. Status stays `backlog` until someone writes the outcome in one sentence.

## Promote

```bash
python3 cli/mazu.py add epic "One backlog file" --parent IDEA-001 \
  --description "A new user can init, add a story, and open the HTML dashboard without extra services."
```

## Do not

- Do not turn a tool wishlist into an epic.
- Do not put project-specific customer data in this repository. Ideas here are about the method, or they live in the consumer project's `mazu-data/` which is gitignored.

## Rules
Operate under wiki/Rules.md. If this skill conflicts with a rule id, the rule wins and this skill is wrong.
