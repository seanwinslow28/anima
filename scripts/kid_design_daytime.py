#!/usr/bin/env python3
"""GRANDMASTER kid — daytime design batch (Sean-authorized, gpt-image/Higgsfield).

Edits the agreed wimpy look-test into flat-daylight, neutral-read design views so
the kid's face/personality are unambiguous and Cy gets a clean anchor. Register held
= primal-sketch-grit (source carries it). Run per-preset:

    python scripts/kid_design_daytime.py turnaround
    python scripts/kid_design_daytime.py candid
    python scripts/kid_design_daytime.py wide
"""
import sys
from pathlib import Path

from pipeline.agents.nb_pro_runner import invoke_image_edit

RUN = Path("runs/2026-07-14-grandmaster-kid-design")
WIMPY = RUN / "kid-wimpy-primal.png"  # the agreed wimpy design (glasses, no headband)
MASTER = Path("registers/primal-sketch-grit/refs/grandmaster-chosen-pose-1.png")

# Per-preset source override (default = WIMPY).
SOURCES = {"master_turnaround": MASTER}

REGISTER = (
    "Keep the reference's EXACT art style — raw visible hand-drawn ink linework with "
    "weight variation, gritty painterly texture, warm earthy desaturated palette "
    "(primal-sketch-grit register) — and keep his identity and small-young-child "
    "proportions. Change the lighting to flat, even, neutral SUNNY-AFTERNOON DAYLIGHT: "
    "this is a daytime kids' party, NOT sunset — remove all dramatic golden-hour glow "
    "and deep shadow so his face reads clearly."
)

PRESETS = {
    "turnaround": (
        "Character-design TURNAROUND model sheet of this same timid boy, shown from FOUR "
        "angles in a row on one sheet — front, three-quarter, side profile, and back — "
        "standing in a relaxed natural neutral pose (arms at his sides, a slight shy "
        "slouch), consistent height and proportions across all four views. He wears his "
        "round too-big glasses and plain everyday t-shirt, shorts and sneakers; NO "
        "headband. Plain empty neutral off-white model-sheet background so every angle of "
        "his design and face is legible. " + REGISTER + " No text, no labels, no watermark."
    ),
    "candid": (
        "Medium shot of this same timid boy standing ALONE at the edge of a suburban "
        "backyard kids' birthday party, holding a paper cup with both hands, shoulders "
        "hunched, watching the other kids from the sidelines with a shy, wistful, "
        "left-out expression — he wants to join but can't. He wears his too-big round "
        "glasses and plain t-shirt, shorts and sneakers; NO headband. Colourful party "
        "details (streamers, a table) soft behind him. " + REGISTER
        + " No text, no watermark."
    ),
    "wide": (
        "WIDE establishing shot of a suburban backyard kids' birthday party. On the RIGHT "
        "side of the frame a group of kids play together, laughing and active. In the "
        "distant BACKGROUND toward the left, small in the frame and ALONE, stands the same "
        "timid boy — too-big round glasses, plain t-shirt and shorts, NO headband — "
        "watching the group from far away, shoulders hunched, left out and apart. The "
        "composition isolates him with lots of empty space between him and the group. "
        + REGISTER + " No text, no watermark."
    ),
    "master_turnaround": (
        "Character-design TURNAROUND model sheet of this same boy as his TRAINED, "
        "confident MASTER self (one year later), shown from FOUR angles in a row on one "
        "sheet — front, three-quarter, side profile, and back — standing in a relaxed but "
        "SELF-ASSURED, grounded stance: chin level, shoulders open, calm and centred (the "
        "opposite of a shy slouch), consistent height and proportions across all four "
        "views. He now wears his late grandmother's faded headband FITTED snugly around his "
        "forehead, and he has NO glasses. Same everyday t-shirt, shorts and sneakers, a "
        "little worn from training. Plain empty neutral off-white model-sheet background so "
        "every angle reads clearly. " + REGISTER
        + " Keep the SAME face and identity as the reference — same boy, now composed and "
        "capable rather than dramatic. No text, no labels, no watermark."
    ),
}


def main() -> int:
    which = sys.argv[1]
    out = RUN / f"kid-daytime-{which}.png"
    src = SOURCES.get(which, WIMPY)
    RUN.mkdir(parents=True, exist_ok=True)
    print(f"[{which}] source={src} -> {out}")
    resp = invoke_image_edit(
        prompt=PRESETS[which],
        reference_images=[src],
        output_path=out,
        cache_dir=RUN / ".cache",
        model="gpt-image-2",
        aspect_ratio=None,
        timeout_s=600,
    )
    print(f"[{which}] ok={getattr(resp, 'ok', None)} "
          f"exit={getattr(resp, 'exit_code', None)} job={getattr(resp, 'job_id', None)} "
          f"size={out.stat().st_size if out.exists() else 0}")
    return 0 if getattr(resp, "ok", False) else 1


if __name__ == "__main__":
    raise SystemExit(main())
