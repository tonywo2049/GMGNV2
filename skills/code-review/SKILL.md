---
name: code-review
description: Independently perform the single complete Review of one fixed GMGN V2 implementation candidate, directly repair bounded findings when safe, and return either the unchanged candidate, a successor candidate requiring Runner validation, or unresolved findings.
---

# Code Review

## Load the simplicity rules

Read `$ponytail:ponytail` completely before inspecting or changing code. Apply it to the full Review and to every repair. If the Skill is unavailable, return blocked instead of silently skipping the required simplicity check.

Use Ponytail to detect removable code, duplicated mechanisms, speculative abstraction, unnecessary dependencies or configuration, dead flexibility, and custom code already covered by the language, platform, or repository. Never simplify away accepted behavior, validation, security, accessibility, compatibility, or another required protection.

Ponytail is mandatory but does not replace Code Review. A minimal implementation can still be wrong, unsafe, or inadequately tested; treat the Ponytail result as one evidence input to the independent verdict.

## Fix the input surface

Bind the Review to one complete fixed Coder candidate C1: its Card/Log checkpoint, every included repository's `origin/main` baseline and candidate commit, complete diffs, task brief, declared workspaces and write boundaries, prepared checks, and relevant anchors already known. A candidate may span multiple repositories and PRs without becoming multiple Reviews. Discover any other context only when needed to judge the candidate. Treat Runner and Coder summaries as evidence, not as Review.

Do not begin from mutable workspaces, a single repair commit, or a partial repository diff without the complete candidate surface. The Runner must stop writing and transfer serial write ownership for every included workspace before this Skill may repair C1.

## Establish an independent review baseline

Reconstruct the required behavior, boundaries, failure handling, and protections from the brief and only the project material needed to resolve them. Do not use a preset document-reading list. Treat the diff, summaries, RED/GREEN evidence, tests, CI, and Ponytail as evidence rather than the definition of correctness.

For every material changed behavior, identify at least one plausible wrong implementation or failure path and the observable that would distinguish it. Use this baseline to decide what code, callers, tests, and commands must be inspected; do not use the changed-file list as the review boundary when real call paths extend beyond it.

## Inspect the complete candidate once

Trace changed behavior through real call paths and inspect every changed file needed to judge it. Check that C1:

Complete inspection means complete semantic coverage, not one unbounded diff command. First fix and inspect the commit list and changed-path inventory, then inspect each necessary changed path and affected call path once. Do not rely on truncated output as evidence that an unseen part was reviewed, and do not print an unchanged complete diff again after it has already been inspected.

- satisfies the brief, relevant project constraints, and write boundary;
- contains only the current Task's code, tests, and necessary documentation, with no unrelated commits, debug artifacts, secrets, local configuration, or broad formatting;
- preserves correctness and applicable regression, data integrity, security, accessibility, performance, recovery, compatibility, concurrency, and resource protections;
- uses tests that can reject plausible wrong implementations;
- has valid brief-derived RED/GREEN evidence where behavior changed;
- passes the full Ponytail deletion and reuse check.

Run or replay only the targeted, negative, integration, project, and RED/GREEN checks needed for the verdict. A skipped, timed-out, unavailable, unauthorized, or incorrectly invoked required check is not pass.

Passing tests, CI, static analysis, or Ponytail cannot produce pass until the independent review baseline and plausible failure paths have been compared with the complete candidate. When a test cannot reject a plausible wrong implementation, treat that as a Review finding or limitation according to its concrete impact.

Do not demand broader architecture, cleanup, coverage, abstraction, or defensive code outside the current Task.

## Repair bounded findings directly

A finding is material only when leaving it unfixed would cause concrete harm, no accepted fallback covers it, and a minimum sufficient repair can be stated.

Repair it directly only when all of these are true:

- the current Task and write boundary already determine the result;
- the intended outcome is decidable and does not require a product, architecture, API, dependency, or scope choice;
- the minimum repair and its verification stay inside the current Task;
- no other active writer is changing any included workspace.

For a behavioral, correctness, security, boundary, or performance defect, use a repair-local TDD cycle:

1. Use an existing failing check or add the minimum brief-derived regression, negative, contract, or resource oracle.
2. Run that same oracle against frozen C1 and confirm RED for the intended reason.
3. Freeze the verdict-affecting test and helpers.
4. Make the minimum Ponytail-compliant repair, producing successor candidate C2.
5. Run the unchanged oracle against C2 for GREEN, then run affected regression checks.

Changing a verdict-affecting test or helper after RED invalidates the RED and requires replay against frozen C1. A temporary mutation or fault injection may prove that a test can discriminate, but it is test evidence rather than behavior RED and must not enter C2.

For deletion, equivalent refactoring, or another no-behavior-change repair, do not invent RED. Establish GREEN on C1, make the minimum change, and replay the same checks for GREEN on C2.

After every repair, repeat the affected correctness checks and Ponytail check. Do not add unrelated cleanup while the file is open.

## Leave authority decisions unresolved

Do not repair a finding that requires a product, architecture, public API, dependency, or Task-scope decision. Return its severity, location, impact, missing decision, minimum pass condition, and required owner. The Runner resolves that decision before creating a new Coder candidate; equal filesystem permissions do not authorize either Coder or Auditor to invent it.

Exclude style preferences, speculative risks, optional expansion, low-impact cleanup, and issues already covered by an accepted safeguard.

## Return the candidate and evidence

Return one of:

- `pass`: C1 was not modified and no material finding remains;
- `repaired: caller validation required`: return C2, the complete C1→C2 repair delta, each finding it resolves, RED→GREEN or GREEN→GREEN evidence, affected regression evidence, and Ponytail result;
- `findings`: return every unresolved material finding and the current candidate identifier.

Also return every original repository baseline and candidate commit, the independent review baseline, reviewed call paths and surface, plausible wrong behaviors challenged, every executed command with environment, exit code, limitation and side effect, the Ponytail result, and any remaining uncertainty. Return concise judgment evidence, not a generic claim that checks passed.

The Runner independently checks an Auditor-produced delta and reruns affected commands before accepting C2. A repair result is not integration approval. Do not perform a second complete Review; a later check may cover only a repair delta, its pass conditions, and direct impact.

Do not modify project-planning documents, Card meaning, Task status, acceptance state, or integration state. In every repository, do not commit, push, fetch, pull, rebase, create or update a PR, merge, or delete a branch; the Runner owns every Git and GitHub transition.

## Check before returning

- C1, every repository baseline and candidate commit, the complete multi-repository surface, brief, write boundaries, and serial writer are fixed.
- The candidate contains no other Task, unrelated commit, temporary artifact, secret, or accidental generated file.
- `$ponytail:ponytail` was read and applied.
- An independent review baseline was derived from the brief and relevant project material without adopting C1, its tests, CI, or summaries as the correctness standard.
- Material changed behavior was challenged with plausible wrong implementations or failure paths through real callers.
- The complete input candidate was reviewed once.
- Every direct repair stayed inside the current Task and write boundary, was minimal, and produced a traceable successor candidate.
- Behavioral repairs have valid frozen-oracle RED→GREEN evidence; equivalent simplifications use GREEN→GREEN.
- Required checks were not treated as pass when skipped, unavailable, or invalid.
- Every unresolved finding has concrete impact, a missing decision, a minimum pass condition, and an owner.
- No preference, optional enhancement, or unrelated issue is included.
- The Runner still must validate any Auditor-produced repair delta.
