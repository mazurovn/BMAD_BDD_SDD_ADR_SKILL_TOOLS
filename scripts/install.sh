#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .claude/skills .agents/skills
for skill in skills/*; do
  name="$(basename "$skill")"
  rm -rf ".claude/skills/$name" ".agents/skills/$name"
  mkdir -p ".claude/skills/$name" ".agents/skills/$name"
  cp "$skill/SKILL.md" ".claude/skills/$name/SKILL.md"
  cp "$skill/SKILL.md" ".agents/skills/$name/SKILL.md"
done
python3 cli/mazu.py doctor
echo "skills copied for Claude and generic agents"
