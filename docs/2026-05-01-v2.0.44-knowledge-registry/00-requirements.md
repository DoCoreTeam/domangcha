# Requirements — Knowledge Registry System (v2.0.44)

> DOC-FIRST 물화: 이전 세션(2026-05-01)에서 Q&A로 설계한 내용을 표준 docs/ 구조로 기록.
> 구현은 v2.0.45+에서 별도 스프린트.

## 배경

DOMANGCHA error-registry.md는 단순 오류 로그다. CEO와 DC-* 에이전트가 업무를 수행하면서
축적하는 지식(패턴, 결정, 도메인 인사이트)을 체계적으로 저장·검색할 인프라가 없다.
이것이 Knowledge Registry의 존재 이유다.

## 기능 요구사항

### FR-1: 지식 저장 구조 (2-Layer)
- Global: `~/.claude/knowledge-registry/` — 모든 프로젝트에 적용되는 패턴
- Project-local: `domangcha/knowledge-registry/` — 이 프로젝트 전용 지식
- 파일 포맷: Markdown + YAML frontmatter

### FR-2: 지식 엔트리 스키마
```yaml
---
id: KNW-YYYY-MM-DD-NNN
type: pattern | decision | error | insight | constraint
severity: critical | high | medium | low
domain: ceo | dc-dev | dc-qa | dc-sec | stack | version | deploy
agent: <DC-* 또는 CEO>
frequency: 1 (발생 횟수)
scope: global | project
---
## Summary
<1줄 요약>
## Context
<언제/어디서 발생>
## Rule
<구체적인 규칙 또는 패턴>
## Example
<코드/명령 예시>
## Related
<관련 엔트리 ID>
```

### FR-3: DC-KNW 에이전트 (18번째 직원)
- 역할: Knowledge Curator — 지식 수집, 검색, 정제, 강화
- 4개 운영 모드:
  - **query**: ID 또는 키워드로 엔트리 검색
  - **record**: 새 지식 엔트리 생성
  - **guard**: 현재 작업이 알려진 패턴/제약을 위반하는지 검사
  - **curate**: 중복/오래된 엔트리 정리, 유사 항목 병합

### FR-4: CEO 파이프라인 통합
- PHASE 1 시작 직전: DC-KNW guard 모드 자동 호출 (관련 제약 확인)
- PHASE 6 GATE 완료 후: DC-KNW record 모드 자동 호출 (이번 작업에서 발견한 패턴 기록)
- PHASE -1 INTENT PARSE 시: DC-KNW query 모드 선택적 호출 (유사 업무 선례 검색)

### FR-5: 명령어
- `/ceo-knowledge <query>` — 지식 베이스 검색
- `/ceo-learn "<패턴>"` — CEO가 직접 지식 기록
- `/ceo-forget <KNW-ID>` — 지식 삭제 (사용자 승인 필요)
- `/ceo-promote <KNW-ID>` — project → global 승격

### FR-6: error-registry.md 마이그레이션
- 기존 error-registry.md 항목을 Knowledge Registry 포맷으로 일괄 변환
- 마이그레이션 완료 후 error-registry.md는 하위 호환성 위해 유지 (읽기 전용)

## 비기능 요구사항

- NFR-1: DC-KNW는 모든 DC-* 에이전트에서 접근 가능 (공유 레이어)
- NFR-2: 검색 응답 < 2초 (파일 기반 grep, 인덱스 없음)
- NFR-3: 엔트리 ID 중복 불가 (날짜+시퀀스 보장)
- NFR-4: guard 모드는 파이프라인을 블로킹하지 않음 (경고만 발생)
- NFR-5: DOMANGCHA 설치 시 knowledge-registry/ 폴더 자동 초기화 (install.sh)
