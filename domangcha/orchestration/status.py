"""Human-facing status rendering for the route, checkpointed task state, and deploy drift.

The engine already records everything it does in typed state, checkpoints, and
events. This module is the only place that turns that state into something a
person can read, so every surface (CLI, Claude hooks, Codex control plane)
reports progress the same way instead of inventing its own wording.
"""
from __future__ import annotations

import os
from dataclasses import asdict, is_dataclass
from typing import Any, Dict, List, Optional

from .security import redact
from .wording import DEFAULT_LANG, LABELS, LANGS, NEXT, PLAN

BAR_WIDTH = 10
FULL, EMPTY = "▓", "░"

ROUTE_ICON = {"DIRECT": "⚡", "LOOP": "\U0001f501", "GRAPH": "\U0001f9ed"}
STATUS_ICON = {
    "PENDING": "⏸",
    "RUNNING": "⏳",
    "WAITING_FOR_APPROVAL": "\U0001f64b",
    "COMPLETED": "✅",
    "FAILED": "❌",
    "ABORTED": "\U0001f6d1",
    "BUDGET_EXHAUSTED": "⛔",
}



def as_dict(value: Any) -> Dict[str, Any]:
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    return dict(value or {})


def bar(done: int, total: int, width: int = BAR_WIDTH) -> str:
    if total <= 0:
        return ""
    ratio = min(max(done / total, 0.0), 1.0)
    filled = int(round(ratio * width))
    return "%s%s %d%%" % (FULL * filled, EMPTY * (width - filled), round(ratio * 100))


def tree(lines: List[str]) -> str:
    body = [line for line in lines if line]
    if not body:
        return ""
    return "\n".join(
        ("└ " if index == len(body) - 1 else "├ ") + line
        for index, line in enumerate(body)
    )



class StatusReporter:
    """Renders friendly progress cards. Pure formatting, no side effects."""

    def __init__(self, lang: Optional[str] = None):
        chosen = (lang or os.environ.get("DOMANGCHA_STATUS_LANG") or DEFAULT_LANG).lower()
        self.lang = chosen if chosen in LANGS else DEFAULT_LANG
        self._index = LANGS.index(self.lang)

    def route_card(self, decision: Any) -> str:
        data = redact(as_dict(decision))
        route = str(data.get("route", "DIRECT"))
        score = "" if data.get("score") is None else " (score %s)" % data["score"]
        header = "\U0001f682 DOMANGCHA · %s %s%s" % (route, ROUTE_ICON.get(route, ""), score)
        reasons = "; ".join(str(x) for x in (data.get("reasons") or [])) or self._t("none")
        lines = [
            "%s: %s" % (self._t("why"), reasons),
            "%s: %s" % (self._t("plan"), self._pick(PLAN, route)),
        ]
        if data.get("approval_required"):
            lines.append(self._t("approval_note"))
        if data.get("ambiguous"):
            lines.append(self._t("ambiguous_note"))
        lines.append("%s: %s" % (self._t("next"), self._pick(NEXT, route)))
        return header + "\n" + tree(lines)

    def graph_card(self, state: Any, total_nodes: Optional[int] = None) -> str:
        data = redact(as_dict(state))
        completed = [str(x) for x in data.get("completed_nodes", [])]
        pending = [str(x) for x in data.get("pending_nodes", [])]
        current = data.get("current_node")
        total = total_nodes or (len(completed) + len(pending) + (1 if current else 0))
        route = str(data.get("route") or "GRAPH")
        graph_ref = " %s@%s" % (data["graph_id"], data.get("graph_version") or "1") if data.get("graph_id") else ""
        progress = "  %s %d/%d %s" % (bar(len(completed), total), len(completed), total, self._t("nodes")) if total else ""
        header = "%s %s%s%s" % (ROUTE_ICON.get(route, ROUTE_ICON["GRAPH"]), route, graph_ref, progress)
        attempts = data.get("attempt_counts", {})
        lines = []
        if completed:
            lines.append("%s: %s" % (self._t("done"), " · ".join(x + " ✅" for x in completed)))
        if current:
            lines.append("%s: %s ⏳ (%s %s)" % (
                self._t("running"), current, self._t("attempt"), attempts.get(current, 1)))
        if pending:
            lines.append("%s: %s" % (self._t("waiting"), " · ".join(x + " ⏸" for x in pending)))
        lines.append(self._budget_line(data.get("usage", {}), self._graph_limits(data.get("budget", {}))))
        lines.extend(self._approval_lines(data.get("approvals", {})))
        lines.append(self._state_line(data.get("status")))
        return header.rstrip() + "\n" + tree(lines)

    def drift_card(self, report: Any) -> str:
        """Read-only: drift before a release is expected, so this never alarms."""
        data = as_dict(report)
        stale = [str(x) for x in data.get("changed", [])] + [str(x) for x in data.get("missing", [])]
        header = "\U0001f4e6 %s %s" % (self._t("deploy"), "⚠️" if stale else "✅")
        if not data.get("installed"):
            return header + "\n" + tree([self._t("not_installed")])
        lines = ["%s → %s" % (data.get("source_version"), data.get("installed_version"))]
        if stale:
            lines.append("%s: %s" % (self._t("stale_files"), " · ".join(sorted(stale))))
            lines.append(self._t("deploy_hint"))
        else:
            lines.append(self._t("in_sync"))
        return header + "\n" + tree(lines)

    def _approval_lines(self, approvals: Dict[str, Any]) -> List[str]:
        waiting = [node for node, item in sorted(approvals.items())
                   if isinstance(item, dict) and item.get("status") not in {"APPROVED", "REJECTED"}]
        return ["%s: %s \U0001f64b" % (self._t("approval"), " · ".join(waiting))] if waiting else []

    def _budget_line(self, usage: Dict[str, Any], limits: Dict[str, Any]) -> str:
        parts = []
        for name, limit in limits.items():
            if limit is None:
                continue
            parts.append("%s %s/%s" % (name, usage.get(name + "_calls", usage.get(name, 0)), limit))
        return "%s: %s" % (self._t("budget"), " · ".join(parts)) if parts else ""

    @staticmethod
    def _graph_limits(budget: Any) -> Dict[str, Any]:
        data = as_dict(budget)
        return {
            "model": data.get("model_calls"),
            "agent": data.get("agent_calls"),
            "tool": data.get("tool_calls"),
            "retries": data.get("retries"),
        }

    def _state_line(self, status: Any) -> str:
        name = getattr(status, "value", status) or "PENDING"
        return "%s: %s %s" % (self._t("state"), name, STATUS_ICON.get(str(name), ""))

    def _t(self, key: str) -> str:
        return LABELS[key][self._index]

    def _pick(self, table: Dict[str, Any], key: str) -> str:
        entry = table.get(key)
        return entry[self._index] if entry else ""
