# self-demo delta spec

## ADDED Requirements

### Requirement: Observable outcome
The system MUST make this outcome observable: Show this repository's own CLI run on the dashboard

#### Scenario: success
- **WHEN** the operator finishes the slice for self-demo
- **THEN** Show this repository's own CLI run on the dashboard
- GIVEN the change self-demo is proposed

#### Scenario: refusal
- **WHEN** archive is requested and a task has no evidence
- **THEN** the command exits non-zero and the change stays active
- GIVEN a task has no evidence
