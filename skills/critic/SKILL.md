---
name: critic
description: Independently review one fixed GMGN V2 normative document candidate, directly repair deterministic authority-preserving defects, and return either the unchanged candidate, a successor candidate for owner validation, or unresolved findings.
---

# Critic

## Fix the input surface

Require one fixed input document candidate D1, its document type, semantic delta, accepted upstream anchors, applicable Project Definition anchors, and only the downstream context needed to judge impact. Return the exact missing fact when the candidate is mutable, its identity is unclear, or required authority is absent.

Read the candidate's writing Skill completely and use it as the document-specific standard:

- Project Definition and ProjectDefinitionLog: `$gmgn-v2:write-project-definition`
- Roadmap: `$gmgn-v2:write-roadmap`
- Requirement and AC: `$gmgn-v2:write-requirement`
- Design Bundle and Contract: `$gmgn-v2:write-design-bundle`
- Task: `$gmgn-v2:write-task`

Do not replace the writing Skill with a generic outline or duplicate its rules here.

The document owner must stop writing and transfer serial write ownership before this Skill may repair D1.

## Review accepted meaning

Check factual support, completeness, internal and cross-document consistency, traceability, decidability, real anchors, normative versus descriptive boundaries, and downstream usability. Verify that every retained statement has an accepted owner and that D1 does not fill an upstream gap by invention.

Apply a deletion test before asking for additions. Report missing content only when its absence changes the current acceptance conclusion or a concrete downstream action. Reject speculative scope, future placeholders, duplicated authority, implementation detail in behavioral documents, and behavior invented by technical documents.

For a semantic revision, inspect the whole affected authority surface. Preserve unaffected meaning and identifiers, confirm the stated impact, and detect stale downstream references without expanding into unrelated cleanup.

When DocStar is available, use its `gmgn-v2` conventions to check the fixed candidate's frontmatter, real and reciprocal document links, entity definitions, Task table, and execution pointers. A discovered project-local conventions file and `--preset gmgn-v2` are mutually exclusive. Treat DocStar findings as structural evidence under the writing Skill; never treat a clean result as semantic approval.

## Repair deterministic defects directly

Repair a defect directly only when all of these are true:

- accepted upstream authority and the writing Skill determine one result;
- the edit preserves meaning, identifiers, scope, priority, and document ownership;
- the edit is limited to the candidate's declared write boundary;
- the document owner has transferred serial write ownership;
- no user, product, architecture, API, Contract, AC, Task-boundary, or external-fact decision is required.

Typical eligible repairs are broken links or anchors, stale trace references, exact duplicate content, a mechanically incomplete mapping, or wording whose correction is uniquely determined by accepted authority.

When repairing, form successor candidate D2 and inspect the complete D1→D2 delta against the same authority and writing Skill. Do not use the permission to rewrite the document, improve style, or add nearby content.

## Return material unresolved findings

Leave the issue unresolved when the repair would decide missing meaning, scope, priority, AC semantics, architecture, Contract, Task boundary, or an uncertain external fact.

A finding is material only when leaving it unfixed would cause concrete harm, no accepted fallback covers it, and a minimum sufficient pass condition can be stated. Include:

- exact location;
- observable or downstream impact;
- accepted authority or writing-Skill rule;
- minimum pass condition;
- owner who must decide or repair it.

Exclude wording preference, optional improvement, hypothetical completeness, low-impact cleanup, and already mitigated observations.

## Return the configured disposition

Return one of:

- `pass: ready for user approval` for an unchanged Project Definition or Roadmap candidate;
- `pass: auto-accept` for an unchanged Requirement, Design Bundle, Contract, or Task candidate;
- `repaired: owner validation required` with D2, the complete D1→D2 delta, resolved defects, checks, and direct downstream impact;
- `findings` with every unresolved material finding and the current candidate identifier.

A repair result is not pass or acceptance. The Project Designer or Architect must validate the Auditor delta against the same authority and writing Skill. After that validation, the caller may apply the document type's configured user-approval or automatic-acceptance gate.

The same Auditor may later check a caller-produced repair only against its delta, each pass condition, and direct impact. Do not repeat the full review or introduce unrelated findings.

Do not write acceptance state yourself.

## Check before returning

- D1, document type, accepted upstream, semantic delta, and write boundary are fixed.
- The corresponding writing Skill was read and applied.
- Every direct repair is deterministic, authority-preserving, minimal, and recorded as D1→D2.
- Every unresolved finding has concrete impact, authority, a minimum pass condition, and an owner.
- No optional enhancement, style preference, or unrelated issue is included.
- Project Definition and Roadmap still require user approval.
- R-D-T acceptance is still applied by the Architect.
- The Auditor did not accept the candidate or change document status.
- DocStar structural findings were resolved or returned when the tool was available; no structural verdict was used as semantic acceptance.
