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
  python -m pipeline.cli bible init --target characters/{character_id}/
  python -m pipeline.cli bible show --character-dir characters/{character_id}/
  python -m pipeline.cli bible approve --character-dir characters/{character_id}/
  python -m pipeline.cli bible mutate --force --actor <name> --reason "<why>" \
      --target IR.<character_id>.<category>.<handle> --field <field> --value <value> \
      --character-dir characters/{character_id}/ --run-dir runs/{run_id} \
      --new-version 1.3.0
  python -m pipeline.cli bible add --character-dir characters/{character_id}/ \
      --spec characters/{character_id}/additions.json \
      --force --actor <name> --reason "<why>" \
      --run-dir runs/{run_id} --content-version 1.1.0
  python -m pipeline.cli bible iterate --character-dir characters/{character_id}/ \
      --target turnarounds,expressions --reject neutral,surprised \
      --reason "<why>" --run-dir runs/{run_id}
"""

from __future__ import annotations

import argparse
import sys

from pipeline.cli import bible, patches, plan


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

    # ----- bible (Cy — character designer) -----
    bible_p = sub.add_parser(
        "bible",
        help="Cy the character designer — init / show / approve / mutate / iterate.",
    )
    bible_sub = bible_p.add_subparsers(dest="bible_cmd", required=True)

    b_init = bible_sub.add_parser("init", help="Scaffold a new character bible folder.")
    b_init.add_argument("--target", required=True, type=str)

    b_show = bible_sub.add_parser("show", help="Render the Bible as a terminal tear sheet.")
    b_show.add_argument("--character-dir", required=True, type=str)

    b_approve = bible_sub.add_parser("approve", help="Lock the character's criteria file.")
    b_approve.add_argument("--character-dir", required=True, type=str)

    b_check_prop = bible_sub.add_parser(
        "check-proportion",
        help="Read-only SF03 proportion check over the body turnarounds (G6.4).",
    )
    b_check_prop.add_argument("--character-dir", required=True, type=str)

    b_mutate = bible_sub.add_parser("mutate", help="Audited mutation of an approved Bible.")
    b_mutate.add_argument("--force", action="store_true")
    b_mutate.add_argument("--actor", default="", type=str)
    b_mutate.add_argument("--reason", default="", type=str)
    b_mutate.add_argument("--target", required=True, type=str)
    b_mutate.add_argument("--field", required=True, type=str)
    b_mutate.add_argument("--value", required=True, type=str)
    b_mutate.add_argument("--character-dir", required=True, type=str)
    b_mutate.add_argument("--run-dir", required=True, type=str)
    b_mutate.add_argument(
        "--new-version", required=False, default=None, type=str,
        help="Optional content revision; recorded as content_version. Does NOT "
             "touch the schema version field (which stays 1.2).",
    )

    b_add = bible_sub.add_parser(
        "add",
        help="Audited additive path: append new plates + IR rules to a locked Bible.",
    )
    b_add.add_argument("--character-dir", required=True, type=str)
    b_add.add_argument("--spec", required=True, type=str,
                       help="JSON file with {\"plates\": [...], \"rules\": [...]}.")
    b_add.add_argument("--force", action="store_true")
    b_add.add_argument("--actor", default="", type=str)
    b_add.add_argument("--reason", default="", type=str)
    b_add.add_argument("--run-dir", required=True, type=str)
    b_add.add_argument(
        "--content-version", required=False, default=None, type=str,
        help="Optional content revision recorded as content_version (NOT the schema version).",
    )

    b_iterate = bible_sub.add_parser(
        "iterate",
        help="Re-run Cy narrowed to rejected plates (preserves cache hits).",
    )
    b_iterate.add_argument("--character-dir", required=True, type=str)
    b_iterate.add_argument(
        "--target", default="", type=str,
        help="Comma-separated plate categories (turnarounds,expressions,motion_plates,...).",
    )
    b_iterate.add_argument(
        "--reject", default="", type=str,
        help="Comma-separated plate handles to regenerate (e.g., neutral,surprised).",
    )
    b_iterate.add_argument("--reason", default="", type=str)
    b_iterate.add_argument("--run-dir", default="", type=str)

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

    if args.cmd == "bible":
        if args.bible_cmd == "init":
            return bible.init_bible(args.target)
        if args.bible_cmd == "show":
            return bible.show_bible(args.character_dir)
        if args.bible_cmd == "approve":
            return bible.approve_bible(args.character_dir)
        if args.bible_cmd == "check-proportion":
            return bible.check_proportion_bible(args.character_dir)
        if args.bible_cmd == "mutate":
            return bible.mutate_bible(
                run_dir=args.run_dir,
                character_dir=args.character_dir,
                force=args.force,
                actor=args.actor,
                reason=args.reason,
                target=args.target,
                field=args.field,
                value=args.value,
                content_version=args.new_version,
            )
        if args.bible_cmd == "add":
            return bible.add_to_bible(
                run_dir=args.run_dir,
                character_dir=args.character_dir,
                force=args.force,
                actor=args.actor,
                reason=args.reason,
                spec_path=args.spec,
                content_version=args.content_version,
            )
        if args.bible_cmd == "iterate":
            targets = [t.strip() for t in args.target.split(",") if t.strip()]
            rejected = [r.strip() for r in args.reject.split(",") if r.strip()]
            return bible.iterate_bible(
                character_dir=args.character_dir,
                targets=targets,
                rejected=rejected,
                reason=args.reason,
                run_dir=args.run_dir or None,
            )

    return 1


if __name__ == "__main__":
    sys.exit(main())
