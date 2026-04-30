#!/bin/bash
set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
WHITE='\033[1;37m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

CLAUDE_DIR="${HOME}/.claude"
AGENTS_DIR="${CLAUDE_DIR}/agents"
COMMANDS_DIR="${CLAUDE_DIR}/commands"
SKILLS_DIR="${CLAUDE_DIR}/skills"

MACC_REPO="https://github.com/DoCoreTeam/domangcha.git"
GSTACK_REPO="https://github.com/garrytan/gstack.git"
ECC_REPO="https://github.com/affaan-m/everything-claude-code.git"

TMP_DIR=$(mktemp -d)
trap "rm -rf $TMP_DIR" EXIT

# ── helper: git update-or-clone ──────────────────
# Usage: git_update_or_clone <repo_url> <dest_dir> <label>
git_update_or_clone() {
    local repo="$1" dest="$2" label="$3"
    if [ -d "${dest}/.git" ]; then
        echo -e "${YELLOW}  ⟳ ${label} — pulling latest${NC}"
        git -C "$dest" fetch --depth 1 origin --quiet
        git -C "$dest" reset --hard origin/HEAD --quiet
    elif [ -d "$dest" ]; then
        echo -e "${YELLOW}  ⟳ ${label} — re-cloning (no .git found)${NC}"
        rm -rf "$dest"
        git clone --depth 1 "$repo" "$dest" --quiet
    else
        echo -e "${GREEN}  ✅ ${label} — cloning fresh${NC}"
        git clone --depth 1 "$repo" "$dest" --quiet
    fi
}

# ── 1. DOMANGCHA ──────────────────────────────────
printf "${DIM}  Fetching DOMANGCHA...${NC}\n"
git clone --depth 1 "$MACC_REPO" "$TMP_DIR/domangcha-repo" --quiet
SRC="${TMP_DIR}/domangcha-repo/domangcha"
DOMANGCHA_VERSION=$(cat "${SRC}/VERSION" 2>/dev/null || echo "unknown")

# ── Banner ─────────────────────────────────────────
clear
echo ""
echo -e "${CYAN}${BOLD}"
echo "  ██████╗  ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗ ██████╗ ██╗  ██╗ █████╗ "
echo "  ██╔══██╗██╔═══██╗████╗ ████║██╔══██╗████╗  ██║██╔════╝ ██║  ██║██╔══██╗"
echo "  ██║  ██║██║   ██║██╔████╔██║███████║██╔██╗ ██║██║  ███╗███████║███████║"
echo "  ██║  ██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║   ██║██╔══██║██╔══██║"
echo "  ██████╔╝╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║╚██████╔╝██║  ██║██║  ██║"
echo "  ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝"
echo -e "${NC}"
echo -e "${WHITE}${BOLD}  돔황차 — 개발 지옥에서 도망쳐  🚗💨${NC}"
echo -e "${DIM}  Your AI getaway car from development hell.${NC}"
echo ""
echo -e "${MAGENTA}  ┌──────────────────────────────────────────────────────┐${NC}"
echo -e "${MAGENTA}  │${NC}  ${GREEN}${BOLD}v${DOMANGCHA_VERSION}${NC}   ${CYAN}16 Agents${NC}  ·  ${CYAN}15 Commands${NC}  ·  ${CYAN}Full Pipeline${NC}  ${MAGENTA}│${NC}"
echo -e "${MAGENTA}  │${NC}  ${DIM}Planner → Builder → Evaluator → GATE → Ship${NC}          ${MAGENTA}│${NC}"
echo -e "${MAGENTA}  │${NC}  ${DIM}by ${NC}${WHITE}docore${DIM} (Michael Dohyeon Kim · KDC CEO)${NC}           ${MAGENTA}│${NC}"
echo -e "${MAGENTA}  │${NC}  ${DIM}github.com/DoCoreTeam${NC}                                ${MAGENTA}│${NC}"
echo -e "${MAGENTA}  └──────────────────────────────────────────────────────┘${NC}"
echo ""

# ── 2. Agents → ~/.claude/agents/ ───────────────
echo ""
echo -e "${BLUE}[2/5] Installing agents → ~/.claude/agents/${NC}"
mkdir -p "$AGENTS_DIR"
for f in "${SRC}/agents/"*.md; do
    name=$(basename "$f")
    [ -f "${AGENTS_DIR}/${name}" ] && echo -e "${YELLOW}  ⟳ ${name}${NC}" || echo -e "${GREEN}  ✅ ${name}${NC}"
    cp "$f" "${AGENTS_DIR}/${name}"
done

# ── 3. Commands → ~/.claude/commands/ ───────────
echo ""
echo -e "${BLUE}[3/5] Installing commands → ~/.claude/commands/${NC}"
mkdir -p "$COMMANDS_DIR"
for f in "${SRC}/commands/"*.md; do
    name=$(basename "$f")
    [ -f "${COMMANDS_DIR}/${name}" ] && echo -e "${YELLOW}  ⟳ ${name}${NC}" || echo -e "${GREEN}  ✅ ${name}${NC}"
    cp "$f" "${COMMANDS_DIR}/${name}"
done

# ── 4. CEO skill ─────────────────────────────────
echo ""
echo -e "${BLUE}[4/5] Installing CEO skill → ~/.claude/skills/ceo-system/${NC}"
mkdir -p "${SKILLS_DIR}/ceo-system"
cp "${SRC}/skills/ceo-system/SKILL.md" "${SKILLS_DIR}/ceo-system/SKILL.md"
echo -e "${GREEN}  ✅ ceo-system/SKILL.md${NC}"

# ── 5. CLAUDE.md → ~/.claude/CLAUDE.md ──────────
echo ""
echo -e "${BLUE}[5/5] Updating CLAUDE.md...${NC}"
if [ -f "${CLAUDE_DIR}/CLAUDE.md" ]; then
    if grep -qE "^# (docrew|DOCORE|MACC|CEO) v" "${CLAUDE_DIR}/CLAUDE.md" 2>/dev/null; then
        echo -e "${YELLOW}  ⟳ CLAUDE.md — updating DOMANGCHA section${NC}"
        python3 - "${CLAUDE_DIR}/CLAUDE.md" "${SRC}/CLAUDE.md" <<'PYEOF'
import sys, re
existing = open(sys.argv[1]).read()
docore_new = open(sys.argv[2]).read()
# Match any of the possible section headers
match = re.search(r'^# (docrew|DOCORE|MACC|CEO) v', existing, re.MULTILINE)
if match:
    existing = existing[:match.start()].rstrip() + "\n"
with open(sys.argv[1], 'w') as out:
    out.write(existing.rstrip() + "\n\n" + docore_new)
PYEOF
    else
        echo -e "${YELLOW}  ⟳ Appending to existing CLAUDE.md${NC}"
        echo "" >> "${CLAUDE_DIR}/CLAUDE.md"
        cat "${SRC}/CLAUDE.md" >> "${CLAUDE_DIR}/CLAUDE.md"
    fi
else
    cp "${SRC}/CLAUDE.md" "${CLAUDE_DIR}/CLAUDE.md"
    echo -e "${GREEN}  ✅ CLAUDE.md created${NC}"
fi

# ── 6. Registries (user data — skip if exists) ───
mkdir -p "${CLAUDE_DIR}/reports"
for file in error-registry skill-registry project-registry decision-log; do
    if [ ! -f "${CLAUDE_DIR}/${file}.md" ]; then
        cp "${SRC}/templates/${file}.md" "${CLAUDE_DIR}/${file}.md"
        echo -e "${GREEN}  ✅ ${file}.md${NC}"
    else
        echo -e "${YELLOW}  ⏭️  ${file}.md preserved (user data)${NC}"
    fi
done

# ── 7. ECC (Everything Claude Code) — skills only, no commands
# ECC commands are NOT installed to avoid cluttering the command list.
# CEO-* orchestrators call ECC internally via skills.
echo ""
echo -e "${BLUE}[Extra] Updating ECC (Everything Claude Code)...${NC}"
echo -e "        183 skills (commands excluded — use CEO-* instead)"

ECC_TMP="${TMP_DIR}/ecc"
git clone --depth 1 "$ECC_REPO" "$ECC_TMP" --quiet

UPDATED_SKILLS=0
NEW_SKILLS=0
for skill_dir in "${ECC_TMP}/skills"/*/; do
    skill_name=$(basename "$skill_dir")
    dest="${SKILLS_DIR}/${skill_name}"
    if [ -d "$dest" ]; then
        rm -rf "$dest"
        UPDATED_SKILLS=$((UPDATED_SKILLS + 1))
    else
        NEW_SKILLS=$((NEW_SKILLS + 1))
    fi
    mkdir -p "$dest"
    cp -r "${skill_dir}"* "$dest/" 2>/dev/null || true
done
echo -e "${GREEN}  ✅ Skills: ${NEW_SKILLS} new, ${UPDATED_SKILLS} updated${NC}"
echo -e "${YELLOW}  ℹ️  ECC commands skipped — access via /ceo-* orchestrators${NC}"

# ── 8. gstack — always update ────────────────────
echo ""
echo -e "${BLUE}[Extra] Updating gstack...${NC}"
git_update_or_clone "$GSTACK_REPO" "${SKILLS_DIR}/gstack" "gstack"

# ── 9. Superpowers — REQUIRED ────────────────────
echo ""
echo -e "${BLUE}[Extra] Installing Superpowers (required)...${NC}"
SUPERPOWERS_INSTALLED=false

# Method 1: Claude Code plugin CLI
if command -v claude &>/dev/null; then
    if claude plugin marketplace list 2>/dev/null | grep -q "obra/superpowers-marketplace"; then
        echo -e "${YELLOW}  ⟳ superpowers-marketplace already registered${NC}"
    else
        claude plugin marketplace add obra/superpowers-marketplace 2>/dev/null && \
            echo -e "${GREEN}  ✅ Marketplace registered: obra/superpowers-marketplace${NC}" || true
    fi

    if claude plugin list 2>/dev/null | grep -q "superpowers"; then
        claude plugin update superpowers 2>/dev/null && \
            echo -e "${GREEN}  ✅ superpowers updated via plugin${NC}" || \
            echo -e "${YELLOW}  ⟳ superpowers already up to date${NC}"
        SUPERPOWERS_INSTALLED=true
    else
        claude plugin install superpowers@superpowers-marketplace 2>/dev/null && \
            SUPERPOWERS_INSTALLED=true && \
            echo -e "${GREEN}  ✅ superpowers installed via plugin${NC}" || true
    fi
fi

# Method 2: GitHub fallback
if [ "$SUPERPOWERS_INSTALLED" = false ]; then
    SUPERPOWERS_REPO="https://github.com/obra/superpowers.git"
    git_update_or_clone "$SUPERPOWERS_REPO" "${SKILLS_DIR}/superpowers" "superpowers" 2>/dev/null && \
        SUPERPOWERS_INSTALLED=true || true
fi

# REQUIRED — fail loudly if not installed
if [ "$SUPERPOWERS_INSTALLED" = false ]; then
    echo ""
    echo -e "\033[0;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m"
    echo -e "\033[0;31m  ❌ SUPERPOWERS INSTALLATION FAILED\033[0m"
    echo -e "\033[0;31m  Superpowers is required for CEO to function.\033[0m"
    echo ""
    echo -e "  Install manually inside Claude Code:"
    echo -e "    \033[1;33m/plugin marketplace add obra/superpowers-marketplace\033[0m"
    echo -e "    \033[1;33m/plugin install superpowers@superpowers-marketplace\033[0m"
    echo -e "\033[0;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m"
    exit 1
fi

# ── 10. DOMANGCHA Hooks — auto-test + auto-fix + CEO enforcer ────────
echo ""
echo -e "${BLUE}[Extra] Installing DOMANGCHA hooks → ~/.claude/hooks/${NC}"
mkdir -p "${CLAUDE_DIR}/hooks"
cp "${SRC}/hooks/macc-post-edit.sh" "${CLAUDE_DIR}/hooks/macc-post-edit.sh"
cp "${SRC}/hooks/macc-stop.sh"      "${CLAUDE_DIR}/hooks/macc-stop.sh"
cp "${SRC}/hooks/macc-ceo-enforcer.py" "${CLAUDE_DIR}/hooks/macc-ceo-enforcer.py"
chmod +x "${CLAUDE_DIR}/hooks/macc-post-edit.sh"
chmod +x "${CLAUDE_DIR}/hooks/macc-stop.sh"
chmod +x "${CLAUDE_DIR}/hooks/macc-ceo-enforcer.py"
echo -e "${GREEN}  ✅ macc-post-edit.sh (auto-test + auto-fix)${NC}"
echo -e "${GREEN}  ✅ macc-stop.sh (CEO quality review)${NC}"
echo -e "${GREEN}  ✅ macc-ceo-enforcer.py (CEO pipeline enforcer — UserPromptSubmit)${NC}"

# ── 11. Inject hooks into settings.json ──────────
echo ""
echo -e "${BLUE}[Extra] Configuring ~/.claude/settings.json hooks...${NC}"
python3 - "${CLAUDE_DIR}" <<'PYEOF'
import sys, json, os

claude_dir = sys.argv[1]
hooks_dir  = os.path.join(claude_dir, "hooks")
settings_path = os.path.join(claude_dir, "settings.json")

MACC_POST = {
    "matcher": "Write|Edit|MultiEdit",
    "hooks": [{"type": "command", "command": f'bash "{hooks_dir}/macc-post-edit.sh"'}]
}
# async: true — CEO quality review runs in background so session ends immediately
MACC_STOP = {
    "hooks": [{"type": "command", "command": f'bash "{hooks_dir}/macc-stop.sh"', "timeout": 120, "async": True}]
}
MACC_ENFORCER = {
    "matcher": "",
    "hooks": [{"type": "command", "command": f'python3 "{hooks_dir}/macc-ceo-enforcer.py"'}]
}
# macc-stop-checks.js: TypeScript check + Playwright smoke test (ECC plugin)
# Runs FIRST so it can read the edited-files accumulator before format-typecheck clears it
MACC_STOP_CHECKS_PATH = os.path.join(claude_dir, "scripts", "hooks", "macc-stop-checks.js")
MACC_STOP_CHECKS = {
    "matcher": "*",
    "hooks": [{"type": "command", "command": f'node "{MACC_STOP_CHECKS_PATH}"', "timeout": 120}],
    "description": "DOMANGCHA Stop Guard: TypeScript BLOCKING check + Playwright smoke test"
} if os.path.exists(MACC_STOP_CHECKS_PATH) else None

settings = {}
if os.path.exists(settings_path):
    try:
        with open(settings_path) as f:
            settings = json.load(f)
    except Exception:
        settings = {}

hooks = settings.get("hooks", {})

# UserPromptSubmit — CEO pipeline enforcer (idempotent)
upr = hooks.get("UserPromptSubmit", [])
upr = [h for h in upr if not any("macc-ceo-enforcer" in sub.get("command","") for sub in h.get("hooks",[]))]
upr.insert(0, MACC_ENFORCER)
hooks["UserPromptSubmit"] = upr

# PostToolUse — remove old DOMANGCHA hook, append fresh
post = hooks.get("PostToolUse", [])
post = [h for h in post if not any("macc-post-edit" in sub.get("command","") for sub in h.get("hooks",[]))]
post.append(MACC_POST)
hooks["PostToolUse"] = post

# Stop — remove old DOMANGCHA hooks, re-inject in correct order
stop = hooks.get("Stop", [])
stop = [h for h in stop if not any(
    "macc-stop" in sub.get("command","") for sub in h.get("hooks",[])
)]
if MACC_STOP_CHECKS:
    stop.insert(0, MACC_STOP_CHECKS)
stop.append(MACC_STOP)
hooks["Stop"] = stop

settings["hooks"] = hooks
with open(settings_path, "w") as f:
    json.dump(settings, f, indent=2)
print("  ✅ settings.json hooks injected (merged safely)")
PYEOF

# ── 12. Playwright MCP — browser testing ─────────
echo ""
echo -e "${BLUE}[Extra] Setting up Playwright MCP (browser testing)...${NC}"
bash "${SRC}/hooks/macc-playwright-setup.sh"

# ── 13. Git hooks — auto-reinstall on pull/clone ──
echo ""
echo -e "${BLUE}[Extra] Installing git hooks (auto-reinstall on update)...${NC}"
# Find the git repo root that contains domangcha/ (works from any working dir)
GIT_REPO=$(git -C "$(dirname "${SRC}")" rev-parse --show-toplevel 2>/dev/null || true)
if [ -n "$GIT_REPO" ]; then
    GIT_HOOKS_DIR="${GIT_REPO}/.git/hooks"
    mkdir -p "$GIT_HOOKS_DIR"

    # post-merge: fires after `git pull` merges changes
    cat > "${GIT_HOOKS_DIR}/post-merge" << 'HOOK_EOF'
#!/bin/bash
# Auto-reinstall DOMANGCHA when repo is updated via git pull
INSTALL_SH="$(git rev-parse --show-toplevel)/domangcha/install.sh"
if [ -f "$INSTALL_SH" ]; then
    echo "[DOMANGCHA] 업데이트 감지 — 재설치 중..."
    bash "$INSTALL_SH"
fi
HOOK_EOF

    # post-checkout: fires after `git clone` (initial checkout)
    cat > "${GIT_HOOKS_DIR}/post-checkout" << 'HOOK_EOF'
#!/bin/bash
# Auto-install DOMANGCHA on first checkout (git clone)
PREV_HEAD=$1
NEW_HEAD=$2
IS_BRANCH_CHECKOUT=$3
# Only fire on branch checkout (IS_BRANCH_CHECKOUT=1), not file checkout
[ "$IS_BRANCH_CHECKOUT" != "1" ] && exit 0
INSTALL_SH="$(git rev-parse --show-toplevel)/domangcha/install.sh"
if [ -f "$INSTALL_SH" ]; then
    echo "[DOMANGCHA] 체크아웃 감지 — 설치 중..."
    bash "$INSTALL_SH"
fi
HOOK_EOF

    chmod +x "${GIT_HOOKS_DIR}/post-merge"
    chmod +x "${GIT_HOOKS_DIR}/post-checkout"
    echo -e "${GREEN}  ✅ .git/hooks/post-merge (git pull 시 자동 재설치)${NC}"
    echo -e "${GREEN}  ✅ .git/hooks/post-checkout (git clone 시 자동 설치)${NC}"
else
    echo -e "${YELLOW}  ⚠️  git 레포 루트를 찾을 수 없음 — git hooks 건너뜀${NC}"
fi

# ── 14. Mark installed version ────────────────────
echo "${DOMANGCHA_VERSION}" > "${CLAUDE_DIR}/domangcha-installed-version"

# ── Done ─────────────────────────────────────────
echo ""
echo -e "${CYAN}${BOLD}"
echo "  ╔══════════════════════════════════════════════════════╗"
echo -e "  ║  ${GREEN}✅  DOMANGCHA v${DOMANGCHA_VERSION} — 설치 완료!${CYAN}                    ║"
echo "  ╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo -e "  ${WHITE}${BOLD}무엇이 설치되었나요?${NC}"
echo -e "  ${DIM}────────────────────────────────────────────────────${NC}"
echo -e "  ${GREEN}✔${NC}  ${YELLOW}~/.claude/agents/dc-*.md${NC}       16 DC-* 에이전트"
echo -e "  ${GREEN}✔${NC}  ${YELLOW}~/.claude/commands/ceo*.md${NC}     /ceo /ceo-init /ceo-ralph ..."
echo -e "  ${GREEN}✔${NC}  ${YELLOW}~/.claude/skills/ceo-system/${NC}   CEO 오케스트레이션 브레인"
echo -e "  ${GREEN}✔${NC}  ${YELLOW}~/.claude/hooks/${NC}               auto-test + CEO review + enforcer"
echo -e "  ${GREEN}✔${NC}  ${YELLOW}~/.claude/settings.json${NC}        hooks 자동 주입"
echo -e "  ${GREEN}✔${NC}  ${YELLOW}~/.claude/CLAUDE.md${NC}            Claude Code 자동 로드"
echo -e "  ${DIM}────────────────────────────────────────────────────${NC}"
echo ""
echo -e "  ${WHITE}${BOLD}🚀 시작하기${NC}"
echo -e "  ${DIM}  1.${NC} Claude Code를 아무 프로젝트에서 열기"
echo -e "  ${DIM}  2.${NC} ${CYAN}/ceo-init${NC}                  프로젝트 초기화"
echo -e "  ${DIM}  3.${NC} ${CYAN}/ceo \"투두앱 만들어줘\"${NC}       풀 파이프라인 시작"
echo ""
echo -e "  ${WHITE}${BOLD}📋 주요 명령어${NC}"
echo -e "  ${CYAN}/ceo \"업무\"${NC}    Q&A → 16에이전트 → GATE → 완료"
echo -e "  ${CYAN}/ceo-ralph${NC}    완료 조건 정의 + 자율 반복 루프"
echo -e "  ${CYAN}/ceo-init${NC}     프로젝트 하네스 셋업"
echo -e "  ${CYAN}/ceo-status${NC}   현황 조회"
echo ""
echo -e "  ${MAGENTA}${BOLD}  개발 지옥에서 도망쳐. 🚗💨 돔황차가 데려다 줄게.${NC}"
echo ""
