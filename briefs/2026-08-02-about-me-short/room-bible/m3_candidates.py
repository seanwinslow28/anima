#!/usr/bin/env python3
"""
MOVEMENT 3, wave 3b — candidate cameras for the three NEW Sean setups. Roughed by
`python3 make_shot_roughs.py m3` into m3-candidates/ at $0. Every entry is a PROPOSAL
for Sean's eye; the lean per setup is stated in the session record, not encoded here.

Naming: S<setup>-<letter>. S15 = beat 11/12 the super wide · S19 = beat 10.5 the side
close-up · S16 = beat 13.1 the monitors' POV. Everything draws room state B (the red M2
fixtures: the code wall, the hole) — the state-C wreck is prose in the plate prompt.

S15 recreates art-viz/route-c--gpt-ref.png — a super wide of the WRECKED room, Sean at
the centre, NOT from the CRT alarm's POV (Sean, 2026-09-06). The inspiration is an
impossible camera: it sees the doorway (west), Sean's desk (north) and the hole (east)
at once, which no lens inside a 26x18 room can. Candidate A copies that honestly as a
CUTAWAY — the south wall removed and the lens standing behind its plane. Candidate B is
a real lens at the south wall with the chaos pulled into the middle of the room, the
inspiration's ARRANGEMENT rather than its geometry. C is the compromise the wave-3b doc
allows for: the high SE corner.
"""
from make_shot_roughs import REST, who

# ── S15 · the super wide, room state C ─────────────────────────────────────────
# A: everyone in their TRUE corner. Gemini stands before where her (removed) wall would
#    be, at the right, so the whirl has the foreground. Sean at the desk, back to the room.
TRUE_CORNERS = [REST["sean"], REST["claude"], REST["codex"], REST["grok"],
                who("gemini", 19.5, 14.0)]
# B: the inspiration's arrangement — chaos SPILLED to the centre. Codex tugs a wire from
#    the computer tower at the LEFT of the desk; Gemini spins at the RIGHT; Claude's pages
#    and Grok's rubble pulled towards the middle.
SPILLED = [REST["sean"], who("claude", 7.0, 6.8), who("codex", 10.3, 4.6),
           who("gemini", 18.2, 6.4), who("grok", 22.4, 4.6)]
# For the two Sean close-ups the lens aims at his head-and-shoulders (z 2.4–4.3 seated),
# not the whole seated block — otherwise the solve pitches down into his lap.
SEAN_BUST = who("sean", 13.5, 3.4, seated=True, z0=2.4)
SEAN_HEAD = who("sean", 13.5, 3.2, h=4.3, w=1.3, z0=2.6)   # head + shoulders only, for the monitors' POV
WIDE_ON = ["SEAN&#8217;S DESK", "PAPER TOWER", "SERVER RACK", "DOORWAY", "THE HOLE",
           "DARTBOARD", "THE CRT", "filing cabinet", "storage bench", "water cooler"]

M3 = {
    "S15-A": dict(pos=(13.0, 28.0), eye=7.0, pitch=-3, fill=0.97, on=WIDE_ON,
                  cast=TRUE_CORNERS, on_cast=True, omit=["south"],
                  note="WIDER THAN REAL — a cutaway: the south wall removed, the lens 10 ft "
                       "behind where it stood. Every corner is its true corner: Claude NW "
                       "far-left, Codex SW near-left at the rack, Grok NE far-right at the "
                       "hole, Sean centre, Gemini near-right where her wall was. An "
                       "impossible camera, like the inspiration."),
    "S15-B": dict(pos=(13.0, 17.4), eye=6.2, pitch=-6, fill=0.95,
                  on=["SEAN&#8217;S DESK", "PAPER TOWER", "DOORWAY", "THE HOLE", "DARTBOARD"],
                  cast=SPILLED, on_cast=True,
                  note="CHAOS SPILLED TO THE CENTRE — a real lens at the south wall's "
                       "middle. Codex tugging a wire from the tower LEFT of the desk, "
                       "Gemini's spin RIGHT of it, Claude's pages and Grok's rubble pulled "
                       "into the middle of the floor: the inspiration's arrangement inside "
                       "a possible room."),
    "S15-C": dict(pos=(25.0, 17.2), eye=9.4, pitch=-10, fill=0.98, on=WIDE_ON,
                  cast=TRUE_CORNERS, on_cast=True,
                  note="THE HIGH SE CORNER — the compromise: a ceiling-corner lens down "
                       "the room's long diagonal, true corners, Claude at the far end. "
                       "The solver caps it at 86°, not 110°; and it stands 5 ft from the "
                       "CRT, so it risks reading as the alarm's POV."),

    # ── S19 · beat 10.5, the side close-up of Sean's desk from the CRT's side ──────
    # The S09 lens (the CRT glass at 24.4, 11.8) pushed in along its own line towards the
    # desk, dropped to his eye level. He faces the desk; when he looks up-right at the CRT
    # his face turns TOWARDS this camera, which is the whole reason the camera is on this side.
    "S19-A": dict(pos=(19.4, 8.0), eye=4.8, pitch=0, fill=0.78,
                  on=["three monitors"], cast=[SEAN_BUST], on_cast=True,
                  note="THE S09 LINE, PUSHED IN — the CRT-side camera walked to 7 ft from "
                       "his chair, at his eye level. ¾ back-profile on the desk; the look "
                       "up-right at the CRT turns his face to us."),
    "S19-B": dict(pos=(19.6, 4.6), eye=4.6, pitch=0, fill=0.78,
                  on=["three monitors"], cast=[SEAN_BUST], on_cast=True,
                  note="SIDE-ON — square to the east side of the desk, a true profile with "
                       "the monitors edge-on at left. The fists-up pose reads cleanest; "
                       "the look up-right is a smaller turn."),

    # ── S16 · beat 13.1, the monitors' POV ─────────────────────────────────────────
    # The lens at desk height between the monitors, looking SOUTH at his face; the room
    # (wrecked, state C) is what lies behind him.
    "S16-A": dict(pos=(13.5, 0.7), eye=3.5, pitch=0, fill=0.45,
                  on=[], cast=[SEAN_HEAD], on_cast=True,
                  note="BETWEEN THE MONITORS — the lens at screen height on the desk, a "
                       "medium on his face, the wrecked room falling away behind him."),
    "S16-B": dict(pos=(13.5, 0.7), eye=2.9, pitch=4, fill=0.5,
                  on=[], cast=[SEAN_HEAD], on_cast=True,
                  note="FROM THE KEYBOARD — lower, looking up a little: a hair more "
                       "ceiling, the chair back framing his shoulders. The monitors' "
                       "reverse of beat 4's low angle."),
}
