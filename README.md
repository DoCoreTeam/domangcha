# DOCORE ADK — Agent Development Kit for Claude Code

> 16 AI Agents. One command. Full development pipeline.
>
> 16개 AI 에이전트. 명령 하나. 완전한 개발 파이프라인.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-ADK-blue)](https://claude.ai/code)

---

## What is DOCORE? / DOCORE란?

**EN** — DOCORE is an **Agent Development Kit (ADK)** for [Claude Code](https://claude.ai/code) that turns Claude into a **CEO orchestrator** managing 16 specialized AI agents — from business planning to deployment.

**KO** — DOCORE는 [Claude Code](https://claude.ai/code)용 **에이전트 개발 키트(ADK)**입니다. Claude를 **CEO 오케스트레이터**로 전환하여 기획부터 배포까지 16개의 전문 AI 에이전트를 관리합니다.

One command triggers the full pipeline / 명령 하나로 전체 파이프라인이 실행됩니다:

```bash
/ceo "Build a SaaS todo app with authentication and payments"
/ceo "인증과 결제 기능이 있는 SaaS 투두앱 만들어줘"
```

---

## Quick Install / 빠른 설치

```bash
curl -sSL https://raw.githubusercontent.com/DoCoreTeam/docore/main/docore/install.sh | bash
```

**EN** — Then open any project in Claude Code and run `/ceo-init`.

**KO** — 설치 후 Claude Code에서 아무 프로젝트나 열고 `/ceo-init`을 실행하세요.

---

## How It Works / 작동 방식

```
/ceo "task"
     │
     ▼
① PLANNER ──── DC-BIZ (business / 사업판단) + DC-RES (research / 리서치) + DC-OSS (libraries / 라이브러리)
     │            → PLAN.md
     ▼
② GENERATOR ── DC-DEV-FE + DC-DEV-BE + DC-DEV-DB + DC-DEV-MOB
     │          DC-DEV-OPS + DC-DEV-INT + DC-WRT + DC-DOC + DC-SEO
     │            → parallel development / 병렬 개발
     ▼
③ EVALUATOR ── DC-QA (tests / 테스트) + DC-SEC (security / 보안) + DC-REV (review / 리뷰)
     │            → FAIL: retry ② max 3x / 실패 시 ②로 재작업 최대 3회
     ▼
④ GATE 1-5 ── pattern scan + completion + version tag + role separation + diff check
     │         금지패턴 + 완료조건 + 버전태그 + 역할분리 + 변경감지
     ▼
⑤ REPORT ──── code + tests + docs + git commit v0.x.0
              코드 + 테스트 + 문서 + 커밋
```

---

## 16 Agents / 16개 에이전트

| Phase / 단계 | Agent | Role (EN) | 역할 (KO) | Model |
|------|-------|-----------|-----------|-------|
| PLANNER | DC-BIZ | Business Judge | 사업 타당성 판단 | Opus |
| PLANNER | DC-RES | Researcher | 리서치 | Haiku |
| PLANNER | DC-OSS | Open Source Scout | 오픈소스 탐색 | Opus |
| GENERATOR | DC-DEV-FE | Frontend Developer | 프론트엔드 개발 | Sonnet |
| GENERATOR | DC-DEV-BE | Backend Developer | 백엔드 개발 | Sonnet |
| GENERATOR | DC-DEV-DB | Database Engineer | 데이터베이스 설계 | Sonnet |
| GENERATOR | DC-DEV-MOB | Mobile Developer | 모바일 개발 | Sonnet |
| GENERATOR | DC-DEV-OPS | DevOps Engineer | DevOps / 인프라 | Sonnet |
| GENERATOR | DC-DEV-INT | Integration Engineer | 외부 API 연동 | Sonnet |
| GENERATOR | DC-WRT | Writer / Copywriter | 카피라이팅 | Sonnet |
| GENERATOR | DC-DOC | Documentation Writer | 문서 작성 | Haiku |
| GENERATOR | DC-SEO | SEO / AEO / GEO Specialist | SEO 최적화 | Haiku |
| EVALUATOR | DC-QA | QA Engineer | 품질 검증 | Haiku |
| EVALUATOR | DC-SEC | Security Reviewer | 보안 검토 | Opus |
| EVALUATOR | DC-REV | Code Reviewer | 코드 리뷰 | Opus |
| SUPPORT | DC-TOK | Token Optimizer | 토큰 비용 최적화 | Haiku |

---

## Commands / 명령어

| Command | EN | KO |
|---------|----|----|
| `/ceo "task"` | Run full pipeline with all 16 agents | 16개 에이전트 전체 파이프라인 실행 |
| `/ceo-init` | Initialize project (registries + harness) | 프로젝트 초기 셋업 (레지스트리 + 하네스) |
| `/ceo-status` | Show current project status | 현재 프로젝트 상태 조회 |

---

## Quality Gates / 품질 게이트

**EN** — Every output passes 5 gates before delivery.

**KO** — 모든 산출물은 5개 게이트를 통과한 후 사용자에게 전달됩니다.

| Gate | Check (EN) | 검사 항목 (KO) |
|------|------------|---------------|
| GATE 1 | Error registry pattern scan | 알려진 오류 패턴 차단 |
| GATE 2 | Completion criteria verification | 완료 조건 충족 여부 |
| GATE 3 | Version tag `v0.0.0` present | 버전 태그 존재 여부 |
| GATE 4 | Builder ≠ Reviewer (role separation) | 개발자 ≠ 리뷰어 역할 분리 |
| GATE 5 | Breaking change detection | 브레이킹 체인지 감지 |

---

## Security Built-in / 내장 보안

- OWASP Top 10 review on every sprint / 매 스프린트 OWASP Top 10 검토
- JWT httpOnly cookies only (no localStorage) / JWT는 httpOnly 쿠키만 사용
- AES-256-GCM for PII encryption / 개인정보 AES-256-GCM 암호화
- Rate limiting on all endpoints / 모든 엔드포인트 레이트 리미팅
- Input validation with Zod / Zod 기반 입력 검증
- RLS (Row Level Security) enforcement / RLS 필수 구현

---

## Repository Structure / 저장소 구조

```
docore/                          ← Copy to ~/.claude/skills/docore
│                                   ~/.claude/skills/docore 에 복사
├── CLAUDE.md                    ← Auto-loaded entry point / 자동 로드 진입점
├── install.sh                   ← Installer / 설치 스크립트
├── agents/                      ← 16 agent definitions / 16개 에이전트 정의
│   ├── dc-biz.md
│   ├── dc-dev-be.md
│   └── ... (16 total)
├── commands/                    ← Slash command definitions / 슬래시 명령어
│   ├── ceo.md
│   ├── ceo-init.md
│   └── ceo-status.md
├── skills/ceo-system/           ← CEO orchestration brain / CEO 오케스트레이션 핵심
│   └── SKILL.md
└── templates/                   ← Registry templates / 레지스트리 템플릿
    ├── error-registry.md
    ├── skill-registry.md
    ├── project-registry.md
    └── decision-log.md
```

---

## Manual Install / 수동 설치

```bash
git clone https://github.com/DoCoreTeam/docore.git /tmp/docore
cp -r /tmp/docore/docore ~/.claude/skills/docore
```

---

## Requirements / 요구사항

- [Claude Code](https://claude.ai/code) CLI
- Anthropic API key with access to Claude Opus, Sonnet, and Haiku
- Anthropic API 키 (Opus, Sonnet, Haiku 모델 접근 권한 필요)

---

## License / 라이선스

MIT — see [LICENSE](LICENSE)

---

## Author / 만든 사람

Built by **Docore** / DoCoreTeam
