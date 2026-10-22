"""The product policies have to reach the model, not just the repository.

A policy file nobody reads is the failure mode these tests exist to catch: each
one pins a path the rules actually travel — the shared policy directory, the
harness skill, the adapter rulebooks, and the loop protocol copied into a user's
project — so deleting a reference breaks a test instead of silently disarming
the policy.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POLICIES = ROOT / "domangcha" / "policies"
TEMPLATES = ROOT / "domangcha" / "loop" / "templates"
LOOP_EDITIONS = (TEMPLATES / "LOOP.md", TEMPLATES / "LOOP.en.md")


class PolicyFileTests(unittest.TestCase):
    def test_prose_policies_were_replaced_by_the_evidence_policy(self):
        self.assertTrue((POLICIES / "evidence.md").exists())
        for name in ("product-ui.md", "delivery.md"):
            self.assertFalse((POLICIES / name).exists(), name)

    def test_the_shared_core_policy_routes_to_the_evidence_gate(self):
        self.assertIn("policies/evidence.md", (POLICIES / "core.md").read_text())

    def test_the_evidence_policy_names_every_adapter_command(self):
        text = (POLICIES / "evidence.md").read_text()
        for command in ("evidence start", "evidence state enter", "evidence trace",
                        "evidence check", "evidence close", "rea-agents"):
            self.assertIn(command, text)

    def test_every_entry_rulebook_references_the_evidence_policy(self):
        for rel in ("CLAUDE.md", "AGENTS.md", "domangcha/skills/ceo-standards/SKILL.md"):
            self.assertIn("evidence.md", (ROOT / rel).read_text(), rel)


class HarnessAgentTests(unittest.TestCase):
    """Builders carry the evidence gate; reviewers are delegated, not shipped."""

    def test_builders_name_the_evidence_gate(self):
        for agent in ("dc-dev-fe", "dc-dev-be"):
            text = (ROOT / "domangcha" / "agents" / ("%s.md" % agent)).read_text()
            self.assertIn("evidence.md", text, agent)

    def test_native_shadows_are_not_shipped(self):
        for agent in ("dc-rev", "dc-sec", "dc-qa", "dc-res", "dc-knw"):
            self.assertFalse((ROOT / "domangcha" / "agents" / ("%s.md" % agent)).exists(), agent)

    def test_review_never_depends_on_an_optional_agent_name(self):
        """code-reviewer and friends come from ECC, not Claude Code; review must still run without them."""
        for rel in ("domangcha/skills/ceo-agents/SKILL.md", "domangcha/CLAUDE.md", "CLAUDE.md"):
            self.assertIn("general-purpose", (ROOT / rel).read_text(), rel)
        false_claims = re.compile(
            r"native (code-reviewer|security-reviewer|e2e-runner|doc-updater|reviewers)"
            r"|네이티브 (code-reviewer|security-reviewer|e2e-runner|리뷰어)"
            r"|reviewers,? and the browser are"
            r"|리뷰어·브라우저는")
        docs = [ROOT / "README.md", ROOT / "CLAUDE.md", ROOT / "domangcha" / "CLAUDE.md"]
        for folder in ("agents", "commands", "skills", "policies"):
            docs += sorted((ROOT / "domangcha" / folder).rglob("*.md"))
        for path in docs:
            self.assertIsNone(false_claims.search(path.read_text()), path)


class LoopProtocolTests(unittest.TestCase):
    """A loop project holds only LOOP.md, so the rules ship inline in both editions."""

    def test_both_editions_carry_the_surface_and_delivery_sections(self):
        for path in LOOP_EDITIONS:
            text = path.read_text()
            self.assertRegex(text, r"(?m)^## 8 ", path.name)
            self.assertRegex(text, r"(?m)^## 9 ", path.name)

    def test_the_self_audit_gained_an_eighth_criterion(self):
        for path in LOOP_EDITIONS:
            text = path.read_text()
            self.assertRegex(text, r"(?m)^  h ", path.name)
            self.assertNotIn("7항 실행", text)
            self.assertNotIn("7-point self-audit", text)

    def test_the_final_audit_checks_the_surface_and_the_completion_conditions(self):
        for path in LOOP_EDITIONS:
            text = path.read_text()
            self.assertRegex(text, r"(?m)^5a ", path.name)
            self.assertRegex(text, r"(?m)^5b ", path.name)

    def test_the_reporting_contract_covers_the_new_criterion(self):
        """The contract names the audit range; leaving it at g hides failures in h."""
        source = (TEMPLATES / "scripts" / "loop.mjs").read_text()
        self.assertIn("a..h", source)
        self.assertIn("a~h", source)
        self.assertNotIn("a..g", source)
        self.assertNotIn("a~g", source)


class InstalledSurfaceTests(unittest.TestCase):
    """This repository's own output is held to the same rules it ships."""

    INSTALLER = ROOT / "domangcha" / "install.sh"

    def test_the_harness_installer_deploys_the_policy_directory(self):
        self.assertIn("policies", self.INSTALLER.read_text())
        self.assertIn(
            "for part in orchestration adapters manifests evidence policies; do",
            self.INSTALLER.read_text(),
        )

    def test_every_ceo_skill_reaches_the_user_machine(self):
        """ceo-standards carries the evidence summary; shipping only ceo-system hid it."""
        source = self.INSTALLER.read_text()
        self.assertIn('for skill_dir in "${SRC}/skills/"ceo-*/; do', source)
        self.assertNotIn(
            'cp "${SRC}/skills/ceo-system/SKILL.md" "${SKILLS_DIR}/ceo-system/SKILL.md"', source
        )

    def test_deployed_rulebooks_name_a_path_that_exists_after_install(self):
        """A repo-relative policy path resolves to nothing from ~/.claude."""
        for rel in (
            "domangcha/CLAUDE.md",
            "domangcha/skills/ceo-system/SKILL.md",
            "domangcha/skills/ceo-standards/SKILL.md",
        ):
            self.assertIn("~/.domangcha/domangcha/policies/", (ROOT / rel).read_text(), rel)

    def test_the_spinner_reports_the_real_exit_status(self):
        """A tick printed regardless of outcome is an unverified completion claim."""
        source = self.INSTALLER.read_text()
        self.assertIn('wait "$pid" || rc=$?', source)
        self.assertIn('return "$rc"', source)

    def test_the_installer_states_no_count_it_did_not_measure(self):
        """Counts of agents, commands, and skills come from the install, not the text."""
        source = self.INSTALLER.read_text()
        for claim in ("18 agents", "183 ECC", "18 Agent Roles", "19 Commands", "18 DC-*"):
            self.assertNotIn(claim, source, claim)
        self.assertIn("INSTALLED_AGENTS=$((agent_new + agent_up))", source)

    def test_extra_skill_bundles_are_opt_in(self):
        """Every installed skill is listed in each session's system prompt; extras cost every user."""
        source = self.INSTALLER.read_text()
        guard = source.index('if [ "${DOMANGCHA_WITH_EXTRAS:-0}" != "1" ]; then')
        for clone in ('claude plugin install ecc@ecc', '"$GSTACK_REPO"', "superpowers@superpowers-marketplace"):
            self.assertGreater(source.index(clone), guard, clone)
        self.assertNotIn("Required for CEO", source)

    def test_ecc_installs_as_the_plugin_never_as_copies(self):
        """Copies beside the plugin list every ECC skill and agent twice in each session."""
        source = self.INSTALLER.read_text()
        self.assertIn('ECC_MARKETPLACE="affaan-m/ECC"', source)
        self.assertNotIn('"${ECC_TMP}/skills"', source)

    def test_taste_skill_is_pinned_and_skippable(self):
        """A default third-party skill runs on every user's machine: pin the commit, allow opt-out."""
        source = self.INSTALLER.read_text()
        for needle in ('TASTE_SHA="63aba5f43b5056758b15bbe7d683da8c86a7a7ad"',
                       'rev-parse HEAD)" = "$TASTE_SHA"', "DOMANGCHA_SKIP_TASTE", "already installed — left untouched"):
            self.assertIn(needle, source)

    def test_the_clone_is_announced_after_it_runs(self):
        """Announcing a fresh install before cloning reports a result nobody checked."""
        source = self.INSTALLER.read_text()
        body = source.split("git_update_or_clone() {", 1)[1].split("\n}", 1)[0]
        for branch in body.split("git clone --depth 1")[1:]:
            self.assertRegex(branch.lstrip(), r'^"\$repo" "\$dest" --quiet\n\s*echo')

    def test_the_loop_installer_distinguishes_a_failed_commit_from_a_clean_one(self):
        source = (ROOT / "bin" / "domangcha-loop.mjs").read_text()
        self.assertIn("git status --porcelain", source)
        self.assertIn("the commit did not run", source)
        self.assertNotIn("/* 변경 없음 또는 git author 미설정, 무시 */", source)

    def test_a_skipped_version_bump_is_reported_on_the_done_line(self):
        source = (TEMPLATES / "scripts" / "loop.mjs").read_text()
        self.assertIn("package.json version not bumped", source)
        self.assertNotIn("catch { /* 건너뜀 */ }", source)


class InstallerLanguageOrderTests(unittest.TestCase):
    """Bilingual output stays English-first; the new lines must not break that."""

    INSTALLER = ROOT / "domangcha" / "install.sh"

    def test_no_installer_line_puts_korean_before_english(self):
        offenders = [
            line for line in self.INSTALLER.read_text().splitlines()
            if re.search(r'[가-힣][^"]*/ [A-Za-z]', line)
        ]
        self.assertEqual(offenders, [])



class BrowserPreferenceTests(unittest.TestCase):
    """ego-browser when installed, else Claude-in-Chrome; never Playwright by default."""

    SURFACES = (
        "domangcha/CLAUDE.md",
        "domangcha/skills/ceo-standards/SKILL.md",
        "domangcha/policies/evidence.md",
        "domangcha/agents/dc-dev-fe.md",
        "domangcha/commands/ceo-debug.md",
        "domangcha/commands/ceo-ship.md",
        "domangcha/loop/templates/LOOP.md",
        "domangcha/loop/templates/LOOP.en.md",
        "README.md",
    )

    def test_every_browser_surface_names_ego_browser_before_chrome(self):
        for rel in self.SURFACES:
            text = (ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(rel=rel):
                self.assertIn("ego-browser", text)
                for line in text.splitlines():
                    if "Claude-in-Chrome" in line and "ego-browser" not in line:
                        self.assertLess(text.index("ego-browser"), text.index(line))

    def test_policy_tells_the_agent_to_load_the_ego_browser_guide(self):
        for rel in ("domangcha/CLAUDE.md", "domangcha/skills/ceo-standards/SKILL.md",
                    "domangcha/policies/evidence.md", "domangcha/loop/templates/LOOP.en.md"):
            with self.subTest(rel=rel):
                self.assertIn("`ego-browser skill`", (ROOT / rel).read_text(encoding="utf-8"))

    def test_playwright_is_never_the_default_browser(self):
        for rel in self.SURFACES:
            text = (ROOT / rel).read_text(encoding="utf-8")
            for line in text.splitlines():
                if "Playwright" in line or "playwright" in line:
                    with self.subTest(rel=rel, line=line):
                        self.assertRegex(line, r"(?i)\bnever\b|\bno\b|금지|말고|쓰지 않")


if __name__ == "__main__":
    unittest.main()
