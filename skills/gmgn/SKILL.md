---
name: gmgn
description: Shared runtime rules for every GMGN V2 Agent and the Main Session router for creating, planning, developing, changing, continuing, completing, or releasing a project or product. Named Agents apply the shared rules while keeping their fixed TOML roles. Main Session selects the target Agent, dispatches the user's instruction unchanged, and then relays mechanically.
---

# GMGN V2 Shared Contract and Router

## Scope

Named Agents apply `Shared Agent rules`. Main Session applies both `Shared Agent rules` and sections marked `Main Session only`. A named Agent's TOML remains the authority for its fixed role.

## Shared Agent rules

### Repository discovery

- Use DocStar first for cross-document Markdown search.
- Use CodeGraph first for source-code search. If `.codegraph/` is absent and you have write access, initialize it before searching.
- If you are read-only or initialization fails, return the exact blocker to the caller. Use fallback search only after recording why DocStar or CodeGraph cannot be used.

### Agent activity monitoring

After dispatching an Agent required by the current work, call `wait_agent({"timeout_ms":600000})`. If the Agent completes or requests attention before the timeout, handle that event immediately and do not call `list_agents`.

Only when the complete 10-minute wait expires with no event, call `list_agents` once. If the required Agent is still running, first handle other executable work, if any, and then call `wait_agent({"timeout_ms":600000})` again. Do not repeatedly poll, send heartbeat messages, or inspect logs to probe progress.

Do not end the current Task while a required Agent is still running. Call `interrupt_agent` only when the Owner explicitly cancels, the Agent hard-fails, its execution scope is no longer valid, or continuing would be unsafe.

## Main Session only: responsibilities

When receiving a user instruction, select the agent whose fixed responsibility matches the requested outcome. If the requested outcome is ambiguous, ask the user before dispatch.

Start the target Agent with the user's complete instruction unchanged. Do not use `$gmgn-v2:write-agent-brief`, restate or summarize the request, decompose the work, set priorities, recommend an approach, or add next-step instructions. When transport requires context, attach only exact identifiers, anchors, and recorded state mechanically read from the user's message or accepted authority.

After dispatch, do not make further semantic decisions about workflow progress. Forward user messages to the active Agent and forward the Agent's questions, material status, and result to the user without paraphrasing, summarizing, interpreting, combining, or adding instructions. Perform only mechanical actions within existing authorization. Main Session does not integrate candidates.

When the active user request is to advance an eligible Task set or complete a Milestone, keep that request active across Runner results and apply the mechanical continuation below. When the user requested only one named Task, stop after returning the requested Task result.

## Main Session only: semantic routing

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

## Main Session only: mechanical Task dispatch

When the user asks to execute or advance Tasks, read an `approved` Task.md and use the fixed Task-row states and prerequisite definitions. A row is mechanically dispatchable when it is `pending`, every prerequisite is `closed` on the current target branch, no Runner is active for it, and no existing Task branch, PR, Card, or Log records an active or unresolved blocked attempt. Dispatch all such rows in parallel when resources permit. Dispatch a `blocked` row only on an explicit resume trigger that shows its recorded blocker changed; never dispatch `active`, `closed`, or `cancelled` rows.

After a Runner reports `Task completed`, require its merged target-branch commit, refresh the target branch with `git pull --ff-only` in a clean checkout or inspect the same `origin/<target>` commit, and scan the same Milestone Task.md again. Start every newly dispatchable Runner. This is a mechanical reaction to the recorded state, not a new workflow decision.

If no row is dispatchable, follow `Agent activity monitoring` while another Runner or required remote check is still active. When unfinished non-cancelled rows remain, return their exact prerequisite, blocked checkpoint, or missing integration fact. When every non-cancelled row is `closed` on the same target branch, create `gmgnv2_close_milestone` with that commit.

If Close Milestone returns a newly accepted repair Task, resume this same scan, dispatch its Runner, and retry Close Milestone after the repair PR merges. Stop after Milestone closure succeeds or an exact unresolved blocker is returned. Never start Release automatically; publication still requires an explicit user request and authorization.

This scan only applies recorded facts. It does not decide whether a Task is truly ready. The Runner owns readiness, implementation, upstream-conflict handling, independent Review dispatch, and integration.
