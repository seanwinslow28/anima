"""The canonical home of anima's closed style_register vocabulary.

One frozen RegisterSpec per register; every register touch-point reads from
here instead of carrying its own copy:

- ``character_designer._build_plate_prompt`` / ``_resolve_plate_model``
  (the clause library + model routing that used to live in
  ``_REGISTER_CLAUSE_LIBRARY`` / ``_REGISTER_MODELS``),
- ``character_designer._STUB_STYLE_REGISTER_BY_KEYWORD`` (derived from the
  specs' ``stub_keywords``),
- ``tests/test_prompt_style_neutrality.py`` (``ALL_REGISTERS`` + markers),
- the human touch-points — the ``character.yaml.template`` permitted-values
  comment and Cy's ``## What good looks like`` blocks — stay prose, and
  ``tests/test_register_registry.py`` enforces they exist per register.

The vocabulary is CLOSED (the style-neutrality doctrine's thesis:
validators cannot recover taste that was absent at generation time). The
registry makes closedness enforced rather than conventional:

- a **nonempty, unrecognized** register (a typo, or a style nobody has
  authored yet) raises :class:`UnknownRegisterError` — loud, never a
  silent coercion to the pencil default;
- an **empty/missing** register is the CALLER's back-compat case — every
  pre-registry character folder relies on empty defaulting to
  ``pencil-test-colored``, so callers pass
  ``get_register(value or DEFAULT_REGISTER)``.

Adding a register is the five-step drill in
docs/COMPLETED/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md
§1.3: research → one RegisterSpec entry here → the Cy example block → the
template-comment line → run the suite (the completeness tests refuse to
pass until all of them exist).

Values for the six existing registers are copied VERBATIM from the
pre-registry tables in character_designer.py / test_prompt_style_neutrality.py
(commit 4a75500); tests/test_register_characterization.py is the
byte-identical oracle proving nothing shifted for the locked Bibles.
"""

from __future__ import annotations

from dataclasses import dataclass

# Google GA image ids replace the -preview ids deprecated 2026-06-25; repinned
# 2026-07-13 per the transport decision D3 rider. NB2 is the
# generation/editing default for most registers (cheaper, faster, more
# identity-stable across edits) — primal-sketch-grit is the exception (its
# costed spike resolved generation to gpt-image, fork #1, 2026-07-11); NB Pro
# is reserved for painterly FINAL renders — a documented seam with no
# consumer yet. The registry records the HONEST model per register; transport
# ownership stays separate (the Gemini-only SUPPORTED_IMAGE_MODELS allowlist
# plus the Higgsfield model map), and an unknown model fails at the boundary.
NB2_FLASH = "gemini-3.1-flash-image"
NB_PRO = "gemini-3-pro-image"
# The GA flagship gpt-image id, pinned against the openai-image-gen skill
# (.claude/skills/openai-image-gen/references/openai-image-capabilities.md).
# invoke_image_edit dispatches this exact id through Higgsfield; it deliberately
# remains outside the Gemini-only SUPPORTED_IMAGE_MODELS allowlist.
GPT_IMAGE = "gpt-image-2"

# The back-compat default. Empty/missing style_register still means the
# pencil-test reference register; the constant lives here so callers spell
# the rule identically.
DEFAULT_REGISTER = "pencil-test-colored"


class UnknownRegisterError(ValueError):
    """A nonempty style_register that is not in the closed vocabulary.

    Raised loud at lookup time so a typo (or an unauthored style) can never
    silently author a pencil-test character. Subclasses ValueError so broad
    caller guards still catch it.
    """

    def __init__(self, name: str):
        self.name = name
        known = ", ".join(sorted(REGISTRY))
        super().__init__(
            f"unknown style_register {name!r} — not in the closed vocabulary "
            f"({known}). Adding a register is a deliberate commit: see "
            f"docs/architecture/prompt-style-neutrality-doctrine.md and "
            f"pipeline/registers.py."
        )


@dataclass(frozen=True)
class RegisterSpec:
    """One deliberately-authored style register. All fields are data the
    touch-points read; the register's *taste* (the Cy worked example, the
    research write-up, the refs/) stays prose and files, enforced-present
    by tests/test_register_registry.py."""

    name: str
    summary: str  # one line for the character.yaml.template human list
    identity_lock: str  # was _REGISTER_CLAUSE_LIBRARY[name]["identity_lock"]
    preserve: str  # was _REGISTER_CLAUSE_LIBRARY[name]["preserve"]
    style_token: str  # was _REGISTER_CLAUSE_LIBRARY[name]["style_token"]
    generation_model: str  # was _REGISTER_MODELS[name]["generation"]
    final_model: str  # was _REGISTER_MODELS[name]["final"]
    markers: frozenset[str]  # was test_prompt_style_neutrality._REGISTERS_TO_MARKERS
    stub_keywords: tuple[str, ...] = ()  # reverse of _STUB_STYLE_REGISTER_BY_KEYWORD
    reference_images: tuple[str, ...] = ()  # registers/{name}/refs/ exemplars


# NOTE: insertion order is load-bearing for ONE consumer — the derived stub
# keyword map (character_designer._STUB_STYLE_REGISTER_BY_KEYWORD) preserves
# the pre-registry precedence (mascot, pixel, watercolor, lineart, photoreal,
# 3d), which requires watercolor's spec to come before line-art-only's.
# tests/test_register_characterization.py pins the precedence edges.
REGISTRY: dict[str, RegisterSpec] = {
    spec.name: spec
    for spec in (
        RegisterSpec(
            name="pencil-test-colored",
            summary=(
                "Sean's Act 1/2 register. Warm cream paper, varied graphite "
                "line weight, hand-drawn construction lines, limited "
                "desaturated palette, visible cross-hatching."
            ),
            identity_lock=(
                "Match the face, hair, full color palette, skin tone, and "
                "proportions of Image 1 exactly."
            ),
            preserve=(
                "Keep the warm cream paper, the cross-hatch shadow, and the full "
                "color of Image 1. Do not render the figure in monochrome. No "
                "photographic shading."
            ),
            style_token=(
                "Warm pencil-test render: graphite line (not vector black), flat "
                "color fills, cross-hatch shadow, warm cream paper, hole-punch "
                "production marks."
            ),
            generation_model=NB2_FLASH,
            final_model=NB2_FLASH,
            markers=frozenset({
                "cross-hatching",
                "construction lines",
                "graphite",
                "cream paper",
                "varied 1-3px",
                "pencil-test rough",
                "pencil-test-colored",
            }),
        ),
        RegisterSpec(
            name="pixel-art-8bit",
            summary=(
                "Claude mascot's register. Quantized palette, dithering "
                "patterns, sub-32-color flat fills."
            ),
            identity_lock=(
                "Match the indexed palette, the round silhouette, and the "
                "head-to-body ratio of Image 1 exactly."
            ),
            preserve="Hard pixel edges. No smooth anti-aliased gradients.",
            style_token=(
                "16-bit pixel-art sprite, limited indexed palette, hard pixel "
                "edges, clean outlines."
            ),
            generation_model=NB2_FLASH,
            final_model=NB2_FLASH,
            markers=frozenset({
                "dithering",
                "integer-pixel grid",
                "anti-aliasing",
                "closed palette",
                "indexed palette",
                "closed indexed palette",
                "limited indexed palette",
                "pixel-art-8bit",
            }),
            stub_keywords=("mascot", "pixel"),
        ),
        RegisterSpec(
            name="watercolor",
            summary="Soft wet-media bleeds, paper grain, layered washes.",
            identity_lock=(
                "Match the face, the pigment-pool palette, and the proportions of "
                "Image 1 exactly."
            ),
            preserve="Keep the paper grain; let washes bleed; no hard vector edges.",
            style_token="Soft watercolor wash, pigment-pool bleed, visible paper grain.",
            generation_model=NB2_FLASH,
            final_model=NB_PRO,
            markers=frozenset({
                "watercolor",
                "edge-feathering",
                "pigment-pool",
                "paper grain",
                "wet-media",
            }),
            stub_keywords=("watercolor",),
        ),
        RegisterSpec(
            name="line-art-only",
            summary="Pure black-on-white linework, no color, no fill.",
            identity_lock=(
                "Match the contour shapes, line weight, hair silhouette, and "
                "proportions of Image 1 exactly."
            ),
            preserve=(
                "No shading, no gradients, no soft shadow, no texture; flat color "
                "fills only."
            ),
            style_token="Clean line art, bold uniform outlines, flat fills.",
            generation_model=NB2_FLASH,
            final_model=NB2_FLASH,
            markers=frozenset({"line-art-only"}),
            stub_keywords=("lineart",),
        ),
        RegisterSpec(
            name="photoreal",
            summary="Photographic rendering, lit volumes, surface detail.",
            identity_lock=(
                "Match the face, skin tone, hair, and proportions of Image 1 exactly."
            ),
            preserve=(
                "Keep the lighting direction and color temperature of Image 1; "
                "clean edges, no halos."
            ),
            style_token=(
                "Photographic rendering, natural lighting, shallow depth of field."
            ),
            generation_model=NB2_FLASH,
            final_model=NB_PRO,
            markers=frozenset({
                "photoreal",
                "lit volume",
                "surface detail",
                "specular",
            }),
            stub_keywords=("photoreal",),
        ),
        RegisterSpec(
            name="3d-rendered",
            summary="Constructed geometry, raytraced or PBR shading.",
            identity_lock=(
                "Match the face, material palette, and proportions of Image 1 exactly."
            ),
            preserve="Keep soft global illumination; no flat-shading artifacts.",
            style_token=(
                "3D-rendered look, soft global illumination, subtle ambient "
                "occlusion."
            ),
            generation_model=NB2_FLASH,
            final_model=NB_PRO,
            markers=frozenset({"3d-rendered", "raytraced", "pbr shading"}),
            stub_keywords=("3d",),
        ),
        # The first post-registry register (Checkpoint 2, 2026-07-03) —
        # GRANDMASTER's Tartakovsky-*Primal* register, authored from the
        # CORRECTED deep research (registers/primal-sketch-grit/research.md):
        # organic-illustrative with a heavy weight-varying ink contour kept
        # OVER the color — NOT flat-angular, and NOT the candy/oil-geyser
        # blood-substitution (that is Samurai Jack's convention; GRANDMASTER
        # borrows it as a deliberate cross-register staging choice). The
        # pencil-test negative controls (no graphite/cream-paper vocabulary)
        # deliberately do NOT appear as prompt negatives here — naming them
        # can evoke them in the image model; drift policing lives in the Cy
        # example block + risk-bible review checks instead. Transport
        # RESOLVED (fork #1, 2026-07-11, Sean-ratified): the §3c NB2
        # hypothesis was judged by the costed spike and generation batched to
        # gpt-image — GPT_IMAGE is the honest recorded model, wired through
        # the separate Higgsfield mapping (SUPPORTED_IMAGE_MODELS remains the
        # exact Gemini-only google-genai allowlist). final_model stays NB Pro
        # (the dormant painterly-final seam; fork #1 scopes only generation).
        RegisterSpec(
            name="primal-sketch-grit",
            summary=(
                "Tartakovsky-Primal register. Heavy weight-varying ink kept "
                "over the color, gritty painterly figure and background, warm "
                "earthy desaturated base, one bold color statement per scene."
            ),
            identity_lock=(
                "Match the face, hair, color palette, proportions, and "
                "silhouette of Image 1 exactly; the heavy ink contour is "
                "surface treatment and must never alter the anatomy."
            ),
            preserve=(
                "Keep the drawn ink line visible over every color area — "
                "thick, near-black, weight varying with mass and silhouette, "
                "deliberately imperfect. Keep the gritty hand-painted texture "
                "on both figure and background and the warm earthy desaturated "
                "base palette. No clean uniform outlines, no outline-free "
                "color-field flatness, no smooth digital gradients or airbrush "
                "polish."
            ),
            style_token=(
                "Raw seventies-pulp 2D animation still: heavy weight-varying "
                "ink line kept over the color, gritty painterly brushwork "
                "shared by figure and background, flat earthy fills with drawn "
                "tonal shading, warm earthy desaturated palette punctuated by "
                "a single bold color statement."
            ),
            generation_model=GPT_IMAGE,
            final_model=NB_PRO,
            markers=frozenset({
                "primal-sketch-grit",
                "weight-varying ink",
                "gritty painterly texture",
                "warm earthy desaturated",
                "line-work kept over the color",
                "dead-stop hold",
            }),
            stub_keywords=("primal",),
        ),
        # Register #2 of the vocabulary expansion (2026-07-11) — the ai-guru
        # pilot's 90s-Nicktoon gross-out school, authored from the wire-ready
        # research (registers/90s-nicktoon-grossout/research.md, Sean-ratified
        # 2026-07-04 cross-engine spike). Two load-bearing corrections baked
        # in: (a) the DEFAULT is the appealing, warm, clean cel-cartoon human
        # (~90% of frames) — the hyper-rendered grotesque gross-out extreme
        # close-up is SPARSE comedic punctuation (one or two beats), never the
        # lead's resting state (research §0; the grotesque-forward first draft
        # was rejected); (b) genericization is doubly load-bearing (research
        # §7) — the register is a school of grotesque cel animation captured
        # attribute-only, no show/artist/creator name in any clause, marker,
        # or comment, and named-source negatives stay OUT of `preserve`
        # (naming a neighbor look can evoke it in the image model; drift
        # policing lives in the Cy example block + risk-bible review checks).
        # Transport: NB2 GO (the spike found NB2 renders both poles — flat
        # appealing base and the gross-up ECU, best of the engines tested), so
        # no forced escalation, unlike primal-sketch-grit.
        RegisterSpec(
            name="90s-nicktoon-grossout",
            summary=(
                "90s-Nicktoon grotesque cel / gross-out register. Flat rubbery "
                "cel figures on solid-then-broken construction over painted, "
                "slightly-decaying backgrounds; a desaturated grimy ground "
                "punctured by one lurid accent; the signature move is a hard "
                "cut-in to a held, hyper-rendered painterly gross-out extreme "
                "close-up."
            ),
            identity_lock=(
                "Match the face, hair, color palette, proportions, and "
                "silhouette of Image 1 exactly. The character is built from "
                "solid wrapped 3D construction (rigid cranium sphere, hinged "
                "elastic jaw/cheek/mouth mass, eye-spheres in sockets); all "
                "distortion is a volume-preserving deformation of these "
                "persistent forms and must never lose the character — the "
                "cranium and identity features stay constant while the "
                "jaw-balloon and eyes are pushed. If the character is not "
                "recognizably itself at the peak of the distortion, the "
                "construction was lost and the frame fails."
            ),
            preserve=(
                "Keep the bold thick-and-thin hand-inked outline where every "
                "line describes a form — heaviest on the outer silhouette and "
                "the undersides of forms, detail lines thinnest and tapering "
                "to points. Keep self-colored (darker-value-of-fill) interior "
                "and organic edges; flat cel color body with hard-edged "
                "cast-shadow shapes; hue-turned, saturation-lifted shadows, "
                "never flat value-darkened. Keep painted, moody, "
                "slightly-decaying backgrounds under flat figures, and a "
                "desaturated grimy ground with exactly one lurid "
                "over-saturated accent. Reserve full continuous-tone photoreal "
                "rendering (wet specular highlights, pores, veins, drips) ONLY "
                "for the isolated gross-out extreme close-up, held one beat "
                "past a normal cut. No clean uniform vector or anime keyline; "
                "no single flat rendering register (the gross-out close-up "
                "must break register); no muted-earthy geometric abstraction "
                "held on-model; no globally photoreal or rendered frame "
                "(rendering stays quarantined to the insert); no flat "
                "value-only shadows; no sanitized clean-glossy surface."
            ),
            style_token=(
                "90s-Nicktoon appealing cel-cartoon animation still: an "
                "expressive, warm, likable hand-inked human — bold "
                "thick-and-thin outline with a logical line-weight hierarchy, "
                "self-colored interior edges, a small round nose, big earnest "
                "eyes, solid appealing construction and squash-and-stretch; "
                "flat cel fills with hard-edged shadow shapes over a warm "
                "harmonious palette (warm peach skin; golden-spotlight or cozy "
                "lived-in grounds); optional hue-turned saturated shadows. For "
                "occasional comedy beats only (never the default), a hard "
                "cut-in to a held, hyper-rendered painterly grotesque "
                "gross-out extreme close-up."
            ),
            generation_model=NB2_FLASH,
            final_model=NB_PRO,
            markers=frozenset({
                "90s-nicktoon-grossout",
                "hyper-rendered gross-out insert",
                "flat cel hard shadow shapes",
                "desaturated ground one lurid accent",
                "hue-turned saturated shadow",
                "solid-construction-then-broken",
                "self-colored swelling ink line",
            }),
            stub_keywords=("nicktoon", "grossout"),
        ),
        # Register #3 of the vocabulary expansion (2026-07-11) — the
        # flat-cinematic Tartakovsky sibling, GRANDMASTER's revised
        # style/identity-hold fallback and one of Sean's two committed go-to
        # registers. Authored from the wire-ready research
        # (registers/samurai-jack-s5/research.md, LOOK RATIFIED — HERO LOCKED
        # 2026-07-13; a live composition-phrase A/B kept all five money-phrases
        # in the injected clause). It is the mutually-exclusive FLAT sibling of
        # primal-sketch-grit: every still-frame axis inverts — where primal
        # keeps a heavy weight-varying ink line OVER the color and paints gritty
        # texture everywhere, samurai-jack-s5 has almost no visible outline
        # (form reads by adjacent color and value contrast), clean flat
        # poster-graphic color shapes, and hard-edged flat shadow masses. Two
        # load-bearing facts: (a) genericization is doubly load-bearing
        # (research §7) — the register is a school of flat cinematic 2D
        # poster-art captured attribute-only, no show/creator/character/studio
        # name in any clause, marker, or comment; named-source negatives stay
        # OUT of `preserve` (naming a neighbor look can evoke it in the image
        # model; drift policing lives in the Cy example block + risk-bible
        # checks); (b) transport = gpt-image (GPT_IMAGE, "gpt-image-2") —
        # wired through the separate Higgsfield mapping while
        # SUPPORTED_IMAGE_MODELS stays the exact Gemini-only google-genai
        # allowlist. final_model stays NB Pro (the dormant painterly-final
        # seam; no consumer yet).
        RegisterSpec(
            name="samurai-jack-s5",
            summary=(
                "Flat cinematic poster-art register. Clean outline-sparse color "
                "shapes, hard-edged flat shadow masses, dramatic negative "
                "space, and one emotional color cast staged with silent-film "
                "clarity."
            ),
            identity_lock=(
                "Match the face, hair, color palette, proportions, and "
                "silhouette of Image 1 exactly. Simplification may remove "
                "interior detail but must preserve the character's unique "
                "silhouette, facial landmarks, and long-axis proportions as "
                "readable flat shapes."
            ),
            preserve=(
                "Keep clean flat color shapes with almost no visible outlines; "
                "define edges through adjacent color and value contrast. Keep "
                "hard-edged flat shadow shapes, restrained facial detail, "
                "dramatic cinematic negative space, and one dominant emotional "
                "color cast across figure and setting. No soft airbrushed "
                "modeling, no rendered volumetric shading, and no busy interior "
                "detail that weakens the silhouette."
            ),
            style_token=(
                "Dark minimalist cinematic 2D poster-art still: clean flat "
                "color shapes, almost no visible outlines, sharp angular "
                "silhouette, long elegant proportions, hard-edged flat shadow "
                "shapes, bold value blocking, dramatic negative space, a single "
                "emotional color cast, and silent-samurai-film staging."
            ),
            generation_model=GPT_IMAGE,
            final_model=NB_PRO,
            markers=frozenset({
                "samurai-jack-s5",
                "outline-sparse flat color shapes",
                "hard-edged flat shadow masses",
                "single emotional color cast",
                "dramatic cinematic negative space",
                "silent-samurai-film staging",
            }),
            stub_keywords=("samurai",),
            # reference_images left default () — no code reads it (red-team
            # fold); the locked hero + provenance live in refs/README.md.
        ),
        # Register #4 of the vocabulary expansion (2026-07-13) — the mixed-media
        # "fusion" register Sean selected by eye (costed Higgsfield image spike +
        # Seedance 2.0 motion test; his eye the sole arbiter). Authored from the
        # wire-ready research (registers/flat-cast-painted-world/research.md, LOOK
        # RATIFIED — HERO LOCKED 2026-07-13). Its identity IS the deliberate
        # TWO-MEDIA SPLIT: a flat, boldly hand-inked cel CAST (living boiling
        # outline, flat cel color, NO rendered volume) that POPS against a richly
        # hand-PAINTED gritty children's-storybook WORLD (dry-brush weathered
        # urban surfaces, muted earthy palette, folk-decorative flourishes,
        # gouache washes, golden-hour grime) — two media in one frame, unified
        # only by the shared warm light + a faint grain. Mutually exclusive from
        # its neighbors on that split: vs Collage Real (painted world, not
        # photographic), vs Gritty Storybook (two media, not one unified paint),
        # vs primal-sketch-grit (grit stays OFF the flat-cel figure vs ink kept
        # OVER the color everywhere), vs samurai-jack-s5 (bold boiling outline +
        # gritty painted world vs near-no-outline + clean flats + negative space).
        # Two load-bearing facts: (a) genericization is doubly load-bearing
        # (research §7) — a school of mixed-media 2D craft captured attribute-only,
        # no show/creator/character/studio name in any clause, marker, or comment;
        # named-source negatives stay OUT of `preserve` (naming a neighbor can
        # evoke it) — in particular the world's real cross-hatched texture is
        # written as "dry-brush / hatched" so pencil-test's `cross-hatch` never
        # leaks. (b) transport = gpt-image (GPT_IMAGE, "gpt-image-2") — wired
        # through the separate Higgsfield mapping: the Step-S NB2 confirmation
        # spike came back NO-GO (NB2
        # collapsed the two-media split into one unified medium and dropped the
        # boiling line), so GPT_IMAGE is the honest recorded model.
        # SUPPORTED_IMAGE_MODELS stays the exact Gemini-only google-genai
        # allowlist. final_model stays NB Pro (the dormant painterly-final seam).
        RegisterSpec(
            name="flat-cast-painted-world",
            summary=(
                "Mixed-media register: a flat, boldly hand-inked cel cast with a "
                "living boiling outline and no rendered volume, popping against a "
                "richly hand-painted gritty children's-storybook world — muted "
                "earthy palette, weathered urban surfaces, folk-decorative "
                "flourishes, golden-hour warmth. Two media, one frame."
            ),
            identity_lock=(
                "Match the face, hair, color palette, proportions, and silhouette "
                "of Image 1 exactly. The character is a flat graphic shape read by "
                "its bold outline and silhouette; the boiling line is surface "
                "treatment on the contour only and must never swim the "
                "proportions, features, or flat colors off-model."
            ),
            preserve=(
                "Keep the cast flat: a bold thick-to-thin hand-inked outline "
                "heaviest on the outer silhouette, a living boiling wobble on the "
                "contour, flat unmodulated cel color inside, and no rendered "
                "volume on the figures. Keep the world a separate hand-painted "
                "medium: dry-brush, scumbled, hatched, weathered urban surfaces, "
                "soft gouache washes, folk-decorative flourishes, and a muted "
                "earthy palette under one warm golden-hour key. Keep the two media "
                "legibly distinct — the flat graphic cast reads against the "
                "painterly world, unified only by the shared warm light and a "
                "faint overall grain. No airbrushed or volumetric modeling on the "
                "figures; no photographic or rendered world; no clean "
                "vector-smooth outline."
            ),
            style_token=(
                "Mixed-media 2D animation still — two media in one frame: a flat, "
                "boldly hand-inked cartoon cast with a living boiling outline, "
                "flat cel color, and no rendered volume, popping against a richly "
                "hand-painted gritty children's-storybook world of dry-brush "
                "weathered urban surfaces, folk-decorative flourishes, soft "
                "gouache washes, and a muted earthy palette (ochre, brick-red, "
                "sage, cream) under warm golden-hour light."
            ),
            generation_model=GPT_IMAGE,
            final_model=NB_PRO,
            markers=frozenset({
                "flat-cast-painted-world",
                "boiling hand-inked cast outline",
                "flat cel cast no rendered volume",
                "hand-painted gritty storybook world",
                "two-media split",
                "muted earthy ochre-brick-sage-cream",
            }),
            stub_keywords=("fusion",),
            # reference_images left default () — no code reads it (red-team
            # fold); the locked hero + provenance live in refs/README.md.
        ),
    )
}

ALL_REGISTERS: frozenset[str] = frozenset(REGISTRY)


def get_register(name: str) -> RegisterSpec:
    """Look up a register by exact name. Nonempty-unknown raises loud.

    Callers own the empty/missing back-compat rule:
    ``get_register(value or DEFAULT_REGISTER)``.
    """
    try:
        return REGISTRY[name]
    except KeyError:
        raise UnknownRegisterError(name) from None
