---
name: write-project-definition
description: Create or semantically revise ProjectDefinition.md and append its accepted change history to ProjectDefinitionLog.md. Use after project brainstorming has established the project's direction and mandatory external research. Keep the document as the top-level source for Roadmap-Requirement-Design Bundle-Task work without imposing a fixed section layout or template.
---

# Write Project Definition

## Preserve its role

Treat `ProjectDefinition.md` as the project's root normative source. It defines the project at a macro level so Roadmap-Requirement-Design Bundle-Task documents can derive their own detail without inventing project intent.

Write in the project's language for readers who do not share the conversation context. Select the organization, headings, prose, tables, and anchors that best express this project's meaning. Do not apply a fixed outline, field list, ID scheme, or template.

## Keep the DocStar machine surface

For every graph-governed Markdown document, keep the English frontmatter keys `locale`, `purpose`, `upstream`, `downstream`, `status`, `type`, and `nature`. Write frontmatter values as plain unquoted text; keep multiple Markdown links comma-separated on one unquoted line. Use only real relative Markdown links or an explicit unquoted `none`; whenever an existing edge changes, update both `upstream` and `downstream`. Do not link a missing future document.

Use `type: project-definition`, `nature: normative` for `ProjectDefinition.md`, and `type: project-definition-log`, `nature: descriptive` for `ProjectDefinitionLog.md`. Use only `draft`, `pending-approval`, `approved`, or `closed` for document `status`. This machine surface does not prescribe headings, section order, prose shape, or Project Definition anchors.

When DocStar is available, use its `gmgn-v2` conventions for the corpus and run its structural check before handoff; use a discovered project-local conventions file instead of also passing a preset. Treat the result as structural evidence, never semantic approval.

## Preserve the required meaning

Make the document clearly establish all of the following, wherever and however they fit best:

- the project's vision, goals, positioning, intended users, and problem or opportunity;
- the project's functional scope and the relative priority of that scope;
- project-level user E2E success scenarios that identify the user and context, starting trigger, critical usage chain, and observable user outcome;
- external project references, including both references supplied by the user and projects discovered independently;
- external technical references that show what can be reused or learned instead of rebuilt;
- what the project explicitly will not do;
- material project-level constraints, assumptions, open questions, or principles needed to interpret the above and guide downstream work.

Use only external facts and source anchors returned by the completed Brainstorm and its Researchers. Do not research, add, or infer new external facts while writing. Return a precise evidence gap when required support is missing.

For each external reference, preserve a verifiable source and enough explanation to show its relevance, applicable boundary, and lesson. Keep supporting detail to the minimum needed for the project choice. Distinguish evidence from project choices: an external project or technology is not automatically a requirement.

Use technical references to identify reusable prior art and project-level constraints. Leave provider, version, interface, data, and algorithm choices to Design unless one is already an explicit project boundary.

Project-level user E2E scenarios are product acceptance scenarios, not test cases. Do not add test data, UI operation scripts, interfaces, exception matrices, or performance thresholds.

Keep the document at project-definition granularity. Do not turn it into a Roadmap, Requirement/AC set, implementation design, Task plan, research notebook, or option dump. Provide stable, unambiguous anchors where downstream traceability needs them, but choose their form based on the document.

## Create or revise

For a new project, write `ProjectDefinition.md` only after `$gmgn-v2:brainstorm` has completed its required user-reference and independent external research.

For a semantic revision, start from the current accepted document and its triggering change. Preserve unaffected meaning and anchors, change every place that owns affected meaning, and remove conclusions that no longer hold. Do not reopen unrelated questions. Treat renames, links, formatting, and status synchronization that do not change meaning as mechanical edits.

Set the candidate document status to `pending-approval`; change it to `approved` only after explicit user approval.

## Maintain the log

Keep `ProjectDefinitionLog.md` descriptive and append-only. Append an entry only after a Project Definition change is accepted. Record enough to identify the accepted change, its reason, affected document anchors, and downstream impact. Do not copy the full old or new text, record rejected exploration, or create a second normative authority.

Normal downstream work must depend on `ProjectDefinition.md`, not the log.

## Check before handoff

- Confirm every required meaning is present without forcing a generic structure.
- Confirm user references, independently discovered projects, and technical references all came from completed research with real source anchors.
- Confirm scope and priorities are clear enough to support Roadmap allocation.
- Confirm every project-level user E2E scenario is clear enough for Roadmap coverage without becoming a test case.
- Confirm non-goals prevent the main foreseeable scope misunderstandings.
- Confirm no downstream document detail or unsupported claim has leaked into the root definition.
- Confirm a revision preserves unaffected meaning and identifies its real downstream impact.
- Confirm the seven frontmatter keys, reciprocal existing-document links, and DocStar `gmgn-v2` structural check when available.
