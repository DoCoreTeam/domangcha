"""Provenance ledger: every claim about the product says how it is known.

observation  something a tool saw (screenshot, network entry, log line, db row); needs `source`
derivation   follows from earlier observations or derivations; needs `sources`
inference    a judgement beyond what was seen; needs `basis`, and nothing may derive from it
unknown      what could not be established; recorded instead of being silently dropped

Claims are grouped into runs. Closing a run diffs it against the previous one by claim key,
so "worked last time, unknown now" surfaces as a regression rather than disappearing.
"""
from __future__ import annotations

import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..orchestration.security import redact

KINDS = ("observation", "derivation", "inference", "unknown")
GROUNDED = {"observation", "derivation"}
# Keys only the adapters may write; a hand-recorded one would forge the gate.
ADAPTER_PREFIXES = ("forced:", "released:", "trace:")
AUTO_KEY = re.compile(r"^c\d+$")


class ClaimError(ValueError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write(path: Path, payload: Dict[str, Any]) -> None:
    """Atomic write through a fresh temp file, so a planted symlink is never followed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".write-")
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as out:
            out.write(json.dumps(redact(payload), ensure_ascii=False, indent=2))
        os.replace(tmp, str(path))
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


class Ledger:
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.root = workspace / ".domangcha" / "evidence"
        self.current_path = self.root / "current.json"
        self.runs = self.root / "runs"

    def _guard(self) -> None:
        """Refuse a store that a cloned repo redirected outside the workspace."""
        base = self.workspace.resolve()
        for part in (self.workspace / ".domangcha", self.root, self.runs):
            if part.is_symlink() or (part.exists() and base not in part.resolve().parents):
                raise ClaimError("%s is a symlink or leaves the workspace; refusing to write" % part)

    def start(self, label: str = "") -> Dict[str, Any]:
        self._guard()
        if self.current_path.exists():
            raise ClaimError("a run is already open; close it first")
        run = {
            "run_id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f"),
            "label": label,
            "started_at": _now(),
            "claims": [],
            "active_states": [],
        }
        _write(self.current_path, run)
        return run

    def current(self) -> Dict[str, Any]:
        try:
            return json.loads(self.current_path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raise ClaimError("no open run; start one with `evidence start`") from None

    def save(self, run: Dict[str, Any]) -> None:
        self._guard()
        _write(self.current_path, run)

    def record(
        self,
        kind: str,
        statement: str,
        source: Optional[str] = None,
        sources: Optional[List[str]] = None,
        basis: Optional[str] = None,
        key: Optional[str] = None,
        adapter: bool = False,
    ) -> Dict[str, Any]:
        if key and key.startswith(ADAPTER_PREFIXES) and not adapter:
            raise ClaimError("keys starting with %s are written by the adapters only" % ", ".join(ADAPTER_PREFIXES))
        run = self.current()
        claim = self._validate(run, kind, statement, source, sources or [], basis)
        claim["id"] = "c%d" % (len(run["claims"]) + 1)
        claim["key"] = key or claim["id"]
        claim["at"] = _now()
        self.save({**run, "claims": run["claims"] + [claim]})
        return claim

    @staticmethod
    def _validate(run, kind, statement, source, sources, basis) -> Dict[str, Any]:
        if kind not in KINDS:
            raise ClaimError("kind must be one of %s" % ", ".join(KINDS))
        if not statement or not statement.strip():
            raise ClaimError("statement is required")
        claim: Dict[str, Any] = {"kind": kind, "statement": statement.strip()}
        if kind == "observation":
            if not source:
                raise ClaimError("an observation needs --source (the tool or artifact that saw it)")
            claim["source"] = source
        if kind == "derivation":
            if not sources:
                raise ClaimError("a derivation needs --from claim ids")
            by_id = {c["id"]: c for c in run["claims"]}
            for ref in sources:
                if ref not in by_id:
                    raise ClaimError("derivation refers to unknown claim %s" % ref)
                if by_id[ref]["kind"] not in GROUNDED:
                    raise ClaimError("derivation cannot rest on %s claim %s" % (by_id[ref]["kind"], ref))
            claim["from"] = list(sources)
        if kind == "inference":
            if not basis:
                raise ClaimError("an inference needs --basis (why you believe it)")
            claim["basis"] = basis
        return claim

    def previous(self) -> Optional[Dict[str, Any]]:
        closed = sorted(self.runs.glob("*.json")) if self.runs.is_dir() else []
        return json.loads(closed[-1].read_text(encoding="utf-8")) if closed else None

    def close(self) -> Dict[str, Any]:
        run = self.current()
        report = self.diff(current=run)
        closed = {**run, "closed_at": _now(), "diff": report}
        self._guard()
        _write(self.runs / (run["run_id"] + ".json"), closed)
        self.current_path.unlink()
        return closed

    def diff(self, previous: Optional[Dict[str, Any]] = None,
             current: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        before = previous if previous is not None else (self.previous() or {"claims": []})
        after = current if current is not None else self.current()
        # Positional ids (c1, c2…) name different claims in different runs; only chosen keys compare.
        old = {c["key"]: c for c in before.get("claims", []) if not AUTO_KEY.match(c["key"])}
        new = {c["key"]: c for c in after.get("claims", []) if not AUTO_KEY.match(c["key"])}
        changed = sorted(k for k in old.keys() & new.keys()
                         if (old[k]["kind"], old[k]["statement"]) != (new[k]["kind"], new[k]["statement"]))
        regressed = sorted(k for k in changed
                           if old[k]["kind"] in GROUNDED and new[k]["kind"] not in GROUNDED)
        return {
            "against": before.get("run_id"),
            "added": sorted(new.keys() - old.keys()),
            "removed": sorted(old.keys() - new.keys()),
            "changed": changed,
            "regressed": regressed,
        }
