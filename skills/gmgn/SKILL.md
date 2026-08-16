---
name: gmgn
description: Shared runtime rules for GMGN V2 Agents and the Main Session router. Use only when the user explicitly invokes `$gmgn-v2:gmgn`.
---

# GMGN V2 Runtime Contract and Router

## 1. Shared runtime contract

### 1.1 Accepted authority and Git paths

In each repository, GitHub `origin/main` is the only accepted Git result. Synchronized local `main` is the read and write surface for semantic authority. An immutable snapshot of the latest `origin/main` in an isolated temporary detached worktree is the read and write surface for a mechanical Task runtime transaction. The repository containing Task.md is the authority repository; its `origin/main` is the only accepted document and Task-state authority. An unpushed local commit or uncommitted candidate is not accepted and must not be consumed downstream.

The semantic authority-document path covers Project Definition, ProjectDefinitionLog, Requirements, Roadmap, Spec, Design Bundle, Contracts, Task meaning, Milestone closure records, and their required authority links or semantic status fields. Project Designer, Architect, Close Milestone, and Main Session modify their owned semantic fields directly on local `main`; they do not create an authority-document branch, worktree, or PR. Main Session, Runner, and repair Architect publish only their owned Task runtime fields and Runner's closure link through section 3.2 without a persistent branch or PR.

Only one semantic authority-document writer may own local `main` at a time. Critic temporarily receives that same write ownership while repairing a candidate. Task runtime writers do not wait for that ownership and never edit the shared checkout or local `main`; their isolated transactions are serialized only by the remote branch's fast-forward rule. Task implementation may continue on its own branches while semantic authority work proceeds.

Repository files are read and changed only through local Git state. Never use a GitHub or other remote file API to read, create, update, or delete repository files. Before reading accepted semantic branch content, synchronize its clean local branch and read local files or local Git objects; a Task runtime owner instead reads its fixed latest `origin/main` snapshot under section 3.2. Before changing remote repository content, edit and commit in an owned local workspace and update it from the target branch. Semantic authority pushes only synchronized local `main`; Task runtime pushes only its validated detached transaction commit. PR, check, server-side merge, tag, Release, asset, and deployment operations may reference only commits first created locally and pushed; they never author repository file content.

Before a semantic authority owner reads accepted authority for its result or starts an authority candidate:

1. run `git fetch origin`;
2. switch to local `main`;
3. require a clean worktree;
4. run `git pull --ff-only origin main`;
5. confirm `HEAD` equals `origin/main`;
6. record that commit; and
7. read accepted authority from local `main`.

Runner reads the fixed latest `origin/main` snapshot created by its Task runtime transaction and synchronizes shared local `main` only when the implementation branch or integration path requires it. Auditor, Coder, and Researcher use the fixed commits and work locations supplied by their caller; this rule does not grant them Git operations forbidden by their role.

If the worktree is dirty or cannot fast-forward, do not stash, overwrite, or delete unknown work. Return the exact synchronization gap.

The semantic authority-document owner edits local `main`, completes Critic and any configured approval, commits the accepted candidate locally, and then fetches `origin` again before pushing:

- If `origin/main` did not change, push normally.
- If only Task runtime state, execution references, merged-Card links, or unrelated implementation changed, rebase onto `origin/main`, preserve the latest runtime values, and repeat affected deterministic checks.
- If authority meaning changed, or implementation changed a fact consumed by the candidate, the candidate is stale. Rebuild it from current `origin/main` and repeat every affected writing, Critic, and approval gate. Never resolve a semantic conflict by combining Git conflict text.

Publish a semantic authority commit only after it exists on the checked-out local `main`. Require a clean worktree, `HEAD` equal to local `main`, and push only the local branch with `git push origin main:main`. Never write semantic authority from `HEAD`, a detached commit, another branch, an arbitrary SHA, or a remote file API. A Task runtime transaction is the sole exception: after the section 3.2 checks pass, it pushes its detached commit with `git push origin HEAD:main`.

After pushing, fetch and confirm that `origin/main` contains the commit. A rejected semantic push leaves the local result unaccepted and repeats the synchronization decision above; a rejected Task runtime push follows section 3.2. If repository policy forbids direct pushes to `main`, return that exact blocker; do not create an authority-document or Task-state branch or PR as a fallback.

The implementation path remains branch-based. One Task uses one Runner and one Card/Log pair. Runner owns every branch, worktree, and PR needed in the repositories required by accepted Design; GMGN sets no numeric PR limit. Their fixed commits form one Task candidate, and every branch and PR contains only that Task's allowed delta. An Architect implementation repair may likewise use the branches, worktrees, and PRs required by its fixed repair boundary. Release changes retain their configured branch and PR. Before creating a new Task branch or worktree in an affected repository, fetch `origin`, switch a clean shared checkout to local `main`, run `git pull --ff-only origin main`, confirm local `main` and `origin/main` identify the same commit, and create the branch or worktree from that local `main`. If the shared checkout is dirty or cannot fast-forward, return the exact synchronization gap; do not bypass local `main` by creating the new workspace directly from `origin/main`. Before the first candidate push or any merge, repeat that local `main` synchronization in every affected repository, update each owned branch from the synchronized local `main`, and repeat any invalidated checks.

After merging an implementation PR, the Agent must fetch that repository, switch the clean shared checkout to local `main`, run `git pull --ff-only origin main`, and confirm local `main` and `origin/main` identify the same commit. It then confirms the merge commit and accepted repository delta from local Git state. Remote inspection or verification in an isolated worktree does not replace this local synchronization. Do not report Task integration success until every required merge, local synchronization, and the joint result are confirmed. Each downstream Git owner performs this synchronization itself; non-Git child Agents use the caller-supplied fixed commits rather than another Agent's mutable local state.

Never use `git push --force` on `main`, `git reset --hard`, or `git clean -fd`. A Task-exclusive or Architect-exclusive implementation branch may use `git push --force-with-lease` only when its configured rebase flow requires it.

### 1.2 Document and code search

DocStar and CodeGraph are required discovery paths when available. Their absence from the current environment is the only reason to skip them; record that absence and use native repository search instead.

- Before reading or searching documents, scan them with DocStar.
- Before reading or searching code, use CodeGraph. If its index is missing, initialize it automatically before use.

### 1.2.1 Bounded repository evidence

Minimize model-visible command output without reducing required inspection or validation coverage.

For Git inspection:

1. Fix the authority commit, Card/Log checkpoint, and every repository's baseline and candidate commit once.
2. In each changed repository, inspect the change shape first with bounded metadata: `git diff --name-status <base>...<candidate>`, `git diff --stat <base>...<candidate>`, `git log --format='%H %s' <base>..<candidate>`, and `git diff --check <base>...<candidate>`.
3. Then inspect only the changed paths and hunks needed for the current decision. Start with `git diff -U3 <base>...<candidate> -- <path>` and enlarge the context only when the current hunk is insufficient.
4. Do not emit an unbounded `git diff`, `git show`, or `git log`, and do not start with broad context such as `--unified=80`.
5. Prefer CodeGraph for callers and complete symbol source instead of enlarging a patch to approximate call-path context.
6. Read a required immutable authority document, Card, or Log completely when its applicable Skill requires complete meaning, but do not print unchanged content repeatedly within one Agent.
7. Reuse fixed commit identities, changed-path inventories, and unchanged inspection results. Repeat a command only when any repository candidate changed or a required fresh-state verification demands it.
8. An independent Auditor recomputes the complete multi-repository candidate identity and inspects every included repository delta, but may do so incrementally by repository, changed path, and call path. Complete coverage does not require one unbounded terminal dump.
9. Keep successful check output to its result and necessary summary. On failure, return the relevant failure region rather than unrelated successful output.
10. Do not combine multiple output-heavy inspections into one tool call merely for parallelism.

### 1.3 Agent responsibility

Each Agent owns the result assigned to its fixed role until one of these conditions is met:

- the result is complete;
- an exact question requiring user or external input is returned;
- an exact blocker that prevents continuation is returned;
- the user explicitly cancels;
- the execution scope becomes invalid; or
- continuing would be unsafe.

The Agent creates, waits for, and handles every child Agent required to produce that result.

Main Session and the caller only pass information; they do not take over unfinished responsibility.

When missing input arrives and the scope remains valid, resume the original Agent.

### 1.4 Child Agent dispatch

Before creating any Agent, use `$gmgn-v2:write-agent-brief` to prepare its input. Do not save the Brief as a project document.

Create every Agent with `fork_turns: "none"`; do not rely on inherited conversation history.

Set `task_name` to `<agent_type>_<work_key>`. Copy `agent_type` unchanged so the role remains visible. Derive `work_key` from the shortest stable identifier already present in the brief, preferring a Task ID, Milestone ID, or candidate ID and otherwise using a short objective slug. Normalize it to lowercase letters, digits, and underscores. If the same caller must create another Agent with the same name, append the existing candidate or version identifier, or the next integer.

Treat dispatch as successful only after receiving a valid Agent ID or canonical task name.

When creation fails:

- fix and retry a recoverable invocation error;
- wait for an existing Agent to release capacity when capacity is exhausted;
- return the exact blocker for a hard failure, invalid scope, or unsafe continuation.

Do not wait for or query an Agent whose dispatch was not confirmed.

### 1.5 Agent activity monitoring

Wait for a child Agent only after the current owner has completed every immediately executable action.

During Main Session Task dispatch, finish the current complete scan, including the Runner pass and any eligible Architect repair batch, before waiting.

Main Session may call `wait_agent` while it owns a confirmed Runner or repair Architect dispatch that has not returned, including the interval before that Agent persists its active state. It may also wait while current Task.md contains a `runner-active` or `architect-active` row whose resume dispatch was confirmed. After all confirmed children return and a complete scan dispatches no successor, do not call `list_agents` or `wait_agent`; return immediately.

Use this call for Agent monitoring:

~~~json
wait_agent({"timeout_ms":600000})
~~~

Apply these rules:

1. If the Agent completes or requests attention within ten minutes, handle the event immediately and do not call `list_agents`.
2. Only after a full ten-minute wait returns no event, call `list_agents` once.
3. If the Agent is still running, first handle any other immediately executable work, then call `wait_agent({"timeout_ms":600000})` again.
4. Use no other monitoring timeout.
5. Do not repeatedly poll with `list_agents`.
6. Do not send empty heartbeat messages.
7. Do not infer activity from execution records.

Do not end the owning work while a required Agent is still running.

Interrupt an Agent only when:

- the user explicitly cancels;
- the Agent hard-fails;
- its execution scope is no longer valid; or
- continuing would be unsafe.

After `interrupt_agent` succeeds, do not call `wait_agent` or `list_agents` for that Agent; `previous_status` is its pre-interruption status. Continue immediately with cleanup, checkpointing, or blocker reporting.

### 1.6 Milestone prerequisites

Before starting Spec, Design Bundle, Task, Task implementation, or Milestone closure work, read the approved `ROADMAP.md`.

Work may start when:

- the Roadmap is approved;
- the current Milestone exists in the Roadmap; and
- every prerequisite Milestone recorded in the Roadmap is complete.

A prerequisite of `none` passes directly.

When a prerequisite is incomplete, do not start the dependent Milestone. Return the blocking Milestone ID and current status.

Independent work that does not depend on that Milestone may continue.

## 2. Main Session routing

### 2.1 Semantic routing

| Requested result | Target Agent |
| --- | --- |
| Discuss project direction; establish or revise Project Definition, Requirement, or Roadmap | `gmgnv2_project_designer` |
| Create or revise Spec, AC, Design Bundle, Contract, Task, or prerequisites | `gmgnv2_architect` |
| Execute accepted Tasks or advance dispatchable Tasks | Enter the Task state machine and create one `gmgnv2_runner` for each dispatchable Task |
| Research one bounded factual question | `gmgnv2_researcher` |
| Critic a fixed document candidate, Review a fixed implementation candidate, or Verify one observable | `gmgnv2_auditor` |
| Close a completed Milestone | `gmgnv2_close_milestone` |
| Package, publish, or deploy an accepted candidate | `gmgnv2_release` |

For a direct coding request:

- when an executable accepted Task exists, enter the Task state machine;
- otherwise send the request to `gmgnv2_architect` to complete the missing Spec, Design, and Task authority.

Do not infer a project stage from guesses.

An Auditor brief sets `Audit Skill:` to exactly one of:

- `$gmgn-v2:critic`;
- `$gmgn-v2:code-review`; or
- `$gmgn-v2:verify`.

Do not combine these actions in one Auditor.

### 2.2 Routing steps

1. Identify the requested result from the user's instruction.
2. When necessary, read the minimum project state needed to confirm whether an accepted Task or fixed candidate exists.
3. Ask the user if the target result remains ambiguous.
4. Select the target Agent.
5. Use `$gmgn-v2:write-agent-brief`.
6. Create the Agent and confirm dispatch.

Main Session does not perform Project Designer, Architect, Runner, Auditor, Close Milestone, or Release work through their stage Skills.

### 2.3 Main Session information passing

After dispatch, Main Session:

- passes user additions to the active Agent;
- passes the Agent's questions, material status, and result to the user;
- performs only the readiness state changes defined by this contract; and
- resumes scanning and dispatch after any Runner or repair Architect returns.

Do not change meaning or add a new objective while passing information.

Main Session does not modify, Review, repair, or merge a named Agent's candidate.

When the user asks to advance a Task set or complete a Milestone, that request remains active after a Runner returns and Main Session continues the Task state machine.

When the user requests only one named Task, scan Task.md after that Task completes, but report other dispatchable Tasks without starting them.

## 3. Task runtime state machine

### 3.1 State source

The only accepted source of Task runtime state is one `Task.md` on `origin/main`; every state owner fetches `origin` and reads one fixed latest `origin/main` snapshot before acting. An implementation, Card/Log, semantic-authority, or stale shared-checkout copy is never a Task runtime source.

After Task.md is accepted, each transition has one writer:

- Main Session changes `waiting` or explicitly retried `blocked` rows to `ready` only after applying the readiness rule;
- Runner owns its row's `runner-active`, `architect-required`, `closed`, `execution`, and closure-time reciprocal Card link; and
- the repair Architect owns its fixed batch's `architect-active`, `waiting`, `blocked`, Log checkpoints, and `execution`.

No other role modifies Task runtime fields. Main Session never reconstructs an Agent-owned state from returned prose.

Each Task's execution material lives at:

~~~text
execution/<Task ID>/Card.md
execution/<Task ID>/Log.md
~~~

Card and Log are created on the Task's execution-record branch in the authority repository. They enter that repository's `origin/main` only after their PR merges. Implementation, tests, and Task-local code documentation may merge through other PRs owned by the same Runner; Log fixes every included repository baseline, candidate commit, PR, and final merge commit. Runner owns the execution-record branch until it persists `architect-required`, then transfers that branch to the fixed repair Architect. Architect updates Log without changing Card's execution-contract meaning and releases the branch when it persists `waiting` or `blocked`.

`execution` uses an immutable reference:

~~~text
<commit>:execution/<Task ID>/Card.md
~~~

This representation does not change after merge; only `<commit>` advances. The commit fixes the complete Card/Log checkpoint even when only Log changed. Task.md stores current state and this pointer, Card stores the execution contract, and Log stores the complete multi-repository candidate and execution evidence.

Main Session dispatches Tasks using only these Task.md fields:

- Task ID;
- `status`;
- prerequisite; and
- `execution`.

### 3.2 State persistence

Each persisted state update is one isolated optimistic transaction:

1. fetch `origin` over SSH and fix the latest `origin/main` commit;
2. create an owned temporary detached worktree at that commit without switching the shared checkout or local `main`;
3. read Task.md from that snapshot and confirm every target Task ID, expected old state, and consumed semantic cells still match;
4. if semantic cells changed, re-evaluate the Task before writing; never carry a stale completion or handoff across changed Task meaning;
5. modify only fields owned by that writer:
   - runtime status;
   - execution reference; and
   - Runner's reciprocal link to a newly merged Card;
6. confirm the complete transaction diff contains only those mechanical fields, then commit it locally;
7. fetch `origin` again immediately before publication;
8. when `origin/main` still identifies the transaction parent, publish with `git push origin HEAD:main` without force;
9. when `origin/main` advanced or the push is rejected, start a fresh transaction from the new `origin/main`, repeat the expected-state and semantic checks, and reapply only the owned field changes; never combine semantic conflict text;
10. fetch and confirm that `origin/main` contains the accepted transaction commit; and
11. remove only the owned temporary worktree after confirmation, then perform dependent work or return the result.

Multiple Agents may prepare transactions concurrently. The remote fast-forward rule accepts one linear `main` update at a time; every rejected writer rebases by fresh replay rather than waiting for another Agent's complete work. If the expected state changed, do not overwrite it. If repository policy rejects direct `main` writes, do not continue from local-only state or create a state branch; return the exact synchronization blocker.

One dispatch scan may persist all deterministic `waiting → ready` transitions in one commit. Runner and Architect update `execution` whenever a new durable Card/Log commit supersedes the current recovery point; ordinary Log edits that do not become the recovery point require no Task.md update.

### 3.3 State transitions

| From | To | Writer | Condition |
| --- | --- | --- | --- |
| `waiting` | `ready` | Main Session | The row passes the readiness rule |
| `blocked` | `ready` | Main Session | The user explicitly requests retry and the row passes the readiness rule |
| `blocked` | `waiting` | Main Session | The user explicitly requests retry and the row does not yet pass the readiness rule |
| `ready` | `runner-active` | Runner | Runner starts or resumes and claims the row before doing Task work |
| `runner-active` | `closed` | Runner | Every required repository merge, local synchronization, joint validation, and merged Card/Log are confirmed |
| `runner-active` | `architect-required` | Runner | An unresolved issue remains outside Runner's safe write boundary and the latest available execution checkpoint is recorded |
| `architect-required` | `architect-active` | Architect | The fixed repair Architect starts and claims the complete batch before repair work |
| `architect-active` | `waiting` | Architect | Repair is complete and Main Session must reapply the readiness rule |
| `architect-active` | `blocked` | Architect | Safe in-scope repair is exhausted and user or external input, permission, environment, or a safe scope decision is still required |

Persist and confirm a transition on `origin/main` before performing work that depends on it.

### 3.4 Dispatch scan

Only one Main Session advances a given Task.md execution set. On initialization and every scan trigger, Main Session:

1. fetches `origin`, fixes the latest `origin/main` commit, and reads Task.md from that immutable snapshot;
2. changes every `waiting` row that passes the readiness rule to `ready`, and on explicit user retry changes each named `blocked` row to `ready` or `waiting` by one section 3.2 transaction;
3. processes each current `ready` row once in canonical table order;
4. uses `$gmgn-v2:write-agent-brief`, resumes the original Runner when section 3.7 applies, and otherwise creates one `gmgnv2_runner`, without changing the row;
5. retains the confirmed Task-to-Runner identity in the current Main Session, including across Architect repair, so a later scan neither duplicates an unclaimed Runner nor replaces a resumable one;
6. leaves a row `ready` when creation fails and continues the scan without immediate retry;
7. fixes every current `architect-required` row as one batch when no repair Architect dispatch is outstanding and no row is `architect-active`;
8. uses `$gmgn-v2:write-agent-brief` and creates one `gmgnv2_architect` for that batch without changing the rows; and
9. waits only after the complete Runner and Architect dispatch pass finishes.

There is no configured Runner concurrency limit and no active-row count. Runtime capacity failure leaves the affected row unchanged for the next scan trigger. Existing or newly dispatched Runners do not defer an eligible Architect batch. Rows that become `architect-required` after the batch is fixed wait for the next repair Architect.

### 3.5 Runner-owned state

Runner claims a new dispatch with `ready → runner-active` before creating or resuming execution artifacts. A resumed Runner may continue from its own existing `runner-active` row. It rejects any other state and never returns `blocked`.

After each durable Card/Log push that becomes the current recovery point, Runner persists its immutable `execution` reference before dependent work continues. When an issue remains outside Runner's safe write boundary, Runner updates Log, pushes every available checkpoint, persists `runner-active → architect-required` and the latest valid `execution`, releases the execution-record branch, and only then returns. A local checkpoint is never represented as remotely durable.

After every required implementation merge, local synchronization, and joint validation succeeds and the Card/Log PR merges last, Runner uses one section 3.2 transaction to persist `runner-active → closed`, replace `execution` with the Card merge reference, and add the reciprocal Task.md-to-Card link. It confirms that transaction on `origin/main` and only then returns `Task completed`.

If an authority-state write itself cannot be persisted, Runner retains the actual current state and returns the exact persistence blocker; Main Session does not translate that return into a new state.

When such a Runner returns while its row remains `runner-active`, Main Session resumes that Runner after the persistence condition changes and creates a replacement only when the original cannot resume.

### 3.6 Architect batch repair

When at least one `architect-required` row exists, no row is `architect-active`, and no repair Architect dispatch is outstanding, Main Session:

1. fix every current `architect-required` row as this batch;
2. use `$gmgn-v2:write-agent-brief` to create one `gmgnv2_architect`; and
3. provide the authority repository, affected repositories, fixed `origin/main` commits, fixed Task.md, execution-record branches, and fixed batch.

If Architect creation fails, the batch remains `architect-required`.

Architect first persists every fixed row as `architect-active`. It directly repairs every issue in the batch without creating a repair Task or Runner. It uses independent workspaces for implementation repair, never modifies a Runner implementation branch or workspace, and temporarily owns each batch Task's execution-record branch only to update Log. It does not change Card's outcome, completion conditions, or validation contract.

Architect changes only the minimum required:

- normative documents such as Spec, Design, Contract, or Task;
- code;
- tests;
- configuration; or
- build and CI.

Architect creates the Auditor required by the actual candidate and sets `Audit Skill:` in its brief:

- use `$gmgn-v2:critic` for a normative document candidate;
- use `$gmgn-v2:code-review` for a code, test, configuration, build, or CI candidate;
- use `$gmgn-v2:verify` only when deterministic checks and Review cannot prove a necessary observable.

One Auditor performs one audit type. When repair requires both normative and implementation changes, finish and push the normative candidate to authority `origin/main` first, then create the required implementation repair branches from the resulting repository baselines.

After integrating the repair, Architect updates each Task's Log and pushes a new execution-record checkpoint. It then persists the new `execution` and one state for every batch Task:

- `waiting` when repair is complete so Main Session can reapply the readiness rule; or
- `blocked` only after Architect exhausts safe in-scope diagnosis and repair and still lacks user or external input, required permission, required environment, or a safe scope decision.

Only Architect may persist `blocked`. Its Log and return include the exact cause, completed actions, required human action, and retry condition. Architect confirms every state commit on authority `origin/main`, releases the execution-record branches, and only then returns. Any `architect-required` row that appears while Architect works waits for the next batch.

When Architect returns an authority-state persistence blocker while a batch row remains `architect-active`, Main Session resumes the same Architect after the condition changes; it does not infer a final row state.

Pass the new accepted commit to active Runners. Each Runner decides whether changed authority requires rebase, validation-contract updates, or repeated invalidated checks.

### 3.7 Resume and retry

For a repaired Task that Main Session has changed from `waiting` to `ready` and that has a recoverable checkpoint:

1. resume the original Runner first;
2. create a replacement Runner only when the original cannot resume;
3. make the replacement reuse the original:
   - Card/Log branch;
   - repository branches;
   - available workspaces;
   - PRs;
   - Card;
   - Log; and
   - checkpoint;
4. never replace a still-valid branch or PR merely because work resumed; record any necessary successor branch or PR in Log after its predecessor merged, closed, or became unusable.

A `blocked` Task changes only when the user explicitly names that Task and requests retry.

On retry:

- change it to `ready` when the row passes the readiness rule;
- otherwise change it to `waiting`.

When another Task's completion will naturally clear a condition, model it as a prerequisite and `waiting`, not `blocked`.

### 3.8 Scan stop conditions

Run a complete scan on initialization, after any Runner returns, after the repair Architect returns, and when the user explicitly requests continue, resume, or retry. Do not rescan merely because an Agent persisted an active state, updated `execution`, sent progress, or because a timer elapsed. If several results are already queued, handle them and scan once.

Main Session stops advancing only when:

- a complete scan has finished and confirmed child Agents can still change state, in which case Main Session waits;
- a dispatch failed and no confirmed child Agent remains to trigger another scan;
- no `ready` row exists, no Architect repair batch is dispatchable under section 3.6, and no active work can change state;
- no active work can change state and an exact blocker was returned; or
- every Task is `closed`.

### 3.9 Milestone closure

When every Task is `closed`, create `gmgnv2_close_milestone`.

If Close Milestone returns a newly accepted repair Task:

1. keep the current user request active;
2. re-enter Task dispatch;
3. execute and integrate the repair Task; and
4. create Close Milestone again after that Task closes.

The flow ends when:

- Milestone closure succeeds; or
- an exact unresolved blocker is returned.

Main Session never starts Release automatically. Packaging, publication, or deployment requires an explicit user request and the applicable authorization.
