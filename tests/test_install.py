import os
import shutil
import subprocess
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "install.sh")
SKILLS = sorted(d for d in os.listdir(os.path.join(ROOT, "skills")) if not d.startswith("."))
START = "<!-- prompt-craft:start -->"


class InstallTest(unittest.TestCase):
    def setUp(self):
        self.home = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.home)

    def path(self, *parts):
        return os.path.join(self.home, *parts)

    def make(self, *dirs):
        for d in dirs:
            os.makedirs(self.path(d), exist_ok=True)

    def run_installer(self, *args):
        env = dict(os.environ, HOME=self.home)
        env.pop("ANTIGRAVITY_SKILLS_DIR", None)
        return subprocess.run(["bash", SCRIPT, *args], env=env, capture_output=True, text=True)

    def read(self, *parts):
        with open(self.path(*parts)) as f:
            return f.read()

    def assert_skills_linked(self, skills_dir):
        for s in SKILLS:
            link = self.path(skills_dir, s)
            self.assertTrue(os.path.islink(link), f"{s} not linked in {skills_dir}")
            self.assertTrue(os.path.isfile(os.path.join(link, "SKILL.md")))

    # --- install ---

    def test_installs_into_both_tools_it_finds(self):
        self.make(".claude", ".gemini/config")
        r = self.run_installer()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assert_skills_linked(".claude/skills")
        self.assert_skills_linked(".gemini/config/skills")
        self.assertIn(f"@{ROOT}/rules/always-on.md", self.read(".claude/CLAUDE.md"))
        self.assertIn("1. Intent first.", self.read(".gemini/GEMINI.md"))

    def test_keeps_the_users_existing_instructions(self):
        self.make(".claude", ".gemini")
        with open(self.path(".claude/CLAUDE.md"), "w") as f:
            f.write("Always answer in British English.\n")
        with open(self.path(".gemini/GEMINI.md"), "w") as f:
            f.write("Use tabs.\n")
        self.run_installer()
        self.assertTrue(self.read(".claude/CLAUDE.md").startswith("Always answer in British English.\n"))
        self.assertTrue(self.read(".gemini/GEMINI.md").startswith("Use tabs.\n"))
        self.assertEqual(self.read(".claude/CLAUDE.md.prompt-craft.bak"), "Always answer in British English.\n")

    def test_running_twice_does_not_duplicate_the_rules(self):
        self.make(".claude", ".gemini")
        self.run_installer()
        self.run_installer()
        self.assertEqual(self.read(".claude/CLAUDE.md").count(START), 1)
        self.assertEqual(self.read(".gemini/GEMINI.md").count(START), 1)

    def test_never_overwrites_a_users_own_skill_with_the_same_name(self):
        self.make(".claude/skills/clear-writer")
        with open(self.path(".claude/skills/clear-writer/SKILL.md"), "w") as f:
            f.write("my own version")
        r = self.run_installer("--claude")
        self.assertEqual(r.returncode, 0)
        self.assertFalse(os.path.islink(self.path(".claude/skills/clear-writer")))
        self.assertEqual(self.read(".claude/skills/clear-writer/SKILL.md"), "my own version")
        self.assertIn("skip clear-writer", r.stderr)
        self.assertTrue(os.path.islink(self.path(".claude/skills/idea-shaper")))

    def test_only_sets_up_the_tool_asked_for(self):
        self.make(".claude", ".gemini")
        self.run_installer("--claude")
        self.assert_skills_linked(".claude/skills")
        self.assertFalse(os.path.exists(self.path(".gemini/GEMINI.md")))
        self.assertFalse(os.path.exists(self.path(".gemini/config/skills")))

    def test_explicit_flag_sets_up_a_tool_that_is_not_installed_yet(self):
        r = self.run_installer("--antigravity")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assert_skills_linked(".gemini/config/skills")

    def test_uses_older_antigravity_skills_folder_when_that_is_what_exists(self):
        self.make(".gemini/antigravity")
        self.run_installer()
        self.assert_skills_linked(".gemini/antigravity/skills")

    def test_fails_clearly_when_no_tool_is_found(self):
        r = self.run_installer()
        self.assertEqual(r.returncode, 1)
        self.assertIn("No Claude Code", r.stderr)

    def test_rejects_unknown_options(self):
        r = self.run_installer("--everything")
        self.assertEqual(r.returncode, 2)
        self.assertIn("unknown option", r.stderr)

    # --- uninstall ---

    def test_uninstall_removes_everything_it_added_and_nothing_else(self):
        self.make(".claude/skills/my-skill", ".gemini/config/skills/other-skill")
        with open(self.path(".claude/CLAUDE.md"), "w") as f:
            f.write("Always answer in British English.\n")
        self.run_installer()
        r = self.run_installer("--uninstall")
        self.assertEqual(r.returncode, 0, r.stderr)
        for d in (".claude/skills", ".gemini/config/skills"):
            for s in SKILLS:
                self.assertFalse(os.path.lexists(self.path(d, s)), f"{s} left in {d}")
        self.assertTrue(os.path.isdir(self.path(".claude/skills/my-skill")))
        self.assertTrue(os.path.isdir(self.path(".gemini/config/skills/other-skill")))
        self.assertEqual(self.read(".claude/CLAUDE.md").strip(), "Always answer in British English.")
        self.assertNotIn(START, self.read(".gemini/GEMINI.md"))

    def test_uninstall_leaves_the_users_own_linked_skills(self):
        self.make(".claude/skills", "my-skills/notes")
        os.symlink(self.path("my-skills/notes"), self.path(".claude/skills/notes"))
        self.run_installer("--claude")
        self.run_installer("--claude", "--uninstall")
        self.assertTrue(os.path.islink(self.path(".claude/skills/notes")))

    def test_uninstall_leaves_a_same_named_skill_that_is_not_ours(self):
        self.make(".claude/skills/clear-writer")
        self.run_installer("--claude", "--uninstall")
        self.assertTrue(os.path.isdir(self.path(".claude/skills/clear-writer")))


if __name__ == "__main__":
    unittest.main()
