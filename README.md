<div align="center"><pre>
██████╗  ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗ ██████╗  ██████╗ ██╗  ██╗ █████╗
██╔══██╗██╔═══██╗████╗ ████║██╔══██╗████╗  ██║██╔════╝ ██╔════╝ ██║  ██║██╔══██╗
██║  ██║██║   ██║██╔████╔██║███████║██╔██╗ ██║██║  ███╗██║      ███████║███████║
██║  ██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║   ██║██║      ██╔══██║██╔══██║
██████╔╝╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║╚██████╔╝╚██████╗ ██║  ██║██║  ██║
╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝
</pre></div>

<div align="center">

### 🚗💨 DOMANGCHA — Adaptive Engineering for Claude Code & OpenAI Codex

**Your coding agent is powerful. DOMANGCHA gives it the right amount of orchestration.**
One command, nothing to memorise: `npx domangcha` reads where you are and installs what that place needs.
Then just say what you want — the loop plans, audits and reports, and proves user-facing work with evidence, not claims.

*Your AI getaway car from development hell.*

[![Version](https://img.shields.io/badge/version-4.0.0-brightgreen?style=for-the-badge&logo=github)](https://github.com/DoCoreTeam/domangcha/blob/main/domangcha/VERSION)
[![npm](https://img.shields.io/npm/v/domangcha?style=for-the-badge&logo=npm&color=CB3837)](https://www.npmjs.com/package/domangcha)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Runtimes](https://img.shields.io/badge/Runtimes-Claude%20Code%20%7C%20Codex-5865F2?style=for-the-badge)](#runtime-compatibility)
[![Agents](https://img.shields.io/badge/Agents-8-FF6B6B?style=for-the-badge)](https://github.com/DoCoreTeam/domangcha#the-8-agent-roles)
[![Gates](https://img.shields.io/badge/Gates-5-orange?style=for-the-badge)](https://github.com/DoCoreTeam/domangcha#the-5-gates)
[![Node](https://img.shields.io/badge/Node-22.13%2B-339933?style=for-the-badge&logo=nodedotjs)](https://nodejs.org)

<br/>

> **I typed one command and got back auth, payments, and a dashboard — tested, reviewed, security-audited. I went to get coffee.**
>
> *— Michael Dohyeon Kim, KDC CEO · builder of DOMANGCHA*

```bash
# In a project it installs the loop here; outside one it installs the harness.
npx domangcha
```

```bash
# Then just say what you want. No slash command needed.
Build a Stripe invoicing tool for freelancers — invoices, email, paid/overdue dashboard
```

```bash
# Nothing else to learn. Say it however you like.
Refactor payments end to end and ship it
```

</div>

---

## ⚡ Why DOMANGCHA?

Claude Code and OpenAI Codex are powerful, but a trivial edit should not pay for a multi-agent pipeline—and a risky cross-cutting change should not rely on one unbounded prompt. **DOMANGCHA selects the minimum reliable execution shape**: DIRECT for simple work, LOOP for iterative correction, and GRAPH for explicit multi-stage topology. One deterministic router owns the decision and evidence adapters own completion; loops, graphs, memory, search, reviewers and the browser are native Claude Code.

<table>
<tr>
<td width="50%">

**🤖 Other AI tools**

```
You press Enter
└── 200 lines of code, immediately
    └── Wrong direction, wasted sprint
        └── Start over...
```

</td>
<td width="50%">

**🚗💨 DOMANGCHA**

```
You press Enter
└── Deterministic TaskRouter
    ├── DIRECT → answer or surgical edit
    ├── LOOP   → plan → execute → validate
    └── GRAPH  → branches → joins → gates
```

</td>
</tr>
</table>

| | DOMANGCHA | Typical AI tool |
|---|:---:|:---:|
| Complexity-aware execution | ✅ DIRECT / LOOP / GRAPH | ❌ One workflow for everything |
| Deterministic control flow | ✅ Typed routes and guarded edges | ❌ Prompt-only decisions |
| Role separation by specialist | ✅ 8 builder roles + native reviewers | ❌ Single writer/reviewer |
| Builder ≠ Reviewer (enforced) | ✅ Always | ❌ None |
| Breaking-change protection | ✅ Gate 5 blocks | ❌ None |
| Completion proven, not claimed | ✅ forced states + browser → DB trace | ❌ "build passed" |
| Feature extraction from other products | ✅ REA (`rea` MCP) in, evidence out | ❌ copy by eye |
| Lean context | ✅ 1.4 KB core, one line per DIRECT prompt | ❌ whole rulebook every turn |
| Checkpoint / resume | ✅ LOOP and GRAPH | ❌ Context-window dependent |
| Claude + Codex policy parity | ✅ Shared policy source | ❌ Runtime-specific drift |

---

## 🚀 Getting started

```bash
npx domangcha
```

That is the whole setup. Run it inside your project and say what you want in plain
language — no slash command, no flag, nothing to memorise.

```
you  ▸ add a login screen with email and password

     ▸ 🔁 DOMANGCHA · P0001 v0.2.0 ▓▓▓▓▓▓░░░░ 60% · items 3/5 · next I04
     ▸ writing the plan first (LOOP.md section 1), then item by item
```

Questions and lookups are answered directly. Anything that changes the repository goes
through plan → item → self-audit → pass, and every pass reports where it stands.

**Run it again to update.** The CLI is refreshed; your `LOOP.md` and `.loop/` state are never
overwritten, and `CLAUDE.md` is replaced only when it is the untouched old edition that loaded
the whole rulebook every session.

<details>
<summary><b>Details — where it installs, other package managers, options</b></summary>

<br/>

`npx domangcha` reads where you are:

| Where you run it | What it installs |
|---|---|
| inside a project | the loop, right there — offline, never writes to `~/.claude` |
| outside a project | the harness into `~/.claude` and `~/.domangcha` |

A project is a directory carrying `.git`, `package.json`, `pyproject.toml`, `go.mod`,
`Cargo.toml`, `pom.xml`, `build.gradle`, `Gemfile`, `composer.json`, `Makefile` or
`CMakeLists.txt`. The two never share a path, so an existing global install keeps working.

> **Run it, do not add it as a dependency.** npm shows `npm i domangcha` on every package
> page; this is a tool you run. Use `npx`, or `pnpm dlx` / `yarn dlx`. `npm i` inside a
> pnpm workspace fails with `Cannot read properties of null (reading 'matches')` — that is
> npm choking on pnpm's `node_modules`, and it can desynchronise your lockfile.

```bash
pnpm dlx domangcha            # pnpm project
yarn dlx domangcha            # Yarn project
npx domangcha --lang en       # English documents and CLI (default is Korean)
npx domangcha --no-migrate    # keep an existing CLAUDE.md where it is
npx domangcha --agents        # also symlink AGENTS.md and GEMINI.md to the CLAUDE.md core
```

Requires Node 22.13+ for the loop (`node:sqlite`, no dependencies). The harness needs
Python 3.10+, bash and git, and installs from the network.

To update the harness: `curl -sSL https://raw.githubusercontent.com/DoCoreTeam/domangcha/main/domangcha/install.sh | bash`,
or run `npx domangcha` from outside any project. Your registries are preserved.

</details>

### It decides when to escalate — you do not

Inside a loop project the global router steps aside and `LOOP.md` drives. When a request
is genuinely graph-scale, the loop asks the harness router and tells you, rather than
waiting for a magic word:

```
you  ▸ rewrite auth and run the migration

     ▸ harness router says: GRAPH (hard graph invariant: security)
     ▸ the loop can carry this as usual; if the harness and its gates would genuinely
       help, offer that to the user and escalate only once they agree
```

`/ceo` still forces the escalation if you want it, and installs the harness on demand.
It is a shortcut, never a requirement.

### Policies the agent writes for itself

A context reset normally erases "you already told me that." Repeated audit failures
become durable rules instead:

```
fail I01 ▸ hardcoded the strings again
         ▸ self-audit: I01 has failed 2 times; the same mistake is repeating
policy add ▸ P001 i18n keys
```

`P001` is re-injected on every later prompt, in `resume` after a context reset, and in
every item's self-audit — three paths, so a compaction cannot lose it. A rule broken three
times is retired and rewritten rather than repeated. Rules must be judgeable from a diff:
"be careful about i18n" is rejected in favour of "adding a user-facing string means editing
the ko and en message files in the same commit."

The loop speaks Korean and English; `--lang en` at install or `loop config set lang en` later
switches messages, the plan template and the protocol document.

---

## 🧭 Adaptive Execution Architecture

```text
User Request
     │
     ▼
Intent Normalization
     │
     ▼
TaskRouter (deterministic first)
     ├── Tier 1 · DIRECT
     ├── Tier 2 · LOOP
     └── Tier 3 · GRAPH
                    ├── native Workflow tool (pipeline / parallel / phase)
                    ├── resume with resumeFromRunId
                    └── approval through AskUserQuestion
```

| Route | Use it for | What DOMANGCHA deliberately avoids |
|---|---|---|
| **DIRECT** | explanations, formatting, summaries, lookups, trivial isolated edits | planner graphs, recursive loops, DOC explosion, unnecessary agent calls |
| **LOOP** | normal bug fixes, iterative refactors, validate-and-correct work | multi-agent topology when one bounded cycle is enough |
| **GRAPH** | cross-cutting architecture, security, DB+API+UI, parallel work, destructive or resumable workflows | free-text edge selection, unbounded retries, hidden failure paths |

Routing is deterministic first. Complexity scoring considers mutation scope, file and subsystem breadth, iteration, security, destructive effects, parallelism, approval, and resumability. An LLM can propose a route only at an ambiguous boundary; schema validation and code-owned invariants decide the final route. DIRECT may escalate to LOOP and LOOP to GRAPH while preserving task state.

### What DOMANGCHA owns, what is native

DOMANGCHA keeps routing and evidence. Everything Claude Code already does natively is delegated, not re-implemented:

| Concern | Where it runs |
|---|---|
| route selection | DOMANGCHA `TaskRouter` (deterministic) |
| LOOP iteration | bounded passes in the session (TodoWrite); native `/loop` + ScheduleWakeup to wait on CI or a deploy, and for `/ceo-ralph` |
| GRAPH topology | native Workflow tool — pipeline / parallel / phase, `resumeFromRunId` |
| human approval | native AskUserQuestion |
| review, security, QA, research, docs, SEO | native code-reviewer, security-reviewer, e2e-runner, Explore, doc-updater, seo-specialist, general-purpose |
| memory | native file memory (`~/.claude/projects/*/memory`, `MEMORY.md`) |
| web search | native WebSearch / WebFetch |
| browser | Claude-in-Chrome |
| completion of user-facing work | DOMANGCHA evidence adapters |
| checkpoints for Codex | DOMANGCHA `orchestration/checkpoint.py` |

### LOOP: bounded iteration

```text
PLAN → EXECUTE → VALIDATE → ACT
                         ├── success → COMPLETE
                         ├── failure → bounded retry
                         └── topology discovered → escalate to GRAPH
```

LOOP runs as bounded passes inside the session; native `/loop` is used only to wait on external state, or when you ask for `/ceo-ralph`. Termination needs completion evidence — tests, validators, an independent reviewer for meaningful code, and a passing evidence check for user-facing work. A model-written “done” is not sufficient.

### GRAPH: explicit topology

GRAPH work runs through the native Workflow tool: phases in a pipeline, independent branches in parallel, resumable with `resumeFromRunId`. Destructive, security-sensitive, or irreversible steps stop for AskUserQuestion approval.

### Evidence: proof, not claims

A user-facing feature is done when its evidence run passes (`domangcha/policies/evidence.md`). `engine.py evidence {init,start,record,state,trace,check,close,diff}` forces loading, empty, error and no-permission and captures each inside its window; traces one marker from the browser request through the server log to the stored database row; and tags every claim observation, derivation, inference or unknown, diffing against the previous run. The Stop hook blocks while an open run fails `check`.

To copy or benchmark a feature from another product, [REA](https://github.com/morluto/rea) (MIT) is connected as the `rea` MCP server (`npx rea-agents setup`). REA extracts from the other product, native Claude Code builds, DOMANGCHA evidence proves it works in ours.

### Token budget: small by default

What reaches the model on every turn is kept to what it needs right then. Hook output, measured in bytes against v4.0.0's first cut:

| Surface | Before | Now |
|---|---|---|
| loop project, loaded every session | 31.8 KB (`CLAUDE.md` + `@LOOP.md`, the whole rulebook) | 1.4 KB core; `LOOP.md` is read by section when it applies |
| loop project, per prompt | 1.7 KB (next action + full reporting contract) | 0.4 KB (next action + active policies) |
| harness, per DIRECT prompt | 1.8 KB (card + contract) | one line, under 0.1 KB |
| harness, per LOOP / GRAPH prompt | 1.8 KB | 0.4 KB (card + one line) |
| Codex plugin, per follow-up prompt | card + full contract | card + control line; contract on each new task and always in `~/.codex/AGENTS.md` |
| `install.sh`, skills listed every session | ECC + gstack + Superpowers forced | DOMANGCHA's own only; extras with `DOMANGCHA_WITH_EXTRAS=1` |

Real sessions, `claude -p` input tokens (2026-10-18, one machine):

| Case | v4.0.0 first cut | Now |
|---|---|---|
| loop project, a question (first turn) | 90,690 | 75,780 (−14,910) |
| loop project, "add a button" to its approval gate | 583,789 · $0.437 | 642,077 · $0.445 — no saving |
| `rea` MCP server, every turn | — | +2,750 |
| Claude Code with no user settings, empty folder | — | 17,560 |

Read the second row honestly: when the work needs the rulebook, the model greps `LOOP.md`'s headings and reads sections 0–2 and 8–9 (seen in the tool log), which costs extra turns. The core wins on questions and small edits. Most per-turn tokens on a busy machine come from user-level setup outside DOMANGCHA — rules, skills, agents and MCP servers — so keep that lean too.

The reporting contract did not go away: it lives once in the installed `CLAUDE.md` and rides on session start and post-compaction resume. Running `npx domangcha` again replaces an untouched old `CLAUDE.md` that imported the whole rulebook; an edited one is left alone and you are told how to slim it.

### Status reporting is on by default

An engine that works silently feels like an engine that is stuck. The route card comes from `orchestration/status.py`; progress after that shows on native surfaces — TodoWrite, Workflow phases, LOOP passes.

```text
🚂 DOMANGCHA · GRAPH 🧭 (score 11)
├ why: database + API + frontend invariant
├ plan: Workflow tool · parallel branches · join · approval gate
└ next: report per node and per branch
```

`engine.py route|status` prints a card by default (route, checkpoint, and drift cards); `--format json` returns the raw state and `--lang en` switches language (`DOMANGCHA_STATUS_LANG` sets the default). Announce the route and why, explain in plain language what an approval is for, and never go silent through a long step or hide a stall.

### Runtime compatibility

| Guarantee | Claude Code | Codex Local / IDE | Codex Cloud |
|---|---|---|---|
| Shared router, state, and validators | ✅ | ✅ | ✅ |
| Native attachment | hooks + commands | plugin skill + lifecycle hooks | plugin skill + checkpoints |
| Logical agent roles | Claude subagents | runtime-native agents | delegated agents when available |
| Human approval | interactive | interactive when supported | checkpoint and review |
| Browser verification | Claude-in-Chrome | capability-resolved | CI/headless capability |
| Checkpoint format | shared | shared | shared |

Runtime behavior is capability-based—not hard-coded to provider model names. Model policies express `HIGH_REASONING`, `BALANCED`, `FAST_CHEAP`, `LONG_CONTEXT`, or `REVIEW`; each adapter maps them to what is actually available. Unknown runtime or model names do not fail by default.

#### Codex-native attachment

Installing the harness (run `npx domangcha` outside a project) puts the bundled DOMANGCHA plugin into a local Codex marketplace and enables its native skill. After installation, open `/hooks` once and trust the DOMANGCHA hook definition. From the next new Codex thread:

- `UserPromptSubmit` automatically creates a canonical task and injects its route and task ID.
- the `domangcha` skill tells Codex how to execute and report through that same state.
- `PostToolUse` records mutations, successful validation commands, and independent subagent evidence.
- `Stop` allows DIRECT answers to finish immediately, but boundedly continues unfinished LOOP/GRAPH work when completion evidence is absent.
- state survives under the workspace `.domangcha/` directory, so follow-ups and continuation prompts reuse the same task instead of restarting.

The hooks are code control, not another prompt-only router: they call the same `ExecutionCoordinator` and `TaskRouter` used by Claude and the CLI.

---

## 🔄 Pipeline

```text
/ceo "task"
      │
      ▼
┌──────────────────────┐
│ INTENT NORMALIZATION │  request, goal, scope, constraints, risk signals
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ TASKROUTER           │  deterministic filter → complexity score
└───┬─────────┬────────┘
    │         │
    │ obvious │ ambiguous boundary only
    │         └── structured semantic proposal → schema + invariant validation
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ DIRECT                 LOOP                       GRAPH              │
│ answer / small edit     PLAN → EXECUTE             Workflow tool     │
│ focused validation     → VALIDATE → ACT            pipeline/parallel │
│                        bounded retry                resumeFromRunId   │
│                        passes in TodoWrite          AskUserQuestion   │
└───────────┬──────────────────┬──────────────────────────┬─────────────┘
            └──────────────────┴──────────────────────────┘
                               ▼
                    task-relevant validators + evidence check
                               ▼
                    COMPLETE / PAUSED / FAILED
```

Complex feature requests still run PLANNER → BUILDER → EVALUATOR inside GRAPH, with native agents as evaluators. Small read-only requests do not create planning documents or invoke all agents. Meaningful implementation preserves Builder ≠ Reviewer; destructive, security-sensitive, or irreversible steps require an explicit approval edge.

---

## 👥 The 8 Agent Roles

<table>
<thead>
<tr><th>Phase</th><th>Agent</th><th>Role</th><th>Model Policy</th></tr>
</thead>
<tbody>
<tr><td><b>🧠 PLANNER</b></td>
  <td><code>DC-BIZ</code></td><td>Business Judge</td><td>HIGH_REASONING</td></tr>
<tr><td rowspan="7"><b>🔨 BUILDER</b></td>
  <td><code>DC-DEV-DB</code></td><td>Database Engineer</td><td>HIGH_REASONING</td></tr>
<tr><td><code>DC-DEV-BE</code></td><td>Backend Developer</td><td>HIGH_REASONING</td></tr>
<tr><td><code>DC-DEV-FE</code></td><td>Frontend Developer</td><td>HIGH_REASONING</td></tr>
<tr><td><code>DC-DEV-OPS</code></td><td>DevOps Engineer</td><td>HIGH_REASONING</td></tr>
<tr><td><code>DC-DEV-MOB</code></td><td>Mobile Developer</td><td>HIGH_REASONING</td></tr>
<tr><td><code>DC-DEV-INT</code></td><td>Integration Engineer</td><td>HIGH_REASONING</td></tr>
<tr><td><code>DC-WRT</code></td><td>Copywriter</td><td>FAST_CHEAP</td></tr>
</tbody>
</table>

> Evaluation and support use native Claude Code agents: code-reviewer, security-reviewer, e2e-runner, Explore, doc-updater, seo-specialist, general-purpose. DIRECT normally invokes none. `domangcha/manifests/agents.json` is the authoritative manifest.

---

## 🛡️ The 5 Gates

> Gates are applied when relevant to the work. DIRECT avoids ceremonial evaluators; code mutation, security, release, and destructive workflows receive the validators and approval boundaries they require.

| Gate | Check |
|:---:|---|
| **① SCAN** | error patterns, secrets, repository rules, maintainability checks |
| **② CRITERIA** | task-specific completion evidence, tests, lint, typecheck, build |
| **③ CONSISTENCY** | manifests, versions, graph schema, reachable terminal states |
| **④ SEPARATION** | meaningful implementation cannot be its only reviewer |
| **⑤ SAFETY** | breaking, destructive, or irreversible work requires explicit approval |

---

## 🆕 What's New

| Version | What changed |
|---|---|
| **v4.0.0** | Native delegation: loops, graphs, memory, search, reviewers, and the browser are Claude Code's own; DOMANGCHA keeps the router and adds evidence adapters (state · trace · provenance) and REA. Token budget: a 1.4 KB loop core instead of the 31.8 KB rulebook, one line per DIRECT prompt, contract sent once per session (Codex: once per task), extra skill bundles opt-in. The installer installs from the checkout it runs in. Breaking: 10 agents and 14 commands removed |
| **v3.0.5** | Terminal output paints English bright and Korean dim, so one language carries and the other confirms |
| **v3.0.4** | No slash command is required: the loop asks the harness router itself; README usage cut to one block |
| **v3.0.3** | Install-time output is bilingual, English first, everywhere |
| **v3.0.2** | Never edits your package.json; an update says it is an update; `npm i` vs `npx` spelled out |
| **v3.0.1** | The loop carries the reporting contract itself, so progress is reported inside a loop project too |
| **v3.0.0** | One flag-free command installs by location; plain language runs a project loop, `/ceo` raises it to the harness; policies self-learn; Korean and English |
| **v2.3.2** | The single renderer stops carrying the phrasebook |
| **v2.3.1** | Hooks stop misfiring on unrelated projects, and stale deployments become visible |
| **v2.3.0** | Progress reporting is on by default |
| **v2.2.0** | Native Codex attachment |
| **v2.1.1** | Full public README restored and modernized |
| **v2.1.0** | Adaptive DIRECT · LOOP · GRAPH architecture |
| **v2.0.58** | Browser verification now Chrome-extension-first |

24 older releases: [full changelog](https://github.com/DoCoreTeam/domangcha/releases)

---

## 🔄 Updates

**How updates work:**

Files are installed to `~/.claude/` on first run. They do **not** auto-update while a project is in progress — the version at install time is what runs.

**To update the harness:** run `curl -fsSL https://raw.githubusercontent.com/DoCoreTeam/domangcha/main/domangcha/install.sh | bash`, or `npx domangcha` from outside a project. Your error registry and project registries are preserved. Memory is native Claude Code file memory and is never overwritten.

**Auto-update prompt (built-in):** Every `/ceo` call silently checks the npm registry for a newer version. If one exists, you'll see:

```
[CEO] New version v2.0.33 available (installed: v2.0.31).
Update before continuing? (y/n):
```

- `y` → reinstalls the harness in place, then continues with your task
- `n` / Enter → skips and continues without updating

Version check failures (offline, etc.) are silently ignored — your task is never blocked.

---

## 🖥️ Commands

**Every command here is optional.** Plain language does the same work; these are shortcuts.

In a loop project: `/plan` writes the plan for a new instruction, `/loop` resumes the next
item, `/policy` checks active policies against your diff. The CLI behind them is
`node scripts/loop.mjs` — run `help` for every subcommand, `resume` for what to do next,
`status --all` for every registered project.

With the harness: `/ceo "task"` routes explicitly, and four more `/ceo-*` intents
(`-ralph -debug -security -ship`) set a minimum route. `/ceo-ralph` runs on native `/loop`;
`/ceo-ship` runs `evidence check` before anything ships. They are adapters into the same
TaskRouter, which already reads plain prompts — so none of them is required.

---

## 📐 Coding Standards

Non-negotiable. Gate 1 enforces on every file.

```
✓ 300 lines max per file  ·  50 lines max per function  ·  4 levels max nesting
✓ Immutability — always create new, never mutate existing
✓ Explicit error handling at every level  ·  Input validation at every boundary
✓ Tests required for every feature  ·  Row-Level Security on every table
```

---

## 📦 Requirements

DOMANGCHA is a runtime-aware developer harness for Claude Code and OpenAI Codex. It uses native capabilities when available and preserves the same routing, safety, state, and reviewer-separation guarantees across runtimes.

| | Project loop (inside a project) | Harness (outside a project, or `/ceo`) |
|---|---|---|
| Coding agent | Claude Code, or Cursor | Claude Code, or OpenAI Codex |
| Node.js | **22.13+** — `node:sqlite`, no npm dependencies | 14+ for npm installation |
| Python | not used | 3.10+ for the deterministic orchestration engine |
| `git` | commits each passing item | installer, repository checks, reviewable diffs |
| Network | not required — templates ship in the package | required — pulls `install.sh` from GitHub |

---

## 🔀 Coming from v2.x

Nothing breaks and nothing was removed.

- **Keep everything as-is** — your harness is untouched. Refresh it with the curl one-liner
  above, or by running `npx domangcha` from outside any project.
- **Try the loop on one project** — `cd` into it and run `npx domangcha`. Your global install
  stays; inside that project the router yields to `LOOP.md`, and `/ceo` brings it straight back.
- **An existing project `CLAUDE.md`** moves to `.claude/heavy/CEO.md` and is read back for
  items marked heavy. Pass `--no-migrate` to keep it in place.
- **Going back** — delete `LOOP.md`, `scripts/loop.mjs` and `.loop/`, then restore `CLAUDE.md`
  from `.claude/heavy/CEO.md`.

**Codex first run:** restart Codex, open `/hooks`, and trust the DOMANGCHA plugin hooks once. Start a new thread; routing and task state are then attached automatically. Use `$domangcha` explicitly when you want to force skill selection.

---

<details>
<summary><b>🇰🇷 한국어 (Korean) — 클릭하여 펼치기 / Click to expand</b></summary>

<br/>
<div align="center"><pre>
██████╗  ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗ ██████╗  ██████╗ ██╗  ██╗ █████╗
██╔══██╗██╔═══██╗████╗ ████║██╔══██╗████╗  ██║██╔════╝ ██╔════╝ ██║  ██║██╔══██╗
██║  ██║██║   ██║██╔████╔██║███████║██╔██╗ ██║██║  ███╗██║      ███████║███████║
██║  ██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║   ██║██║      ██╔══██║██╔══██║
██████╔╝╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║╚██████╔╝╚██████╗ ██║  ██║██║  ██║
╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝
</pre></div>

### 🚗💨 돔황차 — Claude Code와 OpenAI Codex를 위한 적응형 엔지니어링

**강력한 코딩 에이전트에 필요한 만큼의 오케스트레이션만 더합니다.**
명령 하나, 외울 것 없음: `npx domangcha` 가 실행한 자리를 보고 필요한 것을 설치합니다.
그다음엔 그냥 말하면 됩니다 — 루프가 계획하고 감사하고 보고하며, 사용자 화면은 주장 대신 증거로 완료를 증명합니다.

*개발 지옥에서 도망쳐 — 돔황차🚗💨*

[![Version](https://img.shields.io/badge/version-4.0.0-brightgreen?style=for-the-badge&logo=github)](https://github.com/DoCoreTeam/domangcha/blob/main/domangcha/VERSION)
[![npm](https://img.shields.io/npm/v/domangcha?style=for-the-badge&logo=npm&color=CB3837)](https://www.npmjs.com/package/domangcha)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Runtimes](https://img.shields.io/badge/런타임-Claude%20Code%20%7C%20Codex-5865F2?style=for-the-badge)](#runtime-compatibility)
[![Agents](https://img.shields.io/badge/에이전트-8명-FF6B6B?style=for-the-badge)](https://github.com/DoCoreTeam/domangcha)
[![Gates](https://img.shields.io/badge/게이트-5개-orange?style=for-the-badge)](https://github.com/DoCoreTeam/domangcha)
[![Node](https://img.shields.io/badge/Node-22.13%2B-339933?style=for-the-badge&logo=nodedotjs)](https://nodejs.org)

> **명령 하나 쳤더니 인증, 결제, 대시보드가 돌아왔다. 테스트 통과, 보안 감사 완료, 코드 리뷰까지.**
>
> *— Michael Dohyeon Kim, KDC CEO · DOMANGCHA 제작자*

```bash
# 프로젝트 안이면 여기에 루프를, 프로젝트 밖이면 하네스를 설치합니다
npx domangcha
```

```bash
# 그다음엔 그냥 하고 싶은 일을 말하면 됩니다. 슬래시 커맨드 불필요.
프리랜서용 Stripe 인보이스 툴 만들어줘 — 인보이스 생성, 이메일 발송, 미납/완납 대시보드
```

```bash
# 더 배울 것 없습니다. 편한 대로 말하면 됩니다.
결제 전체 리팩터링하고 배포까지
```

---

### 🚀 시작하기

```bash
npx domangcha
```

세팅은 이게 전부입니다. 프로젝트 안에서 실행하고, 하고 싶은 일을 그냥 말하면 됩니다 —
슬래시 커맨드도, 플래그도, 외울 것도 없습니다.

```
당신 ▸ 이메일·비밀번호로 로그인 화면 만들어줘

     ▸ 🔁 DOMANGCHA · P0001 v0.2.0 ▓▓▓▓▓▓░░░░ 60% · 항목 3/5 · 다음 I04
     ▸ 먼저 플랜을 씁니다 (LOOP.md 1절), 그다음 항목 하나씩
```

질문이나 조회는 바로 답합니다. 저장소를 바꾸는 일만 플랜 → 항목 → 자가감사 → 통과를
거치고, 매 패스마다 지금 어디쯤인지 보고합니다.

**업데이트도 같은 명령입니다.** CLI 만 갱신되고 `LOOP.md` 와 `.loop/` 상태는 덮어쓰지 않습니다.
`CLAUDE.md` 는 규정 전체를 매 세션 불러오던 손대지 않은 옛 판일 때만 핵심판으로 바뀝니다.

<details>
<summary><b>자세히 — 어디에 설치되는지, 다른 패키지 매니저, 옵션</b></summary>

<br/>

`npx domangcha` 는 실행한 자리를 보고 판단합니다.

| 어디서 실행했나 | 무엇을 설치하나 |
|---|---|
| 프로젝트 안 | 그 자리에 루프 — 오프라인, `~/.claude` 무접촉 |
| 프로젝트 밖 | `~/.claude` 와 `~/.domangcha` 에 하네스 |

프로젝트로 인정하는 기준은 `.git`, `package.json`, `pyproject.toml`, `go.mod`,
`Cargo.toml`, `pom.xml`, `build.gradle`, `Gemfile`, `composer.json`, `Makefile`,
`CMakeLists.txt` 중 하나가 있는 디렉터리입니다. 두 방식은 경로를 공유하지 않으므로
기존 전역 설치가 그대로 살아 있습니다.

> **설치하지 말고 실행하세요.** npm 페이지는 모든 패키지에 `npm i domangcha` 를 자동으로
> 띄우지만 이건 실행하는 도구입니다. `npx`, 또는 `pnpm dlx` / `yarn dlx` 를 쓰세요.
> pnpm 워크스페이스에서 `npm i` 를 하면 `Cannot read properties of null (reading 'matches')`
> 로 실패하는데, npm 이 pnpm 의 `node_modules` 를 읽지 못해서이며 lockfile 이 어긋날 수 있습니다.

```bash
pnpm dlx domangcha            # pnpm 프로젝트
yarn dlx domangcha            # Yarn 프로젝트
npx domangcha --lang en       # 문서와 CLI 를 영어로 (기본은 한국어)
npx domangcha --no-migrate    # 기존 CLAUDE.md 를 그 자리에 그대로 둠
npx domangcha --agents        # AGENTS.md, GEMINI.md 를 CLAUDE.md 핵심판으로 심볼릭 링크
```

루프는 Node 22.13 이상이 필요합니다 (`node:sqlite`, 의존성 없음). 하네스는 Python 3.10 이상,
bash, git 이 필요하고 네트워크로 설치됩니다.

하네스 갱신: `curl -sSL https://raw.githubusercontent.com/DoCoreTeam/domangcha/main/domangcha/install.sh | bash`
또는 프로젝트 밖에서 `npx domangcha`. 레지스트리는 보존됩니다.

</details>

### 언제 올릴지는 도구가 판단합니다

루프 프로젝트 안에서는 전역 라우터가 물러나고 `LOOP.md` 가 주도합니다. 그러다 요청이
정말 그래프 규모면, 루프가 하네스 라우터에게 직접 물어보고 알려줍니다 — 매직 워드를
기다리지 않습니다.

```
당신 ▸ 인증 갈아엎고 마이그레이션 돌려줘

     ▸ 하네스 라우터 분류: GRAPH (hard graph invariant: security)
     ▸ 루프로 그대로 진행해도 됩니다. 하네스와 게이트가 정말 도움이 되겠다 싶으면
       사용자에게 제안하고 승인받은 뒤에만 올리세요
```

`/ceo` 로 직접 올릴 수도 있고, 하네스가 없으면 그때 설치를 제안합니다.
어디까지나 단축키이지 필수가 아닙니다.

### 에이전트가 스스로 쓰는 정책

컨텍스트가 초기화되면 "아까 말했잖아"가 사라집니다. 반복된 감사 실패를 지속되는
규칙으로 바꿔 둡니다.

```
fail I01 ▸ 또 하드코딩
         ▸ 자체감사: I01 감사 실패 2회 누적, 같은 실수가 반복되고 있음
policy add ▸ P001 i18n 키 강제
```

`P001` 은 이후 모든 프롬프트, 컨텍스트 초기화 후의 `resume`, 매 항목 자가감사
세 경로로 다시 주입됩니다. 같은 정책을 3회 어기면 반복하는 대신 폐기하고 더 구체적으로
다시 씁니다. 규칙은 diff 로 위반 여부를 판정할 수 있어야 하며, "i18n 을 잘 지킨다" 대신
"사용자 노출 문자열을 추가하면 같은 커밋에서 ko en 메시지 파일을 함께 수정한다" 같은
형태만 인정합니다.

루프는 한국어와 영어를 모두 씁니다. 설치할 때 `--lang en`, 또는 나중에
`loop config set lang en` 으로 메시지·플랜 템플릿·프로토콜 문서가 함께 바뀝니다.

---

### ⚡ 왜 DOMANGCHA인가?

Claude Code와 OpenAI Codex는 강력하지만, 간단한 수정에 다중 에이전트 파이프라인을 돌릴 이유는 없습니다. 반대로 보안·DB·API·UI가 얽힌 변경을 단일 프롬프트에 맡겨서도 안 됩니다. **DOMANGCHA는 신뢰성에 필요한 최소 실행 구조**인 DIRECT, LOOP, GRAPH를 결정론적으로 선택하고, 완료는 증거 어댑터가 판정합니다. 루프·그래프·메모리·검색·리뷰어·브라우저는 Claude Code 네이티브 기능을 씁니다.

<table>
<tr>
<td width="50%">

**🤖 다른 AI 도구들**

```
엔터를 치는 순간
└── 코드 200줄, 즉시
    └── 틀린 방향, 낭비된 스프린트
        └── 처음부터 다시...
```

</td>
<td width="50%">

**🚗💨 DOMANGCHA**

```
엔터를 치는 순간
└── 결정론적 TaskRouter
    ├── DIRECT → 답변 또는 국소 수정
    ├── LOOP   → 계획 → 실행 → 검증
    └── GRAPH  → 분기 → 조인 → 게이트
```

</td>
</tr>
</table>

| | DOMANGCHA | 일반 AI 도구 |
|---|:---:|:---:|
| 복잡도별 실행 | ✅ DIRECT / LOOP / GRAPH | ❌ 모든 일에 같은 워크플로 |
| 결정론적 제어 흐름 | ✅ 타입 라우트 + 가드 엣지 | ❌ 프롬프트 전용 판단 |
| 전문가 역할 분리 | ✅ 8개 빌더 역할 + 네이티브 리뷰어 | ❌ 작성자 단독 검토 |
| 빌더 ≠ 리뷰어 강제 | ✅ 항상 분리 | ❌ 없음 |
| 파괴적 변경 보호 | ✅ Gate 5 차단 | ❌ 없음 |
| 주장이 아닌 증거로 완료 | ✅ 강제 상태 + 브라우저 → DB 추적 | ❌ "빌드 통과" |
| 다른 제품 기능 추출 | ✅ REA(`rea` MCP)로 추출, 증거로 검증 | ❌ 눈대중 복제 |
| 가벼운 컨텍스트 | ✅ 1.4 KB 핵심판, DIRECT 는 프롬프트당 한 줄 | ❌ 매 턴 규정 전체 |
| 체크포인트 / 재개 | ✅ LOOP와 GRAPH | ❌ 컨텍스트 창에 종속 |
| Claude + Codex 정책 동등성 | ✅ 공통 정책 원본 | ❌ 런타임별 드리프트 |

---

### 🆕 최신 업데이트

| 버전 | 바뀐 것 |
|---|---|
| **v4.0.0** | 네이티브 위임 — 루프·그래프·메모리·검색·리뷰어·브라우저는 Claude Code 기본 기능으로, DOMANGCHA는 라우터를 남기고 증거 어댑터(state · trace · provenance)와 REA를 더함. 토큰 예산 — 31.8 KB 규정 대신 1.4 KB 루프 핵심판, DIRECT 는 프롬프트당 한 줄, 보고 계약은 세션당 한 번(Codex 는 작업당 한 번), 추가 스킬 묶음은 선택 설치. 설치기는 실행한 체크아웃에서 설치. 호환성 변경: 에이전트 10개·명령 14개 제거 |
| **v3.0.5** | 터미널 출력에서 영어는 또렷하게, 한글은 흐리게 — 한쪽만 읽어도 되게 |
| **v3.0.4** | 슬래시 커맨드 불필요 — 루프가 하네스 라우터에 직접 질의, README 사용법 한 곳으로 압축 |
| **v3.0.3** | 설치 시점 출력 전부 이중언어, 영어 우선 |
| **v3.0.2** | 사용자 package.json 을 건드리지 않음, 업데이트를 업데이트라고 알림, `npm i` 와 `npx` 구분 안내 |
| **v3.0.1** | 루프가 보고 계약을 직접 실어, 루프 프로젝트에서도 진행 상황을 보고함 |
| **v3.0.0** | 플래그 없는 한 명령이 실행 위치를 보고 설치, 자연어는 프로젝트 루프 · `/ceo` 는 하네스로 승격, 정책 자가학습, 한국어·영어 지원 |
| **v2.3.2** | 단일 렌더러에서 문구 사전 분리 |
| **v2.3.1** | 훅 오탐 제거 + 배포 누락 가시화 |
| **v2.3.0** | 진행 상황 보고 기본 활성화 |
| **v2.2.0** | Codex 네이티브 밀착 통합 |
| **v2.1.1** | 기존 공개 README 수준 완전 복원 및 현대화 |
| **v2.1.0** | 적응형 DIRECT · LOOP · GRAPH 아키텍처 |
| **v2.0.58** | 브라우저 검증 기본을 Chrome 확장 우선으로 전환 |

이전 25개 릴리스: [전체 변경 이력](https://github.com/DoCoreTeam/domangcha/releases)

---

### 🔄 적응형 파이프라인

```text
/ceo "업무"
      │
      ▼
의도 정규화 → 결정론적 TaskRouter
      ├── DIRECT  설명·요약·조회·국소 수정
      ├── LOOP    PLAN → EXECUTE → VALIDATE → ACT
      └── GRAPH   네이티브 Workflow 툴 (pipeline / parallel / phase)
                                  → resumeFromRunId → AskUserQuestion 승인
      │
      ▼
업무에 필요한 검증 + 증거 확인만 수행
      │
      └── COMPLETE / PAUSED / FAILED
```

- **DIRECT**는 플래너 그래프, 재귀 루프, 불필요한 문서와 다중 에이전트를 만들지 않습니다.
- **LOOP**는 세션 안에서 한정된 회차로 돌고(TodoWrite), CI·배포처럼 바깥 상태를 기다릴 때와 `/ceo-ralph` 에서만 네이티브 `/loop`·ScheduleWakeup 을 씁니다. 테스트·검증기·독립 리뷰·증거 확인이 있어야 끝납니다.
- **GRAPH**는 보안, 파괴적 변경, DB+API+UI, 병렬 작업, 중단·재개가 필요한 업무에만 쓰며 네이티브 Workflow 툴로 실행합니다.
- LLM은 경계가 모호할 때 구조화된 라우트를 제안할 수 있지만, 안전 불변식과 최종 전이는 코드가 결정합니다.
- DIRECT → LOOP → GRAPH 승격 시 기존 작업 상태를 보존합니다.
- Claude Code는 `CLAUDE.md`, Codex는 `AGENTS.md`를 사용하지만 공유 정책·엔진·체크포인트·검증 규칙은 같습니다.

#### 증거: 주장이 아닌 증명

사용자 화면이 있는 기능은 증거 실행이 통과해야 완료입니다 (`domangcha/policies/evidence.md`).
`engine.py evidence {init,start,record,state,trace,check,close,diff}` 가 로딩·빈 상태·오류·권한 없음을 강제로 띄워 그 창 안에서 캡처하고,
고유 마커 하나를 브라우저 요청 → 서버 로그 → 저장된 DB 행까지 추적하고, 모든 주장을 observation·derivation·inference·unknown 으로 태그해 이전 실행과 비교합니다.
열린 실행이 `check` 를 통과하지 못하면 Stop 훅이 막습니다.

다른 제품의 기능을 가져오거나 벤치마킹할 때는 [REA](https://github.com/morluto/rea)(MIT)를 `rea` MCP 서버로 연결해 씁니다 (`npx rea-agents setup`).
REA 가 추출하고, 네이티브 Claude Code 가 만들고, DOMANGCHA 증거가 우리 제품에서 동작함을 증명합니다.

### 🪶 토큰 예산 — 기본이 가볍게

매 턴 모델에 들어가는 것은 그 순간 필요한 것만 남겼습니다. 훅 출력은 v4.0.0 첫 판과 같은 입력으로 바이트를 잰 값입니다.

| 지점 | 전 | 지금 |
|---|---|---|
| 루프 프로젝트, 매 세션 상시 로드 | 31.8 KB (`CLAUDE.md` + `@LOOP.md` 규정 전체) | 1.4 KB 핵심판, `LOOP.md` 는 필요한 절만 그때 읽음 |
| 루프 프로젝트, 프롬프트마다 | 1.7 KB (다음 행동 + 보고 계약 전체) | 0.4 KB (다음 행동 + 활성 정책) |
| 하네스, DIRECT 프롬프트마다 | 1.8 KB (카드 + 계약) | 한 줄, 0.1 KB 미만 |
| 하네스, LOOP / GRAPH 프롬프트마다 | 1.8 KB | 0.4 KB (카드 + 한 줄) |
| Codex 플러그인, 후속 프롬프트마다 | 카드 + 계약 전체 | 카드 + 제어 줄, 계약은 새 작업마다 그리고 `~/.codex/AGENTS.md` 에 상시 |
| `install.sh`, 매 세션 목록에 오르는 스킬 | ECC + gstack + Superpowers 강제 설치 | DOMANGCHA 것만, 추가 묶음은 `DOMANGCHA_WITH_EXTRAS=1` |

실제 세션, `claude -p` 입력 토큰 (2026-10-18, 한 대의 PC):

| 경우 | v4.0.0 첫 판 | 지금 |
|---|---|---|
| 루프 프로젝트, 질문 하나 (첫 턴) | 90,690 | 75,780 (−14,910) |
| 루프 프로젝트, "버튼 추가" 를 승인 직전까지 | 583,789 · $0.437 | 642,077 · $0.445 — 절감 없음 |
| `rea` MCP 서버, 매 턴 | — | +2,750 |
| 사용자 설정 없는 Claude Code, 빈 폴더 | — | 17,560 |

두 번째 줄을 그대로 읽어 주세요. 규정이 필요한 작업이면 모델이 `LOOP.md` 의 제목을 찾아 0~2절과 8~9절을 읽고(도구 로그로 확인), 그만큼 턴이 늘어납니다. 핵심판이 이기는 건 질문과 작은 수정입니다. 바쁜 PC 의 턴당 토큰 대부분은 DOMANGCHA 밖의 사용자 설정 — 규칙·스킬·에이전트·MCP 서버 — 에서 나오므로 그쪽도 가볍게 유지하세요.

보고 계약은 없어지지 않았습니다. 설치된 `CLAUDE.md` 에 한 번만 있고 세션 시작과 컨텍스트 압축 뒤 재개 때 함께 나갑니다. `npx domangcha` 를 다시 실행하면 규정 전체를 불러오던 손대지 않은 옛 `CLAUDE.md` 는 핵심판으로 바뀌고, 직접 고친 파일은 그대로 두고 줄이는 방법만 알려줍니다.

---

### 📣 진행 상황 보고 (기본 활성)

조용히 도는 엔진은 멈춘 엔진처럼 보입니다. 라우트 카드는 `orchestration/status.py` 가 그리고,
그 뒤 진행은 네이티브 표면 — TodoWrite, Workflow phase, LOOP 회차 — 으로 보입니다.

```text
🚂 DOMANGCHA · GRAPH 🧭 (score 11)
├ 이유: database + API + frontend invariant
├ 계획: Workflow 툴 · 병렬 브랜치 · join · 승인 게이트
└ 다음: 노드별·브랜치별 진행 상태를 보고합니다
```

`engine.py route|status`는 기본으로 카드(라우트·체크포인트·드리프트)를 출력합니다. 원시 상태는 `--format json`,
언어는 `--lang ko|en`(기본값은 `DOMANGCHA_STATUS_LANG`)으로 바꿉니다. 라우트와 그 이유를 먼저 알리고,
승인 앞에서 무엇을 왜 승인받는지 사람의 말로 설명하고, 긴 단계에서 침묵하거나 정체를 감추지 않습니다.

---

### 👥 8개의 에이전트 역할

<table>
<thead>
<tr><th>단계</th><th>에이전트</th><th>역할</th><th>모델 정책</th></tr>
</thead>
<tbody>
<tr><td><b>🧠 기획자</b></td>
  <td><code>DC-BIZ</code></td><td>사업 타당성 판단</td><td>HIGH_REASONING</td></tr>
<tr><td rowspan="7"><b>🔨 빌더</b></td>
  <td><code>DC-DEV-DB</code></td><td>데이터베이스 엔지니어</td><td>HIGH_REASONING</td></tr>
<tr><td><code>DC-DEV-BE</code></td><td>백엔드 개발자</td><td>HIGH_REASONING</td></tr>
<tr><td><code>DC-DEV-FE</code></td><td>프론트엔드 개발자</td><td>HIGH_REASONING</td></tr>
<tr><td><code>DC-DEV-OPS</code></td><td>DevOps 엔지니어</td><td>HIGH_REASONING</td></tr>
<tr><td><code>DC-DEV-MOB</code></td><td>모바일 개발자</td><td>HIGH_REASONING</td></tr>
<tr><td><code>DC-DEV-INT</code></td><td>통합(Integration) 엔지니어</td><td>HIGH_REASONING</td></tr>
<tr><td><code>DC-WRT</code></td><td>카피라이터</td><td>FAST_CHEAP</td></tr>
</tbody>
</table>

> 평가와 지원은 Claude Code 네이티브 에이전트가 맡습니다: code-reviewer, security-reviewer, e2e-runner, Explore, doc-updater, seo-specialist, general-purpose. DIRECT는 보통 역할을 호출하지 않습니다. 권위 원본은 `domangcha/manifests/agents.json`입니다.

---

### 🛡️ 5개의 게이트

> 업무 위험도에 맞는 게이트를 적용합니다. DIRECT에는 의례적인 평가기를 붙이지 않으며, 코드 변경·보안·릴리스·파괴적 작업에는 필요한 검증과 승인 경계를 강제합니다.

| 게이트 | 검증 항목 |
|:---:|---|
| **① 스캔** | 오류 패턴, 비밀정보, 저장소 규칙, 유지보수성 검사 |
| **② 기준** | 업무별 완료 근거, 테스트, 린트, 타입체크, 빌드 |
| **③ 일관성** | 매니페스트, 버전, 그래프 스키마, 도달 가능한 종료 상태 |
| **④ 분리** | 의미 있는 구현의 작성자와 유일 리뷰어를 분리 |
| **⑤ 안전** | 파괴적·비가역·호환성 파괴 작업에 명시적 승인 |

---

### 🖥️ 명령어

**여기 있는 명령은 전부 선택 사항입니다.** 자연어로 말해도 같은 일을 하고, 이건 단축키입니다.

루프 프로젝트에서는 `/plan` 이 새 지시의 플랜을 쓰고, `/loop` 가 다음 항목부터 재개하고,
`/policy` 가 활성 정책을 현재 변경분에 대조합니다. 그 뒤의 CLI 는 `node scripts/loop.mjs` 이고,
`help` 로 전체 하위 명령, `resume` 으로 다음에 할 일, `status --all` 로 등록된 모든 프로젝트를
볼 수 있습니다.

하네스가 있으면 `/ceo "업무"` 로 명시 라우팅을 하고, 4개 `/ceo-*` 인텐트
(`-ralph -debug -security -ship`) 가 최소 라우트를 지정합니다. `/ceo-ralph` 는 네이티브 `/loop` 로 돌고,
`/ceo-ship` 은 배포 전에 `evidence check` 를 실행합니다. 전부 같은
TaskRouter 로 들어가는 어댑터이고, 그 라우터는 이미 평범한 프롬프트를 읽습니다 —
그래서 어느 것도 필수가 아닙니다.

---

### 📐 코딩 표준

타협 불가. Gate 1이 모든 파일에서 강제합니다.

```
✓ 파일당 최대 300줄  ·  함수당 최대 50줄  ·  중첩 최대 4단계
✓ 불변성(Immutability) — 항상 새로 만들고, 절대 변경하지 않기
✓ 모든 계층에서 명시적 에러 처리  ·  모든 경계에서 입력 검증
✓ 모든 기능에 테스트 필수  ·  모든 테이블에 RLS 적용
```

---

### 📦 요구사항

| | 프로젝트 루프 (프로젝트 안) | 하네스 (프로젝트 밖, 또는 `/ceo`) |
|---|---|---|
| 코딩 에이전트 | Claude Code 또는 Cursor | Claude Code 또는 OpenAI Codex |
| Node.js | **22.13 이상** — `node:sqlite`, npm 의존성 없음 | npm 설치용 14 이상 |
| Python | 사용 안 함 | 결정론적 엔진용 3.10 이상 |
| `git` | 항목이 통과할 때마다 커밋 | 설치·저장소 검사·리뷰 가능한 diff |
| 네트워크 | 불필요 — 템플릿이 패키지에 동봉됨 | 필요 — GitHub 에서 `install.sh` 를 받아옴 |

---

### 🔀 v2.x 에서 올라오기

깨지는 것도, 없어지는 것도 없습니다.

- **지금 그대로 쓰고 싶다** — 하네스는 건드려지지 않았습니다. 위 curl 명령이나, 프로젝트 밖에서
  `npx domangcha` 로 갱신하세요.
- **한 프로젝트에서만 루프를 써 보고 싶다** — 그 폴더에서 `npx domangcha`. 전역 설치는 그대로
  있고, 그 프로젝트 안에서만 라우터가 `LOOP.md` 에 자리를 내줍니다.
- **프로젝트에 이미 `CLAUDE.md` 가 있다면** 자동으로 `.claude/heavy/CEO.md` 로 옮겨지고 중량
  항목에서 다시 읽힙니다. 그 자리에 두려면 `--no-migrate`.
- **되돌리려면** `LOOP.md`, `scripts/loop.mjs`, `.loop/` 를 지우고 `.claude/heavy/CEO.md` 를
  `CLAUDE.md` 로 복원하면 됩니다.

**Codex 최초 실행:** Codex를 재시작하고 `/hooks`에서 DOMANGCHA plugin hook을 최초 1회 신뢰하세요. 새 스레드부터 라우팅과 작업 상태가 자동으로 붙습니다. skill 선택을 명시하려면 `$domangcha`를 사용합니다.

</details>

---

<div align="center">

**Escape development hell. 🚗💨 DOMANGCHA is your getaway car.**

[![GitHub](https://img.shields.io/badge/GitHub-DoCoreTeam-181717?style=for-the-badge&logo=github)](https://github.com/DoCoreTeam/domangcha)
[![npm](https://img.shields.io/badge/npm-domangcha-CB3837?style=for-the-badge&logo=npm)](https://www.npmjs.com/package/domangcha)

---

**Built by [Michael Dohyeon Kim](https://github.com/DoCoreTeam)**
CEO of KDC (Korea Development Company) · Serial builder · Claude Code power user

*I built DOMANGCHA because I was drowning in manual orchestration.*
*Now I ship features in hours that used to take days.*
*This is my exact setup — open-sourced.*

MIT License · Star it if it's useful ⭐

</div>
