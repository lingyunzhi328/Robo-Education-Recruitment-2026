"""CLI: python src/main.py [file1.scm file2.scm ...]."""
import sys
from pathlib import Path
from evaluator import evaluate
from parser import parse
from primitives import initial_environment
from printer import format_value
from values import SchemeError


def main(argv=None):
    paths = sys.argv[1:] if argv is None else argv
    environment = initial_environment()
    sys.setrecursionlimit(10000)
    try:
        sources = (Path(path).read_text(encoding="utf-8-sig") for path in paths) if paths else [sys.stdin.read()]
        for source in sources:
            for expression in parse(source):
                result = evaluate(expression, environment)
                if result is not None:
                    print(format_value(result))
    except (SchemeError, OSError, RecursionError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
