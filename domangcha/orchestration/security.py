import re
from pathlib import Path
from typing import Any, Dict


SECRET_KEY = re.compile(r"(token|secret|password|api[_-]?key|authorization)", re.I)
SECRET_VALUE = re.compile(
    r"(?i)(bearer\s+)[A-Za-z0-9._~+/=-]+"
    r"|((?:password|passwd|secret|token|api[_-]?key|access[_-]?key|session(?:id)?)[\"']?\s*[=:]\s*[\"']?)[^\s\"',;&]+"
    r"|\bsk-[A-Za-z0-9_-]{8,}"
    r"|\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"
    r"|\bgh[pousr]_[A-Za-z0-9]{20,}"
    r"|\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"
    r"|(?<=://)[^/\s:@]+:[^/\s@]+(?=@)"
)


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: "[REDACTED]" if SECRET_KEY.search(str(key)) else redact(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, str):
        return SECRET_VALUE.sub(lambda match: (match.group(1) or match.group(2) or "") + "[REDACTED]", value)
    return value


def safe_path(root: Path, candidate: Path) -> Path:
    resolved_root = root.resolve()
    resolved = (root / candidate).resolve() if not candidate.is_absolute() else candidate.resolve()
    if resolved != resolved_root and resolved_root not in resolved.parents:
        raise ValueError("path escapes workspace root")
    return resolved
