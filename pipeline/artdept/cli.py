"""python -m pipeline.artdept validate <dir> — validate only, no scaffold.

Exit codes: 0 valid, 1 problems found, 2 usage/missing dir. Register warnings
print on every path but never affect the exit code: an unauthored register at
the Art Department is a called dependency, not a failure (the hard gate is Cy).
"""

from __future__ import annotations

import argparse
from pathlib import Path

from pipeline.artdept.validate import register_warnings, validate_artdept_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m pipeline.artdept",
        description="Art Department bundle-dir contract checks.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    p_validate = sub.add_parser("validate", help="Validate an Art Department bundle dir.")
    p_validate.add_argument("bundle_dir", metavar="DIR")
    args = parser.parse_args(argv)

    bundle_dir = Path(args.bundle_dir)
    if not bundle_dir.is_dir():
        print(f"error: {bundle_dir} is not a directory")
        return 2
    problems = validate_artdept_dir(bundle_dir)
    for w in register_warnings(bundle_dir):
        print(f"WARN: {w}")
    if problems:
        for p in problems:
            print(f"FAIL: {p}")
        return 1
    print(f"ok: {bundle_dir} is a valid Art Department bundle dir")
    return 0
