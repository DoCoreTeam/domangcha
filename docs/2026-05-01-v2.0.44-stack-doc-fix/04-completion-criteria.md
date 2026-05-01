# Completion Criteria — Stack DOC-FIRST Gap Fix (v2.0.44)

## 완료 조건

- [ ] ceo.md Ralph 설명에 `DOC-FIRST` 명시됨
- [ ] ceo.md Superpowers 설명에 `DOC-FIRST` + `GATE` + `deploy` 명시됨
- [ ] ceo.md gstack 설명에 DOC-FIRST 포함 명시됨
- [ ] ceo.md 정확히 300줄
- [ ] ceo-ralph.md fix_plan.md 템플릿에 `Phase 0: DOC-FIRST` 존재
- [ ] ceo-ralph.md PROMPT.md 완료기준에 DOC-FIRST 항목 존재
- [ ] ceo-ralph.md ≤ 300줄
- [ ] docs/2026-05-01-v2.0.44-stack-doc-fix/ 5개 파일 존재
- [ ] docs/2026-05-01-v2.0.44-knowledge-registry/ 5개 파일 존재
- [ ] domangcha/VERSION = 2.0.44
- [ ] GATE 1-5 통과
- [ ] git commit + push + npm publish 완료

## 종료 기준 (이 항목 중 하나라도 실패 시 배포 차단)
- ceo.md 300줄 초과 → GATE 1 FAIL
- Ralph/Superpowers 설명에 DOC-FIRST 키워드 없음 → 재수정

## 롤백 기준
- 위 항목 수정 불가 시 → 이전 커밋으로 롤백
