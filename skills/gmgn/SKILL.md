---
name: gmgn
description: Use first when the user wants to create, plan, develop, change, continue, complete, or release a project or product. Also use for product ideas, project decisions, milestones, requirements, designs, task breakdown, task execution, milestone closure, and releases. Determine the requested outcome, prepare the target agent's brief, dispatch that agent, and then relay without taking over workflow decisions.
---

# GMGN V2 Router

## Main Session responsibilities

When receiving a user instruction, determine its meaning and select the agent whose fixed responsibility matches the requested outcome. If the requested outcome is ambiguous, ask the user before dispatch.

Before every dispatch, use `$gmgn-v2:write-agent-brief` to create the target Agent's task brief. Pass that brief directly as the Agent input. Do not create or persist a Brief document.

After dispatch, do not make further semantic decisions about workflow progress. Relay user answers and instructions to the active Agent, and relay the Agent's questions, material status, and result to the user. Perform only mechanical actions within existing authorization. Main Session does not integrate candidates.

## Semantic routing

| Requested outcome | Agent |
| --- | --- |
| Establish or substantially rethink the problem, goals, scope, or WhitePaper | `gmgnv2_whitepaper` |
| Record or revise a ruling that affects downstream work | `gmgnv2_decision` |
| Create or revise Milestones and their ordering | `gmgnv2_roadmap` |
| Initiate or revise one Milestone goal | `gmgnv2_goal` |
| Define or revise behavior, constraints, stories, or acceptance criteria | `gmgnv2_requirement` |
| Create or revise architecture, interfaces, data, errors, or implementation design | `gmgnv2_design` |
| Decompose or revise executable Tasks and prerequisites | `gmgnv2_task` |
| Execute eligible Tasks | `gmgnv2_runner` |
| Close a completed Milestone | `gmgnv2_close_milestone` |
| Package, publish, or deploy an accepted candidate | `gmgnv2_release` |
| Directly requested bounded research, document critique, code review, verification, or coding | the matching specialist Agent |

Do not infer a project stage and do not route through stage Skills.

## Mechanical Task dispatch

When the user asks to execute or advance Tasks, read Task.md and use its recorded status and prerequisite definitions. For each Task that is accepted, unfinished, has no unfinished prerequisite, and has no active Runner, create one `gmgnv2_runner`. Dispatch all such Tasks in parallel when resources permit.

This scan only applies recorded facts. It does not decide whether a Task is truly ready. The Runner owns that decision and any resulting action.
