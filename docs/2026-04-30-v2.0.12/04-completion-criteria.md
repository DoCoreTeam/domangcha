# DOMANGCHA GitHub 디스커버리 최적화 — 완료 조건

**프로젝트**: DOMANGCHA GitHub Discovery Optimization  
**버전**: v2.0.12  
**날짜**: 2026-04-30  
**상태**: 기획 단계

---

## 1. 완료 조건 (Completion Criteria)

모든 항목이 완료되어야 GATE 진입 가능:

### 1.1 GitHub 메타데이터

#### 1.1.1 Topics 설정
- [ ] Repository settings → Topics 섹션에서 20개 topic 확인
  - `claude-code`
  - `ai-agents`
  - `anthropic`
  - `llm`
  - `automation`
  - `developer-tools`
  - `cli`
  - `ai`
  - `multi-agent`
  - `bash`
  - `claude`
  - `mcp`
  - `productivity`
  - `devtools`
  - `agentic-ai`
  - `code-generation`
  - `workflow-automation`
  - `open-source`
  - `ai-automation`
  - `shell`

**검증 방법**:
```bash
# GitHub Web 확인
# Settings > Topics 페이지에서 위 20개 모두 표시됨

# 또는 GitHub CLI (gh) 사용
gh repo view DoCoreTeam/domangcha --json repositoryTopics
```

#### 1.1.2 Description 설정
- [ ] Repository description 확인:
  ```
  🚗💨 DOMANGCHA — AI getaway car from development hell. 16-agent Claude Code crew for AI development automation.
  ```

**검증 방법**:
```bash
gh repo view DoCoreTeam/domangcha --json description
```

---

### 1.2 package.json 수정

#### 1.2.1 메타데이터 필드
```json
{
  "name": "domangcha",
  "version": "2.0.12",
  "description": "🚗💨 DOMANGCHA — AI getaway car from development hell. 16-agent Claude Code crew for AI development automation.",
  "private": false,
  "license": "MIT",
  "author": "DOCORE (Michael Dohyeon Kim)",
  "repository": {
    "type": "git",
    "url": "https://github.com/DoCoreTeam/domangcha.git"
  },
  "bugs": {
    "url": "https://github.com/DoCoreTeam/domangcha/issues"
  },
  "homepage": "https://github.com/DoCoreTeam/domangcha",
  "bin": {
    "domangcha": "./bin/domangcha.js"
  },
  "keywords": [
    "claude", "llm", "anthropic", "ai-agents", "agentic-ai",
    "automation", "developer-tools", "devtools", "code-generation",
    "multi-agent", "workflow-automation", "orchestration",
    "bash", "shell", "cli", "mcp",
    "productivity", "open-source", "ai-automation"
  ]
}
```

**검증**:
- [ ] JSON 유효성: `jq . package.json` 오류 없음
- [ ] `"name": "domangcha"` 확인
- [ ] `"private": false` 확인
- [ ] `"bin"` 엔트리 존재 확인

---

### 1.3 .github/ 폴더 파일 생성

#### 1.3.1 CONTRIBUTING.md
파일 경로: `.github/CONTRIBUTING.md`

**포함 내용 체크리스트**:
- [ ] 프로젝트 소개 (1-2문단)
- [ ] 기여 가능 영역:
  - [ ] Triage (이슈 정분류)
  - [ ] Bug Report
  - [ ] Documentation
  - [ ] Code
- [ ] 개발 환경 셋업 (3단계)
  - [ ] Clone & Install
  - [ ] Dependencies
  - [ ] Local Testing
- [ ] PR 프로세스 (5단계)
  - [ ] Fork repository
  - [ ] Create feature branch
  - [ ] Make changes
  - [ ] Test locally
  - [ ] Push & Create PR
- [ ] 코드 스타일 가이드 요약
  - [ ] Linting/formatting 도구
  - [ ] 테스트 커버리지 최소 기준
  - [ ] Commit 메시지 규칙
- [ ] 문의처
  - [ ] GitHub Issues
  - [ ] GitHub Discussions (있으면)
  - [ ] Email

**검증**:
```bash
wc -l .github/CONTRIBUTING.md  # 300줄 미만
grep -q "Fork\|git clone\|npm install" .github/CONTRIBUTING.md
```

#### 1.3.2 FUNDING.yml
파일 경로: `.github/FUNDING.yml`

**포함 내용 체크리스트**:
- [ ] github: `[DoCoreTeam]` 또는 개별 username
- [ ] custom: sponsorship 링크 (예: Buy Me A Coffee)

**파일 예시**:
```yaml
github: [DoCoreTeam]
custom:
  - https://buymeacoffee.com/docore
```

**검증**:
```bash
cat .github/FUNDING.yml
# "github:" 와 "custom:" 존재 확인
```

#### 1.3.3 Issue Template: Bug Report
파일 경로: `.github/ISSUE_TEMPLATE/bug_report.yml`

**포함 내용 체크리스트**:
- [ ] Name: "Bug Report" 또는 유사
- [ ] Description: 간단한 설명
- [ ] Title prefix: `[BUG]`
- [ ] Body fields:
  - [ ] Version (required)
  - [ ] OS (required)
  - [ ] Command (required)
  - [ ] Expected Behavior
  - [ ] Actual Behavior
  - [ ] Logs/Screenshots (optional)

**검증**:
```bash
cat .github/ISSUE_TEMPLATE/bug_report.yml | grep -E "name:|title:|description:"
```

#### 1.3.4 Issue Template: Feature Request
파일 경로: `.github/ISSUE_TEMPLATE/feature_request.yml`

**포함 내용 체크리스트**:
- [ ] Name: "Feature Request" 또는 유사
- [ ] Description: 간단한 설명
- [ ] Title prefix: `[FEATURE]`
- [ ] Body fields:
  - [ ] Background/Context
  - [ ] Proposed Solution
  - [ ] Alternatives (optional)
  - [ ] Additional Context (optional)

**검증**:
```bash
cat .github/ISSUE_TEMPLATE/feature_request.yml | grep -E "name:|title:"
```

#### 1.3.5 Pull Request Template
파일 경로: `.github/pull_request_template.md`

**포함 내용 체크리스트**:
- [ ] PR 타입 (feat, fix, refactor, docs, test)
  ```markdown
  - [ ] feat
  - [ ] fix
  - [ ] refactor
  - [ ] docs
  - [ ] test
  ```
- [ ] Related Issue 링크 필드
- [ ] 변경 사항 요약
- [ ] 테스트 계획
- [ ] Checklist:
  - [ ] Code follows style guide
  - [ ] Tests added/updated
  - [ ] Documentation updated
  - [ ] No breaking changes

**검증**:
```bash
grep -q "PR type\|Related Issue\|Checklist" .github/pull_request_template.md
wc -l .github/pull_request_template.md  # 150줄 미만
```

---

### 1.4 소셜 포스팅 템플릿 (5종)

파일 저장 위치: `docs/social-templates/` 또는 `SOCIAL.md`

#### 1.4.1 X (Twitter) 포스트
파일: `X_post.md`

**포함 내용 체크리스트**:
- [ ] 본문 280자 이내
- [ ] 이모지 1-2개
- [ ] 해시태그 3-5개
- [ ] Call-to-action (설치 링크 또는 명령)
- [ ] 완성된 텍스트 (복붙 가능)

**예시**:
```
🚗💨 DOMANGCHA v2.0.12 is live!

AI-powered dev automation with 16 agents. From chaos to ✨ in one command.

- Auto-install on git clone
- Session version check
- Pipeline enforcement

npx domangcha

#Claude #AI #DevTools #Automation #OpenSource
```

**검증**:
```bash
wc -c social-templates/X_post.md  # 280 바이트 이하
grep -E "#|emoji|domangcha" social-templates/X_post.md
```

#### 1.4.2 LinkedIn 포스트
파일: `LinkedIn_post.md`

**포함 내용 체크리스트**:
- [ ] Opening hook (개발자 고통점)
- [ ] DOMANGCHA 소개 (16-agent 시스템)
- [ ] 주요 기능 (3-4개)
- [ ] Call-to-action ("Try it today", "Learn more")
- [ ] 1300자 이내
- [ ] 전문적 톤
- [ ] 완성된 텍스트

**검증**:
```bash
wc -w social-templates/LinkedIn_post.md  # ~200-250 단어
grep -q "Try\|Learn\|agent\|automation" social-templates/LinkedIn_post.md
```

#### 1.4.3 Dev.to 포스트
파일: `DevTo_post.md`

**포함 내용 체크리스트**:
- [ ] Markdown 포맷
- [ ] Front matter (선택):
  ```yaml
  ---
  title: "DOMANGCHA v2.0.12 — AI Dev Automation"
  tags: claude, ai, automation, devtools, opensource
  ---
  ```
- [ ] 섹션:
  - [ ] 프로젝트 소개
  - [ ] 주요 기능 (코드 스니펫 선택)
  - [ ] 설치 방법
  - [ ] 빠른 시작
  - [ ] 기여 권유
- [ ] 800-1500자
- [ ] 완성된 텍스트

**검증**:
```bash
wc -w social-templates/DevTo_post.md  # 400-750 단어
grep -E "^##|^###|npm install|npx domangcha" social-templates/DevTo_post.md
```

#### 1.4.4 Reddit 포스트
파일: `Reddit_post.md`

**포함 내용 체크리스트**:
- [ ] Subreddit 대상 명시 (r/webdev, r/coding, r/OpenSource)
- [ ] 제목 (80자 이내)
- [ ] 본문 (300-500자)
- [ ] 프로젝트 설명
- [ ] 주요 특징 (bullet points)
- [ ] GitHub 링크
- [ ] Feedback 환영 메시지
- [ ] 커뮤니티 친화적 톤

**검증**:
```bash
wc -w social-templates/Reddit_post.md  # 150-250 단어
grep -q "r/\|GitHub\|feedback\|link" social-templates/Reddit_post.md
```

#### 1.4.5 Velog 포스트 (한국)
파일: `Velog_post.md`

**포함 내용 체크리스트**:
- [ ] 한국어 텍스트
- [ ] 마크다운 포맷
- [ ] Front matter:
  ```yaml
  ---
  title: "DOMANGCHA v2.0.12 — 개발 자동화의 미래"
  tags: [claude, ai, 자동화, 개발도구]
  ---
  ```
- [ ] 섹션:
  - [ ] 개발자 고통점
  - [ ] DOMANGCHA란 무엇인가
  - [ ] 16개 에이전트 역할
  - [ ] 설치 및 사용
  - [ ] 기여 방법
- [ ] 1000-1500자
- [ ] 한국 개발자 커뮤니티 친화적

**검증**:
```bash
file social-templates/Velog_post.md | grep UTF-8  # 한글 인코딩 확인
wc -w social-templates/Velog_post.md  # 500-750 단어
grep -E "^##|^###|npm|깃허브" social-templates/Velog_post.md
```

---

### 1.5 npm 패키지 테스트

#### 1.5.1 npm pack 실행
```bash
npm pack --dry-run
```

**검증 체크리스트**:
- [ ] 명령 성공 (exit code 0)
- [ ] 파일 리스트 출력
- [ ] 필수 파일 포함:
  - [ ] package.json
  - [ ] bin/domangcha.js (또는 해당 파일)
  - [ ] README.md
  - [ ] LICENSE

#### 1.5.2 npx 실행 가능성
```bash
# Local test
npm link
npx domangcha --version
```

**검증 체크리스트**:
- [ ] `npx domangcha` 명령 실행 가능
- [ ] 버전 또는 헬프 메시지 출력
- [ ] 에러 없음

---

### 1.6 스크립트 문법 검사

#### 1.6.1 install.sh
```bash
bash -n install.sh
```

**검증 체크리스트**:
- [ ] exit code 0
- [ ] 문법 오류 없음
- [ ] 실행 권한: `chmod +x install.sh`

---

### 1.7 버전 일치

#### 1.7.1 파일 간 버전 일치 확인
```bash
cat domangcha/VERSION  # → 2.0.12
grep "version" package.json | grep 2.0.12  # 존재 확인
```

**검증 체크리스트**:
- [ ] domangcha/VERSION = "2.0.12"
- [ ] package.json version = "2.0.12"
- [ ] 커밋 메시지: `v2.0.12: ...`

---

## 2. 종료 기준 (Exit Criteria)

프로젝트 종료 조건:

1. **완료 조건 체크**
   - [ ] 섹션 1의 모든 항목 ✅

2. **QA 통과**
   - [ ] npm pack 성공
   - [ ] npx 실행 가능
   - [ ] 파일 크기 제약 준수 (300줄 미만)

3. **보안 검토**
   - [ ] 민감 정보 없음 (API key, 개인정보)
   - [ ] 외부 링크 유효성 확인
   - [ ] GitHub API 토큰 미포함

4. **최종 리뷰**
   - [ ] DC-QA: 모든 완료 조건 확인
   - [ ] DC-SEC: 보안 체크
   - [ ] DC-REV: 최종 승인

5. **사용자 승인**
   - [ ] 사용자 최종 OK

---

## 3. 롤백 기준 (Rollback Criteria)

문제 발생 시 롤백 가능 여부:

### 3.1 npm 레지스트리
- **상황**: npm에 등록된 후 문제 발견
- **롤백 방법**: `npm unpublish domangcha@2.0.12`
- **기간**: 72시간 이내 (npm 정책)
- **가능성**: 가능 ✅

### 3.2 GitHub 메타데이터
- **상황**: Topics, Description 변경 후 문제
- **롤백 방법**: GitHub Web 또는 `gh repo edit` 명령
- **기간**: 즉시
- **가능성**: 가능 ✅

### 3.3 GitHub 파일 (.github/)
- **상황**: PR/Issue 템플릿 변경 후 피드백 부정적
- **롤백 방법**: Git revert 또는 파일 삭제
- **기간**: 즉시
- **가능성**: 가능 ✅

### 3.4 소셜 포스팅
- **상황**: 포스팅 템플릿 내용 수정 필요
- **롤백 방법**: 저장소의 템플릿 파일 수정
- **기간**: 즉시 (게시 전), 게시 후 삭제/수정
- **가능성**: 가능 ✅

**결론**: 모든 변경 사항이 롤백 가능하므로 위험도 낮음

---

## 4. 성공 지표 (Success Metrics)

### 4.1 정량 지표
| 지표 | 목표 | 검증 방법 |
|------|------|----------|
| Topics 개수 | 20개 | GitHub repo settings |
| npm pack 파일 수 | 5개+ | npm pack --dry-run |
| .github/ 파일 | 5개 | ls -la .github/ |
| 포스팅 템플릿 | 5개 | docs/social-templates/ |
| 파일 크기 | <300줄/파일 | wc -l |

### 4.2 정성 지표
| 지표 | 목표 |
|------|------|
| README SEO | 주요 키워드 자연스럽게 포함 |
| 포스팅 톤 | 플랫폼별 최적화 (전문적/친화적/재미) |
| CONTRIBUTING 명확성 | 신규 기여자 5분 내 이해 가능 |

---

## 5. 승인 경로

```
CEO Draft → DC-QA (Functional) → DC-SEC (Security) → DC-REV (Final) → User OK
```

각 게이트별 담당자:
- **DC-QA**: 완료 조건 1.1~1.7 검증
- **DC-SEC**: 섹션 3 (보안) 검증
- **DC-REV**: 전체 검토 + 최종 승인

