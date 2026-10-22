# Spec Delta

## Purpose

The upstream command runs a published methodology CLI and reports that program's own result, including a non-zero exit.

## ADDED Requirements

### Requirement: Pinned CLIs are executable

The kit SHALL expose the OpenSpec, CALM, and BMAD command-line tools at the versions recorded in the lockfile.

#### Scenario: Version is the pinned one

- **WHEN** the operator runs the upstream command for OpenSpec with `version`
- **THEN** the output contains `1.14.3` and the exit code is 0

#### Scenario: Missing install fails closed

- **WHEN** the OpenSpec binary is not installed
- **THEN** the command exits non-zero and names `npm ci --prefix upstream`

### Requirement: CALM documents pass the official validator

Architecture files shipped with the kit MUST be accepted by the published CALM CLI.

#### Scenario: Example architecture

- **WHEN** the operator validates `diagrams/calm/example.calm.json` with the CALM CLI
- **THEN** the validator reports no errors and exits 0
