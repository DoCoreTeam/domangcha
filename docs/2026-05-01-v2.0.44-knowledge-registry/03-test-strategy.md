# Test Strategy — Knowledge Registry System (v2.0.44)

## 단위 테스트 (Sprint 1-2 구현 후)

### DC-KNW query 모드
- 키워드로 엔트리 검색 → 결과 반환 ✅
- 존재하지 않는 키워드 → 빈 결과 + 오류 없음
- ID로 직접 검색 (KNW-YYYY-MM-DD-NNN)

### DC-KNW record 모드
- 유효한 엔트리 생성 → 파일 저장 + INDEX.md 업데이트
- 중복 ID 생성 시도 → 에러 + 새 시퀀스 번호 부여
- 필수 frontmatter 누락 → 유효성 검사 실패

### DC-KNW guard 모드
- 관련 constraint 엔트리 있음 → 경고 출력 (블로킹 없음)
- 없음 → 조용히 통과 (0ms 오버헤드)

### DC-KNW curate 모드
- 중복 엔트리 감지 → 병합 후 원본 archived/
- 오래된(30일+) low 엔트리 → 삭제 제안

## 통합 테스트

### CEO 파이프라인 통합
- PHASE 1 직전 guard 호출 → 결과가 PLANNER에 전달
- PHASE 6 후 record 호출 → 새 엔트리 생성 확인

### 2-Layer 검색
- global에서 먼저 검색, project-local에서 보완
- promote 명령 후 global INDEX.md 업데이트 확인

## 보안 테스트
- 엔트리에 API 키 패턴 포함 시 DC-SEC가 차단
- `kko2349@gmail.com` 등 PII 포함 금지

## 성능 테스트
- 100개 엔트리 기준 grep 검색 < 500ms
- 1000개 엔트리 기준 guard 모드 < 2초

## 회귀 테스트
- DC-KNW 추가 후 기존 17개 에이전트 동작 불변
- error-registry.md 마이그레이션 후 GATE 1 패턴 스캔 정상 동작
