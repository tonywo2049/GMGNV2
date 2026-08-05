# GMGN V2

GMGN V2 是面向 Codex 的 Agent 驱动研发工作流。它把项目想法逐步转化为可追溯的产品权威、可实施工作、经过独立审查的代码，以及明确的 Milestone 关闭结果。

规范架构见 [GMGNV2.md](GMGNV2.md)。本文档负责说明如何安装和使用。英文版见 [README.md](README.md)。

## GMGN V2 提供什么

- 单一项目权威链：`Project Definition → Roadmap → Requirement → Design Bundle → Task`。
- 产品 Brainstorm 和 Design 阶段必须完成外部调研。
- 只有 Project Definition 和 Roadmap 需要人工批准；R-D-T 文档经过独立 Critic 后自动接受。
- 每个 Task 使用独立 branch、worktree 和 PR，并执行 TDD、Ponytail、独立代码 Review 和基于证据的集成。
- Runner 完成后，Main Session 自动扫描并续派发新解锁的 Task。
- Milestone 关闭前完成整体核对，发现缺口时创建 repair Task。
- Release 必须获得明确请求，不会自动启动。

## 环境要求

- 支持插件的 Codex：ChatGPT 桌面端 Work/Codex 模式或 Codex CLI。IDE extension 不支持插件。
- Python 3.11 或更高版本，用于执行仓库验证。
- Git 和 GitHub remote，用于完整 branch/PR 工作流。
- Ponytail 插件及 `$ponytail:ponytail` Skill。Runner 修改代码或测试前必须读取它。
- DocStar 可选。存在时，GMGN V2 使用 `gmgn-v2` conventions 完成文档结构检查。

当前 Codex 插件行为见官方 [Plugins 指南](https://learn.chatgpt.com/docs/plugins)和 [Codex CLI 插件命令](https://learn.chatgpt.com/docs/developer-commands?surface=cli#cli-codex-plugin)。

## 安装

在仓库根目录执行一条命令：

```bash
python3 skills/gmgn/scripts/manage_codex_install.py install
```

该命令会在需要时注册本地 `gmgn-v2` marketplace、安装插件、校验实际安装版本中的 Agent TOML、原子复制到 `${CODEX_HOME:-$HOME/.codex}/agents`，并核对版本和文件哈希。它不会修改 GMGN V1 配置。

插件还带有一个 `SessionStart` Hook，作为通过 Plugins 界面安装或更新时的兜底。Codex 提示时需要检查并信任该 Hook。如果 Hook 报告 Agent 配置发生变化，再启动一个新 Session 后才能派发 GMGN V2 Agent。

安装完成后启动新的 Codex Session，插件 Skill 和 Agent 配置即可使用：

```text
使用 $gmgn-v2:gmgn。我想基于这个想法开发一个新产品：……
```

## 更新

在 GMGN V2 仓库中执行一条更新命令：

```bash
python3 skills/gmgn/scripts/manage_codex_install.py update
```

对于本地 Git marketplace，该命令要求工作区干净，并执行 `git pull --ff-only`；对于已配置的 Git marketplace，它执行 Codex marketplace upgrade。随后安装当前插件版本，从实际安装的插件副本同步 Agent TOML，并核对文件哈希。不需要再执行单独的 Agent 同步命令。

如果更新修改了 Agent TOML，完成后启动新的 Codex Session。

## 快速使用

常见指令：

```text
使用 $gmgn-v2:gmgn，把这个想法整理成 Project Definition 和 Roadmap。
```

```text
继续 Milestone M1，创建它的 Requirement、Design Bundle 和 Task。
```

```text
完成 Milestone M1 中所有可以派发的 Task。
```

```text
关闭 Milestone M1。
```

```text
把 accepted 候选发布为 v1.0.0。
```

Main Session 对当前请求做一次路由，使用 `$gmgn-v2:write-agent-brief` 生成最小任务书，然后由选中的 Agent 负责语义执行。

## 工作流程

1. **Project Designer** 完成带外部调研的 Brainstorm，创建或修订 Project Definition 和 Roadmap。
2. Project Definition 和 Roadmap 通过独立 Critic 后，分别取得用户明确批准。
3. **Architect** 把 accepted Roadmap Milestone 转成 Requirement、Design Bundle 和尽可能并行的 Task。
4. R-D-T 候选通过独立 Critic 后自动接受，并通过一个 document-only PR 合入。
5. Main Session 派发所有 prerequisite 已 `closed`、自身为 `pending`，且没有 active 或 unresolved blocked 尝试的 Task。
6. **Runner** 通过当前 Task 的 branch 和 PR 完成实现，随后返回 `Task completed` 与目标分支 merge commit。
7. Main Session 刷新目标分支并重新扫描同一 Milestone，继续派发新解锁的 Task。
8. 所有非 cancelled Task 都 `closed` 后，**Close Milestone** 核对 Roadmap 验收标准、R/AC、Contract、实现和证据。
9. 关闭阶段发现缺口时，由 Architect 创建新的 repair Task。Main Session 执行它并重新关闭 Milestone，不重开旧 Task。
10. **Release** 只在用户明确请求并提供必要外部操作授权后运行。

## Agent 与 Skill

| Agent | 负责内容 | 主要 Skill |
| --- | --- | --- |
| Project Designer | Brainstorm、Project Definition、ProjectDefinitionLog、Roadmap、用户审批 | `brainstorm`、`write-project-definition`、`write-roadmap`、`write-agent-brief` |
| Architect | Requirement、Design Bundle/Contract、Task 拆分 | `write-requirement`、`write-design-bundle`、`write-task`、`write-agent-brief` |
| Researcher | 一个有边界的证据问题；不推荐或选择 | `research` |
| Runner | 一个 Task 从 readiness 到实现和 PR 集成 | `ponytail`、`write-agent-brief` |
| Auditor | 一个固定的文档 Critic、代码 Review 或独立 Verify | `critic`、`code-review`、`verify` 三者之一 |
| Close Milestone | Milestone 核对、关闭记录、触发 repair Task | `write-agent-brief`；必要时由 Auditor 使用 `verify` |
| Release | 已授权的打包、发布、部署和结果记录 | `write-agent-brief`；必要时由 Auditor 使用 `verify` |

任何 Agent 创建另一个 Agent 前，都必须先使用 `write-agent-brief`。Auditor 不使用通用 mode；具体任务决定它读取哪个审查 Skill。

## 文档与接受规则

| 权威或记录 | 负责人 | 接受方式 |
| --- | --- | --- |
| Project Definition | Project Designer | Critic 通过、用户明确批准、document-only PR 合入 |
| Roadmap | Project Designer | Critic 通过、用户明确批准、document-only PR 合入 |
| Requirement | Architect | Critic 通过、自动语义接受、R-D-T PR 合入 |
| Design Bundle 与 Contract | Architect | Critic 通过、自动语义接受、R-D-T PR 合入 |
| Task.md | Architect | Critic 通过、自动语义接受、R-D-T PR 合入 |
| Task Card 与 Log | Runner | 随 Task PR 集成 |
| Milestone closure | Close Milestone | 整体核对通过且 closure-only PR 合入 |

只有合入目标分支的 commit 才是下游可使用的 active accepted authority。本地候选和未合入 PR 都不是 active authority。

Project Definition 是项目根权威。不存在 Goal 文档，Roadmap 是 Requirement 的直接上游。Task 执行阶段不再创建单独的 Coding 文档；执行证据保存在 Card、Log、测试、代码、PR 和 Git 历史中。

## Task 与 Git 规则

Task 行只使用固定状态：

```text
pending → active → blocked 或 closed
accepted 上游移除结果时，pending 或可恢复 blocked → cancelled
```

已经 closed 的 Task 不重开，后续缺陷创建新 Task。

Git 规则：

- 每个 Task 从最新目标分支开始。
- 一个 Task 只使用一个 Task branch、一个受管 worktree 和一个 PR。
- Codex 默认分支名：`codex/<Task ID>-<short-description>`。
- 不直接在共享分支开发、提交或 push。
- 当前 Task 的代码、测试、Card/Log 和必要的 Task-local 文档更新放在一起。
- 首次 push 或请求合并前执行 `git fetch origin` 和 `git rebase origin/<target-branch>`。
- 完整本地候选和必要门禁通过后才能首次 push。
- 只有 Task 独占 branch 在 rebase 后必须更新远端时才使用 `--force-with-lease`，禁止无保护 force push。
- 按仓库策略合并；仓库没有约定时默认 squash merge。
- 合并后刷新目标分支，只在安全且已授权时删除 Task branch/worktree。

Project Designer 和 Architect 分别使用独立 document-only branch 与 PR。Close Milestone 使用 closure-only PR。Release 的 version-only delta 可以使用 release-only PR。

## Milestone 关闭与发布

Close Milestone 建立以下闭环：

```text
Roadmap 验收标准和交付物 → R/AC → sufficient evidence
```

它核对 retained Contract 的 provider、consumer、失败行为、实现与集成证据。交给 closure replay 的组合型 AC 必须在真实入口和环境执行，不能根据多个局部 pass 推断组合结果。

如果关闭阶段发现实现、测试、Design 或 Task authority 缺口，Architect 创建新的 `pending` repair Task。Main Session 派发该 Task，并在它的 PR 合入后重新执行 closure。

Release 只打包或发布目标分支上的固定 accepted commit。它不改变产品含义，不重复未失效的接受工作，也不会在没有授权时执行外部操作。

## 兼容性

### GMGN V1

GMGN V1 和 V2 可以共存。V2 使用 `gmgn-v2` 插件名和 `gmgnv2_*` Agent 名。当前 Session 调用哪个 Skill，就运行哪个流程；使用 `$gmgn-v2:gmgn` 会运行 V2。

### DocStar

GMGN V2 Markdown 使用英文 frontmatter key、真实互反 Markdown 链接、稳定的 M/R/D/C/T ID，以及固定的 `Task → Card → Log → latest_event` 链。DocStar 可用时，使用项目本地 conventions 或 `gmgn-v2` preset，不同时叠加 V1 与 V2 preset。DocStar 只验证结构，不决定语义接受或 Milestone closure。

## 验证

```bash
python3 tests/validate_repository.py
python3 -m unittest discover -s tests -v
```

验证内容包括插件结构、Skill 集合、Agent runtime 和契约、Agent TOML 仅英文、跨 Agent 流程标记，以及安装脚本隔离性。

## 卸载

在仓库根目录执行一条命令：

```bash
python3 skills/gmgn/scripts/manage_codex_install.py uninstall
```

该命令会卸载 `gmgn-v2` 插件，并只删除被记录为 GMGN V2 管理的命名 Agent 文件，同时兼容删除 v0.1.0 在状态清单出现前安装的配置。它不会删除 GMGN V1 配置、项目文档、branch、PR 或仓库历史。

只有不再使用该 marketplace 中的任何插件时，才按需删除本地 marketplace：

```bash
codex plugin marketplace remove gmgn-v2
```

卸载后重启桌面端或启动新的 CLI Session。使用以下命令检查结果：

```bash
codex plugin list --json
```

## 仓库结构

```text
.codex-plugin/plugin.json        插件清单
.agents/plugins/marketplace.json 本地 marketplace 定义
.codex/agents/                   命名 Agent 配置
hooks/                           SessionStart Agent 同步兜底
skills/                          Router、写作、调研、审查及安装工具
GMGNV2.md                        规范工作流架构
README.md                        英文使用说明
README.zh-CN.md                  中文使用说明
tests/                           仓库契约验证
```
