"""Eval-side prompt-quality lint for the storyboard suite (Tier 1 Slice A).

NOT a production gate — Bea's production structural pass is coverage + script↔board
cast-conflict only, and the human still curates every board at the `storyboard
approve` gate. This is the ONE deterministic prompt-quality warning the first
costed-run post-mortem (Findings 2 + 3) sanctions:

  On a chained pencil-test loop, frame 1 is the establishing generation built from
  the Bibles — a full descriptive prompt is correct there. Every LATER frame is an
  NB2 *edit* off the prior approved frame, so it must be a terse delta, not a full
  re-description: verbose prose competes with the reference image and drifts the
  identities (2026-05-30 NB2-editing research). The accepted terse forms are the
  chained edit (`Same … ONLY CHANGE: <single delta>`) and the loop-return match
  (`composition identical to frame 1`).

edit_frame_form_lint flags any non-establishing frame whose prompt reads as a full
re-description instead of a terse edit delta. It is a warning (the runner asserts
it FLAGS the F2 anti-pattern and ACCEPTS the terse form) — never wired into
production storyboard_validate, because the taste/composition call is Sean's.
"""

from __future__ import annotations

import re

from pipeline.orchestration.shots import ShotList

# The two terse edit-delta forms an NB2 edit frame (id >= 2) may take:
#   - the chained edit:     "Same …, same framing/identities … ONLY CHANGE: <delta>"
#   - the loop-return match: "Composition identical to frame 1"
_ONLY_CHANGE = re.compile(r"only change\s*:", re.IGNORECASE)
_LOOP_MATCH = re.compile(r"identical to frame\s*1", re.IGNORECASE)


def is_edit_delta(prompt: str) -> bool:
    """True if the prompt is a terse edit delta (an `ONLY CHANGE:` opener or a
    loop-return `identical to frame 1` match) rather than a fresh re-description."""
    return bool(_ONLY_CHANGE.search(prompt) or _LOOP_MATCH.search(prompt))


def edit_frame_form_lint(shot_list: ShotList) -> list[int]:
    """Return the ids of non-establishing frames (id >= 2) authored as a full
    re-description instead of a terse edit delta. Empty list = clean.

    Frame id == 1 is the establishing generation and is exempt — a full descriptive
    prompt is correct there. The lint is order-by-id, not position, so it is robust
    to the shot list's frame ordering.
    """
    return sorted(
        s.id for s in shot_list.frames if s.id >= 2 and not is_edit_delta(s.prompt)
    )
