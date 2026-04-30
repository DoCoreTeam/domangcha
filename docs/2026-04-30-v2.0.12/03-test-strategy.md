# 03 — Test Strategy

> **Project**: DOMANGCHA GitHub Discovery Optimization
> **Version**: v2.0.12
> **Date**: 2026-04-30
> **Owner**: DC-OSS / DC-QA
> **Status**: DRAFT — pending [DOC COMPLETE]

---

## 0. Scope & Objectives

### Scope (In)
- `package.json` — npm 패키지 매니페스트 유효성
- `install.sh` — bash 설치 스크립트 무결성
- GitHub repo metadata (topics, description, social preview)
- npm registry publish artifact (배포 직전 검증)
- README.md 외부/내부 링크
- 소셜 포스팅 템플릿 (`.github/` 하위 마크다운/YAML)

### Scope (Out)
- 에이전트 동작 회귀 테스트 (별도 e2e 파이프라인)
- 실제 npm publish (publish는 사용자 승인 후 수동 실행)
- GitHub Actions 런타임 비용 분석

### Test Objectives
1. 배포 전 패키지 무결성 100% 보장
2. 설치 스크립트가 macOS/Linux 양쪽에서 syntax-clean
3. GitHub 디스커버리 시그널(topics, description)이 의도대로 노출
4. 민감 정보(token, .env, 개인 경로) 미포함 보장
5. README 외부 링크 broken rate 0%

---

## 1. Test Priority Matrix

| Priority | Category | Trigger | Blocking? |
|----------|----------|---------|-----------|
| **P0** | 패키지 무결성 / 설치 가능성 | 모든 커밋 | YES — fail 시 머지 차단 |
| **P1** | 디스커버리 메타데이터 / 로컬 링크 | release 직전 | YES — fail 시 publish 차단 |
| **보안** | 민감 정보 누출 | 모든 커밋 + publish 직전 | YES (CRITICAL) |
| **보완** | 외부 링크 / 호환성 | 주 1회 + release 전 | NO — warn만 |

---

## 2. P0 Tests — 배포 차단급 (필수)

### 2.1 `package.json` 유효성 — `npm pack --dry-run`

**목적**: 패키지 메타데이터(name, version, files, bin, engines)가 npm 스펙에 부합하는지 사전 검증.

**실행 명령**:
```bash
cd /Users/dohyeonkim/dev/docore
npm pack --dry-run --json > /tmp/domangcha-pack.json
```

**Pass 조건**:
- exit code = 0
- `name` 필드 존재 + lowercase + npm 명명규칙 준수 (`/^(@[a-z0-9-~][a-z0-9-._~]*\/)?[a-z0-9-~][a-z0-9-._~]*$/`)
- `version` 필드가 `domangcha/VERSION` 파일과 정확히 일치 (단일 소스 원칙)
- `files` 배열이 명시되어 있거나 `.npmignore` 존재
- 패키지 크기 < 5 MB
- `bin` 엔트리가 가리키는 파일이 실제로 존재 + 실행권한
- `engines.node` 명시 (>= 18.0.0 권장)

**Fail 시 액션**: 머지 차단, DC-DEV-OPS 에이전트로 핫픽스.

### 2.2 `install.sh` Bash Syntax Check

**목적**: 설치 스크립트가 `bash -n` 통과 + ShellCheck 위반 0건.

**실행 명령**:
```bash
# 1. Bash 파싱 검증
bash -n /Users/dohyeonkim/dev/docore/install.sh
echo "exit=$?"

# 2. ShellCheck 정적 분석 (severity=error 한정)
shellcheck -S error /Users/dohyeonkim/dev/docore/install.sh
```

**Pass 조건**:
- `bash -n` exit code = 0
- ShellCheck error 0건 (warning은 이슈 등록 후 통과 허용)
- shebang 존재 (`#!/usr/bin/env bash` 또는 `#!/bin/bash`)
- `set -euo pipefail` 또는 동등한 안전 모드 선언
- 모든 외부 명령(`curl`, `git`, `node`, `npm`)에 대해 `command -v` 가용성 체크
- 비대화형 환경에서 stdin 차단 없음 (CI 호환)

**Fail 시 액션**: 머지 차단, DC-DEV-OPS 핫픽스 + error-registry 패턴 등록.

### 2.3 npm pack 산출물 구조 검증

**실행 명령**:
```bash
npm pack --dry-run 2>&1 | tee /tmp/pack.log
```

**Pass 조건**:
- `domangcha-{VERSION}.tgz` 명명 규칙 일치
- 압축 해제 후 다음 파일 포함:
  - `package.json`
  - `install.sh`
  - `README.md`
  - `LICENSE`
  - `domangcha/VERSION`
- 다음 파일/폴더 미포함 (보안 섹션과 중복 검증):
  - `.env`, `.env.*`
  - `node_modules/`
  - `.git/`
  - `.claude/memory/` (개인 메모리)
  - `*.log`

---

## 3. P1 Tests — Release 차단급

### 3.1 GitHub Topics API 응답 검증

**목적**: 디스커버리 최적화 작업의 핵심 산출물(topics 메타데이터)이 실제로 GitHub에 반영됐는지 확인.

**실행 명령**:
```bash
gh api repos/DoCoreTeam/domangcha/topics \
  -H "Accept: application/vnd.github.mercy-preview+json" \
  | jq '.names'
```

**Pass 조건**:
- HTTP 200
- topics 배열에 다음 키워드 **전부** 포함:
  - `claude-code`
  - `ai-agents`
  - `multi-agent`
  - `developer-tools`
  - `automation`
- topics 개수 ≤ 20 (GitHub 제한)
- description 필드: 50–160자 + 한국어/영어 혼용 가독성 확보

**Fail 시 액션**: DC-DEV-OPS가 `gh api` PUT 요청으로 즉시 동기화.

### 3.2 npm Link 로컬 테스트

**목적**: 사용자가 실제로 `npm install -g domangcha` 했을 때 동일하게 동작하는지 사전 시뮬레이션.

**실행 명령**:
```bash
# 1. 로컬 link
cd /Users/dohyeonkim/dev/docore
npm link

# 2. 글로벌 바이너리 작동 확인
which domangcha
domangcha --version

# 3. clean-up
npm unlink -g domangcha
```

**Pass 조건**:
- `npm link` exit code = 0
- `which domangcha`가 valid 경로 출력
- `domangcha --version` 출력값 == `domangcha/VERSION` 파일 내용
- `domangcha --help` 출력에 broken character 없음 (UTF-8 정상)
- unlink 후 `which domangcha`가 빈 결과 반환

**Fail 시 액션**: bin 경로 / shebang 점검 후 재시도.

---

## 4. 보안 테스트 — CRITICAL

### 4.1 npm 패키지 민감 정보 미포함 검증

**목적**: publish 시 토큰, 개인 경로, 비밀 키가 절대 포함되지 않도록 사전 차단.

**실행 명령**:
```bash
# 1. dry-run으로 포함될 파일 목록 추출
npm pack --dry-run 2>&1 \
  | grep -E "^npm notice [0-9]" \
  | awk '{print $NF}' > /tmp/pack-files.txt

# 2. 패턴 스캔
grep -rEn \
  "(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{36}|ghs_[A-Za-z0-9]{36}|AKIA[0-9A-Z]{16}|/Users/[a-z]+/\.|api[_-]?key.*=.*['\"][A-Za-z0-9]{16,})" \
  $(cat /tmp/pack-files.txt) || echo "CLEAN"

# 3. 패키지 실제 압축 후 재검증
npm pack
tar -tzf domangcha-*.tgz | grep -iE "\.(env|pem|key|p12)$" && echo "FAIL" || echo "PASS"
```

**Pass 조건 (전부 충족)**:
- Anthropic API 키 패턴(`sk-ant-...`) 0건
- GitHub PAT 패턴(`ghp_...`, `ghs_...`) 0건
- AWS Access Key 패턴(`AKIA...`) 0건
- 사용자 home 디렉터리 경로(`/Users/...`) 0건
- `.env`, `.pem`, `.key`, `.p12` 확장자 파일 0건
- 빌드 산출물에 `.claude/memory/`, `.claude/projects/` 미포함

**Fail 시 액션**:
1. **즉시 STOP**
2. DC-SEC 에이전트 호출
3. 노출된 secret 즉시 rotate
4. `.npmignore` / `package.json#files` 패치
5. error-registry에 패턴 등록

### 4.2 `.npmignore` 점검

**목적**: ignore 정책이 명시적이고 누락 없는지 확인.

**필수 포함 패턴** (체크리스트):
```
# Sensitive
.env
.env.*
*.pem
*.key
*.p12
*.crt

# Personal
.claude/memory/
.claude/projects/
.claude/settings.local.json

# Build artifacts
node_modules/
*.log
.DS_Store

# Dev
tests/
docs/
.github/workflows/

# VCS
.git/
.gitignore
```

**Pass 조건**:
- `.npmignore` 파일 존재
- 위 13개 패턴 전부 존재
- `package.json#files` 와 정합성: `files` 사용 시 `.npmignore` 미사용 또는 일관

### 4.3 install.sh 보안 검증

**검증 항목**:
- [ ] `curl | bash` 패턴 사용 시 → SHA256 무결성 검증 또는 GPG 서명 확인 코드 포함
- [ ] `eval`, `source <(curl ...)` 등 동적 실행 0건
- [ ] sudo 사용 시 사용자 명시 동의 프롬프트 존재
- [ ] 임시 파일은 `mktemp` 사용 (predictable path 금지)
- [ ] HTTP가 아닌 HTTPS만 사용

---

## 5. 보완 테스트 — Best Effort

### 5.1 README 링크 유효성 (Broken Link Check)

**목적**: 외부 링크 깨짐 0건 보장.

**실행 명령**:
```bash
# 옵션 A — markdown-link-check (npx)
npx --yes markdown-link-check \
  /Users/dohyeonkim/dev/docore/README.md \
  --config .github/link-check-config.json \
  --quiet

# 옵션 B — lychee (rust 기반, CI 친화)
lychee --no-progress \
  --max-concurrency 4 \
  --exclude-loopback \
  /Users/dohyeonkim/dev/docore/README.md
```

**Pass 조건**:
- HTTP 4xx/5xx 응답 0건
- DNS 해석 실패 0건
- relative path 깨짐 0건
- TLS 인증서 오류 0건

**Allowed Warnings** (warn만, fail 아님):
- 429 (rate limit) — 재시도 후 200이면 통과
- 403 (private repo) — 의도된 경우 allowlist 등록

**실행 빈도**: 주 1회 + release 직전.

### 5.2 social preview 이미지 존재 확인

```bash
# 옵션 매트
test -f /Users/dohyeonkim/dev/docore/.github/social-preview.png \
  && file /Users/dohyeonkim/dev/docore/.github/social-preview.png \
  | grep -q "1280 x 640" \
  && echo "PASS" || echo "FAIL"
```

**Pass 조건**: 1280×640 PNG, 1MB 이하.

### 5.3 멀티 OS 호환성 (macOS / Ubuntu)

GitHub Actions matrix:
```yaml
strategy:
  matrix:
    os: [macos-latest, ubuntu-latest]
    node: [18, 20, 22]
```

각 조합에서 `bash install.sh --dry-run` + `npm pack --dry-run` 통과 여부 확인.

---

## 6. 종료 기준 (Exit Criteria)

다음 **전부** 충족 시 release 가능:

| # | Criterion | Verifier |
|---|-----------|----------|
| 1 | `npm pack --dry-run` exit code = 0 | DC-QA |
| 2 | `bash -n install.sh` exit code = 0 | DC-QA |
| 3 | ShellCheck (severity=error) 0건 | DC-QA |
| 4 | `npx domangcha --version` 출력 == `domangcha/VERSION` | DC-QA |
| 5 | `gh api repos/DoCoreTeam/domangcha/topics` 5개 키워드 전부 포함 | DC-DEV-OPS |
| 6 | 보안 스캔 (4.1) → 민감 정보 0건 | DC-SEC |
| 7 | `.npmignore` 13개 필수 패턴 전부 존재 | DC-SEC |
| 8 | README broken link 0건 | DC-QA |
| 9 | social preview 이미지 존재 (1280×640 PNG) | DC-DEV-OPS |
| 10 | GATE 5개 전부 통과 (CLAUDE.md 규칙) | CEO |

**Exit Signal**: `[QA COMPLETE — v2.0.12 RELEASE READY]` 출력 시 release 승인.

---

## 7. Rollback Criteria (롤백 기준)

다음 중 1건이라도 발생 시 즉시 롤백:

1. publish 후 1시간 이내 `npm install -g domangcha` 설치 실패율 > 5%
2. 보안 사고 — secret leak 사후 발견
3. README의 install 명령이 실제로 동작 안 함
4. install.sh가 사용자 시스템 손상 (예: 잘못된 경로 삭제)

**롤백 액션**:
```bash
npm unpublish domangcha@<bad-version> --force  # 72h 이내만 가능
git tag -d v<bad-version>
git push origin :refs/tags/v<bad-version>
# error-registry에 사후 분석 등록
```

---

## 8. Test Execution Pipeline

```
PreToolUse (commit)
  └── P0.1 npm pack --dry-run
  └── P0.2 bash -n + shellcheck
  └── 보안 4.1 secret scan

PostToolUse (push)
  └── 보완 5.1 link check (warn-only)
  └── 보완 5.3 matrix CI

Pre-Release (manual gate)
  └── P1.1 GitHub topics API
  └── P1.2 npm link 로컬 테스트
  └── 보안 4.1, 4.2, 4.3 (재실행)
  └── Exit Criteria 10개 전체 검증
  └── DC-REV 최종 승인
```

---

## 9. Tooling & Dependencies

| Tool | Purpose | Install |
|------|---------|---------|
| `npm` | pack/link 검증 | bundled w/ Node.js |
| `shellcheck` | bash 정적 분석 | `brew install shellcheck` |
| `gh` | GitHub API 호출 | `brew install gh` |
| `jq` | JSON 파싱 | `brew install jq` |
| `markdown-link-check` | 링크 검증 (Node) | `npx` |
| `lychee` | 링크 검증 (Rust, fast) | `brew install lychee` |
| `tar` | 패키지 내용 검사 | OS 기본 |

---

## 10. Test Ownership

| Test Category | Owner Agent | Reviewer |
|---------------|-------------|----------|
| P0 패키지 무결성 | DC-QA | DC-REV |
| P0 install.sh syntax | DC-DEV-OPS | DC-QA |
| P1 GitHub topics | DC-DEV-OPS | DC-REV |
| P1 npm link | DC-QA | DC-REV |
| 보안 (4.1–4.3) | DC-SEC | DC-REV |
| 보완 link check | DC-QA | — |

**Builder ≠ Reviewer 원칙** (GATE 4): install.sh 작성자와 검증자는 반드시 다른 에이전트.

---

> **Version Tag**: v2.0.12
> **Linked Docs**: `00-requirements.md`, `01-architecture.md`, `02-task-breakdown.md`, `04-completion-criteria.md`
