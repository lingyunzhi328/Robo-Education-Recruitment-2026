"""Supplement the official grader with observable spec edge cases."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_program(source):
    return subprocess.run([sys.executable, str(ROOT / "src/main.py")], input=source,
                          text=True, capture_output=True, encoding="utf-8")


class SpecEdges(unittest.TestCase):
    def check(self, source, expected):
        process = run_program(source)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stdout, expected)

    def test_only_false_is_false(self):
        self.check("(if 0 1 2) (if '() 3 4) (and) (or) (and #f missing) (or 0 missing)",
                   "1\n3\n#t\n#f\n#f\n0\n")

    def test_parallel_let_and_lexical_closure(self):
        self.check("(define x 10) (let ((x 1) (y x)) y) "
                   "(define (make x) (lambda (y) (+ x y))) "
                   "(define f (make 3)) (let ((x 100)) (f 2))",
                   "x\n10\nmake\nf\n5\n")

    def test_exact_large_integer_division(self):
        self.check("(/ -100000000000000000000000000001 3) (/ 2) (/ 20 3 2) "
                   "(quotient 7 -2) (quotient -7 -2)",
                   "-33333333333333333333333333333\n0.5\n3\n-3\n3\n")

    def test_pair_identity_and_type_distinctions(self):
        self.check("(define p (list 1 2)) (eq? p p) (eq? p (list 1 2)) "
                   "(equal? p '(1 2)) (equal? #t 1) (equal? 'a \"a\") "
                   "(eq? '() '()) '(1 2 . 3) (cdr '(1 . 2))",
                   "p\n#t\n#f\n#t\n#f\n#f\n#t\n(1 2 . 3)\n2\n")

    def test_string_escapes_and_comment_delimiters(self):
        self.check('"x;()\\n\\t\\\"\\\\" ; comment\n(display "ok") (newline)',
                   '"x;()\\n\\t\\\"\\\\"\nok\n')

    def test_cond_returns_test_and_missing_branches_print_nothing(self):
        self.check("(cond ((+ 1 2))) (cond (#f 1)) (if #f 2) (begin)", "3\n")

    def test_multiple_files_share_global_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            first, second = Path(directory)/"a.scm", Path(directory)/"b.scm"
            first.write_text("(define x 20)", encoding="utf-8")
            second.write_text("(+ x 22)", encoding="utf-8")
            process = subprocess.run([sys.executable, str(ROOT/"src/main.py"), str(first), str(second)],
                                     text=True, capture_output=True, encoding="utf-8")
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(process.stdout, "x\n42\n")

    def test_malformed_input_reports_error(self):
        for source in ["(1", '"unterminated', "(1 . 2 3)", "(car 1)", "missing"]:
            with self.subTest(source=source):
                process = run_program(source)
                self.assertEqual(process.returncode, 1)
                self.assertIn("Error:", process.stderr)


if __name__ == "__main__":
    unittest.main()
