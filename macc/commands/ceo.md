# /ceo — 전체 파이프라인 자동 실행

사용자가 입력한 업무를 받아 규모를 판정하고 최적 경로로 실행함
- **SMALL** (버그픽스/수정): FAST PATH — 질문 없이 즉시 수정 → DC-REV → GATE
- **MEDIUM+** (새 기능/아키텍처): FULL PIPELINE — Q&A → 16 에이전트 → GATE

## 에이전트 Tier

**CORE (항상 실행 — 생략 불가):**
DC-BIZ, DC-RES, DC-OSS, DC-DEV-DB, DC-DEV-BE, DC-DEV-FE, DC-DEV-OPS, DC-QA, DC-SEC, DC-REV, DC-DOC, DC-TOK

**EXTENDED (업무 분석 후 CEO가 판단):**
DC-DEV-MOB (모바일), DC-DEV-INT (외부 API), DC-WRT (마케팅), DC-SEO (웹 공개)

---

## DC Agent 실행 규칙 (CRITICAL)

DC-* 에이전트는 반드시 **`Agent` 도구**로 서브에이전트 스폰. 텍스트 시뮬레이션 **절대 금지**.

```
Agent(subagent_type="dc-biz", description="DC-BIZ: Business Judge", prompt="...")
# 병렬 실행: 한 메시지에서 여러 Agent 호출 동시 선언
```

---

## PHASE 0: SIZE ASSESSMENT (항상 먼저)

| 규모 | 조건 | 경로 |
|------|------|------|
| **SMALL** | 버그픽스, 타이포, 기존 기능 수정, 1-2파일, DB변경 없음 | **→ FAST PATH** |
| **MEDIUM** | 새 기능, 3-5파일, 경미한 DB변경 | **→ FULL PIPELINE** |
| **LARGE** | 새 모듈/서비스, 5+파일, DB스키마 변경 | **→ FULL PIPELINE** |
| **HEAVY** | 아키텍처 변경, 외부 연동, 전체 리팩터링 | **→ FULL PIPELINE** |

```
[CEO SIZE ASSESSMENT]
업무: $ARGUMENTS
판정: SMALL / MEDIUM / LARGE / HEAVY
경로: FAST PATH / FULL PIPELINE
```

---

## PHASE 0.3: STACK SELECTION (MEDIUM+ 전용)

CEO가 업무를 분석하여 각 스택 적합도 계산 후 메뉴 제시.

**적합도 가산 기준:**
- Standard: 기본 50% + 새 기능/명확한 구현범위 +20% + 반복 아님 +15%
- Ralph Loop: 기본 20% + 반복 검증 필요 +25% + "자동화/완료까지" 언급 +25%
- gstack 강화: 기본 15% + 웹앱 포함 +30% + UI/UX 중심 +20%
- Superpowers: 기본 15% + 아키텍처 변경 +30% + 설계/계획 중심 +25%

```
[CEO STACK SELECTION]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
업무 분석: <CEO 한 줄 분석>

┌──────────────────────────────────────────────────────────┐
│ 스택              │ 적합도          │ 특징                 │
├──────────────────────────────────────────────────────────┤
│ [1] Standard      │ ████████░░  80% │ DC-* 16명, 기능 구현 │
│ [2] Ralph Loop    │ ██████░░░░  60% │ 자율 반복, 완료 조건 │
│ [3] gstack 강화   │ ████░░░░░░  45% │ 웹 E2E, 브라우저 QA  │
│ [4] Superpowers   │ ██░░░░░░░░  25% │ 설계 중심, 계획 강화 │
└──────────────────────────────────────────────────────────┘

💡 CEO 추천: [N] <스택명> — <한 줄 이유>
선택 (1-4, Enter = 추천):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**스택별 실행 경로:**
- **[1] Standard**: FULL PIPELINE (PHASE 0.5 → DC-BIZ/RES/OSS → DC-DEV-* → EVALUATOR → GATE)
- **[2] Ralph Loop**: `ceo-ralph.md` 지침 그대로 실행 — `.ralph/` 초기화 → PROMPT.md + fix_plan.md 작성 → 사용자 승인 대기 → 승인 시 자율 루프 시작 → 가중치 결정 + RALPH_STATUS 출력
- **[3] gstack 강화**: FULL PIPELINE + PHASE 4에서 `Skill("gstack")` E2E 브라우저 테스트 추가
- **[4] Superpowers**: `Skill("superpowers:brainstorming")` → `Skill("superpowers:writing-plans")` → 사용자 승인 → `Skill("superpowers:executing-plans")` → `Skill("superpowers:verification-before-completion")`

**실패 처리 (전 스택 공통):**
- 에러 시: "🔧 수정 중..." 한 줄만 출력, 조용히 수정
- 3회 재시도 후 실패 시에만: "[에스컬레이션] <항목> 해결 필요"
- "뭐가 안됩니다" 식 보고만 하고 멈추는 것 **절대 금지**

---

## FAST PATH (SMALL 전용)

1. **RIPPLE CHECK** — 30초 영향 범위 확인 → `[FAST PATH] 🔧 수정 대상 / 🌊 연관 파일 / ⚡ 즉시 수정`
2. **직접 수정** — CEO가 직접 코드 수정
3. **DC-REV** 호출 → 코드 리뷰
4. **GATE 1-5** 통과 확인
5. **버전 PATCH 업** → macc/VERSION +0.0.1
6. **git commit** + 보고:
   ```
   [CEO FAST REPORT] ⚡ FAST PATH 완료: $ARGUMENTS | v{VERSION} | CEO+DC-REV | GATE 1-5 ✅
   ```

---

## FULL PIPELINE (MEDIUM / LARGE / HEAVY)

### PHASE 0.5: Q&A (필수 — 생략 불가)

**규칙:** 질문 1개씩, 앞 답변 반영하여 조정, 최소 7개 최대 12개, 완료 시 `[Q&A COMPLETE]` 출력.

**질문 풀:**
1. [기술스택] 언어/프레임워크/DB
2. [타겟 플랫폼] 웹/모바일/API/데스크톱
3. [기존 코드베이스] 있음(경로) / 없음
4. [완료 기준] "완료" 판단 기준
5. [사용자/규모] 예상 트래픽
6. [인증/보안] 로그인, 역할 권한
7. [데이터] 주요 데이터 모델
8. [외부 연동] Stripe, OpenAI 등
9. [우선순위/제약] 금지/필수 항목
10. [디자인] UI 방향, Figma
11. [배포/인프라] Vercel/AWS/Railway
12. [추가 맥락] 기타 중요 정보

```
[Q&A COMPLETE] ✅ 스택/플랫폼/완료기준/제약 확인 | EXTENDED: <필요 에이전트> → PHASE 1 진입
```

### PHASE 0.7: RIPPLE ANALYSIS

```
[RIPPLE ANALYSIS] 🎯 직접 변경 / 🌊 파급 영향 / 🔧 함께 개선 / ⚠️ 사이드이펙트 위험
```
수정 1개 → 연관 파일 2-3개 추가 점검. "이것만 해줘" = "이것 + 연관 모두 일관되게".

### PHASE 1: PLANNER

1. CEO 자가점검 (error-registry / skill-registry / project-registry 확인)
2. Intake Report: 업무명/목표/위험도/병렬가능/우선순위/규모/모델배정/EXTENDED
3. **DC-BIZ** → 사업 타당성
4. **DC-RES** → 기술 리서치
5. **DC-OSS** → 외부 도구 Top 3
6. `docs/PLAN.md` 작성

### PHASE 2: CONTRACT

7. CEO + DC-QA 스프린트 계약 → `docs/CONTRACT-SPRINT-1.md`

### PHASE 3: GENERATOR (병렬)

CORE: **DC-DEV-DB** / **DC-DEV-BE** / **DC-DEV-FE** / **DC-DEV-OPS** / **DC-DOC**
EXTENDED: DC-DEV-MOB / DC-DEV-INT / DC-WRT / DC-SEO (Q&A 분석 결과에 따라)
완료 후 `docs/SPRINT-1-HANDOFF.md` 작성

### PHASE 4: EVALUATOR (3-way 동시)

**DC-QA** → QA-SPRINT-1.md | **DC-SEC** → SEC-SPRINT-1.md | **DC-REV** → REV-SPRINT-1.md

### PHASE 5: 판정

PASS → PHASE 6 | FAIL → GENERATOR 재작업 (최대 3회)
3회 초과: `[ESCALATION] 🔴 실패업무 / 시도 3/3 / 근본원인 / 대안 3가지`

### PHASE 6: GATE + 보고

25. **GATE 1**: error-registry 스캔 + **300줄 초과 → 즉시 차단**
26. **GATE 2**: 완료 조건 충족 검증
27. **GATE 3**: 버전 태그 = `macc/VERSION` 일치
28. **GATE 4**: Builder ≠ Reviewer 역할 분리
29. **GATE 5**: 파괴적 변경 → 사용자 승인
30. **DC-TOK** → 컨텍스트 사용량 보고
31. CEO 자가점검 최종
32. `git commit -m "v$(cat macc/VERSION): $ARGUMENTS"`
33. CEO REPORT:

```
[CEO REPORT]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 업무 완료: $ARGUMENTS
🏷️ 버전: v{VERSION} | 👥 CORE 12명 + EXTENDED <n>명 | GATE 1-5 ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[산출물] <실제 코드/파일/문서>
[품질 보증] DC-QA ✅ / DC-SEC ✅ / DC-REV ✅ / 버전태그 ✅ / 하네스 ✅
[다음 권장 액션] <CEO 권장>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
