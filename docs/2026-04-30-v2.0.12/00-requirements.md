# DOMANGCHA GitHub 디스커버리 최적화 — 요구사항

**프로젝트**: DOMANGCHA GitHub Discovery Optimization  
**버전**: v2.0.12  
**날짜**: 2026-04-30  
**상태**: 기획 단계

---

## 1. 기능 요구사항

### 1.1 GitHub 메타데이터 최적화

#### 1.1.1 Repository Topics (20개)
GitHub 레포지토리에 다음 20개 topic 설정:
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

**책임**: CLI 명령 또는 스크립트로 자동 설정

#### 1.1.2 Repository Description
GitHub 레포지토리 description:

```
🚗💨 DOMANGCHA — AI getaway car from development hell. 16-agent Claude Code crew for AI development automation.
```

**길이**: 140자 이내 (120자)  
**포함 키워드**: claude-code, ai-agents, automation, getaway

---

### 1.2 package.json 재작성

#### 1.2.1 메타데이터
| 필드 | 값 | 비고 |
|------|-----|------|
| `name` | `domangcha` | npm 검색 가능성 |
| `version` | `2.0.12` | VERSION 파일과 일치 |
| `description` | "🚗💨 DOMANGCHA — AI getaway..." | 140자 이내 |
| `private` | `false` | npm 등록 가능 |
| `license` | `MIT` | 오픈소스 |
| `author` | "DOCORE (Michael Dohyeon Kim)" | 제작자 정보 |
| `repository` | URL | GitHub URL |
| `bugs` | URL | GitHub issues 링크 |
| `homepage` | GitHub URL | |

#### 1.2.2 bin 엔트리
```json
"bin": {
  "domangcha": "./bin/domangcha.js"
}
```

**실행 가능**: `npx domangcha`로 CLI 실행 가능해야 함

#### 1.2.3 Keywords (최대 20개)
도메인별 키워드:
- AI & LLM: claude, llm, anthropic, ai-agents, agentic-ai
- Development: automation, developer-tools, devtools, code-generation
- Architecture: multi-agent, workflow-automation, orchestration
- Technologies: bash, shell, cli, mcp
- Business: productivity, open-source, ai-automation

---

### 1.3 GitHub 기본 파일 (.github/ 폴더)

#### 1.3.1 CONTRIBUTING.md
포함 내용:
- 프로젝트 소개 (1문단)
- 기여 가능 영역 (Triage, Bug Report, Documentation, Code)
- 개발 환경 셋업 (3단계)
- PR 프로세스 (5단계)
- 코드 스타일 가이드 요약
- 문의처 (이슈, 토론, 이메일)

**목표**: 신규 기여자의 온보딩 5분 이내 완료

#### 1.3.2 FUNDING.yml
포함 내용:
```yaml
github: [DoCoreTeam]
custom:
  - "https://buymeacoffee.com/docore"
```

#### 1.3.3 Issue Template 2종

**1.3.3.1 Bug Report** (`bug_report.yml`)
- 제목 자동 채우기: `[BUG] ...`
- 버전, OS, 명령어, 예상 vs 실제 동작
- 로그 attachment 섹션

**1.3.3.2 Feature Request** (`feature_request.yml`)
- 제목 자동 채우기: `[FEATURE] ...`
- 배경, 제안, 대안
- 추가 컨텍스트

#### 1.3.4 Pull Request Template
포함 내용:
- PR 타입 체크박스 (feat, fix, refactor, docs, test)
- Related Issue 링크
- 변경 사항 요약
- 테스트 계획
- 체크리스트 (스타일, 테스트, 문서)

---

### 1.4 소셜 미디어 포스팅 템플릿 (5종)

#### 1.4.1 X (Twitter)
**길이**: 280자  
**톤**: 장난스럽고 기술적  
**포함**: 해시태그 3-5개, 이모지 1-2개

예시 구조:
```
🚗💨 DOMANGCHA v2.0.12 is live!

AI-powered dev automation with 16 agents. From chaos to ✨ in one command.

- Auto-install on git clone
- Session version check
- Pipeline enforcement

npx domangcha

#Claude #AI #DevTools #Automation #OpenSource
```

#### 1.4.2 LinkedIn
**길이**: 1300자 이내  
**톤**: 전문적이고 통찰력 있음  
**포함**: CTA, 3-4개 섹션

구조:
- Opening hook: 개발자의 고통점
- DOMANGCHA 소개: 16-agent 크루 역할
- Key features: 3-4개 기능
- CTA: "Try it today"

#### 1.4.3 Dev.to
**길이**: 800-1500자  
**포맷**: Markdown  
**포함**: 
- 프로젝트 소개
- 주요 기능 (코드 스니펫 선택)
- 설치 방법
- 빠른 시작
- 기여 권유

#### 1.4.4 Reddit (r/webdev, r/coding, r/OpenSource)
**길이**: 300-500자  
**톤**: 커뮤니티 친화적  
**포함**:
- 프로젝트 설명
- 주요 특징
- GitHub 링크
- "Feedback 환영" 메시지

#### 1.4.5 Velog (한국)
**길이**: 1000-1500자  
**포맷**: Markdown (한국어)  
**포함**:
- 프로젝트 배경 (개발자 고통점)
- DOMANGCHA란 무엇인가
- 16개 에이전트 역할
- 설치 및 사용
- 기여 방법

---

### 1.5 README SEO 최적화

#### 1.5.1 구조
1. **Hero Section** (H1): `# DOMANGCHA 🚗💨`
2. **Subtitle**: "AI getaway car from development hell"
3. **Key Metrics**: Stats/badges (downloads, stars, version)
4. **Quick Start** (H2): 3줄 설치 + 1줄 실행
5. **What is DOMANGCHA?** (H2): 2-3단락
6. **Key Features** (H2): 16개 에이전트 개요
7. **Agents** (H2): 에이전트별 설명 (표 또는 리스트)
8. **Getting Started** (H2): 단계별 가이드
9. **Architecture** (H2): 시스템 다이어그램 또는 텍스트
10. **Contributing** (H2): 링크
11. **License** (H2): MIT

#### 1.5.2 검색 키워드 (자연스럽게 삽입)
- H2/H3에 포함될 키워드:
  - "AI automation"
  - "16-agent system"
  - "Claude Code"
  - "workflow automation"
  - "developer productivity"
  - "multi-agent architecture"
  - "open-source tools"

#### 1.5.3 SEO 메타
- `<title>`: "DOMANGCHA — AI Dev Automation with 16-Agent Claude Code Crew"
- `<meta name="description">`: 160자 이내, 주요 키워드 포함

---

## 2. 비기능 요구사항

### 2.1 npm 패키지
- [ ] `npm pack --dry-run` 성공 (파일 리스트 정상 출력)
- [ ] `npx domangcha` 실행 가능 (bin 엔트리 정상)
- [ ] Private = false (공개 패키지)
- [ ] License 명시

### 2.2 포스팅 템플릿
- [ ] 각 템플릿은 "복붙 가능한" 완성본
- [ ] 플레이스홀더 최소화 (필요시만 제공)
- [ ] 플랫폼별 최적 길이 준수

### 2.3 파일 크기
- [ ] 개별 파일 300줄 미만 (관례상 200-250줄 권장)
- [ ] 템플릿 파일: 100-150줄

### 2.4 스크립트
- [ ] bash -n install.sh 통과 (문법 체크)
- [ ] 에러 처리 포함

---

## 3. 제약사항

### 3.1 기술
- npm v8+, Node.js 18+
- GitHub API 버전: v3

### 3.2 비용
- GitHub API 무료 레이트 한계 내 (60 req/hr, auth 후 5000 req/hr)
- npm registry 공개 패키지 (무료)

### 3.3 외부 의존성
- 최소화 (마크다운 생성에만 필요한 라이브러리)

---

## 4. 성공 기준

1. **GitHub 메타데이터**: Topics 20개, Description 설정 완료
2. **package.json**: 유효한 npm 패키지 (npx 실행 가능)
3. **.github/ 파일**: 5개 파일 생성 (CONTRIBUTING.md, FUNDING.yml, 2개 템플릿, PR 템플릿)
4. **포스팅 템플릿**: 5종 완성 (X, LinkedIn, Dev.to, Reddit, Velog)
5. **README**: SEO 키워드 자연스럽게 포함, 구조 명확
6. **테스트**: npm pack, bash 문법, GitHub API 호출 성공

---

## 5. 출시 기준

모든 기능 요구사항 + 비기능 요구사항 충족 후:
- DC-QA, DC-SEC, DC-REV 통과
- 사용자 최종 승인

