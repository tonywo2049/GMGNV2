# GMGN V2

GMGN V2 是面向 Codex 的 Agent 驱动研发工作流。它用文档保证需求明确和过程可追溯，并让独立 Task 并行执行。

核心设计见 [GMGNV2.md](GMGNV2.md)。

## 安装

1. 将本仓库作为本地 Codex 插件安装。
2. 安装命名 Agent：

```bash
python3 skills/gmgn/scripts/install_codex_agents.py
```

V2 使用 `gmgn-v2` 插件名和 `gmgnv2_*` Agent 名，不覆盖 GMGN V1。

## 使用

从 `$gmgn-v2:gmgn` 开始。Main Session 会根据用户当前指令选择 Agent；创建任何 Agent 前，使用 `$gmgn-v2:write-agent-brief` 生成任务书。

## 验证

```bash
python3 tests/validate_repository.py
python3 -m unittest discover -s tests
```
