#!/usr/bin/env python3
"""PreToolUse(Bash): let rtk compress what a shell command prints before the model reads it.

`rtk rewrite <cmd>` owns the rewrite rules:
  0 or 3 + stdout  rewritten                       -> pass the rewritten command on
  other            no equivalent, or a deny rule   -> leave the command alone
The hook only rewrites; it never allows, so every command still meets Claude Code's own
permission checks. Any failure leaves the command alone: it may save tokens, never block work.
"""
from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
import sys

REWRITE_TIMEOUT_SECONDS = 3
BUNDLED_RTK = os.path.expanduser("~/.domangcha/bin/rtk")
# Anything that makes a command more than one simple command, or quotes text that may say "rtk"
SHELL_SYNTAX = re.compile(r"""[;&|<>()`$'"\\{}\n]""")


def find_rtk() -> str | None:
    on_path = shutil.which("rtk")
    if on_path:
        return on_path
    return BUNDLED_RTK if os.access(BUNDLED_RTK, os.X_OK) else None


def rewrite(rtk: str, command: str) -> tuple[int, str]:
    # RTK_REWRITE_HOST relaxes rtk's approval gate; an inherited value must not reach it.
    env = {k: v for k, v in os.environ.items() if k != "RTK_REWRITE_HOST"}
    result = subprocess.run([rtk, "rewrite", command], capture_output=True, text=True,
                            timeout=REWRITE_TIMEOUT_SECONDS, env=env)
    return result.returncode, result.stdout.strip()


def runnable(rtk: str, rewritten: str) -> str | None:
    """The shell must find the binary the rewrite names; None means leave the command alone.

    The bundled binary is off PATH, so it is named by path, and only in a single simple
    command: editing shell text any further could change what the command means.
    """
    if shutil.which("rtk") == rtk:
        return rewritten
    if not rewritten.startswith("rtk ") or SHELL_SYNTAX.search(rewritten):
        return None
    return shlex.quote(rtk) + rewritten[len("rtk"):]


def main() -> int:
    try:
        event = json.load(sys.stdin)
        tool_input = event.get("tool_input") or {}
        command = tool_input.get("command") or ""
        rtk = find_rtk()
        if not command or not rtk:
            return 0
        code, rewritten = rewrite(rtk, command)
    except Exception:
        return 0
    if code not in (0, 3) or not rewritten or rewritten == command:
        return 0
    final = runnable(rtk, rewritten)
    if final is None:
        return 0
    # Never a permissionDecision: the rewritten command goes through Claude Code's own checks.
    output = {"hookEventName": "PreToolUse",
              "updatedInput": {**tool_input, "command": final}}
    print(json.dumps({"hookSpecificOutput": output}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
