<div align="center"><pre>
██████╗  ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗ ██████╗ ██╗  ██╗ █████╗ 
██╔══██╗██╔═══██╗████╗ ████║██╔══██╗████╗  ██║██╔════╝ ██║  ██║██╔══██╗
██║  ██║██║   ██║██╔████╔██║███████║██╔██╗ ██║██║  ███╗███████║███████║
██║  ██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║   ██║██╔══██║██╔══██║
██████╔╝╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║╚██████╔╝██║  ██║██║  ██║
╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
</pre></div>

<div align="center">

### 🚗💨 DOMANGCHA — *Your AI getaway car from development hell.*

**AI Development Automation Tool**

[![Version](https://img.shields.io/badge/version-2.0.12-brightgreen?style=for-the-badge&logo=github)](https://github.com/DoCoreTeam/domangcha/blob/main/domangcha/VERSION)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Required-5865F2?style=for-the-badge)](https://claude.ai/code)
[![Agents](https://img.shields.io/badge/Agents-16-FF6B6B?style=for-the-badge)](https://github.com/DoCoreTeam/domangcha#the-16-agents)
[![Gates](https://img.shields.io/badge/Gates-5-orange?style=for-the-badge)](https://github.com/DoCoreTeam/domangcha#the-5-gates)

<br/>

> **You just hired a 16-person engineering team. With one command.**

```bash
curl -sSL https://raw.githubusercontent.com/DoCoreTeam/domangcha/main/domangcha/install.sh | bash
```

```bash
/ceo "Build a SaaS app with auth, payments, and a dashboard"
```

</div>

---

## ⚡ Why DOMANGCHA?

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
        └── 16 specialists → 5 gates → ship
```

</td>
</tr>
</table>

| | DOMANGCHA | Typical AI tool |
|---|:---:|:---:|
| Requirements before code | ✅ Up to 12 questions | ❌ Codes immediately |
| Role separation by specialist | ✅ 16 agents, parallel | ❌ Single model |
| Builder ≠ Reviewer (enforced) | ✅ Always | ❌ None |
| Breaking-change protection | ✅ Gate 5 blocks | ❌ None |
| Mistakes → permanent patterns | ✅ error-registry | ❌ None |

---

## 🔄 Pipeline

```
/ceo "Build me a SaaS"
           │
           ▼
    ┌─────────────┐
    │  STACK SEL  │  CEO analyzes your task and recommends the best stack
    └──────┬──────┘
           │  [1] Standard    ████████ 80%  16 agents, full pipeline
           │  [2] Ralph Loop  ██████   60%  autonomous until done
           │  [3] gstack      ████     40%  web E2E + browser QA
           │  [4] Superpowers ██       25%  design-first, plan-heavy
           ▼
    ┌─────────────┐
    │    Q & A    │  Up to 12 questions — adaptive, one at a time
    └──────┬──────┘
           │  Stack? Done criteria? External APIs? Auth? Deploy target?
           ▼
    ┌─────────────┐
    │  DOC-FIRST  │  ← IMMUTABLE RULE — all stacks, no exceptions
    └──────┬──────┘
           │  docs/YYYY-MM-DD-vX.X.X/
           │  ├── 00-requirements.md       functional + non-functional reqs
           │  ├── 01-architecture.md       system design, data flow
           │  ├── 02-task-breakdown.md     tasks + priority P0/P1/P2
           │  ├── 03-test-strategy.md      test strategy + security criteria
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

## 👥 The 16 Agents

<table>
<thead>
<tr><th>Phase</th><th>Agent</th><th>Role</th><th>Model</th></tr>
</thead>
<tbody>
<tr><td rowspan="3"><b>🧠 PLANNER</b></td>
  <td><code>DC-BIZ</code></td><td>Business Judge</td><td>Opus</td></tr>
<tr><td><code>DC-RES</code></td><td>Researcher</td><td>Sonnet</td></tr>
<tr><td><code>DC-OSS</code></td><td>OSS Scout</td><td>Opus</td></tr>
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

## 🖥️ Commands

| Command | What it does |
|---|---|
| `/ceo "[task]"` | 🚀 Full pipeline — Q&A → 16 agents → GATE → ship |
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

| | |
|---|---|
| [Claude Code](https://claude.ai/code) | Required |
| Anthropic API Key | Opus + Sonnet + Haiku access |
| `git` | For installer |

---

## 🚀 Install · Update

```bash
# Install or update
curl -sSL https://raw.githubusercontent.com/DoCoreTeam/domangcha/main/domangcha/install.sh | bash
```

```bash
# Update from inside Claude Code
/ceo-update
```

Re-running always pulls the latest. Your registries (errors, instincts, history) are preserved.

---

<details>
<summary><b>🇰🇷 한국어 (Korean) — 클릭하여 펼치기 / Click to expand</b></summary>

<br/>
<div align="center"><pre>
██████╗  ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗ ██████╗ ██╗  ██╗ █████╗ 
██╔══██╗██╔═══██╗████╗ ████║██╔══██╗████╗  ██║██╔════╝ ██║  ██║██╔══██╗
██║  ██║██║   ██║██╔████╔██║███████║██╔██╗ ██║██║  ███╗███████║███████║
██║  ██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║   ██║██╔══██║██╔══██║
██████╔╝╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║╚██████╔╝██║  ██║██║  ██║
╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
</pre></div>

### 🚗💨 돔황차 — *개발 지옥에서 도망쳐*

**AI 개발 자동화 도구**

[![Version](https://img.shields.io/badge/version-2.0.12-brightgreen?style=for-the-badge&logo=github)](https://github.com/DoCoreTeam/domangcha/blob/main/domangcha/VERSION)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-필수-5865F2?style=for-the-badge)](https://claude.ai/code)
[![Agents](https://img.shields.io/badge/에이전트-16명-FF6B6B?style=for-the-badge)](https://github.com/DoCoreTeam/domangcha)
[![Gates](https://img.shields.io/badge/게이트-5개-orange?style=for-the-badge)](https://github.com/DoCoreTeam/domangcha)

> **16명의 엔지니어링 팀을 단 한 줄로 채용하세요.**

```bash
curl -sSL https://raw.githubusercontent.com/DoCoreTeam/domangcha/main/domangcha/install.sh | bash
```

```bash
/ceo "인증, 결제, 대시보드가 있는 SaaS 앱 만들어줘"
```

---

### ⚡ 왜 DOMANGCHA인가?

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
        └── 16명 전문가 → 5 게이트 → 출시
```

</td>
</tr>
</table>

| | DOMANGCHA | 일반 AI 도구 |
|---|:---:|:---:|
| 코드 전 요구사항 분석 | ✅ 최대 12개 질문 | ❌ 바로 코딩 |
| 전문가 역할 분리 | ✅ 16명 병렬 운영 | ❌ 단일 모델 |
| 빌더 ≠ 리뷰어 강제 | ✅ 항상 분리 | ❌ 없음 |
| 파괴적 변경 보호 | ✅ Gate 5 차단 | ❌ 없음 |
| 실수 → 영구 패턴 등록 | ✅ error-registry | ❌ 없음 |

---

### 🔄 파이프라인

```
/ceo "SaaS 만들어줘"
           │
           ▼
    ┌─────────────┐
    │  스택 선택  │  CEO가 업무 분석 후 최적 스택 추천
    └──────┬──────┘
           │  [1] 스탠다드    ████████ 80%  16명 풀 파이프라인 (기본)
           │  [2] 랄프루프    ██████   60%  완료 기준 정의 후 자율 반복
           │  [3] gstack     ████     40%  웹 E2E + 브라우저 QA 강화
           │  [4] 슈퍼파워   ██       25%  설계 중심, 계획 먼저
           ▼
    ┌─────────────┐
    │    Q & A    │  최대 12개 질문 (한 번에 하나씩, 적응형)
    └──────┬──────┘
           │  스택? 완료 기준? 외부 API? 인증? 배포?
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

### 👥 16명의 에이전트

<table>
<thead>
<tr><th>단계</th><th>에이전트</th><th>역할</th><th>모델</th></tr>
</thead>
<tbody>
<tr><td rowspan="3"><b>🧠 기획자</b></td>
  <td><code>DC-BIZ</code></td><td>사업 타당성 판단</td><td>Opus</td></tr>
<tr><td><code>DC-RES</code></td><td>기술 리서치</td><td>Sonnet</td></tr>
<tr><td><code>DC-OSS</code></td><td>오픈소스 도구 탐색</td><td>Opus</td></tr>
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
| `/ceo "[업무]"` | 🚀 전체 파이프라인 — Q&A → 16명 → GATE → 출시 |
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

```bash
# 설치 또는 업데이트
curl -sSL https://raw.githubusercontent.com/DoCoreTeam/domangcha/main/domangcha/install.sh | bash
```

```bash
# Claude Code 내에서 업데이트
/ceo-update
```

인스톨러를 다시 실행하면 항상 최신 버전을 가져옵니다. 레지스트리(에러, 본능, 히스토리)는 보존됩니다.

</details>

---

<div align="center">

**Escape development hell. 🚗💨 DOMANGCHA is your getaway car.**

[![GitHub](https://img.shields.io/badge/GitHub-DoCoreTeam-181717?style=for-the-badge&logo=github)](https://github.com/DoCoreTeam/domangcha)
[![Made by](https://img.shields.io/badge/Made%20by-docore-FF6B6B?style=for-the-badge)](https://github.com/DoCoreTeam)

*Built with **DOMANGCHA** · by [docore](https://github.com/DoCoreTeam) (Michael Dohyeon Kim · KDC CEO)*

MIT License

</div>
