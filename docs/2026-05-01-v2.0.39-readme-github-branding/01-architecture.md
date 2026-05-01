# Architecture — v2.0.39

## 변경 지점 맵

### [A] README.md
- 히어로: 새 태그라인 + 포지셔닝 카피 2줄
- "What it does" 섹션: 한눈에 보이는 3-단계 플로우 다이어그램 (텍스트)
- CTA: 설치 명령어를 더 눈에 띄게

### [B] GitHub Repo Metadata
- About description: `gh repo edit --description "..."`
- Topics: `gh repo edit --add-topic claude-code --add-topic ...`

### [C] package.json
- keywords 필드 확장: 15개 이상

### [D] docs 네이밍 컨벤션 (6개 파일)
- CLAUDE.md (root) — 규칙 3-1, 3-2
- domangcha/CLAUDE.md — 동일
- ~/.claude/CLAUDE.md — 동일
- ceo-system/SKILL.md — FAST PATH doc 단계
- ceo-core/SKILL.md — FULL PIPELINE doc 단계
- ceo-sprint/SKILL.md — 해당 단계

## 데이터 흐름
사용자 요청 → CEO → DC-WRT (카피) + DC-SEO (키워드) → CEO 직접 파일 수정 → DC-DEV-OPS (gh 명령) → DC-REV
