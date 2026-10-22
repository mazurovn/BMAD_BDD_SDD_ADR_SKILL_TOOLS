---
name: tool-calling
description: Call MAZU through OpenAI-style tool schemas and GigaChat functions.
---

# Tool calling

- `tools/openai.json` — GPT, Codex, DeepSeek, Kimi, Grok, OpenCode, Qwen, when the harness speaks OpenAI tools.
- `tools/gigachat.json` — GigaChat `functions`. Flat parameters. No union types.

## Loop

1. Send the schema with the user message.
2. If the model returns a function call, run `python3 cli/mazu.py` with those arguments. Do not answer as if the command ran.
3. Send stdout back as the tool result.
4. GigaChat: when `finish_reason` is `function_call`, return a message with role `function`.

Ask First still applies. A tool result does not cancel a boundary.
