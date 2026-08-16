---
name: write-agent-brief
description: Use when Main Session or a GMGN V2 Agent is about to create an Agent. Produce the smallest complete task brief for the already-selected target Agent without routing work or copying its stable instructions.
---

# Write Agent Brief

Main Session and every GMGN V2 Agent use this Skill before creating an Agent.

The caller has already selected the target Agent. This Skill only prepares that Agent's input.

For Main Session semantic routing, copy the user's complete instruction unchanged into `Objective`. For mechanical Task dispatch, create one brief per selected Task row using the `gmgnv2_runner` input contract. Architect has two distinct triggers: normal document work carries one explicit requested S-D-T outcome; execution-blocker repair carries one fixed shared Task.md batch to repair directly. Never combine those triggers in one brief and do not add a mode field.

## Method

1. Identify the selected Agent and its requested outcome.
2. Gather the applicable inputs from the contract below. Resolve choices owned by the caller before dispatch.
3. For a fixed candidate, resolve every absolute work location, the fixed Card/Log checkpoint and repository commits, and every exact write boundary before dispatch.
4. Draft the brief using only applicable fields from the compact form.
5. Apply the deletion test to every line.
6. Pass the resulting brief directly as the Agent input. Do not save a Brief document.

## Compact form

```text
Target Agent:
Audit Skill:
Objective:
Current facts:
Authority anchors:
Work location and write boundary:
Resolved choices:
Return:
```

Omit empty fields. An anchor is normally a path, section, Task ID, commit, or candidate identifier. Do not copy evidence that the Agent can read from that anchor.

## Deletion test

Delete a brief item unless removing it would prevent the selected Agent from performing its fixed responsibility or producing the requested return.

In particular, delete:

- stable workflow already defined by the target Agent;
- work owned by the caller or another Agent;
- unrelated history, explanation, inventories, and speculative checks;
- duplicated facts and evidence already available through an anchor;
- shared runtime, repository-discovery, monitoring, waiting, or interruption rules owned by the caller;
- extra objectives, assurance, or adjacent risks not required for the return.

The brief is a trigger and current input, not a restriction on a document Agent's global impact analysis.

## Architect trigger forms

For normal S-D-T work, `Objective` is the caller's explicit requested document outcome. When Main Session routes a user instruction, preserve that instruction unchanged. Supply only the accepted baseline and relevant authority or existing document-work anchors already known; do not tell Architect to scan execution blockers.

For an execution-blocker repair batch, write an `Objective` that tells Architect to claim and repair every execution blocker represented by an `architect-required` row in the fixed shared Task.md batch without creating a repair Task or Runner. Put authority `origin/main` and its accepted commit in `Current facts`, and the fixed Task.md path, commit, expected row states, execution references, and execution-record branches in `Authority anchors`. Architect resolves each immutable execution reference with `git show <commit>:<path>`; when remote persistence failed, pass the exact local checkpoint already returned by Runner. In `Work location and write boundary`, include authority local `main`, every Architect-owned repair location, and temporary ownership of each execution-record branch for Log updates; exclude every Runner implementation branch and workspace and every Card contract change. In `Return`, require confirmed repair commits, applicable Auditor conclusions, Log checkpoints, immutable execution references, and authority commits that persist `waiting` or `blocked` for every input row; a `blocked` result also includes the completed actions, required human action, and retry condition. Do not list Task IDs already present in the fixed batch, summarize blockers, copy Log content, prescribe repairs, or include later `architect-required` rows.

## Target input contracts

| Agent | Inputs needed when applicable |
| --- | --- |
| `gmgnv2_project_designer` | user objective; relevant existing anchors and constraints already known; user references when provided; requested outcome; repository and existing document-work anchors |
| `gmgnv2_architect` | either one explicit requested S-D-T outcome, or one fixed shared Task.md `architect-required` batch with expected row states, execution-record branches, available immutable execution references, and any required local checkpoint; relevant authority anchors and constraints already known; authority repository and baseline, affected repositories, required work locations, and existing repair anchors |
| `gmgnv2_runner` | one Task ID and shared `ready` row anchor; recorded execution reference; authority repository and accepted S-D-T baseline; existing repository branches, workspaces, candidate commits, PRs, Card, Log, and checkpoint anchors |
| `gmgnv2_coder` | one implementation result; every required absolute workspace, write boundary, and baseline; validation contract; relevant anchors and checkpoint already known; required return |
| `gmgnv2_auditor` | `Audit Skill:` set to exactly one of `$gmgn-v2:critic`, `$gmgn-v2:code-review`, or `$gmgn-v2:verify`; one matching concrete requested action; every required absolute work location; one fixed input candidate identified by Card/Log checkpoint plus repository commits, candidate ID, commit, blob, or SHA-256; for Critic, every normative document and applicable writing Skill in the single owner-defined change set; authority, pass condition, exact write boundaries and serial write handoff when Critic or Code Review may repair; environment when Verify observes; requested return |
| `gmgnv2_researcher` | one bounded research question; accepted direction when fixed; unresolved external fact; local authority and code facts already checked; decision it informs; claims and current anchors; allowed reference implementations; inclusion and exclusion criteria, including whether alternative discovery is authorized; allowed source classes and recency or version requirements; caller-owned comparison dimensions or metric definitions; stopping condition; whether factual synthesis is requested; required return fields |
| `gmgnv2_close_milestone` | Milestone anchor; authority repository and baseline; affected repositories and baselines; integration status; existing closure work; required checks |
| `gmgnv2_release` | accepted candidate and target-branch commit; repository remote and target branch; version and release target; existing evidence; publication, tag, Release, and asset authorization |

For Auditor, set `Audit Skill:` and describe the matching work. Do not combine document Critic, code Review, and independent Verify in one brief. The selected Skill defines whether a successor candidate may be written; the brief cannot grant Verify permission to modify its candidate.

For Critic, one integrated S-D-T change set may contain multiple normative documents and still constitutes one fixed candidate and one concrete critique action. Do not split that candidate by Task, blocker, or document type.

For Researcher, state explicitly whether the technical direction is fixed. When it is fixed, authorize only the implementation-reference or reuse question and exclude substitute discovery. Do not create a research question merely because a document changed.

For Coder, state the result, workspaces, and boundaries, not a document-reading list or guessed file list. Anchors are optional starting points; Coder discovers other needed context through repository discovery.

Do not add missing inputs that do not apply. If a required current fact cannot be found or resolved, return that single gap to the caller instead of inventing it.
