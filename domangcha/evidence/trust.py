"""A project's evidence.json runs commands, so a cloned repo must not run them unasked.

Trust is the sha256 of the config, recorded per absolute workspace path under the user's
home. Any edit to the config revokes it. `evidence trust` asks on the controlling terminal,
which a model's tool call does not have, so the person approves, not the model.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Optional

from .config import CONFIG_PATH, ConfigError

TRUST_FILE = Path(".domangcha") / "trusted-evidence.json"


def _store(home: Optional[Path]) -> Path:
    return (home or Path.home()) / TRUST_FILE


def _digest(workspace: Path) -> str:
    try:
        return hashlib.sha256((workspace / CONFIG_PATH).read_bytes()).hexdigest()
    except FileNotFoundError:
        raise ConfigError("%s missing — run `engine.py evidence init`" % CONFIG_PATH) from None


def _load(home: Optional[Path]) -> dict:
    try:
        return json.loads(_store(home).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def is_trusted(workspace: Path, home: Optional[Path] = None) -> bool:
    return _load(home).get(str(workspace.resolve())) == _digest(workspace)


def record_trust(workspace: Path, home: Optional[Path] = None) -> str:
    digest = _digest(workspace)
    store = _store(home)
    store.parent.mkdir(parents=True, exist_ok=True)
    data = {**_load(home), str(workspace.resolve()): digest}
    handle, tmp = tempfile.mkstemp(dir=str(store.parent), prefix=".trust-")
    with os.fdopen(handle, "w", encoding="utf-8") as out:
        out.write(json.dumps(data, indent=2))
    os.replace(tmp, str(store))
    return digest


def require_trust(workspace: Path) -> None:
    if not is_trusted(workspace):
        raise ConfigError(
            "%s is not trusted yet (new or edited). Review its commands, then run in your own terminal: "
            "python3 ~/.domangcha/domangcha/engine.py evidence trust --workspace %s"
            % (CONFIG_PATH, workspace.resolve()))


def confirm_on_terminal(workspace: Path) -> str:
    config = (workspace / CONFIG_PATH).read_text(encoding="utf-8")
    try:
        with open("/dev/tty", "r+") as tty:
            tty.write(config + "\nRun these commands for %s? Type 'trust' to approve: " % workspace.resolve())
            tty.flush()
            answer = tty.readline().strip()
    except OSError:
        raise ConfigError("evidence trust needs an interactive terminal; run it yourself, not through the agent") from None
    if answer != "trust":
        raise ConfigError("not trusted")
    return record_trust(workspace)
