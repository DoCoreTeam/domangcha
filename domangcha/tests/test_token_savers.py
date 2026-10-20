import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / "domangcha" / "hooks" / "domangcha-rtk.py"
STYLE = ROOT / "domangcha" / "output-styles" / "domangcha.md"
INSTALLER = ROOT / "domangcha" / "install.sh"

# Stands in for `rtk rewrite`: rewrites git, refuses everything else, as the real binary does.
FAKE_RTK = """#!/bin/sh
case "$2" in
  "git status") echo "rtk git status"; exit 3 ;;
  "git log") echo "rtk git log"; exit 0 ;;
  "git push") exit 2 ;;
  "git log && ls") echo "rtk git log && rtk ls"; exit 3 ;;
  'echo "a; rtk b" | git status') echo 'echo "a; rtk b" | rtk git status'; exit 3 ;;
  *) exit 1 ;;
esac
"""


class RtkHookTests(unittest.TestCase):
    """The hook may save tokens; it must never block work or grant permission."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        bin_dir = Path(self.tmp.name) / "bin"
        bin_dir.mkdir()
        rtk = bin_dir / "rtk"
        rtk.write_text(FAKE_RTK)
        rtk.chmod(0o755)
        self.env = {**os.environ, "HOME": self.tmp.name, "PATH": f"{bin_dir}:{os.environ['PATH']}"}

    def tearDown(self):
        self.tmp.cleanup()

    def hook(self, payload, env=None):
        return subprocess.run(["python3", str(HOOK)], input=payload, text=True,
                              capture_output=True, env=env or self.env, check=False)

    def event(self, command):
        return json.dumps({"tool_name": "Bash", "tool_input": {"command": command, "description": "d"}})

    def test_a_known_command_is_rewritten_and_keeps_its_other_fields(self):
        result = self.hook(self.event("git status"))
        output = json.loads(result.stdout)["hookSpecificOutput"]
        self.assertEqual(output["updatedInput"], {"command": "rtk git status", "description": "d"})

    def test_the_hook_never_grants_permission(self):
        for command in ("git status", "git log"):
            output = json.loads(self.hook(self.event(command)).stdout)["hookSpecificOutput"]
            self.assertNotIn("permissionDecision", output, command)

    def test_anything_else_passes_through_untouched(self):
        for payload in (self.event("python3 -m unittest"), self.event("git push"),
                        self.event(""), "{not json", ""):
            result = self.hook(payload)
            self.assertEqual((result.returncode, result.stdout), (0, ""), payload)

    def test_a_bundled_rtk_off_path_is_named_by_path(self):
        """~/.domangcha/bin is not on the shell's PATH; a bare `rtk` would not run."""
        bundled = Path(self.tmp.name) / ".domangcha" / "bin"
        bundled.mkdir(parents=True)
        (bundled / "rtk").write_text(FAKE_RTK)
        (bundled / "rtk").chmod(0o755)
        env = {**self.env, "PATH": "/usr/bin:/bin"}
        output = json.loads(self.hook(self.event("git status"), env).stdout)["hookSpecificOutput"]
        self.assertEqual(output["updatedInput"]["command"], "%s git status" % (bundled / "rtk"))

    def test_a_bundled_rtk_off_path_never_edits_compound_or_quoted_commands(self):
        """Rewriting shell text beyond the first word could change what a command means."""
        bundled = Path(self.tmp.name) / ".domangcha" / "bin"
        bundled.mkdir(parents=True)
        (bundled / "rtk").write_text(FAKE_RTK)
        (bundled / "rtk").chmod(0o755)
        env = {**self.env, "PATH": "/usr/bin:/bin"}
        for command in ("git log && ls", 'echo "a; rtk b" | git status'):
            result = self.hook(self.event(command), env)
            self.assertEqual((result.returncode, result.stdout), (0, ""), command)

    def test_no_rtk_means_no_rewrite(self):
        env = {**self.env, "PATH": "/usr/bin:/bin"}
        result = self.hook(self.event("git status"), env)
        self.assertEqual((result.returncode, result.stdout), (0, ""))


class OutputStyleTests(unittest.TestCase):
    """The style is in every session's system prompt once selected: keep it small and safe."""

    def test_the_style_is_small_and_keeps_the_reporting_contract(self):
        text = STYLE.read_text()
        self.assertLess(len(text.encode()), 800)
        self.assertIn("name: DOMANGCHA", text)
        self.assertIn("keep-coding-instructions: true", text)
        for kept in ("route line or card", "evidence run_id", "approvals", "failure"):
            self.assertIn(kept, text)


class InstallerTests(unittest.TestCase):
    """Defaults that reach every user's machine are pinned, verified and skippable."""

    source = INSTALLER.read_text()

    def test_rtk_is_the_pinned_oss_build_with_a_checksum_per_platform(self):
        self.assertIn('RTK_VERSION="1.0.1"', self.source)
        assets = re.findall(r'RTK_ASSET="(rtk-[^"]+)"', self.source)
        self.assertEqual(len(assets), 4)
        self.assertTrue(all(a.startswith("rtk-oss-") for a in assets), assets)
        self.assertEqual(len(re.findall(r'RTK_SHA="[0-9a-f]{64}"', self.source)), 4)
        self.assertIn('[ "$(sha256_of "$RTK_TGZ")" = "$RTK_SHA" ]', self.source)
        self.assertIn("DOMANGCHA_SKIP_RTK", self.source)

    def test_the_rtk_hook_yields_to_the_users_own_rtk_hook(self):
        self.assertIn("if rtk_hook and not users_rtk:", self.source)

    def test_the_output_style_never_overrides_the_users_choice(self):
        self.assertIn('if not skip_style and not settings.get("outputStyle") and not os.path.exists(style_marker):', self.source)
        self.assertIn("DOMANGCHA_SKIP_STYLE", self.source)

    def test_the_progress_total_matches_the_steps_that_run(self):
        calls = len(re.findall(r'^\s*step "', self.source, re.M))
        # the extras block has one "skipped" step standing in for its three
        self.assertIn("TOTAL_STEPS=%d" % (calls - 1), self.source)


if __name__ == "__main__":
    unittest.main()
