---
name: gmgn
description: Use first when the user wants to create, plan, develop, change, continue, complete, or release a project or product. Also use for product ideas, project decisions, milestones, requirements, designs, task breakdown, task execution, milestone closure, releases, document critique, code review, or independent verification. Determine the requested outcome, prepare the target agent's brief, dispatch that agent, and then relay without taking over workflow decisions.
---

# GMGN V2 Router

## Main Session responsibilities

When receiving a user instruction, determine its meaning and select the agent whose fixed responsibility matches the requested outcome. If the requested outcome is ambiguous, ask the user before dispatch.

Before every dispatch, use `$gmgn-v2:write-agent-brief` to create the target Agent's task brief. Pass that brief directly as the Agent input. Do not create or persist a Brief document.

After dispatch, do not make further semantic decisions about workflow progress. Relay user answers and instructions to the active Agent, and relay the Agent's questions, material status, and result to the user. Perform only mechanical actions within existing authorization. Main Session does not integrate candidates.

When the active user request is to advance an eligible Task set or complete a Milestone, keep that request active across Runner results and apply the mechanical continuation below. When the user requested only one named Task, stop after returning the requested Task result.

## Semantic routing

| Requested outcome | Agent |
| --- | --- |
| Brainstorm a project, establish or revise its Project Definition, or create or revise Roadmap Milestones | `gmgnv2_project_designer` |
| Create or revise Requirement/AC, Design Bundle/Contract, or executable Tasks and prerequisites | `gmgnv2_architect` |
| Execute an accepted Task or advance eligible Tasks | `gmgnv2_runner` |
| Collect facts for one directly requested bounded research question | `gmgnv2_researcher` |
| Critic a fixed document, Review a fixed implementation candidate, or independently verify one observable | `gmgnv2_auditor` |
| Close a completed Milestone | `gmgnv2_close_milestone` |
| Package, publish, or deploy an accepted candidate | `gmgnv2_release` |

A direct coding request with no accepted executable Task goes to `gmgnv2_architect` to form the missing R-D-T authority; with an accepted Task it goes to `gmgnv2_runner`.

Do not infer a project stage and do not route through stage Skills. Auditor routing names the concrete requested action; it does not add a mode or audit_type.

## Mechanical Task dispatch

When the user asks to execute or advance Tasks, read an `approved` Task.md and use the fixed Task-row states and prerequisite definitions. A row is mechanically dispatchable when it is `pending`, every prerequisite is `closed` on the current target branch, no Runner is active for it, and no existing Task branch, PR, Card, or Log records an active or unresolved blocked attempt. Dispatch all such rows in parallel when resources permit. Dispatch a `blocked` row only on an explicit resume trigger that shows its recorded blocker changed; never dispatch `active`, `closed`, or `cancelled` rows.

After a Runner reports `Task completed`, require its merged target-branch commit, refresh the target branch with `git pull --ff-only` in a clean checkout or inspect the same `origin/<target>` commit, and scan the same Milestone Task.md again. Start every newly dispatchable Runner. This is a mechanical reaction to the recorded state, not a new workflow decision.

If no row is dispatchable, wait while another Runner or required remote check is still active. When unfinished non-cancelled rows remain, return their exact prerequisite, blocked checkpoint, or missing integration fact. When every non-cancelled row is `closed` on the same target branch, create `gmgnv2_close_milestone` with that commit.

If Close Milestone returns a newly accepted repair Task, resume this same scan, dispatch its Runner, and retry Close Milestone after the repair PR merges. Stop after Milestone closure succeeds or an exact unresolved blocker is returned. Never start Release automatically; publication still requires an explicit user request and authorization.

This scan only applies recorded facts. It does not decide whether a Task is truly ready. The Runner owns readiness, implementation, upstream-conflict handling, independent Review dispatch, and integration.
