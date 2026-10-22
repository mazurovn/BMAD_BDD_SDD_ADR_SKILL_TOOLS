---
name: calm
description: Describe architecture as a FINOS CALM JSON document (nodes and relationships).
---

# CALM

Upstream: [finos/architecture-as-code](https://github.com/finos/architecture-as-code) and [calm.finos.org](https://calm.finos.org/). Apache-2.0. This kit ships a valid-shaped example, not the CALM CLI.

## When

You need a machine-readable picture of components and connections. Use Sysl when you also need endpoint behavior. Use both when both matter.

## Minimum document

See [diagrams/calm/backlog.calm.json](../../diagrams/calm/backlog.calm.json).

Required:
- `nodes[]` with `unique-id` and `node-type`
- `relationships[]` with `interacts` or `connects` (`source`, `destination`)

## Rules

- One node per component or actor. Stable `unique-id`.
- Do not put secrets, customer names, or project data in this repository's examples.
- If a relationship changes, update the CALM file in the same change as the ADR.

## Check

```bash
python3 -c "import json; json.load(open('diagrams/calm/backlog.calm.json'))"
```

Rendering needs the FINOS CALM CLI, which is optional. The JSON is the source of truth either way.
