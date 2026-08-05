# GMGN V2

## 目标

GMGN V2 让项目按明确文档推进，每一步可追溯，并在 Task 阶段最大化并行 coding。

权威文档链为：

`Project Definition → Roadmap → Requirement → Design Bundle → Task`

纳入文档图的 Markdown 使用 DocStar `gmgn-v2` 机器接口：固定英文 frontmatter 键、真实互反上下游链接、稳定 M/R/D/C/T ID，以及固定的 Task→Card→Log→latest_event 链。机器接口不规定正文目录。项目已有本地 conventions 时使用该完整配置，否则显式选择 `gmgn-v2`；不与 `gmgn-v1` 叠加。DocStar 只证明结构，不决定语义接受或 Milestone 关闭。

Project Definition 是项目的顶层需求来源，`ProjectDefinitionLog.md` 只记录其 accepted 变更。Task 之后不再创建 Coding 文档；执行结果写入 Card、Log、代码、测试和 Git 历史。不存在 Goal 文档。

每个 Task 由 Runner 使用一个独立 branch、worktree 和 PR；Codex 环境默认使用 `codex/<Task ID>-<short-description>`。新 Task 从 GitHub 最新目标分支创建，不在共享分支开发或 push；Task 的代码、测试和必要文档同 branch 提交，其他问题另建 Task。Auditor 只形成审查结论或受限修复，不 commit、push、rebase、操作 PR 或合并。

GitHub 同步只发生在明确边界：Task 开始和合并后在 clean 目标分支执行 `git pull --ff-only`；恢复远端同名 Task branch 时，仅在本地 clean 且只有远端领先时 fast-forward pull；Task branch 跟进目标分支使用 `git fetch origin` 和 `git rebase origin/<目标分支>`。首次 push 必须等完整本地候选、Auditor 和必要门禁通过；后续只 push 经验证的 Review/CI 修复或同步结果。每个 Task 只有一个 PR，默认 squash merge；rebase 后确需改写远端时只用 `--force-with-lease`，不得直接 push 共享分支或使用无保护的 force push。
Project Designer 和 Architect 各自把一个语义 change set 放入一个独立 document-only branch 与 PR：前者默认 `codex/project-design-<short-description>`，后者默认 `codex/<Milestone ID>-rdt-<short-description>`。候选通过各自接受门禁后才 push；PR 合入目标分支后才成为下游可消费的 active authority。两者不直接提交或 push 共享分支。

GMGN V2 不判断项目处于哪个阶段，只判断当前要做什么、所需上游是否存在、能否继续。

## 运行结构

每个命名 Agent 的 TOML 都在工作前强制读取 [`gmgn` Skill 的 Shared Agent rules](skills/gmgn/SKILL.md#shared-agent-rules)，但不应用其中标记为 Main Session only 的章节。仓库发现、职责所有权和父子 Agent 活动监测只在该处定义，不复制进 Agent TOML 或子 Agent 任务书。Agent 直接创建、监测和处理自身工作所需的子 Agent；经调用者传递问题、状态或 blocker 不转移职责。结果完成或出现取消、必要输入或授权缺失、范围失效、硬失败或不安全等精确 blocker 时，可以结束当前执行；blocker 解除后由原 Agent 继续。

Main Session 接收用户指令时只按固定职责选择目标 Agent，并把用户完整原话不改写地交给它；Main Session 不使用 `gmgn-v2:write-agent-brief`，不生成目标、摘要、拆解、优先级、方案或下一步指令。启动后，Main Session 原样转发用户消息与 Agent 的问题、状态和结果，不改写、总结、解释、合并或附加指导，也不负责集成；只有传输所需的发送方标识，以及从用户消息或 accepted authority 机械读取的精确 ID、锚点和状态可以附加。Main Session 不代替 Agent 履行职责或创建、管理其工作所需的子 Agent；这不限制 Main Session 自身已明确规定的机械派发和续派发。

推进 Task 集合或完成 Milestone 时，Main Session 机械读取 approved Task.md：派发状态为 `pending`、所有 prerequisite 已在目标分支 `closed`、且没有 active 或 unresolved blocked 执行的 Task。Runner 返回 `Task completed` 和 merge commit 后，Main Session 刷新同一目标分支并再次扫描，持续派发新解锁 Task。

没有可派发 Task 时，仍有活动 Runner 就等待，存在未完成 blocker 就返回精确缺口；所有非 cancelled Task 都在同一目标分支 `closed` 时启动 Close Milestone。Close Milestone 返回新 repair Task 时继续同一循环。单个指定 Task 请求完成后停止；Release 永不自动启动。

任何 Agent 创建子 Agent 前，都先使用 `gmgn-v2:write-agent-brief` 生成最小任务书；该 Skill 只用于 Agent 到子 Agent，不用于 Main Session，也不把 Shared Agent rules 复制进任务书。Project Designer 先通过一次一个关键问题，形成初步问题、用户与场景、期望结果和有边界的调研方向；达到该条件后再陈述当前理解、询问用户参考，并并行核对用户参考、主动发现项目和技术先例。Researcher 完整执行 `gmgn-v2:research`，可按调用者给定维度综合事实，但不推荐或选择。Architect 维护 R-D-T。Auditor 不使用 mode；它根据具体任务分别读取 Critic、Code Review 或 Verify Skill，由所读 Skill 决定是否可以形成后继候选。

## Agent

| Agent | 职责 |
| --- | --- |
| Project Designer | 带外部调研完成 Brainstorm，建立或修订 Project Definition 与 Roadmap，并取得用户批准 |
| Architect | 把 Roadmap 转成 Requirement、Design Bundle 和尽可能并行的 Task |
| Researcher | 执行 research Skill，为一个有边界的问题收集并按授权综合可核对证据，不作决策 |
| Runner | 直接负责一个 Task 的 readiness、Card/Log、测试、实现、审查修复和集成 |
| Auditor | 根据具体任务读取 critic、code-review 或 verify；前两者可受限修复，verify 保持候选只读 |
| Close Milestone | 汇总 Task 和证据，重放组合验收，关闭 Milestone 并留档 |
| Release | 发布 accepted 候选并留档 |

## 文档接受

Project Designer 和 Architect 为每个固定输入文档候选创建一个 Auditor，并要求其执行 `gmgn-v2:critic`。Critic 可以直接修复由 accepted 权威唯一确定、且不改变语义和所有权的缺陷，形成后继候选；文档负责人必须验证完整修复差异。需要语义决定的 finding 仍由文档负责人修复，同一 Auditor 只检查该差异和直接影响。Project Definition 和 Roadmap 无未解决 finding 后必须取得用户明确批准；Requirement、Design Bundle 和 Task 由 Architect 自动语义接受。在 Git-backed 项目中，两者都必须把各自 document-only PR 合入目标分支，目标 commit 才是下游 active accepted authority。

Project Designer 只修改 Project Definition 和 Roadmap。其文档 PR 合入后，Architect 才从该目标分支 commit 更新受影响的既有 R-D-T；缺失下游只有在用户目标明确包含继续形成下游时才创建。

## Task 执行

一个 Runner 只负责一个 Task，并管理其 workspace；任一时刻只能有一个写入者。Runner 实现时持有写入权，创建可修复候选的 Auditor 前停止写入并移交，Auditor 返回后收回。Runner 在修改代码或测试前完整执行 `$ponytail:ponytail`，直接建立验证契约、RED/GREEN、最小实现和固定候选，不再创建 Coder。

固定输入实现候选必须由一个 Auditor 执行 `gmgn-v2:code-review`，同时完整执行 `$ponytail:ponytail`。Auditor 可以直接修复权威、Task 和写边界内结论唯一的问题，形成后继候选。行为修复使用冻结 oracle 的 RED→GREEN，纯删除或等价简化使用 GREEN→GREEN。Runner 只验证 Auditor 的修复差异、证据和受影响命令，不进行第二次完整 Review。只有用户或权威明确要求，或一个必要 observable 无法由确定性检查和 Review 证明时，Runner 才创建新的 Auditor 执行 `gmgn-v2:verify`；Verify 不修改候选，失败后由 Runner 形成后继候选并重做被该变化影响的门禁。

Task 行只使用 `pending`、`active`、`blocked`、`closed`、`cancelled`。Architect 创建 `pending` Task；Runner 执行时在 Task branch 记录 `active` 或 `blocked`，最终 PR 候选记录 `closed`；只有该 PR 合入目标分支后 `closed` 才成为权威。合并后的 Task 不重开，后续缺陷创建新 Task。

Runner 在 readiness、实现、测试、finding 修复、rebase 或集成期间发现冲突或其他需要修改上游文档的情况时，创建对应 Project Designer 或 Architect。文档 Agent 完成全局影响分析、Auditor、接受门禁和 document-only PR 后，Runner 从合入目标分支的 commit 重新读取权威并继续；Runner 不自行修改上游含义。

## Milestone 与发布

所有目标 Task 完成并集成后，Close Milestone 建立 `Roadmap 验收标准/交付物 → R/AC → evidence` 闭环，核对 Contract 和实现，直接重放由其负责的组合型 AC 检查，分类 debt 与风险。必要独立 observable 交给 Auditor 执行 `gmgn-v2:verify`。发现实现、测试或 Design 缺口时由 Architect 创建并通过 document-only PR 合入新的 repair Task，Main Session 派发 Runner，修复 PR 合入后重新执行 closure；不重开旧 Task。通过后写入 closure、关闭 Milestone，并记录唯一 accepted_result。

Release 只处理 accepted 固定候选、制品和已授权外部发布动作。必要发布 observable 同样交给 Auditor 执行 `gmgn-v2:verify`。

消息默认只传结果、状态、候选锚点和下一步需要的事实。证据保存在权威文档、Card、Log、测试结果和 Git 中。
