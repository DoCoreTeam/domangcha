# /ceo — 전체 파이프라인 자동 실행

사용자가 입력한 업무를 받아 **모든 에이전트가 개발 순서대로 자동 실행**함
중간 생략 없음 — 항상 전체 파이프라인이 돌아감

## 사용법

```
/ceo "원하는 업무 설명"
```

## 실행 순서 (이 순서 반드시 전부 실행)

### PHASE 1: PLANNER (기획)

CEO가 아래를 순서대로 수행:

1. **CEO 자가점검** 실행
   - 사용자가 명시하지 않았지만 포함해야 할 항목 확인
   - error-registry 관련 패턴 확인
   - skill-registry 사용 가능 패턴 확인
   - project-registry 제약 충돌 확인

2. **Intake Report** 생성
   ```
   [CEO INTAKE REPORT]
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📋 업무명: $ARGUMENTS
   🎯 목표: <달성해야 할 결과>
   ⚠️ 위험도: LOW / MEDIUM / HIGH / CRITICAL
   🔀 병렬 가능: YES / NO
   🚦 우선순위: P0 / P1 / P2 / P3
   💰 규모 판정: SMALL / MEDIUM / LARGE / HEAVY
   🤖 모델 배정: <Opus/Sonnet/Haiku 조합>
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```

3. **DC-BIZ** 호출 → 사업 타당성 판단 (agents/dc-biz.md 참조)
4. **DC-RES** 호출 → 기술 리서치 (agents/dc-res.md 참조)
5. **DC-OSS** 호출 → 외부 라이브러리/도구 Top 3 탐색 (agents/dc-oss.md 참조)
6. CEO가 **docs/PLAN.md** 작성

### PHASE 2: CONTRACT (계약)

7. CEO + **DC-QA** 스프린트 계약 협상
8. **docs/CONTRACT-SPRINT-1.md** 작성 (구현 범위 + 검증 기준 합의)

### PHASE 3: GENERATOR (개발 — 병렬 실행)

관련된 모든 Worker를 동시에 실행함:

9. **DC-DEV-DB** → 스키마 설계 + 마이그레이션 (agents/dc-dev-db.md 참조)
10. **DC-DEV-BE** → API 엔드포인트 + 비즈니스 로직 (agents/dc-dev-be.md 참조)
11. **DC-DEV-FE** → UI 컴포넌트 + 페이지 (agents/dc-dev-fe.md 참조)
12. **DC-DEV-MOB** → 모바일 대응 (agents/dc-dev-mob.md 참조)
13. **DC-DEV-OPS** → CI/CD + 하네스 장치 구축 (agents/dc-dev-ops.md 참조)
14. **DC-DEV-INT** → 외부 API 연동 (agents/dc-dev-int.md 참조)
15. **DC-WRT** → 마케팅 카피/콘텐츠 (agents/dc-wrt.md 참조)
16. **DC-DOC** → API 문서 + 사용 가이드 (agents/dc-doc.md 참조)
17. **DC-SEO** → 메타 태그 + Schema.org + SEO/AEO/GEO 최적화 (agents/dc-seo.md 참조)
18. 완료 후 **docs/SPRINT-1-HANDOFF.md** 작성 (사실만 기록 — 평가 없이)

### PHASE 4: EVALUATOR (검증 — 3-way 동시)

19. **DC-QA** → 기능/품질 테스트 → docs/QA-SPRINT-1.md (agents/dc-qa.md 참조)
20. **DC-SEC** → OWASP 기반 보안 검토 → docs/SEC-SPRINT-1.md (agents/dc-sec.md 참조)
21. **DC-REV** → 코드 리뷰 + 품질 채점 → docs/REV-SPRINT-1.md (agents/dc-rev.md 참조)

### PHASE 5: 판정

22. **전체 PASS** → PHASE 6으로 진행
23. **ANY FAIL** → GENERATOR로 돌아가서 재작업 (최대 3회)
24. **3회 초과** → 에스컬레이션:
    ```
    [ESCALATION]
    🔴 실패 업무: <업무명>
    📊 시도 횟수: 3/3
    🔍 근본 원인: <CEO 분석>
    💡 대안:
      1. 접근 방식 변경
      2. 범위 축소
      3. 수동 처리 권고
    ```

### PHASE 6: GATE + 최종 보고

25. **GATE 1**: error-registry 금지 패턴 스캔
26. **GATE 2**: 완료 조건 충족 검증
27. **GATE 3**: 버전 태그(v0.0.0) 포함 확인
28. **GATE 4**: Builder ≠ Reviewer 역할 분리 확인
29. **GATE 5**: 파괴적 변경 감지 → 있으면 사용자 승인 필요
30. **DC-TOK** → 컨텍스트 사용량 보고 (agents/dc-tok.md 참조)
31. **CEO 자가점검** 최종 실행
32. **git commit** -m "v0.1.0: $ARGUMENTS"
33. **CEO REPORT** 출력:

```
[CEO REPORT]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 업무 완료: $ARGUMENTS
🏷️ 버전: v0.x.x
👥 투입: 전체 에이전트 16명
⏱️ 실행: PLANNER→GENERATOR(병렬)→EVALUATOR(3-way)→GATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[산출물]
(실제 결과물 — 코드, 파일, 문서 등)

[품질 보증]
□ GATE 1-5 모두 통과
□ DC-QA 검증 완료
□ DC-SEC 보안 검토 완료
□ DC-REV 코드 리뷰 완료
□ 버전 태그 적용
□ 하네스 장치 구현 완료
□ CEO 자가점검 완료

[CEO 자체 추가 항목]
• (사용자가 명시하지 않았지만 CEO가 추가한 것)

[다음 권장 액션]
• (CEO가 권장하는 다음 단계)

[Rollback 가이드]
• (문제 발견 시 되돌리는 방법)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
