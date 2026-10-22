## Context

Published CLIs already exist. Re-implementing propose, validate, and architecture checks under the same names hid the difference.

## Goals / Non-Goals

- Goals: run the published binaries, keep their package source in git, and fail when the install is absent.
- Non-goals: committing `node_modules` (344 MB, including mermaid and Playwright), and pretending `apply` writes product code.

## Decisions

- `upstream/package-lock.json` pins the three packages. `npm ci --prefix upstream` recreates `node_modules`.
- `upstream/packages/` holds the package trees themselves so the source is in git even when dependencies are not.
- `python3 cli/mazu.py upstream <tool> -- <args>` execs `upstream/node_modules/.bin/<tool>` and returns its exit code.
- CALM examples use the 1.2 schema shape (`name`, `description`, `relationship-type.interacts.actor/nodes`) because that is what `@finos/calm-cli` 1.65.0 enforces.
- Official skills are the ones `openspec init` writes into `.agents`, `.claude`, `.grok`, `.opencode`, `.qwen`, `.kimi-code`, and `.gigacode`. They are not rewritten.

## Risks / Trade-offs

- A fresh clone does not run the CLIs until `npm ci --prefix upstream`. The command says so and exits non-zero. That is the install, not a fake success.
- Sysl has no Go toolchain in this environment, so no sysl compiler binary is claimed.

## Migration Plan

Existing `check calm` remains a structural check. Official acceptance is `upstream calm -- validate --architecture <file>`.

## Open Questions

None for this change. A Sysl release binary is a separate change.
