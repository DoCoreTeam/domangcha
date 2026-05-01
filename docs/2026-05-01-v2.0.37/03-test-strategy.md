# 03. Test Strategy — v2.0.37 Karpathy Principles Merge

## Verification Approach

1. **Content Integrity Check**: Diff each modified CLAUDE.md against original — confirm only new section added, no existing content removed or modified
2. **Pipeline Rule Preservation**: Verify all 핵심 강제 규칙 sections are word-for-word identical to pre-change state
3. **coding-style.md Coverage**: Confirm all existing concepts (Immutability, KISS/DRY/YAGNI, File Organization, Naming, Error Handling, Input Validation, Code Quality Checklist) appear in new structure
4. **Version Sync**: All 10 version files show 2.0.37

## DC-REV Review Focus

- No CEO pipeline rule was weakened or removed
- Karpathy principles appear AFTER 핵심 강제 규칙 section
- English original preserved, DOMANGCHA context examples are relevant
- coding-style.md integrates all existing content without loss
