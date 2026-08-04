---
name: write-agent-brief
description: Use immediately before creating any GMGN V2 agent. Produce the smallest complete task brief for the already-selected target agent without routing work or copying its stable instructions.
---

# Write Agent Brief

The caller has already selected the target Agent. This Skill only prepares that Agent's input.

## Method

1. Identify the selected Agent and its requested outcome.
2. Gather the applicable inputs from the contract below. Resolve choices owned by the caller before dispatch.
3. Draft the brief using only applicable fields from the compact form.
4. Apply the deletion test to every line.
5. Pass the resulting brief directly as the Agent input. Do not save a Brief document.

## Compact form

```text
目标 Agent：
目标：
当前事实：
权威锚点：
工作位置与写入边界：
已确定选择与授权：
返回：
```

Omit empty fields. An anchor is normally a path, section, Task ID, commit, or candidate identifier. Do not copy evidence that the Agent can read from that anchor.

## Deletion test

Delete a brief item unless removing it would prevent the selected Agent from performing its fixed responsibility or producing the requested return.

In particular, delete:

- stable workflow already defined by the target Agent;
- work owned by the caller or another Agent;
- unrelated history, explanation, inventories, and speculative checks;
- duplicated facts and evidence already available through an anchor;
- extra objectives, assurance, or adjacent risks not required for the return.

The brief is a trigger and current input, not a restriction on a document Agent's global impact analysis.

## Target input contracts

| Agent | Inputs needed when applicable |
| --- | --- |
| `gmgnv2_whitepaper` | user objective; existing WhitePaper anchor; known constraints or unresolved owner choices |
| `gmgnv2_decision` | ruling question; affected authority; existing Decision anchor; decision scope |
| `gmgnv2_roadmap` | accepted WhitePaper and relevant Decision anchors; current Roadmap; requested planning outcome |
| `gmgnv2_goal` | Milestone identifier; accepted Roadmap anchor; current Goal; requested outcome |
| `gmgnv2_requirement` | accepted Goal anchor; affected users or behavior; current Requirement; known constraints |
| `gmgnv2_design` | accepted Requirement anchors; repository or system context; current Design and Contract anchors |
| `gmgnv2_task` | accepted Requirement and Design anchors; current Task document; requested decomposition or change |
| `gmgnv2_runner` | one Task ID and row anchor; upstream anchors; recorded Task state; repository baseline; existing branch or workspace; external-operation authorization |
| `gmgnv2_coder` | fixed Task and Card anchors; workspace and baseline; allowed write boundary; acceptance checks; requested candidate return |
| `gmgnv2_reviewer` | fixed candidate identifier or exact diff; authority anchors; relevant test surface; requested finding format |
| `gmgnv2_verifier` | fixed candidate; exactly one recorded trigger; one independent question; authority-defined observable and pass condition; available environment |
| `gmgnv2_critic` | fixed document candidate; document type; upstream anchors; requested finding format; for follow-up, prior findings and repair delta |
| `gmgnv2_researcher` | one bounded fact question; source and time limits; required output format |
| `gmgnv2_close_milestone` | Milestone anchor; its Task and integration status; recorded completion conditions; required aggregate checks |
| `gmgnv2_release` | accepted candidate; version and release target; existing evidence; publication or deployment authorization |

Do not add missing inputs that do not apply. If a required current fact cannot be found or resolved, return that single gap to the caller instead of inventing it.
