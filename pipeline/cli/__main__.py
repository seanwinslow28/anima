"""anima CLI dispatcher.

Usage:
  python -m pipeline.cli patches list --run-dir runs/{run_id}
"""

from __future__ import annotations

import argparse
import sys

from pipeline.cli import patches


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m pipeline.cli")
    sub = parser.add_subparsers(dest="cmd", required=True)

    patches_p = sub.add_parser("patches", help="Survey staged proposed_patches.")
    patches_sub = patches_p.add_subparsers(dest="patches_cmd", required=True)

    list_p = patches_sub.add_parser(
        "list", help="List staged patches in a run dir, grouped by persona.",
    )
    list_p.add_argument("--run-dir", required=True, type=str)

    args = parser.parse_args(argv if argv is not None else sys.argv[1:])
    if args.cmd == "patches" and args.patches_cmd == "list":
        return patches.list_patches(args.run_dir)
    return 1


if __name__ == "__main__":
    sys.exit(main())
