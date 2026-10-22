# Proposal

## Why

The kit claimed OpenSpec, CALM, and BMAD while shipping only its own checkers. A command that does not execute the published CLI is not that CLI.

## What Changes

- Pin and run `@fission-ai/openspec` 1.14.3, `@finos/calm-cli` 1.65.0, and `bmad-method` 6.12.4.
- Keep the published package trees under `upstream/packages/` and install their dependencies with `npm ci --prefix upstream`.
- Add `mazu upstream`, which executes those binaries and returns their stdout and exit code.
- Replace the example CALM documents so the official `calm validate` accepts them.
- Install the official OpenSpec skills into the agent directories the CLI itself generates.

## Capabilities

### New Capabilities

- `upstream-cli`: Run a pinned upstream CLI and surface its real result.

### Modified Capabilities

- None.

## Impact

- New dependency lockfile in `upstream/package-lock.json`.
- `upstream/node_modules/` stays untracked because it is hundreds of megabytes.
- Agents must call `python3 cli/mazu.py upstream` instead of inventing a pass.
