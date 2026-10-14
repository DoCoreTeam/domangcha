"""Binds one user action end to end: browser request → stored row, with the server log alongside.

The caller types a unique marker into the UI, captures the network entries with
Claude-in-Chrome, and passes them here. The adapter finds the marker in the server
logs and asks the database for the row holding it. Every link becomes a claim; a
missing link becomes `unknown`, never a silent pass. Claims are keyed by a stable
label, not the marker, so the next run's trace diffs against this one.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

from ..orchestration.security import redact, safe_path
from .config import EvidenceConfig
from .ledger import Ledger
from .runner import run

# Starts alphanumeric (never a flag), carries a digit (never a common word), no ':' (keys use it).
MARKER = re.compile(r"^(?=.*\d)[A-Za-z0-9][A-Za-z0-9_.@-]{5,127}$")
LABEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")
LOG_TAIL_LINES = 5000
MAX_MATCHES = 20


class TraceError(ValueError):
    pass


class Tracer:
    def __init__(self, workspace: Path, config: EvidenceConfig, ledger: Ledger):
        self.workspace = workspace
        self.config = config
        self.ledger = ledger

    def trace(self, marker: str, network: List[Dict[str, Any]], label: str = "default") -> Dict[str, Any]:
        if not MARKER.match(marker or ""):
            raise TraceError("marker must be 6-128 chars of [A-Za-z0-9_.@-], start alphanumeric, and contain a digit")
        if not LABEL.match(label or ""):
            raise TraceError("label must match %s" % LABEL.pattern)
        key = "trace:" + label
        hits = [entry for entry in network if marker in json.dumps(entry, ensure_ascii=False)]
        log_lines = self._logs(marker)
        rows, db_note = self._db(marker)
        network_id = self._link(key + ":network", hits, "request carrying %s" % marker, "chrome:network")
        self._link(key + ":log", log_lines, "server logged %s" % marker, "log:" + ",".join(self.config.logs))
        db_id = self._link(key + ":db", rows, "stored row for %s" % marker,
                           "db:" + " ".join(self.config.db)[:200], db_note)
        complete = bool(network_id and db_id)
        if complete:
            via = "with" if log_lines else "without"
            self.ledger.record("derivation", "%s went from the browser to the database (%s a server log line)"
                               % (marker, via), sources=[network_id, db_id], key=key, adapter=True)
        return redact({"marker": marker, "label": label, "complete": complete,
                       "network": hits, "log": log_lines, "db": rows})

    def _link(self, key: str, found: list, what: str, source: str, note: str = "") -> str:
        if found:
            return self.ledger.record("observation", "%s (%d)" % (what, len(found)),
                                      source=source, key=key, adapter=True)["id"]
        self.ledger.record("unknown", "no %s%s" % (what, (" — " + note) if note else ""), key=key, adapter=True)
        return ""

    def _logs(self, marker: str) -> List[str]:
        found: List[str] = []
        for name in self.config.logs:
            try:
                path = safe_path(self.workspace, Path(name))
            except ValueError:
                raise TraceError("log path %r leaves the workspace" % name) from None
            try:
                lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[-LOG_TAIL_LINES:]
            except OSError:
                continue
            found.extend(line for line in lines if marker in line)
        return found[:MAX_MATCHES]

    def _db(self, marker: str):
        if not self.config.db:
            return [], "db command not configured"
        argv = [part.replace("{marker}", marker) for part in self.config.db]
        ok, output = run(argv, self.workspace)
        if not ok:
            return [], output
        return [line for line in output.splitlines() if line.strip()][:MAX_MATCHES], ""
