#!/bin/bash
# Measures the input tokens one real Claude Code turn costs, so the README's token
# numbers can be re-run instead of trusted. Needs the `claude` CLI, logged in.
#   scripts/measure-tokens.sh            # this machine, empty folder
#   scripts/measure-tokens.sh <dir>      # inside a project (e.g. a loop project)
set -euo pipefail
DIR="${1:-$(mktemp -d)}"
MODEL="${MODEL:-haiku}"
EMPTY_MCP=$(mktemp)
echo '{"mcpServers":{}}' > "$EMPTY_MCP"
trap 'rm -f "$EMPTY_MCP"' EXIT

turn() {
    local label="$1"; shift
    (cd "$DIR" && claude -p "Answer in one word: hello" --model "$MODEL" --output-format json \
        --no-session-persistence --max-turns 1 "$@") | python3 -c '
import json, sys
u = json.load(sys.stdin)["usage"]
total = u["input_tokens"] + u["cache_creation_input_tokens"] + u["cache_read_input_tokens"]
print("%-34s %8d input tokens" % (sys.argv[1], total))' "$label"
}

echo "folder: $DIR  model: $MODEL"
turn "everything (as you use it)"
turn "without MCP servers"         --strict-mcp-config --mcp-config "$EMPTY_MCP"
turn "without skills"              --disable-slash-commands
turn "without user-level settings" --setting-sources project,local
