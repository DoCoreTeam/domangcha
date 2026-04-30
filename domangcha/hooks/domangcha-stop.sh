#!/usr/bin/env bash
# ============================================================
# DOMANGCHA Stop Hook — Premature Completion Guard + Quality Review
# exit 2 = force CEO to continue (Block completion)
# exit 0 = allow session to end
# ============================================================

PROJ="${CLAUDE_PROJECT_DIR:-$(pwd)}"
BLOCK_REASON=""

# ── GUARD 1: Uncommitted changes exist ──
GIT_DIRTY=$(git -C "$PROJ" diff --name-only 2>/dev/null | wc -l | tr -d ' ')
GIT_STAGED=$(git -C "$PROJ" diff --cached --name-only 2>/dev/null | wc -l | tr -d ' ')
TOTAL_CHANGES=$((GIT_DIRTY + GIT_STAGED))
if [ "$TOTAL_CHANGES" -gt 0 ]; then
    BLOCK_REASON="${BLOCK_REASON}⚠️ 미커밋 변경파일 ${TOTAL_CHANGES}개 (git commit 필요)\n"
fi

# ── GUARD 2: TODO/FIXME left in modified files ──
if [ "$TOTAL_CHANGES" -gt 0 ]; then
    TODO_FILES=$(git -C "$PROJ" diff --name-only 2>/dev/null | while read -r f; do
        grep -l "TODO\|FIXME\|HACK\|XXX\|미구현\|추후구현" "$PROJ/$f" 2>/dev/null
    done | wc -l | tr -d ' ')
    if [ "$TODO_FILES" -gt 0 ]; then
        BLOCK_REASON="${BLOCK_REASON}⚠️ TODO/FIXME 미해결 파일 ${TODO_FILES}개\n"
    fi
fi

# ── GUARD 3: VERSION file drift ──
VERSION_FILE=$(find "$PROJ" -maxdepth 3 -name "VERSION" 2>/dev/null | head -1)
if [ -n "$VERSION_FILE" ]; then
    FILE_VER=$(cat "$VERSION_FILE" | tr -d ' \n')
    LAST_TAG=$(git -C "$PROJ" log --oneline -1 2>/dev/null | grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+' | head -1)
    if [ -n "$LAST_TAG" ] && [ "v${FILE_VER}" != "$LAST_TAG" ] && [ "$TOTAL_CHANGES" -gt 0 ]; then
        BLOCK_REASON="${BLOCK_REASON}⚠️ VERSION(${FILE_VER}) ↔ 마지막 커밋(${LAST_TAG}) 불일치\n"
    fi
fi

# ── If any guard triggered → block completion ──
if [ -n "$BLOCK_REASON" ]; then
    echo ""
    echo "[HOOK: 미완료 감지]"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "$BLOCK_REASON"
    echo "→ CEO: 위 항목들을 완료한 뒤 종료하세요."
    echo "  GATE 1-5 체크 → lint 확인 → git commit → 버전 업데이트"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 2  # Force CEO to continue
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  [DOMANGCHA] Stop Hook — CEO Quality Review"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

PROMPT="Act as the CEO of DOMANGCHA. Run a rapid final quality review.

Check recently modified files for:
1. SECURITY: Hardcoded secrets, SQL injection, XSS, unvalidated inputs (OWASP Top 10)
2. CODE QUALITY: Files >300 lines, functions >50 lines, missing error handling
3. TESTS: Test coverage exists for changed functionality
4. VERSION: domangcha/VERSION or VERSION file consistent with git log

Output format:
[DOMANGCHA STOP REVIEW]
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
    2>/dev/null || echo "  [DOMANGCHA] Stop review skipped (claude CLI not available)"

exit 0
