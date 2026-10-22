#!/usr/bin/env python3
"""MAZU-ADGILE CLI: backlog, sprints, requirements, ADR, time, dashboard.

Project-agnostic. Stores data in ./mazu-data/store.json (gitignored by default).
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]


def workspace() -> Path:
    return Path.cwd() / "mazu-data"


def data_dir() -> Path:
    pointer = workspace() / "active-project"
    if pointer.exists():
        name = pointer.read_text(encoding="utf-8").strip()
        if name:
            return workspace() / "projects" / name
    return workspace()


def store_path() -> Path:
    return data_dir() / "store.json"


def dash_html() -> Path:
    return data_dir() / "dashboard.html"


def dash_md() -> Path:
    return data_dir() / "dashboard.md"

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
    data_dir().mkdir(parents=True, exist_ok=True)
    if not store_path().exists():
        save(empty_store())
    return json.loads(store_path().read_text(encoding="utf-8"))


def save(data: dict) -> None:
    data_dir().mkdir(parents=True, exist_ok=True)
    store_path().write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


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
    if store_path().exists():
        print(f"already initialized: {store_path()}")
        return
    save(empty_store())
    (data_dir() / "adr").mkdir(exist_ok=True)
    (data_dir() / "specs").mkdir(exist_ok=True)
    print(f"initialized {data_dir()}")


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
    folder = data_dir() / "adr"
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
    dash_md().write_text(md, encoding="utf-8")

    dash_html().write_text(render_html(data, live=False), encoding="utf-8")
    print(md)
    print(f"wrote {dash_md()}")
    print(f"wrote {dash_html()}")


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
        root / "skills" / "skill-creator" / "SKILL.md",
        root / "skills" / "backlog-connectors" / "SKILL.md",
        root / "skills" / "tool-calling" / "SKILL.md",
        root / "skills" / "projects" / "SKILL.md",
        root / "tools" / "openai.json",
        root / "tools" / "gigachat.json",
        root / "opencode.json",
        root / "CLAUDE.md",
        root / "QWEN.md",
        root / "scripts" / "audit.py",
        root / "cli" / "dashboard.html",
        root / "skills" / "create-epics-and-stories" / "SKILL.md",
        root / "skills" / "sprint-planning" / "SKILL.md",
        root / "wiki" / "Home.md",
        root / "wiki" / "BDD.md",
        root / "wiki" / "ADR.md",
        root / "wiki" / "Dashboard.md",
    ]
    missing = [str(p.relative_to(root)) for p in required if not p.exists()]
    if missing:
        print("MISSING:")
        for m in missing:
            print(f"  {m}")
        raise SystemExit(1)
    print(f"ok: {len(required)} required sources present")
    print(f"cli: {Path(__file__).resolve()}")


def slug(value: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    text = text.strip("-")
    if not text:
        raise SystemExit("project name required")
    return text


def cmd_project(args: argparse.Namespace) -> None:
    ws = workspace()
    ws.mkdir(parents=True, exist_ok=True)
    if args.action == "new":
        name = slug(args.name or "")
        folder = ws / "projects" / name
        folder.mkdir(parents=True, exist_ok=True)
        target = folder / "store.json"
        if not target.exists():
            target.write_text(json.dumps(empty_store(), indent=2) + "\n", encoding="utf-8")
        (ws / "active-project").write_text(name + "\n", encoding="utf-8")
        print(name)
        return
    if args.action == "use":
        name = slug(args.name or "")
        folder = ws / "projects" / name
        if not (folder / "store.json").exists():
            raise SystemExit(f"unknown project {name}")
        (ws / "active-project").write_text(name + "\n", encoding="utf-8")
        print(name)
        return
    if args.action == "list":
        projects = ws / "projects"
        if not projects.exists():
            print("(no projects)")
            return
        active = ""
        pointer = ws / "active-project"
        if pointer.exists():
            active = pointer.read_text(encoding="utf-8").strip()
        for child in sorted(p for p in projects.iterdir() if (p / "store.json").exists()):
            mark = "*" if child.name == active else " "
            print(f"{mark} {child.name}")
        return
    raise SystemExit("project action: new | use | list")


def _header_map(headers: list[str]) -> dict[str, int]:
    index = {}
    for i, header in enumerate(headers):
        index[header.strip().lower()] = i
    return index


def _pick(row: list[str], index: dict[str, int], names: tuple[str, ...]) -> str:
    for name in names:
        if name in index and index[name] < len(row):
            return row[index[name]].strip()
    return ""


def map_status(value: str) -> str:
    key = value.strip().lower()
    table = {
        "backlog": "backlog",
        "to do": "backlog",
        "todo": "backlog",
        "open": "backlog",
        "submitted": "backlog",
        "новая": "backlog",
        "ready": "ready",
        "selected for development": "ready",
        "in progress": "in-progress",
        "in-progress": "in-progress",
        "doing": "in-progress",
        "в работе": "in-progress",
        "review": "review",
        "in review": "review",
        "code review": "review",
        "done": "done",
        "closed": "done",
        "resolved": "done",
        "fixed": "done",
        "готово": "done",
    }
    return table.get(key, "backlog")


def map_kind(value: str) -> str:
    key = value.strip().lower()
    table = {
        "epic": "epic",
        "эпик": "epic",
        "story": "story",
        "user story": "story",
        "feature": "story",
        "история": "story",
        "bug": "task",
        "task": "task",
        "sub-task": "task",
        "subtask": "task",
        "задача": "task",
        "idea": "idea",
        "requirement": "requirement",
    }
    return table.get(key, "story")


def map_points(value: str) -> int | None:
    if not value:
        return None
    match = re.search(r"\d+", value)
    if not match:
        return None
    number = int(match.group(0))
    return number if number in FIB else None


def import_rows(rows: list[list[str]], source: str) -> int:
    if not rows:
        raise SystemExit("empty table")
    index = _header_map(rows[0])
    data = load()
    added = 0
    for row in rows[1:]:
        if not any(cell.strip() for cell in row):
            continue
        title = _pick(row, index, ("summary", "title", "name", "subject", "название"))
        if not title:
            continue
        kind = map_kind(_pick(row, index, ("issue type", "type", "тип")))
        status = map_status(_pick(row, index, ("status", "state", "статус")))
        points = map_points(_pick(row, index, ("story points", "story point", "points", "estimation", "оценка")))
        external = _pick(row, index, ("issue key", "issue id", "id", "key", "idreadable"))
        description = _pick(row, index, ("description", "описание"))
        item = add_item(
            kind,
            title,
            description=description,
            points=points,
            status=status,
            source=source,
            external_id=external or None,
        )
        if external:
            data = load()
            found = find(data, item["id"])
            found["external_id"] = external
            found["source"] = source
            save(data)
        added += 1
    return added


def read_csv(path: Path) -> list[list[str]]:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig")
    sample = text[:2048]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    return list(csv.reader(io.StringIO(text), dialect))


def read_xlsx(path: Path) -> list[list[str]]:
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(path) as book:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in book.namelist():
            root = ET.fromstring(book.read("xl/sharedStrings.xml"))
            for item in root.findall("m:si", ns):
                shared.append("".join(node.text or "" for node in item.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t")))
        sheet_name = "xl/worksheets/sheet1.xml"
        if sheet_name not in book.namelist():
            sheets = [name for name in book.namelist() if name.startswith("xl/worksheets/sheet")]
            if not sheets:
                raise SystemExit("xlsx has no worksheet")
            sheet_name = sorted(sheets)[0]
        root = ET.fromstring(book.read(sheet_name))
        rows: list[list[str]] = []
        for row in root.findall("m:sheetData/m:row", ns):
            values: list[str] = []
            for cell in row.findall("m:c", ns):
                ref = cell.attrib.get("r", "A1")
                col = re.match(r"[A-Z]+", ref)
                col_index = 0
                if col:
                    for ch in col.group(0):
                        col_index = col_index * 26 + (ord(ch) - 64)
                    col_index -= 1
                while len(values) < col_index:
                    values.append("")
                kind = cell.attrib.get("t")
                node = cell.find("m:v", ns)
                inline = cell.find("m:is", ns)
                if kind == "s" and node is not None and node.text:
                    text = shared[int(node.text)]
                elif kind == "inlineStr" and inline is not None:
                    text = "".join(t.text or "" for t in inline.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"))
                else:
                    text = node.text if node is not None and node.text else ""
                values.append(text)
            rows.append(values)
        return rows


def write_xlsx(path: Path, rows: list[list[str]]) -> None:
    shared: list[str] = []
    lookup: dict[str, int] = {}

    def sid(value: str) -> int:
        if value not in lookup:
            lookup[value] = len(shared)
            shared.append(value)
        return lookup[value]

    sheet_rows = []
    for r_index, row in enumerate(rows, start=1):
        cells = []
        for c_index, value in enumerate(row):
            col = ""
            n = c_index + 1
            while n:
                n, rem = divmod(n - 1, 26)
                col = chr(65 + rem) + col
            cells.append(f'<c r="{col}{r_index}" t="s"><v>{sid(value)}</v></c>')
        sheet_rows.append(f'<row r="{r_index}">{"".join(cells)}</row>')
    shared_xml = "".join(f"<si><t>{_xml(text)}</t></si>" for text in shared)
    files = {
        "[Content_Types].xml": """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>
</Types>""",
        "_rels/.rels": """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>""",
        "xl/workbook.xml": """<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets><sheet name="backlog" sheetId="1" r:id="rId1"/></sheets></workbook>""",
        "xl/_rels/workbook.xml.rels": """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>
</Relationships>""",
        "xl/sharedStrings.xml": f"""<?xml version="1.0" encoding="UTF-8"?>
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="{len(shared)}" uniqueCount="{len(shared)}">{shared_xml}</sst>""",
        "xl/worksheets/sheet1.xml": f"""<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>{''.join(sheet_rows)}</sheetData></worksheet>""",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as book:
        for name, content in files.items():
            book.writestr(name, content)


def _xml(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def cmd_import(args: argparse.Namespace) -> None:
    path = Path(args.file)
    if not path.exists():
        raise SystemExit(f"not found: {path}")
    if args.kind == "xlsx":
        rows = read_xlsx(path)
    else:
        rows = read_csv(path)
    count = import_rows(rows, args.kind)
    print(f"imported {count} from {args.kind}")


def export_rows(data: dict) -> list[list[str]]:
    rows = [["id", "kind", "title", "status", "points", "sprint", "source", "external_id", "description"]]
    for item in data["items"]:
        rows.append([
            item["id"],
            item["kind"],
            item["title"],
            item["status"],
            "" if item.get("points") is None else str(item["points"]),
            item.get("sprint") or "",
            item.get("source") or "",
            item.get("external_id") or "",
            item.get("description") or "",
        ])
    return rows


def cmd_export(args: argparse.Namespace) -> None:
    rows = export_rows(load())
    path = Path(args.file)
    if args.kind == "xlsx":
        write_xlsx(path, rows)
    else:
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerows(rows)
    print(path)


def cmd_connectors(_args: argparse.Namespace) -> None:
    checks = {
        "jira": ["JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_TOKEN"],
        "youtrack": ["YOUTRACK_URL", "YOUTRACK_TOKEN"],
    }
    for name, keys in checks.items():
        missing = [key for key in keys if not os.environ.get(key)]
        if missing:
            print(f"{name}: not connected, missing {', '.join(missing)}")
        else:
            print(f"{name}: env present")
    print("csv: ready")
    print("xlsx: ready")
    print("live pull is optional. Without tokens use: import jira-csv | import youtrack-csv | import xlsx")


def _http_json(url: str, headers: dict[str, str]) -> dict:
    import urllib.request

    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def cmd_pull(args: argparse.Namespace) -> None:
    if args.system == "jira":
        base = os.environ.get("JIRA_BASE_URL", "").rstrip("/")
        email = os.environ.get("JIRA_EMAIL", "")
        token = os.environ.get("JIRA_TOKEN", "")
        if not (base and email and token):
            raise SystemExit(
                "Jira is not connected. Set JIRA_BASE_URL, JIRA_EMAIL, JIRA_TOKEN "
                "or export a CSV and run: mazu import jira-csv FILE"
            )
        import base64

        auth = base64.b64encode(f"{email}:{token}".encode()).decode()
        jql = args.jql or "ORDER BY updated DESC"
        url = f"{base}/rest/api/3/search/jql?jql={urllib_quote(jql)}&maxResults=50&fields=summary,status,issuetype,description"
        payload = _http_json(url, {"Authorization": f"Basic {auth}", "Accept": "application/json"})
        rows = [["issue key", "issue type", "summary", "status", "description"]]
        for issue in payload.get("issues", []):
            fields = issue.get("fields") or {}
            rows.append([
                issue.get("key", ""),
                (fields.get("issuetype") or {}).get("name", "Story"),
                fields.get("summary") or "",
                (fields.get("status") or {}).get("name", ""),
                "",
            ])
        print(f"imported {import_rows(rows, 'jira')} from jira")
        return
    if args.system == "youtrack":
        base = os.environ.get("YOUTRACK_URL", "").rstrip("/")
        token = os.environ.get("YOUTRACK_TOKEN", "")
        if not (base and token):
            raise SystemExit(
                "YouTrack is not connected. Set YOUTRACK_URL and YOUTRACK_TOKEN "
                "or export a CSV and run: mazu import youtrack-csv FILE"
            )
        query = args.jql or ""
        url = (
            f"{base}/api/issues?fields=idReadable,summary,description"
            f"&$top=50&query={urllib_quote(query)}"
        )
        payload = _http_json(url, {"Authorization": f"Bearer {token}", "Accept": "application/json"})
        rows = [["issue id", "type", "summary", "status", "description"]]
        for issue in payload:
            rows.append([
                issue.get("idReadable", ""),
                "Story",
                issue.get("summary") or "",
                "Open",
                issue.get("description") or "",
            ])
        print(f"imported {import_rows(rows, 'youtrack')} from youtrack")
        return
    raise SystemExit("pull system: jira | youtrack")


def urllib_quote(value: str) -> str:
    from urllib.parse import quote
    return quote(value)


def cmd_skill(args: argparse.Namespace) -> None:
    if args.action != "new":
        raise SystemExit("skill action: new")
    name = slug(args.name or "")
    folder = KIT / "skills" / name
    path = folder / "SKILL.md"
    if path.exists() and not args.force:
        raise SystemExit(f"exists: {path}")
    folder.mkdir(parents=True, exist_ok=True)
    title = args.title or name
    path.write_text(
        "\n".join([
            "---",
            f"name: {name}",
            f"description: {args.description or 'Created by mazu skill new. Fill the procedure before use.'}",
            "---",
            "",
            f"# {title}",
            "",
            "## When",
            "",
            "## Procedure",
            "1. ",
            "",
            "## Commands",
            "```bash",
            "python3 cli/mazu.py --help",
            "```",
            "",
            "## Boundaries",
            "Always: keep store.json valid.",
            "Ask First: change this skill's public procedure.",
            "Never: put product data into the method repository.",
            "",
        ]),
        encoding="utf-8",
    )
    print(path.relative_to(KIT))



def render_html(data: dict, live: bool) -> str:
    template = (KIT / "cli" / "dashboard.html").read_text(encoding="utf-8")
    project = data_dir().name if data_dir().parent.name == "projects" else "local"
    boot = {
        "live": live,
        "generated": now(),
        "project": project,
        "store": data,
        "hours": {item["id"]: hours_for(data, item["id"]) for item in data["items"]},
    }
    payload = json.dumps(boot, ensure_ascii=False).replace("<", "\\u003c")
    if "__BOOT__" not in template:
        raise SystemExit("dashboard template has no boot slot")
    return template.replace("__BOOT__", payload)


def snapshot(live: bool = True) -> dict:
    data = load()
    project = data_dir().name if data_dir().parent.name == "projects" else "local"
    return {
        "live": live,
        "generated": now(),
        "project": project,
        "store": data,
        "hours": {item["id"]: hours_for(data, item["id"]) for item in data["items"]},
    }


def cmd_serve(args: argparse.Namespace) -> None:
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt: str, *values) -> None:
            print(fmt % values)

        def _send(self, code: int, body: bytes, content_type: str) -> None:
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _json(self, code: int, payload: dict) -> None:
            raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self._send(code, raw, "application/json; charset=utf-8")

        def do_GET(self) -> None:
            if self.path in ("/", "/index.html"):
                page = render_html(load(), live=True).encode("utf-8")
                self._send(200, page, "text/html; charset=utf-8")
                return
            if self.path == "/api/store":
                self._json(200, snapshot())
                return
            self._json(404, {"error": "not found"})

        def do_POST(self) -> None:
            length = int(self.headers.get("Content-Length", "0") or "0")
            if length > 100_000:
                self._json(413, {"error": "body too large"})
                return
            try:
                payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
            except json.JSONDecodeError:
                self._json(400, {"error": "bad json"})
                return
            try:
                if self.path == "/api/move":
                    cmd_move(argparse.Namespace(id=payload["id"], status=payload["status"]))
                elif self.path == "/api/log":
                    cmd_log(argparse.Namespace(id=payload["id"], hours=float(payload["hours"]), note=payload.get("note") or ""))
                elif self.path == "/api/add":
                    points = payload.get("points")
                    cmd_add(argparse.Namespace(
                        kind=payload.get("kind") or "story",
                        title=payload.get("title") or "",
                        description="",
                        points=int(points) if points not in (None, "") else None,
                        parent=payload.get("parent") or None,
                        status="backlog",
                        acceptance="",
                        always=None,
                        ask_first=None,
                        never=None,
                    ))
                elif self.path == "/api/sprint":
                    cmd_sprint(argparse.Namespace(action="new", goal=payload.get("goal") or "", id=None, sprint=None))
                else:
                    self._json(404, {"error": "not found"})
                    return
            except SystemExit as exc:
                self._json(400, {"error": str(exc)})
                return
            self._json(200, snapshot())

    server = ThreadingHTTPServer(("127.0.0.1", int(args.port)), Handler)
    print(f"MAZU dashboard http://127.0.0.1:{server.server_address[1]}/")
    server.serve_forever()


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

    p_serve = sub.add_parser("serve", help="interactive pastel dashboard on localhost")
    p_serve.add_argument("--port", type=int, default=8765)
    p_serve.set_defaults(func=cmd_serve)

    p_project = sub.add_parser("project", help="named local projects")
    p_project.add_argument("action", choices=("new", "use", "list"))
    p_project.add_argument("name", nargs="?")
    p_project.set_defaults(func=cmd_project)

    p_import = sub.add_parser("import", help="import csv or xlsx backlog")
    p_import.add_argument("kind", choices=("csv", "jira-csv", "youtrack-csv", "xlsx"))
    p_import.add_argument("file")
    p_import.set_defaults(func=cmd_import)

    p_export = sub.add_parser("export", help="export the active backlog")
    p_export.add_argument("kind", choices=("csv", "xlsx"))
    p_export.add_argument("file")
    p_export.set_defaults(func=cmd_export)

    sub.add_parser("connectors", help="show which live trackers have env").set_defaults(func=cmd_connectors)

    p_pull = sub.add_parser("pull", help="pull Jira or YouTrack when tokens exist")
    p_pull.add_argument("system", choices=("jira", "youtrack"))
    p_pull.add_argument("--jql", default="")
    p_pull.set_defaults(func=cmd_pull)

    p_skill = sub.add_parser("skill", help="create a skill skeleton")
    p_skill.add_argument("action", choices=("new",))
    p_skill.add_argument("name")
    p_skill.add_argument("--title")
    p_skill.add_argument("--description", default="")
    p_skill.add_argument("--force", action="store_true")
    p_skill.set_defaults(func=cmd_skill)
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
