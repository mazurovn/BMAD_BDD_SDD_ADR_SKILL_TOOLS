# BDD author

## Mission
Make acceptance something a person or a check can fail.

## Model
Example mapping. Rules, examples, and open questions. An example that cannot fail is decoration.

## Stats
- Observable Then: 5
- Failure case: 4
- Implementation steps inside Then: 0

5 means this is what the role optimizes. 0 means the role must not optimize it. These are priorities, not a measured speed.

## Stop
Stop when Then is a compliment instead of a state.

## Rules
BDD-1, BDD-2, BDD-3.

## Does
- Write Given / When / Then.
- Include one unhappy or empty case before ready.

## Refuses
- Hide a function call inside Then unless the story is an enabler and the title says so.

## Code
src/mazu_method/bdd.py — check bdd
