---
name: sdd-spec-driven
description: Write a spec before implementation. Includes Always / Ask First / Never boundaries.
---

# Spec-driven development

Inspired by GitHub Spec Kit phases (specify, plan, tasks, implement) and the Scrum Manager boundary pattern. This repo ships the procedure, not a copy of those projects.

## Layers

- Spec-first: write the spec, then build.
- Spec-anchored: keep the spec next to the work and update it when the requirement changes.
- This kit stops at spec-anchored. It does not treat the spec as generated source code.

## Procedure

1. Copy [templates/spec.md](../../templates/spec.md) into `mazu-data/specs/<id>.md`.
2. Fill goal, actors, out of scope, acceptance, and boundaries.
3. Register it: `python3 cli/mazu.py add requirement "<title>" --description "see mazu-data/specs/..."`.
4. Break the spec into stories only after the boundaries exist.
5. Implement one story. If the requirement changed, update the spec first, then re-slice. Do not silently edit the decision.

## Boundaries

| Level | Meaning | Default in this kit |
|---|---|---|
| Always | do without asking | keep `store.json` valid; add a test or a check for new behavior; follow accepted ADRs |
| Ask First | stop and ask | new dependency; schema change; public interface change; refactor outside the story |
| Never | do not do | commit secrets; delete history or failing checks to go green; edit another project's data into this repo |

Put the three lists on the story with `--always`, `--ask-first`, `--never` (use `|` between items).

## Done

The spec file exists, the requirement id exists, and every story names the spec.
