"""`engine.py evidence ...` — the one entry point every runtime (Claude, Codex) calls.

Exit codes: 0 ok, 1 gate not satisfied, 2 invalid input or adapter failure.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .config import CONFIG_PATH, TEMPLATE, ConfigError, EvidenceConfig
from .gate import check
from .ledger import KINDS, ClaimError, Ledger
from .state import StateError, StateForcer
from .trace import TraceError, Tracer
from .trust import confirm_on_terminal, require_trust
from ..orchestration.security import safe_path

ADAPTER_ERRORS = (ClaimError, ConfigError, StateError, TraceError)


def register(sub) -> None:
    parser = sub.add_parser("evidence", help="prove a feature works: state, trace, provenance")
    actions = parser.add_subparsers(dest="action", required=True)
    actions.add_parser("init", help="write a .domangcha/evidence.json template")
    actions.add_parser("trust", help="approve this project's evidence commands (interactive terminal only)")
    start = actions.add_parser("start", help="open an evidence run")
    start.add_argument("--label", default="")
    record = actions.add_parser("record", help="record a tagged claim")
    record.add_argument("kind", choices=KINDS)
    record.add_argument("statement")
    record.add_argument("--source")
    record.add_argument("--from", dest="sources", nargs="+")
    record.add_argument("--basis")
    record.add_argument("--key")
    state = actions.add_parser("state", help="force or restore loading/empty/error/no-permission")
    state.add_argument("op", choices=("enter", "exit", "reset"))
    state.add_argument("name", nargs="?")
    trace = actions.add_parser("trace", help="bind browser request → server log → stored row")
    trace.add_argument("marker")
    trace.add_argument("--network", help="JSON file inside the workspace with captured network entries, or -")
    trace.add_argument("--label", default="default", help="stable name for this flow, so runs diff")
    actions.add_parser("check", help="is the open run complete?")
    close = actions.add_parser("close", help="close the run and diff it against the previous one")
    close.add_argument("--accept-gaps", metavar="REASON", help="close an incomplete run, recording why")
    actions.add_parser("diff", help="diff the open run against the previous one")
    for action in actions.choices.values():
        action.add_argument("--workspace", default=".")


def _network(source, workspace: Path):
    if not source:
        return []
    if source == "-":
        raw = sys.stdin.read()
    else:
        try:
            raw = safe_path(workspace, Path(source)).read_text(encoding="utf-8")
        except ValueError:
            raise TraceError("--network file must be inside the workspace") from None
    data = json.loads(raw)
    entries = data if isinstance(data, list) else data.get("requests", [])
    if not isinstance(entries, list):
        raise TraceError("network JSON must be a list of entries")
    return entries


def _dispatch(args, workspace: Path) -> tuple:
    ledger = Ledger(workspace)
    if args.action == "init":
        path = workspace / CONFIG_PATH
        if path.exists():
            raise ConfigError("%s already exists" % CONFIG_PATH)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(TEMPLATE, indent=2) + "\n", encoding="utf-8")
        ignore = ledger.root / ".gitignore"
        ignore.parent.mkdir(parents=True, exist_ok=True)
        ignore.write_text("# runs can quote logs and rows; keep them local unless you mean to share\n*\n")
        return {"written": str(path), "next": "edit it, then run `evidence trust` in your own terminal"}, 0
    if args.action == "trust":
        return {"trusted": confirm_on_terminal(workspace)}, 0
    if args.action == "start":
        return ledger.start(args.label), 0
    if args.action == "record":
        return ledger.record(args.kind, args.statement, args.source, args.sources, args.basis, args.key), 0
    if args.action == "diff":
        return ledger.diff(), 0
    config = EvidenceConfig.load(workspace)
    if args.action in ("state", "trace"):
        require_trust(workspace)  # these run the project's commands
    if args.action == "state":
        forcer = StateForcer(workspace, config, ledger)
        if args.op == "reset":
            return {"restored": forcer.reset()}, 0
        if not args.name:
            raise StateError("state %s needs a state name" % args.op)
        return getattr(forcer, args.op)(args.name), 0
    if args.action == "trace":
        bundle = Tracer(workspace, config, ledger).trace(args.marker, _network(args.network, workspace), args.label)
        return bundle, 0 if bundle["complete"] else 1
    verdict = check(ledger.current(), config)
    if args.action == "check":
        return verdict, 0 if verdict["ok"] else 1
    if not verdict["ok"] and not args.accept_gaps:
        raise ClaimError("run is incomplete (%s); finish it or pass --accept-gaps REASON"
                         % ", ".join(verdict["missing"]))
    if not verdict["ok"]:
        ledger.record("inference", "closed with gaps: " + ", ".join(verdict["missing"]),
                      basis=args.accept_gaps, key="gaps")
    closed = ledger.close()
    return {"run_id": closed["run_id"], "check": verdict, "diff": closed["diff"]}, 0


def run(args) -> int:
    try:
        payload, code = _dispatch(args, Path(args.workspace).resolve())
    except ADAPTER_ERRORS as exc:
        print("[DOMANGCHA evidence] %s" % exc, file=sys.stderr)
        return 2
    except (OSError, json.JSONDecodeError) as exc:
        print("[DOMANGCHA evidence] %s: %s" % (type(exc).__name__, exc), file=sys.stderr)
        return 2
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return code
