#!/usr/bin/env bash
# Example only. Run from a scratch directory. See methodology/MAZU-ADGILE.md.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/cli/mazu.py" init
python3 "$ROOT/cli/mazu.py" add idea "Practice the method"
python3 "$ROOT/cli/mazu.py" add epic "First visible slice" --parent IDEA-001
python3 "$ROOT/cli/mazu.py" add requirement "Dashboard separates points and hours" --parent EPIC-001
python3 "$ROOT/cli/mazu.py" add story "Show one story on the dashboard" --parent EPIC-001 --points 3 \
  --acceptance "Given one story | When I open the dashboard | Then points and hours are separate columns" \
  --always "keep store json valid" --ask-first "change schema" --never "commit secrets"
python3 "$ROOT/cli/mazu.py" add adr "JSON file is the backlog store"
python3 "$ROOT/cli/mazu.py" sprint new --goal "Dashboard shows the story"
python3 "$ROOT/cli/mazu.py" sprint add --id US-001 --sprint S1
python3 "$ROOT/cli/mazu.py" log US-001 0.5 --note "example"
python3 "$ROOT/cli/mazu.py" dashboard
