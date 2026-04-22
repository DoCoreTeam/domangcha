#!/usr/bin/env bash
# ============================================================
# MACC Stop Hook — CEO Quality Review at Session End
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  [MACC] Stop Hook — CEO Quality Review"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

PROMPT="Act as the CEO of MACC (Multi-Agent Claude Crew). Run a rapid final quality review.

Check recently modified files for:
1. SECURITY: Hardcoded secrets, SQL injection, XSS, unvalidated inputs (OWASP Top 10)
2. CODE QUALITY: Files >300 lines, functions >50 lines, missing error handling
3. TESTS: Test coverage exists for changed functionality
4. VERSION: macc/VERSION or VERSION file consistent with git log

Output format:
[MACC STOP REVIEW]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅/⚠️/🔴 Security: <brief result>
✅/⚠️/🔴 Code Quality: <brief result>
✅/⚠️/🔴 Tests: <brief result>
✅/⚠️/🔴 Version: <brief result>
[Overall: PASS / WARN / FAIL]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
If FAIL: list top 3 issues to fix.
Keep under 20 lines total."

claude -p "$PROMPT" \
    --allowedTools "Read,Grep,Glob,Bash" \
    --max-turns 5 \
    2>/dev/null || echo "  [MACC] Stop review skipped (claude CLI not available)"

exit 0
