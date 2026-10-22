"""Build a source zip. The Node runtime is not packed: it is already installed."""

from __future__ import annotations

import os
import zipfile
from pathlib import Path

SKIP_ANYWHERE = {".git", "__pycache__", ".pytest_cache", "mazu-data"}


def include(root: Path, path: Path) -> bool:
    rel = path.relative_to(root)
    if rel.parts[0] == "dist":
        return False
    if any(part in SKIP_ANYWHERE for part in rel.parts):
        return False
    if rel.as_posix() in {"upstream/node/node", "upstream/node/node.xz"}:
        return False
    if path.suffix == ".pyc":
        return False
    return path.is_file()


def write_zip(root: Path, dest: Path) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as book:
        for dirpath, dirnames, filenames in os.walk(root):
            rel_dir = Path(dirpath).relative_to(root)
            dirnames[:] = [
                name
                for name in sorted(dirnames)
                if name not in SKIP_ANYWHERE and not (rel_dir == Path(".") and name == "dist")
            ]
            for name in sorted(filenames):
                path = Path(dirpath) / name
                if not include(root, path):
                    continue
                book.write(path, Path("mazu-adgile") / path.relative_to(root))
                count += 1
    return count
