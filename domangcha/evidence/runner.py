"""Runs configured argv commands without a shell and reports what happened."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List, Tuple

COMMAND_TIMEOUT_SECONDS = 60


def run(argv: List[str], cwd: Path) -> Tuple[bool, str]:
    try:
        done = subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True,
                              timeout=COMMAND_TIMEOUT_SECONDS, check=False)
    except FileNotFoundError:
        return False, "command not found: %s" % argv[0]
    except subprocess.TimeoutExpired:
        return False, "timed out after %ds: %s" % (COMMAND_TIMEOUT_SECONDS, argv[0])
    output = (done.stdout or "") + (done.stderr or "")
    if done.returncode != 0:
        return False, "exit %d: %s" % (done.returncode, output.strip()[:500])
    return True, output
