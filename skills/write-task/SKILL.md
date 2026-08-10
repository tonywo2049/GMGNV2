---
name: write-task
description: Create or semantically revise Task.md from accepted Spec/AC and a complete Design Bundle. Use to split implementation and its required verification into stable, independently executable, verifiable, integrable, and maximally parallel results with only real prerequisites.
---

# Write Task

## Preserve its role

Treat Task.md as the normative Milestone execution index downstream of accepted Spec/AC and the complete Design Bundle. It records what independent results must be delivered, not how to implement them.

## Keep the DocStar machine surface

Use the English frontmatter keys `locale`, `purpose`, `upstream`, `downstream`, `status`, `type`, and `nature`, with `type: task` and `nature: normative`. Write frontmatter values as plain unquoted text; keep multiple Markdown links comma-separated on one unquoted line. Use real relative Markdown links or explicit unquoted `none`, and keep existing `upstream`/`downstream` edges reciprocal. Link the root Design upstream. Link a Task Card downstream only after its Task PR merges that Card into the target branch; Main Session may add that newly valid reciprocal link in the same mechanical closure update. Use only `draft`, `pending-approval`, `approved`, or `closed` for document `status`.

Keep a new or semantic document candidate `draft`; change its document `status` to `approved` only after the configured Critic and automatic-acceptance gate pass. A caller-classified mechanical edit preserves the current document status. Task-row status remains the execution state and is separate.

Use `T<n>`, `T<n>.<n>`, `M<n>-T<n>`, or `M<n>-T<n>.<n>` IDs. Keep exactly one shared canonical Task table with `| # | task | spec anchor | prerequisite | status | execution |`; write every first-column ID as `| **<Task ID>** |`. Task entities outside it are not authoritative. A dispatched Task has one `execution/<Task ID>/Card.md` and `Log.md` pair in its Task branch, and that pair merges through the Task PR. Its `execution` cell is `none` before a durable remote checkpoint exists, then the immutable Git object reference `<commit>:execution/<Task ID>/Card.md`.

When DocStar is available, use its `gmgn-v2` conventions and run its structural check before handoff; do not combine a discovered project-local conventions file with `--preset gmgn-v2`. Structural results do not decide Task boundaries or acceptance.

Keep the table:

| # | task | spec anchor | prerequisite | status | execution |
| --- | --- | --- | --- | --- | --- |

Replace current status and execution values instead of appending history. Execution contains only `none` or the current immutable Card reference.

## Keep one Task-row state machine

Use only `waiting`, `ready`, `runner-active`, `architect-required`, `architect-active`, `blocked`, or `closed` in the Task-row `status` column:

- Architect initializes a new Task as `ready` when every prerequisite is `closed`, otherwise as `waiting`.
- After the Task document is accepted, Main Session is the sole writer of runtime status, execution references, and a reciprocal link to a newly merged Card. Runner and Architect return the requested next status and evidence; Main Session persists it without semantic interpretation.
- Main Session changes `waiting` to `ready` when every prerequisite is `closed`.
- Main Session changes `ready` to `runner-active` immediately before creating or waking its Runner; if creation fails, restore `ready`.
- Main Session changes `runner-active` to `architect-required` when Runner returns that exact status for a missing S-D-T decision, or to `blocked` when Runner returns an exact non-S-D-T blocker and the condition for retry.
- Main Session changes `runner-active` to `closed` only after confirming the returned Task implementation commit on the remote target branch.
- Main Session changes every current `architect-required` row to `architect-active` immediately before creating one repair Architect; if creation fails, restore `architect-required`.
- After the repair is accepted, Architect returns `ready`, `waiting`, or `blocked` for each input row and Main Session persists it. Architect removes an unclosed Task row when accepted authority removes that result.
- Main Session changes `blocked` only after the user explicitly names that Task and requests retry. It becomes `ready` when every prerequisite is `closed`, otherwise `waiting`.

A `closed` Task never reopens; a later defect requires a new Task.

A Task-row runtime transition, execution-reference update, or newly valid merged-Card reciprocal link uniquely determined by this state machine is mechanical and does not independently trigger Critic. When the same Architect change set also revises Task meaning, result boundaries, anchors, or prerequisites, include those semantic Task deltas in the one integrated S-D-T candidate reviewed after all affected layers are complete.

Main Session mechanically dispatches only `ready` rows. The current shared Task-row status is authoritative: Log content is evidence and repair input, never a routing condition. Never dispatch any other state.

Keep semantic Task meaning and current execution state in the one shared canonical table. Card and Log are Task-specific execution evidence owned in the Task branch and merged through its PR. Task-branch changes contain only implementation, tests, task-local code documentation, Card, Log, and recoverable checkpoints; they never change Task.md or upstream authority.

## Split by independent results

Each Task names one necessary result that, after its prerequisites are satisfied:

- can be executed as an independent unit;
- has one clear pass/fail completion result;
- can be verified and integrated independently; and
- cannot be split into two or more results that each still satisfy these conditions.

Apply the split test repeatedly. Task count is not a simplicity target.

Map every in-scope AC to at least one Task. A Task may cover related AC, and an AC may require multiple Tasks, but coverage does not replace the split test.

Prefer result boundaries over activity or discipline boundaries. Do not split implementation, tests, documentation, or review into separate Tasks when they jointly prove one delivered result.

## Carry verification with the result

Map every required Design verification point to the Task that delivers the result it verifies. The Task result includes the minimum implementation and verification artifacts needed to satisfy that authority; code existing without its required check is not a complete result. The only exception is a composite AC that needs no new implementation or test asset and whose Design names sufficient existing executable checks for close-milestone replay.

Create a separate verification Task only when the Design defines an independently deliverable shared result, such as a cross-implementation conformance suite, reusable test harness, simulator, or migration verifier, and that result independently passes the split test. Do not create generic Tasks named write tests, add coverage, QA, review, or validation.

For every composite AC, identify whether an existing Task or accepted integration gate owns the joint result. If deciding the complete result requires an independent implementation or test asset, create one integration Task that passes the normal Task boundary. Otherwise create no extra Task and leave the exact existing check links, real entry point, and environment to close-milestone for direct replay.

Task.md links the applicable verification authority but does not copy cases or choose commands, fixtures, frameworks, coverage percentages, or evidence locations. Runner turn that authority into the executable verification contract for the fixed Task.

## Preserve real parallelism

Prerequisite records only a true dependency on another delivered result and forms an acyclic graph.

Runtime provider-to-consumer data flow, implementation of the same accepted interface, or a shared approved Contract does not create implementation order. Provider and consumer Tasks remain parallel when accepted authority lets each be completed, verified, and integrated independently. Add a prerequisite only when the later Task's result cannot exist or be judged before the earlier delivered result physically exists.

Do not use ordinary code dependency, likely file overlap, Git conflict, staffing, scheduling, conservative order, or execution waves as prerequisites. Keep all independent results as separate parallel Tasks; runtime dispatch does not change the Task boundary.

## Keep execution detail out

Each spec anchor uses exact provided Project Definition, R/AC, Design, and applicable Contract anchors for the Task result. Do not invent a path or anchor; return a precise missing anchor instead. Do not copy upstream meaning.

Do not put validation cases, commands, file scopes, locks, blockers, candidates, review notes, evidence, progress narrative, implementation steps, or execution history in Task.md. The execution cell's immutable Card reference is its only implementation commit reference.

Delete work without a current AC or accepted Design owner. Do not create tentative, placeholder, speculative, or future Tasks.

## Create or revise

For a new Milestone execution index, cover every in-scope AC and accepted Design result. For a semantic revision, inspect the whole Task graph, preserve unaffected stable IDs and states, update every affected mapping and prerequisite, remove invalid work, and do not change rows whose meaning is unaffected.

## Check before handoff

- Every Task traces to accepted R/AC and Design authority.
- Every row passes the independent result and repeated split tests.
- All in-scope AC and Design results are covered without ownerless work.
- Every required Design verification point belongs to its delivered result or to a justified independent shared verification result.
- Every composite AC has an owning Task or integration gate, or an explicit close-milestone replay path using existing checks.
- An integration Task exists only when the composite result needs an independent implementation or test asset.
- Implementation and its required checks have not been split into activity-only Tasks.
- Runtime data flow and accepted shared interfaces have not been mistaken for Task prerequisites.
- Every spec link is a real provided anchor, not a fabricated path.
- Prerequisites are real result dependencies and the graph is acyclic.
- Independent coding work remains maximally parallel.
- Task.md contains only the execution index, current status, and execution entry links.
- Every Task row uses the fixed state machine; only Main Session's remote merge confirmation permits `runner-active → closed`.
- Task-branch changes contain only the current Task's implementation, tests, task-local code documentation, Card, Log, and checkpoints.
- Task IDs and frontmatter satisfy the DocStar `gmgn-v2` machine surface; an unmerged execution reference is a Git object anchor, while a merged Card uses a real reciprocal Markdown link.
