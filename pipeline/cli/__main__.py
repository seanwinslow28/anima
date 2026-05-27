"""anima CLI dispatcher.

Usage:
  python -m pipeline.cli patches list --run-dir runs/{run_id}
  python -m pipeline.cli plan init --target briefs/{date}-{slug}
  python -m pipeline.cli plan show --plan briefs/{date}-{slug}/plan.md
  python -m pipeline.cli plan approve --brief-dir briefs/{date}-{slug}
  python -m pipeline.cli plan mutate --force --actor <name> --reason "<why>" \
      --target AC.<id> --field <field> --value <value> \
      --brief-dir briefs/{date}-{slug} --run-dir runs/{run_id} \
      --new-version 1.2.0
"""

from __future__ import annotations

import argparse
import sys

from pipeline.cli import patches, plan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m pipeline.cli")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # ----- patches -----
    patches_p = sub.add_parser("patches", help="Survey staged proposed_patches.")
    patches_sub = patches_p.add_subparsers(dest="patches_cmd", required=True)
    list_p = patches_sub.add_parser(
        "list", help="List staged patches in a run dir, grouped by persona.",
    )
    list_p.add_argument("--run-dir", required=True, type=str)

    # ----- plan -----
    plan_p = sub.add_parser("plan", help="Maya the planner — init / show / approve / mutate.")
    plan_sub = plan_p.add_subparsers(dest="plan_cmd", required=True)

    init_p = plan_sub.add_parser("init", help="Scaffold a new brief directory.")
    init_p.add_argument("--target", required=True, type=str)

    show_p = plan_sub.add_parser("show", help="Render plan.md as a terminal tear sheet.")
    show_p.add_argument("--plan", required=True, type=str)

    approve_p = plan_sub.add_parser("approve", help="Lock the brief's criteria file.")
    approve_p.add_argument("--brief-dir", required=True, type=str)

    mutate_p = plan_sub.add_parser("mutate", help="Audited mutation of an approved plan.")
    mutate_p.add_argument("--force", action="store_true")
    mutate_p.add_argument("--actor", default="", type=str)
    mutate_p.add_argument("--reason", default="", type=str)
    mutate_p.add_argument("--target", required=True, type=str)
    mutate_p.add_argument("--field", required=True, type=str)
    mutate_p.add_argument("--value", required=True, type=str)
    mutate_p.add_argument("--brief-dir", required=True, type=str)
    mutate_p.add_argument("--run-dir", required=True, type=str)
    mutate_p.add_argument("--new-version", required=True, type=str)

    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    if args.cmd == "patches" and args.patches_cmd == "list":
        return patches.list_patches(args.run_dir)

    if args.cmd == "plan":
        if args.plan_cmd == "init":
            return plan.init_plan(args.target)
        if args.plan_cmd == "show":
            return plan.show_plan(args.plan)
        if args.plan_cmd == "approve":
            return plan.approve_plan(args.brief_dir)
        if args.plan_cmd == "mutate":
            return plan.mutate_plan(
                run_dir=args.run_dir,
                brief_dir=args.brief_dir,
                force=args.force,
                actor=args.actor,
                reason=args.reason,
                target=args.target,
                field=args.field,
                value=args.value,
                new_version=args.new_version,
            )

    return 1


if __name__ == "__main__":
    sys.exit(main())
