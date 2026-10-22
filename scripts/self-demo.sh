#!/bin/sh
# Rebuild the kit-self demo from the CLIs in this repo. No network.
set -eu
cd "$(dirname "$0")/.."
rm -rf mazu-data openspec/changes/self-demo
python3 cli/mazu.py project new kit-self >/dev/null
python3 cli/mazu.py project use kit-self >/dev/null
IDEA=$(python3 cli/mazu.py add idea "Прогнать CLI этого репозитория без скачивания")
EPIC=$(python3 cli/mazu.py add epic "От идеи до улики на доске" --parent "$IDEA")
add_story() {
  python3 cli/mazu.py add story "$1" --parent "$EPIC" --points "$2" \
    --acceptance "Given the repository When $3 Then the exit code is 0" \
    --always "run the binary already in bin" \
    --ask-first "change a published schema" \
    --never "download a package"
}
US_OS=$(add_story "OpenSpec печатает свою версию" 2 "openspec --version runs")
US_CALM=$(add_story "CALM принимает пример архитектуры" 3 "calm validate runs")
US_BMAD=$(add_story "BMAD печатает свою версию" 2 "bmad --version runs")
US_CUC=$(add_story "Cucumber выполняет сценарий гейта" 3 "cucumber runs the feature")
US_SYSL=$(add_story "Sysl принимает пример модели" 3 "sysl validate runs")
US_SPEC=$(add_story "Specify печатает свою версию" 2 "specify version runs")
US_ADR=$(add_story "adr-tools показывает команды" 1 "adr help runs")
python3 cli/mazu.py add requirement "Бинарники и скрипты лежат в репозитории" --parent "$EPIC" --description "bin and upstream, no download"
ADR=$(python3 cli/mazu.py add adr "Держать CLI внутри репозитория" --description "A checkout must run the CLIs without a package download." --decision "Keep the CLIs in bin and upstream." --consequences "- Positive: offline doctor and release work\n- Negative: binaries must stay pinned in-repo")
python3 cli/mazu.py check adr "$ADR"
python3 cli/mazu.py sprint new --goal "Показать прогон всех CLI на доске kit-self"
for id in $US_OS $US_CALM $US_BMAD $US_CUC $US_SYSL $US_SPEC $US_ADR; do
  python3 cli/mazu.py gate ready "$id"
  python3 cli/mazu.py sprint add --id "$id" --sprint S1
done
python3 cli/mazu.py workflow epics --idea "$IDEA" --epic "$EPIC"
python3 cli/mazu.py workflow sprint --sprint S1
python3 cli/mazu.py gate sprint S1
prove() {
  id=$1
  shift
  python3 cli/mazu.py move "$id" in-progress
  python3 cli/mazu.py log "$id" 0.2 --note "$*"
  python3 cli/mazu.py evidence "$id" --run "$@"
  python3 cli/mazu.py move "$id" review
  python3 cli/mazu.py gate done "$id"
  python3 cli/mazu.py move "$id" done
}
prove "$US_OS" bin/openspec --version
prove "$US_CALM" bin/calm validate --architecture diagrams/calm/example.calm.json --format json
prove "$US_BMAD" bin/bmad --version
prove "$US_CUC" bin/cucumber examples/bdd/gate.feature --require examples/bdd/steps.js
prove "$US_SYSL" bin/sysl validate diagrams/sysl/example.sysl
prove "$US_SPEC" bin/specify version
prove "$US_ADR" bin/adr help
python3 cli/mazu.py openspec propose self-demo --intent "Show this repository's own CLI run on the dashboard"
python3 cli/mazu.py upstream openspec -- validate self-demo --strict
python3 cli/mazu.py upstream openspec -- validate bind-upstreams --strict
python3 cli/mazu.py probe
python3 cli/mazu.py dashboard >/tmp/self-demo-dash.txt
mkdir -p docs/demo
cp mazu-data/projects/kit-self/dashboard.html docs/demo/self-dashboard.html
cp mazu-data/projects/kit-self/store.json docs/demo/kit-self-store.json
echo "SELF_DEMO_OK idea=$IDEA epic=$EPIC"
