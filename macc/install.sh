#!/bin/bash
set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

CLAUDE_DIR="${HOME}/.claude"
AGENTS_DIR="${CLAUDE_DIR}/agents"
COMMANDS_DIR="${CLAUDE_DIR}/commands"
SKILLS_DIR="${CLAUDE_DIR}/skills"

MACC_REPO="https://github.com/DoCoreTeam/domacc.git"
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

# ── 1. MACC ──────────────────────────────────
echo -e "${BLUE}[1/5] Downloading MACC...${NC}"
git clone --depth 1 "$MACC_REPO" "$TMP_DIR/macc-repo" --quiet
SRC="${TMP_DIR}/macc-repo/macc"
MACC_VERSION=$(cat "${SRC}/VERSION" 2>/dev/null || echo "unknown")

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  👔 MACC Installer v${MACC_VERSION}${NC}"
echo -e "${GREEN}  The AI Chief Executive for Claude Code${NC}"
echo -e "${GREEN}  16 Agents. 15 Commands. Full Pipeline.${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}  ✅ Downloaded v${MACC_VERSION}${NC}"

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
        echo -e "${YELLOW}  ⟳ CLAUDE.md — updating MACC section${NC}"
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

# ── 10. MACC Hooks — auto-test + auto-fix ────────
echo ""
echo -e "${BLUE}[Extra] Installing MACC hooks → ~/.claude/hooks/${NC}"
mkdir -p "${CLAUDE_DIR}/hooks"
cp "${SRC}/hooks/macc-post-edit.sh" "${CLAUDE_DIR}/hooks/macc-post-edit.sh"
cp "${SRC}/hooks/macc-stop.sh"      "${CLAUDE_DIR}/hooks/macc-stop.sh"
chmod +x "${CLAUDE_DIR}/hooks/macc-post-edit.sh"
chmod +x "${CLAUDE_DIR}/hooks/macc-stop.sh"
echo -e "${GREEN}  ✅ macc-post-edit.sh (auto-test + auto-fix)${NC}"
echo -e "${GREEN}  ✅ macc-stop.sh (CEO quality review)${NC}"

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
MACC_STOP = {
    "hooks": [{"type": "command", "command": f'bash "{hooks_dir}/macc-stop.sh"'}]
}

settings = {}
if os.path.exists(settings_path):
    try:
        with open(settings_path) as f:
            settings = json.load(f)
    except Exception:
        settings = {}

hooks = settings.get("hooks", {})

# PostToolUse — remove old MACC hook, append fresh
post = hooks.get("PostToolUse", [])
post = [h for h in post if not any("macc-post-edit" in sub.get("command","") for sub in h.get("hooks",[]))]
post.append(MACC_POST)
hooks["PostToolUse"] = post

# Stop — remove old MACC hook, append fresh
stop = hooks.get("Stop", [])
stop = [h for h in stop if not any("macc-stop" in sub.get("command","") for sub in h.get("hooks",[]))]
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

# ── Done ─────────────────────────────────────────
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  ✅ CEO installed/updated successfully!${NC}"
echo ""
echo -e "  Updated:"
echo -e "    ${YELLOW}~/.claude/agents/dc-*.md${NC}          ← 16 MACC agents"
echo -e "    ${YELLOW}~/.claude/commands/ceo*.md${NC}        ← /ceo /ceo-init /ceo-status"
echo -e "    ${YELLOW}~/.claude/skills/ceo-system/${NC}      ← CEO orchestration brain"
echo -e "    ${YELLOW}~/.claude/skills/ecc:*/  ${NC}         ← 183 ECC skills (no commands — use /ceo-*)"
echo -e "    ${YELLOW}~/.claude/skills/gstack/ ${NC}         ← gstack tools"
echo -e "    ${YELLOW}~/.claude/skills/superpowers/${NC}     ← superpowers (or via plugin)"
echo -e "    ${YELLOW}~/.claude/hooks/macc-*.sh${NC}         ← auto-test + CEO review hooks"
echo -e "    ${YELLOW}~/.claude/settings.json${NC}           ← hooks injected (merged)"
echo -e "    ${YELLOW}playwright MCP${NC}                    ← browser testing (headless/headed)"
echo -e "    ${YELLOW}~/.claude/CLAUDE.md${NC}               ← auto-loaded by Claude Code"
echo -e "    ${YELLOW}~/.claude/*-registry.md${NC}           ← preserved (user data)"
echo ""
echo -e "  🚀 ${YELLOW}Getting started:${NC}"
echo -e "     1. Open Claude Code in any project"
echo -e "     2. ${YELLOW}/ceo-init${NC}               Initialize project"
echo -e "     3. ${YELLOW}/ceo \"build a todo app\"${NC}   Start full pipeline"
echo ""
echo -e "  📋 Commands:"
echo -e "     ${YELLOW}/ceo \"task\"${NC}      Q&A → full pipeline (16 agents)"
echo -e "     ${YELLOW}/ceo-init${NC}        Project setup + harness"
echo -e "     ${YELLOW}/ceo-status${NC}      Show current status"
echo ""
echo -e "  🔁 ${YELLOW}Auto-hooks active:${NC}"
echo -e "     PostToolUse(Write/Edit) → test + auto-fix"
echo -e "     Stop                    → CEO quality review"
echo ""
echo -e "  🌐 ${YELLOW}Browser testing:${NC}"
echo -e "     Playwright MCP registered — use browser_* tools in Claude Code"
echo -e "     Headed mode: claude mcp add playwright -s user npx @playwright/mcp --headed"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
