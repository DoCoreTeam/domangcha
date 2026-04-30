# 01-architecture.md — GitHub Discovery Optimization Architecture
# DOMANGCHA v2.0.12 — 2026-04-30

## 1. Overview

GitHub 레포 디스커버리는 크게 3개 채널로 유입된다:
1. **GitHub Explore / Topics** — topic 태그 기반 탐색
2. **GitHub Search** — README/description 키워드 풀텍스트 검색
3. **Trending** — 단기 star 속도 기반 노출 (소셜 바이럴이 트리거)

DOMANGCHA는 이 3개 채널을 동시에 공략한다. npm 등록은 별도 패키지 레지스트리 채널을 추가한다.

---

## 2. GitHub Discovery Architecture

### 2.1 검색 노출 기여 파일 맵

```
DoCoreTeam/domangcha/
├── README.md                  ← SEO 핵심. H1/H2 키워드, 배지, 설치 명령어
├── package.json               ← npm keywords 필드 → npmjs.com 검색 노출
├── .github/
│   ├── ISSUE_TEMPLATE/        ← 커뮤니티 건강도 지표 → Explore 랭킹 가산점
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── FUNDING.yml            ← "Sponsor" 버튼 활성화 → 신뢰도 + 노출
│   ├── workflows/
│   │   └── publish.yml        ← npm auto-publish (tag push 트리거)
│   └── CODEOWNERS             ← 선택사항
├── domangcha/
│   └── install.sh             ← curl 설치 스크립트
└── bin/
    └── domangcha.js           ← npx domangcha 진입점
```

### 2.2 GitHub Topics 전략

실제 데이터 기반 상위 빈도 topics (조사된 1~170k star 레포 분석):

| 우선순위 | Topic | 이유 |
|---------|-------|------|
| P0 | `claude-code` | 8/8 레포 공통 사용. 핵심 카테고리 태그 |
| P0 | `claude` | 6/8 레포 사용. Anthropic 공식 태그 |
| P0 | `ai-agents` | 5/8 레포. 고트래픽 브로드 태그 |
| P0 | `anthropic` | 4/8 레포. 브랜드 연관 |
| P0 | `llm` | 4/8 레포. 검색량 높음 |
| P1 | `developer-tools` | 2/8. GitHub Explore 카테고리와 일치 |
| P1 | `mcp` | 3/8. MCP 에코시스템 연관 |
| P1 | `multi-agent` | 직접적 기능 설명 |
| P1 | `agent-orchestration` | 차별화 키워드 |
| P1 | `ai-automation` | 검색 볼륨 있음 |
| P1 | `productivity` | GitHub Explore 카테고리 매핑 |
| P1 | `codex` | codex CLI 유저 유입 |
| P2 | `cursor` | cursor 유저 유입 |
| P2 | `gemini-cli` | 넓은 AI CLI 유저 대상 |
| P2 | `cli` | npm CLI 도구 카테고리 |
| P2 | `bash` | 설치 방식 명시 |
| P2 | `workflow-automation` | 자동화 검색 유입 |
| P2 | `coding-assistant` | awesome 리스트 연관 |
| P2 | `ai-workflow` | 광의 카테고리 |
| P2 | `open-source` | FOSS 커뮤니티 |

**최종 추천 20개 topics:**
```
claude-code, claude, ai-agents, anthropic, llm, mcp, developer-tools,
multi-agent, agent-orchestration, ai-automation, productivity, codex,
cursor, gemini-cli, cli, bash, workflow-automation, coding-assistant,
ai-workflow, open-source
```

### 2.3 README SEO 구조

GitHub 풀텍스트 인덱스는 README의 H1~H3, 첫 500자를 중점 가중치로 처리한다.

```markdown
# DOMANGCHA — 16-Agent Claude Code Crew

> AI-powered multi-agent automation for Claude Code | 
> 16 specialized agents | auto-install | npx domangcha

[![npm version](https://img.shields.io/npm/v/domangcha)](https://npmjs.com/package/domangcha)
[![GitHub stars](https://img.shields.io/github/stars/DoCoreTeam/domangcha)](...)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](...)
```

**필수 키워드 (README 상단에 자연스럽게 포함):**
- claude-code, Claude Code, multi-agent, agent orchestration
- AI automation, developer productivity, CLAUDE.md
- npx domangcha, curl install
- 16 agents, CEO pipeline, agent crew

### 2.4 Description 전략

GitHub repo description (160자 제한):
```
16-agent AI crew for Claude Code. Auto-installs on clone/pull. 
CEO pipeline: research → build → review → ship. npx domangcha
```

---

## 3. npm 패키지 구조 설계

### 3.1 package.json 설계

```json
{
  "name": "domangcha",
  "version": "2.0.12",
  "description": "16-agent AI automation crew for Claude Code — CEO pipeline: plan → research → build → review → ship",
  "keywords": [
    "claude-code", "claude", "ai-agents", "anthropic", "llm",
    "multi-agent", "agent-orchestration", "ai-automation",
    "developer-tools", "cli", "mcp", "productivity",
    "codex", "cursor", "gemini-cli", "workflow-automation"
  ],
  "bin": {
    "domangcha": "./bin/domangcha.js"
  },
  "engines": {
    "node": ">=18"
  },
  "repository": {
    "type": "git",
    "url": "git+https://github.com/DoCoreTeam/domangcha.git"
  },
  "homepage": "https://github.com/DoCoreTeam/domangcha#readme",
  "bugs": {
    "url": "https://github.com/DoCoreTeam/domangcha/issues"
  },
  "license": "MIT",
  "files": [
    "bin/",
    "domangcha/",
    "README.md",
    "LICENSE"
  ]
}
```

### 3.2 bin/domangcha.js 동작 설계

```
npx domangcha         → 대화형 설치 (install.sh 실행)
npx domangcha install → 직접 설치
npx domangcha version → 버전 출력
npx domangcha update  → 업데이트
```

실행 흐름:
```
bin/domangcha.js
  └── spawn: bash domangcha/install.sh
        └── ~/.claude/ 에 agents/, skills/, CLAUDE.md 복사
```

### 3.3 npm 자동 배포 워크플로

트리거: `git tag v2.0.12 && git push --tags`

`.github/workflows/publish.yml`:
```yaml
on:
  push:
    tags: ['v*']
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'
      - run: npm publish --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

---

## 4. .github/ 폴더 구조 상세

```
.github/
├── ISSUE_TEMPLATE/
│   ├── bug_report.md          ← 버그 리포트 템플릿
│   └── feature_request.md     ← 기능 요청 템플릿
├── PULL_REQUEST_TEMPLATE.md   ← PR 기여 가이드
├── FUNDING.yml                ← GitHub Sponsors 설정
├── workflows/
│   ├── publish.yml            ← npm auto-publish (tag push)
│   └── ci.yml                 ← (선택) install.sh 문법 검증
└── CODEOWNERS                 ← (선택) @DoCoreTeam/maintainers
```

**FUNDING.yml:**
```yaml
github: [dohyeon-kim]
custom: ['https://buymeacoffee.com/docore']
```

---

## 5. 소셜 배포 채널 맵

### 5.1 채널별 목적 및 포스팅 전략

```
┌─────────────────────────────────────────────────────┐
│                  DOMANGCHA LAUNCH                   │
└──────────────┬──────────────────────────────────────┘
               │
    ┌──────────┼──────────┬──────────────┬────────────┐
    ▼          ▼          ▼              ▼            ▼
  Reddit      X/Twitter  Dev.to         LinkedIn     Velog
  r/ClaudeAI  #ClaudeCode Tutorial      B2B Dev     한국 개발자
  r/MachineLearning     Article         Network     커뮤니티
  r/programming
  HN Show
```

### 5.2 채널별 콘텐츠 전략

| 채널 | 포맷 | 핵심 훅 | 타이밍 |
|------|------|---------|-------|
| Reddit r/ClaudeAI | 텍스트 + GIF | "curl 한 줄로 16개 AI 에이전트 설치" | 론치 Day 1 |
| HN Show HN | 텍스트 | "Show HN: DOMANGCHA – 16-agent Claude Code crew" | 한국 시간 오후 2-4시 (HN 골든타임) |
| X/Twitter | 스레드 3-5트윗 | 데모 GIF + npx 명령어 | Day 1 동시 |
| Dev.to | 튜토리얼 기사 | "I built a 16-agent system for Claude Code" | Day 2-3 |
| LinkedIn | 기술 설명 포스트 | 팀 생산성 메트릭 | Day 3-5 |
| Velog | 한국어 상세 설명 | 도입 경위 + 사용법 | Week 1 |

### 5.3 Awesome 리스트 제출 전략

DOMANGCHA가 노출되어야 할 awesome 리스트:
1. `hesreallyhim/awesome-claude-code` (41k stars) — PR 제출
2. `hesreallyhim/a-list-of-claude-code-agents` — 에이전트 목록 등재
3. `ComposioHQ/awesome-claude-skills` — 스킬 목록 등재
4. `sickn33/antigravity-awesome-skills` — 광범위 도구 목록

제출 타이밍: GitHub star 100+ 달성 후 (신뢰도 기준선)

### 5.4 바이럴 트리거 설계

GitHub Trending 진입 조건: 24시간 내 star 속도 급증

트리거 방법:
1. HN Show HN 포스팅 → 해커뉴스 트래픽 → star 폭발
2. Reddit r/ClaudeAI (40만 구독자) → 유기적 확산
3. X/Twitter Claude Code 커뮤니티 (influencer 리트윗 유도)

---

## 6. 전체 아키텍처 다이어그램

```
[GitHub Explore Topics]──────── 20 topics 설정
         │
         ▼
[User discovers DOMANGCHA]
         │
    ┌────┴────────────────────┐
    │                         │
    ▼                         ▼
[README]                  [npm page]
Install via curl          npx domangcha
    │                         │
    ▼                         ▼
[~/.claude/ setup]        [bin/domangcha.js]
agents/ skills/            → install.sh 실행
CLAUDE.md                      │
    │                          │
    └──────────┬───────────────┘
               ▼
      [Claude Code 활성화]
      /ceo "업무" 명령 사용
               │
               ▼
      [사용자 → star → 공유]
      GitHub Trending 진입
```
