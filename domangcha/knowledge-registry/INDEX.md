# DOMANGCHA Knowledge Registry

> 집단 지식 저장소 — DC-KNW가 관리하는 2-layer 파일 기반 레지스트리

## 통계
- 총 엔트리: 3
- 타입별: error(2) · pattern(1) · decision(0) · workflow(0) · skill(0)
- 최근 업데이트: 2026-05-02

## 타입별 디렉토리
| 타입 | 설명 | 경로 |
|------|------|------|
| error | 반복 에러 패턴 | `error/` |
| pattern | 베스트 프랙티스 | `pattern/` |
| decision | 아키텍처 결정 | `decision/` |
| workflow | 프로세스 절차 | `workflow/` |
| skill | 기술 지식 | `skill/` |

## 엔트리 목록
| ID | 타입 | 심각도 | 요약 |
|----|------|--------|------|
| [KNW-2026-05-01-001](error/KNW-2026-05-01-001.md) | error | HIGH | 파일 300줄 초과 — GATE 1 차단 |
| [KNW-2026-05-01-002](error/KNW-2026-05-01-002.md) | error | CRITICAL | 소스코드 시크릿 하드코딩 |
| [KNW-2026-05-01-003](pattern/KNW-2026-05-01-003.md) | pattern | MEDIUM | 버전 업데이트 11개 파일 동시 수정 |

## 사용법
- 검색: `/ceo-knowledge [keyword or KNW-ID]`
- 기록: `/ceo-learn "패턴 설명"`
- 승인: `/ceo-promote` (GATE 완료 후 자동 실행)
- 삭제: `/ceo-forget KNW-ID`
