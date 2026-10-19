import json
import os
import re
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS = os.path.join(ROOT, "skills")


def frontmatter(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    return dict(line.split(":", 1) for line in m.group(1).splitlines() if ":" in line)


class SkillFormatTest(unittest.TestCase):
    """Every skill must load in Claude Code, Claude.ai and Antigravity."""

    def test_every_skill_has_valid_frontmatter(self):
        for name in sorted(os.listdir(SKILLS)):
            if name.startswith("."):
                continue
            with self.subTest(skill=name):
                fm = frontmatter(os.path.join(SKILLS, name, "SKILL.md"))
                self.assertIsNotNone(fm, "SKILL.md must start with --- frontmatter ---")
                self.assertEqual(fm.get("name", "").strip(), name, "name must match the folder")
                self.assertRegex(name, r"^[a-z0-9-]{1,64}$")
                desc = fm.get("description", "").strip()
                self.assertTrue(desc, "description is required")
                # Claude rejects longer descriptions, and every character loads in every session
                self.assertLessEqual(len(desc), 1024)

    def test_frontmatter_rejects_bad_files(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("# no frontmatter\n")
        self.addCleanup(os.remove, f.name)
        self.assertIsNone(frontmatter(f.name))

    def test_plugin_manifests_are_valid_json(self):
        for name in ("plugin.json", "marketplace.json"):
            with self.subTest(file=name), open(os.path.join(ROOT, ".claude-plugin", name)) as f:
                json.load(f)


if __name__ == "__main__":
    unittest.main()
