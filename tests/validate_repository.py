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
    "researcher": ("gpt-5.6-luna", "max", "workspace-write"),
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
TASK_TRANSITION = re.compile(r"^\| `([^`]+)` \| `([^`]+)` \|", re.MULTILINE)
LOCAL_MARKDOWN_LINK = re.compile(r"\[[^]]+\]\((?![a-z]+:|#)([^)#]+)(?:#[^)]*)?\)")
EXPECTED_TASK_TRANSITIONS = {
    ("waiting", "ready"),
    ("blocked", "ready"),
    ("blocked", "waiting"),
    ("ready", "runner-active"),
    ("runner-active", "closed"),
    ("runner-active", "architect-required"),
    ("architect-required", "architect-active"),
    ("architect-active", "waiting"),
    ("architect-active", "blocked"),
}


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


def validate_execution_contract() -> None:
    shared = (ROOT / "skills/gmgn/SKILL.md").read_text(encoding="utf-8")
    review = (ROOT / "skills/code-review/SKILL.md").read_text(encoding="utf-8")
    brief = (ROOT / "skills/write-agent-brief/SKILL.md").read_text(encoding="utf-8")
    task = (ROOT / "skills/write-task/SKILL.md").read_text(encoding="utf-8")
    architect = (ROOT / ".codex/agents/gmgnv2_architect.toml").read_text(encoding="utf-8")
    runner = (ROOT / ".codex/agents/gmgnv2_runner.toml").read_text(encoding="utf-8")
    auditor = (ROOT / ".codex/agents/gmgnv2_auditor.toml").read_text(encoding="utf-8")
    state_table = shared.split("### 3.3 State transitions", 1)[1].split(
        "### 3.4 Dispatch scan", 1
    )[0]
    state_persistence = shared.split("### 3.2 State persistence", 1)[1].split(
        "### 3.3 State transitions", 1
    )[0]
    require(set(TASK_TRANSITION.findall(state_table)) == EXPECTED_TASK_TRANSITIONS,
            "Task transition table does not match the state machine")

    compact_form = brief.split("## Compact form", 1)[1].split(
        "## Deletion test", 1
    )[0]
    require(re.search(r"^Audit Skill:$", compact_form, re.MULTILINE) is not None,
            "Auditor brief is missing the Audit Skill field")
    audit_skills = set(re.findall(r"\$gmgn-v2:(critic|code-review|verify)", auditor))
    require(audit_skills == {"critic", "code-review", "verify"},
            "Auditor does not expose the complete audit Skill set")

    require("<target-branch>" not in runner and "origin/main" in runner,
            "Runner target must be origin/main")
    sync_marker = "confirm local `main` and `origin/main` identify the same commit"
    require(sync_marker in shared and runner.count(sync_marker) >= 2,
            "Task start and completion must synchronize local main with origin/main")
    require("otherwise fetch and create the branch/worktree directly from `origin/main`" not in runner
            and "do not bypass local `main`" in runner,
            "Runner must not bypass local main synchronization")
    require("Remote inspection or verification in an isolated worktree does not replace this local synchronization"
            in shared and runner,
            "Remote-only verification must not replace local main synchronization")
    require("git push origin main:main" in shared
            and "Never write semantic authority from `HEAD`" in shared
            and "git push origin HEAD:main" in shared,
            "Semantic and runtime direct-main publication paths are incomplete")
    require("Repository files are read and changed only through local Git state" in shared
            and "remote file API to read, create, update, or delete repository files" in shared
            and "reads one fixed latest `origin/main` snapshot" in shared
            and "never a Task runtime source" in shared
            and "confirm the accepted delta from local Git state" in runner
            and "confirm and validate the joint result from local Git state" in architect,
            "Repository content must be synchronized locally before reads or writes")
    require("owned temporary detached worktree" in shared
            and "without switching the shared checkout or local `main`" in shared
            and "remote fast-forward rule" in shared
            and "start a fresh transaction from the new `origin/main`" in shared
            and "git push origin HEAD:main" in shared
            and "without force" in shared,
            "Task runtime updates must use optimistic detached transactions")
    require("wait until no other authority-document writer owns local `main`" not in state_persistence
            and "acquire the authority write turn" not in runner
            and "acquire the authority write turn" not in architect
            and "shared section 3.2 transaction" in runner
            and "shared section 3.2 transaction" in architect
            and "isolated temporary detached transactions" in task,
            "Task runtime writers must not wait for semantic local-main ownership")
    release = (ROOT / ".codex/agents/gmgnv2_release.toml").read_text(encoding="utf-8")
    require("create the worktree from that synchronized local branch" in release
            and "from `origin/<target-branch>`" not in release,
            "Release must not bypass the synchronized local target branch")
    require("<commit>:execution/<Task ID>/Card.md" in task,
            "Task execution pointer format is missing")
    require("| # | task | spec anchor | prerequisite | status | execution |" in task,
            "Task table schema changed")
    require("no numeric PR limit" in shared and "no numeric PR limit" in runner,
            "Multi-repository Tasks must not impose a PR count limit")
    require("may span multiple repositories and PRs without becoming multiple Reviews" in review,
            "Code Review must cover one complete multi-repository candidate")
    require("### 1.2.1 Bounded repository evidence" in shared
            and "git diff --name-status <base>...<candidate>" in shared
            and "do not start with broad context such as `--unified=80`" in shared,
            "Bounded repository evidence rules are incomplete")
    require("Complete inspection means complete semantic coverage" in review
            and "not one unbounded diff command" in review,
            "Code Review does not define bounded complete inspection")
    require("After `interrupt_agent` succeeds, do not call `wait_agent` or `list_agents`"
            in shared and "`previous_status` is its pre-interruption status" in shared,
            "Interrupted Agents must not re-enter monitoring")
    require("owns a confirmed Runner or repair Architect dispatch that has not returned" in shared
            and "After all confirmed children return and a complete scan dispatches no successor"
            in shared,
            "Main Session monitoring must cover dispatch-to-claim and stop after the final scan")
    require("each transition has one writer" in shared
            and "Main Session never reconstructs an Agent-owned state from returned prose" in shared
            and "Runner owns its row's `runner-active`, `architect-required`, `closed`, `execution`" in shared
            and "the repair Architect owns its fixed batch's `architect-active`, `waiting`, `blocked`"
            in shared,
            "Task runtime fields must be written by the role that performs the transition")
    require("persist `ready → runner-active`" in runner
            and "persist `runner-active → architect-required`" in runner
            and "persist `closed`" in runner
            and "Main Session owns" not in runner,
            "Runner must claim, hand off, and close its own Task row")
    require("persist the complete batch as `architect-active`" in architect
            and "update each transferred Log" in architect
            and "persist each row's new checkpoint reference plus `waiting`" in architect,
            "Architect must claim its batch and persist Log, execution, and final state")
    require("Only Architect may persist `blocked`" in shared
            and "return `blocked`" in runner,
            "Only Architect may block a Task")
    require("There is no configured Runner concurrency limit" in shared
            and "At most 15" not in shared,
            "Task dispatch must not impose a fixed Runner concurrency limit")
    require("Run a complete scan on initialization, after any Runner returns, after the repair Architect returns"
            in shared
            and "Do not rescan merely because an Agent persisted an active state, updated `execution`, sent progress"
            in shared,
            "Main Session scan triggers must be event-driven")
    require("Existing or newly dispatched Runners do not defer an eligible Architect batch" in shared
            and "Rows that become `architect-required` after the batch is fixed wait for the next repair Architect"
            in shared,
            "Main Session must dispatch one fixed Architect batch in each complete scan")
    require("shared `ready` row anchor" in brief
            and "shared Task.md `architect-required` batch" in brief,
            "Task briefs must dispatch unclaimed Runner and Architect states")


def validate_markdown_links() -> None:
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in LOCAL_MARKDOWN_LINK.findall(text):
            require((path.parent / target).is_file(),
                    f"Broken local Markdown link in {path}: {target}")


def validate_user_surface() -> None:
    for script in (
        ROOT / "skills/gmgn/scripts/install_codex_agents.py",
        ROOT / "skills/gmgn/scripts/manage_codex_install.py",
    ):
        require(script.is_file(), f"Missing installer: {script}")

    for name in ("README.md", "README.zh-CN.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        require("$gmgn-v2:gmgn" in text, f"{name} is missing the explicit trigger")
        require("skills/gmgn/SKILL.md" in text, f"{name} is missing the runtime contract link")
        for action in ("install", "update", "uninstall"):
            command = f"python3 skills/gmgn/scripts/manage_codex_install.py {action}"
            require(command in text, f"{name} is missing the {action} command")
    require(not (ROOT / "GMGNV2.md").exists(), "Duplicated GMGNV2.md must not exist")


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
    validate_execution_contract()
    validate_markdown_links()
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
