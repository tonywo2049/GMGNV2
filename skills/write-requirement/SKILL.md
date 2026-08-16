---
name: write-requirement
description: Create or semantically revise natural-language Requirement documents from an accepted ProjectDefinition.md, user decisions, and applicable information. Use to maintain the accepted product requirements, product specifications, and explicit TBDs that Roadmap, Spec, and Design need as their current product baseline.
---

# Write Requirement

## Preserve its role

Treat each Requirement as evolving, human-facing product authority between the Project Definition and Roadmap. Record the currently accepted product requirements and specifications for one coherent domain or cross-Milestone capability, plus explicit product questions that remain TBD.

The Project Definition owns project scope, goals, principles, and non-goals. A Requirement may add detail within that accepted scope. Return the exact Project Definition gap when a proposed requirement changes those project-level boundaries.

Approval accepts the current Requirement baseline. It does not claim that the document will never change or that every recorded TBD is resolved.

Choose the smallest useful document set. Follow the repository's semantic layout; when none exists, keep Requirements under `requirements/`. Do not create one file per feature, a mandatory index, an empty placeholder, or one document that mixes unrelated domains. Do not impose a fixed body template.

## Keep the DocStar machine surface

Use the English frontmatter keys `locale`, `purpose`, `upstream`, `downstream`, `status`, `type`, and `nature`, with `type: requirement` and `nature: normative`. Write frontmatter values as plain unquoted text; keep multiple Markdown links comma-separated on one unquoted line. Use real relative Markdown links or explicit unquoted `none`, and keep existing reciprocal links. Link the accepted Project Definition upstream and an existing Roadmap downstream; never link a missing future document.

Use only `draft`, `pending-approval`, `approved`, or `closed` for document `status`. Keep a semantic candidate `draft` during writing and Critic review, set it to `pending-approval` after Critic pass, and change it to `approved` only after explicit user approval. An approved Requirement may contain explicit TBDs.

Write for human readers. Use descriptive headings and stable anchors where Roadmap needs traceability. Do not define `R<n>` or `R<n>-AC<n>` here; Spec creates those machine identifiers only for allocated, sufficiently clear product meaning.

When DocStar is available, use its `gmgn-v1` preset and run its structural check before handoff; use a discovered project-local conventions file instead of also passing a preset. Treat structural results as evidence, never semantic approval.

## Maintain the current product baseline

Use the current user instruction, accepted authority, applicable project material, and sourced constraints. Treat every input as information to reconcile through the normal authority rules; do not create source-specific writing rules.

State the product meaning needed to distinguish acceptable from unacceptable outcomes for the scope being advanced. Include precise product rules when downstream work would otherwise need to choose between observably different results. Let the actual domain determine the document structure and level of detail.

Do not treat silence in the Project Definition as proof that an in-scope requirement does not exist. Do not treat supplied material as accepted merely because it is detailed. Ask for a decision when current authority does not determine which product meaning applies.

## Track TBDs without blocking unrelated work

Use `TBD` for a known product question that is not yet decided. Record enough context to determine what remains open and whether it affects the scope currently being advanced.

Do not require every TBD to be resolved before approving the Requirement or revising Roadmap. If a TBD changes the product meaning needed by the current Spec, Design, or Task, return that exact gap and stop only the affected work. Preserve unrelated progress.

Resolving a TBD is a semantic Requirement revision and follows the normal Critic and explicit user-approval gate. A downstream document may expose or request that revision, but it must not choose the answer itself.

## Separate product meaning from implementation

A choice belongs in Requirement when alternatives would change product results, externally observable behavior, compatibility, safety boundaries, operating conclusions, or acceptance conclusions.

Leave a choice to Design only when the alternatives are equivalent under all accepted product meaning. If that boundary is unclear, return the Requirement gap instead of assuming the choice is technical.

## Leave allocation and implementation downstream

Do not assign behavior to Milestones, define schedules, or describe temporary implementation shortcuts. Roadmap allocates the current accepted baseline. Spec translates only the allocated and sufficiently clear meaning into traceable, decidable R/AC. Design chooses the technical implementation. None of them may silently add or change product meaning.

When research, Spec, Design, implementation, Review, or verification reveals a product change, revise the Project Definition for project-level boundaries or the Requirement for in-scope product meaning. Preserve unaffected meaning and identify the real impact on Roadmap, Spec, Design, Contract, and Task documents.

## Create or revise

Create a Requirement only when accepted scope needs durable product detail beyond Project Definition granularity. Every new document and every semantic revision requires one complete Critic pass and explicit user approval. Mechanical link, anchor, formatting, or status synchronization that preserves meaning does not require another semantic approval.

## Check before handoff

- The current scope has enough accepted product meaning to proceed without downstream invention.
- Known requirements, specifications, and TBDs are represented accurately.
- No TBD is presented as an accepted product rule.
- A TBD blocks only work whose product result depends on it.
- Roadmap can allocate the accepted meaning without redefining it.
- Spec can formalize the allocated meaning without adding product semantics.
- Every choice left to Design is equivalent under the accepted product meaning.
- No Milestone allocation, implementation, Task, test procedure, or evidence has leaked into the Requirement.
- Every semantic change identifies affected downstream authority and waits for explicit user approval.
- Stable anchors, frontmatter, reciprocal links, and the applicable DocStar structural check are valid.
