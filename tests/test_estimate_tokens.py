import contextlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = os.path.join(os.path.dirname(__file__), "..", "skills", "token-budget", "scripts")
sys.path.insert(0, SCRIPTS)
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

    def test_level_boundaries(self):
        # spending exactly the budget is not over it; "near" starts above 80%
        self.assertEqual(level(1000, 1000), "near budget")
        self.assertEqual(level(800, 1000), "ok")

    def test_exit_code_reflects_budget(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("x" * 4000)  # ~1000 tokens
        try:
            self.assertEqual(main([f.name, "--budget", "2000"]), 0)
            self.assertEqual(main([f.name, "--budget", "500"]), 1)
        finally:
            os.unlink(f.name)

    def test_totals_several_files(self):
        paths = []
        for chars in (400, 800):  # ~100 + ~200 tokens
            with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
                f.write("x" * chars)
            paths.append(f.name)
        try:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                main(paths + ["--budget", "1000"])
            self.assertIn("300  TOTAL", out.getvalue())
        finally:
            for p in paths:
                os.unlink(p)

    def test_skips_missing_file_but_measures_the_rest(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("x" * 400)
        try:
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = main([f.name, "/nonexistent/file.txt"])
            self.assertEqual(code, 0)
            self.assertIn("100  TOTAL", out.getvalue())
            self.assertIn("skip /nonexistent/file.txt", err.getvalue())
        finally:
            os.unlink(f.name)

    def test_measures_piped_text(self):
        script = os.path.join(SCRIPTS, "estimate_tokens.py")
        r = subprocess.run([sys.executable, script, "--budget", "50"], input="x" * 400,
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)  # ~100 tokens is over a 50 budget
        self.assertIn("100  TOTAL", r.stdout)

    def test_no_input_shows_usage_instead_of_waiting(self):
        class Terminal(io.StringIO):
            def isatty(self):
                return True

        err = io.StringIO()
        with mock.patch("sys.stdin", Terminal()), contextlib.redirect_stderr(err):
            self.assertEqual(main([]), 2)
        self.assertIn("usage:", err.getvalue())

    def test_unreadable_files_are_an_error(self):
        self.assertEqual(main(["/nonexistent/file.txt"]), 2)

    def test_budget_must_be_positive(self):
        with self.assertRaises(SystemExit):
            main(["--budget", "0", __file__])


if __name__ == "__main__":
    unittest.main()
