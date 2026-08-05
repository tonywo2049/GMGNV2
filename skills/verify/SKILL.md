---
name: verify
description: Independently answer one bounded verification question about a fixed GMGN V2 candidate by observing one authority-defined outcome. Use only when the caller records a necessary observable that ordinary deterministic checks and Review cannot prove, or when the user or accepted authority explicitly requires independent verification.
---

# Verify

## Fix one question

Require one fixed candidate, one recorded trigger, one independent question, one expected observable, one pass condition, and the necessary environment. Confirm that applicable earlier blockers are cleared and that the trigger still applies.

Return the exact gap when the task contains multiple questions, lacks a decidable pass condition, or does not identify the candidate. Do not convert ordinary deterministic checks into independent verification.

## Choose the minimum valid observation

Select the smallest method that can produce the planned observable. A command supplied by the caller is binding only when accepted authority defines it as the unique valid path.

Prepare and execute only what the observation needs. Do not create or modify tests, oracle logic, evidence files, production code, or tracked state.

Verification observes candidate V1; it never repairs V1. Reading the candidate does not transfer implementation or document ownership to the Verifier.

## Distinguish invocation errors from candidate failure

If a path, syntax, working directory, identifier, or equivalent invocation error prevents the planned observable, do not fail the candidate. When candidate and inputs are unchanged, correct the invocation in the same task and rerun only the affected step.

Return fail only when a correct planned observation conflicts with the pass condition. Return blocked when the required environment or authority is unavailable. A skip, timeout, unavailable check, or unrelated fallback is never pass.

Reconfirm candidate identity after any command that could alter it. Material drift invalidates both pass and fail evidence.

On candidate failure, return the evidence to the caller. The caller or owning Agent forms a successor candidate V2, completes every gate invalidated by that change, and requests verification again only when the original trigger still applies.

## Keep the boundary

Do not add a second question, expand into a test suite, repeat ordinary Runner checks, perform a code or document Review, or provide implementation advice. Report an incidental issue only when it causes concrete material harm, has no accepted fallback, and has a minimum sufficient pass condition.

Return the candidate, method, exact command or action, environment, exit status, actual observable, pass/fail/blocked verdict, limitations, and side effects.

## Check before returning

- Candidate and environment are fixed and unchanged.
- There is exactly one trigger, question, observable, and pass condition.
- The method is the minimum valid way to produce that observable.
- Invocation errors were corrected rather than treated as candidate failure.
- Candidate failure was returned to the owner rather than repaired here.
- Skip, timeout, and unavailable environment were not treated as pass.
- No test, oracle, evidence file, production code, or tracked state was created or modified.
- The result contains the actual observable and a decidable verdict.
