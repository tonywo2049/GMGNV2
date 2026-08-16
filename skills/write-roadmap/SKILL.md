---
name: write-roadmap
description: Create or semantically revise ROADMAP.md from an accepted ProjectDefinition.md and accepted Requirement documents. Use to allocate the current accepted product baseline into result-oriented Milestone increments whose acceptance criteria and deliverables guide later Spec and R/AC, while leaving unrelated Requirement TBDs open and recording concise future items in a Backlog.
---

# Write Roadmap

## Preserve its role

Treat `ROADMAP.md` as the allocation authority between the accepted Project Definition plus Requirements and each Spec. It assigns the current accepted product obligations to stages that can each be completed and accepted without redefining product meaning.

Write in the project's language for readers who do not share the conversation context. Choose the structure that best explains this project's stages. Do not impose a fixed outline or template.

## Keep the DocStar machine surface

Use the English frontmatter keys `locale`, `purpose`, `upstream`, `downstream`, `status`, `type`, and `nature`, with `type: roadmap` and `nature: normative`. Write frontmatter values as plain unquoted text; keep multiple Markdown links comma-separated on one unquoted line. Use real relative Markdown links or explicit unquoted `none`, and keep existing `upstream`/`downstream` edges reciprocal. Link the accepted Project Definition and every applicable accepted Requirement upstream, and existing Specs downstream; do not link missing future documents. Use only `draft`, `pending-approval`, `approved`, or `closed` for document `status`.

Use `M<n>` for each Milestone, `M<n>-AC<n>` for its acceptance criteria, and `M<n>-D<n>` for its deliverables. Define each machine ID once in its own list item under a heading that clearly names its kind, and bold only the ID. These identifiers do not prescribe the document outline or heading order.

When DocStar is available, use its `gmgn-v1` preset and run its structural check before handoff; a project-local conventions file and `--preset gmgn-v1` are alternatives, not layers. Structural results do not decide semantic acceptance.

## Split by accepted results

Build a complete Milestone graph from the accepted Project Definition and Requirements. Each Milestone must provide:

- a stable identifier or anchor;
- the Project Definition anchors, Requirement sections or stable anchors, and project-level user E2E scenarios it covers;
- the stage result, value, and scope boundary;
- the allocated increment, whether it first establishes or completely satisfies the upstream obligation, and the claim boundary of that result;
- adjacent accepted Requirements explicitly deferred to another named Milestone when omission could be mistaken for cancellation or contrary behavior;
- explicit acceptance criteria that make stage completion decidable;
- the deliverables that must exist when those criteria pass;
- only real result prerequisites, or an explicit `none`;
- Milestone status using only `open` or `closed`, initially `open`, and one canonical `accepted_result`, initially `none`.

Project Designer initializes every Milestone as `open`. Only Close Milestone changes `open` to `closed`, in the same closure change that replaces `accepted_result: none` with one non-empty canonical result. A closed Milestone never reopens; later corrective work belongs to a new Milestone or an accepted extension allocated by Roadmap revision.

Acceptance criteria are mandatory for every Milestone. State observable product, user, operational, or organizational results. Keep them specific enough for Spec to derive detailed R/AC, but do not turn the Roadmap itself into a Requirement or Spec document.

Allocate every currently accepted Project Definition capability, project-level user E2E scenario, and Requirement outcome. One Milestone must own complete satisfaction of each accepted outcome; earlier Milestones may own named, independently decidable increments. For each increment, state which upstream meaning is selected and which meaning remains deferred. Do not allocate a TBD as if it were decided. If a TBD or ambiguity affects the current allocation, return it to `$gmgn-v2:write-requirement`; leave unrelated TBDs open and continue.

Split stages by independently valuable, acceptable outcomes rather than code modules, teams, or technical steps. Preserve parallel Milestones when no real prerequisite exists; ordering, numbering, or display position does not create a dependency. Deferral permits a capability to be absent in an earlier stage; it never authorizes a public behavior that contradicts accepted Requirements.

## Keep a future Backlog

Include a `Backlog` section. Write each future item as one concise list item and use `none` when there are no future items. Do not add acceptance criteria, deliverables, dependencies, status, priority, schedule, design, Tasks, tests, or evidence to a Backlog item.

A Backlog item records future intent only. It does not change the accepted Project Definition or authorize Requirement, Design, or Task work. Before implementation, add the item to the accepted Project Definition scope when necessary, convert it into a Milestone, and remove it from the Backlog in the same Roadmap revision.

## Hand off to Spec

Treat each Milestone's source allocation, acceptance criteria, and deliverables as the direct stage input for later Spec and R/AC. Preserve stable anchors and enough boundary information for the Architect to translate only the allocated natural-language requirements into R/AC without inventing stage intent.

Do not add product behavior, edge cases, thresholds, or R/AC here. If a Milestone needs product meaning that accepted Requirements do not provide, return that gap to `$gmgn-v2:write-requirement`; Spec may formalize accepted meaning but may not supply it.

## Exclude planning and implementation detail

Do not include dates, deadlines, durations, release windows, staffing, workload, velocity, effort estimates, schedule forecasts, `now | next | later`, or implementation-efficiency and runtime-performance targets. Real result prerequisites and logical stage order remain valid.

Do not include detailed R/AC, technical design, Tasks, test cases, evidence, or implementation steps. Do not invent Milestone scope outside the accepted Project Definition or Requirements, and do not copy their full behavior into the Roadmap.

## Create or revise

For a new Roadmap, allocate the whole accepted Project Definition and every accepted Requirement. For a semantic revision, preserve unaffected Milestones and anchors, update every affected allocation or dependency, remove invalid stages, and recheck complete upstream coverage.

Set a document that has never received explicit user approval to `pending-approval`; change it to `approved` only after its first explicit approval. Keep a later semantic revision of a previously approved document `draft` while writing and reviewing it, then return it to `approved` after Critic pass without another approval. A caller-classified mechanical edit preserves the current document status.

## Check before handoff

- Every Milestone has explicit, decidable acceptance criteria and required deliverables.
- Every Milestone is `open` with `accepted_result: none` or `closed` with one non-empty canonical `accepted_result`; only Close Milestone performs that transition.
- All currently accepted Project Definition capabilities, project-level user E2E scenarios, and Requirement outcomes have one complete-satisfaction owner without conflicting ownership; incremental owners and claim boundaries are explicit.
- No TBD is allocated as decided, and an unrelated TBD does not block other accepted scope.
- No Milestone omission authorizes behavior contrary to an accepted Requirement, and any test-only seam is clearly outside the product contract.
- Every dependency is a real prerequisite and the graph is acyclic; independent work remains parallel.
- Spec can trace each later R/AC through a Milestone allocation and acceptance criterion or deliverable to its Requirement section or Project Definition anchor.
- The Backlog contains only concise future items, and no Backlog item is treated as accepted scope or downstream authority.
- No time, effort, efficiency, detailed Requirement, design, Task, test, evidence, or implementation content has leaked into the Roadmap.
- A revision preserves unaffected meaning and identifies its real downstream impact.
- Every Milestone, criterion, and deliverable has one DocStar-compatible definition, and the seven frontmatter fields and reciprocal links are valid.
