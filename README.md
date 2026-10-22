# BMAD_BDD_SDD_ADR_SKILL_TOOLS

Method kit for BMAD, SDD, BDD, ADR, Sysl, CALM, and agile delivery.
Python 3.11+. No services. No product data.

## Start

```bash
git clone https://github.com/mazurovn/BMAD_BDD_SDD_ADR_SKILL_TOOLS.git
cd BMAD_BDD_SDD_ADR_SKILL_TOOLS
python3 cli/mazu.py doctor
bash scripts/smoke.sh
```

Read [methodology/MAZU-ADGILE.md](methodology/MAZU-ADGILE.md) and [ONBOARDING.md](ONBOARDING.md).

## Layout

| Path | What |
|---|---|
| `cli/mazu.py` | Projects, backlog, sprints, hours, Kanban, dashboard, CSV/xlsx, Jira/YouTrack |
| `skills/` | Procedures, including skill-creator and backlog connectors |
| `agents/` | Eleven roles plus the four Grok expert bots |
| `tools/` | OpenAI tool schema and GigaChat functions |
| `configs/` | GPT, Codex, DeepSeek, Kimi, GigaChat, GigaCode, Grok, Grok bot |
| `templates/` | ADR, spec, story, epic, boundaries |
| `diagrams/sysl` | Sysl behavior spec |
| `diagrams/calm` | FINOS CALM structure spec |
| `methodology/` | MAZU-ADGILE |
| `wiki/` | Short references |
| `configs/` | Claude, Cursor, Grok |
| `schemas/store.schema.json` | Store shape |
| `scripts/smoke.sh` | Out-of-the-box check |

`mazu-data/` is created locally and gitignored.

## License

MIT for this kit. Upstream projects stay in their repos; see [docs/SOURCES.md](docs/SOURCES.md).
