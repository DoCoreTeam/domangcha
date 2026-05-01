# Task Breakdown — Knowledge Registry System (v2.0.44)

> 이 태스크 목록은 v2.0.45+ 구현 스프린트를 위한 준비 사항이다.
> 현재 버전(v2.0.44)에서는 이 문서만 생성하고, 구현은 다음 스프린트에서 진행.

## Sprint 1 — 인프라 (P0)

- [ ] P0-1: `domangcha/agents/dc-knw.md` 에이전트 파일 생성
  - 4개 모드 (query/record/guard/curate) 구현
  - 모델: claude-sonnet-4-6

- [ ] P0-2: `domangcha/knowledge-registry/` 디렉토리 구조 초기화
  - INDEX.md 포함
  - 5개 타입 폴더 생성

- [ ] P0-3: `domangcha/install.sh`에 Knowledge Registry 초기화 스텝 추가
  - global (`~/.claude/knowledge-registry/`) 자동 생성
  - project-local (`domangcha/knowledge-registry/`) 자동 생성

## Sprint 2 — CEO 파이프라인 통합 (P0)

- [ ] P0-4: `domangcha/commands/ceo.md`에 DC-KNW 통합 포인트 추가
  - PHASE 1 직전: guard 모드 자동 호출
  - PHASE 6 후: record 모드 자동 호출

- [ ] P0-5: 에이전트 카운트 17 → 18 동기화 (8개 파일)
  - CLAUDE.md, ceo.md, README.md 등

- [ ] P0-6: `domangcha/commands/ceo-knowledge.md` 신규 명령어 파일
  - /ceo-knowledge, /ceo-learn, /ceo-forget, /ceo-promote 정의

## Sprint 3 — 마이그레이션 (P1)

- [ ] P1-1: `domangcha/error-registry.md` → Knowledge Registry 포맷 변환 스크립트
- [ ] P1-2: 기존 error-registry 엔트리 일괄 import (타입: error)
- [ ] P1-3: error-registry.md 읽기 전용 표시

## Sprint 4 — QA (P1)

- [ ] P1-4: DC-QA: DC-KNW 모든 모드 동작 검증
- [ ] P1-5: DC-SEC: 지식 엔트리 민감 정보 스캔 (API 키 등)
- [ ] P1-6: DC-REV: 코드 리뷰 + 80점 이상

## P2 (선택)

- [ ] P2-1: `/ceo-knowledge` 결과를 README에 "Knowledge Stats" 섹션으로 노출
- [ ] P2-2: DC-KNW curate 모드 자동 주간 실행 (Cron)
