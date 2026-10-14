# DOMANGCHA v4.0.0 — Adaptive Execution

DOMANGCHA ships two install shapes. The default is a per-project loop; the harness
(router, evidence adapters, 8 agent roles, 5 commands) installs globally, and neither
overwrites the other. Everything else — loops, graphs, memory, search, reviewers, the
browser — is native Claude Code.

## Install shapes

There is one command and no install-mode flag. `npx domangcha` reads where it runs:

| Where it runs | What it installs |
|---|---|
| inside a project | the loop there: `LOOP.md`, `CLAUDE.md`, `scripts/loop.mjs`, `.claude/`, `.cursor/`, `.loop/` |
| outside a project | the harness into `~/.claude` and `~/.domangcha` |
| `/ceo` with no harness | offers to install the harness, then runs the request |

A project holding `.loop/` and `scripts/loop.mjs` owns its protocol: the global
`UserPromptSubmit` hook yields to it instead of emitting a route card, so one protocol
reaches the model at a time. `/ceo` is the exception and the escalation path — it always
reaches the router. Everything below describes the harness.
Loop policy is in `domangcha/policies/loop.md`.

## Request flow

```text
Request → IntentNormalizer → TaskRouter → DIRECT | LOOP | GRAPH → validation → completion
```

- DIRECT: explanations, formatting, lookup, and trivial isolated changes. No mandatory planner, recursive loop, agent fan-out, DOC folder, version bump, or publish.
- LOOP: bounded PLAN → EXECUTE → VALIDATE → ACT, run through the native `/loop` skill and ScheduleWakeup.
- GRAPH: multi-phase or parallel work, run through the native Workflow tool (pipeline/parallel/phase, `resumeFromRunId`); approvals go through AskUserQuestion.

Use `python3 domangcha/engine.py route "<request>"`. Claude's UserPromptSubmit hook calls the same router automatically. Model output may propose an ambiguous classification but cannot override deterministic safety invariants.

## Invariants

- Preserve state when escalating DIRECT → LOOP → GRAPH.
- Security-sensitive, destructive, cross-cutting, resumable, or approval-gated work uses GRAPH.
- A meaningful implementation's writer cannot be its only reviewer.
- Validate ordinary facts—schemas, files, versions, tests, budgets, route enums—in code.
- Never commit, push, publish, deploy, or perform irreversible work without task-specific authority.
- Persist no secrets in checkpoints or structured logs.
- A user-facing feature is complete only when `domangcha/policies/evidence.md` passes: the four
  states (loading, empty, error, no-permission) forced and captured, one marker traced browser →
  server log → stored row, and every claim tagged observation/derivation/inference/unknown.
  `engine.py evidence {init,start,record,state,trace,check,close,diff}` runs it; the Stop hook
  blocks while an open run fails `check`. Code existing or a build passing is not completion.
- To copy or benchmark a feature from another product, extract it with REA (`rea` MCP server,
  `npx rea-agents setup`); its findings are input, never proof about our product.
- Report progress by default, in the user's language: route and reason up front, then progress
  through native surfaces (TodoWrite, Workflow phases, `/loop` iterations). `domangcha/orchestration/status.py`
  renders the route, checkpoint, and drift cards.

Shared policy is under `domangcha/policies/`; `evidence.md` governs whether a user-facing feature works. Claude-specific agents and hooks are adapters; Codex uses `AGENTS.md`. The 8 agent roles (dc-biz, dc-dev-be, dc-dev-db, dc-dev-fe, dc-dev-int, dc-dev-mob, dc-dev-ops, dc-wrt) are defined by `domangcha/manifests/agents.json`; review, security, QA, research, and docs use native agents (code-reviewer, security-reviewer, e2e-runner, Explore, doc-updater). Model selection is capability/policy based rather than a permanent model ID.

## Commands

Loop projects need no slash command — the prompt hook injects the protocol and the
active policies on every prompt. The commands below belong to the full harness.

- `/ceo "task"`: automatic route
- `/ceo-ralph "task"`: minimum LOOP route
- `/ceo-debug`, `/ceo-security`, `/ceo-ship`: workflow intents routed through the same engine

## Validation

```bash
python3 -m unittest discover -s domangcha/tests
python3 domangcha/engine.py validate
```

Official version source: `domangcha/VERSION` = 4.0.0.
