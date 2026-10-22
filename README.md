# BMAD_BDD_SDD_ADR_SKILL_TOOLS

Method kit for BMAD, SDD, BDD, ADR, Sysl, CALM, and agile delivery.
Python 3.11+. No services. No product data.

## Start

```bash
git clone https://github.com/mazurovn/BMAD_BDD_SDD_ADR_SKILL_TOOLS.git
cd BMAD_BDD_SDD_ADR_SKILL_TOOLS
python3 cli/mazu.py doctor
python3 cli/mazu.py check sysl diagrams/sysl/example.sysl
python3 cli/mazu.py check calm diagrams/calm/example.calm.json
bash scripts/smoke.sh
```

Read [methodology/MAZU-ADGILE.md](methodology/MAZU-ADGILE.md) and [ONBOARDING.md](ONBOARDING.md).

## Layout

| Path | What |
|---|---|
| `cli/mazu.py` | Backlog, gates, checks, workflows, dashboard, import |
| `src/mazu_method/` | BMAD, SDD boundaries, BDD, ADR, agile, points, Sysl, CALM |
| `skills/` | Procedures the agents follow |
| `agents/` | Roles, including three architects and the lazy senior |
| `diagrams/sysl` | Behavior diagrams checked by `mazu check sysl` |
| `diagrams/calm` | Structure diagrams checked by `mazu check calm` |
| `wiki/Manual.md` | How to apply every command |
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
