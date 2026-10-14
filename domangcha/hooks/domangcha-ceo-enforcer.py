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


REPORTING_CONTRACT = """진행 상황 보고 규칙 (기본 활성 · 끄려면 사용자가 명시적으로 요청):
1. 응답 시작에 위 라우트 카드를 그대로 보여준다. 사용자가 "지금 무엇을 왜 하는지"를 먼저 알게 한다.
2. 진행은 네이티브로 보고한다 — 단계는 TodoWrite, LOOP는 /loop 회차, GRAPH는 Workflow phase.
   DOMANGCHA는 루프·그래프·체크포인트를 따로 돌리지 않는다.
3. 30초 이상 걸리는 단계는 침묵하지 않는다. 시작·중간·끝을 짧게 알린다.
4. 파괴적·되돌릴 수 없는 작업 앞에서는 무엇을·왜 승인받는지 말하고 AskUserQuestion으로 멈춘다.
5. 사용자 화면이 바뀌는 기능은 증거 런이 통과해야 완료다: `{engine} evidence start` →
   state enter/exit(4상태 캡처) → trace <marker> → check. 완료 보고에 run_id와 check 결과를 인용한다.
6. 톤: 사용자의 언어로, 친절하고 간결하게. 실패는 감추지 말고 있는 그대로 + 다음 조치를 함께 말한다."""

ENGINE_HINT = "python3 ~/.domangcha/domangcha/engine.py"

CEO_COMMAND = re.compile(r"^\s*/ceo\b", re.IGNORECASE)

YIELD_MESSAGE = """[DOMANGCHA] 이 프로젝트는 프로젝트 루프로 운영됩니다 (.loop/ 감지).
전역 라우터는 물러나고 프로젝트 규정인 LOOP.md 가 우선합니다.
지시 기록과 다음 행동은 프로젝트 훅(scripts/loop.mjs)이 이어서 출력합니다.
하네스가 필요하면 /ceo 로 시작하세요 — 그때는 이 라우터가 다시 맡습니다."""

ESCALATION_NOTICE = """[DOMANGCHA] /ceo 로 프로젝트 루프에서 하네스로 올라갑니다.
이번 요청에 한해 아래 라우트를 따르고, 끝나면 LOOP.md 로 돌아갑니다.
결과는 loop pass 또는 loop plan revise 로 프로젝트 플랜에 반영하세요."""



def _message(result: dict, card: str) -> str:
    return """[DOMANGCHA ADAPTIVE ROUTER]
{card}

route={route} score={score} approval_required={approval}

{contract}

Use the canonical route. DIRECT has no planner graph, recursive loop, mandatory DOC, or agent fan-out.
LOOP runs on the native /loop skill (bounded PLAN→EXECUTE→VALIDATE→ACT).
GRAPH runs on the native Workflow tool; destructive effects require approval via AskUserQuestion.
Do not use legacy SMALL/MEDIUM/FULL-PIPELINE prose to override this decision.
""".format(
        card=card,
        route=result["route"],
        score=result["score"],
        approval=str(result["approval_required"]).lower(),
        contract=REPORTING_CONTRACT.format(engine=ENGINE_HINT),
    )


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
