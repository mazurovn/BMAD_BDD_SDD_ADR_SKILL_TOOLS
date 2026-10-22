# Setup

Requirements: Python 3.11+ (system). Specify uses the vendored CPython 3.12 under `upstream/cpython`.

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

`python3 cli/mazu.py doctor` prints `pytest: available` or `pytest: missing`. Release and `python3 cli/mazu.py audit` expect a working pytest for the full gate set. Doctor also requires vendored `upstream/py` (specify_cli) and exits non-zero if it is absent.

## Specify (`upstream/py`)

`bin/specify` loads `specify_cli` from `upstream/py/lib/python3.12/site-packages` on `upstream/cpython` (see `upstream/bin/specify`). That tree is **vendored in git** (~138 MiB, ~2170 files), reconstructed from the published v1.3.0 release zip so a fresh clone can run `specify` / `probe` / pytest CLI checks / `self-demo` / `release` without undocumented pip installs.

| Item | Value |
|---|---|
| Size (approx.) | ~138 MiB on disk |
| Primary package | `specify-cli` 1.2.3 (MIT, GitHub Spec Kit) |
| Other wheels | transitive deps of specify-cli (click, pydantic, mcp, cryptography, …) — each keeps its own license under `*.dist-info` |
| Python runtime | `upstream/cpython` 3.12.15 (already in-tree); `upstream/py/bin/python*` is a duplicate venv interpreter from the zip |

See also `wiki/SETUP.md` and `docs/SOURCES.md`.

## Diagram validators

Release runs both:

1. In-house lint: `python3 cli/mazu.py check sysl|calm …`
2. Upstream: `bin/sysl validate …` and `bin/calm validate --architecture … --format json`

Fail closed: either non-zero stops the archive.
