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
