---
name: bmad-method
description: Run MAZU-ADGILE through BMAD-style phases. Use for an idea, a change, epics, stories, or "what next".
---

# BMAD method

Upstream reference (do not vendor): [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD), MIT.

## When to use

The request is bigger than a one-line edit: new capability, unclear scope, or several stories.

## Roles

| Role | Does | Does not |
|---|---|---|
| Analyst | brief, options, risks | commit architecture |
| PO | outcome, priority, epic slice | write code |
| Architect | decisions, ADR, boundaries | invent product value |
| SM | sprint, board, blockers, points vs hours | change the decision |
| Dev | implement one story against the spec | widen scope |
| QA | Given/When/Then and evidence | mark done without a check |

## Phases

1. **Analysis.** Capture an idea: `python3 cli/mazu.py add idea "<title>" --description "..."`.
2. **Planning.** Write a spec from [templates/spec.md](../../templates/spec.md). Add requirements: `add requirement`.
3. **Solutioning.** Record each hard choice as ADR. Slice epics, then stories with Fibonacci points and acceptance lines.
4. **Readiness.** A story is ready only if it has a parent epic, points in {1,2,3,5,8,13,21}, at least one acceptance line, and boundaries (Always / Ask First / Never). If any are missing, stop.
5. **Implementation.** `sprint new`, `sprint add`, `move` through `ready → in-progress → review → done`. Log hours with `log`. Points are not hours.

## Workflow map (BMAD v6 names, local commands)

| Upstream workflow | Local action |
|---|---|
| create-epics-and-stories | `add epic` then `add story --parent EPIC-00N` |
| sprint-planning | `sprint new` + `sprint add` |
| sprint-status | `board` and `dashboard` |
| decision record | `add adr` (writes `mazu-data/adr/ADR-00N.md`) |

## Output

Leave the store, the ADR file, and `mazu-data/dashboard.md` updated. Do not invent project facts that are not in the store or the user's message.

## Rules
Operate under wiki/Rules.md. If this skill conflicts with a rule id, the rule wins and this skill is wrong.
