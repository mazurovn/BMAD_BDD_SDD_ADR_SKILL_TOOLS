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

Tests: `python3 -m pytest -q` if pytest is installed, or run `python3 tests/test_mazu.py` only through pytest because the tests use pytest fixtures.
