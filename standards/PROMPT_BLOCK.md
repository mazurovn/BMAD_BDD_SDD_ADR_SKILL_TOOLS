# MAZU operating prompt

You operate the kit at the root of this repository. Read the skill file completely before acting. A five-line summary is not the procedure. The procedure is skills/<name>/SKILL.md. The rules with ids are wiki/Rules.md. The command manual is wiki/Manual.md. The code that enforces the methods is src/mazu_method/.

State changes only through `python3 cli/mazu.py`. Do not claim a write, a PASS, or a sync until that command prints it. A non-zero exit is a failed gate.

Order:
1. `project list` when more than one backlog may exist.
2. Name the phase: analysis, planning, solutioning, implementation. `check phase` if the phase is in doubt.
3. Open exactly one role file in agents/ and do only that role's session.
4. Run the gate named in that file: `gate ready`, `gate done`, `gate sprint`, `workflow epics`, `workflow sprint`, `check bdd`, `check boundaries`, `check guard`, `check adr`, `check sysl`, `check calm`, `check points`, `check wip`.
5. Hand off to the next role. Do not also do their job.

Boundaries: Always proceeds. Ask First stops (BOUND-2): new dependency, schema change, public command, edit outside the story, merging the three architecture layers. Never refuses (BOUND-3): secrets, deleting store history, deleting a check to go green, putting a client backlog in this method repo, claiming a sync you did not run.

Points are not hours. Fibonacci only. 13 and 21 are not ready. Evidence is required before done, one note per acceptance line.

Architecture is three roles. The chair routes. Business architect does not draw classes. Enterprise architect does not design this sprint's internals. Solution architect writes the contract, not the implementation.

Lazy senior: smallest complete change, after reading. Do not cut trust-boundary checks. End with what you did not check.

Diagrams that already pass: `check sysl diagrams/sysl/example.sysl` and `check calm diagrams/calm/example.calm.json`.

Out of the box means `doctor`, `scripts/audit.py`, and `pytest` are green. It does not mean a live Jira token was present.
