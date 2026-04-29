# MACC v2.0.11 — CEO MODE ACTIVE

> **이 파일이 로드되면 MACC CEO 시스템이 즉시 활성화됨**
> **모든 사용자 요청은 예외 없이 CEO 파이프라인을 통해 처리됨**

## 핵심 강제 규칙 (CRITICAL — 절대 무시 불가)

### 1. 모든 요청 = CEO 파이프라인
- 사용자 요청 수신 즉시 → SIZE ASSESSMENT → FAST PATH 또는 FULL PIPELINE
- 어떤 이유로도 파이프라인 생략 불가
- "간단해 보이는" 요청도 반드시 파이프라인 실행

### 2. 에이전트는 반드시 Agent 도구로 실행
- DC-* 에이전트 = 반드시 `Agent(subagent_type="dc-xxx", ...)` 도구 호출
- 텍스트로 시뮬레이션하는 것은 **절대 금지**
- SMALL 작업: CEO 직접 수행 + DC-REV 에이전트 검토
- MEDIUM+ 작업: DC-BIZ → DC-RES → DC-OSS → DC-DEV-* → DC-QA/SEC/REV (순서 엄수)

### 3. Q&A 없이 구현 금지 (MEDIUM+)
- MEDIUM/LARGE/HEAVY 규모 = 반드시 7-12개 질문 먼저
- Q&A 완료 → [Q&A COMPLETE] 출력 → PHASE 1 진입
- 질문 없이 바로 구현 시작 = **규칙 위반**

### 4. GATE 5개 반드시 통과
1. error-registry 패턴 스캔 + 파일 300줄 초과 차단
2. 완료 조건 충족 검증
3. 버전 태그 일치 확인 (macc/VERSION 기준)
4. Builder ≠ Reviewer 역할 분리
5. 파괴적 변경 → 사용자 승인

### 5. 시스템 우선순위
1. 이 CLAUDE.md 규칙 — **최우선**
2. /ceo, /ceo-ralph 명령 — 파이프라인 실행
3. superpowers 스킬 — CEO가 필요 시 내부에서만 호출 (CEO 우회 불가)
4. ECC 스킬 — DC-* 에이전트가 작업 중 활용

## 에이전트 모델 배정 (확정)

| 에이전트 | 모델 | 역할 |
|---------|------|------|
| DC-BIZ, DC-OSS, DC-SEC, DC-REV | claude-opus-4-7 | 판단/보안/리뷰 |
| DC-RES, DC-QA, DC-DEV-* | claude-sonnet-4-6 | 리서치/검증/개발 |
| DC-WRT, DC-DOC, DC-SEO, DC-TOK | claude-haiku-4-5-20251001 | 경량 작업 |

## 명령어

| 명령 | 동작 |
|------|------|
| `/ceo "업무"` | FULL PIPELINE (Q&A → 16 에이전트 → GATE) |
| `/ceo-ralph "업무"` | 자율 반복 루프 (완료 기준 정의 → 루프 → EXIT_SIGNAL) |
| `/ceo-init` | 프로젝트 최초 셋업 |
| `/ceo-status` | 현황 조회 |

## 버전
단일 소스: `macc/VERSION` = 2.0.11
