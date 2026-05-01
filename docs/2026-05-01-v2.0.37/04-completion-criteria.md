# 04. Completion Criteria — v2.0.37 Karpathy Principles Merge

## Done When

1. All 3 CLAUDE.md files contain ## Grand Principles section with Karpathy 4 principles
2. Section is placed AFTER 핵심 강제 규칙, BEFORE 스킬/에이전트 sections
3. coding-style.md follows 4-principle structure; all original concepts present
4. zh/coding-style.md mirrors same structure in Chinese
5. GATE 1-5 pass:
   - G1: No file exceeds 300 lines that didn't before; no error-registry violations
   - G2: All completion criteria met (this list)
   - G3: domangcha/VERSION = 2.0.37, all 10 sync files updated
   - G4: DC-REV reviewed (Builder ≠ Reviewer)
   - G5: No destructive changes to existing CEO pipeline rules
6. DC-REV PASS (score ≥ 80/100)
7. git commit + push + npm publish complete
8. README updated with v2.0.37 What's New

## Rollback Criteria

If DC-REV finds any CEO pipeline enforcement rule was inadvertently modified → revert and re-apply only additive changes.
