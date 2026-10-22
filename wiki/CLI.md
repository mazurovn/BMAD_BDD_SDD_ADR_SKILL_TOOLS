# CLI

```bash
python3 cli/mazu.py init
python3 cli/mazu.py add {idea|epic|story|task|requirement|adr} "title"
python3 cli/mazu.py list --kind story --status ready
python3 cli/mazu.py show US-001
python3 cli/mazu.py move US-001 in-progress
python3 cli/mazu.py log US-001 1.5 --note "slice"
python3 cli/mazu.py sprint new --goal "..."
python3 cli/mazu.py sprint add --id US-001 --sprint S1
python3 cli/mazu.py board
python3 cli/mazu.py dashboard
python3 cli/mazu.py doctor
```

Data: `mazu-data/store.json` (gitignored). Schema: `schemas/store.schema.json`.
