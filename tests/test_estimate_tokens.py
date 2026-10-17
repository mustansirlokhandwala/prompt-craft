import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "token-budget", "scripts"))
from estimate_tokens import estimate, level, main  # noqa: E402


class EstimateTokensTest(unittest.TestCase):
    def test_estimate(self):
        self.assertEqual(estimate(""), 0)
        self.assertEqual(estimate("a"), 1)
        self.assertEqual(estimate("x" * 400), 100)

    def test_level(self):
        self.assertEqual(level(100, 1000), "ok")
        self.assertEqual(level(900, 1000), "near budget")
        self.assertEqual(level(1001, 1000), "OVER BUDGET")

    def test_exit_code_reflects_budget(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("x" * 4000)  # ~1000 tokens
        try:
            self.assertEqual(main([f.name, "--budget", "2000"]), 0)
            self.assertEqual(main([f.name, "--budget", "500"]), 1)
        finally:
            os.unlink(f.name)


if __name__ == "__main__":
    unittest.main()
