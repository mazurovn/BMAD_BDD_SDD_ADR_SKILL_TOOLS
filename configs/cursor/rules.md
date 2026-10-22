Cursor project rules.

# MAZU rules

Follow wiki/Manual.md and wiki/Rules.md. State is only `python3 cli/mazu.py`. The methods are code in src/mazu_method/, not only text.

Before a story is ready: `gate ready ID`. It checks the parent, Fibonacci points 1-8, Given/When/Then, and Always/Ask First/Never.
Before done: `evidence` for every scenario, then `gate done ID`.
Before a sprint: `workflow sprint --sprint S1`.
Before an epic is called sliced: `workflow epics --idea IDEA --epic EPIC`.
Boundaries: `check guard "action" --ask "..." --never "..."`. Ask First stops. Never refuses.
Diagrams: `check sysl FILE` and `check calm FILE`.
Points and hours: `check points ID`. Do not add them together.
Phases: `check phase implementation --outcome "..." --has-boundaries --has-check`.
A non-zero exit is a failed gate. Do not say the work passed.

BMAD-1 phases in order. SDD-1 spec before code.
BOUND-3 Never: secrets, deleting history, deleting a check to go green, client backlog in this repo.
DEV-1 smallest complete change. DEV-2 do not cut a trust-boundary check. DEV-4 name what you did not check.
ARCH-4 the chair routes business, enterprise, and solution architects. Do not merge the three layers.
