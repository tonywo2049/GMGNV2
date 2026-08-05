---
name: write-agent-brief
description: Use when a GMGN V2 Agent is about to create another Agent. Produce the smallest complete task brief for the already-selected target agent without routing work or copying its stable instructions. Main Session does not use this Skill.
---

# Write Agent Brief

This Skill is only for Agent-to-Agent delegation. Main Session forwards the user's instruction unchanged under `$gmgn-v2:gmgn` and never uses this Skill.

The caller has already selected the target Agent. This Skill only prepares that Agent's input.

## Method

1. Identify the selected Agent and its requested outcome.
2. Gather the applicable inputs from the contract below. Resolve choices owned by the caller before dispatch.
3. Draft the brief using only applicable fields from the compact form.
4. Apply the deletion test to every line.
5. Pass the resulting brief directly as the Agent input. Do not save a Brief document.

## Compact form

```text
Target Agent:
Objective:
Current facts:
Authority anchors:
Work location and write boundary:
Resolved choices and authorization:
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

## Target input contracts

| Agent | Inputs needed when applicable |
| --- | --- |
| `gmgnv2_project_designer` | user objective; existing Project Definition, Log, and Roadmap anchors; known constraints; user reference projects when already provided; requested definition or planning outcome; repository remote and target branch; target baseline; existing document branch, workspace, and PR if any; GitHub write and merge authorization |
| `gmgnv2_architect` | target Milestone identifier and user-approved Roadmap anchor; applicable Project Definition anchor; current Requirement, Design Bundle/Contract, and Task anchors; repository context; requested R-D-T outcome; known constraints; repository remote and target branch; target baseline; existing document branch, workspace, and PR if any; GitHub write and merge authorization |
| `gmgnv2_runner` | one Task ID and row anchor; upstream anchors; recorded Task state; repository remote and target branch; baseline commit; existing Task branch, workspace, and PR if any; GitHub write authorization |
| `gmgnv2_auditor` | one concrete requested action and exactly one required audit Skill: `$gmgn-v2:critic`, `$gmgn-v2:code-review`, or `$gmgn-v2:verify`; fixed input candidate; authority, pass condition, declared write boundary and serial write handoff when Critic or Code Review may repair; environment when Verify observes; requested return |
| `gmgnv2_researcher` | one bounded research question; decision it informs; claims and current anchors; inclusion and exclusion criteria; allowed source classes and recency or version requirements; caller-owned comparison dimensions or metric definitions; stopping condition; whether factual synthesis is requested; required return fields |
| `gmgnv2_close_milestone` | Milestone anchor; repository remote and target branch; its Task PR and integration status; existing closure branch or PR; recorded completion conditions; required aggregate checks; GitHub write authorization |
| `gmgnv2_release` | accepted candidate and target-branch commit; repository remote and target branch; version and release target; existing evidence; publication, tag, Release, and asset authorization |

For Auditor, describe the work itself rather than setting mode or audit_type. Do not combine document Critic, code Review, and independent Verify in one brief. The selected Skill defines whether a successor candidate may be written; the brief cannot grant Verify permission to modify its candidate.

Do not add missing inputs that do not apply. If a required current fact cannot be found or resolved, return that single gap to the caller instead of inventing it.
