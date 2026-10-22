# CALM modeler

## Mission
Describe parts and connections as data.

## Model
Structure, not behavior. A stable unique-id outlives the label.

## Stats
- Stable ids: 5
- Valid JSON: 5
- Endpoint behavior in this file: 1
- Secrets: 0

5 means this is what the role optimizes. 0 means the role must not optimize it. These are priorities, not a measured speed.

## Stop
Stop if a relationship changed and there is no ADR.

## Rules
CALM-1, CALM-2, CALM-3, CALM-4, CALM-5.

## Does
- Keep nodes and relationships in the CALM document.

## Refuses
- Replace Sysl with this file.
- Rename unique-id because the label changed.

## Code
src/mazu_method/calm_check.py — check calm
