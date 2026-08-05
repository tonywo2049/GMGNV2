#!/usr/bin/env python3
"""Manage GMGN V2 named Codex agents without touching other profiles."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import tomllib


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / ".codex" / "agents"
STATE_FILE = ".gmgn-v2-managed.json"
REQUIRED_FIELDS = ("name", "description", "developer_instructions")


def effective_codex_home() -> Path:
    configured = os.environ.get("CODEX_HOME")
    return Path(configured).expanduser() if configured else Path.home() / ".codex"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def plugin_version(source_dir: Path) -> str:
    manifest = source_dir.parents[1] / ".codex-plugin" / "plugin.json"
    try:
        return json.loads(manifest.read_text())["version"]
    except (KeyError, OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read plugin version from {manifest}: {exc}") from exc


def read_sources(source_dir: Path = SOURCE_DIR) -> dict[str, bytes]:
    sources = sorted(source_dir.glob("gmgnv2_*.toml"))
    if not sources:
        raise ValueError(f"No GMGN V2 Agent profiles found: {source_dir}")

    result: dict[str, bytes] = {}
    names: set[str] = set()
    for source in sources:
        if not source.is_file() or source.is_symlink():
            raise ValueError(f"Agent profile must be a regular file: {source}")
        data = source.read_bytes()
        try:
            profile = tomllib.loads(data.decode())
        except (UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
            raise ValueError(f"Invalid Agent profile {source}: {exc}") from exc
        missing = [
            field
            for field in REQUIRED_FIELDS
            if not isinstance(profile.get(field), str) or not profile[field].strip()
        ]
        if missing:
            raise ValueError(f"Agent profile {source} is missing: {', '.join(missing)}")
        if profile["name"] != source.stem:
            raise ValueError(f"Agent name does not match filename: {source}")
        if profile["name"] in names:
            raise ValueError(f"Duplicate Agent name: {profile['name']}")
        names.add(profile["name"])
        result[source.name] = data
    return result


def read_state(destination_dir: Path) -> dict:
    path = destination_dir / STATE_FILE
    if not path.exists():
        return {}
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Invalid GMGN V2 state file: {path}")
    try:
        state = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read GMGN V2 state file {path}: {exc}") from exc
    if state.get("schema_version") != 1 or not isinstance(state.get("files"), dict):
        raise ValueError(f"Unsupported GMGN V2 state file: {path}")
    for name, expected_hash in state["files"].items():
        if Path(name).name != name or not name.startswith("gmgnv2_") or not name.endswith(".toml"):
            raise ValueError(f"Unsafe managed Agent filename: {name}")
        if not isinstance(expected_hash, str):
            raise ValueError(f"Invalid managed Agent hash: {name}")
    return state


def atomic_write(path: Path, data: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def sync(source_dir: Path = SOURCE_DIR) -> tuple[Path, list[str], list[str], list[str]]:
    sources = read_sources(source_dir)
    destination_dir = effective_codex_home() / "agents"
    destination_dir.mkdir(parents=True, exist_ok=True)
    state = read_state(destination_dir)
    installed: list[str] = []
    unchanged: list[str] = []
    removed: list[str] = []
    stale = sorted(set(state.get("files", {})) - set(sources))
    state_path = destination_dir / STATE_FILE

    for name in sources:
        destination = destination_dir / name
        if destination.is_symlink():
            raise ValueError(f"Refusing to overwrite symlink: {destination}")
        if destination.exists() and not destination.is_file():
            raise ValueError(f"Agent destination is not a regular file: {destination}")
    for name in stale:
        destination = destination_dir / name
        if destination.exists() and not destination.is_file() and not destination.is_symlink():
            raise ValueError(f"Managed Agent destination is not a file: {destination}")
    if state_path.is_symlink() or (state_path.exists() and not state_path.is_file()):
        raise ValueError(f"Invalid GMGN V2 state path: {state_path}")

    for name, data in sources.items():
        destination = destination_dir / name
        if destination.is_file() and destination.read_bytes() == data:
            unchanged.append(name)
        else:
            atomic_write(destination, data)
            installed.append(name)

    for name in stale:
        destination = destination_dir / name
        if destination.exists() or destination.is_symlink():
            destination.unlink()
            removed.append(name)

    managed_state = {
        "schema_version": 1,
        "plugin_version": plugin_version(source_dir),
        "files": {name: digest(data) for name, data in sources.items()},
    }
    state_data = (json.dumps(managed_state, indent=2, sort_keys=True) + "\n").encode()
    if not state_path.is_file() or state_path.read_bytes() != state_data:
        atomic_write(state_path, state_data)

    return destination_dir, installed, unchanged, removed


def install() -> tuple[Path, list[str], list[str]]:
    destination, installed, unchanged, _ = sync()
    return destination, installed, unchanged


def check(source_dir: Path = SOURCE_DIR) -> tuple[Path, list[str]]:
    sources = read_sources(source_dir)
    destination_dir = effective_codex_home() / "agents"
    state = read_state(destination_dir)
    issues: list[str] = []
    expected_hashes = {name: digest(data) for name, data in sources.items()}

    if not state:
        issues.append(f"Missing state file: {destination_dir / STATE_FILE}")
    else:
        if state.get("plugin_version") != plugin_version(source_dir):
            issues.append("Installed Agent version does not match the plugin version")
        if state.get("files") != expected_hashes:
            issues.append("Managed Agent manifest does not match the plugin profiles")

    for name, expected_hash in expected_hashes.items():
        destination = destination_dir / name
        if destination.is_symlink() or not destination.is_file():
            issues.append(f"Missing regular Agent profile: {destination}")
        elif digest(destination.read_bytes()) != expected_hash:
            issues.append(f"Agent profile differs from the plugin: {destination}")

    return destination_dir, issues


def uninstall(source_dir: Path = SOURCE_DIR) -> tuple[Path, list[str]]:
    destination_dir = effective_codex_home() / "agents"
    state = read_state(destination_dir)
    names = set(state.get("files", {}))
    names.update(read_sources(source_dir))
    removed: list[str] = []

    for name in sorted(names):
        destination = destination_dir / name
        if destination.exists() or destination.is_symlink():
            if not destination.is_file() and not destination.is_symlink():
                raise ValueError(f"Managed Agent destination is not a file: {destination}")
            destination.unlink()
            removed.append(name)

    state_path = destination_dir / STATE_FILE
    if state_path.exists() or state_path.is_symlink():
        if not state_path.is_file() and not state_path.is_symlink():
            raise ValueError(f"Invalid GMGN V2 state path: {state_path}")
        state_path.unlink()
    return destination_dir, removed


def print_sync_result(
    destination: Path,
    installed: list[str],
    unchanged: list[str],
    removed: list[str],
) -> None:
    print(f"GMGN V2 Agent directory: {destination}")
    print(f"Installed: {', '.join(installed) if installed else 'none'}")
    print(f"Unchanged: {', '.join(unchanged) if unchanged else 'none'}")
    print(f"Removed: {', '.join(removed) if removed else 'none'}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("sync", "check", "uninstall"), nargs="?", default="sync")
    parser.add_argument("--hook", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    try:
        if args.action == "sync":
            destination, installed, unchanged, removed = sync()
            if args.hook:
                if installed or removed:
                    print(json.dumps({
                        "hookSpecificOutput": {
                            "hookEventName": "SessionStart",
                            "additionalContext": "GMGN V2 Agent profiles changed. Start a new Codex session before dispatching GMGN V2 Agents.",
                        }
                    }))
            else:
                print_sync_result(destination, installed, unchanged, removed)
            return 0
        if args.action == "check":
            destination, issues = check()
            if issues:
                for issue in issues:
                    print(issue, file=sys.stderr)
                return 1
            print(f"GMGN V2 Agent profiles match the plugin: {destination}")
            return 0

        destination, removed = uninstall()
        print(f"GMGN V2 Agent directory: {destination}")
        print(f"Removed: {', '.join(removed) if removed else 'none'}")
        return 0
    except (OSError, ValueError) as exc:
        print(f"GMGN V2 Agent operation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
