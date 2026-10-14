"""Decides whether a run proves the feature works. Pure function over the ledger."""
from __future__ import annotations

import re
from typing import Any, Dict, List

from .config import EvidenceConfig

TRACE_KEY = re.compile(r"^trace:[^:]+$")


def _captured_in_window(claims: List[Dict[str, Any]], name: str) -> bool:
    window_open = False
    for claim in claims:
        if claim["key"] == "forced:" + name and claim["kind"] == "observation":
            window_open = True
        elif claim["key"] == "released:" + name:
            window_open = False
        elif window_open and claim["key"] == "state:" + name and claim["kind"] == "observation":
            return True
    return False


def check(run: Dict[str, Any], config: EvidenceConfig) -> Dict[str, Any]:
    claims = run.get("claims", [])
    missing = ["state:" + name for name in config.required_states if not _captured_in_window(claims, name)]
    missing += ["active:" + name for name in run.get("active_states", [])]
    if not any(c["kind"] == "derivation" and TRACE_KEY.match(c["key"]) for c in claims):
        missing.append("trace")
    latest = {c["key"]: c for c in claims}
    unknown = sorted(k for k, c in latest.items() if c["kind"] == "unknown")
    return {"run_id": run.get("run_id"), "ok": not missing, "missing": missing, "unknown": unknown}
