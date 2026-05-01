# 01. Architecture — v2.0.37 Karpathy Principles Merge

## Information Architecture

```
CLAUDE.md (all 3)
├── [EXISTING] Header + Version
├── [EXISTING] 핵심 강제 규칙 (Critical Enforcement — UNCHANGED)
├── [NEW] ## Grand Principles (Karpathy 4 principles, English, DOMANGCHA examples)
├── [EXISTING] 스킬/에이전트/명령어 sections
└── [EXISTING] 버전 관리 정책

rules/common/coding-style.md
├── [NEW] ## 1. Think Before Coding
│   └── (absorbs: none from existing — new philosophy layer)
├── [NEW] ## 2. Simplicity First
│   └── (absorbs: Immutability, KISS, DRY, YAGNI, Code Smells)
├── [NEW] ## 3. Surgical Changes
│   └── (absorbs: File Organization, Naming Conventions)
├── [NEW] ## 4. Goal-Driven Execution
│   └── (absorbs: Error Handling, Input Validation, Code Quality Checklist)
└── [NEW] Footer: "These guidelines are working if..."

rules/zh/coding-style.md
└── [REWRITE] Same structure in Chinese
```

## Priority Layer Model

```
Layer 1 (HIGHEST): CEO Pipeline Enforcement Rules
  - GATE 1-5, DOC-FIRST, Q&A mandatory, INTENT PARSE
  - These are non-negotiable procedures

Layer 2: Karpathy Grand Principles (NEW)
  - Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven Execution
  - Applied to all code writing, inform HOW to approach tasks

Layer 3: Detailed Coding Standards (rules/common/coding-style.md)
  - Specific conventions, checklists, naming rules
```

## Key Design Decision

Karpathy principles in CLAUDE.md = always loaded into CEO context → applies to all agents
coding-style.md = loaded when rules context is active → detailed implementation guidance
No duplication: CLAUDE.md has the 4 principles compact, coding-style.md has full detail
