#!/usr/bin/env python3
"""Install GMGN V2 named Codex agents without touching GMGN V1 profiles."""

import os
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / ".codex" / "agents"


def effective_codex_home() -> Path:
    configured = os.environ.get("CODEX_HOME")
    return Path(configured).expanduser() if configured else Path.home() / ".codex"


def install() -> tuple[Path, list[str], list[str]]:
    sources = sorted(SOURCE_DIR.glob("gmgnv2_*.toml"))
    if not sources:
        raise ValueError(f"No GMGN V2 Agent profiles found: {SOURCE_DIR}")

    destination_dir = effective_codex_home() / "agents"
    destination_dir.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    unchanged: list[str] = []

    for source in sources:
        destination = destination_dir / source.name
        if destination.is_symlink():
            raise ValueError(f"Refusing to overwrite symlink: {destination}")
        if destination.is_file() and destination.read_bytes() == source.read_bytes():
            unchanged.append(source.name)
            continue
        shutil.copyfile(source, destination)
        installed.append(source.name)

    return destination_dir, installed, unchanged


def main() -> int:
    try:
        destination, installed, unchanged = install()
    except (OSError, ValueError) as exc:
        print(f"GMGN V2 Agent installation failed: {exc}", file=sys.stderr)
        return 1

    print(f"GMGN V2 Agent directory: {destination}")
    print(f"Installed: {', '.join(installed) if installed else 'none'}")
    print(f"Unchanged: {', '.join(unchanged) if unchanged else 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
