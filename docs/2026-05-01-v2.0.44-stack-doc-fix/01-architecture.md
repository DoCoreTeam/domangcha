# Architecture — Stack DOC-FIRST Gap Fix (v2.0.44)

## 수정 대상 파일

```
domangcha/commands/
├── ceo.md              ← PHASE 0.3 스택 설명 3줄 수정 (300줄 유지)
└── ceo-ralph.md        ← STEP 1 fix_plan 템플릿 + PROMPT 완료기준 수정 (300줄 유지)
```

## 스택별 최종 흐름 (수정 후)

### Standard (변경 없음)
```
Q&A → TASK SYNTHESIS → DOC-FIRST(PHASE 0.65) → RIPPLE → PLANNER → GENERATOR → EVALUATOR → GATE → deploy
```

### Ralph Loop (수정)
```
.ralph/ 초기화 → PROMPT.md + fix_plan.md 생성(STEP 1)
  → DOC-FIRST: docs/<slug>/ 5개 파일(STEP 1.7 신규)  ← 추가
  → 자율 루프(STEP 2~3.5)
  → EXIT_SIGNAL: true
  → GATE 1-5
  → git commit + push + npm publish  ← 명시
```

### gstack (명시화만)
```
Q&A → DOC-FIRST(PHASE 0.65) → PLANNER → GENERATOR → EVALUATOR + Skill("gstack") E2E → GATE → deploy
```

### Superpowers (수정)
```
brainstorming → writing-plans → 승인(user approval)
  → DOC-FIRST: writing-plans 내용 → docs/<slug>/ 5개 파일  ← 추가
  → executing-plans
  → GATE 1-5  ← 추가
  → git commit + push + npm publish  ← 추가
```

## 핸드오프 포인트

각 스택이 고유 단계를 마치면 공통 DOMANGCHA 플로우로 합류하는 지점:

| 스택 | 고유 단계 종료 지점 | DOMANGCHA 플로우 합류 |
|------|------------------|---------------------|
| Ralph | STEP 1(PROMPT.md 생성) 직후 | DOC-FIRST → 루프 → GATE → deploy |
| Superpowers | 승인(승인) 직후 | DOC-FIRST → executing-plans → GATE → deploy |
| gstack | PHASE 0.65 이미 내포 | (변경 없음) |
