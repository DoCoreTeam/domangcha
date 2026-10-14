#!/usr/bin/env python3
"""Claude UserPromptSubmit adapter for the canonical DOMANGCHA router."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path


def _load_engine():
    candidates = [
        Path(__file__).resolve().parents[2],
        Path.home() / ".domangcha",
        Path.home() / ".claude" / "domangcha",
        Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())),
    ]
    for root in candidates:
        if (root / "domangcha" / "engine.py").exists():
            sys.path.insert(0, str(root))
            break
        if (root / "engine.py").exists() and (root / "orchestration").is_dir():
            sys.path.insert(0, str(root.parent))
            break
    else:
        raise RuntimeError("DOMANGCHA engine is not installed")
    from domangcha.engine import route_request
    from domangcha.orchestration.status import StatusReporter
    return route_request, StatusReporter


CEO_COMMAND = re.compile(r"^\s*/ceo\b", re.IGNORECASE)

YIELD_MESSAGE = """[DOMANGCHA] 이 프로젝트는 프로젝트 루프로 운영됩니다 (.loop/ 감지).
전역 라우터는 물러나고 프로젝트 규정인 LOOP.md 가 우선합니다.
지시 기록과 다음 행동은 프로젝트 훅(scripts/loop.mjs)이 이어서 출력합니다.
하네스가 필요하면 /ceo 로 시작하세요 — 그때는 이 라우터가 다시 맡습니다."""

ESCALATION_NOTICE = """[DOMANGCHA] /ceo 로 프로젝트 루프에서 하네스로 올라갑니다.
이번 요청에 한해 아래 라우트를 따르고, 끝나면 LOOP.md 로 돌아갑니다.
결과는 loop pass 또는 loop plan revise 로 프로젝트 플랜에 반영하세요."""



# The reporting contract is static, so it lives once in the installed CLAUDE.md
# (loaded and prompt-cached per session) instead of being re-sent with every prompt.
# DIRECT — most prompts — gets one line; LOOP and GRAPH get the card plus one line.
NATIVE_RUNTIME = {
    "LOOP": "run on the native /loop skill (bounded PLAN→EXECUTE→VALIDATE→ACT)",
    "GRAPH": "run on the native Workflow tool; destructive effects need AskUserQuestion approval",
}


def _message(result: dict, card: str) -> str:
    route = result["route"]
    if route == "DIRECT":
        reasons = "; ".join(r for r in result.get("reasons") or []
                            if not r.startswith("deterministic complexity"))
        return "[DOMANGCHA ADAPTIVE ROUTER] ⚡ DIRECT score=%s%s" % (
            result["score"], " · " + reasons if reasons else "")
    return "[DOMANGCHA ADAPTIVE ROUTER]\n%s\nroute=%s score=%s approval_required=%s · %s" % (
        card, route, result["score"], str(result["approval_required"]).lower(),
        NATIVE_RUNTIME.get(route, ""))


def _project_loop_root() -> Path | None:
    """A project running the v3 lightweight loop owns its own protocol."""
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))
    if (root / ".loop").is_dir() and (root / "scripts" / "loop.mjs").exists():
        return root
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        prompt = payload.get("prompt", "")
        if not prompt:
            return 0
        loop_root = _project_loop_root()
        escalating = loop_root is not None
        if escalating and not CEO_COMMAND.match(prompt):
            print(YIELD_MESSAGE)
            return 0
        route_request, reporter = _load_engine()
        result = route_request(prompt)
        if escalating:
            print(ESCALATION_NOTICE)
        print(_message(result, reporter().route_card(result)))
        return 0
    except Exception as exc:
        print("[DOMANGCHA ROUTER DEGRADED] %s. Use the safest applicable route." % exc)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
