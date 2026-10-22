---
name: projects
description: Keep more than one local backlog under mazu-data/projects without mixing them.
---

# Projects

```bash
python3 cli/mazu.py project new alpha
python3 cli/mazu.py project list
python3 cli/mazu.py project use alpha
python3 cli/mazu.py add story "First slice" --points 3
python3 cli/mazu.py dashboard
```

`project use` switches `mazu-data/active-project`. Each project has its own store, ADR folder, and dashboard. With no pointer, the CLI uses `mazu-data/store.json`.

`mazu-data/` is gitignored. Do not commit a client backlog into the method repository.

## Rules
Operate under wiki/Rules.md. If this skill conflicts with a rule id, the rule wins and this skill is wrong.
