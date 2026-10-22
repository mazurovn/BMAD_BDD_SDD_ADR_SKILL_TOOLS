import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, str(ROOT / "cli" / "mazu.py")]


def run(args, cwd, check=True):
    return subprocess.run(CLI + args, cwd=cwd, text=True, capture_output=True, check=check)


def test_battle_story_lifecycle(tmp_path):
    run(["init"], tmp_path)
    run(["project", "new", "battle"], tmp_path)
    run(["add", "idea", "Operator sees a failed gate"], tmp_path)
    run(["add", "epic", "Ready is checked", "--parent", "IDEA-001"], tmp_path)
    vague = run(
        ["add", "story", "Vague", "--parent", "EPIC-001", "--points", "3",
         "--acceptance", "Given a When b Then works well", "--never", "Commit secrets"],
        tmp_path,
    )
    assert vague.returncode == 0
    bad = run(["gate", "ready", "US-001"], tmp_path, check=False)
    assert bad.returncode == 1
    assert "not observable" in bad.stdout

    run(["add", "story", "Save", "--parent", "EPIC-001", "--points", "5",
         "--acceptance", "Given a user When they save Then the store has the story | Given an empty title When they save Then the command exits non-zero",
         "--always", "Keep the store valid", "--never", "Commit secrets"], tmp_path)
    run(["gate", "ready", "US-002"], tmp_path)
    run(["workflow", "epics", "--idea", "IDEA-001", "--epic", "EPIC-001"], tmp_path, check=False)
    # US-001 is still a child and fails the tree. That is the point of the battle.
    tree = run(["workflow", "epics", "--idea", "IDEA-001", "--epic", "EPIC-001"], tmp_path, check=False)
    assert tree.returncode == 1
    assert "US-001" in tree.stdout

    blocked = run(["check", "guard", "commit secrets", "--never", "commit secrets"], tmp_path, check=False)
    assert blocked.returncode != 0
    points = run(["add", "story", "Bad points", "--parent", "EPIC-001", "--points", "4"], tmp_path, check=False)
    assert points.returncode != 0

    run(["sprint", "new", "--goal", "Ship the save"], tmp_path)
    run(["sprint", "add", "--id", "US-002", "--sprint", "S1"], tmp_path)
    plan = run(["workflow", "sprint", "--sprint", "S1"], tmp_path, check=False)
    assert plan.returncode == 0
    run(["move", "US-002", "in-progress"], tmp_path)
    run(["log", "US-002", "1.5", "--note", "battle"], tmp_path)
    run(["move", "US-002", "review"], tmp_path)
    early = run(["gate", "done", "US-002"], tmp_path, check=False)
    assert early.returncode == 1
    false_claim = run(["evidence", "US-002", "pytest passed all tests"], tmp_path, check=False)
    assert false_claim.returncode != 0
    assert "requires a real command" in (false_claim.stdout + false_claim.stderr)
    failing_run = run(
        ["evidence", "US-002", "--run", sys.executable, "-c", "raise SystemExit(1)"],
        tmp_path,
        check=False,
    )
    assert failing_run.returncode != 0
    run(["evidence", "US-002", "--run", sys.executable, "-c", "print('happy path observed')"], tmp_path)
    run(["evidence", "US-002", "--run", sys.executable, "-c", "print('empty title exits non-zero')"], tmp_path)
    run(["gate", "done", "US-002"], tmp_path)
    run(["check", "sysl", str(ROOT / "diagrams/sysl/example.sysl")], tmp_path)
    run(["check", "calm", str(ROOT / "diagrams/calm/example.calm.json")], tmp_path)
    run(["check", "sysl", str(ROOT / "diagrams/sysl/backlog.sysl")], tmp_path)
    run(["check", "calm", str(ROOT / "diagrams/calm/backlog.calm.json")], tmp_path)
