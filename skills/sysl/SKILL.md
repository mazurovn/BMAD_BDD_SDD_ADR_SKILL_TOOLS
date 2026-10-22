---
name: sysl
description: Describe a system as a Sysl specification so sequence and integration views can be generated later.
---

# Sysl

Upstream: [anz-bank/sysl](https://github.com/anz-bank/sysl), Apache-2.0. This kit does not ship the Sysl compiler. It ships a spec style and an example.

## When

You need endpoints, types, and who calls whom — before or beside a CALM diagram.

## Minimum spec

See [diagrams/sysl/backlog.sysl](../../diagrams/sysl/backlog.sysl).

## Rules

- One application block per deployable or actor.
- Name the endpoint and the return type.
- Do not paste secrets or environment-specific hosts.
- If behavior changes, update the `.sysl` file in the same change as the ADR.

## Render

If `sysl` is installed locally:

```bash
sysl sd --output out.png diagrams/sysl/backlog.sysl
```

If it is not installed, keep the `.sysl` as the source of truth and say the diagram was not rendered.
