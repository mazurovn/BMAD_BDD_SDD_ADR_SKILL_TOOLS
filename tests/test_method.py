import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
CLI = [sys.executable, str(ROOT / "cli" / "mazu.py")]

from mazu_method.bdd import scenario_issues
from mazu_method.calm_check import issues as calm_issues
from mazu_method.estimation import classify_points
from mazu_method.sdd import decide, guard, merge
from mazu_method.sysl_check import issues as sysl_issues


def test_points_and_boundaries_and_bdd():
    assert classify_points(4) == "invalid"
    assert classify_points(13) == "split"
    assert classify_points(5) == "ok"
    assert scenario_issues("Given a user When they save Then the row exists") == []
    assert any("not observable" in issue for issue in scenario_issues("Given a When b Then works well"))
    rules = {"always": ["valid store"], "ask_first": ["new dependency"], "never": ["commit secrets"]}
    assert decide("commit secrets now", rules) == "never"
    assert guard("add a new dependency", rules).startswith("BOUND-2")
    assert "commit secrets" in merge(rules, {"never": []})["never"]
    # Synonym cover: paraphrase must still hit Never / Ask First; reverse substring must not.
    assert decide("push credentials to git", rules) == "never"
    assert guard("push credentials to git", rules).startswith("BOUND-3")
    assert decide("install a package from pip", rules) == "ask_first"
    assert decide("e", {"never": ["commit secrets"]}) == "unspecified"
    assert decide("refactor the dashboard layout", rules) == "unspecified"


def test_documented_guard_examples_stop():
    import re
    import shlex

    pattern = re.compile(r'check guard "[^"]+"(?: --(?:always|ask|never) "[^".]+")+')
    examples = set()
    for path in list((ROOT / "agents").glob("*.md")) + list((ROOT / "skills").glob("*/SKILL.md")):
        examples.update(pattern.findall(path.read_text(encoding="utf-8")))
    assert examples
    for example in sorted(examples):
        argv = shlex.split(example)
        if "--ask" not in argv and "--never" not in argv:
            continue
        proc = subprocess.run(CLI + argv, text=True, capture_output=True)
        assert proc.returncode != 0, example


def test_documented_failing_examples_fail():
    import re
    import shlex

    pattern = re.compile(r"`python3 cli/mazu\.py ([^`]+)` ожидаемо падает")
    examples = set()
    for path in list((ROOT / "agents").glob("*.md")) + list((ROOT / "skills").glob("*/SKILL.md")):
        examples.update(pattern.findall(path.read_text(encoding="utf-8")))
    assert examples
    for example in sorted(examples):
        proc = subprocess.run(CLI + shlex.split(example), text=True, capture_output=True)
        assert proc.returncode != 0, example
    filled = subprocess.run(CLI + ["check", "phase", "planning", "--outcome", "One outcome"], text=True, capture_output=True)
    assert filled.returncode == 0 and filled.stdout.strip() == "PASS"


def test_diagrams_pass():
    assert sysl_issues((ROOT / "diagrams/sysl/example.sysl").read_text(encoding="utf-8")) == []
    assert calm_issues((ROOT / "diagrams/calm/example.calm.json").read_text(encoding="utf-8")) == []
    assert sysl_issues((ROOT / "diagrams/sysl/backlog.sysl").read_text(encoding="utf-8")) == []
    assert calm_issues((ROOT / "diagrams/calm/backlog.calm.json").read_text(encoding="utf-8")) == []


def test_cli_workflow_and_checks(tmp_path):
    subprocess.run(CLI + ["init"], cwd=tmp_path, check=True)
    subprocess.run(CLI + ["add", "idea", "One outcome"], cwd=tmp_path, check=True)
    subprocess.run(CLI + ["add", "epic", "First slice", "--parent", "IDEA-001"], cwd=tmp_path, check=True)
    story = [
        "add", "story", "Save the row", "--parent", "EPIC-001", "--points", "3",
        "--acceptance", "Given a user When they save Then the store has the story",
        "--always", "Keep the store valid",
        "--never", "Commit secrets",
    ]
    subprocess.run(CLI + story, cwd=tmp_path, check=True)
    subprocess.run(CLI + ["gate", "ready", "US-001"], cwd=tmp_path, check=True)
    bad = subprocess.run(CLI + ["check", "phase", "implementation", "--outcome", "x"], cwd=tmp_path, text=True, capture_output=True)
    assert bad.returncode == 1
    assert "BMAD-1" in bad.stdout + bad.stderr
    blocked = subprocess.run(
        CLI + ["check", "guard", "add a new dependency", "--ask", "new dependency"],
        cwd=tmp_path, text=True, capture_output=True,
    )
    assert blocked.returncode != 0
    subprocess.run(CLI + ["check", "sysl", str(ROOT / "diagrams/sysl/example.sysl")], cwd=tmp_path, check=True)
    subprocess.run(CLI + ["check", "calm", str(ROOT / "diagrams/calm/example.calm.json")], cwd=tmp_path, check=True)
    flow = subprocess.run(CLI + ["workflow", "epics", "--idea", "IDEA-001", "--epic", "EPIC-001"], cwd=tmp_path, text=True, capture_output=True)
    assert flow.returncode == 0
    assert "PASS" in flow.stdout
    subprocess.run(CLI + ["sprint", "new", "--goal", "Ship the save"], cwd=tmp_path, check=True)
    subprocess.run(CLI + ["sprint", "add", "--id", "US-001", "--sprint", "S1"], cwd=tmp_path, check=True)
    subprocess.run(CLI + ["workflow", "sprint", "--sprint", "S1"], cwd=tmp_path, check=True)
    guide = subprocess.run(CLI + ["guide", "bdd"], cwd=tmp_path, text=True, capture_output=True)
    assert guide.returncode == 0
    assert "Given" in guide.stdout
    store = json.loads((tmp_path / "mazu-data/store.json").read_text(encoding="utf-8"))
    assert store["items"][-1]["points"] == 3
