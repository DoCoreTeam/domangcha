# docrew — The AI Chief Executive for Claude Code

> **EN** — You are the Founder. docrew runs your entire engineering team.
>
> **KO** — 당신은 창업자입니다. docrew가 당신의 전체 엔지니어링 팀을 운영합니다.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-docrew-blue)](https://claude.ai/code)

---

## This is not a prompt. This is an engineering team.

> 이것은 프롬프트가 아닙니다. 엔지니어링 팀입니다.

**EN** — Every serious software team needs specialists: a business strategist, researcher, database architect, frontend engineer, backend engineer, security auditor, QA lead, technical writer, DevOps engineer. Hiring all of them costs $2M+ per year.

docrew gives you all 16 — orchestrated by an AI Chief Executive who never forgets a step, never skips a gate, and always asks the right questions before writing a single line of code.

**KO** — 진지한 소프트웨어 팀에는 전문가가 필요합니다. 이들을 모두 고용하면 연간 20억 원 이상이 들고, 완벽하게 조율하는 것은 거의 불가능합니다.

docrew는 이 16명 전부를 제공합니다 — 단 하나의 명령으로, 단 한 단계도 빠뜨리지 않고, 코드 한 줄 쓰기 전에 반드시 올바른 질문을 먼저 묻는 AI 최고경영자가 오케스트레이션합니다.

```bash
# Install once. Runs everywhere. / 한 번 설치. 어디서나 실행.
curl -sSL https://raw.githubusercontent.com/DoCoreTeam/docrew/main/docore/install.sh | bash
```

```bash
# Give orders. CEO handles the rest.
/ceo "Build a SaaS app with auth, payments, and a dashboard"
/ceo "인증, 결제, 대시보드가 있는 SaaS 앱 만들어줘"
```

---

## What makes CEO different / CEO가 다른 이유

### 1. Asks before acting / 행동 전 반드시 묻습니다

**EN** — Other AI tools start writing code the moment you press Enter. CEO asks up to 12 targeted questions — one at a time, adjusting each question based on your previous answers. Tech stack, platform, codebase, done criteria, scale, auth, data models, external APIs, constraints, design direction, deployment, extra context. Only after all questions are answered does the pipeline begin.

**KO** — 다른 AI 도구는 Enter를 누르는 순간 코드를 씁니다. CEO는 최대 12개 질문을 스텝바이스텝으로 묻습니다 — 앞 답변을 반영해 다음 질문을 조정하면서. 답변이 완전히 끝난 후에만 파이프라인이 시작됩니다.

---

### 2. 16 specialists working in parallel / 16명의 전문가가 병렬로 작동합니다

**EN** — Three planners analyze your business case and scout the best open-source tools. Then specialists build simultaneously. Three evaluators audit every line for quality, security, and correctness. One optimizer tracks token usage. All coordinated. All accountable.

**KO** — 3명의 기획자가 사업 타당성을 분석하고 최적의 오픈소스 도구를 탐색합니다. 전문가들이 동시에 빌드합니다. 3명의 평가자가 모든 코드를 품질, 보안, 정확성으로 감사합니다.

---

### 3. Never ships broken code / 망가진 코드를 절대 배포하지 않습니다

**EN** — Every output passes 5 mandatory gates. 300-line files are blocked automatically. Known error patterns are caught before they reach you. If a reviewer finds a bug, the system loops back to the builder — up to 3 times — until it passes. Builder and Reviewer are always different agents.

**KO** — 모든 산출물은 5개의 필수 게이트를 통과합니다. 300줄 초과 파일은 자동 차단됩니다. 리뷰어가 버그를 발견하면 시스템이 빌더에게 돌아가 최대 3회 재작업합니다.

---

### 4. The best tools in one place / 최고의 도구들이 한 곳에

**EN** — CEO installs three elite tool systems and unifies them through CEO-* orchestrators. ECC commands are intentionally not exposed individually — access everything through CEO-* so your command list stays clean.

**KO** — CEO는 세 가지 엘리트 도구 시스템을 설치하고 CEO-* 오케스트레이터로 통합합니다. ECC 커맨드는 개별 노출하지 않아 커맨드 목록이 깔끔합니다.

---

### 5. Gets smarter every session / 매 세션마다 더 똑똑해집니다

**EN** — CEO maintains an error registry. Every mistake becomes a GATE pattern — so it never happens again. It learns your project's coding patterns as instincts. The longer you use it, the better it knows your codebase.

**KO** — CEO는 오류 레지스트리를 유지합니다. 모든 실수는 GATE 패턴으로 기록되어 반복되지 않습니다. 프로젝트 코딩 패턴을 인스팅트로 학습합니다.

---

## Quick Install / 빠른 설치

```bash
curl -sSL https://raw.githubusercontent.com/DoCoreTeam/docrew/main/docore/install.sh | bash
```

**EN** — One command installs everything. Re-running always updates to the latest version.

**KO** — 명령 하나로 모든 것이 설치됩니다. 재실행하면 항상 최신 버전으로 업데이트됩니다.

### Update / 업데이트

```bash
# Inside Claude Code / Claude Code 안에서
/ceo-update

# Terminal / 터미널에서
curl -sSL https://raw.githubusercontent.com/DoCoreTeam/docrew/main/docore/install.sh | bash
```

| What gets updated | Behavior |
|-------------------|----------|
| CEO agents, commands, SKILL.md | ✅ Always overwritten to latest |
| ECC (183 skills) | ✅ Full replacement — skills only, no individual commands |
| gstack | ✅ `git pull` (re-clone if needed) |
| Superpowers | ✅ `claude plugin update` (re-clone if needed) — **required** |
| Registries (error-registry etc.) | ⏭️ Preserved — your data stays |

| 업데이트 항목 | 동작 |
|--------------|------|
| CEO 에이전트, 커맨드, SKILL.md | ✅ 항상 최신으로 덮어씀 |
| ECC (스킬 183개) | ✅ 전체 교체 — 스킬만, 개별 커맨드 없음 |
| gstack | ✅ `git pull` (필요 시 재클론) |
| Superpowers | ✅ `plugin update` (필요 시 재클론) — **필수** |
| 레지스트리 (error-registry 등) | ⏭️ 보존 — 사용자 데이터 유지 |

### What gets installed / 설치 항목

1. **16 CEO agents** → `~/.claude/agents/`
2. **15 CEO commands** → `~/.claude/commands/` — `/ceo` + 10 CEO-* orchestrators + utility commands
3. **CEO brain** → `~/.claude/skills/ceo-system/SKILL.md`
4. **CLAUDE.md** → `~/.claude/` — activates CEO mode on every session
5. **ECC** → `~/.claude/skills/ecc:*/` — 183 skills (accessed via CEO-*)
6. **gstack** → `~/.claude/skills/gstack/`
7. **Superpowers** → via `claude plugin` or GitHub fallback (**required**)

---

## How It Works / 작동 방식

```
/ceo "Build me a SaaS" → /ceo "SaaS 만들어줘"
          │
          ▼
⓪  Q&A ── Step-by-step, up to 12 questions
           스텝바이스텝, 최대 12개 질문
           Each answer shapes the next question
           앞 답변이 다음 질문을 조정
          │
          ▼  [Answers complete / 답변 완료]
          │
① PLANNER (parallel / 병렬)
  ├── DC-BIZ  Business case & ROI
  ├── DC-RES  Tech research & patterns
  └── DC-OSS  Top 3 open-source tools
          │
          ▼  → PLAN.md
          │
② GENERATOR (parallel / 병렬)
  CORE — always runs:
  ├── DC-DEV-DB   Schema + migrations
  ├── DC-DEV-BE   API + business logic
  ├── DC-DEV-FE   UI + pages
  ├── DC-DEV-OPS  CI/CD + harness
  └── DC-DOC      API docs
  EXTENDED — added by CEO based on Q&A:
  ├── DC-DEV-MOB  Mobile (if mobile platform)
  ├── DC-DEV-INT  External APIs (if integrations needed)
  ├── DC-WRT      Marketing copy (if needed)
  └── DC-SEO      SEO (if public web)
          │
          ▼
③ CYCLE ── IMPLEMENT → REVIEW → TEST  (max 3x / 최대 3회)
          │
          ▼
④ EVALUATOR (simultaneous / 동시)
  ├── DC-QA   Functional tests & edge cases
  ├── DC-SEC  OWASP Top 10, secrets, auth, RLS
  └── DC-REV  Code quality, 300-line limit
          │
          ▼
⑤ GATE 1-5 ── All must pass / 전부 통과 필수
          │
          ▼
⑥ REPORT ── Code + tests + docs + git commit
```

---

## CEO-* Orchestrators / CEO-* 오케스트레이터

**EN** — 10 tactical commands that combine the best tools from ECC, gstack, and Superpowers simultaneously.

**KO** — ECC, gstack, Superpowers의 최고 도구들을 동시에 결합하는 10개 전술 커맨드.

| Command | What it does | Tools combined |
|---------|-------------|----------------|
| `/ceo-feature "feature"` | Full feature lifecycle | `/ceo-plan` + `/ceo-test` + `/ceo-review` + `/ceo-ship` |
| `/ceo-plan "feature"` | Q&A → BIZ → research → plan | DC-BIZ, DC-RES, DC-OSS, ECC prp-plan, gstack plan |
| `/ceo-review` | Security + quality + PR review | ECC security/code/pr-review, gstack review, DC-SEC, DC-REV |
| `/ceo-test` | TDD + unit + E2E + browser QA | ECC tdd + e2e + coverage, gstack qa, DC-QA |
| `/ceo-ship` | Gate + review + build + deploy | gstack ship + canary + qa, ECC quality-gate, DC-DEV-OPS |
| `/ceo-design "ui"` | Direction + system + components | gstack design-* × 5, ECC ui-design, DC-DEV-FE |
| `/ceo-debug "bug"` | Investigate + fix + perf + verify | gstack investigate, ECC debug + build-fix + perf-check |
| `/ceo-quality` | Health + coverage + refactor + security | gstack health, ECC quality-gate + refactor-clean, DC-QA/SEC/REV |
| `/ceo-security` | Secrets + OWASP + auth + API | ECC security-review, DC-SEC (full OWASP Top 10) |
| `/ceo-doc` | Codemaps + API docs + SEO | gstack docs, ECC update-docs + codemaps, DC-DOC, DC-SEO |
| `/ceo-learn` | Extract + evaluate + instincts + retro | gstack retro + learn, ECC learn + instinct-* + promote |

---

## 16 Agents / 16개 에이전트

| Phase | Tier | Agent | Role | Model |
|-------|------|-------|------|-------|
| PLANNER | CORE | DC-BIZ | Business Judge — is this worth building? | Opus |
| PLANNER | CORE | DC-RES | Researcher — tech, patterns, references | Haiku |
| PLANNER | CORE | DC-OSS | Open Source Scout — Top 3 libraries | Opus |
| GENERATOR | CORE | DC-DEV-FE | Frontend Developer | Sonnet |
| GENERATOR | CORE | DC-DEV-BE | Backend Developer | Sonnet |
| GENERATOR | CORE | DC-DEV-DB | Database Engineer | Sonnet |
| GENERATOR | CORE | DC-DEV-OPS | DevOps Engineer | Sonnet |
| GENERATOR | CORE | DC-DOC | Documentation Writer | Haiku |
| GENERATOR | EXTENDED | DC-DEV-MOB | Mobile Developer *(mobile platform only)* | Sonnet |
| GENERATOR | EXTENDED | DC-DEV-INT | Integration Engineer *(3rd-party APIs only)* | Sonnet |
| GENERATOR | EXTENDED | DC-WRT | Writer / Copywriter *(marketing pages only)* | Sonnet |
| GENERATOR | EXTENDED | DC-SEO | SEO / AEO / GEO Specialist *(public web only)* | Haiku |
| EVALUATOR | CORE | DC-QA | QA Engineer | Haiku |
| EVALUATOR | CORE | DC-SEC | Security Reviewer | Opus |
| EVALUATOR | CORE | DC-REV | Code Reviewer | Opus |
| SUPPORT | CORE | DC-TOK | Token Optimizer | Haiku |

---

## Full Command Reference / 전체 커맨드 레퍼런스

### CEO Commands

| Command | EN | KO |
|---------|----|----|
| `/ceo "task"` | Q&A → full 16-agent pipeline | Q&A 후 16개 에이전트 전체 파이프라인 |
| `/ceo-feature "feature"` | Full feature lifecycle | 기능 전체 라이프사이클 |
| `/ceo-plan "feature"` | Planning with Q&A | Q&A 포함 기획 |
| `/ceo-review` | All review tools combined | 모든 리뷰 도구 결합 |
| `/ceo-test` | All test tools combined | 모든 테스트 도구 결합 |
| `/ceo-ship` | Full deploy pipeline | 전체 배포 파이프라인 |
| `/ceo-design "ui"` | Full design pipeline | 전체 디자인 파이프라인 |
| `/ceo-debug "bug"` | Full debug pipeline | 전체 디버그 파이프라인 |
| `/ceo-quality` | Full quality audit | 전체 품질 감사 |
| `/ceo-security` | Full security audit | 전체 보안 감사 |
| `/ceo-doc` | Full documentation pipeline | 전체 문서화 파이프라인 |
| `/ceo-learn` | Full learning pipeline | 전체 학습 파이프라인 |
| `/ceo-update` | Update all components to latest | 모든 컴포넌트 최신 버전 업데이트 |
| `/ceo-init` | Initialize project | 프로젝트 초기화 |
| `/ceo-status` | Show current status | 현재 상태 조회 |

---

### ECC Capabilities (accessed via CEO-*)

> **EN** — 183 skills from [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code). Not installed as individual commands — use CEO-* orchestrators to access them.
>
> **KO** — 183개 스킬. 개별 커맨드로 설치하지 않습니다 — CEO-* 오케스트레이터를 통해 접근합니다.

#### Planning / 기획

| Command | EN | KO |
|---------|----|----|
| `/plan` | Step-by-step plan | 단계별 계획 |
| `/feature-dev` | Feature dev with codebase analysis | 코드베이스 분석 기반 기능 개발 |
| `/implement` | Execute implementation plan | 구현 계획 실행 |
| `/spec` | Generate technical specification | 기술 명세 생성 |
| `/prp-prd` | Interactive PRD generator | 인터랙티브 PRD 생성 |
| `/prp-plan` | Implementation plan with pattern extraction | 패턴 추출 기반 구현 계획 |
| `/prp-implement` | Execute PRP with validation loops | 검증 루프 포함 PRP 실행 |
| `/prp-commit` | Smart commit with natural language | 자연어 스마트 커밋 |
| `/prp-pr` | Create GitHub PR | GitHub PR 생성 |
| `/multi-plan` | Multi-model planning | 멀티모델 기획 |
| `/multi-execute` | Multi-model execution | 멀티모델 실행 |
| `/multi-frontend` | Frontend-focused multi-model | 프론트엔드 집중 멀티모델 |
| `/multi-backend` | Backend-focused multi-model | 백엔드 집중 멀티모델 |
| `/multi-workflow` | Full multi-model workflow | 전체 멀티모델 워크플로우 |

#### Code Review / 코드 리뷰

| Command | EN | KO |
|---------|----|----|
| `/code-review` | Review changes or PR | 변경사항 / PR 리뷰 |
| `/review-pr` | Comprehensive PR review | 종합 PR 리뷰 |
| `/security-review` | OWASP Top 10, secrets, auth | OWASP, 시크릿, 인증 감사 |
| `/quality-gate` | Run all 5 gates | 5개 게이트 실행 |
| `/santa-loop` | Dual adversarial review loop | 이중 적대적 리뷰 루프 |
| `/refactor-clean` | Remove dead code and duplicates | 데드코드 및 중복 제거 |
| `/perf-check` | Performance bottleneck analysis | 성능 병목 분석 |
| `/test-coverage` | Coverage gap analysis | 커버리지 부족 분석 |
| `/python-review` | Python — PEP 8, type hints, security | Python 전문 리뷰 |
| `/go-review` | Go — idiomatic, concurrency | Go 전문 리뷰 |
| `/rust-review` | Rust — ownership, lifetimes | Rust 전문 리뷰 |
| `/cpp-review` | C++ — memory, modern idioms | C++ 전문 리뷰 |
| `/flutter-review` | Flutter/Dart — widgets, state | Flutter 전문 리뷰 |
| `/kotlin-review` | Kotlin — null safety, coroutines | Kotlin 전문 리뷰 |

#### Test & TDD / 테스트

| Command | EN | KO |
|---------|----|----|
| `/tdd` | RED → GREEN → REFACTOR | TDD 워크플로우 |
| `/test` | Run tests, report failures | 테스트 실행 |
| `/e2e` | Playwright E2E testing | Playwright E2E |
| `/go-test` | Go TDD — table-driven, 80%+ | Go TDD |
| `/rust-test` | Rust TDD — cargo-llvm-cov | Rust TDD |
| `/cpp-test` | C++ TDD — GoogleTest | C++ TDD |
| `/flutter-test` | Flutter — unit, widget, golden | Flutter 테스트 |
| `/kotlin-test` | Kotlin TDD — Kotest + Kover | Kotlin TDD |

#### Build & Fix / 빌드 및 수정

| Command | EN | KO |
|---------|----|----|
| `/build-fix` | Fix build errors incrementally | 빌드 오류 단계적 수정 |
| `/go-build` | Fix Go build, vet, linter | Go 빌드 수정 |
| `/rust-build` | Fix Rust build, borrow checker | Rust 빌드 수정 |
| `/cpp-build` | Fix C++ build, CMake, linker | C++ 빌드 수정 |
| `/flutter-build` | Fix Dart analyzer, Flutter | Flutter 빌드 수정 |
| `/kotlin-build` | Fix Kotlin/Gradle build | Kotlin 빌드 수정 |
| `/gradle-build` | Fix Gradle for Android/KMP | Gradle 빌드 수정 |

#### Session & Context / 세션 및 컨텍스트

| Command | EN | KO |
|---------|----|----|
| `/save-session` | Save session to `~/.claude/session-data/` | 세션 저장 |
| `/resume-session` | Resume last session with full context | 마지막 세션 재개 |
| `/sessions` | Manage session history | 세션 히스토리 관리 |
| `/checkpoint` | Save progress checkpoint | 체크포인트 저장 |
| `/context-budget` | Monitor context window | 컨텍스트 모니터링 |
| `/aside` | Side question without losing context | 컨텍스트 유지 부가 질문 |

#### Learning & Instincts / 학습 및 인스팅트

| Command | EN | KO |
|---------|----|----|
| `/learn` | Extract patterns from session | 세션 패턴 추출 |
| `/learn-eval` | Extract, evaluate, save | 패턴 추출 + 평가 + 저장 |
| `/evolve` | Analyze and improve instincts | 인스팅트 분석 및 개선 |
| `/instinct-status` | Show instincts with confidence | 신뢰도 포함 인스팅트 표시 |
| `/instinct-import` | Import instincts from file/URL | 파일/URL에서 가져오기 |
| `/instinct-export` | Export instincts to file | 파일로 내보내기 |
| `/promote` | Promote project instincts to global | 글로벌 승격 |
| `/prune` | Delete stale instincts (30+ days) | 30일 이상 인스팅트 정리 |
| `/projects` | List projects and instinct stats | 프로젝트 및 통계 |

#### Hooks & Automation / 훅

| Command | EN | KO |
|---------|----|----|
| `/hookify` | Create hooks from conversation | 대화에서 훅 생성 |
| `/hookify-configure` | Enable/disable hookify rules | 훅 규칙 활성화/비활성화 |
| `/hookify-help` | Help with hookify system | hookify 도움말 |
| `/hookify-list` | List all configured hooks | 설정된 훅 목록 |

#### DevOps / 데브옵스

| Command | EN | KO |
|---------|----|----|
| `/pipeline` | Set up CI/CD pipeline | CI/CD 파이프라인 설정 |
| `/pm2` | Initialize PM2 | PM2 초기화 |
| `/setup-pm` | Configure package manager | 패키지 매니저 설정 |
| `/devfleet` | Claude DevFleet deployment | DevFleet 배포 |

#### Docs & Cost / 문서 및 비용

| Command | EN | KO |
|---------|----|----|
| `/docs` | Lookup docs via Context7 | Context7 문서 조회 |
| `/update-docs` | Update project docs | 프로젝트 문서 업데이트 |
| `/update-codemaps` | Regenerate codemaps | 코드맵 재생성 |
| `/report` | Generate status report | 상태 보고서 생성 |
| `/cost-estimate` | Estimate token cost | 토큰 비용 추정 |
| `/model-route` | Route to optimal model | 최적 모델 라우팅 |
| `/prompt-optimize` | Optimize prompt for cost | 비용 최적화 프롬프트 |

#### Loop & Orchestration / 루프

| Command | EN | KO |
|---------|----|----|
| `/loop-start` | Start recurring agent loop | 반복 에이전트 루프 시작 |
| `/loop-status` | Show loop status | 루프 상태 표시 |
| `/orchestrate` | Multi-agent orchestration | 멀티에이전트 오케스트레이션 |
| `/santa-loop` | Adversarial dual-review loop | 적대적 이중 리뷰 루프 |

#### Misc / 기타

| Command | EN | KO |
|---------|----|----|
| `/debug` | Systematic bug diagnosis | 체계적 버그 진단 |
| `/design` | Design system and UI | 디자인 시스템 및 UI |
| `/ui-design` | UI component generation | UI 컴포넌트 생성 |
| `/jira` | Jira ticket management | Jira 티켓 관리 |
| `/skill-create` | Generate SKILL.md from git | git으로 SKILL.md 생성 |
| `/skill-health` | Skill portfolio dashboard | 스킬 포트폴리오 대시보드 |
| `/agent-sort` | Sort agents by fit | 적합도 기반 에이전트 정렬 |
| `/rules-distill` | Distill rules from codebase | 코드베이스에서 규칙 정제 |
| `/evaluate-oss` | Evaluate OSS library fit | 오픈소스 라이브러리 평가 |

---

### gstack Commands

> **EN** — 35+ battle-tested commands from [garrytan/gstack](https://github.com/garrytan/gstack).
>
> **KO** — Garry Tan의 검증된 35개 이상 커맨드.

#### Ship & Deploy / 배포

| Command | EN | KO |
|---------|----|----|
| `/ship` | Full ship workflow | 전체 배포 워크플로우 |
| `/land-and-deploy` | Land changes + deploy | 변경 랜딩 + 배포 |
| `/canary` | Canary release | 카나리 릴리즈 |
| `/setup-deploy` | Set up deployment config | 배포 설정 구성 |

#### QA & Testing / QA

| Command | EN | KO |
|---------|----|----|
| `/qa` | Browser QA with screenshots | 스크린샷 포함 브라우저 QA |
| `/qa-only` | QA without shipping | 배포 없는 QA |
| `/test` | Run tests | 테스트 실행 |
| `/benchmark` | Performance benchmarks | 성능 벤치마크 |

#### Review & Debug / 리뷰 및 디버그

| Command | EN | KO |
|---------|----|----|
| `/review` | Code review for current diff | 현재 diff 리뷰 |
| `/health` | Project health check | 프로젝트 헬스 체크 |
| `/investigate` | Root cause analysis | 근본 원인 분석 |

#### Planning / 기획

| Command | EN | KO |
|---------|----|----|
| `/plan` | Interactive Q&A planning | 인터랙티브 Q&A 기획 |
| `/autoplan` | Auto-generate plan from context | 컨텍스트 기반 자동 계획 |
| `/plan-ceo-review` | CEO-level plan review | CEO 레벨 계획 리뷰 |
| `/plan-eng-review` | Engineering architecture review | 엔지니어링 아키텍처 리뷰 |
| `/plan-design-review` | Design review at plan stage | 기획 단계 디자인 리뷰 |
| `/office-hours` | Brainstorm + feasibility | 브레인스토밍 + 타당성 |

#### Design / 디자인

| Command | EN | KO |
|---------|----|----|
| `/design` | Brand + system + components | 브랜드 + 디자인 시스템 + 컴포넌트 |
| `/design-review` | Visual design review | 비주얼 디자인 리뷰 |
| `/design-consultation` | Design direction consultation | 디자인 방향 컨설팅 |
| `/design-html` | HTML/CSS from design specs | 디자인 명세 → HTML/CSS |
| `/design-shotgun` | Rapid multi-direction exploration | 다방향 빠른 탐색 |

#### Docs & Learning / 문서 및 학습

| Command | EN | KO |
|---------|----|----|
| `/docs` | Update or generate docs | 문서 업데이트/생성 |
| `/document-release` | Update docs after shipping | 배포 후 문서 업데이트 |
| `/learn` | Save session learnings | 세션 학습 저장 |
| `/retro` | Weekly retrospective | 주간 회고 |
| `/checkpoint` | Save progress checkpoint | 체크포인트 저장 |

#### Safety / 안전

| Command | EN | KO |
|---------|----|----|
| `/freeze` | Freeze file/module | 파일/모듈 동결 |
| `/unfreeze` | Unfreeze file/module | 파일/모듈 해제 |
| `/guard` | Add regression guards | 회귀 방지 가드 추가 |
| `/careful` | Extra-careful mode | 초주의 모드 |

#### Browser & Misc / 브라우저 및 기타

| Command | EN | KO |
|---------|----|----|
| `/browse` | Open and inspect URL | URL 열기 및 검사 |
| `/connect-chrome` | Connect to Chrome | Chrome 연결 |
| `/setup-browser-cookies` | Configure browser cookies | 브라우저 쿠키 설정 |
| `/codex` | Code exploration | 코드 탐색 |
| `/cso` | Chief of Staff — comms triage | 커뮤니케이션 분류 |
| `/gstack-upgrade` | Upgrade gstack | gstack 업그레이드 |

---

## Quality Gates / 품질 게이트

> **EN** — Every output passes 5 mandatory gates. No exceptions.
>
> **KO** — 모든 산출물은 5개 필수 게이트를 통과합니다. 예외 없음.

| Gate | Check |
|------|-------|
| GATE 1 | Error registry scan + **300-line file limit** (auto-blocked) |
| GATE 2 | All completion criteria verified |
| GATE 3 | Version tag `v0.0.0` present |
| GATE 4 | Builder ≠ Reviewer (enforced, no exceptions) |
| GATE 5 | Breaking changes blocked without explicit approval |

---

## Coding Standards / 코딩 표준

> **EN** — Non-negotiable. Enforced by GATE 1 on every file.
>
> **KO** — 협상 불가. GATE 1이 모든 파일에 강제 적용.

| Rule | EN | KO |
|------|----|----|
| **300 lines max per file** | GATE 1 auto-blocks | GATE 1 자동 차단 |
| 50 lines max per function | — | — |
| 4 levels max nesting | — | — |
| Immutability | Always create new objects, never mutate | 항상 새 객체 생성 |
| Error handling | Explicit at every level | 모든 레벨에서 명시적 처리 |
| Input validation | At all system boundaries | 모든 시스템 경계에서 검증 |
| Tests | Required for every feature | 모든 기능에 테스트 필수 |
| RLS | Row Level Security always | 항상 구현 |

---

## Security Built-in / 내장 보안

> **EN** — Security runs on every sprint, not just at the end.
>
> **KO** — 보안은 마지막이 아닌 매 스프린트에 실행됩니다.

| Rule | EN | KO |
|------|----|----|
| OWASP Top 10 | Reviewed every sprint | 매 스프린트 검토 |
| JWT | httpOnly cookies only | httpOnly 쿠키만 |
| Encryption | AES-256-GCM for all PII | 개인정보 AES-256-GCM |
| Rate limiting | All endpoints | 모든 엔드포인트 |
| Input validation | Zod at all boundaries | 모든 경계에서 Zod |
| RLS | Always enforced | 항상 강제 |

---

## Dependencies / 의존성

| System | Repo | What it provides |
|--------|------|-----------------|
| **ECC** | [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) | 183 skills — accessed via CEO-* |
| **gstack** | [garrytan/gstack](https://github.com/garrytan/gstack) | Garry Tan's battle-tested toolkit |
| **Superpowers** | obra/superpowers-marketplace | **Required.** Installer fails if not installed |

---

## Requirements / 요구사항

| Requirement | Details |
|-------------|---------|
| [Claude Code](https://claude.ai/code) CLI | Required |
| Anthropic API key | Opus + Sonnet + Haiku access |
| `git` | For installer |

---

## License / 라이선스

MIT — see [LICENSE](LICENSE)

---

*Built by **docrew** / CEO of KDC*
