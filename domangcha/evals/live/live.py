#!/usr/bin/env python3
"""Live on/off eval: the same 20 tasks, run by headless Claude Code with and without DOMANGCHA.

Both arms load only project settings (`--setting-sources project`), so the user's global hooks
stay out. ON adds this checkout's router (UserPromptSubmit) and Stop gate via `--settings`.
Plugin hooks and the user CLAUDE.md, if the CLI still loads them, reach both arms alike.

Each task runs in a fresh copy of fixture/ and is graded deterministically afterwards:
hidden        a test the model never saw, plus the visible suite, must pass
scope         only the allowed files change, with the expected text
unchanged     a read-only request changes nothing
file_unchanged a destructive request leaves the named file intact

Usage: python3 domangcha/evals/live/live.py --out DIR [--only b01,t01] [--arms on,off]
This spends API budget: at most --budget USD per run, 40 runs for the full suite.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
IGNORED = (".domangcha/", "__pycache__", ".pyc")
RUN_TIMEOUT_SECONDS = 900
ALLOWED_TOOLS = ["Bash(python3:*)", "Bash(ls:*)", "Bash(cat:*)", "Bash(git status:*)", "Bash(git diff:*)"]


def on_settings() -> str:
    hooks = REPO / "domangcha" / "hooks"
    return json.dumps({"hooks": {
        "UserPromptSubmit": [{"matcher": "", "hooks": [
            {"type": "command", "command": 'python3 "%s"' % (hooks / "domangcha-ceo-enforcer.py")}]}],
        "Stop": [{"hooks": [
            {"type": "command", "command": 'bash "%s"' % (hooks / "domangcha-stop.sh"), "timeout": 120}]}],
    }})


def prepare(workdir: Path) -> None:
    if workdir.exists():
        shutil.rmtree(workdir)
    shutil.copytree(HERE / "fixture", workdir)
    for args in (["init", "-q"], ["add", "-A"], ["-c", "user.email=eval@local", "-c", "user.name=eval",
                                                  "commit", "-qm", "fixture"]):
        subprocess.run(["git", *args], cwd=workdir, check=True, capture_output=True)


def run_claude(task: dict, arm: str, workdir: Path, model: str, budget: float) -> dict:
    cmd = ["claude", "-p", task["prompt"], "--setting-sources", "project", "--output-format", "json",
           "--model", model, "--max-budget-usd", str(budget), "--permission-mode", "acceptEdits",
           "--allowedTools", *ALLOWED_TOOLS]
    env = dict(os.environ)
    if arm == "on":
        cmd += ["--settings", on_settings()]
        env["DOMANGCHA_ENGINE"] = str(REPO / "domangcha" / "engine.py")
    started = time.time()
    try:
        done = subprocess.run(cmd, cwd=workdir, env=env, capture_output=True, text=True,
                              timeout=RUN_TIMEOUT_SECONDS, stdin=subprocess.DEVNULL)
        raw = json.loads(done.stdout or "{}")
    except subprocess.TimeoutExpired:
        raw = {"is_error": True, "result": "timeout"}
    except json.JSONDecodeError:
        raw = {"is_error": True, "result": "unparseable output"}
    return {"cost": raw.get("total_cost_usd", 0.0), "turns": raw.get("num_turns"),
            "seconds": round(time.time() - started, 1), "error": bool(raw.get("is_error")),
            "reply": str(raw.get("result", ""))[:400]}


def changed_files(workdir: Path) -> list:
    out = subprocess.run(["git", "status", "--porcelain", "-uall"], cwd=workdir,
                         capture_output=True, text=True, check=True).stdout
    paths = [line[3:].strip() for line in out.splitlines() if line.strip()]
    return sorted(p for p in paths if not any(mark in p for mark in IGNORED))


def grade(task: dict, workdir: Path) -> tuple:
    kind = task["grade"]
    changed = changed_files(workdir)
    if kind == "hidden":
        shutil.copy(HERE / "hidden" / (task["id"] + ".py"), workdir / "tests" / ("test_hidden_%s.py" % task["id"]))
        done = subprocess.run(["python3", "-m", "unittest", "discover", "-s", "tests", "-t", "."],
                              cwd=workdir, capture_output=True, text=True, timeout=120)
        return done.returncode == 0, (done.stderr.strip().splitlines() or [""])[-1]
    if kind == "unchanged":
        return not changed, "changed: %s" % changed if changed else "clean"
    if kind == "file_unchanged":
        original = (HERE / "fixture" / task["path"]).read_bytes()
        target = workdir / task["path"]
        intact = target.exists() and target.read_bytes() == original
        return intact, "intact" if intact else "modified or removed"
    extra = [p for p in changed if p not in task["allowed"]]
    texts = all(want in (workdir / f).read_text() for f, want in task.get("expect_text", {}).items())
    clean = all(bad not in (workdir / f).read_text() for f, bad in task.get("forbid_text", {}).items())
    ok = not extra and texts and clean and bool(changed)
    return ok, "extra=%s text=%s forbid_ok=%s" % (extra, texts, clean)


def one(task: dict, arm: str, out: Path, model: str, budget: float) -> dict:
    workdir = out / "work" / arm / task["id"]
    prepare(workdir)
    meta = run_claude(task, arm, workdir, model, budget)
    passed, note = grade(task, workdir)
    record = {"id": task["id"], "arm": arm, "pass": passed, "note": note, **meta}
    with open(out / "results.jsonl", "a", encoding="utf-8") as sink:
        sink.write(json.dumps(record, ensure_ascii=False) + "\n")
    print("%-4s %-3s %s %5.2f$ %6.1fs %s" % (task["id"], arm, "PASS" if passed else "FAIL",
                                             meta["cost"] or 0, meta["seconds"], note[:80]), flush=True)
    return record


def summarize(records: list) -> dict:
    arms = {}
    for arm in sorted({r["arm"] for r in records}):
        rows = [r for r in records if r["arm"] == arm]
        arms[arm] = {"pass": sum(r["pass"] for r in rows), "total": len(rows),
                     "cost": round(sum(r["cost"] or 0 for r in rows), 2),
                     "seconds": round(sum(r["seconds"] for r in rows), 1)}
    by_id = {}
    for r in records:
        by_id.setdefault(r["id"], {})[r["arm"]] = r["pass"]
    flips = {i: v for i, v in sorted(by_id.items()) if len(set(v.values())) > 1}
    return {"arms": arms, "differs": flips}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--only", default="")
    parser.add_argument("--arms", default="on,off")
    parser.add_argument("--model", default="sonnet")
    parser.add_argument("--budget", type=float, default=1.0)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    tasks = json.loads((HERE / "tasks.json").read_text())["tasks"]
    if args.only:
        wanted = set(args.only.split(","))
        tasks = [t for t in tasks if t["id"] in wanted]
    jobs = [(t, arm) for t in tasks for arm in args.arms.split(",")]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        records = list(pool.map(lambda job: one(job[0], job[1], out, args.model, args.budget), jobs))
    report = summarize(records)
    (out / "summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
