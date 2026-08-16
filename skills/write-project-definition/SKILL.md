---
name: write-project-definition
description: Create or semantically revise ProjectDefinition.md and append its accepted change history to ProjectDefinitionLog.md after the project's direction is sufficiently established. Consume Brainstorm research when product decisions required it, but do not trigger research merely because the document changes. Keep the document as the root source for Requirements, Roadmap, Spec, Design Bundle, and Task work without imposing a fixed section layout or template.
---

# Write Project Definition

## Preserve its role

Treat `ProjectDefinition.md` as the project's root normative source. It defines the project at a macro level so Requirement, Roadmap, Spec, Design Bundle, and Task documents can derive their own detail without inventing project intent.

Write in the project's language for readers who do not share the conversation context. Select the organization, headings, prose, tables, and anchors that best express this project's meaning. Do not apply a fixed outline, field list, ID scheme, or template.

Write the Project Definition as natural-language project authority for human readers. Do not define `R<n>` or `R<n>-AC<n>` here; only Spec turns allocated meaning into that specification form.

## Keep the DocStar machine surface

For every graph-governed Markdown document, keep the English frontmatter keys `locale`, `purpose`, `upstream`, `downstream`, `status`, `type`, and `nature`. Write frontmatter values as plain unquoted text; keep multiple Markdown links comma-separated on one unquoted line. Use only real relative Markdown links or an explicit unquoted `none`; whenever an existing edge changes, update both `upstream` and `downstream`. Link existing Requirement documents and Roadmap downstream when applicable. Do not link a missing future document.

Use `type: project-definition`, `nature: normative` for `ProjectDefinition.md`, and `type: project-definition-log`, `nature: descriptive` for `ProjectDefinitionLog.md`. Use only `draft`, `pending-approval`, `approved`, or `closed` for document `status`. This machine surface does not prescribe headings, section order, prose shape, or Project Definition anchors.

When DocStar is available, use its `gmgn-v1` preset for the corpus and run its structural check before handoff; use a discovered project-local conventions file instead of also passing a preset. Treat the result as structural evidence, never semantic approval.

## Preserve the required meaning

Make the document clearly establish all of the following, wherever and however they fit best:

- the project's vision, goals, positioning, intended users, and problem or opportunity;
- the project's functional scope and the relative priority of that scope;
- project-level user E2E success scenarios that identify the user and context, starting trigger, critical usage chain, and observable user outcome;
- external project references when they informed a project choice or targeted question;
- external technical references when they established a project-level constraint or relevant prior art;
- what the project explicitly will not do;
- material project-level constraints, assumptions, open questions, or principles needed to interpret the above and guide downstream work.

When external facts informed the accepted direction, use only facts and source anchors returned by the completed Brainstorm and its Researchers. Do not research, add, or infer new external facts while writing, and do not add references merely to satisfy a quota. Return a precise evidence gap when an accepted conclusion depends on missing support.

For each external reference, preserve a verifiable source and enough explanation to show its relevance, applicable boundary, and lesson. Keep supporting detail to the minimum needed for the project choice. Distinguish evidence from project choices: an external project or technology is not automatically a requirement.

Use technical references to identify reusable prior art and project-level constraints. Leave provider, version, interface, data, and algorithm choices to Design unless one is already an explicit project boundary.

Project-level user E2E scenarios are product acceptance scenarios, not test cases. Do not add test data, UI operation scripts, interfaces, exception matrices, or performance thresholds.

Keep the document at project-definition granularity. Do not turn it into a Requirement, Roadmap, Spec/AC set, implementation design, Task plan, research notebook, or option dump. Provide stable, unambiguous anchors where downstream traceability needs them, but choose their form based on the document.

## Create or revise

For a new project, write `ProjectDefinition.md` after the direction is sufficiently established. Fully complete `$gmgn-v2:brainstorm` and its bounded research first only when unresolved product choices required them.

For a semantic revision, start from the current accepted document and its triggering change. Preserve unaffected meaning and anchors, change every place that owns affected meaning, and remove conclusions that no longer hold. Do not reopen unrelated questions. Treat renames, links, formatting, and status synchronization that do not change meaning as mechanical edits.

Keep every new or semantically revised candidate `draft` during writing and Critic review, set it to `pending-approval` after Critic pass, and change it to `approved` only after explicit user approval. A mechanical edit that preserves meaning does not require another semantic approval.

## Maintain the log

Keep `ProjectDefinitionLog.md` descriptive and append-only. Append an entry only after a Project Definition change is accepted. Record enough to identify the accepted change, its reason, affected document anchors, and downstream impact. Do not copy the full old or new text, record rejected exploration, or create a second normative authority.

Normal downstream work must depend on `ProjectDefinition.md` directly or through accepted Requirements and Roadmap, not the log.

## Check before handoff

- Confirm every required meaning is present without forcing a generic structure.
- Confirm the document remains readable natural language and contains no Requirement R/AC specification.
- Confirm every included external reference came from completed research with a real source anchor; do not require references when none informed the project decision.
- Confirm scope and priorities are clear enough to support Roadmap allocation.
- Confirm each business domain or cross-Milestone capability that needs detail beyond this document can be handed to `$gmgn-v2:write-requirement` without inventing project scope.
- Confirm every project-level user E2E scenario is clear enough for Roadmap coverage without becoming a test case.
- Confirm non-goals prevent the main foreseeable scope misunderstandings.
- Confirm no downstream document detail or unsupported claim has leaked into the root definition.
- Confirm a revision preserves unaffected meaning and identifies its real downstream impact.
- Confirm the seven frontmatter keys, reciprocal existing-document links, and DocStar `gmgn-v1` structural check when available.
