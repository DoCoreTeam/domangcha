# DOMANGCHA Project Registry

> 현재 진행 중인 프로젝트와 확정된 기술 결정사항을 기록
> CEO는 새 작업 착수 전 이 파일을 확인하여 제약 충돌을 사전 방지

---

## 활성 프로젝트

| 코드 | 프로젝트명 | 상태 | 기술스택 | 담당자 |
|------|-----------|------|---------|-------|
| DOCORE | DOMANGCHA CEO System | ACTIVE | Claude Code + Bash + MD | CEO |

---

## DOCORE — 기술 결정사항

### 아키텍처
- **언어**: Bash + Markdown + JavaScript (hooks)
- **에이전트 런타임**: Claude Code subagent (Agent tool)
- **설정 소스**: `domangcha/VERSION` — 단일 버전 소스
- **에이전트 위치**: `~/.claude/agents/dc-*.md` (런타임) + `domangcha/agents/` (소스)

### 버전 관리
- VERSION 파일이 단일 소스
- PATCH: CEO 자동 (버그픽스, Phase 진행)
- MINOR/MAJOR: 사용자 명시 필요

### 에이전트 모델 배정 (확정 2026-04-29)
| 에이전트 | 모델 |
|---------|-----|
| DC-BIZ, DC-OSS, DC-SEC, DC-REV | claude-opus-4-7 |
| DC-RES, DC-DEV-*, DC-QA | claude-sonnet-4-6 |
| DC-WRT, DC-DOC, DC-SEO, DC-TOK | claude-haiku-4-5-20251001 |

### Ralph Loop (추가 2026-04-29)
- `/ceo-ralph` 명령으로 자율 반복 루프 실행
- `.ralph/` 디렉토리에 상태 관리
- RALPH_STATUS 블록으로 완료 조건 추적
- Circuit Breaker: 무진행 3회 또는 동일 에러 5회 시 중단

### 금지사항
- `CLAUDE_CODE_SUBAGENT_MODEL` 전역 설정 금지 (에이전트별 frontmatter 모델 사용)
- SKILL.md 1,969줄 이상 확장 금지 (분할 우선)
- error-registry.md 없이 GATE 1 통과 불가

---

## 프로젝트 등록 템플릿

```markdown
### PRJ-XXX — 프로젝트명
- **목적**: 
- **기술스택**: 
- **완료 기준**: 
- **제약사항**: 
- **시작일**: YYYY-MM-DD
- **관련 문서**: 
```
