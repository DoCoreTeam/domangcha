<div align="center"><pre>
██████╗  ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗ ██████╗  ██████╗ ██╗  ██╗ █████╗ 
██╔══██╗██╔═══██╗████╗ ████║██╔══██╗████╗  ██║██╔════╝ ██╔════╝ ██║  ██║██╔══██╗
██║  ██║██║   ██║██╔████╔██║███████║██╔██╗ ██║██║  ███╗██║      ███████║███████║
██║  ██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║   ██║██║      ██╔══██║██╔══██║
██████╔╝╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║╚██████╔╝╚██████╗ ██║  ██║██║  ██║
╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝
</pre></div>

<div align="center">

### 🚗💨 DOMANGCHA — *Your AI getaway car from development hell.*

**17 AI specialists. One command. From requirements to shipped code.**

[![Version](https://img.shields.io/badge/version-2.0.36-brightgreen?style=for-the-badge&logo=github)](https://github.com/DoCoreTeam/domangcha/blob/main/domangcha/VERSION)
[![npm](https://img.shields.io/npm/v/domangcha?style=for-the-badge&logo=npm&color=CB3837)](https://www.npmjs.com/package/domangcha)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Required-5865F2?style=for-the-badge)](https://claude.ai/code)
[![Agents](https://img.shields.io/badge/Agents-17-FF6B6B?style=for-the-badge)](https://github.com/DoCoreTeam/domangcha#the-16-agents)
[![Gates](https://img.shields.io/badge/Gates-5-orange?style=for-the-badge)](https://github.com/DoCoreTeam/domangcha#the-5-gates)

<br/>

> **I typed one command and got back auth, payments, and a dashboard — tested, reviewed, security-audited. I went to get coffee.**
>
> *— Michael Dohyeon Kim, KDC CEO · builder of DOMANGCHA*

```bash
# Install (30 seconds)
npx domangcha
```

```bash
# Then, inside Claude Code:
/ceo "Build a Stripe invoicing tool for freelancers — invoices, email, paid/overdue dashboard"
```

</div>

---

## ⚡ Why DOMANGCHA?

DOMANGCHA is a **multi-agent system** that brings workflow automation to Claude Code. Unlike traditional developer tools, it orchestrates 17 specialized AI agents in parallel, delivering end-to-end project delivery with zero context-switching.

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
└── "Hold on — I have questions"
    └── 12 sharp questions
        └── Risk check → 17 specialists
            → 5 gates → ship
```

</td>
</tr>
</table>

| | DOMANGCHA | Typical AI tool |
|---|:---:|:---:|
| Requirements before code | ✅ Up to 12 questions | ❌ Codes immediately |
| Tradeoff check before building | ✅ Catches risks upfront | ❌ None |
| Role separation by specialist | ✅ 17 agents, parallel | ❌ Single model |
| Builder ≠ Reviewer (enforced) | ✅ Always | ❌ None |
| Breaking-change protection | ✅ Gate 5 blocks | ❌ None |
| Mistakes → permanent patterns | ✅ error-registry | ❌ None |
| Rule memory auto-sync on update | ✅ v2.0.33 | ❌ None |

---

## 🎬 Watch a Real Sprint

> `/ceo "Build a Stripe-powered invoicing tool for freelancers — create invoices, send via email, track paid/overdue"`

```
[INTENT PARSED]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Input:   Build a Stripe-powered invoicing tool for freelancers —
         create invoices, send via email, track paid/overdue
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Parsed:  Freelancer creates an invoice for a client, emails it with a
         Stripe payment link, tracks real-time payment status
         (draft → sent → paid/overdue) in a dashboard
Goal:    Invoice create → email send → Stripe pay → dashboard auto-update (3 flows)
Scope:   IN  — invoice CRUD, Stripe Payment Links, email via Resend, webhook status sync
         OUT — tax calculation, multi-currency, accounting software sync, PDF export
Context: Web app / greenfield / Stripe confirmed / stack TBD → Q&A needed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[CEO SIZE ASSESSMENT]
Task:   Freelancer invoicing tool (Stripe + email + status dashboard)
Rating: MEDIUM  →  FULL PIPELINE

[TRADEOFF CHECK] ✅ CLEAR — No architectural risks detected. Proceeding to Q&A.

[CEO] Q1: What's your stack? (Next.js / Express / other?)
> Next.js 14 + Supabase

[CEO] Q2: Should freelancers manage multiple clients, each with their own invoice history?
> Yes — each client has a profile, invoices are linked to a client

[CEO] Q3: When a client pays via Stripe, should the invoice status update automatically (webhook)?
> Yes, paid status should flip in real time — no manual refresh

[CEO] Q4: What does "done" look like? Which flows need to work end-to-end in the browser?
> ① Create invoice → send to client email  ② Client clicks link → pays via Stripe
> ③ Dashboard shows "Paid" automatically. All 3 in Stripe test mode.

[CEO] Q5: Auth for the freelancer — GitHub OAuth, email/password, or something else?
> GitHub OAuth — quickest to set up

[Q&A COMPLETE] ✅  Stack / data model / Stripe webhook / done criteria / auth confirmed

[TASK REFINED]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Original Input:  Stripe-powered invoicing tool for freelancers
Q&A Summary:     Next.js 14 + Supabase / clients table per user /
                 Stripe Payment Links + webhook / Resend email / GitHub OAuth /
                 3 E2E flows in Stripe test mode
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Final Task:   Next.js 14 + Supabase + Stripe + Resend.
              GitHub OAuth login, RLS on all tables.
              clients + invoices + stripe_events tables.
              CRUD invoices → generate Stripe Payment Link →
              send email via Resend → webhook flips status to "paid".
Done When:    ① Freelancer creates invoice → client receives email with pay link
              ② Client pays via Stripe (test mode) → webhook fires
              ③ Dashboard shows invoice status "Paid" without page refresh
Out of Scope: Tax calculation, multi-currency, PDF export, accounting integrations
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[DOC-FIRST] Creating docs/2026-05-01-v2.0.33/
  ✔ 00-requirements.md       (invoice lifecycle + Stripe webhook + Resend SLA)
  ✔ 01-architecture.md       (GitHub OAuth → Supabase RLS + Stripe webhook flow)
  ✔ 02-task-breakdown.md     P0: Auth+RLS+Stripe  P1: Invoice CRUD+email  P2: Dashboard UI
  ✔ 03-test-strategy.md      (Stripe test mode E2E + webhook signature security test)
  ✔ 04-completion-criteria.md  (3-flow checklist + rollback criteria)
[DOC COMPLETE]

━━━━━━━━━━━━━━━ PHASE 1: PLANNER ━━━━━━━━━━━━━━━
DC-BIZ  ✔  Freelancer invoicing is a proven pain point. Stripe + email is the right wedge. Build.
DC-RES  ✔  Stripe Payment Links beat custom checkout for v1 speed. Resend > SendGrid for DX.
DC-OSS  ✔  stripe-node (39k★), resend (5k★), @supabase/ssr. All stable, actively maintained.

━━━━━━━━━━━━━━━ PHASE 2: BUILDER ━━━━━━━━━━━━━━━
DC-DEV-DB   ✔  users · clients · invoices · stripe_events tables + RLS — 4 migrations
DC-DEV-BE   ✔  /api/invoices (CRUD) · /api/stripe/webhook · /api/send-invoice (Resend)
DC-DEV-FE   ✔  InvoiceForm · ClientList · StatusBadge · Dashboard · SendButton — 6 components
DC-DEV-OPS  ✔  .env.example (STRIPE_SECRET · STRIPE_WEBHOOK_SECRET · RESEND_API_KEY) · Vercel

━━━━━━━━━━━━━━━ PHASE 3: EVALUATOR ━━━━━━━━━━━━━
DC-QA   ✔  22 unit tests · 3 E2E flows (create→send→paid) · Stripe test mode all green
DC-SEC  ✔  Stripe webhook signature verified · RLS all tables · 0 vulnerabilities
DC-REV  ✔  Code approved · no logic duplication · types sound

━━━━━━━━━━━━━━━━━━ GATE 1–5 ━━━━━━━━━━━━━━━━━━━
① Scan       ✅  0 error-registry hits · all files ≤ 300 lines
② Criteria   ✅  3 E2E flows passing in Stripe test mode
③ Version    ✅  v2.0.33 consistent across all files
④ Separation ✅  Builder ≠ Reviewer confirmed
⑤ Breaking   ✅  Greenfield — no breaking changes

[CEO REPORT] ✅ Done in 31 minutes.
  Files: 18 new  ·  Tests: 22 passing  ·  Security: Stripe sig + RLS  ·  Deploy: Vercel ready
```

**A complete invoicing tool with real Stripe payments. You didn't write a line.**

---

## 🔄 Pipeline

```
/ceo "Build a Stripe invoicing tool for freelancers"
           │
           ▼
    ┌─────────────────┐
    │  INTENT PARSE   │  Every input → structured [INTENT PARSED] block
    └────────┬────────┘
             │  Input / Parsed / Goal / Scope / Context
             ▼
    ┌──────────────────┐
    │ TRADEOFF CHECK   │  CEO scans for risks before any code is written
    └────────┬─────────┘
             │  ✅ CLEAR → proceed   ⚠️ DETECTED → show risks + 4 options
             ▼
    ┌─────────────┐
    │  STACK SEL  │  CEO analyzes your task and recommends the best stack
    └──────┬──────┘
           │  [1] Standard    ████████ 80%  17 agents, full pipeline
           │  [2] Ralph Loop  ██████   60%  autonomous until done
           │  [3] gstack      ████     40%  web E2E + browser QA
           │  [4] Superpowers ██       25%  design-first, plan-heavy
           ▼
    ┌─────────────┐
    │    Q & A    │  Up to 12 questions — adaptive, one at a time
    └──────┬──────┘
           │  Stack? Done criteria? External APIs? Auth? Deploy target?
           ▼
    ┌──────────────────┐
    │  TASK SYNTHESIS  │  Q&A answers → structured [TASK REFINED] block
    └────────┬─────────┘
             │  Final task / Done criteria / Out-of-scope locked
             ▼
    ┌─────────────┐
    │  DOC-FIRST  │  ← IMMUTABLE RULE — all stacks, no exceptions
    └──────┬──────┘
           │  docs/YYYY-MM-DD-vX.X.X/
           │  ├── 00-requirements.md         functional + non-functional reqs
           │  ├── 01-architecture.md         system design, data flow
           │  ├── 02-task-breakdown.md       tasks + priority P0/P1/P2
           │  ├── 03-test-strategy.md        test strategy + security criteria
           │  └── 04-completion-criteria.md  done condition + exit + rollback
           │  ↳ Planner self-checks for gaps → asks user if needed → [DOC COMPLETE]
           ▼
    ┌─────────────┐
    │   PLANNER   │  DC-BIZ · DC-RES · DC-OSS  (parallel)
    └──────┬──────┘
           ▼
    ┌─────────────┐
    │   BUILDER   │  DB · BE · FE · OPS · DOC  (parallel CORE)
    └──────┬──────┘  + MOB · INT · WRT · SEO   (added on demand)
           │  implement → ripple analysis → review  (max 3 loops)
           ▼
    ┌─────────────┐
    │  EVALUATOR  │  DC-QA + DC-SEC + DC-REV   (simultaneous)
    └──────┬──────┘
           ▼
    ┌─────────────┐
    │  GATE 1–5   │  All must pass before ship
    └──────┬──────┘
           ▼
        🚀 SHIP
```

---

## 👥 The 17 Agents

<table>
<thead>
<tr><th>Phase</th><th>Agent</th><th>Role</th><th>Model</th></tr>
</thead>
<tbody>
<tr><td rowspan="4"><b>🧠 PLANNER</b></td>
  <td><code>DC-BIZ</code></td><td>Business Judge</td><td>Opus</td></tr>
<tr><td><code>DC-RES</code></td><td>Researcher</td><td>Sonnet</td></tr>
<tr><td><code>DC-OSS</code></td><td>OSS Scout</td><td>Opus</td></tr>
<tr><td><code>DC-ANA</code></td><td>Codebase Analyst</td><td>Sonnet</td></tr>
<tr><td rowspan="9"><b>🔨 BUILDER</b></td>
  <td><code>DC-DEV-DB</code></td><td>Database Engineer</td><td>Sonnet</td></tr>
<tr><td><code>DC-DEV-BE</code></td><td>Backend Developer</td><td>Sonnet</td></tr>
<tr><td><code>DC-DEV-FE</code></td><td>Frontend Developer</td><td>Sonnet</td></tr>
<tr><td><code>DC-DEV-OPS</code></td><td>DevOps Engineer</td><td>Sonnet</td></tr>
<tr><td><code>DC-DEV-MOB</code></td><td>Mobile Developer</td><td>Sonnet</td></tr>
<tr><td><code>DC-DEV-INT</code></td><td>Integration Engineer</td><td>Sonnet</td></tr>
<tr><td><code>DC-DOC</code></td><td>Documentation Writer</td><td>Haiku</td></tr>
<tr><td><code>DC-WRT</code></td><td>Copywriter</td><td>Haiku</td></tr>
<tr><td><code>DC-SEO</code></td><td>SEO / AEO / GEO</td><td>Haiku</td></tr>
<tr><td rowspan="3"><b>🔍 EVALUATOR</b></td>
  <td><code>DC-QA</code></td><td>QA Engineer</td><td>Sonnet</td></tr>
<tr><td><code>DC-SEC</code></td><td>Security Reviewer</td><td>Opus</td></tr>
<tr><td><code>DC-REV</code></td><td>Code Reviewer</td><td>Opus</td></tr>
<tr><td><b>⚙️ SUPPORT</b></td>
  <td><code>DC-TOK</code></td><td>Token Optimizer</td><td>Haiku</td></tr>
</tbody>
</table>

> **CORE** (runs every sprint) — BIZ, RES, OSS, DB, BE, FE, OPS, QA, SEC, REV, DOC, TOK  
> **EXTENDED** (added on demand) — MOB, INT, WRT, SEO

---

## 🛡️ The 5 Gates

> Every output must pass **all five**. No exceptions.

| Gate | Check |
|:---:|---|
| **① SCAN** | error-registry pattern scan + **300-line file limit (auto-blocked)** |
| **② CRITERIA** | All completion criteria verified 100% |
| **③ VERSION** | Version tag matches `domangcha/VERSION` |
| **④ SEPARATION** | Builder ≠ Reviewer — always enforced |
| **⑤ BREAKING** | Breaking changes blocked without **explicit user approval** |

---

## 🆕 What's New

| Version | Feature |
|---|---|
| **v2.0.36** | **npx-first updates** — `/ceo-update` and `/ceo-version` now use `npx domangcha` as primary, `curl \| bash` as fallback. Fixes stale bin version + `curl -fsSL` safety flag. |
| **v2.0.35** | **DC-ANA (17th Agent)** — DOMANGCHA's internal codebase analyst. Absorbs all ECC code-explorer capabilities. Auto-triggered for gap analysis, refactoring, and LARGE/HEAVY tasks. `code-explorer` (ECC) calls now banned. |
| **v2.0.34** | **FAST PATH Lightweight DOC** — Every task, even small fixes, generates a `00-summary.md`. No more undocumented changes. |
| **v2.0.33** | **Memory Sync** — rule memories auto-refresh on every `npx domangcha` update. User feedback and project context are never overwritten. |
| **v2.0.31** | **Tradeoff Check** — CEO surfaces architectural risks and side effects before any Q&A or implementation begins. |
| **v2.0.30** | Agent color-coding system — visual group identification across all pipeline output. |

---

## 🔄 Updates

**How updates work:**

Files are installed to `~/.claude/` on first run. They do **not** auto-update while a project is in progress — the version at install time is what runs.

**To update:** re-run `npx domangcha`. Your error registry and project registries are preserved. Rule memories in `~/.claude/projects/*/memory/` are automatically refreshed with the latest version's rule definitions — user feedback and project context are never overwritten.

**Auto-update prompt (built-in):** Every `/ceo` call silently checks the npm registry for a newer version. If one exists, you'll see:

```
[CEO] New version v2.0.33 available (installed: v2.0.31).
Update before continuing? (y/n):
```

- `y` → runs `npx domangcha`, updates in-place, then continues with your task
- `n` / Enter → skips and continues without updating

Version check failures (offline, etc.) are silently ignored — your task is never blocked.

---

## 🖥️ Commands

Every command triggers the multi-agent system to orchestrate tasks across planning, building, quality, and deployment phases.

| Command | What it does |
|---|---|
| `/ceo "[task]"` | 🚀 Full pipeline — version check → Q&A → 17 agents → GATE → ship |
| `/ceo-ralph "[task]"` | 🔁 Autonomous loop until completion criteria met |
| `/ceo-init` | 🔧 Project harness setup |
| `/ceo-debug "[bug]"` | 🐛 Investigate → fix → verify |
| `/ceo-review` | 🔍 Security + quality + PR review |
| `/ceo-test` | ✅ TDD + unit + E2E + browser QA |
| `/ceo-ship` | 📦 Gate → review → build → deploy |
| `/ceo-status` | 📊 Show current status |

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

DOMANGCHA is a developer tool built for Claude Code users who want AI-driven automation and multi-agent coordination without manual orchestration.

| | |
|---|---|
| [Claude Code](https://claude.ai/code) | Required |
| Anthropic API Key | Opus + Sonnet + Haiku access |
| `git` | For installer |

---

## 🚀 Install · Update

**Option 1 — npx (recommended)**
```bash
npx domangcha
```

**Option 2 — curl**
```bash
curl -sSL https://raw.githubusercontent.com/DoCoreTeam/domangcha/main/domangcha/install.sh | bash
```

**Option 3 — global install**
```bash
npm install -g domangcha && domangcha
```

Re-running always pulls the latest. Your registries (errors, instincts, history) are preserved.

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

### 🚗💨 돔황차 — *개발 지옥에서 도망쳐*

**17명 AI 전문가. 명령 하나. 요구사항부터 배포까지.**

[![Version](https://img.shields.io/badge/version-2.0.36-brightgreen?style=for-the-badge&logo=github)](https://github.com/DoCoreTeam/domangcha/blob/main/domangcha/VERSION)
[![npm](https://img.shields.io/npm/v/domangcha?style=for-the-badge&logo=npm&color=CB3837)](https://www.npmjs.com/package/domangcha)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-필수-5865F2?style=for-the-badge)](https://claude.ai/code)
[![Agents](https://img.shields.io/badge/에이전트-17명-FF6B6B?style=for-the-badge)](https://github.com/DoCoreTeam/domangcha)
[![Gates](https://img.shields.io/badge/게이트-5개-orange?style=for-the-badge)](https://github.com/DoCoreTeam/domangcha)

> **명령 하나 쳤더니 인증, 결제, 대시보드가 돌아왔다. 테스트 통과, 보안 감사 완료, 코드 리뷰까지.**
>
> *— Michael Dohyeon Kim, KDC CEO · DOMANGCHA 제작자*

```bash
# 방법 1 — npx (권장)
npx domangcha

# 방법 2 — curl
curl -sSL https://raw.githubusercontent.com/DoCoreTeam/domangcha/main/domangcha/install.sh | bash
```

```bash
/ceo "프리랜서용 Stripe 인보이스 툴 만들어줘 — 인보이스 생성, 이메일 발송, 미납/완납 대시보드"
```

---

### ⚡ 왜 DOMANGCHA인가?

DOMANGCHA는 Claude Code를 위한 **다중 에이전트 시스템**입니다. 17명의 전문화된 AI 에이전트를 병렬로 조율하여 문맥 전환 없이 엔드-투-엔드 프로젝트를 완성합니다.

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
└── "잠깐, 질문이 있어요"
    └── 12개 핵심 질문
        └── 리스크 체크 → 17명 전문가
            → 5 게이트 → 출시
```

</td>
</tr>
</table>

| | DOMANGCHA | 일반 AI 도구 |
|---|:---:|:---:|
| 코드 전 요구사항 분석 | ✅ 최대 12개 질문 | ❌ 바로 코딩 |
| 구현 전 트레이드오프 체크 | ✅ 리스크 사전 발굴 | ❌ 없음 |
| 전문가 역할 분리 | ✅ 17명 병렬 운영 | ❌ 단일 모델 |
| 빌더 ≠ 리뷰어 강제 | ✅ 항상 분리 | ❌ 없음 |
| 파괴적 변경 보호 | ✅ Gate 5 차단 | ❌ 없음 |
| 실수 → 영구 패턴 등록 | ✅ error-registry | ❌ 없음 |
| 업데이트 시 규칙 메모리 자동 갱신 | ✅ v2.0.33 | ❌ 없음 |

---

### 🆕 최신 업데이트

| 버전 | 기능 |
|---|---|
| **v2.0.36** | **npx 우선 업데이트** — `/ceo-update`, `/ceo-version`이 `npx domangcha`를 1순위, `curl \| bash`를 fallback으로 사용. bin 버전 싱크 + `curl -fsSL` 보안 플래그 통일. |
| **v2.0.35** | **DC-ANA (17번째 에이전트)** — DOMANGCHA 전용 내부 코드베이스 분석가. ECC code-explorer 기능 완전 흡수. 갭분석·리팩터링·LARGE/HEAVY 업무 시 자동 소환. `code-explorer`(ECC) 직접 호출 금지. |
| **v2.0.34** | **FAST PATH 경량 DOC** — 소규모 수정도 `00-summary.md` 자동 생성. 문서 없는 변경 원천 차단. |
| **v2.0.33** | **메모리 자동 동기화** — `npx domangcha` 업데이트 시 규칙 메모리 자동 갱신. 사용자 피드백/프로젝트 컨텍스트는 절대 덮어쓰지 않음. |
| **v2.0.31** | **트레이드오프 체크** — Q&A 및 구현 시작 전 CEO가 아키텍처 리스크와 부작용을 사전에 표면화. |
| **v2.0.30** | 에이전트 컬러 코딩 시스템 — 파이프라인 출력 전체에서 그룹 시각적 식별. |

---

### 🔄 파이프라인

```
/ceo "프리랜서용 Stripe 인보이스 툴 만들어줘"
           │
           ▼
    ┌───────────────────┐
    │  인텐트 파싱      │  모든 입력 → 구조화된 [INTENT PARSED] 블록 출력
    └────────┬──────────┘
             │  원본 / 정제 / 목표 / 범위 / 전제
             ▼
    ┌──────────────────┐
    │  트레이드오프 체크│  CEO가 구현 전 리스크를 스캔
    └────────┬─────────┘
             │  ✅ 이상 없음 → 진행   ⚠️ 위험 감지 → 리스크 + 4가지 선택지 제시
             ▼
    ┌─────────────┐
    │  스택 선택  │  CEO가 업무 분석 후 최적 스택 추천
    └──────┬──────┘
           │  [1] 스탠다드    ████████ 80%  17명 풀 파이프라인 (기본)
           │  [2] 랄프루프    ██████   60%  완료 기준 정의 후 자율 반복
           │  [3] gstack     ████     40%  웹 E2E + 브라우저 QA 강화
           │  [4] 슈퍼파워   ██       25%  설계 중심, 계획 먼저
           ▼
    ┌─────────────┐
    │    Q & A    │  최대 12개 질문 (한 번에 하나씩, 적응형)
    └──────┬──────┘
           │  스택? 완료 기준? 외부 API? 인증? 배포?
           ▼
    ┌──────────────────┐
    │  태스크 정제      │  Q&A 답변 → 구조화된 [TASK REFINED] 블록 출력
    └────────┬─────────┘
             │  최종 태스크 / 완료 조건 / 제외 범위 확정
             ▼
    ┌─────────────┐
    │  문서 먼저  │  ← 절대 불변 — 어떤 스택이든, 예외 없음
    └──────┬──────┘
           │  docs/YYYY-MM-DD-vX.X.X/
           │  ├── 00-requirements.md        기능/비기능 요구사항
           │  ├── 01-architecture.md        시스템 설계, 데이터 흐름
           │  ├── 02-task-breakdown.md      태스크 목록 + 우선순위(P0/P1/P2)
           │  ├── 03-test-strategy.md       테스트 전략 + 보안/보완 기준
           │  └── 04-completion-criteria.md 완료 조건 · 종료 기준 · 롤백 기준
           │  ↳ 기획자 자가점검 → 갭 발견 시 추가 질문 → [DOC COMPLETE]
           ▼
    ┌─────────────┐
    │    기  획   │  DC-BIZ · DC-RES · DC-OSS  (병렬)
    └──────┬──────┘
           ▼
    ┌─────────────┐
    │    빌  드   │  DB · BE · FE · OPS · DOC  (병렬 CORE)
    └──────┬──────┘  + 모바일 · 연동 · 카피 · SEO  (필요 시 추가)
           │  구현 → 파급 분석 → 리뷰  (최대 3회 반복)
           ▼
    ┌─────────────┐
    │    평  가   │  DC-QA + DC-SEC + DC-REV   (동시 진행)
    └──────┬──────┘
           ▼
    ┌─────────────┐
    │  게이트 1-5 │  전부 통과해야 출시
    └──────┬──────┘
           ▼
        🚀 출시
```

---

### 👥 17명의 에이전트

<table>
<thead>
<tr><th>단계</th><th>에이전트</th><th>역할</th><th>모델</th></tr>
</thead>
<tbody>
<tr><td rowspan="4"><b>🧠 기획자</b></td>
  <td><code>DC-BIZ</code></td><td>사업 타당성 판단</td><td>Opus</td></tr>
<tr><td><code>DC-RES</code></td><td>기술 리서치</td><td>Sonnet</td></tr>
<tr><td><code>DC-OSS</code></td><td>오픈소스 도구 탐색</td><td>Opus</td></tr>
<tr><td><code>DC-ANA</code></td><td>코드베이스 분석가</td><td>Sonnet</td></tr>
<tr><td rowspan="9"><b>🔨 빌더</b></td>
  <td><code>DC-DEV-DB</code></td><td>데이터베이스 엔지니어</td><td>Sonnet</td></tr>
<tr><td><code>DC-DEV-BE</code></td><td>백엔드 개발자</td><td>Sonnet</td></tr>
<tr><td><code>DC-DEV-FE</code></td><td>프론트엔드 개발자</td><td>Sonnet</td></tr>
<tr><td><code>DC-DEV-OPS</code></td><td>DevOps 엔지니어</td><td>Sonnet</td></tr>
<tr><td><code>DC-DEV-MOB</code></td><td>모바일 개발자</td><td>Sonnet</td></tr>
<tr><td><code>DC-DEV-INT</code></td><td>통합(Integration) 엔지니어</td><td>Sonnet</td></tr>
<tr><td><code>DC-DOC</code></td><td>문서 작성자</td><td>Haiku</td></tr>
<tr><td><code>DC-WRT</code></td><td>카피라이터</td><td>Haiku</td></tr>
<tr><td><code>DC-SEO</code></td><td>SEO / AEO / GEO</td><td>Haiku</td></tr>
<tr><td rowspan="3"><b>🔍 평가자</b></td>
  <td><code>DC-QA</code></td><td>QA 엔지니어</td><td>Sonnet</td></tr>
<tr><td><code>DC-SEC</code></td><td>보안 리뷰어</td><td>Opus</td></tr>
<tr><td><code>DC-REV</code></td><td>코드 리뷰어</td><td>Opus</td></tr>
<tr><td><b>⚙️ 지원</b></td>
  <td><code>DC-TOK</code></td><td>토큰 예산 관리</td><td>Haiku</td></tr>
</tbody>
</table>

> **CORE** (매 스프린트 가동) — BIZ, RES, OSS, DB, BE, FE, OPS, QA, SEC, REV, DOC, TOK  
> **EXTENDED** (필요 시 추가) — MOB, INT, WRT, SEO

---

### 🛡️ 5개의 게이트

> 모든 산출물은 **다섯 개를 전부** 통과해야 합니다. 예외 없음.

| 게이트 | 검증 항목 |
|:---:|---|
| **① 스캔** | error-registry 패턴 스캔 + **300줄 초과 파일 자동 차단** |
| **② 기준** | 모든 완료 기준 충족 100% 검증 |
| **③ 버전** | 버전 태그 = `domangcha/VERSION` 일치 확인 |
| **④ 분리** | 빌더 ≠ 리뷰어 — 항상 강제 |
| **⑤ 파괴** | 파괴적 변경 → **사용자 명시 승인 없으면 차단** |

---

### 🖥️ 명령어

| 명령어 | 동작 |
|---|---|
| `/ceo "[업무]"` | 🚀 전체 파이프라인 — Q&A → 17명 → GATE → 출시 |
| `/ceo-ralph "[업무]"` | 🔁 완료 기준 충족까지 자율 반복 루프 |
| `/ceo-init` | 🔧 프로젝트 하네스 초기화 |
| `/ceo-debug "[버그]"` | 🐛 조사 → 수정 → 검증 |
| `/ceo-review` | 🔍 보안 + 품질 + PR 리뷰 |
| `/ceo-test` | ✅ TDD + 단위 + E2E + 브라우저 QA |
| `/ceo-ship` | 📦 게이트 → 리뷰 → 빌드 → 배포 |
| `/ceo-status` | 📊 현황 조회 |

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

| | |
|---|---|
| [Claude Code](https://claude.ai/code) | 필수 |
| Anthropic API 키 | Opus + Sonnet + Haiku 액세스 |
| `git` | 인스톨러용 |

---

### 🚀 설치 · 업데이트

**방법 1 — npx (권장)**
```bash
npx domangcha
```

**방법 2 — curl**
```bash
curl -sSL https://raw.githubusercontent.com/DoCoreTeam/domangcha/main/domangcha/install.sh | bash
```

**방법 3 — 전역 설치**
```bash
npm install -g domangcha && domangcha
```

인스톨러를 다시 실행하면 항상 최신 버전을 가져옵니다. 레지스트리(에러, 본능, 히스토리)는 보존됩니다. `~/.claude/projects/*/memory/`의 규칙 메모리는 최신 버전 정의로 자동 갱신되며, 사용자 피드백/프로젝트 컨텍스트는 절대 덮어쓰지 않습니다.

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
