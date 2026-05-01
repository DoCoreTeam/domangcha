# Architecture — Knowledge Registry System (v2.0.44)

## 디렉토리 구조

```
~/.claude/
└── knowledge-registry/          # Global layer
    ├── INDEX.md                  # 전체 엔트리 목록 (ID + 1줄 요약)
    ├── pattern/
    │   └── KNW-2026-05-01-001.md
    ├── decision/
    ├── error/
    ├── insight/
    └── constraint/

domangcha/
└── knowledge-registry/          # Project-local layer
    ├── INDEX.md
    ├── pattern/
    ├── decision/
    ├── error/
    ├── insight/
    └── constraint/
```

## DC-KNW 에이전트 위치

```
domangcha/agents/dc-knw.md      # 18번째 DOMANGCHA 직원
```

- 그룹: 🟦 PLANNER (지식 관리는 계획 단계 지원)
- 모델: claude-sonnet-4-6 (검색/분류 작업)
- ECC subagent_type: `dc-knw`

## CEO 파이프라인 통합 흐름

```
PHASE -1 (INTENT PARSE)
  └── [선택적] DC-KNW query → 유사 업무 선례 조회

PHASE 1 (PLANNER) 시작 직전
  └── DC-KNW guard → 현재 작업 관련 제약/패턴 확인
         ↓
    경고 있으면 → CEO에게 보고 (블로킹 없음)

PHASE 6 (GATE 통과 후)
  └── DC-KNW record → 이번 작업에서 발견된 패턴/결정 기록
```

## 명령어 라우팅

```
/ceo-knowledge <query>
  CEO → DC-KNW(query) → 결과 반환

/ceo-learn "<패턴>"
  CEO → DC-KNW(record) → 새 엔트리 생성 → INDEX.md 업데이트

/ceo-forget <KNW-ID>
  CEO → GATE 5 (파괴적 변경 → 사용자 승인) → DC-KNW(delete)

/ceo-promote <KNW-ID>
  CEO → project-local → global 복사 → scope: global 변경
```

## 데이터 흐름

```
CEO/DC-* 에이전트
    │
    ▼ (새 패턴 발견)
DC-KNW record
    │
    ▼
knowledge-registry/<type>/KNW-<date>-<seq>.md 생성
    │
    ▼
INDEX.md 업데이트 (항목 추가)
```

## install.sh 변경 (v2.0.45 구현 시)

```bash
# Step N: Knowledge Registry 초기화
mkdir -p ~/.claude/knowledge-registry/{pattern,decision,error,insight,constraint}
if [ ! -f ~/.claude/knowledge-registry/INDEX.md ]; then
  echo "# Knowledge Registry Index\n\n| ID | Type | Summary |\n|---|---|---|" > ~/.claude/knowledge-registry/INDEX.md
fi
```
