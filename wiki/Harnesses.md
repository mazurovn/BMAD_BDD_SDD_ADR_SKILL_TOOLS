# Harnesses

Any agent that can read a file can use this repo.

1. Read [ONBOARDING.md](../ONBOARDING.md).
2. Read the skill under `skills/<name>/SKILL.md` for the job.
3. Read the role under `agents/`.
4. Run `python3 cli/mazu.py` for state. Do not keep a second backlog in chat.

| Harness | Config |
|---|---|
| Claude | configs/claude/skills.json and `.claude/skills` via `scripts/install.sh` |
| Cursor | configs/cursor/rules.md |
| Codex / other | AGENTS.md |
| Grok | configs/grok/prompt.md plus the four bots in agents/catalog.json |

Subagents are the six files in `agents/`. They are prompts, not separate runtimes.
