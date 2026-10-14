import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from domangcha.evidence.config import ConfigError, EvidenceConfig
from domangcha.evidence.ledger import ClaimError, Ledger
from domangcha.evidence.state import StateError, StateForcer
from domangcha.evidence.trace import TraceError, Tracer
from domangcha.evidence.gate import check

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "domangcha" / "engine.py"
PY = sys.executable


def write_config(workspace: Path, **overrides) -> EvidenceConfig:
    config = {
        "states": {
            name: {
                "enter": [PY, "-c", "open('state.txt','w').write('%s')" % name],
                "exit": [PY, "-c", "open('state.txt','w').write('normal')"],
            }
            for name in ("loading", "empty", "error", "no-permission")
        },
        "logs": ["server.log"],
        "db": [PY, "-c", "import sys; print('row', sys.argv[1]) if sys.argv[1] == 'order-42' else None", "{marker}"],
    }
    config.update(overrides)
    path = workspace / ".domangcha" / "evidence.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config))
    return EvidenceConfig.load(workspace)


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tmp.name)
        self.ledger = Ledger(self.workspace)
        self.ledger.start("first")

    def tearDown(self):
        self.tmp.cleanup()

    def test_observation_requires_a_source(self):
        with self.assertRaises(ClaimError):
            self.ledger.record("observation", "list shows 3 rows")

    def test_inference_requires_a_basis(self):
        with self.assertRaises(ClaimError):
            self.ledger.record("inference", "users will not notice")

    def test_derivation_cannot_rest_on_inference(self):
        guess = self.ledger.record("inference", "cache is warm", basis="fast second load")
        with self.assertRaises(ClaimError):
            self.ledger.record("derivation", "no db hit", sources=[guess["id"]])

    def test_derivation_rests_on_observations(self):
        seen = self.ledger.record("observation", "200 OK", source="chrome:network")
        derived = self.ledger.record("derivation", "save succeeded", sources=[seen["id"]])
        self.assertEqual(derived["from"], [seen["id"]])

    def test_unknown_kind_is_rejected(self):
        with self.assertRaises(ClaimError):
            self.ledger.record("hunch", "probably fine")

    def test_secrets_are_redacted_before_persisting(self):
        self.ledger.record("observation", "header Bearer abc.def", source="chrome:network")
        stored = (self.workspace / ".domangcha" / "evidence" / "current.json").read_text()
        self.assertNotIn("abc.def", stored)

    def test_diff_reports_regression_from_observation_to_unknown(self):
        self.ledger.record("observation", "empty state shown", source="chrome:shot", key="state:empty")
        self.ledger.close()
        self.ledger.start("second")
        self.ledger.record("unknown", "empty state not reachable", key="state:empty")
        report = self.ledger.diff()
        self.assertEqual(report["regressed"], ["state:empty"])

    def test_close_without_open_run_fails(self):
        self.ledger.close()
        with self.assertRaises(ClaimError):
            self.ledger.close()


class ConfigTests(unittest.TestCase):
    def test_missing_config_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ConfigError):
                EvidenceConfig.load(Path(tmp))

    def test_state_command_must_be_argv_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ConfigError):
                write_config(Path(tmp), states={"empty": {"enter": "rm -rf /", "exit": ["true"]}})


class StateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tmp.name)
        self.config = write_config(self.workspace)
        self.ledger = Ledger(self.workspace)
        self.ledger.start("states")
        self.forcer = StateForcer(self.workspace, self.config, self.ledger)

    def tearDown(self):
        self.tmp.cleanup()

    def test_enter_runs_command_and_marks_state_active(self):
        self.forcer.enter("empty")
        self.assertEqual((self.workspace / "state.txt").read_text(), "empty")
        self.assertEqual(self.ledger.current()["active_states"], ["empty"])

    def test_exit_restores_and_clears_active(self):
        self.forcer.enter("error")
        self.forcer.exit("error")
        self.assertEqual((self.workspace / "state.txt").read_text(), "normal")
        self.assertEqual(self.ledger.current()["active_states"], [])

    def test_unconfigured_state_is_rejected(self):
        with self.assertRaises(StateError):
            self.forcer.enter("offline")

    def test_failing_enter_command_is_recorded_as_unknown(self):
        config = write_config(self.workspace, states={
            "empty": {"enter": [PY, "-c", "raise SystemExit(3)"], "exit": [PY, "-c", "pass"]}})
        forcer = StateForcer(self.workspace, config, self.ledger)
        with self.assertRaises(StateError):
            forcer.enter("empty")
        kinds = [c["kind"] for c in self.ledger.current()["claims"]]
        self.assertIn("unknown", kinds)
        # a half-applied enter may have changed the system: keep it restorable and flagged
        self.assertEqual(self.ledger.current()["active_states"], ["empty"])
        forcer.exit("empty")
        self.assertEqual(self.ledger.current()["active_states"], [])


class TraceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tmp.name)
        self.config = write_config(self.workspace)
        self.ledger = Ledger(self.workspace)
        self.ledger.start("trace")
        (self.workspace / "server.log").write_text("boot\nPOST /orders order-42 201\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_marker_links_network_log_and_db(self):
        network = [{"url": "/api/orders", "method": "POST", "status": 201, "body": "order-42"},
                   {"url": "/api/health", "status": 200}]
        bundle = Tracer(self.workspace, self.config, self.ledger).trace("order-42", network)
        self.assertTrue(bundle["complete"])
        self.assertEqual(len(bundle["network"]), 1)
        self.assertEqual(bundle["log"], ["POST /orders order-42 201"])
        self.assertEqual(bundle["db"], ["row order-42"])

    def test_missing_db_row_is_unknown_and_incomplete(self):
        bundle = Tracer(self.workspace, self.config, self.ledger).trace("order-99", [])
        self.assertFalse(bundle["complete"])
        unknown = [c["key"] for c in self.ledger.current()["claims"] if c["kind"] == "unknown"]
        self.assertIn("trace:default:db", unknown)

    def test_marker_rejects_shell_metacharacters(self):
        with self.assertRaises(TraceError):
            Tracer(self.workspace, self.config, self.ledger).trace("x'; drop table", [])


class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tmp.name)
        self.config = write_config(self.workspace)
        self.ledger = Ledger(self.workspace)
        self.ledger.start("gate")
        (self.workspace / "server.log").write_text("order-42\n")

    def tearDown(self):
        self.tmp.cleanup()

    def capture_all_states(self, skip=()):
        forcer = StateForcer(self.workspace, self.config, self.ledger)
        for name in ("loading", "empty", "error", "no-permission"):
            forcer.enter(name)
            if name not in skip:
                self.ledger.record("observation", name + " screen", source="chrome:screenshot", key="state:" + name)
            forcer.exit(name)

    def test_complete_run_passes(self):
        self.capture_all_states()
        Tracer(self.workspace, self.config, self.ledger).trace("order-42", [{"url": "/o", "body": "order-42"}])
        self.assertEqual(check(self.ledger.current(), self.config)["missing"], [])

    def test_uncaptured_state_fails(self):
        self.capture_all_states(skip=("error",))
        Tracer(self.workspace, self.config, self.ledger).trace("order-42", [])
        self.assertIn("state:error", check(self.ledger.current(), self.config)["missing"])

    def test_capture_outside_forced_window_does_not_count(self):
        self.ledger.record("observation", "empty screen", source="chrome:screenshot", key="state:empty")
        self.assertIn("state:empty", check(self.ledger.current(), self.config)["missing"])

    def test_state_left_active_fails(self):
        StateForcer(self.workspace, self.config, self.ledger).enter("loading")
        self.assertIn("active:loading", check(self.ledger.current(), self.config)["missing"])

    def test_no_trace_fails(self):
        self.capture_all_states()
        self.assertIn("trace", check(self.ledger.current(), self.config)["missing"])


class CliTests(unittest.TestCase):
    def run_engine(self, workspace: Path, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([PY, str(ENGINE), "evidence", *args, "--workspace", str(workspace)],
                              capture_output=True, text=True)

    def test_start_record_check_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            write_config(workspace)
            self.assertEqual(self.run_engine(workspace, "start", "--label", "cli").returncode, 0)
            recorded = self.run_engine(workspace, "record", "observation", "list renders",
                                       "--source", "chrome:screenshot")
            self.assertEqual(recorded.returncode, 0, recorded.stderr)
            checked = self.run_engine(workspace, "check")
            self.assertEqual(checked.returncode, 1)
            self.assertIn("state:loading", json.loads(checked.stdout)["missing"])

    def test_invalid_claim_exits_with_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self.run_engine(workspace, "start")
            result = self.run_engine(workspace, "record", "observation", "no source")
            self.assertEqual(result.returncode, 2)
            self.assertIn("source", result.stderr)


if __name__ == "__main__":
    unittest.main()
