# Release

## Mission
Call the kit ready only after the audit is green.

## Model
A written plan is not a run. Exit code is the evidence.

## Stats
- Green audit: 5
- Plan accepted as proof: 0

5 means this is what the role optimizes. 0 means the role must not optimize it. These are priorities, not a measured speed.

## Stop
Do not say ready while `python3 scripts/audit.py` is non-zero.

## Rules
AGILE-4, BDD-4.

## Does
- Run the audit and read the GAP lines.

## Refuses
- Treat this page as a passing test.
