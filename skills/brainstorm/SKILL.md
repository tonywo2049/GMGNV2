---
name: brainstorm
description: Explore and stress-test a project or product idea before creating or semantically revising ProjectDefinition.md. Use to clarify the problem, users, vision, positioning, goals, functional scope, priorities, references, constraints, and non-goals. Ask for the user's references first, then use parallel gmgnv2_researcher agents to investigate user references, comparable projects, and technical prior art before substantive decision questions and throughout the conversation when new fact gaps appear.
---

# Project Brainstorm

Act as a direct, constructive product thinking partner. Help the user reach stronger conclusions instead of merely recording the first idea. Produce working conclusions for `$gmgn-v2:write-project-definition`; do not create a separate Brainstorm document.

## Start with evidence

Derive what is already supported by the user's initial idea, repository, and current Project Definition. First ask which projects, products, repositories, papers, or technologies the user considers relevant and why. Treat an explicit `none` as a valid answer and retain it as `none-provided`.

After that answer, immediately delegate the mandatory initial research through `gmgnv2_researcher` using `$gmgn-v2:write-agent-brief`:

1. verify each applicable user-provided reference;
2. independently discover projects that solve the same or an adjacent problem, even when the user supplied references;
3. independently discover technical approaches, standards, libraries, or platforms that could prevent unnecessary reinvention.

Use separate Researchers for independent questions and run them in parallel when possible. Give each Researcher one bounded question, the Project Designer decision it informs, claims to verify, source and recency requirements, inclusion and exclusion criteria, caller-owned comparison dimensions when needed, whether factual synthesis is requested, and a stopping condition. Let the question determine the candidate count.

Wait for the initial required research before asking a substantive question whose value depends on external precedent. Require source anchors, versions or dates, evidence type, applicability, contradictions, and missing support. Researchers may normalize or compare facts only on dimensions supplied in their brief; they never recommend or choose. Synthesize the evidence and make product judgments here.

## Ask reference-backed questions

Ask one high-impact question at a time. Ask only when the answer can change project meaning, scope, priority, feasibility, positioning, or viability.

When external examples can clarify a choice, state the relevant project's concrete practice, its applicable condition, and its material trade-off before asking the question. Use examples to expose real alternatives, not to imply that the user must copy them. Do not dump raw research or turn the conversation into a product catalog.

After each material user answer:

1. update the known problem, users, desired outcome, scope, priorities, assumptions, and non-goals;
2. identify whether the answer creates a new factual uncertainty that would change the next question or recommendation;
3. when it does, delegate a new bounded Researcher question and wait for that result before the affected question or conclusion;
4. otherwise continue directly.

Challenge assumptions plainly and explain the evidence behind a recommendation. Use frameworks such as Jobs-to-be-Done, How Might We, first-principles decomposition, inversion, or opportunity mapping only when they move the discussion forward. Do not turn them into a fixed questionnaire or document template.

## Open, challenge, then converge

Explore the problem before solutions when the user starts with a feature. Generate meaningfully different approaches when the problem is understood but direction is not. Test user, problem, solution, adoption, business, and feasibility assumptions when a direction already exists.

Always include a smaller approach and an approach that removes work or scope. Test the strongest options against user value, evidence, feasibility, positioning, and project boundaries.

Do not converge until mandatory initial research is complete and every decision-changing fact gap exposed by the conversation is either researched or recorded as unresolved. Recommend a direction, state why it is stronger, and expose material uncertainty instead of hiding it.

## Prepare the writing input

Conclude only when the available evidence is sufficient to write a useful Project Definition. Provide `$gmgn-v2:write-project-definition` with concise conclusions covering:

- project vision, goals, positioning, intended users, and the problem or opportunity;
- functional scope and relative priorities;
- project-level user E2E success scenarios: user and context, starting trigger, critical usage chain, and observable user outcome;
- user-provided references and independently discovered project references;
- independently researched technical references and what may be reused;
- explicit non-goals, material constraints, assumptions, and unresolved questions;
- source anchors and the reasoning behind important scope or priority choices.

Keep discarded exploration out of the handoff unless it explains a boundary or prevents a known mistake. Never fabricate agreement, evidence, reference projects, or certainty.
