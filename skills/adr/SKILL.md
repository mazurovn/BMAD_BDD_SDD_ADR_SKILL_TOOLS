---
name: adr-records
description: Record an architecture or process decision as an ADR. Use when a choice will be expensive to reverse.
---

# ADR

## When to write one

A choice constrains later work: storage, interface, workflow, or a methodology rule. Skip ADRs for trivia.

## Procedure

1. `python3 cli/mazu.py add adr "<decision title>" --description "<context in one paragraph>"`
2. Edit `mazu-data/adr/ADR-00N.md`. Fill Decision and Consequences. Leave Status as the store status.
3. Status meanings:
   - `backlog` / `ready` — proposed
   - `in-progress` — under discussion
   - `review` — waiting for acceptance
   - `done` — accepted
4. Supersede by adding a new ADR whose description names the old id. Do not delete the old file.

## Template

[templates/adr.md](../../templates/adr.md)

## Rule

If two stories disagree, the accepted ADR wins until a newer accepted ADR says otherwise.

## Rules
Operate under wiki/Rules.md. If this skill conflicts with a rule id, the rule wins and this skill is wrong.
