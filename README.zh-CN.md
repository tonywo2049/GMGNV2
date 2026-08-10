# GMGN V2

GMGN V2 是面向 Codex 的 Agent 驱动研发工作流。它把产品想法转化为可追溯的产品权威、可实施工作、经过独立审查的代码和明确的 Milestone 关闭结果。

规范架构见 [GMGNV2.md](GMGNV2.md)。本文档只说明安装和使用。英文版见 [README.md](README.md)。

## GMGN V2 提供什么

- 权威链：`Project Definition + Requirements → Roadmap → Spec → Design Bundle → Task`。
- 只在产品决定需要时做针对性调研；只为未解决的外部实现事实做有边界的实现调研。
- 新建或语义修订的 Project Definition 与 Requirement 需要明确批准；Roadmap 只需首次批准；语义文档候选需要独立 Critic。
- 每个 Task 使用独立 branch、worktree 和 PR；Coder 执行 TDD 与 Ponytail，非机械候选还需独立 Review。
- 按容量并行派发 Task，完成 Milestone 关闭，并只在明确请求后执行 Release。

## 环境要求

- 支持插件的 Codex：ChatGPT 桌面端 Work/Codex 模式或 Codex CLI。IDE extension 不支持插件。
- Python 3.11 或更高版本，用于执行仓库验证。
- Git 和 GitHub remote，用于完整 branch/PR 工作流。
- Ponytail 插件及 `$ponytail:ponytail` Skill。Coder 修改代码或测试前使用它；Auditor 每次 Code Review 时也使用它。
- DocStar 可选。存在时，GMGN V2 使用 `gmgn-v2` conventions 检查文档结构。

当前 Codex 插件行为见官方 [Plugins 指南](https://learn.chatgpt.com/docs/plugins)和 [Codex CLI 插件命令](https://learn.chatgpt.com/docs/developer-commands?surface=cli#cli-codex-plugin)。

## 安装

在仓库根目录执行：

```bash
python3 skills/gmgn/scripts/manage_codex_install.py install
```

该命令会在需要时注册本地 marketplace、安装插件、校验已安装的 Agent TOML，并把命名 Agent 配置原子复制到 `${CODEX_HOME:-$HOME/.codex}/agents`。它不会修改 GMGN V1 配置。

插件还包含一个 `SessionStart` Hook，作为通过 Plugins 界面安装或更新时的兜底。Codex 提示时需要检查并信任该 Hook。Agent 配置发生变化后，启动新的 Codex Session。

## 更新

在 GMGN V2 仓库中执行：

```bash
python3 skills/gmgn/scripts/manage_codex_install.py update
```

对于本地 Git marketplace，该命令要求工作区干净并执行 `git pull --ff-only`；对于已配置的 Git marketplace，它执行 Codex marketplace upgrade。随后安装当前插件版本并同步 Agent 配置。

Agent 配置发生变化后，启动新的 Codex Session。

## 快速使用

```text
使用 $gmgn-v2:gmgn，把这个想法整理成 Project Definition、Requirements 和 Roadmap：……
```

```text
使用 $gmgn-v2:gmgn，继续 Milestone M1，创建它的 Spec、Design Bundle 和 Task。
```

```text
使用 $gmgn-v2:gmgn，完成 Milestone M1 中所有可以派发的 Task。
```

```text
使用 $gmgn-v2:gmgn，关闭 Milestone M1。
```

```text
使用 $gmgn-v2:gmgn，把 accepted 候选发布为 v1.0.0。
```

只有明确调用 `$gmgn-v2:gmgn` 才会启用 GMGN V2。路由、文档接受、Task 状态、Git、关闭和 Release 规则统一见 [GMGNV2.md](GMGNV2.md)。

## 验证

```bash
python3 tests/validate_repository.py
python3 -m unittest discover -s tests -v
```

验证覆盖插件结构、Skill 与 Agent 集合、Agent 运行配置、安装行为和其他机械契约。语义一致性由 Critic 审查，不能从文本标记校验推断。

## 卸载

在仓库根目录执行：

```bash
python3 skills/gmgn/scripts/manage_codex_install.py uninstall
```

该命令会卸载 `gmgn-v2` 插件，并只删除被记录为 GMGN V2 管理的命名 Agent 文件。它不会删除 GMGN V1 配置、项目文档、branch、PR 或仓库历史。

只有不再使用该 marketplace 中的任何插件时，才删除本地 marketplace：

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
hooks/                           SessionStart Agent 同步
skills/                          Router、写作、调研、审查及安装工具
GMGNV2.md                        规范工作流架构
README.md                        英文使用说明
README.zh-CN.md                  中文使用说明
tests/                           机械仓库验证
```
