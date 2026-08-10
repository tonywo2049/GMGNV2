---
name: critic
description: Independently review one fixed GMGN V2 normative candidate, directly repair every material finding within its authority and write boundary, obtain an exact user or upstream decision only when repair cannot proceed without one, validate the final candidate, and return pass or an exact blocker.
---

# Critic

## Fix the input surface

Require one fixed input normative candidate D1, its complete semantic delta, every affected document type and location, accepted upstream anchors, applicable Project Definition anchors, and only the downstream context needed to judge impact. D1 may span multiple normative documents when they form one owner-defined integrated change set, including one Architect S-D-T change set or execution-blocker repair batch. It must not combine unrelated owner objectives. Return the exact missing fact when the candidate is mutable, its identity or complete write boundary is unclear, or required authority is absent.

Read every writing Skill applicable to the candidate completely and use them together as the document-specific standards:

- Project Definition and ProjectDefinitionLog: `$gmgn-v2:write-project-definition`
- Requirement: `$gmgn-v2:write-requirement`
- Roadmap: `$gmgn-v2:write-roadmap`
- Spec and AC: `$gmgn-v2:write-spec`
- Design Bundle and Contract: `$gmgn-v2:write-design-bundle`
- Task: `$gmgn-v2:write-task`

Do not replace the writing Skill with a generic outline or duplicate its rules here.

The candidate owner must stop writing and transfer serial write ownership for the complete candidate before this Skill may repair D1. After transfer, the candidate owner never repairs or reviews a Critic finding or repair.

## Establish an independent semantic baseline

Derive the obligations that D1 must satisfy from accepted upstream authority, applicable Project Definition anchors, the writing Skill, and required downstream decisions. Do not use D1's headings, claims, omissions, or self-description as the review checklist, and do not assume that meaning repeated consistently inside D1 is accepted or complete.

For each material obligation, identify the downstream decision or action it must enable and the concrete failure caused by an absent, contradictory, or ambiguous rule. This baseline constrains judgment but does not authorize new product meaning.

## Review accepted meaning

Check factual support, completeness, internal and cross-document consistency, traceability, decidability, real anchors, normative versus descriptive boundaries, and downstream usability. Verify that every retained statement has an accepted owner and that D1 does not fill an upstream gap by invention.

Actively try to disprove material conclusions. Test alternative reasonable interpretations, missing actors or states, boundary values, success and failure paths, recovery, conflicting upstream statements, and a downstream consumer attempting to act from D1 alone. Keep only challenges whose failure would change acceptance or a concrete downstream action. Passing structural checks, internal consistency, polished prose, or agreement with the author's summary is not semantic evidence by itself.

For Requirement, verify that accepted product meaning and explicit TBDs are represented accurately, no TBD is presented as decided, and a TBD blocks only dependent work. For Roadmap, verify that every allocated obligation is accepted upstream, no TBD is allocated as decided, and incremental allocations preserve claim boundaries. For Spec, verify that only allocated, sufficiently clear upstream meaning is formalized without adding product semantics.

Apply a deletion test before asking for additions. Report missing content only when its absence changes the current acceptance conclusion or a concrete downstream action. Reject speculative scope, unowned placeholders, duplicated authority, implementation detail in behavioral documents, and behavior invented by downstream documents. An explicit Requirement TBD is valid when it is not presented as decided and its affected scope is clear.

For a semantic revision, inspect the whole affected authority surface. Preserve unaffected meaning and identifiers, confirm the stated impact, detect stale downstream references, and verify cross-document consistency across the complete candidate without expanding into unrelated cleanup.

Only after completing the independent semantic review, use mechanical checks to validate the resulting candidate. When DocStar is available, use its `gmgn-v2` conventions to check the fixed candidate's frontmatter, real and reciprocal document links, entity definitions, Task table, and execution pointers. A discovered project-local conventions file and `--preset gmgn-v2` are mutually exclusive. Treat DocStar findings as structural evidence under the writing Skill; never treat a clean result as semantic approval.

## Repair every material finding directly

Own every material finding through repair and validation. Do not return a finding for the document owner to fix or review.

For each material finding:

- repair it directly when accepted authority and the writing Skill determine the result;
- when product meaning is missing and the writing Skill permits unresolved meaning, write an explicit `TBD` only if the open question, affected scope, and blocked work can be stated without choosing an answer;
- otherwise return `decision-required` with one exact user or upstream question. The caller relays that question unchanged. When the answer or accepted upstream authority returns, the same Critic applies it and continues validation; the caller does not edit the candidate.

A relayed user answer authorizes only the meaning it states. Preserve every unaffected identifier, scope, priority, and ownership boundary. Stay inside the candidate's declared write boundary; return an exact blocker when the required repair belongs to another document.

When repairing, form successor candidate D2. Do not use the permission to rewrite the document, improve style, or add nearby content.

## Validate the final candidate

Before returning pass, run every applicable mechanical check required by the writing Skill and repository against the final candidate. When D2 exists, also inspect the complete D1→D2 delta against the same authority, writing Skill, semantic boundary, and direct downstream links. Do not delegate this validation to the caller. A failed or unavailable required check prevents pass and must be repaired or returned as an exact blocker.

## Return a decision request or blocker only when repair cannot continue

Do not return a repairable finding. Return `decision-required` only when the final candidate cannot be determined without new user meaning or accepted upstream authority and an explicit `TBD` is not valid for the document or current scope. Return `blocked` only when the fixed input, required authority, write authorization, or required validation is unavailable.

Exclude wording preference, optional improvement, hypothetical completeness, low-impact cleanup, and already mitigated observations.

## Return the configured disposition

Return one of:

- `pass: ready for Project Designer acceptance` for a final Project Definition, Requirement, or Roadmap candidate;
- `pass: auto-accept` for a final Spec, Design Bundle, Contract, or Task candidate;
- `decision-required` with one self-contained question, the candidate identifier, exact affected location and impact, known accepted meaning, and the minimum answer needed;
- `blocked` with the candidate identifier and exact unavailable input, authority, authorization, document boundary, or validation.

For either pass, return the final candidate identifier, the independent semantic baseline and actual review coverage, the material alternative interpretations or failure paths challenged, any complete D1→D2 repair delta, resolved defects, completed checks, and direct downstream impact. Return concise judgment evidence, not hidden reasoning or a generic claim that the document was reviewed. A completed Critic never returns a repair awaiting caller validation. The Project Designer or Architect applies the document type's configured user-approval or automatic-acceptance gate directly to the passed candidate without mechanically revalidating a Critic-produced repair.

After `decision-required`, the same Critic applies the relayed answer and resumes from the current successor candidate. The caller never produces or reviews the repair.

Do not write acceptance state yourself.

## Check before returning

- D1, every affected document type, accepted upstream, complete semantic delta, and write boundary are fixed.
- Every corresponding writing Skill was read and applied.
- An independent semantic baseline was derived from accepted authority without adopting D1 as its own review checklist.
- Material conclusions were challenged with applicable alternative interpretations, failure paths, boundaries, and downstream use.
- Every material finding was repaired by the Critic, represented by an accurate explicit `TBD`, or returned as one exact decision request or blocker.
- Every repair is minimal, stays inside the write boundary, is recorded as D1→D2, and is validated by the Critic.
- Every pass identifies a final candidate that completed all applicable mechanical checks.
- Every relayed decision was applied by the same Critic; the document owner did not repair or review a Critic finding.
- No optional enhancement, style preference, or unrelated issue is included.
- Every semantic Project Definition and Requirement still requires explicit user approval; Roadmap still requires its first user approval.
- S-D-T acceptance is still applied by the Architect.
- The Auditor did not accept the candidate or change document status.
- DocStar structural findings were resolved or returned when the tool was available; no structural verdict was used as semantic acceptance.
