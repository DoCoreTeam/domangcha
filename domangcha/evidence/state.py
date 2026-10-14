"""Forces the four states a screen must handle, so each can be captured for real.

`enter` runs the project's command that puts the server/DB into a state (seed nothing,
delay responses, fail an endpoint, drop a permission) and opens a capture window.
A capture recorded as `state:<name>` only counts inside that window. `exit` restores.
"""
from __future__ import annotations

from pathlib import Path

from .config import EvidenceConfig
from .ledger import Ledger
from .runner import run


class StateError(RuntimeError):
    pass


class StateForcer:
    def __init__(self, workspace: Path, config: EvidenceConfig, ledger: Ledger):
        self.workspace = workspace
        self.config = config
        self.ledger = ledger

    def _spec(self, name: str):
        spec = self.config.states.get(name)
        if spec is None:
            raise StateError("state %r is not configured in .domangcha/evidence.json" % name)
        return spec

    def enter(self, name: str) -> dict:
        spec = self._spec(name)
        run_state = self.ledger.current()
        if name in run_state["active_states"]:
            raise StateError("state %r is already active" % name)
        # Mark active before running: a command that fails halfway may still have changed the
        # system, so it must stay restorable by `exit`/`reset` and flagged by the gate.
        self.ledger.save({**run_state, "active_states": run_state["active_states"] + [name]})
        ok, output = run(spec["enter"], self.workspace)
        if not ok:
            self.ledger.record("unknown", "could not force %s: %s" % (name, output),
                               key="forced:" + name, adapter=True)
            raise StateError("entering %s failed: %s — run `evidence state exit %s` to restore" % (name, output, name))
        return self.ledger.record("observation", "forced %s" % name,
                                  source="cmd:" + " ".join(spec["enter"])[:200], key="forced:" + name, adapter=True)

    def exit(self, name: str) -> dict:
        spec = self._spec(name)
        if name not in self.ledger.current()["active_states"]:
            raise StateError("state %r is not active" % name)
        ok, output = run(spec["exit"], self.workspace)
        if not ok:
            self.ledger.record("unknown", "could not restore from %s: %s" % (name, output),
                               key="released:" + name, adapter=True)
            raise StateError("leaving %s failed: %s — the system may still be in that state" % (name, output))
        claim = self.ledger.record("observation", "restored from %s" % name,
                                   source="cmd:" + " ".join(spec["exit"])[:200], key="released:" + name,
                                   adapter=True)
        run_state = self.ledger.current()
        self.ledger.save({**run_state, "active_states": [s for s in run_state["active_states"] if s != name]})
        return claim

    def reset(self) -> list:
        return [self.exit(name) for name in list(self.ledger.current()["active_states"])]
