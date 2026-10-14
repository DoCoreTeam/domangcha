import json
import os
import subprocess
import unittest
from pathlib import Path
from unittest import mock

from domangcha.orchestration.contracts import GraphState, Route, RunStatus
from domangcha.orchestration.status import StatusReporter, bar, tree


ROOT = Path(__file__).resolve().parents[2]


def run(*args) -> subprocess.CompletedProcess:
    return subprocess.run(["python3", *args], text=True, capture_output=True, cwd=ROOT, check=False)


def graph_state(**overrides) -> GraphState:
    base = dict(
        task_id="t1",
        request="build login",
        normalized_intent={},
        route=Route.GRAPH,
        graph_id="full_pipeline",
        completed_nodes=["intake", "plan"],
        current_node="build",
        pending_nodes=["review", "ship"],
        status=RunStatus.RUNNING,
        usage={"model_calls": 4, "agent_calls": 2, "tool_calls": 11},
    )
    base.update(overrides)
    return GraphState(**base)


class BarTests(unittest.TestCase):
    def test_returns_empty_string_when_total_is_unknown(self):
        self.assertEqual(bar(3, 0), "")

    def test_renders_percentage_and_clamps_overflow(self):
        self.assertTrue(bar(1, 4).endswith("25%"))
        self.assertTrue(bar(9, 4).endswith("100%"))

    def test_tree_marks_only_the_last_line_as_terminal(self):
        rendered = tree(["a", "", "b"]).splitlines()
        self.assertEqual(rendered, ["├ a", "└ b"])


class RouteCardTests(unittest.TestCase):
    def test_reports_route_reason_plan_and_next_step(self):
        card = StatusReporter("ko").route_card(
            {"route": "LOOP", "score": 4, "reasons": ["deterministic complexity score=4"]}
        )
        self.assertIn("LOOP", card)
        self.assertIn("deterministic complexity score=4", card)
        self.assertIn("계획", card)
        self.assertIn("다음", card)

    def test_announces_approval_requirement(self):
        card = StatusReporter("en").route_card({"route": "GRAPH", "approval_required": True})
        self.assertIn("approval", card)

    def test_omits_score_when_state_has_none(self):
        self.assertNotIn("score", StatusReporter().route_card({"route": "DIRECT"}))

    def test_redacts_secret_values_from_reasons(self):
        card = StatusReporter().route_card({"route": "DIRECT", "reasons": ["api_key: abcd1234"]})
        self.assertNotIn("abcd1234", card)
        self.assertIn("[REDACTED]", card)


class GraphCardTests(unittest.TestCase):
    def test_reports_completed_running_and_waiting_nodes(self):
        card = StatusReporter("ko").graph_card(graph_state())
        self.assertIn("intake ✅", card)
        self.assertIn("build ⏳", card)
        self.assertIn("ship ⏸", card)
        self.assertIn("2/5", card)

    def test_reports_pending_human_gate(self):
        state = graph_state(status=RunStatus.WAITING_FOR_APPROVAL, approvals={"gate": {"status": "PENDING"}})
        card = StatusReporter("en").graph_card(state)
        self.assertIn("awaiting approval: gate", card)

    def test_resolved_approvals_are_not_reported_as_waiting(self):
        state = graph_state(approvals={"gate": {"status": "APPROVED"}})
        self.assertNotIn("awaiting approval", StatusReporter("en").graph_card(state))

    def test_uses_the_route_of_the_checkpoint_in_the_header(self):
        card = StatusReporter().graph_card(graph_state(route=Route.LOOP, graph_id="", pending_nodes=[]))
        self.assertTrue(card.startswith("\U0001f501 LOOP"))


class LanguageTests(unittest.TestCase):
    def test_defaults_to_korean_and_falls_back_on_unknown_language(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(StatusReporter().lang, "ko")
            self.assertEqual(StatusReporter("fr").lang, "ko")

    def test_english_is_selectable(self):
        self.assertEqual(StatusReporter("EN").lang, "en")

    def test_environment_selects_the_language_when_no_argument_is_given(self):
        with mock.patch.dict(os.environ, {"DOMANGCHA_STATUS_LANG": "en"}, clear=True):
            self.assertEqual(StatusReporter().lang, "en")


class DefaultSurfaceTests(unittest.TestCase):
    """Status reporting has to be the default, not an opt-in flag."""

    def test_route_command_renders_a_card_without_being_asked(self):
        result = run("domangcha/engine.py", "route", "explain this repository")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.startswith("\U0001f682 DOMANGCHA · DIRECT"), result.stdout)

    def test_route_command_still_exposes_raw_state(self):
        result = run("domangcha/engine.py", "route", "explain this repository", "--format", "json")
        self.assertEqual(json.loads(result.stdout)["route"], "DIRECT")

    def test_drift_card_names_the_stale_files(self):
        card = StatusReporter("ko").drift_card({
            "installed": True,
            "install_path": "/home/.domangcha/domangcha",
            "source_version": "2.3.1",
            "installed_version": "2.3.0",
            "changed": ["orchestration/validation.py"],
            "missing": [],
        })
        self.assertIn("orchestration/validation.py", card)
        self.assertIn("2.3.1", card)
        self.assertIn("install.sh", card)

    def test_drift_card_confirms_a_matching_runtime(self):
        card = StatusReporter("ko").drift_card({
            "installed": True,
            "install_path": "/home/.domangcha/domangcha",
            "source_version": "2.3.1",
            "installed_version": "2.3.1",
            "changed": [],
            "missing": [],
        })
        self.assertIn("✅", card)
        self.assertNotIn("install.sh", card)

    def test_drift_command_reports_without_failing(self):
        result = run("domangcha/engine.py", "drift", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("changed", json.loads(result.stdout))

    def test_claude_hook_injects_the_card_without_resending_the_contract(self):
        result = subprocess.run(
            ["python3", str(ROOT / "domangcha/hooks/domangcha-ceo-enforcer.py")],
            input=json.dumps({"prompt": "병렬로 로그인 API와 화면을 구현해줘"}),
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("\U0001f682 DOMANGCHA · GRAPH", result.stdout)
        self.assertNotIn("진행 상황 보고 규칙", result.stdout)
        self.assertIn("route=GRAPH", result.stdout)
        self.assertIn("Workflow", result.stdout)

    def test_a_direct_prompt_costs_one_line(self):
        """DIRECT is most prompts; the static contract lives in CLAUDE.md, not in each prompt."""
        result = subprocess.run(
            ["python3", str(ROOT / "domangcha/hooks/domangcha-ceo-enforcer.py")],
            input=json.dumps({"prompt": "fix typo in README"}),
            text=True, capture_output=True, cwd=ROOT, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(result.stdout.strip().splitlines()), 1, result.stdout)
        self.assertIn("DIRECT", result.stdout)

    def test_the_installed_rulebook_carries_the_reporting_contract(self):
        text = (ROOT / "domangcha/CLAUDE.md").read_text()
        self.assertIn("## Reporting contract", text)
        self.assertIn("evidence start", text)


if __name__ == "__main__":
    unittest.main()
