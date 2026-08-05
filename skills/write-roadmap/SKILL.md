---
name: write-roadmap
description: Create or semantically revise ROADMAP.md from an accepted ProjectDefinition.md. Use to split the whole project into result-oriented Milestones whose acceptance criteria and deliverables directly guide later Requirement Specs and R/AC, without schedules, effort estimates, performance targets, or implementation detail.
---

# Write Roadmap

## Preserve its role

Treat `ROADMAP.md` as the direct normative upstream of Requirement. It allocates the accepted Project Definition into implementation stages that can each be completed and accepted without redefining project intent.

Write in the project's language for readers who do not share the conversation context. Choose the structure that best explains this project's stages. Do not impose a fixed outline or template.

## Keep the DocStar machine surface

Use the English frontmatter keys `locale`, `purpose`, `upstream`, `downstream`, `status`, `type`, and `nature`, with `type: roadmap` and `nature: normative`. Write frontmatter values as plain unquoted text; keep multiple Markdown links comma-separated on one unquoted line. Use real relative Markdown links or explicit unquoted `none`, and keep existing `upstream`/`downstream` edges reciprocal. The accepted Project Definition is the upstream; link an existing Requirement as downstream, but do not link a missing future document. Use only `draft`, `pending-approval`, `approved`, or `closed` for document `status`.

Use `M<n>` for each Milestone, `M<n>-AC<n>` for its acceptance criteria, and `M<n>-D<n>` for its deliverables. Define each machine ID once in its own list item under a heading that clearly names its kind, and bold only the ID. These identifiers do not prescribe the document outline or heading order.

When DocStar is available, use its `gmgn-v2` conventions and run its structural check before handoff; a project-local conventions file and `--preset gmgn-v2` are alternatives, not layers. Structural results do not decide semantic acceptance.

## Split by accepted results

Build a complete Milestone graph from the accepted Project Definition. Each Milestone must provide:

- a stable identifier or anchor;
- the Project Definition scope and project-level user E2E scenarios it covers;
- the stage result, value, and scope boundary;
- explicit acceptance criteria that make stage completion decidable;
- the deliverables that must exist when those criteria pass;
- only real result prerequisites, or an explicit `none`;
- current status and one canonical `accepted_result`, initially `none`.

Acceptance criteria are mandatory for every Milestone. State observable product, user, operational, or organizational results. Keep them specific enough for Requirement to derive detailed R/AC, but do not turn the Roadmap itself into a Requirement document or test plan.

Cover every in-scope Project Definition capability and project-level user E2E scenario. Split stages by independently valuable, acceptable outcomes rather than code modules, teams, or technical steps. Preserve parallel Milestones when no real prerequisite exists; ordering, numbering, or display position does not create a dependency.

## Hand off to Requirement

Treat each Milestone's acceptance criteria and deliverables as direct owners for later Requirement Specs and R/AC. Preserve stable anchors and enough boundary information for the Architect to determine what behavior must be specified without inventing stage intent.

Do not define detailed behavior, edge cases, thresholds, or Requirement-level R/AC here. If a Milestone acceptance criterion requires that detail, state the result that must be decidable and leave its behavioral specification to Requirement.

## Exclude planning and implementation detail

Do not include dates, deadlines, durations, release windows, staffing, workload, velocity, effort estimates, schedule forecasts, `now | next | later`, or implementation-efficiency and runtime-performance targets. Real result prerequisites and logical stage order remain valid.

Do not add a separate Backlog. Do not include detailed R/AC, technical design, Tasks, test cases, evidence, or implementation steps. Do not invent scope outside the accepted Project Definition.

## Create or revise

For a new Roadmap, allocate the whole accepted Project Definition. For a semantic revision, preserve unaffected Milestones and anchors, update every affected allocation or dependency, remove invalid stages, and recheck complete Project Definition and E2E coverage.

Set the candidate document status to `pending-approval`; change it to `approved` only after explicit user approval.

## Check before handoff

- Every Milestone has explicit, decidable acceptance criteria and required deliverables.
- All in-scope Project Definition capabilities and project-level user E2E scenarios are covered once without conflicting ownership.
- Every dependency is a real prerequisite and the graph is acyclic; independent work remains parallel.
- Requirement can trace each later R/AC to a Milestone acceptance criterion or deliverable.
- No time, effort, efficiency, detailed Requirement, design, Task, test, evidence, or implementation content has leaked into the Roadmap.
- A revision preserves unaffected meaning and identifies its real downstream impact.
- Every Milestone, criterion, and deliverable has one DocStar-compatible definition, and the seven frontmatter fields and reciprocal links are valid.
