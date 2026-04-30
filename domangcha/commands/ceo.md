# /ceo — 전체 파이프라인 자동 실행

사용자가 입력한 업무를 받아 규모를 판정하고 최적 경로로 실행함
- **SMALL** (버그픽스/수정): FAST PATH — 질문 없이 즉시 수정 → 🟥 DC-REV → GATE
- **MEDIUM+** (새 기능/아키텍처): FULL PIPELINE — Q&A → 16 에이전트 → GATE

## 에이전트 Tier & 인라인 컬러 규칙 (CRITICAL)

**에이전트 이름은 어디서 언급하든 반드시 그룹 이모지를 prefix로 붙일 것:**

| 그룹 | 이모지 | 에이전트 |
|------|--------|---------|
| PLANNER | 🟦 | DC-BIZ · DC-RES · DC-OSS |
| GENERATOR | 🟩 | DC-DEV-BE · DC-DEV-FE · DC-DEV-DB · DC-DEV-OPS · DC-DEV-MOB · DC-DEV-INT · DC-WRT · DC-DOC · DC-SEO |
| EVALUATOR | 🟥 | DC-QA · DC-SEC · DC-REV |
| SUPPORT | 🟨 | DC-TOK |

예: `🟦 DC-BIZ`, `🟩 DC-DEV-BE`, `🟥 DC-REV`, `🟨 DC-TOK`

**CORE (항상 실행 — 생략 불가):**
🟦 DC-BIZ, 🟦 DC-RES, 🟦 DC-OSS, 🟩 DC-DEV-DB, 🟩 DC-DEV-BE, 🟩 DC-DEV-FE, 🟩 DC-DEV-OPS, 🟥 DC-QA, 🟥 DC-SEC, 🟥 DC-REV, 🟩 DC-DOC, 🟨 DC-TOK

**EXTENDED (업무 분석 후 CEO가 판단):**
🟩 DC-DEV-MOB (모바일), 🟩 DC-DEV-INT (외부 API), 🟩 DC-WRT (마케팅), 🟩 DC-SEO (웹 공개)

---

## DC Agent 실행 규칙 (CRITICAL)

DC-* 에이전트는 반드시 **`Agent` 도구**로 서브에이전트 스폰. 텍스트 시뮬레이션 **절대 금지**.

```
Agent(subagent_type="dc-biz", description="DC-BIZ: Business Judge", prompt="...")
# 병렬 실행: 한 메시지에서 여러 Agent 호출 동시 선언
```

---

## PHASE -2: VERSION CHECK (항상 먼저 — INTENT PARSE 전)

**목적:** 업데이트가 있을 때만 사용자에게 알림. npm 호출은 최대 1시간에 1번으로 제한.

**작동 방식 (hook이 자동 처리 — CEO가 npm 직접 호출하지 않음):**
- `domangcha-ceo-enforcer.py` hook이 캐시(`~/.claude/.domangcha-version-cache`)를 확인
- 캐시 유효(1시간 이내) → 파일 읽기만, npm 호출 없음 (거의 0ms)
- 캐시 만료/없음 → npm 1번 호출 → 캐시 갱신
- 버전 같으면 → 완전 무음, CEO는 아무것도 하지 않음
- 버전 다를 때만 → hook이 시스템 메시지에 `[⚠️ UPDATE]` 주입

**CEO 실행 규칙:**
1. 시스템 메시지에 `[⚠️ UPDATE]`가 있으면 → 아래 질문만 출력하고 **즉시 멈춤** (PHASE -1 절대 진입 금지):
   ```
   [CEO] 새 버전 v{LATEST}가 있습니다 (현재 설치: v{INSTALLED}).
   업데이트하고 진행할까요? (y/n, 기본값 n):
   ```
   → 이 응답에서 추가 처리 없음. 사용자 답변 대기.
2. 사용자가 **y** → `npx domangcha` 실행 → "✅ 업데이트 완료" → PHASE -1 진행
3. 사용자가 **n** 또는 엔터 → "⏩ 건너뜀" → PHASE -1 진행
4. `[⚠️ UPDATE]` 없으면 → 바로 PHASE -1 진행 (알림 없음)

---

## PHASE -1: INTENT PARSE (항상 먼저)

입력을 구조화된 태스크로 변환. 핵심 정보 누락 시 최대 2-3개 질문. 항상 아래 블록 출력:

```
[INTENT PARSED]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
원본: <사용자 입력>  |  정제: <구조화 태스크>  |  목표: <1줄>  |  범위: <포함/제외>  |  전제: <스택·제약>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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
- **[1] Standard**: FULL PIPELINE (PHASE 0.5 → 🟦 DC-BIZ/RES/OSS → 🟩 DC-DEV-* → 🟥 EVALUATOR → GATE)
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
3. **🟥 DC-REV** 호출 → 코드 리뷰
4. **GATE 1-5** 통과 확인
5. **버전 PATCH 업** → domangcha/VERSION +0.0.1
6. **README 업데이트** (필수 — 생략 불가) — 변경 사항을 README에 반영. 새 기능/명령어/동작 변경 모두 포함. 형식적 수정 금지, 실제 내용 반영.
7. **git commit** + **git push** + **npm publish** (3개 세트 — 생략 불가):
   ```bash
   git commit -m "v{VERSION}: $ARGUMENTS"
   git push origin main
   npm publish --access public
   ```
8. 보고:
   ```
   [CEO FAST REPORT] ⚡ FAST PATH 완료: $ARGUMENTS | v{VERSION} | CEO+🟥 DC-REV | GATE 1-5 ✅ | npm@{VERSION} ✅
   ```

---

## FULL PIPELINE (MEDIUM / LARGE / HEAVY)

### PHASE 0.5: Q&A (필수 — 생략 불가)

**규칙:** 질문 1개씩, 앞 답변 반영하여 조정, 최소 7개 최대 12개, 완료 시 `[Q&A COMPLETE]` 출력.

**질문 풀 (7-12개):** 기술스택 · 플랫폼 · 기존코드 · 완료기준 · 트래픽 · 인증/보안 · 데이터모델 · 외부연동 · 우선순위/제약 · 디자인 · 배포인프라 · 추가맥락

```
[Q&A COMPLETE] ✅ 스택/플랫폼/완료기준/제약 확인 | EXTENDED: <필요 에이전트>
```

### PHASE 0.6: TASK SYNTHESIS (Q&A 완료 후 2차 정제 — 항상 실행)

Q&A 답변 전체 + INTENT PARSE 결과를 종합하여 최종 실행 태스크 확정.

```
[TASK REFINED]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
원본 입력: <사용자 원본>
Q&A 핵심 답변: <스택 / 완료기준 / 제약 / 맥락 요약>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
최종 태스크: <정제된 실행 명세 — 구체적, 측정 가능, 범위 명확>
완료 조건: <"완료"를 판단하는 기준 목록>
제외 범위: <이번 스프린트에서 하지 않을 것>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
→ PHASE 0.65 진입
```

### PHASE 0.65: DOC-FIRST (절대 불변 — 생략 불가 — 모든 스택 예외 없음)

**[TASK REFINED] 직후 실행.** `mkdir -p docs/$(date +%Y-%m-%d)-v$(cat domangcha/VERSION)`

5개 문서 필수: `00-requirements.md` · `01-architecture.md` · `02-task-breakdown.md` · `03-test-strategy.md` · `04-completion-criteria.md`

기획자 자가점검 → 갭 해소 → `[DOC COMPLETE] ✅` 출력 → PHASE 0.8 진입

**건너뛰기 절대 금지** — 모든 스택 동일

### PHASE 0.8: RIPPLE ANALYSIS

```
[RIPPLE ANALYSIS] 🎯 직접 변경 / 🌊 파급 영향 / 🔧 함께 개선 / ⚠️ 사이드이펙트 위험
```
수정 1개 → 연관 파일 2-3개 추가 점검. "이것만 해줘" = "이것 + 연관 모두 일관되게".

### PHASE 1: PLANNER

1. CEO 자가점검 (error-registry / skill-registry / project-registry 확인)
2. Intake Report: 업무명/목표/위험도/병렬가능/우선순위/규모/모델배정/EXTENDED
3. **🟦 DC-BIZ** → 사업 타당성
4. **🟦 DC-RES** → 기술 리서치
5. **🟦 DC-OSS** → 외부 도구 Top 3
6. `docs/PLAN.md` 작성

### PHASE 2: CONTRACT

7. CEO + 🟥 DC-QA 스프린트 계약 → `docs/CONTRACT-SPRINT-1.md`

### PHASE 3: GENERATOR (병렬)

CORE: **🟩 DC-DEV-DB** / **🟩 DC-DEV-BE** / **🟩 DC-DEV-FE** / **🟩 DC-DEV-OPS** / **🟩 DC-DOC**
EXTENDED: 🟩 DC-DEV-MOB / 🟩 DC-DEV-INT / 🟩 DC-WRT / 🟩 DC-SEO (Q&A 분석 결과에 따라)
완료 후 `docs/SPRINT-1-HANDOFF.md` 작성

**에이전트 그룹 출력 형식 (필수 — 매 그룹 실행 결과 보고 시 사용):**
```
┌─────────────────────────────────────────────────────┐
│ 🟦 PLANNER                                          │
│  └ 🟦 DC-BIZ ✅ 사업타당성  🟦 DC-RES ✅ 리서치  🟦 DC-OSS ✅ OSS Top3 │
├─────────────────────────────────────────────────────┤
│ 🟩 GENERATOR                                        │
│  └ 🟩 DC-DEV-BE ✅  🟩 DC-DEV-FE ✅  🟩 DC-DEV-DB ✅  🟩 DC-DEV-OPS ✅  🟩 DC-DOC ✅ │
│    [EXTENDED] 🟩 DC-DEV-MOB ✅  🟩 DC-DEV-INT ✅  🟩 DC-WRT ✅  🟩 DC-SEO ✅ │
├─────────────────────────────────────────────────────┤
│ 🟥 EVALUATOR                                        │
│  └ 🟥 DC-QA ✅ PASS  🟥 DC-SEC ✅ PASS  🟥 DC-REV ✅ 88/100  │
├─────────────────────────────────────────────────────┤
│ 🟨 SUPPORT                                          │
│  └ 🟨 DC-TOK ✅ 컨텍스트 45% 사용                       │
└─────────────────────────────────────────────────────┘
```

### PHASE 4: EVALUATOR (3-way 동시)

**🟥 DC-QA** → QA-SPRINT-1.md | **🟥 DC-SEC** → SEC-SPRINT-1.md | **🟥 DC-REV** → REV-SPRINT-1.md

### PHASE 5: 판정

PASS → PHASE 6 | FAIL → GENERATOR 재작업 (최대 3회)
3회 초과: `[ESCALATION] 🔴 실패업무 / 시도 3/3 / 근본원인 / 대안 3가지`

### PHASE 6: GATE + 보고

25. **GATE 1**: error-registry 스캔 + **300줄 초과 → 즉시 차단**
26. **GATE 2**: 완료 조건 충족 검증
27. **GATE 3**: 버전 태그 = `domangcha/VERSION` 일치
28. **GATE 4**: Builder ≠ Reviewer 역할 분리
29. **GATE 5**: 파괴적 변경 → 사용자 승인
30. **🟨 DC-TOK** → 컨텍스트 사용량 보고
31. CEO 자가점검 최종
32. **README 업데이트** (필수 — 생략 불가) — 새 기능/명령어/동작 변경을 README에 강력 반영. 형식적 수정 금지.
33. **배포 3-pack** (필수 — 생략 불가):
    ```bash
    git commit -m "v$(cat domangcha/VERSION): $ARGUMENTS"
    git push origin main
    npm publish --access public
    ```
34. CEO REPORT:

```
[CEO REPORT]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 업무 완료: $ARGUMENTS
🏷️ 버전: v{VERSION} | GATE 1-5 ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┌─────────────────────────────────────────────────────┐
│ 🟦 PLANNER                                          │
│  └ 🟦 DC-BIZ ✅  🟦 DC-RES ✅  🟦 DC-OSS ✅                  │
├─────────────────────────────────────────────────────┤
│ 🟩 GENERATOR                                        │
│  └ 🟩 DC-DEV-BE ✅  🟩 DC-DEV-FE ✅  🟩 DC-DEV-DB ✅  ...   │
├─────────────────────────────────────────────────────┤
│ 🟥 EVALUATOR                                        │
│  └ 🟥 DC-QA ✅  🟥 DC-SEC ✅  🟥 DC-REV ✅ (<점수>/100)      │
├─────────────────────────────────────────────────────┤
│ 🟨 SUPPORT                                          │
│  └ 🟨 DC-TOK ✅ 컨텍스트 <n>% 사용                     │
└─────────────────────────────────────────────────────┘
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[산출물] <실제 코드/파일/문서>
[배포] git push ✅ / npm@{VERSION} ✅ / README ✅
[다음 권장 액션] <CEO 권장>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
