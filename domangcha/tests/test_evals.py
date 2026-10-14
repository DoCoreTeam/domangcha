import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class EvalSuiteTests(unittest.TestCase):
    def test_suite_has_twenty_cases(self):
        cases = json.loads((ROOT / "domangcha/evals/cases.json").read_text())
        self.assertEqual(len(cases["route"]) + len(cases["evidence"]), 20)

    def test_the_evidence_gate_judges_every_scenario_correctly(self):
        result = subprocess.run([sys.executable, str(ROOT / "domangcha/evals/run.py"), "--json"],
                                capture_output=True, text=True, check=False)
        report = json.loads(result.stdout)
        self.assertEqual(report["evidence"]["wrong_on"], [])
        self.assertLess(report["evidence"]["off"], report["evidence"]["on"])


if __name__ == "__main__":
    unittest.main()
