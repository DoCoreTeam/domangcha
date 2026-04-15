# 🏢 DOCORE — 16 AI Agents Orchestration for Claude Code

> One command. All agents. Full pipeline. Every time.

```bash
/ceo "Build a todo app with authentication"
```

This single command activates **16 specialized AI agents** that plan, develop, test, and deploy your project — in the correct development order, with no steps skipped.

## ⚡ Install

```bash
# One-line install
curl -sSL https://raw.githubusercontent.com/docore/docore/main/install.sh | bash

# Or manual
git clone https://github.com/docore/docore.git ~/.claude/skills/docore
```

## 🎯 How It Works

You type one command → CEO orchestrates everything:

```
/ceo "원하는 것"
     │
     ▼
① PLANNER ──── DC-BIZ (사업판단) + DC-RES (리서치) + DC-OSS (라이브러리)
     │            → PLAN.md 산출
     ▼
② GENERATOR ── DC-DEV-FE + DC-DEV-BE + DC-DEV-DB + DC-DEV-MOB
     │          DC-DEV-OPS + DC-DEV-INT + DC-WRT + DC-DOC + DC-SEO
     │            → 병렬 개발
     ▼
③ EVALUATOR ── DC-QA (테스트) + DC-SEC (보안) + DC-REV (리뷰)
     │            → FAIL이면 ②로 재작업 (최대 3회)
     ▼
④ GATE 1-5 ── 금지패턴 + 완료조건 + 버전태그 + 역할분리 + 변경감지
     │
     ▼
⑤ CEO REPORT ─ 완성된 코드 + 테스트 + 문서 + git commit v0.x.0
```

## 📋 Commands

| Command | What it does |
|---------|-------------|
| `/ceo "task"` | Run full pipeline with all 16 agents |
| `/ceo-init` | Initialize project (registries + harness) |
| `/ceo-status` | Show project status |

## 🤖 16 Agents

### PLANNER (기획)
| Agent | Role | Model |
|-------|------|-------|
| DC-BIZ | Business Judge | Opus |
| DC-RES | Researcher | Haiku |
| DC-OSS | Open Source Scout | Opus |

### GENERATOR (개발)
| Agent | Role | Model |
|-------|------|-------|
| DC-DEV-FE | Frontend Developer | Sonnet |
| DC-DEV-BE | Backend Developer | Sonnet |
| DC-DEV-DB | Database Engineer | Sonnet |
| DC-DEV-MOB | Mobile Developer | Sonnet |
| DC-DEV-OPS | DevOps Engineer | Sonnet |
| DC-DEV-INT | Integration Engineer | Sonnet |
| DC-WRT | Writer/Copywriter | Sonnet |
| DC-DOC | Documentation Writer | Haiku |
| DC-SEO | SEO/AEO/GEO Specialist | Haiku |

### EVALUATOR (검증)
| Agent | Role | Model |
|-------|------|-------|
| DC-QA | QA Engineer | Haiku |
| DC-SEC | Security Reviewer | Opus |
| DC-REV | Code/Content Reviewer | Opus |

### SUPPORT (지원)
| Agent | Role | Model |
|-------|------|-------|
| DC-TOK | Token Optimizer | Haiku |

## 🔧 Quality Gates

Every output passes through 5 gates before delivery:

- **GATE 1**: Error registry pattern scan
- **GATE 2**: Completion criteria verification
- **GATE 3**: Version tag (v0.0.0) check
- **GATE 4**: Builder ≠ Reviewer separation
- **GATE 5**: Breaking change detection

## 📁 Structure

```
docore/
├── CLAUDE.md                    ← Entry point (auto-loaded)
├── install.sh                   ← One-line installer
├── skills/ceo-system/SKILL.md   ← CEO brain (full system)
├── agents/                      ← 16 agent definitions
│   ├── dc-biz.md ... dc-tok.md
├── commands/                    ← Slash commands
│   ├── ceo.md                   ← /ceo "task"
│   ├── ceo-init.md              ← /ceo-init
│   └── ceo-status.md            ← /ceo-status
└── templates/                   ← Registry templates
    ├── error-registry.md
    ├── skill-registry.md
    ├── project-registry.md
    └── decision-log.md
```

## 🛡️ Security Built-in

- OWASP Top 10 review on every sprint
- JWT httpOnly cookies only (no localStorage)
- AES-256-GCM for PII encryption
- Rate limiting on all endpoints
- Input validation with Zod
- RLS (Row Level Security) enforcement

## 📄 License

MIT

## 🙋 Author

Built by **Docore** — CEO of KDC (Korea Digital Certification)
