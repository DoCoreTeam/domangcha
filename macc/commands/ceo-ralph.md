# /ceo-ralph — 자율 반복 완료 루프

Ralph Loop 패턴을 MACC 파이프라인에 통합한 자율 실행 명령.
완료 조건을 CEO가 직접 정의하고, 조건 충족까지 루프를 돌림.

## 사용법

```
/ceo-ralph "업무 설명"
/ceo-ralph reset          # 이전 작업 리셋 후 fresh start
/ceo-ralph status         # 현재 루프 상태 확인
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
# 1. 현재 변경사항 보존 (stash)
git stash push -m "ralph-reset-$(date +%Y%m%d-%H%M%S)"

# 2. .ralph/fix_plan.md 초기화
# 3. .ralph/decisions/ 이전 결정 archived/ 이동
# 4. 새 루프 시작
```

출력:
```
[RALPH RESET]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🗑️ 이전 작업 git stash에 보존
📁 결정 문서 archived/ 이동
🔄 clean slate에서 재시작
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### STEP 0.5: .ralph 디렉토리 초기화 (자동)

루프 시작 전 반드시 실행:

```bash
mkdir -p .ralph/decisions .ralph/archived
# status.json이 없으면 초기화
if [ ! -f .ralph/status.json ]; then
  cat > .ralph/status.json << 'EOF'
{"current_task":null,"loop_number":0,"tasks_completed":0,"files_modified":0,"tests_status":"NOT_RUN","evaluators_status":"PENDING","gate_status":"PENDING","exit_signal":false,"circuit_breaker":{"status":"CLOSED","no_progress_count":0,"same_error_count":0,"gate_fail_count":0}}
EOF
fi
```

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
1. [ ] fix_plan.md의 모든 항목이 [x]로 체크됨
2. [ ] DC-QA 검증 통과 (CRITICAL/HIGH 이슈 없음)
3. [ ] DC-SEC 보안 검토 통과
4. [ ] DC-REV 코드 리뷰 통과 (점수 80+)
5. [ ] GATE 1-5 전부 통과
6. [ ] 테스트 에러 없음

## 제약사항
<하면 안 되는 것들>

## 컨텍스트
<관련 배경 정보>
```

**`.ralph/fix_plan.md` 생성:**
```markdown
# Fix Plan — <업무명>
생성: YYYY-MM-DD

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
- [ ] git commit
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
4. **기술 선택 발생 시 → WEIGHTED DECISION 실행** (아래 참조)
5. 의사결정 문서화 → `.ralph/decisions/DECISION-<날짜>-<주제>.md`
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

루프 중 기술 선택/접근법 선택이 필요할 때 **반드시** 이 형식으로 처리:

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

EXIT_SIGNAL: true 설정 후:
1. GATE 1-5 최종 확인
2. 버전 PATCH 업 (`macc/VERSION`)
3. git commit
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
