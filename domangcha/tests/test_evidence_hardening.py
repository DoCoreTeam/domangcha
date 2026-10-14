"""Security and code-review findings on the evidence adapters, pinned as regressions."""
import subprocess
import tempfile
import unittest
from pathlib import Path

from domangcha.evidence.ledger import ClaimError, Ledger
from domangcha.evidence.trace import TraceError, Tracer
from domangcha.tests.test_evidence import ENGINE, PY, write_config


class HardeningTests(unittest.TestCase):
    """Security review findings: an untrusted clone must not run or read what it likes."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tmp.name) / "repo"
        self.workspace.mkdir()
        self.home = Path(self.tmp.name) / "home"
        self.home.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def engine(self, *args):
        import os
        env = dict(os.environ, HOME=str(self.home))
        return subprocess.run([PY, str(ENGINE), "evidence", *args, "--workspace", str(self.workspace)],
                              capture_output=True, text=True, env=env)

    def test_untrusted_config_never_runs_commands(self):
        write_config(self.workspace)
        self.engine("start")
        result = self.engine("state", "enter", "empty")
        self.assertEqual(result.returncode, 2)
        self.assertIn("evidence trust", result.stderr)
        self.assertFalse((self.workspace / "state.txt").exists())

    def test_trust_is_invalidated_when_the_config_changes(self):
        from domangcha.evidence.trust import is_trusted, record_trust
        write_config(self.workspace)
        record_trust(self.workspace, self.home)
        self.assertTrue(is_trusted(self.workspace, self.home))
        write_config(self.workspace, logs=["other.log"])
        self.assertFalse(is_trusted(self.workspace, self.home))

    def test_trusted_config_runs(self):
        from domangcha.evidence.trust import record_trust
        write_config(self.workspace)
        record_trust(self.workspace, self.home)
        self.engine("start")
        self.assertEqual(self.engine("state", "enter", "empty").returncode, 0)
        self.assertEqual((self.workspace / "state.txt").read_text(), "empty")

    def test_symlinked_temp_file_cannot_redirect_a_write(self):
        victim = Path(self.tmp.name) / "victim.txt"
        victim.write_text("keep me")
        evidence = self.workspace / ".domangcha" / "evidence"
        evidence.mkdir(parents=True)
        (evidence / "current.tmp").symlink_to(victim)
        Ledger(self.workspace).start()
        self.assertEqual(victim.read_text(), "keep me")

    def test_symlinked_evidence_directory_is_refused(self):
        outside = Path(self.tmp.name) / "outside"
        outside.mkdir()
        (self.workspace / ".domangcha").mkdir()
        (self.workspace / ".domangcha" / "evidence").symlink_to(outside)
        with self.assertRaises(ClaimError):
            Ledger(self.workspace).start()

    def test_log_paths_outside_the_workspace_are_refused(self):
        config = write_config(self.workspace, logs=["/etc/hosts"])
        ledger = Ledger(self.workspace)
        ledger.start()
        with self.assertRaises(TraceError):
            Tracer(self.workspace, config, ledger).trace("order-42", [])

    def test_weak_or_flag_like_markers_are_refused(self):
        config = write_config(self.workspace)
        ledger = Ledger(self.workspace)
        ledger.start()
        for marker in (".", "a", "abcdefgh", "-rf-123456"):
            with self.assertRaises(TraceError, msg=marker):
                Tracer(self.workspace, config, ledger).trace(marker, [])

    def test_network_file_outside_the_workspace_is_refused(self):
        from domangcha.evidence.trust import record_trust
        write_config(self.workspace)
        record_trust(self.workspace, self.home)
        self.engine("start")
        outside = Path(self.tmp.name) / "secrets.json"
        outside.write_text("[]")
        result = self.engine("trace", "order-42", "--network", str(outside))
        self.assertEqual(result.returncode, 2)

    def test_init_keeps_runs_out_of_git(self):
        self.assertEqual(self.engine("init").returncode, 0)
        self.assertTrue((self.workspace / ".domangcha" / "evidence" / ".gitignore").exists())


class ReviewFindingTests(unittest.TestCase):
    """Code review findings: the gate must not be forgeable and diffs must compare like with like."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tmp.name)
        self.ledger = Ledger(self.workspace)
        self.ledger.start()

    def tearDown(self):
        self.tmp.cleanup()

    def test_adapter_keys_cannot_be_recorded_by_hand(self):
        for key in ("forced:empty", "released:empty", "trace:default"):
            with self.assertRaises(ClaimError, msg=key):
                self.ledger.record("observation", "fake", source="x", key=key)

    def test_unkeyed_claims_are_not_diffed_across_runs(self):
        self.ledger.record("observation", "first thing", source="x")
        self.ledger.close()
        self.ledger.start()
        self.ledger.record("unknown", "something else entirely")
        report = self.ledger.diff()
        self.assertEqual(report["changed"], [])
        self.assertEqual(report["regressed"], [])

    def test_trace_regression_is_visible_across_runs_with_different_markers(self):
        config = write_config(self.workspace)
        (self.workspace / "server.log").write_text("")
        Tracer(self.workspace, config, self.ledger).trace("order-42", [{"b": "order-42"}])
        self.ledger.close()
        self.ledger.start()
        Tracer(self.workspace, config, self.ledger).trace("order-77", [{"b": "order-77"}])
        self.assertIn("trace:default:db", self.ledger.diff()["regressed"])


if __name__ == "__main__":
    unittest.main()
