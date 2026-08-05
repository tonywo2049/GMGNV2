---
name: write-design-bundle
description: Create or semantically revise an implementable Design Bundle from accepted Requirement and AC. Use after bounded external solution research to choose and justify the minimum architecture, close interfaces and data flows, and define risk-matched verification points without implementation or Task decomposition.
---

# Write Design Bundle

## Preserve its role

Treat the Design Bundle as the normative technical authority between accepted Requirement/AC and Task. It must remove shared and cross-unit implementation decisions that a Runner would otherwise have to invent.

Write in the project's language and choose the organization that best fits the system. Do not impose a generic section template or pre-create modules and contracts.

## Keep the DocStar machine surface

For every Markdown file in the Bundle, use the English frontmatter keys `locale`, `purpose`, `upstream`, `downstream`, `status`, `type`, and `nature`. Write frontmatter values as plain unquoted text; keep multiple Markdown links comma-separated on one unquoted line. Use real relative Markdown links or explicit unquoted `none`, and reciprocal existing-document edges. `Design.md` uses `type: design`, `nature: normative`; split normative modules and Contracts also declare their own type and `nature: normative`, link to `Design.md`, and are linked back from it. Link the accepted Requirement upstream and an existing Task downstream; never link a missing future document. Use only `draft`, `pending-approval`, `approved`, or `closed` for document `status`.

Keep the complete Bundle candidate `draft`; change every file in that same accepted Bundle to `approved` only after the configured Critic and automatic-acceptance gate pass.

Give each Design element referenced outside its defining text a stable `D<n>` ID and each Contract a stable `C<n>` ID. Define each machine ID once in its own list item under a heading that clearly names its kind, and bold only the ID. This does not prescribe Bundle heading order or file count.

When DocStar is available, use its `gmgn-v2` conventions and run its structural check on the complete Bundle before handoff; a project-local conventions file replaces, rather than augments, the preset. Structural results cannot select a Design or accept the Bundle.

## Require bounded solution research

Before semantic creation or revision, consume completed external research matched to the current delta and direct impact. Mechanical edits do not require new research.

Research must define the technical question, hard constraints, exclusions, comparison dimensions, source and version requirements, and the Design decision it supports. Prefer standards, official documentation, specifications, maintainer source and tests, release records, production reports, audits, or papers. Keep one credible candidate when only one fits, compare two when a real trade-off exists, and use a third only for a materially different credible path. A supported no-fit is valid.

Select against R/AC coverage, verified current-system constraints, compatibility, security boundaries, operational complexity, maintenance, adoption cost, and relevant scale or resource limits. Compare only credible choices that differ on a decisive dimension. Record the selected choice, decisive evidence, material trade-offs and consequences, and the condition that would justify revisiting it; do not create a full ADR or alternatives table when there is no real decision.

Trace the critical user and system scenarios end to end before finalizing components. Make assumptions explicit and verify them against accepted authority or system facts. Do not preselect a stack that accepted authority has not fixed.

Research informs technical choices; it cannot supply missing product behavior or turn an implementation convention into Requirement authority.

When the Design includes an explicit API, or the current need could plausibly reuse an existing implementation, the completed research must include GitHub reference-code search. Prefer reuse or adaptation over redevelopment whenever a credible source slice satisfies current R/AC.

For each reused reference, map the owning Design element to the repository, checked revision, path, and applicable symbol or code region; state the reuse or adaptation target and local landing point. Do not prescribe line-by-line changes. Do not evaluate license or authorization risk; neither gates reuse in this workflow.


## Keep one minimal Bundle

Design.md is always the root normative authority and the complete R/AC mapping entry point.

Create design/module-id.md only when scale, specialist ownership, or parallel writing makes a separate normative module necessary. Create design/Contract.md only for current independent module, Task, process, team, repository, or external-system boundaries. Keep small contracts in the owning Design location; split them only for size or independent review. Add machine-readable schema or compilable interface authority only when correctness depends on exact structure.

Do not create empty files, directories, duplicate definitions, or future placeholders.

## Define the minimum implementable decisions
Before choosing a Design, classify every unresolved point by owner. Input units, validity rules, fidelity, grouping meaning, visible defaults and ordering, output form, user-visible errors, exit behavior, and other externally observable semantics belong in Requirement when different choices would change acceptance.

If accepted R/AC permits multiple observably different choices and the choice matters to users or external systems, return the exact Requirement gap; do not pick the easiest implementation. Design may choose among techniques only when they are behaviorally equivalent under accepted authority.


Only when required by current R/AC or a sourced invariant, define:

- selected stack and dependencies;
- component responsibility, ownership, trust boundaries, calls, and data flow;
- data, state transitions, storage, transactions, migration, concurrency, order, and idempotency;
- non-trivial algorithms, errors, recovery, rollback, compatibility, security, performance, resources, and observability;
- the implementation result and verification point owned by each Design element.

Leave local replaceable expressions to implementation. Apply a deletion test: remove a Design element unless its absence would break a current R/AC, accepted Project Definition constraint, sourced invariant, or required cross-unit result.

Do not turn accepted behavior into line-by-line pseudocode. Exact local method calls and call order remain implementation detail unless changing them would alter a required cross-unit result, shared invariant, or accepted failure precedence.

## Close every boundary

For every retained cross-unit boundary, define the path from authoritative producer through transformation or derivation to consumer validation and state effect. State legal object stages, the unique validation authority, production call sites, success, observable failure, and applicable atomicity, concurrency, ordering, retry, cancellation, idempotency, recovery, compatibility, authentication, authorization, and resource behavior.

Give each cross-unit interface a stable Contract ID. Identify provider, every in-scope consumer, interaction form, request, success, errors, preconditions, postconditions, invariants, state effects, and conformance points. Link an exact structural authority when field type, width, encoding, signature domain, state key, error enum, or method signature affects correctness; Markdown explains semantics without duplicating the structure.

Define a unique error order when the first of multiple failures changes compatibility, security, or retry behavior.

## Design the verification strategy

Map every R/AC and material Design invariant to the lowest-cost deterministic oracle that can reject a plausible wrong implementation at the owning boundary. Use the testing pyramid as a selection heuristic, not a quota:

- use unit checks for isolated rules, transformations, and algorithms;
- use integration checks for storage, framework, process, network, and external-system boundaries;
- use Contract conformance checks for independently implemented producers and consumers;
- use a small number of E2E checks only for critical user or cross-system paths that lower layers cannot prove;
- use schema validation, dry-run, migration checks, smoke checks, visual or accessibility checks, or load and resilience checks only when the changed authority requires them.

For each composite AC, define the minimum executable acceptance boundary: the real entry point, required environment, participating results or Contracts, and only the harness needed to observe their joint outcome. If an existing executable mechanism is sufficient, link it instead of redesigning or duplicating it. Define a new integration gate or harness only when no existing mechanism can decide the composite AC.

Prioritize business-critical paths, error handling, edge cases, trust boundaries, data integrity, state transitions, idempotency, concurrency, recovery, and compatibility when they are in scope. Do not require checks for trivial forwarding or framework behavior already covered by an accepted dependency.

Write each verification point as one short clause containing only its exact authority link, owning boundary, oracle layer, and fault class. Link to R/AC for expected behavior; never repeat exact expected values, argument lists, example inputs, scenario matrices, assertion expressions, commands, coverage percentages, or evidence. Runner derive those during Task execution. Define shared seams, deterministic clocks or randomness, fixtures, simulators, or test dependencies only when they are necessary cross-unit Design decisions.

## Preserve trace and evidence

Map every R/AC once from the root Design to the owner of its structure, necessary data, failure behavior, interface authority, implementation result, and verification point. Every Design element has one owner.

Keep only the selected solution or supported no-fit, checked version or date, decisive evidence, applicable gap, and reuse boundary. Do not create a Research.md or retain search logs and candidate timelines. When reusing source, retain only the minimum closed slice needed by current R/AC plus unavoidable dependencies and protections, with upstream version, local location, adaptation, exclusions, and minimum checks.

## Create or revise

For a new Design Bundle, derive the complete minimum implementable authority from accepted R/AC and verified system facts. For a semantic revision, inspect real code and call paths, preserve unaffected owners and anchors, update every affected producer/consumer and trace, and remove invalid decisions.

## Check before handoff

- Required solution research is complete and the selection or no-fit has primary evidence.
- Explicit APIs and plausible reuse opportunities include GitHub reference-code research; reused Design elements name the source region, adaptation target, and local landing point without license or authorization review.
- No externally observable behavior was invented to fill a Requirement gap.
- No accepted product behavior, shared parameter, or implementation-level decision remains for the Runner to invent.
- Every R/AC and Design element has an owner, implementation result, and verification point.
- Every composite AC has a minimum executable boundary, real entry point, environment, and sufficient existing or new harness authority.
- Every boundary has one structural authority and a closed producer-to-state path.
- Contracts exist only for real independent boundaries and cover all in-scope consumers.
- Verification uses the lowest sufficient layer, covers applicable material risks, and can reject a plausible wrong result.
- Verification points do not duplicate R/AC or contain executable case detail.
- No replaceable local call sequence is fixed as Design authority.
- Applicable schema compiles or validates, necessary vectors reproduce, and no Design structure can be deleted.
- The complete Bundle is internally and globally consistent.
- Every cross-document D/C ID has one DocStar-compatible definition, and all Bundle frontmatter and reciprocal links are valid.
