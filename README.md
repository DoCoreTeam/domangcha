# DOMACC

### You just hired a 16-person engineering team.
### 16명의 엔지니어링 팀을 단 한 줄로 채용하세요.

[![Version](https://img.shields.io/badge/version-2.0.11-brightgreen.svg)](https://github.com/DoCoreTeam/domacc/blob/main/macc/VERSION)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-DOMACC-blue)](https://claude.ai/code)

```bash
curl -sSL https://raw.githubusercontent.com/DoCoreTeam/domacc/main/macc/install.sh | bash
```

```bash
/ceo Build a SaaS app with auth, payments, and a dashboard
```

That's it. A CEO agent assembles 16 specialists, asks 12 sharp questions, then ships code that passes 5 mandatory gates.

---

## Why DOMACC

**Other AI tools start coding the second you press Enter.** DOMACC refuses to write a single line until it understands the problem. Then it deploys planners, builders, and evaluators in parallel — and blocks anything that fails review.

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

*Built with **DOMACC** · by [docore](https://github.com/DoCoreTeam) (Michael Dohyeon Kim · KDC CEO)*

---

# 한국어

# DOMACC

### You just hired a 16-person engineering team.
### 16명의 엔지니어링 팀을 단 한 줄로 채용하세요.

[![Version](https://img.shields.io/badge/version-2.0.11-brightgreen.svg)](https://github.com/DoCoreTeam/domacc/blob/main/macc/VERSION)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-DOMACC-blue)](https://claude.ai/code)

```bash
curl -sSL https://raw.githubusercontent.com/DoCoreTeam/domacc/main/macc/install.sh | bash
```

```bash
/ceo Build a SaaS app with auth, payments, and a dashboard
```

이게 전부입니다. CEO 에이전트(Agent)가 16명의 전문가를 소집하고, 핵심을 꿰뚫는 12개의 질문을 던진 뒤, 5개의 필수 게이트(Gate)를 통과한 코드를 출시합니다.

---

## 왜 DOMACC인가

**다른 AI 도구는 엔터를 누르는 순간 코드부터 쏟아냅니다.** DOMACC는 문제를 완전히 이해하기 전까지 단 한 줄도 쓰지 않습니다. 그다음 플래너(Planner), 빌더(Builder), 평가자(Evaluator)를 병렬로 투입하고, 검토를 통과하지 못한 결과물은 모조리 막아냅니다.

- **코드 작성 전 최대 12개 질문.** 추측 없음. 헛된 스프린트 없음.
- **16명의 전문가, 단 하나의 명령.** 비즈니스, 리서치, OSS 스카우팅, 풀스택, DevOps, 모바일, 통합, 문서, 카피, SEO, QA, 보안, 코드 리뷰, 토큰 예산까지.
- **5개의 게이트(Gate). 예외는 없습니다.** 300줄 파일 제한, 버전 고정, 역할 분리, 기준 검증, 파괴적 변경 승인.
- **빌더(Builder) ≠ 리뷰어(Reviewer).** 언제나. 어떤 에이전트도 자기 숙제를 채점하지 않습니다.
- **자가 진화.** 모든 실수는 영구적인 게이트(Gate) 패턴이 됩니다.

---

## 작동 방식

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

## 명령어

| 명령어 | 동작 |
|---------|--------------|
| `/ceo [task]` | 전체 파이프라인(Pipeline) — Q&A, 플랜, 빌드, 감사, 출시 |
| `/ceo-review` | 보안 + 품질 + PR 리뷰 |
| `/ceo-test` | TDD + 단위 테스트 + E2E + 브라우저 QA |
| `/ceo-ship` | 게이트(Gate) → 리뷰 → 빌드 → 배포 |
| `/ceo-debug [bug]` | 조사 → 수정 → 검증 |
| `/ceo-ralph [task]` | 완료 기준 충족까지 자율 반복 루프 |

언제든지 `/ceo-status`를 실행해 현재 위치를 확인할 수 있습니다. `/ceo-update`는 최신 버전을 가져옵니다.

---

## 16명의 에이전트

| 단계 | 에이전트 | 역할 | 모델 |
|-------|-------|------|-------|
| **PLANNER** | DC-BIZ | 비즈니스 판단자(Business Judge) | Opus |
| | DC-RES | 리서처(Researcher) | Sonnet |
| | DC-OSS | 오픈소스 스카우트(Open Source Scout) | Opus |
| **GENERATOR** | DC-DEV-DB | 데이터베이스 엔지니어 | Sonnet |
| | DC-DEV-BE | 백엔드 개발자 | Sonnet |
| | DC-DEV-FE | 프론트엔드 개발자 | Sonnet |
| | DC-DEV-OPS | DevOps 엔지니어 | Sonnet |
| | DC-DOC | 문서 작성자 | Haiku |
| | DC-DEV-MOB | 모바일 개발자 | Sonnet |
| | DC-DEV-INT | 통합(Integration) 엔지니어 | Sonnet |
| | DC-WRT | 카피라이터 | Haiku |
| | DC-SEO | SEO / AEO / GEO | Haiku |
| **EVALUATOR** | DC-QA | QA 엔지니어 | Sonnet |
| | DC-SEC | 보안 리뷰어 | Opus |
| | DC-REV | 코드 리뷰어 | Opus |
| **SUPPORT** | DC-TOK | 토큰 최적화 담당 | Haiku |

CORE 전문가들은 모든 스프린트(Sprint)에서 가동됩니다. EXTENDED 전문가는 작업이 실제로 필요로 할 때만 합류합니다.

---

## 5개의 게이트(Gate)

모든 산출물은 다섯 개를 전부 통과해야 합니다. 예외는 없습니다.

| 게이트(Gate) | 검증 항목 |
|------|-------|
| **1** | 에러 레지스트리(error-registry) 스캔 + 300줄 파일 제한 (자동 차단) |
| **2** | 모든 완료 기준 충족 검증 |
| **3** | 버전 태그가 `macc/VERSION`과 일치 |
| **4** | 빌더(Builder) ≠ 리뷰어(Reviewer) 강제 |
| **5** | 명시적 승인 없는 파괴적 변경 차단 |

---

## 코딩 표준

타협 불가. 모든 파일에서 게이트(Gate) 1이 강제합니다.

- 파일당 최대 300줄 · 함수당 최대 50줄 · 중첩 최대 4단계
- 불변성(Immutability) — 항상 새로 만들고, 절대 변경하지 않기
- 모든 계층에서 명시적 에러 처리
- 모든 경계에서 입력 검증
- 모든 기능에 테스트 필수
- 모든 테이블에 RLS(Row-Level Security) 적용

---

## 요구사항

| | |
|---|---|
| [Claude Code](https://claude.ai/code) | 필수 |
| Anthropic API 키 | Opus + Sonnet + Haiku 액세스 |
| `git` | 인스톨러용 |

---

## 설치 · 업데이트

```bash
# First time, or to update
curl -sSL https://raw.githubusercontent.com/DoCoreTeam/domacc/main/macc/install.sh | bash

# From inside Claude Code
/ceo-update
```

인스톨러를 다시 실행하면 항상 최신 버전을 가져옵니다. 레지스트리(에러, 본능, 히스토리)는 그대로 보존됩니다.

---

## 라이선스

MIT — [LICENSE](LICENSE) 참조.

---

*Built with **DOMACC** · by [docore](https://github.com/DoCoreTeam) (Michael Dohyeon Kim · KDC CEO)*
