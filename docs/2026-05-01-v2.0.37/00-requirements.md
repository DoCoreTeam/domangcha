# 00. Requirements — v2.0.37 Karpathy Principles Merge

## Functional Requirements

1. Add Karpathy 4 grand principles to all 3 CLAUDE.md files
   - ~/.claude/CLAUDE.md
   - domangcha/CLAUDE.md
   - CLAUDE.md (project root)
2. Rewrite ~/.claude/rules/common/coding-style.md using Karpathy 4-principle structure, integrating existing content
3. Rewrite ~/.claude/rules/zh/coding-style.md with same structure (Chinese)

## Non-Functional Requirements

- CEO pipeline enforcement rules (GATE 1-5, DOC-FIRST, Q&A, INTENT PARSE) must remain unchanged
- Karpathy principles: English original, with DOMANGCHA-specific context examples replacing generic ones
- Principles placed AFTER critical enforcement rules section in each CLAUDE.md
- No new files created (merge only)
- Version bump: 2.0.36 → 2.0.37 (PATCH)

## Priority Rules (confirmed by user)

- Karpathy principles = upper-level philosophy (applies to all code writing)
- CEO mandatory enforcement rules = non-negotiable, take precedence over principles where they specify exact procedures
- The two coexist: principles guide HOW, pipeline rules define WHAT MUST happen
