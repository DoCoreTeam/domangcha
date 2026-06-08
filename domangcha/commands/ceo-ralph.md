# /ceo-ralph — 자율 반복 완료 루프

Ralph Loop 패턴을 DOMANGCHA 파이프라인에 통합한 자율 실행 명령.
완료 조건을 CEO가 직접 정의하고, 조건 충족까지 루프를 돌림.

## 사용법

```
/ceo-ralph "업무 설명"
/ceo-ralph reset          # 이전 작업 리셋 후 fresh start
/ceo-ralph status         # 현재 루프 상태 확인
```

---

## RALPH LOOP 불변 원칙 (CRITICAL — 절대 금지)

```
[RALPH INTEGRITY RULES]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ LOOP-001: 루프 중간 사용자 질문 금지 (루프 시작 전 STEP 0.4 Q&A는 예외)
   → 모호한 점 발생 시 CEO가 직접 판단 + DECISION 문서에 기록
   → 사용자에게 답을 구하기 위해 멈추는 것은 루프 종료로 간주 = 위반

❌ LOOP-002: 선택지에서 멈추기 금지
   → 기술 선택, 접근법 선택 발생 시 → WEIGHTED DECISION 즉시 실행
   → CEO가 추천 선택 확정 → .ralph/decisions/ 문서화 → 루프 계속
   → 사용자 승인 없이 선택 진행 (선택 결과는 루프 완료 시 일괄 보고)

❌ LOOP-003: Circuit Breaker 외 중단 금지 (정상 EXIT_SIGNAL 완료는 중단이 아님 — 해당 없음)
   → 오직 Circuit Breaker 조건(무진행 3회 / 동일에러 5회 / GATE실패 3회)만 중단 허용
   → "어렵다", "확인 필요", "스코프 불명확" 등의 이유로 중단 절대 금지
   → 문제 발생 시 CEO가 해결책을 스스로 찾아서 계속 진행

✅ LOOP-004: 결정 즉시 문서화 + 루프 완료 시 일괄 공유
   → 루프 중 모든 결정(선택이든 판단이든)은 DECISION 파일에 즉시 기록
   → 루프 완료 보고 시 "[루프 중 자율 결정 내역]" 섹션에 전체 결정 내역 포함
   (LOOP-002는 "언제 결정하는가" / LOOP-004는 "어떻게 기록/공유하는가")
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## CEO 실행 지침

### STEP 0: 명령 파싱

```
인자가 "reset"이면 → RESET PROCEDURE 실행
인자가 "status"면 → STATUS CHECK 실행
그 외 → 신규 루프 시작
```

### RESET PROCEDURE

사용자가 "다시 해줘", "이건 아닌 것 같아", "다른 방식으로" 등을 말한 경우:

```bash
# 0. 엔진 정지 — active:false 로 내려 루프 재개를 막는다
python3 -c "import json,pathlib;p=pathlib.Path('.ralph/status.json');s=json.loads(p.read_text()) if p.exists() else {};s['active']=False;s['exit_signal']=False;s['loop_count']=0;p.write_text(json.dumps(s,ensure_ascii=False,indent=2))" 2>/dev/null || true

# 1. 현재 변경사항 보존 (stash)
git stash push -m "ralph-reset-$(date +%Y%m%d-%H%M%S)"

# 2. .ralph/fix_plan.md 초기화
# 3. .ralph/decisions/ 이전 결정 archived/ 이동
# 4. STEP 0.4(종료조건 Q&A)부터 재시작 — 이전 EXIT CONDITIONS 재사용 금지
```

출력:
```
[RALPH RESET]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🗑️ 이전 작업 git stash에 보존
📁 결정 문서 archived/ 이동
🔄 STEP 0.4(종료조건 Q&A)부터 재시작
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### STEP 0.4: 종료조건 Q&A (신규 루프 시작 시 필수 — 생략 절대 금지)

루프 시작 전, 사용자에게 **최대 2개** 질문으로 종료조건을 확정합니다.
자동 정의만으로 루프 시작하는 것은 **절대 금지**입니다.

```
[RALPH EXIT CONDITION Q&A]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
업무: <업무 설명>

Q1. [종료 조건] 이 루프가 "완료"라고 판단하는 기준은 무엇인가요?
    (예: "모든 테스트 통과", "특정 기능 동작", "에러 없음" 등)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

→ 사용자 답변 대기
→ 답변 받은 후 필요 시 Q2 추가:

```
Q2. [중단 조건] 루프를 중단해야 하는 특별한 조건이 있나요?
    없으면 기본 Circuit Breaker만 적용됩니다.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

→ Q&A 완료 후:

```
[EXIT CONDITIONS CONFIRMED]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 종료 조건: <사용자 답변 기반>
✅ 중단 조건: <사용자 답변 or "기본 Circuit Breaker">
→ STEP 0.5 진입 — 루프 시작
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**사용자 종료조건은 PROMPT.md의 "완료 기준" 섹션에 그대로 반영됩니다.**

---

### STEP 0.5: .ralph 디렉토리 초기화 (자동)

루프 시작 전 반드시 실행:

```bash
mkdir -p .ralph/decisions .ralph/archived
# status.json 초기화 — active:true 로 엔진(domangcha-ralph-loop.py)을 켠다
cat > .ralph/status.json << 'EOF'
{"active":true,"current_task":"<업무명>","loop_number":0,"loop_count":0,"max_loops":30,"tasks_completed":0,"files_modified":0,"tests_status":"NOT_RUN","evaluators_status":"PENDING","gate_status":"PENDING","exit_signal":false,"circuit_breaker":{"status":"CLOSED","no_progress_count":0,"same_error_count":0,"gate_fail_count":0,"last_error":null},"last_updated":null}
EOF
```

> ⚙️ **엔진 동작 (domangcha-ralph-loop.py — Stop hook):**
> `active:true` 인 동안, 응답이 끝나려 할 때마다 hook이 `.ralph/status.json` 을 검사한다.
> `exit_signal` 이 아직 `false` 이고 `loop_count < max_loops` 이며 Circuit Breaker 가 CLOSED 이면
> **`exit 2` 로 종료를 막고 CEO를 자동으로 다시 깨운다** → 끝까지 루프가 돈다.
> 완료조건 충족 시 **반드시 `exit_signal:true` 를 직접 설정**해야 루프가 멈춘다 (STEP 5).
> `max_loops`(기본 30) 초과 시 엔진이 안전 종료시킨다 (런어웨이 방지).

### STEP 1: 완료 조건 정의 및 문서화

CEO는 업무를 분석하여 `.ralph/PROMPT.md`와 `.ralph/fix_plan.md`를 생성한다.

**`.ralph/PROMPT.md` 생성:**
```markdown
# Ralph Loop — 업무: <업무명>
생성일: YYYY-MM-DD HH:MM
버전: v{VERSION}

## 목표
<업무의 핵심 목표>

## 완료 기준 (Completion Criteria)
다음 조건이 모두 충족될 때 EXIT_SIGNAL: true 설정:

### [사용자 정의 종료조건] ← STEP 0.4 Q&A 답변을 그대로 기재
1. [ ] <사용자가 Q1에서 답한 종료조건>
2. [ ] <사용자가 Q2에서 답한 중단조건 — 없으면 이 항목 생략>

### [시스템 필수 조건] ← 항상 포함 (사용자 정의와 병합)
3. [ ] fix_plan.md의 모든 항목이 [x]로 체크됨
4. [ ] DC-QA 검증 통과 (CRITICAL/HIGH 이슈 없음)
5. [ ] DC-SEC 보안 검토 통과
6. [ ] DC-REV 코드 리뷰 통과 (점수 80+)
7. [ ] GATE 1-5 전부 통과
8. [ ] 테스트 에러 없음
9. [ ] DOC-FIRST: docs/<slug>/ 5개 기획 문서 ✅

## 제약사항
<하면 안 되는 것들>

## 컨텍스트
<관련 배경 정보>
```

**`.ralph/fix_plan.md` 생성:**
```markdown
# Fix Plan — <업무명>
생성: YYYY-MM-DD

## Phase 0: DOC-FIRST
- [ ] docs/<slug>/ 5개 기획 문서 생성

## Phase 1: 구현
- [ ] <태스크 1>
- [ ] <태스크 2>
...

## Phase 2: 검증
- [ ] DC-QA 테스트 실행
- [ ] DC-SEC 보안 검토
- [ ] DC-REV 코드 리뷰

## Phase 3: 마무리
- [ ] GATE 1-5 통과
- [ ] 버전 업데이트
- [ ] git commit + push + npm publish
```

### STEP 1.5: 가중치 매트릭스 도출 (Q&A 컨텍스트 기반)

PROMPT.md 작성 시 Q&A 답변에서 가중치 매트릭스를 자동 도출:

| Q&A 답변 | 속도 | 안정성 | 비용 | 확장성 | 보안 |
|---------|------|--------|------|--------|------|
| 프로토타입 | 40% | 20% | 30% | 5% | 5% |
| 상용서비스 | 15% | 35% | 10% | 25% | 15% |
| 소규모(~100명) | 35% | 25% | 30% | 5% | 5% |
| 대규모(10K+명) | 10% | 30% | 10% | 35% | 15% |
| 보안/금융 | 10% | 25% | 5% | 15% | 45% |

**복합 컨텍스트**: 여러 조건 해당 시 평균. `.ralph/status.json`의 `weight_matrix` 필드에 저장.

### STEP 2: 루프 실행

각 루프 반복:
1. `fix_plan.md` 읽기 → 미완료 항목 중 최우선 1개 선택
2. 해당 태스크 실행 (CEO가 직접 또는 DC-* 에이전트 위임)
3. 완료 시 `fix_plan.md`의 해당 항목 `[x]`로 체크
4. **기술 선택 발생 시 → WEIGHTED DECISION 즉시 실행** (아래 참조)
   ⚠️ **LOOP-002 강제**: 선택지에서 멈추기 절대 금지 — CEO가 즉시 결정 후 루프 계속
5. 의사결정 문서화 → `.ralph/decisions/DECISION-<날짜>-<주제>.md`
   ⚠️ **LOOP-004 강제**: 문서화 후 루프 즉시 계속 — 사용자 확인 대기 없이 다음 항목으로
6. **RALPH_STATUS 블록 출력** (매 루프 종료 시 필수):

```
---RALPH_STATUS---
STATUS: IN_PROGRESS | COMPLETE | BLOCKED
LOOP_NUMBER: <n>
TASKS_COMPLETED_THIS_LOOP: <number>
FILES_MODIFIED: <number>
TESTS_STATUS: PASSING | FAILING | NOT_RUN
EVALUATORS_STATUS: PENDING | QA_PASS | SEC_PASS | REV_PASS | ALL_PASS
GATE_STATUS: PENDING | 1-PASS | 2-PASS | ... | ALL_PASS
EXIT_SIGNAL: false | true
RECOMMENDATION: <다음 루프에서 할 일 한 줄>
---END_RALPH_STATUS---
```

6. EXIT 판정:
   - `fix_plan.md` 체크되지 않은 항목이 있으면 → 다음 루프
   - 모든 항목 체크 + EVALUATORS_STATUS: ALL_PASS + GATE_STATUS: ALL_PASS → `EXIT_SIGNAL: true` 설정 → 루프 종료

### STEP 3: Circuit Breaker

다음 조건 시 루프 중단하고 사용자에게 보고:
- **무진행 3회 연속**: 파일 수정 없이 3루프 진행
- **동일 에러 5회**: 같은 에러 메시지 5번 반복
- **GATE 실패 3회**: 동일 GATE에서 3회 연속 실패

**중단 시 엔진 정지 필수** — `circuit_breaker.status:"OPEN"` + `active:false` 를 `.ralph/status.json` 에 기록해야 엔진이 재개하지 않는다:
```bash
python3 -c "import json,pathlib;p=pathlib.Path('.ralph/status.json');s=json.loads(p.read_text());s['active']=False;s.setdefault('circuit_breaker',{})['status']='OPEN';p.write_text(json.dumps(s,ensure_ascii=False,indent=2))"
```

중단 시 출력:
```
[RALPH CIRCUIT BREAKER — OPEN]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⛔ 트리거: <무진행|동일에러|GATE실패>
📊 반복 횟수: <n>회
🔍 근본 원인: <분석>
💡 권장:
  1. <접근 방식 변경 제안>
  2. <범위 축소 제안>
  3. /ceo-ralph reset 후 재시작
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### STEP 3.5: WEIGHTED DECISION (기술 선택 발생 시)

루프 중 기술 선택/접근법 선택이 필요할 때 **반드시** 이 형식으로 처리.

**LOOP-002 강제 규칙:**
- CEO가 WEIGHTED DECISION을 즉시 실행하고 스스로 선택 확정
- 사용자에게 승인 요청 없이 루프 계속 진행
- 선택 결과는 `.ralph/decisions/`에 문서화 후 루프 완료 보고에 일괄 포함
- "어떤 게 나을까요?" / "확인 후 진행하겠습니다" → **LOOP-002 위반 = 루프 중단으로 간주**

```
[RALPH DECISION #N]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚖️ 결정: <무엇을 선택해야 하는가>
📊 가중치 (컨텍스트: <프로토타입|상용|소규모|대규모|보안>)
   속도 <W>% | 안정성 <W>% | 비용 <W>% | 확장성 <W>% | 보안 <W>%

선택지 평가:
┌──────────────┬──────┬────────┬──────┬────────┬──────┬───────┐
│ 옵션         │ 속도 │ 안정성 │ 비용 │ 확장성 │ 보안 │ 총점  │
├──────────────┼──────┼────────┼──────┼────────┼──────┼───────┤
│ <옵션A>      │  85  │   70   │  90  │   60   │  75  │ 78.0  │ ← 선택
│ <옵션B>      │  60  │   85   │  70  │   80   │  90  │ 71.5  │
│ <옵션C>      │  95  │   50   │  95  │   40   │  55  │ 64.5  │
└──────────────┴──────┴────────┴──────┴────────┴──────┴───────┘

✅ 선택: <옵션A> (총점: 78.0/100)
📝 이유: <한 줄 이유>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**총점 계산**: 각 선택지 점수 × 가중치 합산
**기록**: 즉시 `.ralph/decisions/DECISION-<날짜>-<주제>.md` 작성

### STEP 4: 의사결정 문서화

중요 결정(기술 선택, 아키텍처 변경, 리셋 이유 등) 발생 시 즉시:

**`.ralph/decisions/DECISION-<YYYYMMDD>-<주제>.md` 생성:**
```markdown
# Decision: <제목>
날짜: YYYY-MM-DD
루프: #<n>

## 결정
<무엇을 결정했는가>
## 배경
<왜 이 결정이 필요했는가>
## 고려한 대안
1. <대안 1> — 기각 이유: <이유>
2. <대안 2> — 기각 이유: <이유>
## 최종 선택
<선택한 방법과 근거>
## 영향
<이 결정이 미치는 영향>
## 번복 조건
<이 결정을 바꾸게 될 조건>
```

### STEP 5: 루프 완료

완료조건(fix_plan 전 항목 [x] + DC-QA/SEC/REV 통과 + GATE 1-5 통과) 충족 시:

```bash
# 엔진 정지 — exit_signal:true + active:false 를 반드시 기록해야 루프가 멈춘다
python3 - << 'EOF'
import json, pathlib
p = pathlib.Path(".ralph/status.json")
s = json.loads(p.read_text())
s["exit_signal"] = True
s["active"] = False
p.write_text(json.dumps(s, ensure_ascii=False, indent=2))
EOF
```

그 후:
1. GATE 1-5 최종 확인
2. 버전 PATCH 업 (`domangcha/VERSION`)
3. git commit + git push + npm publish
4. 최종 보고:

```
[RALPH LOOP COMPLETE]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 업무 완료: <업무명>
🔄 총 루프 수: <n>회
📝 완료된 태스크: <n>개
📋 결정 문서: .ralph/decisions/ (<n>개)
🏷️ 버전: v{VERSION}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[완료 조건 체크]
✅ fix_plan.md 전 항목 체크
✅ DC-QA 통과
✅ DC-SEC 통과
✅ DC-REV 통과 (점수: <n>/100)
✅ GATE 1-5 통과

[루프 중 자율 결정 내역] ← .ralph/decisions/ 파일이 있으면 반드시 포함 / 없으면 "없음" 출력
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
루프 중 자율적으로 결정한 사항 보고 (루프를 멈추지 않고 CEO가 스스로 판단한 결정들):

결정이 없었던 경우: "자율 결정 없음 — 모든 태스크가 단일 경로로 진행됨"

결정이 있었던 경우:
| # | 결정 주제 | 선택된 옵션 | 총점 | 이유 |
|---|-----------|------------|------|------|
| 1 | <주제>     | <옵션명>    | <점수>/100 또는 N/A | <한 줄 이유> |
| 2 | <주제>     | <옵션명>    | <점수>/100 또는 N/A | <한 줄 이유> |

상세 내역: .ralph/decisions/*.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[생성된 문서]
- .ralph/PROMPT.md
- .ralph/fix_plan.md
- .ralph/decisions/*.md

[다음 권장 액션]
<CEO 권장 사항>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## .ralph 디렉토리 구조

```
.ralph/
├── PROMPT.md          # 업무 설명 + 완료 기준 (CEO 작성)
├── fix_plan.md        # 태스크 체크리스트 (CEO 작성, 루프마다 업데이트)
├── status.json        # 현재 루프 상태 (JSON)
├── decisions/         # 의사결정 문서
│   └── DECISION-YYYYMMDD-<topic>.md
└── archived/          # 리셋 시 이전 결정 이동
    └── reset-YYYYMMDD-HHMMSS/
```

---

## STATUS CHECK

`/ceo-ralph status` 실행 시:

```
[RALPH STATUS]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 현재 업무: <PROMPT.md에서 읽기>
🔄 루프 진행: <완료 태스크>/<전체 태스크>
📊 체크된 항목: <n>/<total>
📝 결정 문서: <n>개
🏷️ Circuit Breaker: CLOSED | OPEN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
