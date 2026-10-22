#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 cli/mazu.py doctor
tmpdir="$(mktemp -d)"
(
  cd "$tmpdir"
  python3 "$OLDPWD/cli/mazu.py" init
  python3 "$OLDPWD/cli/mazu.py" add idea "Smoke"
  python3 "$OLDPWD/cli/mazu.py" add epic "Smoke epic" --parent IDEA-001
  python3 "$OLDPWD/cli/mazu.py" add story "Smoke story" --parent EPIC-001 --points 2 \
    --acceptance "Given smoke | When run | Then dashboard exists" \
    --always "valid json" --never "secrets"
  python3 "$OLDPWD/cli/mazu.py" sprint new --goal "smoke"
  python3 "$OLDPWD/cli/mazu.py" sprint add --id US-001 --sprint S1
  python3 "$OLDPWD/cli/mazu.py" log US-001 0.25 --note smoke
  python3 "$OLDPWD/cli/mazu.py" move US-001 done
  python3 "$OLDPWD/cli/mazu.py" dashboard
  test -f mazu-data/dashboard.html
  python3 -c "import json; json.load(open('mazu-data/store.json'))"
)
rm -rf "$tmpdir"
python3 -c "import json; json.load(open('diagrams/calm/backlog.calm.json'))"
echo "smoke ok"
