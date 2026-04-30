# MACC

### You just hired a 16-person engineering team.
### 16명의 엔지니어링 팀을 단 한 줄로 채용하세요.

[![Version](https://img.shields.io/badge/version-2.0.11-brightgreen.svg)](https://github.com/DoCoreTeam/domacc/blob/main/macc/VERSION)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-MACC-blue)](https://claude.ai/code)

```bash
curl -sSL https://raw.githubusercontent.com/DoCoreTeam/domacc/main/macc/install.sh | bash
```

```bash
/ceo Build a SaaS app with auth, payments, and a dashboard
```

That's it. A CEO agent assembles 16 specialists, asks 12 sharp questions, then ships code that passes 5 mandatory gates.

---

## Why MACC

**Other AI tools start coding the second you press Enter.** MACC refuses to write a single line until it understands the problem. Then it deploys planners, builders, and evaluators in parallel — and blocks anything that fails review.

- **Up to 12 questions before code.** No guessing. No wasted sprints.
- **16 specialists. One command.** Business, research, OSS scouting, full-stack, DevOps, mobile, integrations, docs, copy, SEO, QA, security, code review, token budget.
- **5 gates. Zero exceptions.** 300-line file limit, version pinning, role separation, criteria checks, breaking-change approval.
- **Builder ≠ Reviewer.** Always. No agent grades its own homework.
- **Self-improving.** Every mistake becomes a permanent GATE pattern.

---

## How It Works

```
/ceo "Build me a SaaS"
        │
        ▼
  Q&A  ── up to 12 questions, one at a time, adaptive
        │
        ▼
  PLAN  ── DC-BIZ + DC-RES + DC-OSS  (parallel)
        │
        ▼
  BUILD ── DB · BE · FE · OPS · DOC  (parallel CORE)
           +MOB · INT · WRT · SEO    (added when needed)
        │
        ▼
  LOOP  ── implement → review+ripple → test  (max 3x)
        │
        ▼
  AUDIT ── DC-QA + DC-SEC + DC-REV   (simultaneous)
        │
        ▼
  GATES ── 1·2·3·4·5  ── all must pass
        │
        ▼
  SHIP  ── code + tests + docs + commit
```

---

## Commands

| Command | What it does |
|---------|--------------|
| `/ceo [task]` | Full pipeline — Q&A, plan, build, audit, ship |
| `/ceo-review` | Security + quality + PR review |
| `/ceo-test` | TDD + unit + E2E + browser QA |
| `/ceo-ship` | Gate → review → build → deploy |
| `/ceo-debug [bug]` | Investigate → fix → verify |
| `/ceo-ralph [task]` | Autonomous loop until completion criteria met |

Run `/ceo-status` anytime to see where you are. `/ceo-update` pulls the latest.

---

## The 16 Agents

| Phase | Agent | Role | Model |
|-------|-------|------|-------|
| **PLANNER** | DC-BIZ | Business Judge | Opus |
| | DC-RES | Researcher | Sonnet |
| | DC-OSS | Open Source Scout | Opus |
| **GENERATOR** | DC-DEV-DB | Database Engineer | Sonnet |
| | DC-DEV-BE | Backend Developer | Sonnet |
| | DC-DEV-FE | Frontend Developer | Sonnet |
| | DC-DEV-OPS | DevOps Engineer | Sonnet |
| | DC-DOC | Documentation Writer | Haiku |
| | DC-DEV-MOB | Mobile Developer | Sonnet |
| | DC-DEV-INT | Integration Engineer | Sonnet |
| | DC-WRT | Copywriter | Haiku |
| | DC-SEO | SEO / AEO / GEO | Haiku |
| **EVALUATOR** | DC-QA | QA Engineer | Sonnet |
| | DC-SEC | Security Reviewer | Opus |
| | DC-REV | Code Reviewer | Opus |
| **SUPPORT** | DC-TOK | Token Optimizer | Haiku |

CORE specialists run every sprint. EXTENDED specialists are added only when the task actually needs them.

---

## The 5 Gates

Every output must pass all five. No exceptions.

| Gate | Check |
|------|-------|
| **1** | Error-registry scan + 300-line file limit (auto-blocked) |
| **2** | All completion criteria verified |
| **3** | Version tag matches `macc/VERSION` |
| **4** | Builder ≠ Reviewer (enforced) |
| **5** | Breaking changes blocked without explicit approval |

---

## Coding Standards

Non-negotiable. Enforced by Gate 1 on every file.

- 300 lines max per file · 50 lines max per function · 4 levels max nesting
- Immutability — always create, never mutate
- Explicit error handling at every level
- Input validation at every boundary
- Tests required for every feature
- Row-Level Security on every table

---

## Requirements

| | |
|---|---|
| [Claude Code](https://claude.ai/code) | Required |
| Anthropic API key | Opus + Sonnet + Haiku access |
| `git` | For installer |

---

## Install · Update

```bash
# First time, or to update
curl -sSL https://raw.githubusercontent.com/DoCoreTeam/domacc/main/macc/install.sh | bash

# From inside Claude Code
/ceo-update
```

Re-running the installer always pulls the latest. Your registries (errors, instincts, history) are preserved.

---

## License

MIT — see [LICENSE](LICENSE).

---

*Built with **MACC**.*
