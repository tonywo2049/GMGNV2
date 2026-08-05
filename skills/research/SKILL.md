---
name: research
description: Collect and optionally synthesize traceable evidence for one bounded GMGN V2 research question without making product, architecture, prioritization, or implementation decisions. Use to validate user references, discover comparable or substitute projects, investigate technical prior art and reusable code, compare source-backed facts, synthesize user-research evidence, or analyze metric facts before the caller decides.
---

# Research

## Fix one research contract

Require one bounded question and only the inputs that apply: the decision it informs, claims to verify, current facts and anchors, inclusion and exclusion criteria, allowed source classes, recency or version requirements, caller-owned comparison dimensions or metric definitions, stopping condition, and required return fields.

Treat the decision context as a relevance boundary, not permission to make the decision. Return the exact blocking gap when the question, authority, access, or stopping condition is not usable. Do not turn user research, competitive research, technical research, and metric research into separate modes.

## Match evidence to each claim

Use the smallest credible source set that can answer the question. Source quality depends on the claim:

- For product capability, API, price, version, or release claims, prefer the product itself, official documentation, standards, specifications, maintainer source and tests, and release records.
- For behavior and experience claims, prefer direct observation, interviews, support records, and product telemetry. Treat reviews and community posts as attributed reports, not product authority.
- For company, market, or adoption claims, prefer filings, registries, official statistics, and primary datasets. Label analyst, press, social, and job-posting evidence as secondary reports or weak directional signals.
- For repository facts, inspect active code, tests, and history at a fixed revision; exclude declared archives.

Trace repeated claims back to their original source. Multiple pages repeating one announcement are one origin, not independent confirmation. Distinguish "not found within the checked boundary" from evidence that something is absent.

Use caller-defined inclusion, exclusion, and stopping conditions for candidate discovery. Do not impose a global candidate count, add weak candidates to fill a quota, or continue after sufficient evidence is available.

## Record evidence precisely

For every retained fact or calculation, record:

- the fact;
- evidence type: direct observation, source claim, or derived result;
- source identity and exact anchor;
- checked version, revision, or date;
- applicable method, population, sample, segment, metric definition, or formula;
- applicability, limitations, conflicting evidence, and missing support.

Use the minimum source excerpt needed to support the fact. Do not copy long passages.

For user evidence, distinguish what people did from what they said or preferred. Report frequency as `n/N` with the relevant segment and method; preserve contradictions and outliers. Do not invent personas or convert observations into opportunities.

For metric evidence, fix the qualifying event, numerator, denominator, population, window, timezone, aggregation, cohort or segment, baseline or target, and data freshness before comparing values. State formulas and assumptions, expose instrumentation or comparability problems, use ranges when precision is unsupported, and never turn correlation or event coincidence into causation.

## Synthesize facts only when requested

When the research contract requires cross-source synthesis, you may:

- normalize candidates on caller-owned dimensions;
- count observations or compare values using an explicit denominator or formula;
- identify agreement, conflict, independent corroboration, outliers, and evidence gaps;
- classify alternatives by stated inclusion criteria;
- return a source-backed comparison without ranking it.

This is evidence synthesis, not semantic judgment. Do not create dimensions or weights that change the decision, score candidates without a supplied decidable rubric, rank or select solutions, recommend product or technical direction, set priorities, write strategic implications, or attribute causes without sufficient causal evidence. The Project Designer, Architect, or direct caller owns those decisions.

## Stop and return

Stop when the contract's condition is met, the allowed search boundary is exhausted, or a precise blocker prevents further work. Return:

- the fixed question, scope, and checked-at date or revision;
- source-backed evidence records;
- only the requested factual synthesis;
- contradictions, missing evidence, and material limitations.

Keep raw search history, discarded weak sources, and recommendation prose out of the result. Do not create a Research document or modify project authority.

## Check before returning

- There is one bounded research question and a usable stopping condition.
- Every fact, calculation, and comparison has a source anchor and applicable context.
- Claim type determined source choice; repeated claims were not counted as independent evidence.
- User evidence distinguishes behavior from statements and reports frequency with a denominator.
- Metric comparisons use fixed definitions and do not imply causation.
- Any cross-source synthesis stayed inside caller-owned dimensions and methods.
- No candidate count, score, recommendation, selection, priority, or semantic decision was invented.
- Unknowns and search limits are explicit, and no project authority was modified.
