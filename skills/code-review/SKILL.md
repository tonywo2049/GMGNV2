---
name: code-review
description: Independently perform the single complete Review of one fixed GMGN V2 implementation candidate, directly repair bounded findings when safe, and return either the unchanged candidate, a successor candidate requiring Runner validation, or unresolved findings.
---

# Code Review

## Load the simplicity rules

Read `$ponytail:ponytail` completely before inspecting or changing code. Apply it to the full Review and to every repair. If the Skill is unavailable, return blocked instead of silently skipping the required simplicity check.

Use Ponytail to detect removable code, duplicated mechanisms, speculative abstraction, unnecessary dependencies or configuration, dead flexibility, and custom code already covered by the language, platform, or repository. Never simplify away accepted behavior, validation, security, accessibility, compatibility, or another required protection.

## Fix the input surface

Bind the Review to one complete fixed input candidate C1, its target-branch baseline, complete Task branch diff and commits, Task, Requirement, Design, applicable Contract, Card, declared write boundary, RED/GREEN checkpoints, and prepared deterministic checks. Treat Runner self-checks and summaries as evidence, not as Review.

Do not begin from a mutable workspace, a single repair commit, or a partial diff without the complete candidate surface. The Runner must stop writing and transfer serial write ownership before this Skill may repair C1.

## Inspect the complete candidate once

Trace changed behavior through real call paths and inspect every changed file needed to judge it. Check that C1:

- satisfies Task, R/AC, Design, Contract, Card, and write boundaries;
- contains only the current Task's code, tests, and necessary documentation, with no unrelated commits, debug artifacts, secrets, local configuration, or broad formatting;
- preserves correctness and applicable regression, data integrity, security, accessibility, performance, recovery, compatibility, concurrency, and resource protections;
- uses tests that can reject plausible wrong implementations;
- has valid authority-derived RED/GREEN evidence where behavior changed;
- passes the full Ponytail deletion and reuse check.

Run or replay only the targeted, negative, integration, project, and RED/GREEN checks needed for the verdict. A skipped, timed-out, unavailable, unauthorized, or incorrectly invoked required check is not pass.

Do not demand broader architecture, cleanup, coverage, abstraction, or defensive code without a current accepted owner.

## Repair bounded findings directly

A finding is material only when leaving it unfixed would cause concrete harm, no accepted fallback covers it, and a minimum sufficient repair can be stated.

Repair it directly only when all of these are true:

- accepted Task, R/AC, Design, Contract, Card, and write boundary already authorize the result;
- the intended outcome is decidable and does not require a product, architecture, API, dependency, or scope choice;
- the minimum repair and its verification stay inside the current Task;
- no other active writer is changing the workspace.

For a behavioral, correctness, security, boundary, or performance defect, use a repair-local TDD cycle:

1. Use an existing failing check or add the minimum authority-derived regression, negative, contract, or resource oracle.
2. Run that same oracle against frozen C1 and confirm RED for the intended reason.
3. Freeze the verdict-affecting test and helpers.
4. Make the minimum Ponytail-compliant repair, producing successor candidate C2.
5. Run the unchanged oracle against C2 for GREEN, then run affected regression checks.

Changing a verdict-affecting test or helper after RED invalidates the RED and requires replay against frozen C1. A temporary mutation or fault injection may prove that a test can discriminate, but it is test evidence rather than behavior RED and must not enter C2.

For deletion, equivalent refactoring, or another no-behavior-change repair, do not invent RED. Establish GREEN on C1, make the minimum change, and replay the same checks for GREEN on C2.

After every repair, repeat the affected correctness checks and Ponytail check. Do not add unrelated cleanup while the file is open.

## Leave authority decisions unresolved

Do not repair a finding that changes accepted meaning, Task boundary, public contract, architecture, dependency choice, or another owner’s decision. Return its severity, exact location, observable impact, accepted authority, minimum pass condition, and required owner.

Exclude style preferences, speculative risks, optional expansion, low-impact cleanup, and issues already covered by an accepted safeguard.

## Return the candidate and evidence

Return one of:

- `pass`: C1 was not modified and no material finding remains;
- `repaired: caller validation required`: return C2, the complete C1→C2 repair delta, each finding it resolves, RED→GREEN or GREEN→GREEN evidence, affected regression evidence, and Ponytail result;
- `findings`: return every unresolved material finding and the current candidate identifier.

Also return the original baseline, reviewed surface, every executed command with environment, exit code, limitation and side effect, and any remaining uncertainty.

The Runner independently checks an Auditor-produced delta and reruns affected commands before accepting C2. A repair result is not integration approval. Do not perform a second complete Review; a later check may cover only a repair delta, its pass conditions, and direct impact.

Do not modify accepted authority, Card meaning, Task status, acceptance state, or integration state. Do not commit, push, fetch, pull, rebase, create or update a PR, merge, or delete a branch; the Runner owns every Git and GitHub transition.

## Check before returning

- C1, target baseline, complete Task branch surface, Task, authority, Card, write boundary, and serial writer are fixed.
- The candidate contains no other Task, unrelated commit, temporary artifact, secret, or accidental generated file.
- `$ponytail:ponytail` was read and applied.
- The complete input candidate was reviewed once.
- Every direct repair was authority-preserving, bounded, minimal, and produced a traceable successor candidate.
- Behavioral repairs have valid frozen-oracle RED→GREEN evidence; equivalent simplifications use GREEN→GREEN.
- Required checks were not treated as pass when skipped, unavailable, or invalid.
- Every unresolved finding has concrete impact, authority, a minimum pass condition, and an owner.
- No preference, optional enhancement, or unrelated issue is included.
- The Runner still must validate any Auditor-produced repair delta.
