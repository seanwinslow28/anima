#!/usr/bin/env python3
"""One-off GRANDMASTER kid design look-test (Sean-authorized, gpt-image/Higgsfield).

Edits a master-kid reference into the TIMID Act-1 (pre-training) design, holding
identity + register from the source. Not a Cy Bible plate — an exploratory design
look-test that also exercises the across-edit identity gate. Run per-register:

    python scripts/kid_design_looktest.py primal   # edits pose-1 (gritty Primal)
    python scripts/kid_design_looktest.py warm      # edits pose-3 (warm cream-paper)
"""
import sys
from pathlib import Path

from pipeline.agents.nb_pro_runner import invoke_image_edit

RUN = Path("runs/2026-07-14-grandmaster-kid-design")
SOURCES = {
    "primal": Path("registers/primal-sketch-grit/refs/grandmaster-chosen-pose-1.png"),
    "warm": Path("registers/primal-sketch-grit/refs/grandmaster-chosen-pose-3.png"),
}

WIMPY_PROMPT = (
    "Redraw this same boy — identical face, head shape, messy black hair, skin tone, "
    "and the EXACT same drawing/rendering style, linework, palette, and texture as this "
    "reference image — as the TIMID, un-trained version of himself at a suburban backyard "
    "birthday party one year EARLIER, before any training.\n\n"
    "Full-body, three-quarter standing view. His body language reads shy and small: "
    "shoulders drawn inward and hunched, chin tucked down, weight on the back foot, one "
    "hand nervously gripping the hem of his t-shirt, eyes cast down and away — he avoids "
    "looking toward the camera.\n\n"
    "He wears large round eyeglasses a size too big for his face, sliding down his nose "
    "(this is NEW — the reference has no glasses). He does NOT wear a headband (he does not "
    "have it yet). Plain, clean, tidy everyday t-shirt, shorts, and sneakers — undirtied.\n\n"
    "Keep his identity, his small-young-child proportions, and the reference's exact art "
    "style, linework, colour palette and texture. Keep the background a simple, softly-lit, "
    "mostly-empty backyard so the figure reads clearly. Cinematic. No text, no watermark."
)


def main() -> int:
    which = sys.argv[1] if len(sys.argv) > 1 else "primal"
    src = SOURCES[which]
    out = RUN / f"kid-wimpy-{which}.png"
    RUN.mkdir(parents=True, exist_ok=True)
    print(f"[{which}] source={src}  ->  {out}")
    resp = invoke_image_edit(
        prompt=WIMPY_PROMPT,
        reference_images=[src],
        output_path=out,
        cache_dir=RUN / ".cache",
        model="gpt-image-2",
        aspect_ratio=None,
        timeout_s=600,
    )
    print(f"[{which}] ok={getattr(resp, 'ok', None)} "
          f"cache_hit={getattr(resp, 'cache_hit', None)} "
          f"exit={getattr(resp, 'exit_code', None)} "
          f"job={getattr(resp, 'job_id', None)}")
    print(f"[{which}] result_url={getattr(resp, 'result_url', None)}")
    print(f"[{which}] output exists={out.exists()} "
          f"size={out.stat().st_size if out.exists() else 0}")
    return 0 if getattr(resp, "ok", False) else 1


if __name__ == "__main__":
    raise SystemExit(main())
