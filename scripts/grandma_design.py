#!/usr/bin/env python3
"""GRANDMASTER grandma — design batch (Sean-authorized, gpt-image/Higgsfield).

Net-new character. Establish the YOUNG-warrior reveal look first, then age that
same face into the warm old photo (unmistakably one woman). Register = primal-grit,
staged as aged photographs. Run per-preset:

    python scripts/grandma_design.py young        # the 1970s warrior reveal (fresh)
    python scripts/grandma_design.py old_with_kid # aged same face + the kid (edit)
"""
import sys
from pathlib import Path

from pipeline.agents.nb_pro_runner import invoke_image_edit

RUN = Path("runs/2026-07-14-grandmaster-kid-design")
YOUNG = RUN / "grandma-young-warrior.png"
KID_TURN = RUN / "kid-daytime-turnaround.png"  # for family resemblance + the boy

PRIMAL = (
    "Raw hand-drawn register of Genndy Tartakovsky's Primal: visible weight-varying ink "
    "linework, gritty painterly texture, warm earthy desaturated palette."
)

PRESETS = {
    "young": {
        "sources": [],  # fresh text-to-image (no ref) — but invoke needs >=1; see main()
        "prompt": (
            "COMPLETELY REPLACE THE SUBJECT of the reference image: do NOT depict the boy — "
            "keep ONLY the reference's art-style and rendering treatment. Depict instead "
            "a single image styled as an OLD, FADED 1970s PHOTOGRAPH / film still — grainy, "
            "worn, softly yellowed, the look of a treasured decades-old snapshot — of a "
            "YOUNG woman in her late twenties: a 1970s kung-fu movie heroine caught MID "
            "FLYING-KICK in a dynamic martial-arts pose, fierce, airborne, unmistakably "
            "capable and real. She wears a faded cloth headband tied around her forehead "
            "(a specific, characterful headband). Period 1970s martial-arts attire. Brown "
            "skin, dark hair pulled back, a specific striking memorable face — a real "
            "person, not a generic action hero. Dramatic and iconic, like a frame from the "
            "vintage kung-fu movies a grieving boy keeps on his wall. " + PRIMAL
            + " No text, no watermark."
        ),
    },
    "old_with_kid": {
        "sources": [YOUNG, KID_TURN],
        "prompt": (
            "Using the FIRST reference for the woman's face/identity and the SECOND "
            "reference for the young boy's face: a warm, ordinary, slightly faded OLD "
            "PHOTOGRAPH of an ELDERLY grandmother and her young grandson together. She is "
            "the SAME woman as the first reference but now about seventy years old — grey "
            "hair, a gentle lined face, a soft warm smile, the same eyes and bone "
            "structure. Her arm is around the timid young bespectacled boy from the second "
            "reference. An everyday tender family snapshot; she is kind and specific, never "
            "a stereotype. Faded warm worn photograph. " + PRIMAL + " No text, no watermark."
        ),
    },
}


def main() -> int:
    which = sys.argv[1]
    spec = PRESETS[which]
    out = RUN / f"grandma-{'young-warrior' if which == 'young' else which}.png"
    RUN.mkdir(parents=True, exist_ok=True)
    # gpt-image needs at least one reference image; for the fresh 'young' gen we seed
    # with a register exemplar so the transport has an input, and lean on the prompt.
    sources = spec["sources"] or [
        Path("registers/primal-sketch-grit/refs/grandmaster-chosen-pose-1.png")
    ]
    print(f"[{which}] sources={[str(s) for s in sources]} -> {out}")
    resp = invoke_image_edit(
        prompt=spec["prompt"],
        reference_images=sources,
        output_path=out,
        cache_dir=RUN / ".cache",
        model="gpt-image-2",
        aspect_ratio=None,
        timeout_s=600,
    )
    print(f"[{which}] ok={getattr(resp, 'ok', None)} exit={getattr(resp, 'exit_code', None)} "
          f"job={getattr(resp, 'job_id', None)} size={out.stat().st_size if out.exists() else 0}")
    return 0 if getattr(resp, "ok", False) else 1


if __name__ == "__main__":
    raise SystemExit(main())
