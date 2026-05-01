---
name: DOC-FIRST 절대 불변 규칙 (PHASE 0.65)
description: Q&A→TASK SYNTHESIS 완료 후 모든 스택에서 docs/YYYY-MM-DD-vX.X.X-<task-slug>/ 생성 + 5개 기획 문서 필수. 건너뛰면 규칙 위반.
type: project
---
## DOC-FIRST 규칙 (절대 불변)

**적용 범위**: Standard, Ralph Loop, gstack, Superpowers — 어떤 스택이라도 예외 없음

**트리거**: [TASK REFINED] 출력 직후 자동 실행 (PHASE 0.65)

### 실행 순서

1. **폴더 생성**: `docs/YYYY-MM-DD-vX.X.X-<task-slug>/` (오늘 날짜 + domangcha/VERSION + slug: lowercase-kebab, EN, 1-3 words)
2. **문서 작성** (5개 필수):
   - `00-requirements.md` — 기능/비기능 요구사항
   - `01-architecture.md` — 시스템 설계, 데이터 흐름, 컴포넌트 구조
   - `02-task-breakdown.md` — 태스크 목록, 우선순위(P0/P1/P2), 의존 관계
   - `03-test-strategy.md` — 테스트 우선순위 · 유닛/통합/E2E 구분 · 보안 테스트 기준
   - `04-completion-criteria.md` — 완료 조건 · 종료 기준 · 롤백 기준
3. **기획자 자가점검**: 갭 분석 → 사용자에게 질문 → 갭 해소 + 승인
4. **[DOC COMPLETE]** 출력 후 PHASE 0.8 → PHASE 1 진입

### 완료 신호
```
[DOC COMPLETE] ✅ docs/YYYY-MM-DD-vX.X.X-<slug>/ 생성 완료
  요구사항 ✅ | 아키텍처 ✅ | 태스크 ✅ | 테스트전략 ✅ | 완료기준 ✅
```

**Why**: 구현 중 방향 혼선, 테스트 누락, 완료 기준 불명확 문제를 방지. 문서가 없으면 16명이 제각각 방향으로 구현하는 혼돈 발생.
**How to apply**: 어떤 /ceo 명령이든 Q&A→TASK SYNTHESIS 완료 직후 이 단계를 반드시 실행. 건너뛰는 것은 규칙 위반.
