#!/usr/bin/env python3
"""Validate the minimal GMGN V2 plugin and named-agent contracts."""

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
    "runner": ("gpt-5.6-luna", "max", "workspace-write"),
    "auditor": ("gpt-5.6-sol", "xhigh", "workspace-write"),
    "close_milestone": ("gpt-5.6-luna", "max", "workspace-write"),
    "release": ("gpt-5.6-luna", "max", "workspace-write"),
}
SPAWNERS = {
    "project_designer", "architect", "runner", "close_milestone", "release",
}
HAN_TEXT = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate() -> None:
    plugin = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
    require(plugin["name"] == "gmgn-v2", "插件名必须为 gmgn-v2")
    require(plugin["version"] == "0.1.1", "发布版本必须为 0.1.1")

    marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
    require(re.fullmatch(r"[A-Za-z0-9_-]+", marketplace["name"]) is not None,
            "Marketplace name must be CLI-safe")
    entry = next(item for item in marketplace["plugins"] if item["name"] == plugin["name"])
    require(entry["version"] == plugin["version"], "Marketplace version must match plugin version")

    hook_config = json.loads((ROOT / "hooks/hooks.json").read_text())
    session_hooks = hook_config["hooks"]["SessionStart"]
    require(len(session_hooks) == 1, "GMGN V2 must define one SessionStart sync hook")
    hook_command = session_hooks[0]["hooks"][0]["command"]
    require("${PLUGIN_ROOT}/skills/gmgn/scripts/install_codex_agents.py" in hook_command,
            "SessionStart hook must run the installed Agent synchronizer")
    require("--hook" in hook_command, "SessionStart Agent sync must use hook output mode")

    installer = (ROOT / "skills/gmgn/scripts/install_codex_agents.py").read_text()
    for marker in (
        ".gmgn-v2-managed.json", "os.replace", "def sync(", "def check(", "def uninstall(",
        "Refusing to overwrite symlink", "plugin_version",
    ):
        require(marker in installer, f"Agent installer is missing lifecycle behavior: {marker}")

    manager = (ROOT / "skills/gmgn/scripts/manage_codex_install.py").read_text()
    for marker in (
        'choices=("install", "update", "uninstall")', "git", "pull", "--ff-only",
        "plugin", "marketplace", "upgrade", "installedPath", '"sync"', '"check"',
    ):
        require(marker in manager, f"Codex install manager is missing lifecycle behavior: {marker}")

    for readme_name in ("README.md", "README.zh-CN.md"):
        readme = (ROOT / readme_name).read_text()
        for action in ("install", "update", "uninstall"):
            command = f"python3 skills/gmgn/scripts/manage_codex_install.py {action}"
            require(command in readme, f"{readme_name} is missing the unified {action} command")

    skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
    expected_skills = {
        "brainstorm", "code-review", "critic", "gmgn", "research", "verify",
        "write-agent-brief", "write-project-definition", "write-roadmap",
        "write-requirement", "write-design-bundle", "write-task",
    }
    require({path.parent.name for path in skill_files} == expected_skills, "Skill 集合与 V2 契约不一致")
    for path in skill_files:
        text = path.read_text()
        require(text.startswith("---\n"), f"缺少 frontmatter: {path}")
        require((path.parent / "agents/openai.yaml").is_file(), f"缺少 UI metadata: {path}")

    agent_dir = ROOT / ".codex/agents"
    expected_files = {f"gmgnv2_{role}.toml" for role in AGENTS}
    actual_files = {path.name for path in agent_dir.glob("*.toml")}
    require(actual_files == expected_files, "Agent TOML 集合与 V2 角色不一致")

    agent_instructions = {}
    for role, runtime in AGENTS.items():
        path = agent_dir / f"gmgnv2_{role}.toml"
        raw_profile = path.read_text()
        require(HAN_TEXT.search(raw_profile) is None, f"Agent TOML must be English: {role}")
        profile = tomllib.loads(raw_profile)
        require(profile["name"] == f"gmgnv2_{role}", f"Agent name 不匹配: {role}")
        require((profile["model"], profile["model_reasoning_effort"], profile["sandbox_mode"]) == runtime,
                f"Agent runtime 不匹配: {role}")
        instructions = profile["developer_instructions"]
        agent_instructions[role] = instructions
        require(len(instructions.strip()) >= 120, f"developer_instructions 过短: {role}")
        require("Brief inputs:" not in instructions, f"任务书输入不应复制到 Agent TOML: {role}")
        for section in ("Position:", "Responsibilities:", "Workflow:", "Do not:", "Checklist:"):
            require(section in instructions, f"developer_instructions 缺少 {section}: {role}")
        for discovery_rule in (
            "Repository discovery:",
            "Use DocStar first for cross-document Markdown search",
            "Use CodeGraph first for source-code search",
            "Use fallback search only after recording why DocStar or CodeGraph cannot be used",
        ):
            require(discovery_rule in instructions, f"Agent 缺少 repository discovery 规则: {role}: {discovery_rule}")
        if role in SPAWNERS:
            require("$gmgn-v2:write-agent-brief" in instructions,
                    f"可创建子 Agent 的角色未使用任务书 Skill: {role}")

    router = (ROOT / "skills/gmgn/SKILL.md").read_text()
    for marker in (
        "semantic", "gmgnv2_project_designer", "gmgnv2_architect",
        "gmgnv2_runner", "gmgnv2_researcher", "gmgnv2_auditor",
        "$gmgn-v2:write-agent-brief", "does not integrate", "mode or audit_type",
        "After a Runner reports `Task completed`", "gmgnv2_close_milestone",
        "newly accepted repair Task", "Never start Release automatically",
    ):
        require(marker in router, f"Router 缺少契约: {marker}")

    brief = (ROOT / "skills/write-agent-brief/SKILL.md").read_text()
    require("Deletion test" in brief, "任务书 Skill 缺少删除测试")
    for role in AGENTS:
        require(f"gmgnv2_{role}" in brief, f"任务书 Skill 缺少输入契约: {role}")
    for marker in ("$gmgn-v2:critic", "$gmgn-v2:code-review", "$gmgn-v2:verify",
                   "rather than setting mode or audit_type", "serial write handoff",
                   "cannot grant Verify permission"):
        require(marker in brief, f"任务书 Skill 缺少 Auditor 契约: {marker}")
    for marker in ("repository remote and target branch", "baseline commit",
                   "existing Task branch, workspace, and PR", "GitHub write authorization",
                   "target baseline", "existing document branch, workspace, and PR",
                   "GitHub write and merge authorization",
                   "Task PR and integration status", "target-branch commit"):
        require(marker in brief, f"任务书 Skill 缺少 Git 输入契约: {marker}")
    for marker in (
        "decision it informs", "claims and current anchors",
        "caller-owned comparison dimensions or metric definitions",
        "whether factual synthesis is requested", "stopping condition",
    ):
        require(marker in brief, f"任务书 Skill 缺少 Researcher 契约: {marker}")

    project_designer = agent_instructions["project_designer"]
    for marker in (
        "$gmgn-v2:brainstorm", "$gmgn-v2:write-project-definition",
        "$gmgn-v2:write-roadmap", "After receiving user references or `none-provided`, immediately",
        "When helpful, include concrete practices from reference projects",
        "gmgnv2_researcher", "gmgnv2_auditor", "$gmgn-v2:critic",
        "project-level user E2E", "Every Milestone must have explicit, decidable acceptance criteria",
        "explicit user approval", "gmgnv2_architect", "Do not modify R-D-T directly",
        "ProjectDefinitionLog.md", "validate the complete repair delta", "claims to verify",
        "whether factual synthesis is required", "Researcher does not recommend or select",
        "document-only branch", "codex/project-design-<short-description>",
        "git rebase origin/<target-branch>", "active accepted authority",
        "do not hand a local candidate to Runner",
    ):
        require(marker in project_designer, f"Project Designer 缺少契约: {marker}")

    architect = agent_instructions["architect"]
    for marker in (
        "$gmgn-v2:write-requirement", "$gmgn-v2:write-design-bundle",
        "$gmgn-v2:write-task", "gmgnv2_researcher", "gmgnv2_auditor",
        "$gmgn-v2:critic", "Requirement → Design Bundle → Task", "split test",
        "semantically accepted automatically", "wait for human approval of R-D-T", "validate the complete repair delta",
        "Researcher may normalize and compare facts along supplied dimensions",
        "does not score, rank, recommend, or select",
        "document-only branch", "codex/<Milestone ID>-rdt-<short-description>",
        "Initialize new Task rows as `pending`", "active accepted authority",
        "do not dispatch Runner",
    ):
        require(marker in architect, f"Architect 缺少契约: {marker}")

    researcher = agent_instructions["researcher"]
    for marker in (
        "$gmgn-v2:research", "bounded factual comparison, calculation, or cross-source synthesis",
        "without a global count limit", "Do not create decision dimensions",
        "rank, recommend, select, attribute causality, or make semantic decisions",
    ):
        require(marker in researcher, f"Researcher 缺少契约: {marker}")
    require("collect at most three" not in researcher, "Researcher 仍硬编码全局候选数量")
    require("Do not synthesize across sources" not in researcher, "Researcher 仍禁止所有事实综合")

    research_skill = (ROOT / "skills/research/SKILL.md").read_text()
    for marker in (
        "one bounded question", "separate modes",
        "Source quality depends on the claim",
        "one origin, not independent confirmation",
        "Do not impose a global candidate count",
        "direct observation, source claim, or derived result",
        "n/N", "numerator, denominator",
        "Synthesize facts only when requested", "caller-owned dimensions",
        "without ranking it", "evidence synthesis, not semantic judgment",
        "Do not create a Research document",
    ):
        require(marker in research_skill, f"Research Skill 缺少契约: {marker}")

    brainstorm = (ROOT / "skills/brainstorm/SKILL.md").read_text()
    for marker in (
        "First ask which projects", "immediately delegate the mandatory initial research",
        "verify each applicable user-provided reference",
        "independently discover projects", "technical approaches",
        "Wait for the initial required research before asking a substantive question",
        "state the relevant project's concrete practice",
        "gmgnv2_researcher", "Let the question determine the candidate count",
        "Researchers may normalize or compare facts only on dimensions supplied",
        "they never recommend or choose",
    ):
        require(marker in brainstorm, f"Brainstorm Skill 缺少调研提问循环: {marker}")

    writer = (ROOT / "skills/write-project-definition/SKILL.md").read_text()
    for marker in (
        "Do not apply a fixed outline", "functional scope", "Do not research",
        "Leave provider, version, interface, data, and algorithm choices to Design",
        "project-level user E2E success scenarios", "not test cases", "ProjectDefinitionLog.md",
        "Keep the DocStar machine surface", "type: project-definition-log",
        "pending-approval", "reciprocal existing-document links", "gmgn-v2",
    ):
        require(marker in writer, f"Project Definition 写作 Skill 缺少契约: {marker}")

    roadmap_writer = (ROOT / "skills/write-roadmap/SKILL.md").read_text()
    for marker in (
        "Do not impose a fixed outline", "direct normative upstream of Requirement",
        "Acceptance criteria are mandatory for every Milestone",
        "Project Definition scope and project-level user E2E scenarios",
        "Do not include dates", "Do not add a separate Backlog",
        "`M<n>-AC<n>`", "`M<n>-D<n>`", "bold only the ID", "gmgn-v2",
    ):
        require(marker in roadmap_writer, f"Roadmap 写作 Skill 缺少契约: {marker}")

    requirement_writer = (ROOT / "skills/write-requirement/SKILL.md").read_text()
    for marker in (
        "normative behavioral specification", "Roadmap Milestone acceptance criterion or deliverable → R/AC",
        "minimum acceptance criteria", "Apply a deletion test", "Do not impose a generic section template",
        "Do not invent a term definition", "This is coverage analysis, not a required document outline or a test plan",
        "An AC is behavioral authority from which tests can be derived",
        "Do not operationally redefine an ambiguous upstream condition",
        "A boundary disclaimer does not make an invented definition acceptable",
        "stable composite AC", "never infer the complete result only because each local AC passes",
        "`R<n>-AC<n>`", "bold only the ID", "reciprocal", "gmgn-v2",
    ):
        require(marker in requirement_writer, f"Requirement 写作 Skill 缺少契约: {marker}")

    design_writer = (ROOT / "skills/write-design-bundle/SKILL.md").read_text()
    for marker in (
        "normative technical authority", "Require bounded solution research",
        "Design.md is always the root normative authority", "stable Contract ID",
        "closed producer-to-state path", "Do not impose a generic section template",
        "return the exact Requirement gap", "Design the verification strategy",
        "lowest-cost deterministic oracle", "testing pyramid as a selection heuristic, not a quota",
        "Do not turn accepted behavior into line-by-line pseudocode",
        "Write each verification point as one short clause",
        "GitHub reference-code search", "Do not evaluate license or authorization risk",
        "minimum executable acceptance boundary", "link it instead of redesigning or duplicating it",
        "`D<n>`", "`C<n>`", "bold only the ID", "reciprocal", "gmgn-v2",
    ):
        require(marker in design_writer, f"Design Bundle 写作 Skill 缺少契约: {marker}")

    task_writer = (ROOT / "skills/write-task/SKILL.md").read_text()
    for marker in (
        "normative Milestone execution index", "Apply the split test repeatedly",
        "Prerequisite records only a true dependency", "maximally parallel",
        "| # | task | spec anchor | prerequisite | status | execution |",
        "Runtime provider-to-consumer data flow", "Do not invent a path",
        "Carry verification with the result", "Do not create generic Tasks named write tests",
        "For every composite AC", "one integration Task", "close-milestone for direct replay",
        "`M<n>-T<n>`", "execution/<Task ID>/Card.md", "canonical Task table", "gmgn-v2",
        "`| **<Task ID>** |`",
        "Keep one Task-row state machine", "`pending`", "`active`", "`blocked`",
        "`closed`", "`cancelled`", "merged final Task PR",
    ):
        require(marker in task_writer, f"Task 写作 Skill 缺少契约: {marker}")

    for name, content in (
        ("Project Definition", writer), ("Roadmap", roadmap_writer),
        ("Requirement", requirement_writer), ("Design", design_writer),
        ("Task", task_writer),
    ):
        for marker in ("`locale`", "`purpose`", "`upstream`", "`downstream`",
                       "`status`", "`type`", "`nature`", "real relative Markdown links",
                       "plain unquoted text", "comma-separated on one unquoted line"):
            require(marker in content, f"{name} 写作 Skill 缺少 DocStar frontmatter 契约: {marker}")

    auditor = agent_instructions["auditor"]
    for marker in (
        "Do not use a generic mode or audit_type", "$gmgn-v2:critic",
        "$gmgn-v2:code-review", "$gmgn-v2:verify",
        "Read exactly one matching audit Skill", "forming a successor candidate",
        "Verify must not modify the candidate", "exceed the repair permission of the selected Skill",
        "Do not commit, push, pull, fetch, rebase", "The caller owns every Git and GitHub state change",
    ):
        require(marker in auditor, f"Auditor 缺少按工作读取 Skill 的契约: {marker}")

    critic_skill = (ROOT / "skills/critic/SKILL.md").read_text()
    for marker in (
        "one fixed input document candidate", "$gmgn-v2:write-project-definition",
        "$gmgn-v2:write-roadmap", "$gmgn-v2:write-requirement",
        "$gmgn-v2:write-design-bundle", "$gmgn-v2:write-task",
        "pass: ready for user approval", "pass: auto-accept",
        "repaired: owner validation required", "Repair deterministic defects directly",
        "Do not write acceptance state yourself", "must validate the Auditor delta",
        "gmgn-v2", "structural evidence", "never treat a clean result as semantic approval",
    ):
        require(marker in critic_skill, f"Critic Skill 缺少契约: {marker}")

    review_skill = (ROOT / "skills/code-review/SKILL.md").read_text()
    for marker in (
        "single complete Review", "complete fixed input candidate C1",
        "$ponytail:ponytail", "Repair bounded findings directly",
        "repair-local TDD cycle", "RED for the intended reason",
        "GREEN on C1", "GREEN on C2", "repaired: caller validation required",
        "Do not perform a second complete Review", "Runner independently checks",
        "complete Task branch diff", "no unrelated commits", "Do not commit, push",
    ):
        require(marker in review_skill, f"Code Review Skill 缺少契约: {marker}")

    verify_skill = (ROOT / "skills/verify/SKILL.md").read_text()
    for marker in (
        "one recorded trigger", "one expected observable", "minimum valid observation",
        "correct the invocation", "Return fail only", "Return blocked",
        "never pass", "Do not create or modify tests", "never repairs V1",
        "forms a successor candidate V2",
    ):
        require(marker in verify_skill, f"Verify Skill 缺少契约: {marker}")

    runner = agent_instructions["runner"]
    for marker in (
        "Exactly one writer exists at a time", "$ponytail:ponytail",
        "Use $ponytail:ponytail to implement the minimum production change",
        "gmgnv2_project_designer", "gmgnv2_architect",
        "requires an upstream document change",
        "gmgnv2_auditor", "$gmgn-v2:code-review", "$gmgn-v2:verify",
        "Runner does not review its own implementation", "C1→C2", "RED on C1 and GREEN on C2",
        "GREEN→GREEN", "Verify does not modify the candidate", "do not run a second full Review",
        "Main Session does not integrate", "execution/<Task ID>/Card.md",
        "type: task-card", "type: execution-log", "execution_log", "latest_event",
        "unquoted plain text", "DocStar", "gmgn-v2", "structural results do not replace implementation gates",
        "git pull --ff-only", "git fetch origin", "git rebase origin/<target-branch>",
        "git push -u origin <Task branch>", "git push --force-with-lease",
        "never `git push --force`", "Never push directly to a shared branch",
        "One Task uses exactly one branch", "squash merge",
        "git branch -d <Task branch>", "git push origin --delete <Task branch>",
        "Ordinary dispatch accepts only `pending`", "set the current row and Log to `blocked`",
        "`closed` becomes authoritative only after that PR merges",
        "Do not modify any tracked execution record after merge", "`Task completed`",
    ):
        require(marker in runner, f"Runner 缺少合并实现或上游回路契约: {marker}")
    require("gmgnv2_coder" not in runner, "Runner 仍依赖已删除 Coder")
    require("随后更新最终执行记录" not in runner, "Runner 仍要求在 PR 合并后修改 tracked 执行记录")

    close_milestone = agent_instructions["close_milestone"]
    for marker in (
        "composite AC explicitly assigned to close-milestone replay", "directly replay its exact existing check",
        "no composite result was inferred from local passes", "gmgnv2_auditor", "$gmgn-v2:verify",
        "DocStar", "gmgn-v2", "Tools prove structure, not semantic closure",
        "git pull --ff-only", "closure-only PR", "Do not reuse a Task branch or modify or push a shared branch directly",
        "gmgnv2_architect", "new `pending` repair Task", "`repair Task accepted`",
        "Never reopen or reuse the branch or PR of a merged `closed` Task",
    ):
        require(marker in close_milestone, f"Close Milestone 缺少契约: {marker}")

    release = agent_instructions["release"]
    for marker in (
        "gmgnv2_auditor", "$gmgn-v2:verify", "external-operation authorization",
        "git pull --ff-only", "release-only PR", "Never commit or push directly to a shared branch",
        "create and push the tag only from that commit without pushing another code branch",
    ):
        require(marker in release, f"Release 缺少 Auditor 或授权契约: {marker}")

    legacy = [
        ROOT / ".codex/agents/gmgn_commander.toml",
        ROOT / ".codex/agents/gmgn_author.toml",
        ROOT / ".codex/agents/gmgnv2_coder.toml",
        ROOT / ".codex/agents/gmgnv2_critic.toml",
        ROOT / ".codex/agents/gmgnv2_reviewer.toml",
        ROOT / ".codex/agents/gmgnv2_verifier.toml",
        ROOT / "skills/run-task/SKILL.md",
        ROOT / "skills/write-design/SKILL.md",
        ROOT / ".codex/agents/gmgnv2_whitepaper.toml",
        ROOT / ".codex/agents/gmgnv2_decision.toml",
        ROOT / ".codex/agents/gmgnv2_project_definition.toml",
        ROOT / ".codex/agents/gmgnv2_roadmap.toml",
        ROOT / ".codex/agents/gmgnv2_goal.toml",
        ROOT / ".codex/agents/gmgnv2_project_design.toml",
        ROOT / ".codex/agents/gmgnv2_requirement.toml",
        ROOT / ".codex/agents/gmgnv2_design.toml",
        ROOT / ".codex/agents/gmgnv2_task.toml",
    ]
    require(not any(path.exists() for path in legacy), "仍存在旧 Agent 或阶段路由")


if __name__ == "__main__":
    try:
        validate()
    except (AssertionError, KeyError, OSError, ValueError, tomllib.TOMLDecodeError) as exc:
        print(f"GMGN V2 validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("GMGN V2 validation passed")
