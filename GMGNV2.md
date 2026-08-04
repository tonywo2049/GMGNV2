# GMGN V2

## 目标

GMGN V2 让项目按明确文档推进，每一步可追溯，并在 Task 阶段最大化并行 coding。

权威文档链为：

`WhitePaper → Roadmap → Goal → Requirement → Design → Task`

Decision 记录会影响下游的裁决。Task 之后不再创建 Coding 文档；执行结果写入 Card、Log、代码、测试和 Git 历史。

GMGN V2 不判断项目处于哪个阶段，只判断当前要做什么、所需上游是否存在、能否继续。

## 运行结构

Main Session 接收用户指令时做一次语义路由，使用 `gmgn-v2:write-agent-brief` 生成任务书并启动目标 Agent。启动后，Main Session 只传递用户消息、Agent 问题、状态和结果，不替执行 Agent 做推进决策，也不负责集成。

推进 Task 时，Main Session 机械读取 Task.md：对已接受、未完成、没有未完成 prerequisite、且当前没有活动 Runner 的 Task，各启动一个 Runner。Task 是否真正可执行及后续处理由 Runner 判断。

Agent 按自己的固定职责完成工作，并在需要时直接创建其他 Agent。调用关系不设中央白名单。任何 Agent 创建子 Agent 前，都先使用 `gmgn-v2:write-agent-brief` 生成最小任务书。

## Agent

| Agent | 职责 |
| --- | --- |
| WhitePaper | 在内部完成 Brainstorm，建立或修订 WhitePaper |
| Decision | 记录影响下游的裁决 |
| Roadmap | 把方向拆成有结果和顺序的 Milestone |
| Goal | 定义一个 Milestone 的目标和完成信号 |
| Requirement | 定义可验证的行为、约束和 AC |
| Design | 把 Requirement 转成可实现的设计 |
| Task | 把设计拆成尽可能并行的 Task |
| Runner | 负责一个 Task 从 readiness 到集成的完整执行 |
| Coder | 实现一个固定 Task 候选并提供测试结果 |
| Reviewer | 对固定实现候选执行唯一一次独立 Review |
| Verifier | 对一个固定候选回答一个独立验证问题 |
| Critic | 审查固定文档候选是否满足上游和文档职责 |
| Researcher | 收集一个有边界问题的可核对事实 |
| Close Milestone | 核对 Milestone 完成条件并留档 |
| Release | 发布已接受候选并留档 |

## 文档接受

文档 Agent 创建固定候选后，只创建一个 Critic。Critic 无有效 finding，文档自动接受，不再等待 Owner 审批。存在 finding 时，文档 Agent 修复已接受的 finding，由同一个 Critic 只检查修复及其直接影响；通过后自动接受。

文档 Agent 基于全局权威和影响范围决定修改内容。调用者的任务书只说明触发原因，不限制文档 Agent 只改调用者提到的局部内容。

## 执行与留档

一个 Runner 只负责一个 Task。Runner 直接管理该 Task 的 branch、workspace、子 Agent、冲突裁决和集成。Runner 中断且 Task 未完成时留下可恢复 checkpoint；下一次可以由新的 Runner 继续。

实现候选只做一次完整 Review。Review 可由 Runner 完成，也可在明确需要独立 Review 时交给一个 Reviewer；两者不能重复。修复 finding 后只检查修复及受影响检查，不再执行第二次完整 Review。

只有权威或用户明确要求独立验证，或必要 observable 无法由确定性测试和 Review 证明时，才创建一个 Verifier。一次 Verifier 任务只包含一个触发条件、一个验证问题和一个通过判据。

消息默认只传结果、状态、候选锚点和下一步需要的事实。证据保存在权威文档、Card、Log、测试结果和 Git 中；接收者确实需要立即据此判断时，才在消息中附最小观察。
