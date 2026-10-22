# Harnesses

Any agent that can read a file and run `python3 cli/mazu.py` can use this repo.

| Harness | What it reads |
|---|---|
| Claude Code | `CLAUDE.md`, `skills/` |
| Codex | `AGENTS.md`, `configs/codex/PROMPT.md` |
| Qwen Code | `QWEN.md` and `AGENTS.md` |
| OpenCode | `opencode.json`, `.opencode/agent/mazu.md`, `AGENTS.md` |
| Kimi CLI | `AGENTS.md`, `configs/kimi/PROMPT.md` |
| GPT | `configs/gpt/PROMPT.md`, `tools/openai.json` |
| DeepSeek | `configs/deepseek/PROMPT.md`, `tools/openai.json` |
| GigaChat | `configs/gigachat/PROMPT.md`, `tools/gigachat.json` |
| GigaCode | `configs/gigacode/PROMPT.md` (paste; no verified project filename) |
| Grok | `configs/grok/prompt.md` |
| Grok bot | `configs/grok-bot/PROMPT.md`, `agents/catalog.json` |

Tool loop: `skills/tool-calling/SKILL.md`.

Roles: eleven files in `agents/`. The four Grok bots stay the expert bots. The other roles are prompts.
