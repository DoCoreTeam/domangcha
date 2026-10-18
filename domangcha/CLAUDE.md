# DOMANGCHA v4.0.0 — Claude Code Adapter

This file contains Claude-specific integration only. Shared execution policy lives in `domangcha/policies/` in the repository, installed at `~/.domangcha/domangcha/policies/`; deterministic control lives in `engine.py`. `evidence.md` decides when a user-facing feature is complete, on every route.

## Two install shapes

- `npx domangcha` decides by location: inside a project it installs the loop there (`loop/templates/` → project root) and never writes to `~/.claude`; outside a project it runs `install.sh` and installs everything below into `~/.claude` and `~/.domangcha`.
- `hooks/domangcha-ceo-enforcer.py` yields when the project carries `.loop/` and `scripts/loop.mjs`, so a global install and a loop project never both speak — except for `/ceo`, which always reaches the router and is the documented escalation path.
- `loop/templates/scripts/loop.mjs` gates `/ceo` on machines without the harness and offers to install it, so a loop-only project still has a route up.

## Claude integration

- `hooks/domangcha-ceo-enforcer.py` calls the canonical TaskRouter.
- LOOP runs as bounded passes in the session, tracked in TodoWrite; the native `/loop` skill and ScheduleWakeup are for waiting on external state and for `/ceo-ralph`. GRAPH runs through the native Workflow tool (pipeline/parallel/phase, `resumeFromRunId`). Memory is native file memory (`~/.claude/projects/*/memory`, `MEMORY.md`); search is native WebSearch/WebFetch.
- `orchestration/status.py` renders the route, checkpoint, and drift cards. Status reporting is on by default.
- `agents/dc-*.md` hold the 8 logical roles (dc-biz, dc-dev-be, dc-dev-db, dc-dev-fe, dc-dev-int, dc-dev-mob, dc-dev-ops, dc-wrt), resolved through `manifests/agents.json`. Review, security, and QA run on an independent reviewer subagent — `code-reviewer`, `security-reviewer`, `e2e-runner`, `doc-updater` or `seo-specialist` when installed (ECC ships them, also as `ecc:<name>`), otherwise native `general-purpose` in a context separate from the writer; `Explore` for research.
- Browser verification uses Claude-in-Chrome.
- Approvals go through AskUserQuestion. A rejected approval aborts the relevant branch.
- Evidence adapters: `engine.py evidence {init,start,record,state,trace,check,close,diff}` force and capture the four states, trace a marker browser → server log → stored row, and tag every claim by provenance. The Stop hook blocks while an open run fails `check`.
- REA (`rea` MCP server, `npx rea-agents setup`) extracts features from other products; DOMANGCHA evidence proves the result in ours.

## Reporting contract

The prompt hook sends only the route — one line for DIRECT, the card for LOOP and GRAPH — so these rules live here, once per session, not in every prompt.

1. Open the reply with the route line or card the hook printed, so the user sees what and why first.
2. Report progress natively: steps in TodoWrite, LOOP as numbered passes, GRAPH as Workflow phases.
3. Never go silent through a step over 30 seconds; say start, middle, end.
4. Before destructive or irreversible work, say what approval is for and why, then stop on AskUserQuestion.
5. A user-facing feature is done only when an evidence run passes: `python3 ~/.domangcha/domangcha/engine.py evidence start` → state enter/exit (four states) → trace <marker> → check; quote run_id and the check result.
6. The user's language, brief and plain; never hide a failure — state it with the next action.

Do not reconstruct the legacy mandatory CEO/FULL PIPELINE from prompts. Follow DIRECT, LOOP, or GRAPH returned by `engine.py`.

Official version source: `VERSION` = 4.0.0.
