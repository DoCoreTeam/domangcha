#!/bin/bash
set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  🏢 DOCORE Installer v1.0.0${NC}"
echo -e "${GREEN}  16 AI Agents Orchestration for Claude Code${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

INSTALL_DIR="${HOME}/.claude/skills/docore"
REPO_URL="https://github.com/docore/docore.git"

# Install or update
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}DOCORE already installed. Updating...${NC}"
    cd "$INSTALL_DIR"
    git pull origin main
else
    echo -e "${GREEN}Installing DOCORE...${NC}"
    mkdir -p "${HOME}/.claude/skills"
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# Create global registries if not exist
mkdir -p "${HOME}/.claude/reports"

for file in error-registry skill-registry project-registry decision-log; do
    if [ ! -f "${HOME}/.claude/${file}.md" ]; then
        cp "$INSTALL_DIR/templates/${file}.md" "${HOME}/.claude/${file}.md"
        echo -e "${GREEN}  ✅ ${file}.md created${NC}"
    else
        echo -e "${YELLOW}  ⏭️ ${file}.md already exists, skipping${NC}"
    fi
done

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  ✅ DOCORE installed successfully!${NC}"
echo ""
echo -e "  📁 Location: $INSTALL_DIR"
echo -e "  🤖 Agents:   16 (CEO + 15 Workers)"
echo ""
echo -e "  🚀 ${YELLOW}Usage:${NC}"
echo -e "     1. Open Claude Code in your project"
echo -e "     2. ${YELLOW}/ceo-init${NC}              Initialize project"
echo -e "     3. ${YELLOW}/ceo \"build a todo app\"${NC}  Start development"
echo -e ""
echo -e "  📋 All commands:"
echo -e "     ${YELLOW}/ceo \"task\"${NC}     Full pipeline (all 16 agents)"
echo -e "     ${YELLOW}/ceo-init${NC}       Project setup + harness"
echo -e "     ${YELLOW}/ceo-status${NC}     Show current status"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
