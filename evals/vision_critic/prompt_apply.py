"""G6.9 Gate 3 (pure core) — corpus parsing + deterministic diff splice.

The empirical loop (patch_efficacy.py) needs to turn "Em's corrective clause" plus
"the prompt that produced the defect fixture" into a single re-generation prompt,
deterministically — NO LLM "apply" step, which would smear the very signal Gate 3
exists to attribute to Em's diff. This module is that splice, kept pure (no model,
no I/O beyond reading the committed corpus markdown) so it is fully unit-testable.

Two responsibilities:
  parse_corpus(md)            -> {corpus_id: prompt_text} from the fixture-corpus md
  build_corrected_prompt(...) -> the re-generation prompt for one corrected case

Apply-mechanism (the deliberate, documented choice):
  The base is the defect case's CLEAN PAIR prompt (every defect case pairs with a
  clean C01–C16 fixture), NOT the defect prompt. "clean stem + Em's corrective
  clause" is exactly "the defect prompt with Em's substitution applied," and the
  pair gives an EXACT clean stem by construction — no fragile defect-clause parsing
  (the corpus introduces defects three different ways: ", but …", ", rendered …",
  ", drawn …"), and no stripped-style-line to restore (the clean pair carries the
  full canonical style line already). Two specials this module handles:
  - the corrected prompt ALWAYS re-emits the full canonical style line, so a
    palette/shading correction can never ship axis-deficient.
  - view-correctness defects are label-side (the image is pixel-correct, the
    declared view is wrong) — a re-generation cannot clear them, so the splice
    REFUSES and the caller takes a no-regeneration branch.

  KNOWN ATTRIBUTION CAVEAT (deferred to the costed phase — a Sean-decision on real
  Em patch semantics): a clean base means a USELESS corrective clause can still
  regenerate a clean frame (the scene itself isn't defective), inflating fix-rate.
  The golden arm (positive control) + the identity/style-held re-critique are what
  keep the signal honest; the costed run refines the apply rule against real diffs.
"""
from __future__ import annotations

import re
from pathlib import Path

# The verbatim full style line (corpus md "The style line (verbatim, every prompt)").
# Re-emitted on EVERY corrected prompt so a defect prompt that stripped its axis
# phrase (monochrome -> color wash; shading -> cross-hatch) is restored to full.
CANONICAL_STYLE_LINE = (
    "Maintain the warm 2D Disney pencil-test render: soft graphite line "
    "(not vector black), light hand-painted color wash, cross-hatch shadow, "
    "warm cream paper."
)

_STYLE_MARKER = "Maintain the warm 2D Disney pencil-test render"

# A corpus id: letters, optional dash-segment, digits (C01, P-D1, PA-D2, CL-B1, …).
# Requires a trailing digit so non-id bold spans (e.g. **Totals**) never match.
_ID_LINE = re.compile(
    r"^\*\*(?P<id>[A-Z]{1,2}(?:-[A-Z])?-?\d{1,2})\*\*"   # **C01** / **P-D1** / **PA-D2**
    r"\s*(?:\*\([^)]*\)\*)?"                              # optional *(pair … note)*
    r"\s*[—-]\s*"                                         # the em-dash (or -) separator
    r"(?P<prompt>.+?)\s*$"
)


class NoRegenForView(Exception):
    """build_corrected_prompt refuses a view-correctness case: the defect is in the
    declared view (cases.yaml beat_description), not the pixels, so re-generation
    cannot clear it. The caller must correct the declared view and re-critique the
    SAME fixture instead."""


def parse_corpus(md_path: Path | str) -> dict[str, str]:
    """Parse the fixture-corpus markdown into {corpus_id: prompt_text}.

    One bold-id line == one entry. Full prompts (clean pool + generated defects)
    carry the style marker; the hand-drawn borderline notes do not — both are
    returned, and the caller distinguishes them (a note is not regeneratable).
    """
    out: dict[str, str] = {}
    for line in Path(md_path).read_text(encoding="utf-8").splitlines():
        m = _ID_LINE.match(line.strip())
        if not m:
            continue
        out[m.group("id")] = m.group("prompt").strip()
    return out


def has_full_prompt(text: str) -> bool:
    """True when a parsed entry is a regeneratable prompt (carries the style line),
    False for a hand-drawn borderline note."""
    return _STYLE_MARKER in text


def clean_stem_of(base_prompt: str) -> str:
    """The scene/pose description of a CLEAN prompt, with its style line removed.

    Contract: pass a clean (pair) prompt. As a cheap guard the ', but …' defect tail
    is dropped if present, but defect prompts that inject the corruption mid-sentence
    (', rendered …' / ', drawn …') are NOT reliably strippable — that is caller error
    by the clean-pair contract, not something this function pretends to repair."""
    idx = base_prompt.find(_STYLE_MARKER)
    body = (base_prompt[:idx] if idx != -1 else base_prompt).strip()
    bi = body.lower().find(", but ")
    if bi != -1:
        body = body[:bi]
    return body.strip().rstrip(" .,")


def build_corrected_prompt(base_prompt: str, corrective_clause: str, *, label: str) -> str:
    """Make the re-generation prompt: the clean stem (from the defect case's PAIR
    prompt) + the corrective clause + the canonical full style line.

    `base_prompt` is the CLEAN PAIR prompt (see module docstring). Raises
    NoRegenForView for view-correctness, ValueError for an empty clause.
    """
    if label == "view-correctness":
        raise NoRegenForView(
            "view-correctness is label-side; correct the declared view and "
            "re-critique the same fixture — do not regenerate.")
    clause = corrective_clause.strip().rstrip(".").strip()
    if not clause:
        raise ValueError("empty corrective clause")
    return f"{clean_stem_of(base_prompt)}, {clause}. {CANONICAL_STYLE_LINE}"
