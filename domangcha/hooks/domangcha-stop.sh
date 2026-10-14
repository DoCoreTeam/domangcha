#!/usr/bin/env bash
# Claude Stop adapter. Canonical validation is deterministic and runtime-neutral.
set -u

PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
ENGINE=""

if [ -n "${DOMANGCHA_ENGINE:-}" ] && [ -f "$DOMANGCHA_ENGINE" ]; then
    ENGINE="$DOMANGCHA_ENGINE"  # explicit engine, e.g. a source checkout under evaluation
elif [ -f "$PROJECT_ROOT/domangcha/engine.py" ]; then
    ENGINE="$PROJECT_ROOT/domangcha/engine.py"
elif [ -f "$HOME/.domangcha/domangcha/engine.py" ]; then
    ENGINE="$HOME/.domangcha/domangcha/engine.py"
fi

[ -z "$ENGINE" ] && exit 0

# Repository metadata validation applies only to the DOMANGCHA source repo.
# The manifest is what actually identifies that repo: an unrelated project may
# legitimately keep its own domangcha/VERSION as an application version marker.
if [ -f "$PROJECT_ROOT/domangcha/manifests/agents.json" ] && [ -f "$PROJECT_ROOT/domangcha/VERSION" ] && [ -f "$PROJECT_ROOT/package.json" ]; then
    OUTPUT=$(python3 "$ENGINE" validate --root "$PROJECT_ROOT" 2>&1)
    STATUS=$?
    if [ "$STATUS" -ne 0 ]; then
        echo "[DOMANGCHA STOP VALIDATION FAILED]" >&2
        echo "$OUTPUT" >&2
        exit 2
    fi
fi

# Evidence gate: an open evidence run must pass before the turn may end.
# A run committed to git came with the clone, not this session, so it never blocks.
RUN_FILE="$PROJECT_ROOT/.domangcha/evidence/current.json"
if [ -f "$RUN_FILE" ] && ! git -C "$PROJECT_ROOT" ls-files --error-unmatch "$RUN_FILE" >/dev/null 2>&1; then
    OUTPUT=$(python3 "$ENGINE" evidence check --workspace "$PROJECT_ROOT" 2>&1)
    STATUS=$?
    if [ "$STATUS" -ne 0 ]; then
        echo "[DOMANGCHA EVIDENCE INCOMPLETE] finish the run, or close it: engine.py evidence close --accept-gaps \"reason\" (no .domangcha/evidence.json yet? run evidence init first)" >&2
        echo "$OUTPUT" >&2
        exit 2
    fi
fi

exit 0
