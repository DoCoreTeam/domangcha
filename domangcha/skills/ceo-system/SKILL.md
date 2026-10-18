---
name: ceo-system
description: DOMANGCHA adaptive execution adapter. Uses one deterministic TaskRouter for DIRECT, LOOP, and GRAPH.
---

# DOMANGCHA Adaptive Execution

The canonical authority is `domangcha/engine.py`; this skill does not define a second router.

1. Normalize the request and call the engine route command.
2. DIRECT uses minimal context and validation without mandatory agents or DOC output.
3. LOOP runs as bounded passes in the session, tracked in TodoWrite and capped by the route's budget; native `/loop` and ScheduleWakeup only when a pass waits on external state.
4. GRAPH runs through the native Workflow tool (pipeline/parallel/phase, `resumeFromRunId`); approvals go through AskUserQuestion.
5. A model cannot lower a route selected by a safety invariant.
6. Resolve logical roles from `manifests/agents.json` through runtime-native capabilities.
7. Use policies rather than hard-coded provider model IDs.
8. Do not commit, push, publish, deploy, or perform irreversible work without task-specific authority.
9. Report progress by default: route and reason up front (`orchestration/status.py` renders the
   route, checkpoint, and drift cards), then progress through native surfaces — TodoWrite, Workflow
   phases, LOOP passes — and a plain-language explanation before every approval. Never go
   silent through a long step.

Shared policies live under `domangcha/policies/` in the repository, installed at `~/.domangcha/domangcha/policies/`.
Beyond routing, `evidence.md` decides when a user-facing task is complete; the `ceo-standards`
skill carries its condensed form.
Claude-specific instructions live in CLAUDE.md; Codex-specific instructions live in AGENTS.md.
