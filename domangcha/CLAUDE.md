# DOMANGCHA v4.0.0 — Claude Code Adapter

This file contains Claude-specific integration only. Shared execution policy lives in `domangcha/policies/` in the repository, installed at `~/.domangcha/domangcha/policies/`; deterministic control lives in `engine.py`. `evidence.md` decides when a user-facing feature is complete, on every route.

## Two install shapes

- `npx domangcha` decides by location: inside a project it installs the loop there (`loop/templates/` → project root) and never writes to `~/.claude`; outside a project it runs `install.sh` and installs everything below into `~/.claude` and `~/.domangcha`.
- `hooks/domangcha-ceo-enforcer.py` yields when the project carries `.loop/` and `scripts/loop.mjs`, so a global install and a loop project never both speak — except for `/ceo`, which always reaches the router and is the documented escalation path.
- `loop/templates/scripts/loop.mjs` gates `/ceo` on machines without the harness and offers to install it, so a loop-only project still has a route up.

## Claude integration

- `hooks/domangcha-ceo-enforcer.py` calls the canonical TaskRouter.
- LOOP runs through the native `/loop` skill and ScheduleWakeup; GRAPH runs through the native Workflow tool (pipeline/parallel/phase, `resumeFromRunId`). Memory is native file memory (`~/.claude/projects/*/memory`, `MEMORY.md`); search is native WebSearch/WebFetch.
- `orchestration/status.py` renders the route, checkpoint, and drift cards. Status reporting is on by default.
- `agents/dc-*.md` hold the 8 logical roles (dc-biz, dc-dev-be, dc-dev-db, dc-dev-fe, dc-dev-int, dc-dev-mob, dc-dev-ops, dc-wrt), resolved through `manifests/agents.json`. Review, security, and QA use native code-reviewer, security-reviewer, and e2e-runner.
- Browser verification uses Claude-in-Chrome.
- Approvals go through AskUserQuestion. A rejected approval aborts the relevant branch.
- Evidence adapters: `engine.py evidence {init,start,record,state,trace,check,close,diff}` force and capture the four states, trace a marker browser → server log → stored row, and tag every claim by provenance. The Stop hook blocks while an open run fails `check`.
- REA (`rea` MCP server, `npx rea-agents setup`) extracts features from other products; DOMANGCHA evidence proves the result in ours.

Do not reconstruct the legacy mandatory CEO/FULL PIPELINE from prompts. Follow DIRECT, LOOP, or GRAPH returned by `engine.py`.

Official version source: `VERSION` = 4.0.0.
