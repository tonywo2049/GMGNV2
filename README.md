# GMGN V2

GMGN V2 is an agent-driven delivery workflow for Codex. It uses a traceable document chain to make implementation explicit, then runs independent Tasks in parallel.

See [GMGNV2.md](GMGNV2.md) for the normative architecture and [README.zh-CN.md](README.zh-CN.md) for Chinese setup instructions.

## Install named agents

```bash
python3 skills/gmgn/scripts/install_codex_agents.py
```

GMGN V2 uses the `gmgn-v2` plugin identity and `gmgnv2_*` agent names, so it can coexist with GMGN V1.

## Validate

```bash
python3 tests/validate_repository.py
python3 -m unittest discover -s tests
```
