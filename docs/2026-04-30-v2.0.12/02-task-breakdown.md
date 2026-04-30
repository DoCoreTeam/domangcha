# 02-task-breakdown.md — GitHub Discovery Optimization Task Breakdown
# DOMANGCHA v2.0.12 — 2026-04-30

## 우선순위 체계
- **P0 (즉시)**: 오늘 오전 — 검색 노출에 직접 영향, 지금 당장 안 하면 손해
- **P1 (오늘)**: 오늘 오후 — 론치 품질 완성, 사용자 첫인상 결정
- **P2 (이번 주)**: 3-7일 내 — 지속 성장 인프라

---

## P0 — 즉시 (오늘 오전)

### P0-1: GitHub Topics 설정 스크립트
**목적:** GitHub Explore에서 20개 topics로 노출 극대화

**액션:**
```bash
gh api repos/DoCoreTeam/domangcha \
  --method PATCH \
  --field topics[]='claude-code' \
  --field topics[]='claude' \
  --field topics[]='ai-agents' \
  --field topics[]='anthropic' \
  --field topics[]='llm' \
  --field topics[]='mcp' \
  --field topics[]='developer-tools' \
  --field topics[]='multi-agent' \
  --field topics[]='agent-orchestration' \
  --field topics[]='ai-automation' \
  --field topics[]='productivity' \
  --field topics[]='codex' \
  --field topics[]='cursor' \
  --field topics[]='gemini-cli' \
  --field topics[]='cli' \
  --field topics[]='bash' \
  --field topics[]='workflow-automation' \
  --field topics[]='coding-assistant' \
  --field topics[]='ai-workflow' \
  --field topics[]='open-source'
```

**완료 기준:** `gh api repos/DoCoreTeam/domangcha --jq '.topics | length'` → 20

---

### P0-2: package.json 재작성
**목적:** npm 패키지로 등록 가능한 구조로 변경 + npx 지원

**현재:** `{"name": "docore", "version": "1.0.0", "private": true}`

**변경 후:**
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
  "main": "./bin/domangcha.js",
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
  ],
  "scripts": {
    "test": "bash -n domangcha/install.sh && echo 'install.sh syntax OK'"
  }
}
```

**완료 기준:** `npm pack --dry-run` 실행 시 에러 없음

---

### P0-3: README SEO 키워드 최적화
**목적:** GitHub 풀텍스트 검색 + 첫인상 전환율 향상

**필수 변경 사항:**

1. **H1 타이틀 변경:**
   ```markdown
   # DOMANGCHA — 16-Agent Claude Code Crew
   ```

2. **뱃지 라인 추가 (H1 바로 아래):**
   ```markdown
   [![npm version](https://img.shields.io/npm/v/domangcha?style=flat-square)](https://npmjs.com/package/domangcha)
   [![GitHub stars](https://img.shields.io/github/stars/DoCoreTeam/domangcha?style=flat-square)](https://github.com/DoCoreTeam/domangcha)
   [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
   [![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-blue?style=flat-square)](https://claude.ai/code)
   ```

3. **tagline / 한 줄 설명 (뱃지 다음):**
   ```markdown
   > AI-powered multi-agent automation for Claude Code.  
   > 16 specialized agents | CEO pipeline | auto-installs on git clone
   ```

4. **Quick Install 섹션 (상단 1/3 내):**
   ```markdown
   ## Quick Install
   
   ```bash
   # Option 1: curl (recommended)
   curl -fsSL https://raw.githubusercontent.com/DoCoreTeam/domangcha/main/domangcha/install.sh | bash
   
   # Option 2: npx
   npx domangcha
   ```
   ```

5. **키워드 자연 삽입 (Features 섹션):**
   - "Claude Code multi-agent orchestration"
   - "16 specialized AI agents"
   - "CEO pipeline: research → build → review → ship"
   - "CLAUDE.md auto-configuration"

**완료 기준:** README 상단 500자 이내에 `claude-code`, `multi-agent`, `npx`, `curl install` 키워드 포함

---

## P1 — 오늘 오후

### P1-1: bin/domangcha.js 작성
**목적:** `npx domangcha` 실행 시 install.sh 실행

**파일:** `/bin/domangcha.js`
```javascript
#!/usr/bin/env node
'use strict';

const { execSync, spawnSync } = require('child_process');
const path = require('path');
const os = require('os');

const args = process.argv.slice(2);
const command = args[0] || 'install';

const INSTALL_URL = 'https://raw.githubusercontent.com/DoCoreTeam/domangcha/main/domangcha/install.sh';
const VERSION = require('../package.json').version;

switch (command) {
  case 'version':
  case '-v':
  case '--version':
    console.log(`domangcha v${VERSION}`);
    break;

  case 'install':
  default:
    console.log(`Installing DOMANGCHA v${VERSION}...`);
    const result = spawnSync(
      'bash',
      ['-c', `curl -fsSL ${INSTALL_URL} | bash`],
      { stdio: 'inherit', shell: false }
    );
    process.exit(result.status || 0);
}
```

**완료 기준:** `node bin/domangcha.js version` → `domangcha v2.0.12`

---

### P1-2: .github/ISSUE_TEMPLATE/ 생성

**bug_report.md:**
```markdown
---
name: Bug report
about: Create a report to help us improve DOMANGCHA
title: '[BUG] '
labels: bug
assignees: ''
---

**Describe the bug**
...

**Claude Code version**
Run: `claude --version`

**DOMANGCHA version**
Check: `cat ~/.claude/domangcha/VERSION`

**Steps to reproduce**
...
```

**feature_request.md:**
```markdown
---
name: Feature request
about: Suggest an idea for DOMANGCHA
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

**Which agent should handle this?**
(DC-BIZ / DC-RES / DC-DEV-* / DC-QA / etc.)

**Describe the feature**
...
```

**완료 기준:** GitHub Issues 탭에서 "New Issue" 클릭 시 템플릿 선택 UI 노출

---

### P1-3: .github/PULL_REQUEST_TEMPLATE.md 생성

```markdown
## Summary
- [ ] What does this PR do?

## Type of Change
- [ ] Bug fix
- [ ] New agent / skill
- [ ] Documentation
- [ ] Other

## Tested With
- Claude Code version:
- Agent affected:

## Checklist
- [ ] Tested install.sh from scratch
- [ ] No secrets or API keys included
- [ ] CLAUDE.md updated if needed
```

**완료 기준:** PR 생성 시 템플릿 자동 로드

---

### P1-4: 소셜 포스팅 템플릿 작성
**목적:** 론치 당일 즉시 배포 가능한 완성본 템플릿

작성할 파일: `docs/2026-04-30-v2.0.12/launch-posts/`

| 파일 | 채널 | 길이 |
|------|------|------|
| `post-reddit-claudeai.md` | r/ClaudeAI | 300-500자 |
| `post-hn-show.md` | Hacker News Show HN | 200자 + URL |
| `post-twitter-thread.md` | X/Twitter | 5트윗 스레드 |
| `post-devto.md` | Dev.to | 800-1200자 튜토리얼 |

**완료 기준:** 각 포스트 파일 존재 + 실제 npx 명령어/GitHub URL 포함

---

### P1-5: GitHub repo description 업데이트

```bash
gh api repos/DoCoreTeam/domangcha \
  --method PATCH \
  --field description='16-agent AI crew for Claude Code. CEO pipeline: research → build → review → ship. curl install + npx domangcha' \
  --field homepage='https://github.com/DoCoreTeam/domangcha'
```

**완료 기준:** GitHub 레포 메인 페이지에서 description 표시 확인

---

## P2 — 이번 주 (3-7일 내)

### P2-1: .github/FUNDING.yml
**목적:** GitHub Sponsors 버튼 활성화 → 신뢰도 + 커뮤니티 신호

```yaml
# .github/FUNDING.yml
github: [dohyeon-kim]
custom:
  - 'https://buymeacoffee.com/docore'
```

**완료 기준:** GitHub 레포 상단에 "Sponsor" 버튼 노출

---

### P2-2: .github/workflows/publish.yml — npm auto-publish
**목적:** `git tag v2.0.13 && git push --tags` 로 npm 자동 배포

```yaml
name: Publish to npm

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'
      
      - name: Verify package name
        run: node -e "const p=require('./package.json'); if(p.name!=='domangcha') process.exit(1);"
      
      - name: Publish
        run: npm publish --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

**사전 조건:** npmjs.com에서 `domangcha` 패키지 이름 사전 등록, `NPM_TOKEN` GitHub Secret 등록

**완료 기준:** tag push 후 npmjs.com에서 패키지 확인

---

### P2-3: npm 최초 수동 배포
**목적:** `npx domangcha` 동작 확인 + npmjs.com 검색 노출 시작

```bash
# 사전 체크
npm whoami
npm pack --dry-run

# 배포
npm publish --access public
```

**완료 기준:** `npx domangcha version` 출력 확인

---

### P2-4: Awesome 리스트 PR 제출
**목적:** 41k stars 레포에서 backlink + 발견 가능성 증가

대상:
1. `hesreallyhim/awesome-claude-code` — "Agent Orchestrators" 섹션에 DOMANGCHA 추가
2. `hesreallyhim/a-list-of-claude-code-agents` — 16개 에이전트 목록 추가

**사전 조건:** GitHub star 100+ (신뢰도 기준선)

**완료 기준:** PR 머지 또는 승인 대기 중

---

### P2-5: .github/workflows/ci.yml — 기본 CI
**목적:** 커뮤니티 기여자 신뢰 + GitHub Actions 배지

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate install.sh
        run: bash -n domangcha/install.sh
      - name: Validate package.json
        run: node -e "require('./package.json')"
```

**완료 기준:** 커밋 푸시 시 green check 확인

---

## 전체 타임라인

```
오늘 오전 (2시간)
├── P0-1: GitHub topics 20개 설정 (5분)
├── P0-2: package.json 재작성 (15분)
└── P0-3: README SEO 최적화 (40분)

오늘 오후 (3시간)
├── P1-1: bin/domangcha.js 작성 (20분)
├── P1-2: .github/ISSUE_TEMPLATE/ 생성 (20분)
├── P1-3: .github/PULL_REQUEST_TEMPLATE.md (10분)
├── P1-4: 소셜 포스팅 템플릿 4개 작성 (60분)
└── P1-5: GitHub description 업데이트 (5분)

이번 주 내
├── P2-1: FUNDING.yml (10분)
├── P2-2: publish.yml 워크플로 (20분)
├── P2-3: npm 최초 수동 배포 (30분)
├── P2-4: Awesome 리스트 PR (30분 × 2)
└── P2-5: ci.yml 기본 CI (15분)
```

---

## 의존성 맵

```
P0-2 (package.json) ──→ P1-1 (bin/domangcha.js) ──→ P2-3 (npm publish)
                                                          │
                                                          ▼
                                                     P2-2 (auto-publish)

P0-3 (README) ──→ P1-4 (소셜 포스팅) ──→ [론치]

P1-2 + P1-3 ──→ 독립 실행 가능

P2-1 (FUNDING) ──→ 독립 실행 가능
P2-4 (Awesome PR) ──→ P2-3 완료 후 (npmjs.com 확인 링크 필요)
```
