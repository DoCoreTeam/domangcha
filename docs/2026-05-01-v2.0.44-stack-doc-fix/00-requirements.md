# Requirements — Stack DOC-FIRST Gap Fix (v2.0.44)

## 기능 요구사항

### FR-1: Ralph Loop DOC-FIRST 강제
- Ralph Loop 실행 시 STEP 1(완료조건 정의) 완료 직후, STEP 2(루프 시작) 진입 전
- `docs/YYYY-MM-DD-vX.X.X-<slug>/` 폴더 생성 + 5개 기획 문서 작성 필수
- `.ralph/PROMPT.md` 내용을 기반으로 5개 파일 채움
- fix_plan.md에 Phase 0: DOC-FIRST 단계 추가

### FR-2: Superpowers DOC-FIRST 강제
- writing-plans 완료 + 사용자 승인(승인) 직후
- `docs/` 폴더 생성 + 5개 기획 문서 작성 필수 (writing-plans 산출물 → docs/ 변환)
- 이후 executing-plans 진입
- executing-plans 완료 후 GATE → deploy 연결

### FR-3: gstack DOC-FIRST 명시화
- gstack이 FULL PIPELINE을 사용하므로 PHASE 0.65 DOC-FIRST가 이미 포함됨
- 설명에 "DOC-FIRST PHASE 0.65 포함" 명시로 혼란 제거

### FR-4: Ralph Loop deploy 핸드오프
- STEP 5(루프 완료) 후 GATE → README 업데이트 → git commit + push + npm publish 명시
- 기존 STEP 5에 누락된 npm publish 추가

## 비기능 요구사항

- NFR-1: ceo.md 파일 300줄 제약 유지
- NFR-2: ceo-ralph.md 파일 300줄 제약 유지
- NFR-3: 각 스택의 고유 아이덴티티 보존
  - Ralph: `.ralph/` 폴더 구조, WEIGHTED DECISION, Circuit Breaker 유지
  - Superpowers: brainstorming → writing-plans → 승인 흐름 유지
  - gstack: FULL PIPELINE + Skill("gstack") E2E 구조 유지
