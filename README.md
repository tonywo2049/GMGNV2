# GMGN V2

GMGN V2 is an agent-driven delivery workflow for Codex. It turns a project idea into traceable product authority, implementation-ready work, independently reviewed code, and an explicit Milestone closure.

The normative architecture is defined in [GMGNV2.md](GMGNV2.md). This README is the usage guide. See [README.zh-CN.md](README.zh-CN.md) for Chinese.

## What GMGN V2 provides

- A single project authority chain: `Project Definition → Roadmap → Requirement → Design Bundle → Task`.
- Mandatory external research during product Brainstorming and Design work.
- Human approval only for Project Definition and Roadmap; R-D-T documents are accepted automatically after independent Critic review.
- One branch, worktree, and PR per Task, with TDD, Ponytail, independent code Review, and evidence-backed integration.
- Mechanical Task redispatch after each Runner completion.
- Milestone-level reconciliation and repair Tasks before closure.
- Explicit release authorization; Release never starts automatically.

## Requirements

- A Codex surface with plugin support: the ChatGPT desktop app in Work/Codex mode or Codex CLI. Plugins are not available in the IDE extension.
- Python 3.11 or newer for repository validation.
- Git and a GitHub remote for the complete branch/PR workflow.
- The Ponytail plugin and `$ponytail:ponytail` Skill. Runner requires it before changing code or tests.
- DocStar is optional. When available, GMGN V2 uses its `gmgn-v2` conventions for structural document checks.

For current Codex plugin behavior, see the official [Plugins guide](https://learn.chatgpt.com/docs/plugins) and [Codex CLI plugin commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli#cli-codex-plugin).

## Install

From the repository root, run one command:

```bash
python3 skills/gmgn/scripts/manage_codex_install.py install
```

This command registers the local `gmgn-v2` marketplace when needed, installs the plugin, validates the installed Agent TOML files, copies them atomically into `${CODEX_HOME:-$HOME/.codex}/agents`, and verifies their version and hashes. It never changes GMGN V1 profiles.

The plugin also contains a `SessionStart` Hook as a fallback for installation or updates performed through the Plugins UI. Review and trust that Hook when Codex asks. If the Hook reports that Agent profiles changed, start one more new session before dispatching a GMGN V2 Agent.

Start a new Codex session after installation. Installed plugin Skills and Agent profiles are then available:

```text
Use $gmgn-v2:gmgn. I want to build a new product from this idea: ...
```

## Update

Run the single update command from the GMGN V2 repository:

```bash
python3 skills/gmgn/scripts/manage_codex_install.py update
```

For a local Git marketplace, the command requires a clean worktree and runs `git pull --ff-only`. For a configured Git marketplace, it runs the Codex marketplace upgrade. It then installs the current plugin version, synchronizes the Agent TOML files from the actual installed plugin copy, and verifies their hashes. No separate Agent-sync command is required.

Start a new Codex session after an update that changes Agent TOML files.

## Quick use

Typical requests:

```text
Use $gmgn-v2:gmgn to turn this idea into a Project Definition and Roadmap.
```

```text
Continue Milestone M1 and create its Requirement, Design Bundle, and Tasks.
```

```text
Complete every dispatchable Task in Milestone M1.
```

```text
Close Milestone M1.
```

```text
Release the accepted candidate as v1.0.0.
```

Main Session routes the current request once and dispatches the selected Agent with the user's complete instruction unchanged. It does not use `$gmgn-v2:write-agent-brief`, summarize the request, or add next-step guidance; after dispatch it only forwards messages unchanged. `write-agent-brief` is reserved for Agent-to-Agent delegation.

## Workflow

1. **Project Designer** first clarifies enough user context to form bounded research questions, then asks for references, runs researched Brainstorming, and creates or revises the Project Definition and Roadmap.
2. The user explicitly approves both Project Definition and Roadmap after independent Critic review.
3. **Architect** converts an accepted Roadmap Milestone into Requirement, Design Bundle, and maximally parallel Tasks.
4. R-D-T candidates are accepted automatically after independent Critic review and merged through one document-only PR.
5. Main Session dispatches every `pending` Task whose prerequisites are `closed` and which has no active or unresolved blocked attempt.
6. **Runner** implements one Task through its Task branch and PR, then returns `Task completed` with the merged target-branch commit.
7. Main Session refreshes the target branch and scans the same Milestone again, dispatching newly unblocked Tasks.
8. When every non-cancelled Task is `closed`, **Close Milestone** reconciles Roadmap acceptance criteria, R/AC, Contracts, implementation, and evidence.
9. A closure defect creates a new repair Task through Architect. Main Session runs it and retries closure. An old closed Task is never reopened.
10. **Release** runs only after an explicit user request and required external-operation authorization.

## Agents and Skills

| Agent | Owns | Primary Skills |
| --- | --- | --- |
| Project Designer | Brainstorm, Project Definition, ProjectDefinitionLog, Roadmap, user approval | `brainstorm`, `write-project-definition`, `write-roadmap`, `write-agent-brief` |
| Architect | Requirement, Design Bundle/Contract, Task decomposition | `write-requirement`, `write-design-bundle`, `write-task`, `write-agent-brief` |
| Researcher | One bounded evidence question; no recommendation or selection | `research` |
| Runner | One Task from readiness through implementation and PR integration | `ponytail`, `write-agent-brief` |
| Auditor | One fixed critique, code Review, or independent verification | Exactly one of `critic`, `code-review`, or `verify` |
| Close Milestone | Milestone reconciliation, closure record, repair-Task trigger | `write-agent-brief`; `verify` through Auditor when required |
| Release | Authorized packaging, publishing, deployment, and release record | `write-agent-brief`; `verify` through Auditor when required |

Every named Agent reads the [`gmgn` Shared Agent rules](skills/gmgn/SKILL.md#shared-agent-rules) before work while retaining its fixed TOML role. Repository discovery and Agent monitoring are defined only there. Every Agent that creates another Agent first uses `write-agent-brief`, which does not copy shared rules into the child brief; Main Session never uses it. Auditor does not use a generic mode; the requested work determines which one audit Skill it reads.

## Documents and acceptance

| Authority or record | Owner | Acceptance |
| --- | --- | --- |
| Project Definition | Project Designer | Critic pass, explicit user approval, then document-only PR merge |
| Roadmap | Project Designer | Critic pass, explicit user approval, then document-only PR merge |
| Requirement | Architect | Critic pass, automatic semantic acceptance, then R-D-T PR merge |
| Design Bundle and Contract | Architect | Critic pass, automatic semantic acceptance, then R-D-T PR merge |
| Task.md | Architect | Critic pass, automatic semantic acceptance, then R-D-T PR merge |
| Task Card and Log | Runner | Integrated with the Task PR |
| Milestone closure | Close Milestone | Reconciliation passes and the closure-only PR merges |

Only a commit merged into the target branch is active accepted authority for downstream work. Local candidates and open PRs are not active authority.

Project Definition is the root project authority. There is no Goal document. Roadmap is the direct upstream of Requirement. Task execution does not create a separate Coding document; execution evidence lives in Card, Log, tests, code, PRs, and Git history.

## Task and Git rules

Task row states are fixed:

```text
pending → active → blocked or closed
pending or recoverable blocked → cancelled when accepted upstream removes the result
```

A closed Task never reopens. A later defect becomes a new Task.

Git rules:

- Start each Task from the latest target branch.
- Use one Task branch, one managed worktree, and one PR for one Task.
- Default Codex branch name: `codex/<Task ID>-<short-description>`.
- Never develop, commit, or push directly on a shared branch.
- Keep Task code, tests, Card/Log, and necessary Task-local document updates together.
- Run `git fetch origin` and `git rebase origin/<target-branch>` before the first push or merge request.
- Push the first time only after the complete local candidate and required gates pass.
- Use `--force-with-lease` only when a Task-exclusive rebased branch must be updated; never use unprotected force push.
- Merge through the repository's policy; default to squash merge when no policy exists.
- After merge, refresh the target branch and remove the Task branch/worktree only when safe and authorized.

Project Designer and Architect use separate document-only branches and PRs. Close Milestone uses a closure-only PR. Release may use a release-only PR for a version-only delta.

## Milestone closure and release

Close Milestone builds the chain:

```text
Roadmap acceptance criteria and deliverables → R/AC → sufficient evidence
```

It reconciles retained Contracts with providers, consumers, failure behavior, implementation, and integration evidence. Composite AC assigned to closure replay must run at the real entry point and environment; local passes cannot be used to infer the composite result.

If closure finds an implementation, test, Design, or Task-authority gap, Architect creates a new `pending` repair Task. Main Session dispatches that Task and retries closure after its PR merges.

Release packages or publishes only a fixed accepted target-branch commit. It does not change product meaning or repeat unaffected acceptance work, and it does not perform external operations without authorization.

## Compatibility

### GMGN V1

GMGN V1 and V2 can coexist because V2 uses the `gmgn-v2` plugin identity and `gmgnv2_*` Agent names. The active workflow is selected by the Skill invoked in the current session. Use `$gmgn-v2:gmgn` to run V2.

### DocStar

GMGN V2 Markdown uses English frontmatter keys, reciprocal Markdown links, stable M/R/D/C/T IDs, and the fixed `Task → Card → Log → latest_event` chain. When DocStar is available, use project-local conventions or the `gmgn-v2` preset, never both V1 and V2 presets together. DocStar validates structure; it does not decide semantic acceptance or Milestone closure.

## Validate

```bash
python3 tests/validate_repository.py
python3 -m unittest discover -s tests -v
```

The validation checks plugin structure, the Skill set, Agent runtimes and contracts, English-only Agent TOML, cross-Agent workflow markers, and installer isolation.

## Uninstall

Run one command from the repository root:

```bash
python3 skills/gmgn/scripts/manage_codex_install.py uninstall
```

This removes the `gmgn-v2` plugin and only the named Agent files recorded as GMGN V2-managed, including profiles installed by v0.1.0 before the state manifest existed. It does not remove GMGN V1 profiles, project documents, branches, PRs, or repository history.

Optionally remove the local marketplace only when no other plugin from it is needed:

```bash
codex plugin marketplace remove gmgn-v2
```

Restart the desktop app or start a new CLI session after uninstalling. Verify the result with:

```bash
codex plugin list --json
```

## Repository layout

```text
.codex-plugin/plugin.json       Plugin manifest
.agents/plugins/marketplace.json Local marketplace entry
.codex/agents/                  Named Agent profiles
hooks/                          SessionStart Agent-sync fallback
skills/                         Router, writing, research, audit, and install tooling
GMGNV2.md                       Normative workflow architecture
README.md                       English usage guide
README.zh-CN.md                 Chinese usage guide
tests/                          Repository contract validation
```
