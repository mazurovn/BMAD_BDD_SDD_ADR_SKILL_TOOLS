# Setup

Requirements: Python 3.11+.

```bash
git clone https://github.com/mazurovn/BMAD_BDD_SDD_ADR_SKILL_TOOLS.git
cd BMAD_BDD_SDD_ADR_SKILL_TOOLS
python3 cli/mazu.py doctor
python3 cli/mazu.py init
python3 cli/mazu.py dashboard
```

Optional: `bash scripts/install.sh` copies skills into `.claude/skills` and `.agents/skills` in this clone.

Tests need pytest on the same interpreter as the CLI:

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pytest -q
```

`python3 cli/mazu.py doctor` prints `pytest: available` or `pytest: missing`. Release and `python3 cli/mazu.py audit` expect a working pytest for the full gate set.

## Specify (`upstream/py`)

`bin/specify` needs `upstream/py` (a local Python env with `specify_cli`). That tree was present in the published v1.3.0 zip but is **not** in git (`upstream/py/.gitignore` is `*`). A fresh clone therefore fails `probe`, `test_every_shipped_cli_runs`, `self-demo`, and `release` at specify.

**Ask First:** vendoring `upstream/py` into git (new large dependency / binary tree) or adding a network install step. Until that decision, doctor prints `specify: missing upstream/py`.
