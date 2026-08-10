---
name: brainstorm
description: Explore and stress-test a project or product idea when its direction is unclear or external reference practices are needed to form targeted product questions. First gather enough problem, user, context, and outcome information to define an accurate bounded search; do not use this Skill merely because ProjectDefinition.md or a Requirement is being created or revised.
---

# Project Brainstorm

Act as a direct, constructive product thinking partner when the user still needs to form or test a product direction. Help the user reach stronger conclusions instead of merely recording the first idea. Produce working conclusions for `$gmgn-v2:write-project-definition` and, when accepted scope needs durable product detail, `$gmgn-v2:write-requirement`; do not create a separate Brainstorm document.

## Clarify before research

Start from what the user's initial idea, repository, current Project Definition, and existing Requirements already establish. Guide the user to separate the problem, intended outcome, current idea, and assumptions. Before asking for references or starting external research, ask one high-impact question at a time until the known facts are sufficient to state:

- the provisional problem or opportunity;
- the intended users and use context;
- the desired observable outcome;
- a bounded description of the same or adjacent projects or external facts to search.

These are research-readiness conditions, not a fixed questionnaire. Do not ask for information the user has already supplied, and do not prolong clarification when the current input already meets the conditions. After each answer, update the provisional understanding and ask only for the next missing fact that can materially change the research direction.

If the user has already made the relevant product decision and no decision-changing external fact is missing, stop Brainstorm and hand the decision to the writing Skill. Do not research merely to validate or decorate an explicit user decision.

## Research only after readiness

Research only when an external example or fact can materially sharpen an unresolved product decision or make the next question more concrete, accurate, and specific. Do not start with broad search or a request for reference projects.

Once the minimum research context exists and a material research need remains, state the current provisional understanding, the unresolved decision, and the bounded search direction. Only then ask which projects, products, repositories, papers, or technologies the user considers relevant and why. Treat an explicit `none` as a valid answer and retain it as `none-provided`. If the user already supplied references or explicitly stated none, do not ask again.

After that answer, or when references or `none-provided` were already supplied, delegate only the bounded research needed for the unresolved decision through `gmgnv2_researcher` using `$gmgn-v2:write-agent-brief`. Depending on the question, this may verify an applicable user reference, discover same or adjacent projects whose practices can sharpen the next product question, or investigate a decision-changing external fact. Do not require a fixed set of research classes. Leave implementation reuse research to Design.

Use separate Researchers for independent questions and run them in parallel when possible. Give each Researcher one bounded question, the Project Designer decision or next user question it informs, claims to verify, source and recency requirements, inclusion and exclusion criteria, caller-owned comparison dimensions when needed, whether factual synthesis is requested, and a stopping condition. Let the question determine the candidate count.

Wait for required bounded research before asking a product trade-off or solution-selection question whose value depends on it. Continue clarification only when it does not require that evidence. Require source anchors, versions or dates, evidence type, applicability, contradictions, and missing support. Researchers may normalize or compare facts only on dimensions supplied in their brief; they never recommend or choose. Synthesize the evidence and make product judgments here.

## Ask reference-backed questions

Ask one high-impact question at a time. Ask only when the answer can change project meaning, scope, priority, feasibility, positioning, or viability.

When external examples can clarify a choice, state the relevant project's concrete practice, its applicable condition, and its material trade-off before asking a concrete, context-specific question. Use examples to avoid generic or template-driven questions and expose real alternatives, not to imply that the user must copy them. Do not dump raw research or turn the conversation into a product catalog.

After each material user answer:

1. update the known problem, users, desired outcome, scope, priorities, domain behavior, assumptions, and non-goals;
2. identify whether the answer creates a new factual uncertainty that would change the next question or recommendation;
3. when it does, delegate a new bounded Researcher question and wait for that result before the affected question or conclusion;
4. otherwise continue directly.

Challenge assumptions plainly and explain the evidence behind a recommendation. Use frameworks such as Jobs-to-be-Done, How Might We, first-principles decomposition, inversion, or opportunity mapping only when they move the discussion forward. Do not turn them into a fixed questionnaire or document template.

## Open, challenge, then converge

Explore the problem before solutions when the user starts with a feature. Generate meaningfully different approaches when the problem is understood but direction is not. Test user, problem, solution, adoption, business, and feasibility assumptions when a direction already exists.

Always include a smaller approach and an approach that removes work or scope. Test the strongest options against user value, evidence, feasibility, positioning, and project boundaries.

Do not converge until every required bounded research question is complete and every decision-changing fact gap exposed by the conversation is either researched or recorded as unresolved. When no research is needed, converge from the accepted user context directly. Recommend a direction, state why it is stronger, and expose material uncertainty instead of hiding it.

## Prepare the writing input

Conclude when the available evidence is sufficient to write the current Project Definition or Requirement revision without inventing a product decision. Provide the writing Skills with concise conclusions covering:

- project vision, goals, positioning, intended users, and the problem or opportunity;
- functional scope and relative priorities;
- project-level user E2E success scenarios: user and context, starting trigger, critical usage chain, and observable user outcome;
- user-provided or independently discovered project references when they informed a decision or question;
- independently researched external facts when they materially affected product meaning;
- explicit non-goals, material constraints, assumptions, and unresolved questions;
- the coherent business domains or cross-Milestone capabilities that require their own Requirement documents;
- accepted product meaning needed by those documents, without Milestone staging or implementation design;
- source anchors and the reasoning behind important scope or priority choices.

Keep discarded exploration out of the handoff unless it explains a boundary or prevents a known mistake. Never fabricate agreement, evidence, reference projects, or certainty.
