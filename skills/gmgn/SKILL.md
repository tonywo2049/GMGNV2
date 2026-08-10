---
name: gmgn
description: Shared runtime rules for GMGN V2 Agents and the Main Session router. Use only when the user explicitly invokes `$gmgn-v2:gmgn`.
---

# GMGN V2 Shared Contract and Router

## Scope

Named Agents apply `Shared Agent rules`. Main Session applies both `Shared Agent rules` and sections marked `Main Session only`. A named Agent's TOML remains the authority for its fixed role.

Main Session activates this router only for the exact user invocation `$gmgn-v2:gmgn`. General requests to create, plan, develop, change, continue, complete, or release a project do not trigger GMGN V2.

## Shared Agent rules

### Repository discovery

- Use DocStar first for cross-document Markdown search.
- Use CodeGraph first for source-code search. If `.codegraph/` is absent and you have write access, initialize it before searching.
- If the current Agent is read-only, CodeGraph is unavailable, or initialization or exploration fails after an actual attempt, record the exact reason and continue with fallback search. Absence alone is not a blocker.

These discovery rules do not apply to Main Session semantic routing. Main Session repository reads are limited to `mechanical Task dispatch`.

### Git baseline and synchronization

These rules apply to named Agents that consume or change a Git-backed repository and to Main Session only during `mechanical Task dispatch`.

Before reading accepted authority, deciding readiness, or creating or resuming a work branch, fix the remote and target branch, run `git fetch <remote>`, and record the commit at `<remote>/<target-branch>`. A local target branch is usable only when its checkout is clean, `git pull --ff-only <remote> <target-branch>` succeeds, and it resolves to that same commit. Otherwise read or create an isolated worktree directly from `<remote>/<target-branch>`. Never base work on an unverified local target branch.

Named Agents push only their owned work branches under the role-specific rules; they never push a shared target branch. Before the first candidate push or merge request, fetch and rebase the owned branch onto `<remote>/<target-branch>`.

Main Session has one shared-target exception during `mechanical Task dispatch`: it may commit and push a mechanical Task.md change whose diff contains only runtime `status`, `execution`, and a reciprocal link to a newly merged Card. Fetch first, use a clean target checkout or isolated worktree, confirm the remote target contains the state commit before creating the next Agent, and never continue from an unpushed local state. If repository policy rejects that push, restore no local fiction and return the exact synchronization blocker.

A request that assigns a Git-backed Project Definition, Requirement, Roadmap, Spec, Design Bundle, Task, or Milestone closure result carries bounded integration authorization for its owning Project Designer, Architect, Runner, or Close Milestone Agent. After the applicable role and repository gates pass, that Agent may push only its owned branch, create or update its single PR, merge under repository policy, and delete the owned remote branch after confirming merge. A required Project Designer or Architect child inherits the same authorization for its document-only branch and PR. Coder and Auditor do not. Do not ask for, require, or pass separate GitHub write or merge authorization. Except for Main Session's mechanical Task.md state commit above, this does not authorize direct pushes to a shared target branch or any Release, publication, tag, deployment, or other external operation.

After merging a PR, the Agent that owns the merge must fetch again, confirm `<remote>/<target-branch>` contains the returned merge commit and merged candidate, then refresh a clean local target branch with a fast-forward-only pull or verify the same remote commit in an isolated worktree. If the shared target checkout is dirty or in use, do not modify it; return its unsynchronized state and the verified remote commit. Do not report successful integration before this remote confirmation. Downstream work always repeats the pre-work fetch and never relies on another Agent's local refresh.

### Outcome ownership

Own the result assigned by the fixed role, including creating, monitoring, and handling every child Agent required by that work. Do not ask Main Session or the caller to perform those responsibilities. Treat questions, status, and blockers sent through the caller as transport, not an ownership transfer.

End the current attempt only when the result is complete, the Owner cancels, required user or external input is unavailable, authorization is missing, the execution scope is invalid, a hard failure prevents continuation, or continuing would be unsafe. Return the exact result, question, or blocker. When blocking input arrives and the scope remains valid, resume the same owning Agent.

Main Session must not take over an Agent's responsibilities or create or manage that Agent's required child Agents. This does not restrict the mechanical dispatch and continuation explicitly assigned to Main Session.

### Agent dispatch

Before creating any Agent, use `$gmgn-v2:write-agent-brief` to prepare the selected Agent's input. This applies to Main Session and named Agents. Do not create or persist a Brief document.

Create an Agent by calling `spawn_agent` directly through the collaboration tool namespace. Never call or search for `spawn_agent` through `functions.exec`, `ALL_TOOLS`, the shell, or another nested tool registry. Its absence from those registries does not mean dispatch is unavailable. Report dispatch capability as unavailable only when the direct `spawn_agent` call itself returns an unavailable or unsupported error; correct recoverable invocation errors and retry, and handle capacity under the rule below.

Create every Agent with `fork_turns: "none"`. Do not omit `fork_turns`, use `"all"`, or pass a positive turn count. Supply the prompt already required by the caller's role; do not rely on inherited conversation history.

After the creation call returns, confirm that dispatch succeeded from a valid returned Agent identifier or canonical task name before treating the Agent as active. If dispatch failed or returned no valid identifier, correct any recoverable invocation error and retry the creation call. Do not call `wait_agent` or `list_agents` for an unconfirmed dispatch. If dispatch cannot succeed after recoverable causes are exhausted because of a hard failure, invalid scope, or unsafe continuation, return the exact blocker.

Capacity exhaustion is a wait condition, not a failed dispatch. Do not immediately retry a capacity rejection. If an active Agent owned by the current work can release a slot, wait under `Agent activity monitoring` and retry only after its terminal event; otherwise return the exact capacity blocker.

### Milestone prerequisite gate

Before creating an Agent for or performing Spec, Design Bundle, Task, implementation, or closure work for a Roadmap Milestone, read the accepted `ROADMAP.md` from the current target-branch commit. A prerequisite Milestone is satisfied only when its status is `closed` and its canonical `accepted_result` is neither empty nor `none` on that same commit. Approval, started work, completed Tasks, a branch, or a PR does not satisfy the prerequisite. A Milestone with prerequisite `none` passes this gate.

If any prerequisite is unsatisfied, do not create the downstream Agent, modify downstream work, or continue the dependent Milestone. Return the target-branch commit and each blocking Milestone's identifier, status, and `accepted_result`. Work on independent Milestones whose prerequisites are satisfied may continue.

### Agent activity monitoring

After dispatching an Agent required by the current work, call `wait_agent({"timeout_ms":600000})`. No other `wait_agent` timeout is permitted for Agent monitoring. If the Agent completes or requests attention before the timeout, handle that event immediately and do not call `list_agents`.

Only when the complete 10-minute wait expires with no event, call `list_agents` once. If the required Agent is still running, first handle other executable work, if any, and then call `wait_agent({"timeout_ms":600000})` again. Do not repeatedly poll, send heartbeat messages, or inspect logs to probe progress.

Do not end the current Task while a required Agent is still running. Call `interrupt_agent` only when the Owner explicitly cancels, the Agent hard-fails, its execution scope is no longer valid, or continuing would be unsafe.

## Main Session only: responsibilities

When receiving a user instruction, select the agent whose fixed responsibility matches the requested outcome. Outside `mechanical Task dispatch`, route from the user's instruction alone; do not read project files or run Git, DocStar, or CodeGraph before dispatch. If the requested outcome is ambiguous, ask the user before dispatch.

Use `$gmgn-v2:write-agent-brief` after selecting the target Agent. For semantic routing, place the user's complete instruction unchanged in the brief's `Objective`; do not restate, summarize, decompose, prioritize, recommend an approach, or add next-step instructions. For mechanical Task dispatch, prepare one brief from each selected Task row under the dispatch rules below instead of passing one plural Task-set request to a Runner.

After dispatch, do not make further semantic decisions about workflow progress. Forward user messages to the active Agent and forward the Agent's questions, material status, and result to the user without paraphrasing, summarizing, interpreting, combining, or adding instructions. Do not interpret an ambiguous approval, confirmation, or selection; forward it unchanged so the owning Agent can request clarification. Perform only mechanical actions within the active request's scope. Main Session does not integrate candidates.

When the active user request is to advance an eligible Task set or complete a Milestone, keep that request active across Runner results and apply the mechanical continuation below. When the user requested only one named Task, still perform the post-completion scan, then report newly dispatchable rows without starting work outside the authorized Task.

## Main Session only: shared Task execution state

Mechanical Task dispatch uses exactly one `Task.md` on the remote target branch. Each Task's `execution/<Task ID>/Card.md` and `Log.md` live in that Task's branch until its PR merges them into the target branch. Runner changes only that Task's implementation, tests, task-local code documentation, Card, Log, and recoverable checkpoint; it never changes Task.md or upstream authority. Architect initializes new rows and may revise Task meaning in its document-only candidate; after acceptance, Main Session is the sole writer of runtime status and execution references.

Persist every Task.md transition through Main Session's mechanical state commit and confirm it on the remote target branch before the next dispatch action. Promote `waiting` to `ready` when all prerequisites are `closed`. Persist `ready → runner-active` before creating or waking Runner; if creation fails, persist the restoration to `ready`. A terminal `architect-required` or `blocked` result is valid only after Runner pushes its Task branch checkpoint, Card, and Log and returns the immutable execution reference `<commit>:execution/<Task ID>/Card.md`. Persist that status and reference without reading Log content. For `Task completed`, first confirm that the remote target merge contains the implementation, tests, Card, and Log, then persist `runner-active → closed` with the merge-commit execution reference. Log is evidence and repair input, never a Main Session routing condition.

Before creating one execution-blocker repair Architect, persist every current `architect-required` row as `architect-active`; those rows and execution references are the fixed batch. If creation fails, persist their restoration to `architect-required`. Main Session continues to persist other Runner results while Architect works; no Task.md freeze or Log replay exists. Architect reads only the fixed Git references, preserves current runtime statuses and execution references in its document candidate, and returns `ready`, `waiting`, or `blocked` for each batch row after its accepted S-D-T change merges. Main Session persists those returned states without semantic interpretation. A later `architect-required` row waits for the next batch.

## Main Session only: semantic routing

| Requested outcome | Agent |
| --- | --- |
| Brainstorm a project, establish or revise its Project Definition or Requirements, or create or revise Roadmap Milestones | `gmgnv2_project_designer` |
| Create or revise Spec/AC, Design Bundle/Contract, or executable Tasks and prerequisites | `gmgnv2_architect` |
| Execute an accepted Task or advance eligible Tasks | Enter `mechanical Task dispatch`; create one `gmgnv2_runner` per authorized dispatchable row |
| Collect facts for one directly requested bounded research question | `gmgnv2_researcher` |
| Critic a fixed document, Review a fixed implementation candidate, or independently verify one observable | `gmgnv2_auditor` |
| Close a completed Milestone | `gmgnv2_close_milestone` |
| Package, publish, or deploy an accepted candidate | `gmgnv2_release` |

A direct coding request with no accepted executable Task goes to `gmgnv2_architect` to form the missing S-D-T authority; with an accepted Task it enters `mechanical Task dispatch`.

Do not infer a project stage and do not route through stage Skills. Auditor routing names the concrete requested action; it does not add a mode or audit_type.

## Main Session only: mechanical Task dispatch

Task execution requests enter `mechanical Task dispatch` before any Runner is created; never create one Runner directly from semantic routing for a Task set. Fetch the remote target branch, read its one approved Task.md, persist mechanically satisfied `waiting → ready` transitions, and dispatch only `ready` rows. Do not route from a local-only Task.md, Task branches, Cards, or Logs. At most 15 Main Session-owned Runners may be `runner-active` at once. Maintain the active count from status transitions; do not call `list_agents` merely to count Runners.

Process `ready` rows in canonical Task-table order. Persist one row as `runner-active`, use `$gmgn-v2:write-agent-brief`, and create its `gmgnv2_runner`; persist `ready` again if creation fails. Continue until 15 rows are `runner-active` or the runtime reports no capacity. If the count is already 15, create no Runner and wait under `Agent activity monitoring`. A capacity rejection ends only the current dispatch pass: restore that row to `ready`, leave later rows unchanged, create no branch, Card, or Log for them, and retry only after a terminal event releases capacity.

Every Main Session-owned Runner terminal result removes one `runner-active` row, persists its returned state and immutable execution reference, and triggers another complete scan. After `Task completed`, require its merged target-branch commit, run `git fetch <remote>`, and confirm `<remote>/<target-branch>` contains that commit and the Card/Log before writing `closed`. For `architect-required` or `blocked`, require the pushed Task-branch commit and execution reference but do not inspect Log content to choose the state. Fill every available slot and repeat until either 15 Runners are active, runtime capacity is exhausted, or a complete scan finds no `ready` row. Do not return or end the active request before this refill reaches one of those conditions.

When a complete scan finds no `ready` row, do not wait for otherwise healthy `runner-active` rows before repairing S-D-T gaps. If at least one row is `architect-required` and none is `architect-active`, persist every current `architect-required` row as `architect-active` and create exactly one `gmgnv2_architect`. Its brief identifies the repository, target-branch commit, and fixed Task.md batch; Architect resolves each execution reference with `git show <commit>:<path>`. Main Session does not read, summarize, select, or interpret Log content.

After the Architect returns, require its accepted target-branch commit and one returned state for every batch row: `ready`, `waiting`, or `blocked`. Persist those states to the remote target before notifying active Runners. A Runner already writing through Coder or Auditor may finish that handoff, but before another authority-dependent handoff, Review, or merge its Task branch must rebase onto that commit and reevaluate only changed authority anchors. Rebase replays and preserves the Task's code, Card, and Log commits; it is not a document-only operation.

For a repaired `ready` Task with a recoverable checkpoint, first wake the original Runner. If it cannot be resumed, create a replacement Runner that reuses the exact Task branch, workspace when available, PR, Card, Log, and checkpoint; never create a second Task branch. Then repeat the complete dispatch scan. A `blocked` row changes only after the user explicitly names that Task and requests retry; set it to `ready` when all prerequisites are `closed`, otherwise `waiting`. If a blocker clears when another Task closes, model it as a prerequisite and `waiting`, not `blocked`. When no active work can change the state, return the exact remaining blocker or missing integration fact. When every row is `closed`, create `gmgnv2_close_milestone` from the verified shared baseline.

If Close Milestone returns a newly accepted repair Task, resume this same scan, dispatch its Runner, and retry Close Milestone after the repair PR merges. Stop after Milestone closure succeeds or an exact unresolved blocker is returned. Never start Release automatically; publication still requires an explicit user request and authorization.
