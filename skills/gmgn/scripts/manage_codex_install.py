#!/usr/bin/env python3
"""Install, update, or uninstall GMGN V2 and its named Codex agents."""

import argparse
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[3]
PLUGIN = "gmgn-v2"
MARKETPLACE = "gmgn-v2"
SELECTOR = f"{PLUGIN}@{MARKETPLACE}"


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
        raise RuntimeError(f"Command failed: {' '.join(command)}\n{detail}")
    return result.stdout


def run_json(command: list[str]) -> dict:
    output = run(command)
    try:
        return json.loads(output)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Command did not return JSON: {' '.join(command)}") from exc


def marketplace() -> dict | None:
    data = run_json(["codex", "plugin", "marketplace", "list", "--json"])
    return next((item for item in data.get("marketplaces", []) if item.get("name") == MARKETPLACE), None)


def ensure_marketplace() -> dict:
    current = marketplace()
    if current:
        return current
    run_json(["codex", "plugin", "marketplace", "add", str(ROOT), "--json"])
    current = marketplace()
    if not current:
        raise RuntimeError(f"Marketplace was not registered: {MARKETPLACE}")
    return current


def update_marketplace(current: dict) -> None:
    source_type = current.get("marketplaceSource", {}).get("sourceType")
    if source_type == "git":
        run_json(["codex", "plugin", "marketplace", "upgrade", MARKETPLACE, "--json"])
        return
    if source_type != "local":
        raise RuntimeError(f"Unsupported marketplace source type: {source_type}")

    root = Path(current["root"])
    if run(["git", "-C", str(root), "status", "--porcelain"]).strip():
        raise RuntimeError(f"Local marketplace has uncommitted changes: {root}")
    run(["git", "-C", str(root), "pull", "--ff-only"])


def install_plugin() -> Path:
    result = run_json(["codex", "plugin", "add", SELECTOR, "--json"])
    installed_path = result.get("installedPath")
    if not installed_path:
        raise RuntimeError("Codex did not return the installed plugin path")
    path = Path(installed_path)
    installer = path / "skills" / "gmgn" / "scripts" / "install_codex_agents.py"
    if not installer.is_file():
        raise RuntimeError(f"Installed plugin is missing its Agent installer: {installer}")
    run([sys.executable, str(installer), "sync"])
    run([sys.executable, str(installer), "check"])
    return path


def uninstall_plugin() -> None:
    data = run_json(["codex", "plugin", "list", "--json"])
    installed = any(item.get("pluginId") == SELECTOR for item in data.get("installed", []))
    if installed:
        run_json(["codex", "plugin", "remove", SELECTOR, "--json"])
    run([sys.executable, str(ROOT / "skills/gmgn/scripts/install_codex_agents.py"), "uninstall"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("install", "update", "uninstall"))
    args = parser.parse_args(argv)

    try:
        if args.action == "uninstall":
            uninstall_plugin()
            print("GMGN V2 plugin and named Agents were uninstalled.")
            return 0

        current = ensure_marketplace()
        if args.action == "update":
            update_marketplace(current)
        installed_path = install_plugin()
        print(f"GMGN V2 installed from: {installed_path}")
        print("Start a new Codex session before using GMGN V2 Agents.")
        return 0
    except (KeyError, OSError, RuntimeError) as exc:
        print(f"GMGN V2 {args.action} failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
