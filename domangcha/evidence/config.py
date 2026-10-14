"""Per-project adapter configuration, read from `.domangcha/evidence.json`.

Commands are argv lists and never pass through a shell, so a marker or a state name
cannot become shell syntax.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

CONFIG_PATH = Path(".domangcha") / "evidence.json"
REQUIRED_STATES: Tuple[str, ...] = ("loading", "empty", "error", "no-permission")


class ConfigError(ValueError):
    pass


def _argv(value: object, where: str) -> List[str]:
    if not isinstance(value, list) or not value or not all(isinstance(x, str) and x for x in value):
        raise ConfigError("%s must be a non-empty argv list of strings" % where)
    return list(value)


@dataclass(frozen=True)
class EvidenceConfig:
    states: Dict[str, Dict[str, List[str]]] = field(default_factory=dict)
    logs: Tuple[str, ...] = ()
    db: Tuple[str, ...] = ()
    required_states: Tuple[str, ...] = REQUIRED_STATES

    @classmethod
    def load(cls, workspace: Path) -> "EvidenceConfig":
        path = workspace / CONFIG_PATH
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raise ConfigError("%s missing — run `engine.py evidence init`" % CONFIG_PATH) from None
        except json.JSONDecodeError as exc:
            raise ConfigError("%s invalid json: %s" % (CONFIG_PATH, exc)) from None
        return cls.parse(raw)

    @classmethod
    def parse(cls, raw: object) -> "EvidenceConfig":
        if not isinstance(raw, dict):
            raise ConfigError("evidence config must be an object")
        states = {}
        for name, spec in (raw.get("states") or {}).items():
            if not isinstance(spec, dict):
                raise ConfigError("states.%s must be an object" % name)
            states[name] = {
                "enter": _argv(spec.get("enter"), "states.%s.enter" % name),
                "exit": _argv(spec.get("exit"), "states.%s.exit" % name),
            }
        logs = raw.get("logs") or []
        if not isinstance(logs, list) or not all(isinstance(x, str) for x in logs):
            raise ConfigError("logs must be a list of paths")
        db = _argv(raw["db"], "db") if raw.get("db") else []
        required = raw.get("required_states", list(REQUIRED_STATES))
        if not isinstance(required, list) or not all(isinstance(x, str) for x in required):
            raise ConfigError("required_states must be a list of names")
        return cls(states=states, logs=tuple(logs), db=tuple(db), required_states=tuple(required))


TEMPLATE = {
    "states": {
        name: {"enter": ["REPLACE", "command that forces " + name], "exit": ["REPLACE", "command that restores"]}
        for name in REQUIRED_STATES
    },
    "logs": ["REPLACE/path/to/server.log"],
    "db": ["REPLACE", "query that prints the row holding", "{marker}"],
}
