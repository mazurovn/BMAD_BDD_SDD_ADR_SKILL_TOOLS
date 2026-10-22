Kimi CLI reads AGENTS.md. Paste this if there is a separate system prompt.

# MAZU rules

Follow wiki/Rules.md. State is only `python3 cli/mazu.py`.

BMAD-1 phases in order. BMAD-4 no second backlog in chat.
SDD-1 spec before code. SDD-2 change the spec before widening a story.
BOUND-1 Always: valid store, a check for new behavior, accepted ADR.
BOUND-2 Ask First stops: new dependency, schema change, public command, edit outside the story, blending the three architecture layers.
BOUND-3 Never: secrets, deleting history, deleting a check to go green, client backlog in this repo, a sync you did not run.
BDD-1 Then is observable. BDD-4 done only with evidence.
ADR-4 supersede, do not delete.
EST-1 points are not hours. EST-2 Fibonacci only.
EPIC-2 a 13 is split, a 21 is not ready. SPRINT-3 velocity is done story points only.
SYSL-1 behavior. CALM-1 structure. They do not replace each other.
ARCH-1 business capabilities. ARCH-2 system ownership. ARCH-3 the contract other teams build. ARCH-4 the chair routes, it does not merge the layers.
DEV-1 walk the ladder and stop at the first rung that fully works. DEV-2 do not cut trust-boundary checks. DEV-4 name what you did not check.
PERF-1 one role question per pass.
