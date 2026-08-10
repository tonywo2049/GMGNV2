# GMGN V2

## 目标

GMGN V2 让项目按明确文档推进，每一步可追溯，并在 Task 阶段最大化并行 coding。

权威文档链为：

`Project Definition + Requirements → Roadmap → Spec → Design Bundle → Task`

纳入文档图的 Markdown 使用 DocStar `gmgn-v2` 机器接口：固定英文 frontmatter 键和稳定 M/R/D/C/T ID。Task PR 合入前，Task.md 用不可变 Git 引用 `<commit>:execution/<Task ID>/Card.md` 指向 Card；合入后由 Main Session 添加真实 Task/Card 互反链接，Card 链接 Log，Log 链接 `latest_event`。Requirement 使用 `type: requirement`，以自然语言和稳定章节锚点维护当前产品基线；Spec 使用 `type: spec` 和 R/AC ID。机器接口不规定正文目录。项目已有本地 conventions 时使用该完整配置，否则显式选择 `gmgn-v2`；不与 `gmgn-v1` 叠加。DocStar 只证明结构，不决定语义接受或 Milestone 关闭。

Project Definition 是项目根权威；Requirements 在其范围内持续维护当前 accepted 产品需求、产品规格和明确 TBD。Roadmap 从当前 accepted 上游分配完整达成 Milestone 和必要的前置增量；无关 TBD 不阻塞推进，影响当前范围的 TBD 必须先回到 Requirement 解决。Spec 只把已分配且含义充分明确的内容转成 R/AC，不增加产品语义。`ProjectDefinitionLog.md` 只记录 Project Definition 的 accepted 变更。Task 之后不再创建 Coding 文档；执行结果写入 Card、Log、代码、测试和 Git 历史。不存在 Goal 文档。

每个 Task 由 Runner 使用一个独立 branch、worktree 和 PR；Codex 环境默认使用 `codex/<Task ID>-<short-description>`。新 Task 从 GitHub 最新目标分支创建；Task branch 只提交当前 Task 的代码、测试、Task-local 代码文档、Card、Log 和可恢复 checkpoint，不修改 Task.md 或上游权威。PR 合入且 Runner 确认目标分支包含代码、测试、Card 和 Log 后，Runner 在返回 `Task completed` 前直接删除该 Task 的 worktree、本地 branch 和远端 branch。其他问题另建 Task。Auditor 只形成审查结论或受限修复，不 commit、push、rebase、操作 PR 或合并。

远端跟踪引用 `<remote>/<目标分支>` 是 GitHub 最新性的依据。消费 accepted authority、判断 readiness、创建或恢复工作 branch 前必须执行 `git fetch <remote>` 并记录该 commit；本地目标分支只有在 clean、可通过 `git pull --ff-only <remote> <目标分支>` 快进且 SHA 相同时才能作为基线，否则直接使用该远端引用的隔离 worktree。命名 Agent 只 push 自己拥有的工作 branch，不直接 push 共享目标分支；唯一例外是 Main Session 可把仅含 Task.md 运行时状态、execution 引用和新合入 Card 互反链接的机械提交 push 到目标分支，并在下一次派发前确认远端已包含它。完整候选通过必要门禁后才作为候选 push；Runner 只可为返回 `architect-required` 或 `blocked` 提前 push Card、Log 和 checkpoint。Task branch 跟进目标分支使用 fetch 和 rebase。PR 合并后由合并者再次 fetch，确认远端目标分支包含返回的 merge commit 和候选，再快进 clean 的本地目标分支或在隔离 worktree 核对同一 commit；本地 checkout dirty 或被占用时不得修改，必须返回未刷新状态和已核对的远端 commit。下游仍须自行重新 fetch，不依赖其他 Agent 的本地刷新。每个 Task 只有一个 PR，默认 squash merge；rebase 后确需改写远端时只用 `--force-with-lease`，不得使用无保护的 force push。
Project Designer 和 Architect 各自把一个语义 change set 放入一个独立 document-only branch 与 PR：前者默认 `codex/project-design-<short-description>`，后者默认 `codex/<Milestone ID>-sdt-<short-description>`。候选通过各自接受门禁后才 push；PR 合入目标分支后才成为下游可消费的 active authority。两者不直接提交或 push 共享分支。

多个 Architect 可以基于各自固定的目标分支 commit 并行工作。每个候选记录缺口、消费的 accepted authority 锚点和准备修改的文档锚点，且不得写入 Runner 的 Task branch 或 workspace。合并前重新 fetch：Task 行仅运行时状态、execution 引用或新合入 Card 链接变化时 rebase 并保留最新值；语义权威锚点变化时，候选立即失效，不得把语义冲突当作 Git 文本冲突合并。Architect 必须从最新 accepted authority 重新判断：缺口已解决就关闭候选，不合并；缺口仍存在就只重建剩余差异，并重新执行受影响的写作、Critic 和接受门禁。

同一 Architect trigger 先按 S-D-T 顺序完成全部适用文档，再固定一个完整语义候选并只创建一个 Critic；执行阻塞修复批次覆盖固定 Task.md 批次内全部 `architect-active` 行，不按 Task 或文档层拆分候选。Design 调研由未解决的外部实现事实触发，不由文档变化或 blocker 数量触发；方向已经 accepted 时只核对该方案的实现模式和可复用源码，不重新搜索替代方案。

GMGN V2 不判断项目处于哪个阶段，只判断当前要做什么、所需上游是否存在、能否继续。

## 运行结构

每个命名 Agent 的 TOML 都在工作前强制读取 [`gmgn` Skill 的 Shared Agent rules](skills/gmgn/SKILL.md#shared-agent-rules)，但不应用其中标记为 Main Session only 的章节。仓库发现、职责所有权、Agent 派发和父子 Agent 活动监测只在该处定义，不复制进 Agent TOML 或子 Agent 任务书。Agent 直接创建、监测和处理自身工作所需的子 Agent；经调用者传递问题、状态或 blocker 不转移职责。创建 Agent 时必须显式使用 `fork_turns: "none"`，并从创建调用返回的有效 Agent 标识确认派发成功；未成功时修正可恢复的调用问题后重试，未确认前不进入监测。槽位不足是等待条件，不是派发失败；存在可释放槽位的活动 Agent 时等其结束，否则返回精确容量 blocker，不立即重试。监测只使用 `wait_agent({"timeout_ms":600000})`，不允许其他 timeout、短轮询或心跳检查。结果完成或出现取消、必要输入或授权缺失、范围失效、硬失败或不安全等精确 blocker 时，可以结束当前执行；blocker 解除后由原 Agent 继续。

Roadmap Milestone 只使用 `open` 和 `closed`：Project Designer 初始化为 `open` 与 `accepted_result: none`；只有 Close Milestone 在同一次关闭修改中写入 `closed` 和一个非空的唯一 `accepted_result`；关闭后不重开。prerequisite 只有在目标分支同一 accepted commit 上满足该关闭状态时才算完成。此前不得为依赖它的 Milestone 创建或推进 Spec、Design Bundle、Task、实现或关闭工作；批准、Task 完成、branch 或 PR 都不能代替 Milestone 正式关闭。没有 prerequisite 的独立 Milestone 不受阻塞。

只有用户明确调用 `$gmgn-v2:gmgn` 才启用 Main Session Router；普通项目请求不触发 GMGN V2。启用后，Main Session 只按固定职责选择目标 Agent；除 Task 机械派发外，只根据用户指令路由，派发前不读取项目文件，也不运行 Git、DocStar 或 CodeGraph。每次创建 Agent 前，Main Session 都使用 `gmgn-v2:write-agent-brief`：语义路由把用户完整原话放入 `Objective`，不生成摘要、拆解、优先级、方案或下一步指令；Task 派发则按每个已选 Task 分别生成任务书。启动后，Main Session 原样转发用户消息与 Agent 的问题、状态和结果，不改写、总结、解释、合并或附加指导，也不负责集成；含糊的批准、确认或选择由负责该语义的 Agent 澄清，Main Session 不代替解释。Main Session 不代替 Agent 履行职责或创建、管理其工作所需的子 Agent；这不限制 Main Session 自身已明确规定的机械派发和续派发。

推进 Task 集合或完成 Milestone 时，Main Session 只读取远端目标分支的 approved Task.md：满足 prerequisite 的 `waiting` 机械变为 `ready`，按表顺序把 `ready` 改为 `runner-active`，提交、push 并确认远端状态后再创建 Runner，同时最多保留 15 个 `runner-active`。创建失败也要持久化恢复 `ready`。Runner 结束后返回 `Task completed`、`architect-required` 或 `blocked` 以及不可变 execution 引用；Main Session 写入远端后重新扫描，其中 `closed` 必须先 fetch 并确认远端目标分支包含 merge commit、Card 和 Log。Main Session 不读取 Log 来选择下一 Agent。

没有 `ready` Task 时，只要存在 `architect-required` 且没有 `architect-active`，Main Session 就把全部当前 `architect-required` 改为 `architect-active` 并启动唯一修复 Architect，不等待其他 Runner。Architect 合入修复后为每个批次行返回 `ready`、`waiting` 或 `blocked`，由 Main Session 照抄。`blocked` 只有在用户明确指定该 Task 并要求重试时才恢复；所有 Task 都在同一目标分支 `closed` 时启动 Close Milestone。Release 永不自动启动。

Main Session 或任何 Agent 创建 Agent 前，都先使用 `gmgn-v2:write-agent-brief` 生成最小任务书，且不把 Shared Agent rules 复制进任务书。固定候选任务书必须写明绝对工作位置、固定候选标识和精确写入边界。Project Designer 只在产品方向仍需形成或检验时使用 Brainstorm；它维护可持续修订的 Requirement 基线，明确 TBD 只阻塞依赖它的范围；它先通过一次一个关键问题收集到足以形成准确搜索的问题、用户与场景、期望结果和待定决定，再询问用户参考并只研究能改善下一步产品问题的外部实践。明确的用户决定直接进入写作。Researcher 完整执行 `gmgn-v2:research`，可按调用者给定维度综合事实，但不推荐或选择。Architect 维护 S-D-T。Auditor 不使用 mode；它根据具体任务分别读取 Critic、Code Review 或 Verify Skill，由所读 Skill 决定是否可以形成后继候选。

## Agent

| Agent | 职责 |
| --- | --- |
| Project Designer | 必要时用外部参考辅助 Brainstorm 提出针对性问题，建立或修订 Project Definition、Requirements 与 Roadmap，并执行各自批准门禁 |
| Architect | 把 Roadmap 分配和适用 Requirements 转成 Spec、Design Bundle 和尽可能并行的 Task |
| Researcher | 执行 research Skill，为一个有边界的问题收集并按授权综合可核对证据，不作决策 |
| Runner | 负责一个 Task 的 readiness、Card/Log、Coder/Auditor 调度、验证和集成 |
| Coder | 在 Runner 的 Task workspace 中按任务书编写测试和代码，并形成固定候选 |
| Auditor | 根据具体任务读取 critic、code-review 或 verify；前两者可受限修复，verify 保持候选只读 |
| Close Milestone | 汇总 Task 和证据，重放组合验收，关闭 Milestone 并留档 |
| Release | 发布 accepted 候选并留档 |

## 文档接受

Project Designer 为其配置的文档候选创建 Auditor；Architect 则在同一 trigger 的全部适用 Spec、Design Bundle、Contract 和 Task 修改完成后，为完整固定候选创建一次 Auditor，并要求其执行 `gmgn-v2:critic`。结果能由 accepted authority 唯一确定，且可证明不改变含义、范围、所有权、接受状态、分配、依赖、验证点或 Task 边界的机械修改，由文档负责人直接执行确定性检查；Task 行的机械状态变化不独立触发 Critic。无法证明时按语义修改处理。Critic 先从 accepted authority 独立重建完整候选的义务，再主动检查遗漏、矛盾、多种合理解释、跨文档一致性、失败边界和下游可执行性；格式、链接和 DocStar 等机械检查只是证据，不能形成语义 pass。Critic 负责直接修复写入边界内的全部 material finding，并自行检查修复差异和执行适用机械检查；文档负责人不修复 finding，也不审查 Critic 的修复。缺少产品决定时，Critic 在写作 Skill 允许且不影响当前工作继续的情况下写入边界明确的显式 `TBD`；否则返回一个准确的用户或上游决定问题，文档负责人只原样转交问题和答案，同一 Critic 根据答案完成修改与验证。只有最终候选通过时 Critic 才返回 pass。每个新建或语义修订的 Project Definition 和 Requirement 都需要一次 Critic pass 与一次用户明确批准；Roadmap 首次接受需要相同门禁，后续语义修订在 Critic pass 后自动接受。Architect 的完整 S-D-T 语义候选在一次 Critic pass 后自动接受。在 Git-backed 项目中，两者都必须把各自 document-only PR 合入目标分支，目标 commit 才是下游 active accepted authority。

Project Designer 只修改 Project Definition、ProjectDefinitionLog、Requirements 和 Roadmap；一个 Project Design PR 只包含这四类文档，并在合入前闭合其拥有的所有现存直接互链。其文档 PR 合入后，Architect 才从该目标分支 commit 更新受影响的既有 S-D-T；缺失下游只有在用户目标明确包含继续形成下游时才创建。

## Task 执行

一个 Runner 只负责一个 Task，并管理其 workspace；任一时刻只能有一个写入者。Runner 建立验证契约后创建一个 `luna+max` Coder，并把 workspace 写入权移交给它。Coder 从任务书出发，按需查找实现信息，在修改代码或测试前完整执行 `$ponytail:ponytail`，完成 RED/GREEN、最小实现和固定候选。Runner 收回写入权并验证候选，但不编写或审查代码；非机械候选再交给 Auditor，机械候选记录证据后跳过 Code Review。

改变行为或无法证明为机械修改的 Coder 候选必须由一个 Auditor 执行 `gmgn-v2:code-review`。只有完整差异可证明不改变运行行为、接口、依赖、数据、构建、安全、兼容性、并发和资源行为时，Runner 才能记录依据并跳过 Review。Code Review 从任务书出发，按需查找判断所需信息，追踪真实调用与失败路径，并用可能错误的实现检验测试是否有效。Auditor 同时完整执行 `$ponytail:ponytail`；测试、CI 和 Ponytail 都只是证据。现有 Task 和写边界已唯一确定的 finding 由 Auditor 直接修复。需要产品、架构、API、依赖或 Task 范围决定时，Coder 和 Auditor 都无权猜测；Runner 先交给对应文档 Agent，决定合入后再创建 Coder 候选。Runner 只验证 Auditor 的修复差异和受影响命令，不进行第二次完整 Review。

Task 行只使用 `waiting`、`ready`、`runner-active`、`architect-required`、`architect-active`、`blocked`、`closed`。Architect 按 prerequisite 把新 Task 初始化为 `ready` 或 `waiting`；接受后只有 Main Session 修改远端 Task.md 的运行时状态和 execution 引用。Runner 和 Architect 返回结构化结果，Main Session 不作语义判断。Log 只保存证据和修复细节，不参与路由。合并后的 `closed` Task 不重开，后续缺陷创建新 Task。

Runner 发现 S-D-T 决定缺失时停止相关工作，把 checkpoint、Card 和 Log commit 并 push 到 Task branch，再返回 `architect-required`、commit 和 `<commit>:execution/<Task ID>/Card.md`；不得自行创建 Architect、猜测决定或把 Task.md 未记录的其他 Task 当作 prerequisite。Main Session 只按 Task.md 状态启动修复 Architect；Architect 用 `git show <commit>:<path>` 读取证据。修复合入后，原 Runner 或复用相同 branch、workspace、PR、Card、Log 和 checkpoint 的替代 Runner 继续。

Coder 候选只记录实际使用的项目文档位置及目标分支 commit。Code Review 前和 Task PR 合并前重新 fetch；任一位置发生相关变化时，候选失效，Runner 更新 Card 与验证契约，并创建新的 Coder 候选。基于过期设计的实现不能合并。

## Milestone 与发布

所有目标 Task 完成并集成后，Close Milestone 建立 `Requirement/Project Definition → Roadmap 分配与验收标准/交付物 → Spec R/AC → evidence` 闭环，复用仍绑定当前 commit 的 Task Review、Card、Log、测试和集成证据，不重放 Task 执行。它只重放明确交由 closure 的组合型 AC 或缺失、失效的 Milestone 级确定性检查，只证明当前 Milestone 获分配的增量和声明边界。必要独立 observable 交给 Auditor 执行 `gmgn-v2:verify`。发现实现、测试、Design 或 Contract 缺口时只记录失败 observable 与受影响锚点，由 Architect 按固定状态机创建并合入新的 repair Task；Close Milestone 不直接修改 Design 或实现。Main Session 在 repair Task `ready` 后派发 Runner，修复 PR 合入后重新执行 closure；不重开旧 Task。通过后写入 closure、关闭 Milestone，并记录唯一 accepted_result。

Release 只处理 accepted 固定候选、制品和已授权外部发布动作。必要发布 observable 同样交给 Auditor 执行 `gmgn-v2:verify`。

消息默认只传结果、状态、候选锚点和下一步需要的事实。证据保存在权威文档、Card、Log、测试结果和 Git 中。
