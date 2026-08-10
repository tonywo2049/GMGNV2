# GMGN V2

GMGN V2 is an Agent-driven delivery workflow for Codex. It turns product ideas into traceable product authority, implementable work, independently reviewed code, and explicit Milestone closure.

See [GMGNV2.md](GMGNV2.md) for the normative workflow architecture. This document covers installation and use. See [README.zh-CN.md](README.zh-CN.md) for Chinese.

## What GMGN V2 provides

- Authority flow: `Project Definition + Requirements → Roadmap → Spec → Design Bundle → Task`.
- Targeted product research only when a decision needs it; bounded implementation research only for unresolved external facts.
- Explicit approval for new or semantically revised Project Definitions and Requirements; first approval for Roadmap; independent Critic gates for semantic document candidates.
- One branch, worktree, and PR per Task, with Coder TDD and Ponytail plus independent Review for non-mechanical candidates.
- Capacity-aware parallel Task dispatch, Milestone closure, and explicitly requested Release.

## Requirements

- A Codex surface with plugin support: the ChatGPT desktop app in Work/Codex mode or Codex CLI. Plugins are not available in the IDE extension.
- Python 3.11 or newer for repository validation.
- Git and a GitHub remote for the complete branch/PR workflow.
- The Ponytail plugin and `$ponytail:ponytail` Skill. Coder uses it before changing code or tests; Auditor uses it for every Code Review.
- DocStar is optional. When available, GMGN V2 uses its `gmgn-v2` conventions for structural document checks.

For current Codex plugin behavior, see the official [Plugins guide](https://learn.chatgpt.com/docs/plugins) and [Codex CLI plugin commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli#cli-codex-plugin).

## Install

Run from the repository root:

```bash
python3 skills/gmgn/scripts/manage_codex_install.py install
```

The command registers the local marketplace when needed, installs the plugin, validates the installed Agent TOML, and atomically copies named Agent profiles into `${CODEX_HOME:-$HOME/.codex}/agents`. It does not modify GMGN V1 configuration.

The plugin also includes a `SessionStart` Hook as a fallback for installation or updates through the Plugins UI. Review and trust the Hook when Codex prompts. Start a new Codex session when Agent profiles change.

## Update

Run from the GMGN V2 repository:

```bash
python3 skills/gmgn/scripts/manage_codex_install.py update
```

For a local Git marketplace, the command requires a clean worktree and runs `git pull --ff-only`. For a configured Git marketplace, it runs Codex marketplace upgrade. It then installs the current plugin version and synchronizes Agent profiles.

Start a new Codex session when Agent profiles change.

## Quick use

```text
Use $gmgn-v2:gmgn to turn this idea into a Project Definition, Requirements, and Roadmap: ...
```

```text
Use $gmgn-v2:gmgn to continue Milestone M1 and create its Spec, Design Bundle, and Task.
```

```text
Use $gmgn-v2:gmgn to complete every dispatchable Task in Milestone M1.
```

```text
Use $gmgn-v2:gmgn to close Milestone M1.
```

```text
Use $gmgn-v2:gmgn to release the accepted candidate as v1.0.0.
```

Only an explicit `$gmgn-v2:gmgn` invocation activates GMGN V2. See [GMGNV2.md](GMGNV2.md) for routing, document acceptance, Task state, Git, closure, and Release rules.

## Validation

```bash
python3 tests/validate_repository.py
python3 -m unittest discover -s tests -v
```

Validation covers plugin structure, Skill and Agent sets, Agent runtime configuration, installer behavior, and other mechanical contracts. Semantic consistency is reviewed by Critic, not inferred from text-marker checks.

## Uninstall

Run from the repository root:

```bash
python3 skills/gmgn/scripts/manage_codex_install.py uninstall
```

The command removes the `gmgn-v2` plugin and only named Agent files recorded as GMGN V2 managed. It does not delete GMGN V1 configuration, project documents, branches, PRs, or repository history.

Remove the local marketplace only when no plugin in it is still needed:

```bash
codex plugin marketplace remove gmgn-v2
```

Restart the desktop app or start a new CLI session after uninstalling. Check the result with:

```bash
codex plugin list --json
```

## Repository structure

```text
.codex-plugin/plugin.json        Plugin manifest
.agents/plugins/marketplace.json Local marketplace definition
.codex/agents/                   Named Agent profiles
hooks/                           SessionStart Agent synchronization
skills/                          Router, writing, research, audit, and installation tools
GMGNV2.md                        Normative workflow architecture
README.md                        English usage
README.zh-CN.md                  Chinese usage
tests/                           Mechanical repository validation
```
