#!/bin/bash
set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
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

DOMANGCHA_REPO="https://github.com/DoCoreTeam/domangcha.git"
GSTACK_REPO="https://github.com/garrytan/gstack.git"
ECC_MARKETPLACE="affaan-m/ECC"

TMP_DIR=$(mktemp -d)
trap "rm -rf $TMP_DIR" EXIT

TOTAL_STEPS=15
CURRENT_STEP=0

# ── progress bar ─────────────────────────────────
step() {
    CURRENT_STEP=$((CURRENT_STEP + 1))
    local label_ko="$1"
    local label_en="$2"
    local filled=$((CURRENT_STEP * 20 / TOTAL_STEPS))
    local empty=$((20 - filled))
    local bar="${GREEN}${BOLD}"
    for i in $(seq 1 $filled); do bar="${bar}█"; done
    bar="${bar}${DIM}"
    for i in $(seq 1 $empty); do bar="${bar}░"; done
    bar="${bar}${NC}"
    echo ""
    printf "  ${CYAN}[%d/%d]${NC} ${WHITE}${BOLD}%-34s${NC}${DIM} / %s${NC}\n" \
        "$CURRENT_STEP" "$TOTAL_STEPS" "$label_en" "$label_ko"
    printf "  %b  ${DIM}%d%%${NC}\n" "$bar" "$((CURRENT_STEP * 100 / TOTAL_STEPS))"
}

# ── spinner ───────────────────────────────────────
spin() {
    local pid=$! frames='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏' i=0 rc=0
    while kill -0 $pid 2>/dev/null; do
        printf "\r  ${CYAN}${frames:$((i % ${#frames})):1}${NC}  ${DIM}%s${NC}" "$1"
        sleep 0.1
        i=$((i + 1))
    done
    wait "$pid" || rc=$?
    if [ "$rc" -eq 0 ]; then
        printf "\r  ${GREEN}✔${NC}  %-40s\n" "$1"
    else
        printf "\r  ${RED}✖${NC}  %-40s ${DIM}failed, exit %d${NC}\n" "$1" "$rc"
    fi
    return "$rc"
}

# ── helper: git update-or-clone ──────────────────
# Report the outcome after the work, never before it: a line printed ahead of the clone
# claims a result nobody checked.
git_update_or_clone() {
    local repo="$1" dest="$2" label="$3"
    if [ -d "${dest}/.git" ]; then
        git -C "$dest" fetch --depth 1 origin --quiet
        git -C "$dest" reset --hard origin/HEAD --quiet
        echo -e "${GREEN}  ✅ ${label} — updated${DIM} / 갱신됨${NC}"
    elif [ -d "$dest" ]; then
        rm -rf "$dest"
        git clone --depth 1 "$repo" "$dest" --quiet
        echo -e "${GREEN}  ✅ ${label} — re-cloned${DIM} / 재클론됨${NC}"
    else
        git clone --depth 1 "$repo" "$dest" --quiet
        echo -e "${GREEN}  ✅ ${label} — installed${DIM} / 신규 설치됨${NC}"
    fi
}

# ── 1. DOMANGCHA download ─────────────────────────
clear 2>/dev/null || true  # no terminal (CI, TERM=dumb) must not abort the install
echo ""
echo -e "${CYAN}${BOLD}"
echo "  ██████╗  ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗ ██████╗  ██████╗ ██╗  ██╗ █████╗ "
echo "  ██╔══██╗██╔═══██╗████╗ ████║██╔══██╗████╗  ██║██╔════╝ ██╔════╝ ██║  ██║██╔══██╗"
echo "  ██║  ██║██║   ██║██╔████╔██║███████║██╔██╗ ██║██║  ███╗██║      ███████║███████║"
echo "  ██║  ██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║   ██║██║      ██╔══██║██╔══██║"
echo "  ██████╔╝╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║╚██████╔╝╚██████╗ ██║  ██║██║  ██║"
echo "  ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝"
echo -e "${NC}"
echo -e "${WHITE}${BOLD}  Your AI getaway car from development hell.  🚗💨${NC}"
echo -e "${DIM}  돔황차 — 개발 지옥에서 도망쳐${NC}"
echo ""
echo -e "  ${MAGENTA}${BOLD}AI Development Automation Tool${NC}  ${DIM}·${NC}  ${MAGENTA}AI 개발 자동화 도구${NC}"
echo -e "  ${DIM}Escape hand-coding — an AI crew builds for you${NC}"
echo -e "  ${DIM}손코딩에서 도망쳐 — AI 크루가 대신 짭니다${NC}"
echo ""
echo -e "${DIM}  ──────────────────────────────────────────────────────${NC}"
echo -e "  ${WHITE}Reinstall${NC}${DIM} / 재설치${NC}:${NC}  ${CYAN}curl -fsSL https://raw.githubusercontent.com/DoCoreTeam/domangcha/main/domangcha/install.sh | bash${NC}"
echo -e "  ${WHITE}or${NC}${DIM} / 또는${NC}:${NC}  ${DIM}curl -sSL https://raw.githubusercontent.com/DoCoreTeam/domangcha/main/domangcha/install.sh | bash${NC}"
echo -e "${DIM}  ──────────────────────────────────────────────────────${NC}"
echo -e "  ${WHITE}Starting installation...${NC}${DIM} / 설치를 시작합니다${NC}"
echo ""
# Let the explicit check below do the reporting rather than aborting on set -e here.
# Run from a checkout (`bash domangcha/install.sh`), install that checkout: cloning main
# instead would install a different version than the one the caller is looking at.
# Piped from curl there is no script path, so the download below is used.
LOCAL_SRC=""
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
    LOCAL_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    [ -f "${LOCAL_SRC}/engine.py" ] && [ -d "${LOCAL_SRC}/evidence" ] || LOCAL_SRC=""
fi
if [ -n "$LOCAL_SRC" ]; then
    # Only the package directory and the Codex plugin files — never the rest of the working tree.
    REPO_ROOT="$(dirname "$LOCAL_SRC")"
    mkdir -p "$TMP_DIR/domangcha-repo/domangcha"
    tar -C "$LOCAL_SRC" -cf - . | tar -C "$TMP_DIR/domangcha-repo/domangcha" -xf -
    for extra in plugins/domangcha .agents/plugins; do
        if [ -d "${REPO_ROOT}/${extra}" ]; then
            mkdir -p "$TMP_DIR/domangcha-repo/${extra}"
            tar -C "${REPO_ROOT}/${extra}" -cf - . | tar -C "$TMP_DIR/domangcha-repo/${extra}" -xf -
        fi
    done
    echo -e "  ${GREEN}✔${NC}  using this checkout: ${REPO_ROOT}${DIM} / 현재 체크아웃으로 설치${NC}"
else
    ( git clone --depth 1 "$DOMANGCHA_REPO" "$TMP_DIR/domangcha-repo" --quiet ) & spin "Downloading DOMANGCHA... / DOMANGCHA 다운로드 중" || true
fi
SRC="${TMP_DIR}/domangcha-repo/domangcha"
if [ ! -d "$SRC" ]; then
    echo -e "  ${RED}✖${NC}  Download failed — nothing to install from ${DOMANGCHA_REPO}${DIM} / 다운로드 실패, 설치할 원본 없음${NC}"
    echo -e "     ${DIM}Check your network or GitHub access, then run the installer again.${NC}"
    exit 1
fi
REPO_SRC="${TMP_DIR}/domangcha-repo"
DOMANGCHA_VERSION=$(cat "${SRC}/VERSION" 2>/dev/null || echo "unknown")

# ── 2. Agents ────────────────────────────────────
step "에이전트 설치" "Installing agents"
mkdir -p "$AGENTS_DIR"
agent_new=0; agent_up=0
for f in "${SRC}/agents/"*.md; do
    name=$(basename "$f")
    if [ -f "${AGENTS_DIR}/${name}" ]; then
        agent_up=$((agent_up + 1))
    else
        agent_new=$((agent_new + 1))
    fi
    cp "$f" "${AGENTS_DIR}/${name}"
done
echo -e "  ${GREEN}✔${NC}  ${GREEN}${agent_new}개 신규(new)${NC}  ${YELLOW}${agent_up}개 업데이트(updated)${NC}  ${DIM}→ ~/.claude/agents/${NC}"

# ── 3. Commands ───────────────────────────────────
step "명령어 설치" "Installing commands"
mkdir -p "$COMMANDS_DIR"
cmd_new=0; cmd_up=0
for f in "${SRC}/commands/"*.md; do
    name=$(basename "$f")
    if [ -f "${COMMANDS_DIR}/${name}" ]; then
        cmd_up=$((cmd_up + 1))
    else
        cmd_new=$((cmd_new + 1))
    fi
    cp "$f" "${COMMANDS_DIR}/${name}"
done
echo -e "  ${GREEN}✔${NC}  ${GREEN}${cmd_new}개 신규(new)${NC}  ${YELLOW}${cmd_up}개 업데이트(updated)${NC}  ${DIM}→ ~/.claude/commands/${NC}"

# ── 4. CEO skills ─────────────────────────────────
step "CEO 스킬 설치" "Installing CEO skills"
ceo_skill_names=""
for skill_dir in "${SRC}/skills/"ceo-*/; do
    [ -d "$skill_dir" ] || continue
    skill_name=$(basename "$skill_dir")
    rm -rf "${SKILLS_DIR:?}/${skill_name}"
    mkdir -p "${SKILLS_DIR}/${skill_name}"
    cp -r "${skill_dir}"* "${SKILLS_DIR}/${skill_name}/"
    ceo_skill_names="${ceo_skill_names}${ceo_skill_names:+ }${skill_name}"
done
if [ -z "$ceo_skill_names" ]; then
    echo -e "  ${RED}✖${NC}  no CEO skill found in the downloaded source${DIM} / 원본에 CEO 스킬 없음${NC}"
    exit 1
fi
echo -e "  ${GREEN}✔${NC}  ${ceo_skill_names}  ${DIM}→ ~/.claude/skills/${NC}"

# Canonical adaptive engine — shared by hooks and runtime adapters.
ENGINE_ROOT="${HOME}/.domangcha"
ENGINE_DIR="${ENGINE_ROOT}/domangcha"
mkdir -p "$ENGINE_DIR"
cp "${SRC}/engine.py" "$ENGINE_DIR/engine.py"
cp "${SRC}/VERSION" "$ENGINE_DIR/VERSION"
rm -rf "${ENGINE_DIR:?}/graphs"
for part in orchestration adapters manifests evidence policies; do
    rm -rf "${ENGINE_DIR:?}/${part}"
    cp -R "${SRC}/${part}" "${ENGINE_DIR}/${part}"
done
touch "$ENGINE_DIR/__init__.py"
echo -e "  ${GREEN}✔${NC}  adaptive engine  ${DIM}→ ~/.domangcha/domangcha/${NC}"

# Codex adapter: managed global block, shared policy remains in ~/.domangcha.
CODEX_DIR="${CODEX_HOME:-${HOME}/.codex}"
mkdir -p "$CODEX_DIR"
CODEX_AGENTS="$CODEX_DIR/AGENTS.md"
python3 - "$CODEX_AGENTS" <<'PYEOF'
import pathlib, re, sys
path = pathlib.Path(sys.argv[1])
existing = path.read_text() if path.exists() else ""
start, end = "<!-- DOMANGCHA:START -->", "<!-- DOMANGCHA:END -->"
block = """<!-- DOMANGCHA:START -->
## DOMANGCHA Adaptive Execution
The DOMANGCHA Codex plugin attaches native lifecycle hooks and a reusable skill.
Follow the injected task ID, DIRECT/LOOP/GRAPH route, and exact completion control command.
Use `$domangcha` to select the skill explicitly. Review plugin hooks once with `/hooks`.
Manual fallback: `python3 ~/.domangcha/domangcha/engine.py route \"<request>\"`.
Shared policy: `~/.domangcha/domangcha/policies/`. Preserve task state on escalation.
Use Codex-native agents and tools; never emulate Claude-specific `Agent(...)` syntax.
Reporting: open with the route card; report LOOP passes and GRAPH phases; never go silent
on long steps; explain an approval before pausing; a user-facing feature is complete only
when `engine.py evidence check` passes; state failures with the next action.
<!-- DOMANGCHA:END -->"""
pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
updated = pattern.sub(block, existing) if pattern.search(existing) else (existing.rstrip() + "\n\n" + block + "\n")
path.write_text(updated.lstrip())
PYEOF
echo -e "  ${GREEN}✔${NC}  Codex adapter  ${DIM}→ ${CODEX_AGENTS}${NC}"

# Native Codex plugin: skill + lifecycle hooks backed by the same canonical engine.
CODEX_MARKETPLACE="${ENGINE_ROOT}/codex-marketplace"
if [ -d "${REPO_SRC}/plugins/domangcha" ] && [ -f "${REPO_SRC}/.agents/plugins/marketplace.json" ]; then
    rm -rf "${CODEX_MARKETPLACE:?}/plugins/domangcha" "${CODEX_MARKETPLACE:?}/.agents/plugins"
    mkdir -p "${CODEX_MARKETPLACE}/plugins" "${CODEX_MARKETPLACE}/.agents/plugins"
    cp -R "${REPO_SRC}/plugins/domangcha" "${CODEX_MARKETPLACE}/plugins/domangcha"
    cp "${REPO_SRC}/.agents/plugins/marketplace.json" "${CODEX_MARKETPLACE}/.agents/plugins/marketplace.json"
    if command -v codex >/dev/null 2>&1; then
        CURRENT_ROOT=$(codex plugin marketplace list --json 2>/dev/null | python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
    print(next((x.get("root", "") for x in data.get("marketplaces", []) if x.get("name") == "domangcha-local"), ""))
except Exception:
    print("")
' || true)
        if [ -n "$CURRENT_ROOT" ] && [ "$CURRENT_ROOT" != "$CODEX_MARKETPLACE" ]; then
            codex plugin marketplace remove domangcha-local --json >/dev/null 2>&1 || true
            CURRENT_ROOT=""
        fi
        if [ -z "$CURRENT_ROOT" ]; then
            codex plugin marketplace add "$CODEX_MARKETPLACE" --json >/dev/null
        fi
        codex plugin add domangcha@domangcha-local --json >/dev/null
        echo -e "  ${GREEN}✔${NC}  Codex native plugin  ${DIM}skill + lifecycle hooks installed${NC}"
        echo -e "  ${YELLOW}⚠${NC}  ${WHITE}Open ${CYAN}/hooks${NC}${WHITE} in Codex once and trust the DOMANGCHA hooks${NC}${DIM} / Codex 에서 /hooks 를 열어 최초 1회 신뢰${NC}"
    else
        echo -e "  ${YELLOW}⚠${NC}  ${WHITE}Codex CLI not detected — plugin bundle staged at ${CODEX_MARKETPLACE}${NC}${DIM} / Codex CLI 미감지, 번들만 준비됨${NC}"
    fi
fi

# Retire what earlier versions shipped and the runtime now provides natively.
# Only DOMANGCHA-owned names are removed; a user's own skills are never touched.
retired=0
for name in dc-rev dc-sec dc-qa dc-res dc-doc dc-seo dc-ana dc-oss dc-tok dc-knw; do
    [ -f "${AGENTS_DIR}/${name}.md" ] && rm -f "${AGENTS_DIR}/${name}.md" && retired=$((retired + 1))
done
for name in clarify design doc feature init knowledge learn plan quality review status test update version; do
    [ -f "${COMMANDS_DIR}/ceo-${name}.md" ] && rm -f "${COMMANDS_DIR}/ceo-${name}.md" && retired=$((retired + 1))
done
for name in ceo-loop ceo-sprint; do
    [ -d "${SKILLS_DIR}/${name}" ] && rm -rf "${SKILLS_DIR:?}/${name}" && retired=$((retired + 1))
done
rm -f "${CLAUDE_DIR}/hooks/domangcha-ralph-loop.py" "${CLAUDE_DIR}/hooks/domangcha-playwright-setup.sh"
echo -e "  ${GREEN}✔${NC}  ${WHITE}${retired} retired items removed — now native${NC}${DIM} / 네이티브로 대체된 항목 ${retired}개 정리${NC}"

# ── 5. CLAUDE.md ──────────────────────────────────
step "CLAUDE.md 업데이트" "Updating CLAUDE.md"
if [ -f "${CLAUDE_DIR}/CLAUDE.md" ]; then
    if grep -qE "^# (docrew|DOCORE|DOMANGCHA|CEO) v" "${CLAUDE_DIR}/CLAUDE.md" 2>/dev/null; then
        echo -e "${YELLOW}  ⟳ CLAUDE.md — updating the DOMANGCHA section${DIM} / DOMANGCHA 섹션 갱신${NC}"
        python3 - "${CLAUDE_DIR}/CLAUDE.md" "${SRC}/CLAUDE.md" <<'PYEOF'
import sys, re
existing = open(sys.argv[1]).read()
docore_new = open(sys.argv[2]).read()
# Match any of the possible section headers
match = re.search(r'^# (docrew|DOCORE|DOMANGCHA|CEO) v', existing, re.MULTILINE)
if match:
    existing = existing[:match.start()].rstrip() + "\n"
with open(sys.argv[1], 'w') as out:
    out.write(existing.rstrip() + "\n\n" + docore_new)
PYEOF
    else
        echo -e "  ${YELLOW}⟳${NC}  updating existing CLAUDE.md${DIM} / 기존 CLAUDE.md 갱신${NC}"
        echo "" >> "${CLAUDE_DIR}/CLAUDE.md"
        cat "${SRC}/CLAUDE.md" >> "${CLAUDE_DIR}/CLAUDE.md"
    fi
else
    cp "${SRC}/CLAUDE.md" "${CLAUDE_DIR}/CLAUDE.md"
    echo -e "  ${GREEN}✔${NC}  CLAUDE.md created${DIM} / 생성 완료${NC}"
fi

# ── 6. Registries ─────────────────────────────────
step "레지스트리 초기화" "Initializing registries"
mkdir -p "${CLAUDE_DIR}/reports"
for file in error-registry skill-registry project-registry decision-log; do
    if [ ! -f "${CLAUDE_DIR}/${file}.md" ]; then
        cp "${SRC}/templates/${file}.md" "${CLAUDE_DIR}/${file}.md"
        echo -e "  ${GREEN}✔${NC}  ${file}.md  ${DIM}신규(new)${NC}"
    else
        echo -e "  ${YELLOW}⏭${NC}  ${file}.md  ${DIM}보존(preserved — user data)${NC}"
    fi
done

# Adaptive documentation is route-dependent. The installer never rewrites a
# user's .gitignore or untracks their documentation.

# ── 7–9. Third-party skill bundles (opt-in) ──────
# ECC, gstack and Superpowers are not needed by the router, the loop, evidence or REA,
# and every installed skill is listed in each session's system prompt. They install only
# when asked: DOMANGCHA_WITH_EXTRAS=1. Bundles already on the machine are never removed.
ECC_STATE="opt-in"
if [ "${DOMANGCHA_WITH_EXTRAS:-0}" != "1" ]; then
    CURRENT_STEP=$((CURRENT_STEP + 2))
    step "추가 스킬 묶음 건너뜀" "Skipping extra skill bundles"
    echo -e "  ${DIM}·${NC}  ECC, gstack, Superpowers not installed — each skill costs context in every session${DIM} / 매 세션 컨텍스트를 차지하므로 설치 안 함${NC}"
    echo -e "  ${DIM}·${NC}  to add them: DOMANGCHA_WITH_EXTRAS=1 bash install.sh${DIM} / 필요하면 이 명령으로 추가${NC}"
else
    # ── 7. ECC
    step "ECC 플러그인 설치" "Installing the ECC plugin"
    echo -e "  ${WHITE}commands excluded — use the /ceo-* orchestrators${NC}${DIM} / 명령어 제외 — /ceo-* 오케스트레이터로 접근${NC}"

    # As a plugin (namespaced ecc:<name>), never copied into ~/.claude/skills — a copy beside
    # the plugin lists every skill and agent twice in each session.
    if ! command -v claude >/dev/null 2>&1; then
        echo -e "  ${YELLOW}⚠${NC}  claude CLI not found — inside Claude Code run: /plugin marketplace add ${ECC_MARKETPLACE} then /plugin install ecc@ecc${DIM} / 나중에 설치${NC}"
    elif case "$(claude plugin list 2>/dev/null || true)" in *ecc@ecc*) true ;; *) false ;; esac; then
        claude plugin update ecc@ecc >/dev/null 2>&1 \
            && echo -e "  ${GREEN}✔${NC}  ECC plugin updated${DIM} / 업데이트${NC}" \
            || echo -e "  ${YELLOW}⚠${NC}  ECC plugin update failed — keeping the installed version${DIM} / 기존 버전 유지${NC}"
    else
        claude plugin marketplace add "$ECC_MARKETPLACE" >/dev/null 2>&1 || true
        claude plugin install ecc@ecc >/dev/null 2>&1 \
            && echo -e "  ${GREEN}✔${NC}  ECC plugin installed  ${DIM}→ ecc:<name>${NC}" \
            || echo -e "  ${YELLOW}⚠${NC}  ECC plugin install failed — inside Claude Code run: /plugin install ecc@ecc${DIM} / 설치 실패${NC}"
    fi
    # Captured before matching: grep -q closing a pipe early fails the pipeline under pipefail.
    case "$( (command -v claude >/dev/null 2>&1 && claude plugin list 2>/dev/null) || true)" in
        *ecc@ecc*) ECC_STATE="plugin" ;;
    esac

    # ── 8. gstack ─────────────────────────────────────
    step "gstack 업데이트" "Updating gstack"
    ( git_update_or_clone "$GSTACK_REPO" "${SKILLS_DIR}/gstack" "gstack" 2>&1 ) & spin "Syncing gstack... / gstack 동기화 중" || \
        echo -e "  ${YELLOW}⚠${NC}  gstack was not synced — the rest of the install continues without it${DIM} / gstack 미동기화, 나머지 설치는 계속${NC}"

    # ── 9. Superpowers ────────────────────────────────
    step "Superpowers 설치" "Installing Superpowers"
    SUPERPOWERS_INSTALLED=false

    # Method 1: Claude Code plugin CLI
    if command -v claude &>/dev/null; then
        if claude plugin marketplace list 2>/dev/null | grep -q "obra/superpowers-marketplace"; then
            echo -e "  ${YELLOW}⟳${NC}  superpowers-marketplace already registered${DIM} / 이미 등록됨${NC}"
        else
            claude plugin marketplace add obra/superpowers-marketplace 2>/dev/null && \
                echo -e "${GREEN}  ✅ Marketplace registered: obra/superpowers-marketplace${NC}" || true
        fi

        if claude plugin list 2>/dev/null | grep -q "superpowers"; then
            if claude plugin update superpowers 2>/dev/null; then
                echo -e "${GREEN}  ✅ superpowers updated via plugin${NC}"
            else
                echo -e "${YELLOW}  ⚠ superpowers update command failed — keeping the version already installed${NC}"
            fi
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

    # Asked for explicitly — fail loudly if not installed
    if [ "$SUPERPOWERS_INSTALLED" = false ]; then
        echo ""
        echo -e "${RED}  ╔══════════════════════════════════════════╗${NC}"
        echo -e "${RED}  ║  ❌  SUPERPOWERS INSTALL FAILED${DIM} / 설치 실패 ║${NC}"
        echo -e "${RED}  ║  Requested by DOMANGCHA_WITH_EXTRAS=1    ║${NC}"
        echo -e "${RED}  ╚══════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "  Install manually inside Claude Code${DIM} / Claude Code 내에서 수동 설치:${NC}"
        echo -e "    \033[1;33m/plugin marketplace add obra/superpowers-marketplace\033[0m"
        echo -e "    \033[1;33m/plugin install superpowers@superpowers-marketplace\033[0m"
        exit 1
    fi
fi

# ── 10. Hooks ─────────────────────────────────────
step "훅 설치 (자동 테스트 + CEO 검토)" "Installing hooks (auto-test + CEO review)"
mkdir -p "${CLAUDE_DIR}/hooks"
cp "${SRC}/hooks/domangcha-post-edit.sh" "${CLAUDE_DIR}/hooks/domangcha-post-edit.sh"
cp "${SRC}/hooks/domangcha-stop.sh"      "${CLAUDE_DIR}/hooks/domangcha-stop.sh"
cp "${SRC}/hooks/domangcha-ceo-enforcer.py" "${CLAUDE_DIR}/hooks/domangcha-ceo-enforcer.py"
cp "${SRC}/hooks/domangcha-rtk.py"       "${CLAUDE_DIR}/hooks/domangcha-rtk.py"
chmod +x "${CLAUDE_DIR}/hooks/domangcha-post-edit.sh"
chmod +x "${CLAUDE_DIR}/hooks/domangcha-stop.sh"
chmod +x "${CLAUDE_DIR}/hooks/domangcha-ceo-enforcer.py"
echo -e "  ${GREEN}✔${NC}  domangcha-post-edit.sh  ${DIM}auto-test + auto-fix${DIM} / 자동 테스트·수정${NC}"
echo -e "  ${GREEN}✔${NC}  domangcha-stop.sh        ${DIM}validation + evidence gate${DIM} / 검증 + 증거 게이트${NC}"
echo -e "  ${GREEN}✔${NC}  domangcha-ceo-enforcer.py  ${DIM}CEO pipeline enforcer${DIM} / CEO 파이프라인 강제${NC}"

# ── 11. Output style ──────────────────────────────
# Shorter replies cut output tokens; selected in settings.json below unless the user chose one.
step "출력 스타일 설치" "Installing the output style"
mkdir -p "${CLAUDE_DIR}/output-styles"
cp "${SRC}/output-styles/domangcha.md" "${CLAUDE_DIR}/output-styles/domangcha.md"
echo -e "  ${GREEN}✔${NC}  output style DOMANGCHA  ${DIM}terse replies; route, evidence, failures kept whole${DIM} / 짧은 답${NC}"

# ── 12. rtk (compress command output) ─────────────
# rtk's Apache-2.0 "oss" build, pinned and checksum-checked; a copy already on PATH is used as is.
step "rtk 설치 (명령 출력 압축)" "Installing rtk (command output compression)"
RTK_VERSION="1.0.1"
RTK_BIN="${HOME}/.domangcha/bin/rtk"
RTK_HOOK=0
case "$(uname -s)/$(uname -m)" in
    Darwin/arm64)   RTK_ASSET="rtk-oss-aarch64-apple-darwin.tar.gz"
                    RTK_SHA="4a4d9d09656ff29423336aa506e680afc3f7b6dafe84f0194a1c9a523a3c80e1" ;;
    Darwin/x86_64)  RTK_ASSET="rtk-oss-x86_64-apple-darwin.tar.gz"
                    RTK_SHA="2cf4d6dd2cabccbc74aa6aba2a48e60aad85b1a31e3d740e6ca0b2fa0060b06a" ;;
    Linux/x86_64)   RTK_ASSET="rtk-oss-x86_64-unknown-linux-musl.tar.gz"
                    RTK_SHA="a44e8ffc43981100b4ddf1710399a1649a6c874591aa6d0c0727fe6cbd983c41" ;;
    Linux/aarch64|Linux/arm64)
                    RTK_ASSET="rtk-oss-aarch64-unknown-linux-gnu.tar.gz"
                    RTK_SHA="ee24a43dac9162de55fea8460b5efcd56d401ec28b5117c921bffa8a57bc136e" ;;
    *)              RTK_ASSET="" ; RTK_SHA="" ;;
esac
sha256_of() {
    if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | cut -d' ' -f1
    else shasum -a 256 "$1" | cut -d' ' -f1; fi
}
if [ "${DOMANGCHA_SKIP_RTK:-0}" = "1" ]; then
    echo -e "  ${DIM}·${NC}  skipped by DOMANGCHA_SKIP_RTK=1${DIM} / 건너뜀${NC}"
elif [ -x "$RTK_BIN" ] && case "$("$RTK_BIN" --version 2>/dev/null || true)" in "rtk ${RTK_VERSION}"*) true ;; *) false ;; esac; then
    RTK_HOOK=1
    echo -e "  ${DIM}·${NC}  rtk ${RTK_VERSION} already installed${DIM} / 이미 설치됨${NC}"
elif command -v rtk >/dev/null 2>&1; then
    RTK_HOOK=1
    echo -e "  ${DIM}·${NC}  $(rtk --version 2>/dev/null || echo rtk) already on PATH — kept${DIM} / 기존 rtk 사용${NC}"
elif [ -z "$RTK_ASSET" ]; then
    echo -e "  ${YELLOW}⚠${NC}  no rtk build for $(uname -s)/$(uname -m) — skipped${DIM} / 지원 안 되는 플랫폼${NC}"
else
    RTK_TGZ="${TMP_DIR}/${RTK_ASSET}"
    if curl -fsSL --max-time 120 -o "$RTK_TGZ" "https://github.com/rtk-ai/rtk/releases/download/v${RTK_VERSION}/${RTK_ASSET}" 2>/dev/null \
        && [ "$(sha256_of "$RTK_TGZ")" = "$RTK_SHA" ] \
        && mkdir -p "${TMP_DIR}/rtk" "$(dirname "$RTK_BIN")" \
        && tar xzf "$RTK_TGZ" -C "${TMP_DIR}/rtk" rtk 2>/dev/null \
        && [ -f "${TMP_DIR}/rtk/rtk" ] && [ ! -L "${TMP_DIR}/rtk/rtk" ] \
        && install -m 755 "${TMP_DIR}/rtk/rtk" "$RTK_BIN" 2>/dev/null; then
        RTK_HOOK=1
        echo -e "  ${GREEN}✔${NC}  rtk ${RTK_VERSION} installed  ${DIM}→ ~/.domangcha/bin/rtk (Apache-2.0, checksum verified)${NC}"
    else
        echo -e "  ${YELLOW}⚠${NC}  rtk ${RTK_VERSION} not downloaded or checksum mismatch — skipped${DIM} / 건너뜀${NC}"
    fi
fi

# ── 13. settings.json ─────────────────────────────
step "settings.json 훅 주입" "Injecting hooks into settings.json"
python3 - "${CLAUDE_DIR}" "${RTK_HOOK}" "${DOMANGCHA_SKIP_STYLE:-0}" "${HOME}/.domangcha/.output-style-set" <<'PYEOF'
import sys, json, os, re

claude_dir = sys.argv[1]
rtk_hook = sys.argv[2] == "1"
skip_style = sys.argv[3] == "1"
style_marker = sys.argv[4]

def entries(event):
    """A settings.json hook list, read defensively: a hand-edited file must not abort the install."""
    value = hooks.get(event, [])
    return [h for h in value if isinstance(h, dict)] if isinstance(value, list) else []

def commands(entry):
    subs = entry.get("hooks", [])
    return [sub.get("command", "") for sub in subs if isinstance(sub, dict)] if isinstance(subs, list) else []
hooks_dir  = os.path.join(claude_dir, "hooks")
settings_path = os.path.join(claude_dir, "settings.json")

DOMANGCHA_POST = {
    "matcher": "Write|Edit|MultiEdit",
    "hooks": [{"type": "command", "command": f'bash "{hooks_dir}/domangcha-post-edit.sh"'}]
}
# async: true — CEO quality review runs in background so session ends immediately
DOMANGCHA_STOP = {
    "hooks": [{"type": "command", "command": f'bash "{hooks_dir}/domangcha-stop.sh"', "timeout": 120}]
}
# PreToolUse(Bash) — rtk compresses command output before the model reads it
DOMANGCHA_RTK = {
    "matcher": "Bash",
    "hooks": [{"type": "command", "command": f'python3 "{hooks_dir}/domangcha-rtk.py"'}]
}
DOMANGCHA_ENFORCER = {
    "matcher": "",
    "hooks": [{"type": "command", "command": f'python3 "{hooks_dir}/domangcha-ceo-enforcer.py"'}]
}
# domangcha-stop-checks.js: TypeScript check (ECC plugin)
# Runs FIRST so it can read the edited-files accumulator before format-typecheck clears it
DOMANGCHA_STOP_CHECKS_PATH = os.path.join(claude_dir, "scripts", "hooks", "domangcha-stop-checks.js")
DOMANGCHA_STOP_CHECKS = {
    "matcher": "*",
    "hooks": [{"type": "command", "command": f'node "{DOMANGCHA_STOP_CHECKS_PATH}"', "timeout": 120}],
    "description": "DOMANGCHA Stop Guard: TypeScript BLOCKING check"
} if os.path.exists(DOMANGCHA_STOP_CHECKS_PATH) else None

settings = {}
if os.path.exists(settings_path):
    try:
        with open(settings_path) as f:
            settings = json.load(f)
    except Exception as exc:
        # Never replace a settings file we cannot read: that would erase the user's config.
        print(f"  ✖  {settings_path} is not valid JSON ({exc}); fix it and rerun — hooks not injected")
        sys.exit(0)

hooks = settings.get("hooks", {}) if isinstance(settings, dict) and isinstance(settings.get("hooks", {}), dict) else {}
if not isinstance(settings, dict):
    print(f"  ✖  {settings_path} is not a JSON object; fix it and rerun — hooks not injected")
    sys.exit(0)

# UserPromptSubmit — CEO pipeline enforcer (idempotent)
upr = [h for h in entries("UserPromptSubmit") if not any("domangcha-ceo-enforcer" in c for c in commands(h))]
upr.insert(0, DOMANGCHA_ENFORCER)
hooks["UserPromptSubmit"] = upr

# PostToolUse — remove old DOMANGCHA hook, append fresh
post = [h for h in entries("PostToolUse") if not any("domangcha-post-edit" in c for c in commands(h))]
post.append(DOMANGCHA_POST)
hooks["PostToolUse"] = post

# Stop — remove old DOMANGCHA hooks (including the retired ralph loop), re-inject in order
stop = [h for h in entries("Stop") if not any(
    ("domangcha-stop" in c or "domangcha-ralph-loop" in c) for c in commands(h)
)]
if DOMANGCHA_STOP_CHECKS:
    stop.insert(0, DOMANGCHA_STOP_CHECKS)
stop.append(DOMANGCHA_STOP)
hooks["Stop"] = stop

# PreToolUse — ours only when rtk is present and the user has no rtk hook of their own
pre = [h for h in entries("PreToolUse") if not any("domangcha-rtk" in c for c in commands(h))]
users_rtk = any(re.search(r"\brtk\b", c) for h in pre for c in commands(h))
if rtk_hook and not users_rtk:
    pre.append(DOMANGCHA_RTK)
if pre or "PreToolUse" in hooks:
    hooks["PreToolUse"] = pre

# Output style — once, and only when the user has not chosen one; clearing it later sticks
if not skip_style and not settings.get("outputStyle") and not os.path.exists(style_marker):
    settings["outputStyle"] = "DOMANGCHA"
    os.makedirs(os.path.dirname(style_marker), exist_ok=True)
    open(style_marker, "w").close()

settings["hooks"] = hooks
tmp_path = settings_path + ".domangcha-tmp"
with open(tmp_path, "w") as f:
    json.dump(settings, f, indent=2)
os.replace(tmp_path, settings_path)  # atomic: a crash never leaves a half-written settings.json
print("  ✔  settings.json hooks injected, merged safely / 훅 주입 완료")
PYEOF

# ── 14. REA (extract features from other products) ──
# Browser verification is the ego-browser skill when installed, else Claude-in-Chrome; no Playwright or Chromium is installed.
step "REA MCP 연결" "Connecting REA MCP"
REA_PACKAGE="rea-agents@6.4.0"
if [ "${DOMANGCHA_SKIP_REA:-0}" = "1" ]; then
    echo -e "  ${DIM}·${NC}  skipped by DOMANGCHA_SKIP_REA=1${DIM} / 건너뜀${NC}"
elif ! command -v claude >/dev/null 2>&1; then
    echo -e "  ${YELLOW}⚠${NC}  claude CLI not found — run later: claude mcp add --scope user rea -- npx -y ${REA_PACKAGE} mcp${DIM} / 나중에 실행${NC}"
elif REA_EXISTING=$(claude mcp get rea 2>/dev/null); then
    if printf '%s' "$REA_EXISTING" | grep -q "${REA_PACKAGE}"; then
        echo -e "  ${DIM}·${NC}  rea MCP already registered${DIM} / 이미 등록됨${NC}"
    else
        echo -e "  ${YELLOW}⚠${NC}  an MCP server named rea exists but is not ${REA_PACKAGE} — left untouched; check: claude mcp get rea${DIM} / 기존 rea 유지${NC}"
    fi
elif claude mcp add --scope user rea -- npx -y "${REA_PACKAGE}" mcp >/dev/null 2>&1; then
    echo -e "  ${GREEN}✔${NC}  rea MCP registered  ${DIM}→ ${REA_PACKAGE} (MIT)${NC}"
else
    echo -e "  ${YELLOW}⚠${NC}  rea MCP registration failed — run: claude mcp add --scope user rea -- npx -y ${REA_PACKAGE} mcp${DIM} / 등록 실패${NC}"
fi

# ── 15. taste-skill (UI/UX art direction) ──
# One upstream skill, pinned to a commit and linked, not copied; an existing install is kept.
step "taste-skill 연결" "Linking taste-skill"
TASTE_REPO="https://github.com/leonxlnx/taste-skill.git"
TASTE_TAG="v2.1.3"
TASTE_SHA="63aba5f43b5056758b15bbe7d683da8c86a7a7ad"
TASTE_DIR="${HOME}/.domangcha/vendor/taste-skill"
TASTE_LINK="${SKILLS_DIR}/design-taste-frontend"
TASTE_STATE="not installed"
if [ "${DOMANGCHA_SKIP_TASTE:-0}" = "1" ]; then
    echo -e "  ${DIM}·${NC}  skipped by DOMANGCHA_SKIP_TASTE=1${DIM} / 건너뜀${NC}"
elif [ -e "$TASTE_LINK" ] || [ -L "$TASTE_LINK" ]; then
    TASTE_STATE="installed"
    echo -e "  ${DIM}·${NC}  design-taste-frontend already installed — left untouched${DIM} / 기존 설치 유지${NC}"
else
    rm -rf "$TASTE_DIR"
    mkdir -p "$(dirname "$TASTE_DIR")"
    if git clone -q --depth 1 --branch "$TASTE_TAG" "$TASTE_REPO" "$TASTE_DIR" 2>/dev/null \
        && [ "$(git -C "$TASTE_DIR" rev-parse HEAD)" = "$TASTE_SHA" ] \
        && [ -d "$TASTE_DIR/skills/taste-skill" ] \
        && ln -s "$TASTE_DIR/skills/taste-skill" "$TASTE_LINK" 2>/dev/null; then
        TASTE_STATE="installed"
        echo -e "  ${GREEN}✔${NC}  design-taste-frontend linked  ${DIM}→ taste-skill ${TASTE_TAG} (MIT; Node 22+ and Chrome)${NC}"
    else
        rm -rf "$TASTE_DIR"
        echo -e "  ${YELLOW}⚠${NC}  taste-skill ${TASTE_TAG} not fetched, not the pinned commit, or not linkable — skipped${DIM} / 건너뜀${NC}"
    fi
fi

# ── 16. Git hooks ─────────────────────────────────
step "git 훅 설치 (자동 재설치)" "Installing git hooks (auto-reinstall)"
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
    echo -e "  ${GREEN}✔${NC}  post-merge  ${DIM}auto-reinstall on git pull${DIM} / git pull 시 자동 재설치${NC}"
    echo -e "  ${GREEN}✔${NC}  post-checkout  ${DIM}auto-install on git clone${DIM} / git clone 시 자동 설치${NC}"
else
    echo -e "  ${YELLOW}⚠${NC}  git repo root not found, skipping git hooks${DIM} / git 레포 루트 없음, git 훅 건너뜀${NC}"
fi

# ── 17. Mark installed version ────────────────────
echo "${DOMANGCHA_VERSION}" > "${CLAUDE_DIR}/domangcha-installed-version"
rm -f "${CLAUDE_DIR}/.domangcha-version-cache"

# ── Done — clear + full screen ───────────────────
clear 2>/dev/null || true  # no terminal (CI, TERM=dumb) must not abort the install
INSTALLED_AGENTS=$((agent_new + agent_up))
INSTALLED_COMMANDS=$((cmd_new + cmd_up))
python3 - "${DOMANGCHA_VERSION}" "${INSTALLED_AGENTS}" "${INSTALLED_COMMANDS}" "${ECC_STATE}" "${TASTE_STATE}" "${RTK_HOOK}" <<'PYEOF'
import sys, unicodedata, shutil

v, n_agents, n_commands, ecc_state, taste_state, rtk_hook = sys.argv[1:7]
cols = shutil.get_terminal_size((80, 24)).columns

def dw(s):
    return sum(2 if unicodedata.east_asian_width(c) in ('W','F') else 1 for c in s)

CY="\033[0;36m"; CB="\033[0;36m\033[1m"; GR="\033[0;32m"
MG="\033[0;35m"; WH="\033[1;37m"; DM="\033[2m"; NC="\033[0m"; BD="\033[1m"

# ── ASCII banner (wide: full art / narrow: text) ──
wide = cols >= 86
if wide:
    print(f"\n{CB}")
    for line in [
        "  ██████╗  ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗ ██████╗  ██████╗ ██╗  ██╗ █████╗ ",
        "  ██╔══██╗██╔═══██╗████╗ ████║██╔══██╗████╗  ██║██╔════╝ ██╔════╝ ██║  ██║██╔══██╗",
        "  ██║  ██║██║   ██║██╔████╔██║███████║██╔██╗ ██║██║  ███╗██║      ███████║███████║",
        "  ██║  ██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║   ██║██║      ██╔══██║██╔══██║",
        "  ██████╔╝╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║╚██████╔╝╚██████╗ ██║  ██║██║  ██║",
        "  ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝",
    ]: print(line)
    print(NC)
else:
    print(f"\n{CB}  🚗💨 DOMANGCHA{NC}")

print(f"{WH}{BD}  Escape development hell. DOMANGCHA is your getaway car.  🚗💨{NC}")
print(f"{DM}  돔황차 — 개발 지옥에서 도망쳐{NC}")
print(f"  {MG}{BD}AI Development Automation Tool{NC}  {DM}·  AI 개발 자동화 도구{NC}")
print()

# ── Version block (wide: big digits / narrow: inline) ──
if wide:
    digits = {
        '0':["┌─┐","│ │","└─┘"],'1':[" ┐ "," │ "," ┴ "],'2':["┌─┐","┌─┘","└─┘"],
        '3':["┌─┐"," ─┤","└─┘"],'4':["┬ ┬","└─┤","  ┴"],'5':["┌─ ","└─┐","└─┘"],
        '6':["┌─ ","├─┐","└─┘"],'7':["┌─┐","  │","  ╵"],'8':["┌─┐","├─┤","└─┘"],
        '9':["┌─┐","└─┤","  ┘"],'.':["   ","   "," · "],'-':["   ","───","   "],
        'v':["   ","\\/ ","   "],
    }
    print(f"{GR}{BD}")
    lines = ["  ","  ","  "]
    for c in "v" + v:
        d = digits.get(c, ["   ","   ","   "])
        for i in range(3): lines[i] += d[i] + " "
    for l in lines: print(l)
    print(NC)
else:
    print(f"  {GR}{BD}v{v}{NC}\n")

# ── Info box (width-adaptive) ──
rows = [
    (WH, "DIRECT · LOOP · GRAPH → validation  ·  minimum reliable orchestration"),
    (DM, "요청마다 최소한의 경로를 고르고 검증까지 이어서 실행"),
    (WH, "by docore  (Michael Dohyeon Kim · KDC CEO)"),
    (DM, "github.com/DoCoreTeam/domangcha"),
    (GR, "refresh the harness:  curl -fsSL .../install.sh | bash"),
    (DM, "하네스 갱신"),
]
max_content = max(dw(t) for _, t in rows)
box_inner = min(max_content + 4, cols - 6)
bar = "─" * (box_inner)
def row(col, text):
    pad = box_inner - dw(text) - 4
    return f"  {MG}│{NC}  {col}{text}{NC}{' ' * max(pad,0)}  {MG}│{NC}"
print(f"  {MG}┌{bar}┐{NC}")
for col, text in rows:
    print(row(col, text))
print(f"  {MG}└{bar}┘{NC}")
print()

# ── Installed items ──
sep = "  " + "─" * min(cols - 6, 56)
print(f"{WH}{BD}  What's installed{NC}{DM} / 설치된 항목{NC}")
print(f"{DM}{sep}{NC}")
items = [
    ("~/.claude/agents/dc-*.md",   f"{n_agents} DC-* worker agents"),
    ("~/.claude/commands/ceo*.md", f"{n_commands} /ceo-* commands, all optional"),
    ("~/.claude/skills/",          ("CEO skills (incl. ceo-standards); ECC plugin (ecc:<name>), gstack, Superpowers" if ecc_state == "plugin" else "CEO skills (incl. ceo-standards) — extras opt-in")),
    ("~/.claude/hooks/ + settings.json", "auto-test, router, evidence gate"),
    ("~/.claude/output-styles/domangcha.md", "output style DOMANGCHA — shorter replies (/config to change)"),
    *([("rtk + PreToolUse(Bash) hook", "compresses command output before the model reads it")] if rtk_hook == "1" else []),
    ("~/.claude/CLAUDE.md",        "auto-loaded by Claude Code"),
    ("~/.domangcha/domangcha/policies/", "execution and evidence policy"),
    ("~/.domangcha/domangcha/evidence/", "state · trace · provenance adapters (engine.py evidence)"),
    ("claude mcp: rea",            "REA — extract features from other products"),
    *([("~/.claude/skills/design-taste-frontend", "taste-skill — UI/UX art direction, checked in a browser")] if taste_state == "installed" else []),
    ("~/.domangcha/codex-marketplace", "Codex plugin + skill + lifecycle hooks"),
]
for path, desc in items:
    print(f"  {GR}✔{NC}  \033[1;33m{path}{NC}")
    print(f"     {DM}{desc}{NC}")
print(f"{DM}{sep}{NC}")
print()

# ── Getting started ──
print(f"{WH}{BD}  🚀 Getting started{NC}{DM} / 시작하기{NC}")
print(f"  {DM}1.{NC} {WH}Open Claude Code in any project{NC}{DM}  / 아무 프로젝트에서 Claude Code 열기{NC}")
print(f"  {DM}2.{NC} {WH}Just say what you want — no slash command needed{NC}{DM}  / 하고 싶은 일을 그냥 말하면 됩니다{NC}")
print(f"  {DM}3.{NC} {CY}\"Build me a todo app\"{NC}{DM}  → DIRECT/LOOP/GRAPH chosen for you / 자동 선택{NC}")
print()
print(f"  {WH}{BD}📦 Update / Reinstall{NC}{DM} / 업데이트·재설치{NC}")
print(f"  {GR}  npx domangcha{NC}  {DM}← inside a project / 프로젝트 안에서{NC}")
print(f"  {DM}  curl -sSL https://raw.githubusercontent.com/DoCoreTeam/domangcha/main/domangcha/install.sh | bash{NC}")
print()
print(f"  {WH}{BD}📋 Optional shortcuts{NC}{DM} / 선택 사항인 단축키{NC}")
cmds = [
    ("/ceo \"task\"", "explicit routing, never required"),
    ("/ceo-ralph",    "minimum LOOP route (runs on native /loop)"),
    ("/ceo-ship",     "ship after the evidence check"),
]
for cmd, desc in cmds:
    print(f"  {CY}{cmd:<20}{NC}  {DM}{desc}{NC}")
print()
print(f"  {MG}{BD}Escape development hell. 🚗💨{NC}{DM}  개발 지옥에서 도망쳐, 돔황차가 데려다 줄게{NC}")
print(f"  {DM}Escape development hell. DOMANGCHA is your getaway car.{NC}")
print()
PYEOF
