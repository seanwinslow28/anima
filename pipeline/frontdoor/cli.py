"""python -m pipeline.frontdoor validate <dir> — validate only, no scaffold (A6).

Exit codes: 0 valid, 1 problems found, 2 usage/missing dir.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from pipeline.frontdoor.validate import validate_brief_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m pipeline.frontdoor",
        description="Front-door brief-dir contract checks.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    p_validate = sub.add_parser("validate", help="Validate a front-door brief dir.")
    p_validate.add_argument("brief_dir", metavar="DIR")
    args = parser.parse_args(argv)

    brief_dir = Path(args.brief_dir)
    if not brief_dir.is_dir():
        print(f"error: {brief_dir} is not a directory")
        return 2
    problems = validate_brief_dir(brief_dir)
    if problems:
        for p in problems:
            print(f"FAIL: {p}")
        return 1
    print(f"ok: {brief_dir} is a valid front-door brief dir")
    return 0
