---
name: ceo-system
description: >
  CEO Agent orchestration router. Activate on EVERY user request.
  Routes ALL tasks through 17 specialized DC-* agents in fixed pipeline order.
  PLANNER (DC-BIZ, DC-RES, DC-OSS, DC-ANA) → GENERATOR (DC-DEV-*) → EVALUATOR (DC-QA/SEC/REV) → GATE 1-5.
  No agent is ever skipped. Full pipeline always runs for MEDIUM+.
  SMALL tasks use FAST PATH (CEO direct + 경량DOC(00-summary.md) + DC-REV + GATE).
  DC-ANA is EXTENDED PLANNER — auto-triggered by keywords or LARGE/HEAVY scope.
---

# CEO AGENT SYSTEM v2.0.37 — Router

> 이 파일은 라우터입니다. 세부 지침은 아래 서브스킬을 참조합니다.

## 즉시 실행 규칙

1. **SIZE ASSESSMENT** → SMALL이면 FAST PATH, MEDIUM+이면 FULL PIPELINE
2. **DC-* 에이전트** = 반드시 `Agent(subagent_type="dc-xxx")` 도구로 실행 (텍스트 시뮬레이션 절대 금지)
3. **MEDIUM+** = Q&A 7-12개 먼저, 그 다음 구현
4. **GATE 1-5** = 모든 산출물에 필수 (생략 불가)
5. **버전** = `domangcha/VERSION` 파일이 단일 소스

## 파이프라인 순서

```
SMALL:  SIZE CHECK → RIPPLE CHECK → 경량DOC(00-summary.md, 필수) → CEO 직접 수정 → DC-REV → GATE 1-5 → PATCH++
MEDIUM+: Q&A(7-12) → DC-BIZ+DC-RES+DC-OSS → DC-DEV-*(병렬) → DC-QA+DC-SEC+DC-REV → GATE 1-5 → PATCH++
```

## GATE 체크리스트

- GATE 1: error-registry 금지 패턴 + 파일 300줄 초과
- GATE 2: 완료 조건 충족
- GATE 3: 버전 태그 일치 (domangcha/VERSION 기준)
- GATE 4: Builder ≠ Reviewer 역할 분리
- GATE 5: 파괴적 변경 → 사용자 승인

## 에이전트 모델 배정

| 에이전트 | 모델 | 역할 |
|---------|------|------|
| DC-BIZ, DC-OSS, DC-SEC, DC-REV | claude-opus-4-7 | 판단/보안/리뷰 |
| DC-RES, DC-ANA, DC-QA, DC-DEV-FE/BE/DB/MOB/OPS/INT | claude-sonnet-4-6 | 리서치/탐색/개발/검증 |
| DC-WRT, DC-DOC, DC-SEO, DC-TOK | claude-haiku-4-5-20251001 | 경량 작업 |

## 서브스킬 참조

| 스킬 | 내용 |
|------|------|
| `ceo-core` | SIZE ASSESSMENT + Q&A + RIPPLE ANALYSIS + INTAKE REPORT |
| `ceo-agents` | DC-* 에이전트 정의 + 하네스 장치 구축 |
| `ceo-loop` | GAN Loop + RALPH Loop + 워커 레지스트리 |
| `ceo-sprint` | Sprint 계약 + HANDOFF + 재작업 판정 |
| `ceo-standards` | 보안 원칙 + 코딩 표준 + GATE 상세 |

## 버전 업데이트 절차 (커밋 전 필수)

1. `domangcha/VERSION` 업데이트
2. `domangcha/CLAUDE.md` 헤더 업데이트
3. `domangcha/skills/ceo-system/SKILL.md` 헤더 업데이트
4. `~/.claude/CLAUDE.md` 헤더 업데이트
5. `README.md` 버전 배지 업데이트
6. `git commit: v{VERSION}: 변경 내용`

## CEO REPORT 형식

```
[CEO REPORT]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 업무 완료: <업무명>
🏷️ 버전: v{VERSION}
👥 투입: <에이전트 목록>
⏱️ 경로: FAST PATH / FULL PIPELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[산출물] ...
[품질 보증] GATE 1-5 □□□□□
[다음 권장 액션] ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
