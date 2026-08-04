#!/usr/bin/env python3
"""Validate the minimal GMGN V2 plugin and named-agent contracts."""

import json
from pathlib import Path
import sys
import tomllib


ROOT = Path(__file__).resolve().parents[1]
AGENTS = {
    "whitepaper": ("gpt-5.6-sol", "max", "workspace-write"),
    "decision": ("gpt-5.6-sol", "max", "workspace-write"),
    "roadmap": ("gpt-5.6-sol", "max", "workspace-write"),
    "goal": ("gpt-5.6-sol", "max", "workspace-write"),
    "requirement": ("gpt-5.6-sol", "max", "workspace-write"),
    "design": ("gpt-5.6-sol", "max", "workspace-write"),
    "task": ("gpt-5.6-sol", "max", "workspace-write"),
    "runner": ("gpt-5.6-sol", "xhigh", "workspace-write"),
    "coder": ("gpt-5.6-luna", "max", "workspace-write"),
    "reviewer": ("gpt-5.6-sol", "xhigh", "workspace-write"),
    "verifier": ("gpt-5.6-sol", "xhigh", "workspace-write"),
    "critic": ("gpt-5.6-sol", "xhigh", "read-only"),
    "researcher": ("gpt-5.6-luna", "max", "read-only"),
    "close_milestone": ("gpt-5.6-sol", "xhigh", "workspace-write"),
    "release": ("gpt-5.6-sol", "xhigh", "workspace-write"),
}
SPAWNERS = {
    "whitepaper", "decision", "roadmap", "goal", "requirement", "design",
    "task", "runner", "close_milestone", "release",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate() -> None:
    plugin = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
    require(plugin["name"] == "gmgn-v2", "插件名必须为 gmgn-v2")
    require(plugin["version"] == "0.1.0", "初始版本必须为 0.1.0")

    skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
    require({path.parent.name for path in skill_files} == {"gmgn", "write-agent-brief"},
            "只能发布 gmgn 与 write-agent-brief 两个 Skill")
    for path in skill_files:
        text = path.read_text()
        require(text.startswith("---\n"), f"缺少 frontmatter: {path}")
        require((path.parent / "agents/openai.yaml").is_file(), f"缺少 UI metadata: {path}")

    agent_dir = ROOT / ".codex/agents"
    expected_files = {f"gmgnv2_{role}.toml" for role in AGENTS}
    actual_files = {path.name for path in agent_dir.glob("*.toml")}
    require(actual_files == expected_files, "Agent TOML 集合与 V2 角色不一致")

    for role, runtime in AGENTS.items():
        path = agent_dir / f"gmgnv2_{role}.toml"
        profile = tomllib.loads(path.read_text())
        require(profile["name"] == f"gmgnv2_{role}", f"Agent name 不匹配: {role}")
        require((profile["model"], profile["model_reasoning_effort"], profile["sandbox_mode"]) == runtime,
                f"Agent runtime 不匹配: {role}")
        instructions = profile["developer_instructions"]
        require(len(instructions.strip()) >= 120, f"developer_instructions 过短: {role}")
        if role in SPAWNERS:
            require("$gmgn-v2:write-agent-brief" in instructions,
                    f"可创建子 Agent 的角色未使用任务书 Skill: {role}")

    router = (ROOT / "skills/gmgn/SKILL.md").read_text()
    for marker in ("semantic", "no unfinished prerequisite", "gmgnv2_runner",
                   "$gmgn-v2:write-agent-brief", "does not integrate"):
        require(marker in router, f"Router 缺少契约: {marker}")

    brief = (ROOT / "skills/write-agent-brief/SKILL.md").read_text()
    require("Deletion test" in brief, "任务书 Skill 缺少删除测试")
    for role in AGENTS:
        require(f"gmgnv2_{role}" in brief, f"任务书 Skill 缺少输入契约: {role}")

    runner = tomllib.loads((agent_dir / "gmgnv2_runner.toml").read_text())["developer_instructions"]
    for marker in ("只执行一次完整 Review", "不执行第二次完整 Review", "Main Session 不负责集成"):
        require(marker in runner, f"Runner 缺少门禁: {marker}")

    critic = tomllib.loads((agent_dir / "gmgnv2_critic.toml").read_text())["developer_instructions"]
    require("自动 accepted" in critic and "无需 Owner 审批" in critic,
            "Critic 通过后必须自动接受")

    legacy = [
        ROOT / ".codex/agents/gmgn_commander.toml",
        ROOT / ".codex/agents/gmgn_author.toml",
        ROOT / "skills/run-task/SKILL.md",
        ROOT / "skills/write-design/SKILL.md",
    ]
    require(not any(path.exists() for path in legacy), "仍存在旧 Agent 或阶段路由")


if __name__ == "__main__":
    try:
        validate()
    except (AssertionError, KeyError, OSError, ValueError, tomllib.TOMLDecodeError) as exc:
        print(f"GMGN V2 validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("GMGN V2 validation passed")
