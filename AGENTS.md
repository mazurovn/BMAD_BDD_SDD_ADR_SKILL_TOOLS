# AGENTS.md

This repository is a method kit, not an application.

- Start with ONBOARDING.md, methodology/MAZU-ADGILE.md, and methodology/MAZU-ADGILE.ru.md.
- Change backlog state only through `python3 cli/mazu.py`.
- Jira, YouTrack, CSV, and Excel go through `import` / `export` / `pull`. `pull` without tokens is a failure.
- Run `python3 scripts/audit.py` before calling the kit ready.
- Do not commit mazu-data/.
- Do not add product or customer data.
