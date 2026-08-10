---
name: write-spec
description: Create or semantically revise a Milestone Spec.md from an accepted Roadmap allocation and its applicable Requirements. Use to express the allocated stage as traceable R/AC without adding product meaning or choosing implementation or tests.
---

# Write Spec

## Preserve its role

Treat `Spec.md` as the normative Milestone specification between an accepted Roadmap allocation plus its applicable Requirements and the Design Bundle. Translate only the allocated, sufficiently clear product meaning into traceable R/AC without adding or redefining it.

Write in the project's language for readers who do not share the conversation context. Choose the organization that best expresses the behavior. Do not impose a generic section template.

## Keep the DocStar machine surface

Use the English frontmatter keys `locale`, `purpose`, `upstream`, `downstream`, `status`, `type`, and `nature`, with `type: spec` and `nature: normative`. Write frontmatter values as plain unquoted text; keep multiple Markdown links comma-separated on one unquoted line. Use real relative Markdown links or explicit unquoted `none`, and keep existing `upstream`/`downstream` edges reciprocal. Link the accepted Roadmap upstream and an existing root Design downstream; do not link a missing future document. Cite allocated Requirement sections or stable anchors in the body instead of adding direct document-graph edges around Roadmap. Use only `draft`, `pending-approval`, `approved`, or `closed` for document `status`.

Keep a new or semantic candidate `draft`; change it to `approved` only after the configured Critic and automatic-acceptance gate pass. A caller-classified mechanical edit preserves the current document status.

Use `R<n>` for each Requirement and `R<n>-AC<n>` for each AC. Define each machine ID once in its own list item under a heading that clearly names its kind, and bold only the ID. Preserve identifiers across revisions and keep them globally unique across Spec documents. The machine form does not impose a generic section outline or heading order.

When DocStar is available, use its `gmgn-v2` conventions and run its structural check before handoff; do not combine a discovered project-local conventions file with `--preset gmgn-v2`. Structural results do not decide Spec meaning or acceptance.

## Derive only from accepted authority

Use the target accepted Roadmap Milestone allocation, its applicable accepted Requirement sections or stable anchors, applicable Project Definition anchors, and external constraints with explicit sources. Implementation, tests, code, or downstream documents can expose a gap but cannot silently define product meaning.

Give each retained Spec requirement a stable R identifier. Each R expresses one coherent observable stage behavior, capability, or constraint and names the Roadmap allocation plus Requirement, Project Definition invariant, or sourced external constraint that owns it.

Cover every target Milestone acceptance criterion, deliverable, and allocated upstream obligation, but do not absorb unallocated parts of a complete Requirement. Keep the trace explicit:

Requirement section or Project Definition anchor → Roadmap Milestone allocation and acceptance criterion or deliverable → R/AC

If Roadmap does not identify the selected portion of a Requirement clearly enough, return the exact allocation or upstream clarity gap. Do not split, weaken, or reinterpret it here.

Do not turn a purely technical reference into a Spec requirement unless it is already an accepted product boundary or creates an externally observable constraint.

An upstream Requirement deferred to a later Milestone may be absent from the current stage. It does not authorize a contrary public behavior. A temporary test seam may bypass an unimplemented business entry only when it is explicitly non-product, creates no compatibility promise, and the Milestone claim excludes the complete business path.

## Analyze behavior before writing

For each upstream acceptance obligation, identify the actor or external system, trigger or input, relevant precondition, state change, observable success, and observably distinct failure. Check whether empty, invalid, boundary, duplicate, retry, interruption, permission, and state-transition cases are applicable. This is coverage analysis, not a required document outline or a test plan.

Retain only cases that can change the acceptance conclusion and have an accepted owner. Do not multiply AC for imagined possibilities. Do not invent a term definition, validity rule, fidelity guarantee, default, ordering, interface behavior, or error semantic merely to complete the coverage. If an applicable case requires an observable choice that accepted authority does not own, return the exact gap or ask one user question instead of selecting a plausible rule.

Do not operationally redefine an ambiguous upstream condition. If terms such as verified, confirmed, active, available, or ready could mean a user assertion, recorded system state, or external fact, and that difference changes permission or a state transition, return the exact missing definition. A boundary disclaimer does not make an invented definition acceptable.

## Write decidable acceptance criteria

Give each R the minimum acceptance criteria needed to decide pass or fail, using stable identifiers such as R1-AC1. State the applicable precondition, action or check, and observable result; Given/When/Then is optional.

Cover the core success path and every applicable rejection, failure, recovery, boundary, or unchanged-state outcome needed to distinguish correct behavior. Keep an outcome only when an upstream acceptance obligation or invariant owns it; otherwise report the missing decision.

When a Milestone success signal depends on multiple R, accepted components, or separately observable outcomes holding together, add at least one stable composite AC with one decidable verdict for the joint result. Link every participating R and the owning Milestone signal. Local ACs remain necessary but are not sufficient; never infer the complete result only because each local AC passes.

An AC is behavioral authority from which tests can be derived. It must not prescribe test layers, frameworks, fixtures, commands, or implementation-specific assertions.

For an upstream-owned threshold, state the value, unit, scope or measurement condition, and pass/fail rule. Link inherited values to their accepted authority; return a Requirement TBD that affects the current Milestone instead of choosing its value here. Replace words such as reasonable, complete, sufficient, high-performance, or robust when they do not produce a decidable result.

## Keep the boundary

Define what users or external systems can observe, not architecture, interfaces, data structures, algorithms, implementation steps, Task boundaries, test code, or evidence.

Apply a deletion test to every R and AC: remove it unless its absence would make a current Milestone acceptance criterion, deliverable, accepted project invariant, or sourced external constraint fail. Future reuse, possible scale, configurability, or implementation convenience is not an owner.

## Create or revise

For a new target Milestone, derive the complete minimal Spec set. For a semantic revision, preserve unaffected R/AC and stable identifiers, update every affected trace, remove obligations that lost their owner, and identify the real Design and Task impact.

## Check before handoff

- Every Milestone acceptance criterion and deliverable is covered.
- Every R/AC has one explicit upstream section or anchor and a stable identifier.
- Every AC is externally decidable and changes the acceptance conclusion.
- Every multi-R or multi-component Milestone signal has a decidable composite AC; local ACs are not treated as proof of the joint result.
- Applicable success, failure, negative, boundary, and state-transition behavior has been checked without inventing semantics.
- Every behavior-gating term or precondition has accepted meaning; no disclaimer hides an invented definition.
- Thresholds have complete value, unit, scope, condition, and pass/fail meaning.
- No observable definition, default, safeguard, or error rule lacks an accepted owner.
- No implementation, Design, Task, test code, evidence, or speculative behavior has leaked into Spec.
- A revision preserves unaffected meaning and identifies its downstream impact.
- Every R/AC has one DocStar-compatible definition, and the seven frontmatter fields and reciprocal links are valid.
