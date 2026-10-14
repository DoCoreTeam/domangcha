#!/usr/bin/env python3
"""DOMANGCHA eval: router accuracy and evidence-gate on/off.

route     — does the deterministic router pick the expected route? (harness on only;
            without it there is no route to measure)
evidence  — each scenario ends with the model claiming "done". OFF accepts the claim,
            as a harness without the gate does. ON accepts it only when `check` passes.
            A pass is the verdict matching the truth (expect_ok).

Usage: python3 domangcha/evals/run.py [--json]
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from domangcha.engine import route_request  # noqa: E402
from domangcha.evidence.config import EvidenceConfig  # noqa: E402
from domangcha.evidence.gate import check  # noqa: E402
from domangcha.evidence.ledger import Ledger  # noqa: E402
from domangcha.evidence.state import StateError, StateForcer  # noqa: E402
from domangcha.evidence.trace import Tracer  # noqa: E402

PY = sys.executable
STATES = ("loading", "empty", "error", "no-permission")
MARKER = "eval-42"


def config_for(failing_enter: str = "") -> dict:
    states = {}
    for name in STATES:
        code = "raise SystemExit(1)" if name == failing_enter else "pass"
        states[name] = {"enter": [PY, "-c", code], "exit": [PY, "-c", "pass"]}
    db = [PY, "-c", "import sys; print('row', sys.argv[1]) if sys.argv[1] == %r else None" % MARKER, "{marker}"]
    return {"states": states, "logs": ["server.log"], "db": db}


def play(scenario: str, workspace: Path) -> dict:
    action, _, target = scenario.partition(":")
    raw = config_for(target if action == "failing_enter" else "")
    (workspace / ".domangcha").mkdir(parents=True, exist_ok=True)
    (workspace / ".domangcha/evidence.json").write_text(json.dumps(raw))
    (workspace / "server.log").write_text("POST /items %s\n" % MARKER)
    config = EvidenceConfig.load(workspace)
    ledger = Ledger(workspace)
    ledger.start(scenario)
    if action == "nothing":
        return check(ledger.current(), config)
    forcer = StateForcer(workspace, config, ledger)
    for name in STATES:
        if action == "capture_outside" and name == target:
            ledger.record("observation", name + " screen", source="chrome:shot", key="state:" + name)
        try:
            forcer.enter(name)
        except StateError:
            ledger.record("observation", name + " screen", source="chrome:shot", key="state:" + name)
            continue
        if not ((action == "skip_state" and name == target) or (action == "capture_outside" and name == target)):
            ledger.record("observation", name + " screen", source="chrome:shot", key="state:" + name)
        if not (action == "leave_active" and name == target):
            forcer.exit(name)
    if action != "no_trace":
        marker = "eval-99" if action == "no_db_row" else MARKER
        network = [{"url": "/items", "status": 201, "body": marker}]
        if action == "network_only":
            raw["db"] = [PY, "-c", "pass", "{marker}"]
            (workspace / ".domangcha/evidence.json").write_text(json.dumps(raw))
            config = EvidenceConfig.load(workspace)
        Tracer(workspace, config, ledger).trace(marker, network)
    return check(ledger.current(), config)


def run_route(cases: list) -> list:
    return [{**c, "got": route_request(c["prompt"])["route"]} for c in cases]


def run_evidence(cases: list) -> list:
    results = []
    for case in cases:
        with tempfile.TemporaryDirectory() as folder:
            verdict = play(case["scenario"], Path(folder))
        results.append({**case, "on_ok": verdict["ok"], "off_ok": True, "missing": verdict["missing"]})
    return results


def main() -> int:
    cases = json.loads((Path(__file__).with_name("cases.json")).read_text())
    routes = run_route(cases["route"])
    evidence = run_evidence(cases["evidence"])
    route_pass = sum(r["got"] == r["expect"] for r in routes)
    on_pass = sum(e["on_ok"] == e["expect_ok"] for e in evidence)
    off_pass = sum(e["off_ok"] == e["expect_ok"] for e in evidence)
    report = {
        "route": {"pass": route_pass, "total": len(routes),
                  "misses": [{k: r[k] for k in ("id", "prompt", "expect", "got")} for r in routes if r["got"] != r["expect"]]},
        "evidence": {"on": on_pass, "off": off_pass, "total": len(evidence),
                     "caught_by_gate": [e["id"] for e in evidence if not e["expect_ok"] and not e["on_ok"]],
                     "wrong_on": [e["id"] for e in evidence if e["on_ok"] != e["expect_ok"]]},
    }
    if "--json" in sys.argv:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("route     %d/%d" % (route_pass, len(routes)))
        for miss in report["route"]["misses"]:
            print("  ✗ %(id)s %(prompt)s → %(got)s (expected %(expect)s)" % miss)
        print("evidence  on %d/%d · off %d/%d  (off = no gate: every \"done\" is accepted as claimed)"
              % (on_pass, len(evidence), off_pass, len(evidence)))
        for e in evidence:
            print("  %s %s on=%s off=%s %s" % ("✓" if e["on_ok"] == e["expect_ok"] else "✗", e["id"],
                                              e["on_ok"], e["off_ok"], ",".join(e["missing"])))
    return 0 if on_pass == len(evidence) else 1


if __name__ == "__main__":
    raise SystemExit(main())
