#!/usr/bin/env python3
"""MAZU-ADGILE CLI: backlog, sprints, requirements, ADR, time, dashboard.

Project-agnostic. Stores data in ./mazu-data/store.json (gitignored by default).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
DATA = ROOT / "mazu-data"
STORE = DATA / "store.json"
DASH_HTML = DATA / "dashboard.html"
DASH_MD = DATA / "dashboard.md"

STATUSES = ("backlog", "ready", "in-progress", "review", "done")
KINDS = ("idea", "epic", "story", "task", "requirement", "adr")
FIB = (1, 2, 3, 5, 8, 13, 21)


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def empty_store() -> dict:
    return {
        "version": 1,
        "items": [],
        "sprints": [],
        "time_logs": [],
        "links": [],
    }


def load() -> dict:
    DATA.mkdir(exist_ok=True)
    if not STORE.exists():
        save(empty_store())
    return json.loads(STORE.read_text(encoding="utf-8"))


def save(data: dict) -> None:
    DATA.mkdir(exist_ok=True)
    STORE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def next_id(data: dict, kind: str) -> str:
    prefix = {
        "idea": "IDEA",
        "epic": "EPIC",
        "story": "US",
        "task": "TASK",
        "requirement": "REQ",
        "adr": "ADR",
    }[kind]
    n = 1 + sum(1 for i in data["items"] if i["kind"] == kind)
    return f"{prefix}-{n:03d}"


def find(data: dict, item_id: str) -> dict:
    for item in data["items"]:
        if item["id"] == item_id:
            return item
    raise SystemExit(f"not found: {item_id}")


def add_item(kind: str, title: str, **extra) -> dict:
    if not title.strip():
        raise SystemExit("title required")
    data = load()
    points = extra.pop("points", None)
    if points is not None and int(points) not in FIB:
        raise SystemExit(f"points must be one of {FIB}")
    item = {
        "id": next_id(data, kind),
        "kind": kind,
        "title": title.strip(),
        "description": extra.pop("description", ""),
        "status": extra.pop("status", "backlog"),
        "points": int(points) if points is not None else None,
        "parent": extra.pop("parent", None),
        "sprint": None,
        "acceptance": extra.pop("acceptance", []),
        "boundaries": extra.pop("boundaries", {"always": [], "ask_first": [], "never": []}),
        "created_at": now(),
        "updated_at": now(),
    }
    item.update(extra)
    if item["status"] not in STATUSES:
        raise SystemExit(f"bad status {item['status']}")
    data["items"].append(item)
    save(data)
    return item


def cmd_init(_args: argparse.Namespace) -> None:
    if STORE.exists():
        print(f"already initialized: {STORE}")
        return
    save(empty_store())
    (DATA / "adr").mkdir(exist_ok=True)
    (DATA / "specs").mkdir(exist_ok=True)
    print(f"initialized {DATA}")


def cmd_add(args: argparse.Namespace) -> None:
    ac = [line.strip() for line in (args.acceptance or "").split("|") if line.strip()]
    boundaries = {
        "always": _split(args.always),
        "ask_first": _split(args.ask_first),
        "never": _split(args.never),
    }
    item = add_item(
        args.kind,
        args.title,
        description=args.description or "",
        points=args.points,
        parent=args.parent,
        acceptance=ac,
        boundaries=boundaries,
        status=args.status,
    )
    if args.kind == "adr":
        write_adr_file(item)
    print(item["id"])


def _split(value: str | None) -> list[str]:
    if not value:
        return []
    return [p.strip() for p in value.split("|") if p.strip()]


def write_adr_file(item: dict) -> None:
    folder = DATA / "adr"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{item['id']}.md"
    path.write_text(
        "\n".join(
            [
                f"# {item['id']}: {item['title']}",
                "",
                f"## Status",
                item["status"],
                "",
                "## Context",
                item.get("description") or "_fill in_",
                "",
                "## Decision",
                "_fill in_",
                "",
                "## Consequences",
                "- Positive:",
                "- Negative:",
                "",
            ]
        ),
        encoding="utf-8",
    )


def cmd_list(args: argparse.Namespace) -> None:
    data = load()
    rows = data["items"]
    if args.kind:
        rows = [i for i in rows if i["kind"] == args.kind]
    if args.status:
        rows = [i for i in rows if i["status"] == args.status]
    if args.sprint:
        rows = [i for i in rows if i.get("sprint") == args.sprint]
    if not rows:
        print("(empty)")
        return
    print(f"{'ID':<12} {'KIND':<12} {'ST':<12} {'SP':<4} {'SPRINT':<12} TITLE")
    for i in rows:
        sp = "-" if i.get("points") is None else str(i["points"])
        sprint = i.get("sprint") or "-"
        print(f"{i['id']:<12} {i['kind']:<12} {i['status']:<12} {sp:<4} {sprint:<12} {i['title']}")


def cmd_show(args: argparse.Namespace) -> None:
    item = find(load(), args.id)
    print(json.dumps(item, indent=2, ensure_ascii=False))


def cmd_move(args: argparse.Namespace) -> None:
    if args.status not in STATUSES:
        raise SystemExit(f"status must be one of {STATUSES}")
    data = load()
    item = find(data, args.id)
    item["status"] = args.status
    item["updated_at"] = now()
    save(data)
    print(f"{item['id']} -> {args.status}")


def cmd_log(args: argparse.Namespace) -> None:
    if args.hours <= 0:
        raise SystemExit("hours must be > 0")
    data = load()
    find(data, args.id)
    data["time_logs"].append(
        {"item": args.id, "hours": round(float(args.hours), 2), "note": args.note or "", "at": now()}
    )
    save(data)
    print(f"logged {args.hours}h on {args.id}")


def cmd_sprint(args: argparse.Namespace) -> None:
    data = load()
    if args.action == "new":
        sid = f"S{len(data['sprints']) + 1}"
        data["sprints"].append(
            {
                "id": sid,
                "goal": args.goal or "",
                "status": "planned",
                "created_at": now(),
            }
        )
        save(data)
        print(sid)
        return
    if args.action == "add":
        if not args.id or not args.sprint:
            raise SystemExit("need --id and --sprint")
        item = find(data, args.id)
        if not any(s["id"] == args.sprint for s in data["sprints"]):
            raise SystemExit(f"unknown sprint {args.sprint}")
        item["sprint"] = args.sprint
        if item["status"] == "backlog":
            item["status"] = "ready"
        item["updated_at"] = now()
        save(data)
        print(f"{item['id']} in {args.sprint}")
        return
    raise SystemExit("sprint action: new | add")


def hours_for(data: dict, item_id: str) -> float:
    return round(sum(t["hours"] for t in data["time_logs"] if t["item"] == item_id), 2)


def velocity(data: dict, sprint_id: str) -> int:
    return sum(
        int(i["points"] or 0)
        for i in data["items"]
        if i.get("sprint") == sprint_id and i["status"] == "done" and i["kind"] == "story"
    )


def cmd_dashboard(_args: argparse.Namespace) -> None:
    data = load()
    by_status: dict[str, int] = {s: 0 for s in STATUSES}
    by_kind: dict[str, int] = {k: 0 for k in KINDS}
    points_open = 0
    points_done = 0
    for item in data["items"]:
        by_status[item["status"]] = by_status.get(item["status"], 0) + 1
        by_kind[item["kind"]] = by_kind.get(item["kind"], 0) + 1
        if item["kind"] == "story" and item.get("points"):
            if item["status"] == "done":
                points_done += int(item["points"])
            else:
                points_open += int(item["points"])
    total_hours = round(sum(t["hours"] for t in data["time_logs"]), 2)

    lines = [
        "# MAZU dashboard",
        "",
        f"Generated: {now()}",
        "",
        "## By status",
    ]
    for status in STATUSES:
        lines.append(f"- {status}: {by_status.get(status, 0)}")
    lines += ["", "## By kind"]
    for kind in KINDS:
        lines.append(f"- {kind}: {by_kind.get(kind, 0)}")
    lines += [
        "",
        "## Estimation",
        f"- story points open: {points_open}",
        f"- story points done: {points_done}",
        f"- hours logged: {total_hours}",
        "",
        "## Sprints",
    ]
    if not data["sprints"]:
        lines.append("- (none)")
    for sprint in data["sprints"]:
        lines.append(f"- {sprint['id']} [{sprint['status']}] velocity={velocity(data, sprint['id'])} goal: {sprint.get('goal') or '-'}")
    lines += ["", "## Board", ""]
    lines.append("| ID | Kind | Status | SP | Hours | Sprint | Title |")
    lines.append("|---|---|---|---|---|---|---|")
    for item in data["items"]:
        sp = "" if item.get("points") is None else str(item["points"])
        lines.append(
            f"| {item['id']} | {item['kind']} | {item['status']} | {sp} | {hours_for(data, item['id'])} | {item.get('sprint') or ''} | {item['title']} |"
        )
    md = "\n".join(lines) + "\n"
    DASH_MD.write_text(md, encoding="utf-8")

    def cell(text: str) -> str:
        return (
            str(text)
            .replace("&", "&")
            .replace("<", "<")
            .replace(">", ">")
        )

    rows = []
    for item in data["items"]:
        rows.append(
            "<tr>"
            f"<td>{cell(item['id'])}</td>"
            f"<td>{cell(item['kind'])}</td>"
            f"<td>{cell(item['status'])}</td>"
            f"<td>{cell('' if item.get('points') is None else item['points'])}</td>"
            f"<td>{hours_for(data, item['id'])}</td>"
            f"<td>{cell(item.get('sprint') or '')}</td>"
            f"<td>{cell(item['title'])}</td>"
            "</tr>"
        )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>MAZU dashboard</title>
<style>
body {{ font-family: ui-sans-serif, system-ui, sans-serif; margin: 2rem; background: #0f1419; color: #e7ecf1; }}
h1 {{ font-weight: 600; }}
.cards {{ display: flex; gap: 1rem; flex-wrap: wrap; }}
.card {{ background: #1b2430; border-radius: 10px; padding: 1rem 1.2rem; min-width: 140px; }}
.card b {{ display: block; font-size: 1.6rem; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 1.5rem; }}
th, td {{ border-bottom: 1px solid #2a3644; text-align: left; padding: 0.45rem 0.5rem; }}
th {{ color: #9fb0c3; font-weight: 500; }}
</style>
</head>
<body>
<h1>MAZU-ADGILE</h1>
<p>Generated {cell(now())}. Story points are complexity. Hours are time spent. They are not the same.</p>
<div class="cards">
  <div class="card"><b>{len(data['items'])}</b>items</div>
  <div class="card"><b>{points_open}</b>SP open</div>
  <div class="card"><b>{points_done}</b>SP done</div>
  <div class="card"><b>{total_hours}</b>hours</div>
  <div class="card"><b>{len(data['sprints'])}</b>sprints</div>
</div>
<h2>Backlog</h2>
<table>
<thead><tr><th>ID</th><th>Kind</th><th>Status</th><th>SP</th><th>Hours</th><th>Sprint</th><th>Title</th></tr></thead>
<tbody>
{''.join(rows) or '<tr><td colspan="7">empty</td></tr>'}
</tbody>
</table>
</body>
</html>
"""
    DASH_HTML.write_text(html, encoding="utf-8")
    print(md)
    print(f"wrote {DASH_MD}")
    print(f"wrote {DASH_HTML}")


def cmd_board(args: argparse.Namespace) -> None:
    data = load()
    items = data["items"]
    if args.sprint:
        items = [i for i in items if i.get("sprint") == args.sprint]
    for status in STATUSES:
        bucket = [i for i in items if i["status"] == status]
        print(f"\n## {status} ({len(bucket)})")
        for item in bucket:
            sp = "" if item.get("points") is None else f" [{item['points']}sp]"
            print(f"  {item['id']} {item['title']}{sp}")


def cmd_doctor(_args: argparse.Namespace) -> None:
    root = Path(__file__).resolve().parents[1]
    required = [
        root / "skills" / "bmad" / "SKILL.md",
        root / "skills" / "sdd" / "SKILL.md",
        root / "skills" / "bdd" / "SKILL.md",
        root / "skills" / "adr" / "SKILL.md",
        root / "skills" / "agile-delivery" / "SKILL.md",
        root / "skills" / "product-ideas" / "SKILL.md",
        root / "skills" / "requirements" / "SKILL.md",
        root / "skills" / "sysl" / "SKILL.md",
        root / "skills" / "calm" / "SKILL.md",
        root / "methodology" / "MAZU-ADGILE.md",
        root / "agents" / "catalog.json",
        root / "templates" / "adr.md",
        root / "templates" / "user-story.md",
        root / "templates" / "spec.md",
        root / "templates" / "sprint-status.yaml",
        root / "schemas" / "store.schema.json",
    ]
    missing = [str(p.relative_to(root)) for p in required if not p.exists()]
    if missing:
        print("MISSING:")
        for m in missing:
            print(f"  {m}")
        raise SystemExit(1)
    print(f"ok: {len(required)} required sources present")
    print(f"cli: {Path(__file__).resolve()}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mazu", description="MAZU-ADGILE backlog CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="create mazu-data/store.json").set_defaults(func=cmd_init)
    sub.add_parser("dashboard", help="print dashboard and write html/md").set_defaults(func=cmd_dashboard)
    sub.add_parser("doctor", help="check kit sources exist").set_defaults(func=cmd_doctor)

    p_add = sub.add_parser("add", help="add an artifact")
    p_add.add_argument("kind", choices=KINDS)
    p_add.add_argument("title")
    p_add.add_argument("--description", default="")
    p_add.add_argument("--points", type=int)
    p_add.add_argument("--parent")
    p_add.add_argument("--status", default="backlog")
    p_add.add_argument("--acceptance", help="Given/When/Then blocks separated by |")
    p_add.add_argument("--always")
    p_add.add_argument("--ask-first", dest="ask_first")
    p_add.add_argument("--never")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="list artifacts")
    p_list.add_argument("--kind", choices=KINDS)
    p_list.add_argument("--status", choices=STATUSES)
    p_list.add_argument("--sprint")
    p_list.set_defaults(func=cmd_list)

    p_show = sub.add_parser("show")
    p_show.add_argument("id")
    p_show.set_defaults(func=cmd_show)

    p_move = sub.add_parser("move")
    p_move.add_argument("id")
    p_move.add_argument("status", choices=STATUSES)
    p_move.set_defaults(func=cmd_move)

    p_log = sub.add_parser("log", help="log hours spent (not story points)")
    p_log.add_argument("id")
    p_log.add_argument("hours", type=float)
    p_log.add_argument("--note", default="")
    p_log.set_defaults(func=cmd_log)

    p_sprint = sub.add_parser("sprint")
    p_sprint.add_argument("action", choices=("new", "add"))
    p_sprint.add_argument("--goal")
    p_sprint.add_argument("--id")
    p_sprint.add_argument("--sprint")
    p_sprint.set_defaults(func=cmd_sprint)

    p_board = sub.add_parser("board", help="kanban by status")
    p_board.add_argument("--sprint")
    p_board.set_defaults(func=cmd_board)
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
