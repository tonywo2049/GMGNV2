#!/usr/bin/env python3
"""Validate the mechanical GMGN V2 plugin contracts."""

import json
import re
from pathlib import Path
import sys
import tomllib


ROOT = Path(__file__).resolve().parents[1]
AGENTS = {
    "project_designer": ("gpt-5.6-sol", "max", "workspace-write"),
    "architect": ("gpt-5.6-sol", "max", "workspace-write"),
    "researcher": ("gpt-5.6-luna", "max", "read-only"),
    "runner": ("gpt-5.6-terra", "xhigh", "workspace-write"),
    "coder": ("gpt-5.6-luna", "max", "workspace-write"),
    "auditor": ("gpt-5.6-sol", "xhigh", "workspace-write"),
    "close_milestone": ("gpt-5.6-luna", "max", "workspace-write"),
    "release": ("gpt-5.6-luna", "max", "workspace-write"),
}
SPAWNERS = {
    "project_designer", "architect", "runner", "close_milestone", "release",
}
EXPECTED_SKILLS = {
    "brainstorm", "code-review", "critic", "gmgn", "research", "verify",
    "write-agent-brief", "write-design-bundle", "write-project-definition",
    "write-requirement", "write-roadmap", "write-spec", "write-task",
}
REQUIRED_AGENT_SECTIONS = (
    "Position:", "Responsibilities:", "Workflow:", "Do not:", "Checklist:",
)
HAN_TEXT = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
VERSION = re.compile(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON root must be an object: {path}")
    return value


def base_version(version: str) -> str:
    return version.split("+", 1)[0]


def validate_manifest() -> None:
    plugin = load_json(ROOT / ".codex-plugin/plugin.json")
    require(plugin.get("name") == "gmgn-v2", "Plugin name must be gmgn-v2")
    version = plugin.get("version")
    require(isinstance(version, str) and VERSION.fullmatch(version) is not None,
            "Plugin version must be a supported semantic version")
    prompts = plugin.get("interface", {}).get("defaultPrompt")
    require(isinstance(prompts, list) and len(prompts) == 1
            and "$gmgn-v2:gmgn" in prompts[0],
            "Plugin must provide one explicit GMGN V2 trigger prompt")

    marketplace = load_json(ROOT / ".agents/plugins/marketplace.json")
    require(re.fullmatch(r"[A-Za-z0-9_-]+", str(marketplace.get("name"))) is not None,
            "Marketplace name must be CLI-safe")
    entries = [
        item for item in marketplace.get("plugins", [])
        if item.get("name") == plugin["name"]
    ]
    require(len(entries) == 1, "Marketplace must contain one gmgn-v2 entry")
    entry = entries[0]
    require(base_version(entry.get("version", "")) == base_version(version),
            "Marketplace and plugin base versions must match")
    require(entry.get("source") == {"source": "local", "path": "./"},
            "Marketplace must point at this local plugin")
    require(entry.get("policy", {}).get("installation") == "AVAILABLE",
            "Plugin must be available for installation")
    require(entry.get("policy", {}).get("authentication") == "ON_INSTALL",
            "Plugin authentication policy must be ON_INSTALL")


def validate_hook() -> None:
    config = load_json(ROOT / "hooks/hooks.json")
    hooks = config.get("hooks", {}).get("SessionStart", [])
    require(len(hooks) == 1, "Exactly one SessionStart hook is required")
    commands = hooks[0].get("hooks", [])
    require(len(commands) == 1 and commands[0].get("type") == "command",
            "SessionStart must contain one command hook")
    command = commands[0].get("command", "")
    require("install_codex_agents.py" in command and "sync --hook" in command,
            "SessionStart must run Agent synchronization in hook mode")


def validate_skills() -> None:
    skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
    require({path.parent.name for path in skill_files} == EXPECTED_SKILLS,
            "Skill set does not match the GMGN V2 contract")
    for path in skill_files:
        require(path.read_text(encoding="utf-8").startswith("---\n"),
                f"Skill is missing frontmatter: {path}")
        require((path.parent / "agents/openai.yaml").is_file(),
                f"Skill is missing UI metadata: {path}")


def validate_agents() -> None:
    directory = ROOT / ".codex/agents"
    expected = {f"gmgnv2_{role}.toml" for role in AGENTS}
    require({path.name for path in directory.glob("*.toml")} == expected,
            "Agent profile set does not match the GMGN V2 roles")

    for role, runtime in AGENTS.items():
        path = directory / f"gmgnv2_{role}.toml"
        raw = path.read_text(encoding="utf-8")
        require(HAN_TEXT.search(raw) is None, f"Agent profile must be English: {role}")
        profile = tomllib.loads(raw)
        require(profile.get("name") == f"gmgnv2_{role}",
                f"Agent name does not match its filename: {role}")
        actual_runtime = (
            profile.get("model"),
            profile.get("model_reasoning_effort"),
            profile.get("sandbox_mode"),
        )
        require(actual_runtime == runtime, f"Agent runtime does not match: {role}")
        instructions = profile.get("developer_instructions", "")
        require(all(section in instructions for section in REQUIRED_AGENT_SECTIONS),
                f"Agent instructions are incomplete: {role}")
        require("read $gmgn-v2:gmgn completely" in instructions
                and "Apply its Shared Agent rules" in instructions,
                f"Agent does not load the shared contract: {role}")
        if role in SPAWNERS:
            require("$gmgn-v2:write-agent-brief" in instructions,
                    f"Spawning Agent does not use write-agent-brief: {role}")


def validate_user_surface() -> None:
    for script in (
        ROOT / "skills/gmgn/scripts/install_codex_agents.py",
        ROOT / "skills/gmgn/scripts/manage_codex_install.py",
    ):
        require(script.is_file(), f"Missing installer: {script}")

    for name in ("README.md", "README.zh-CN.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        require("$gmgn-v2:gmgn" in text, f"{name} is missing the explicit trigger")
        for action in ("install", "update", "uninstall"):
            command = f"python3 skills/gmgn/scripts/manage_codex_install.py {action}"
            require(command in text, f"{name} is missing the {action} command")


def validate_legacy_cleanup() -> None:
    legacy = (
        ".codex/agents/gmgn_commander.toml",
        ".codex/agents/gmgn_author.toml",
        ".codex/agents/gmgnv2_critic.toml",
        ".codex/agents/gmgnv2_reviewer.toml",
        ".codex/agents/gmgnv2_verifier.toml",
        "skills/run-task/SKILL.md",
        "skills/write-design/SKILL.md",
        "skills/write-project-requirement/SKILL.md",
    )
    require(not any((ROOT / path).exists() for path in legacy),
            "Legacy GMGN Agent or Skill remains")


def validate() -> None:
    validate_manifest()
    validate_hook()
    validate_skills()
    validate_agents()
    validate_user_surface()
    validate_legacy_cleanup()


if __name__ == "__main__":
    try:
        validate()
    except (AssertionError, KeyError, OSError, ValueError, json.JSONDecodeError,
            tomllib.TOMLDecodeError) as exc:
        print(f"GMGN V2 validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("GMGN V2 validation passed")
