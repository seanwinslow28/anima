#!/usr/bin/env python3
"""
MOVEMENT 2 — candidate cameras, one dict entry each. Roughed by make_shot_roughs.py
into m2-candidates/ at $0. Every entry is a PROPOSAL for Sean's eye; nothing here is
ratified. The `note` on each is the named specific the camera is for.

Naming: B<beat>-<letter>. Beat 3½ is B3h. Letters are just order, not rank; the
lean per beat is stated in the session record, not encoded here.

Everything draws room state B (the red M2 fixtures) unless a shot says otherwise.
"""
from make_shot_roughs import REST, who

# Where everyone stands for the reaction beat: at their rest spots, turned to the CRT.
# Beat 3½ plays in room state A — the room reacts BEFORE anything is wrecked. Grok has
# stepped off his corner toward the screen, so he enters HUGE from frame-right.
ROOM = [REST["sean"], REST["claude"], REST["codex"], REST["gemini"],
        who("grok", 21.0, 6.8)]
ALL_CORNERS = ["SEAN&#8217;S DESK", "PAPER TOWER", "SERVER RACK", "worktable",
               "side table", "DARTBOARD", "filing cabinet", "storage cabinet",
               "water cooler", "storage bench"]

M2 = {
    # ── 3½ · THE ROOM REACTS · the CRT's own point of view ────────────────
    # The CRT sits on the east wall, x 24.6–26, y 10.7–12.9, z 6.5–9.0.
    # The lens sits at the CRT's glass (x 24.6 is the screen face), never inside the box.
    "B3h-A": dict(pos=(24.4, 11.8), eye=7.75, fill=0.98, on=ALL_CORNERS,
                  cast=ROOM, on_cast=True, state="A",
                  note="THE ALARM LOOKS BACK — lens IN the screen, 7'9\" up, "
                       "level with the room. Grok and Gemini near and big, Sean "
                       "middle, Claude and Codex tiny at the far wall."),
    "B3h-B": dict(pos=(24.3, 11.8), eye=9.6, pitch=-14, fill=0.98, on=ALL_CORNERS,
                  cast=ROOM, on_cast=True, state="A",
                  note="BIRD'S EYE from just above the CRT — steeper, more floor, "
                       "the room as a map with five dots turning."),
    # NOT the CRT's eye — the honest alternative. The room's longest axis is the
    # SE→NW diagonal, so this is the widest the scale-as-distance idea can ever get.
    "B3h-C": dict(pos=(25.2, 17.0), eye=9.4, pitch=-8, fill=0.98, on=ALL_CORNERS,
                  cast=ROOM, on_cast=True, state="A",
                  note="THE HIGH CORNER — not a POV: a ceiling corner above the "
                       "moodboard wrap looking down the room's long diagonal, "
                       "Claude at the far end of it."),


    # ── 4 · THE SILENT GO · Sean, turned to the room, seen from the room ──
    # Sean ruled 2026-09-03: 3½ is locked; beat 4 is a medium or closeup of Sean turned
    # around, the mascots looking at him for the GO. Chair spun 180° from the monitors,
    # so the three screens sit behind his head. State A: nothing is wrecked yet.
    "B4-A": dict(pos=(13.5, 7.6), eye=2.3, pitch=2, fill=0.96,
                 on=["three monitors"],
                 cast=[who("sean", 13.5, 3.6, seated=True)], on_cast=True, state="A",
                 note="FROM THEIR HEIGHT — the lens at a mascot's eye level, 2′3″ off "
                      "the floor, looking slightly up at him. The room literally looks up "
                      "to him; the monitors glow behind his head."),
    "B4-B": dict(pos=(13.5, 7.4), eye=5.0, pitch=-2, fill=0.96,
                 on=["three monitors"],
                 cast=[who("sean", 13.5, 3.6, seated=True)], on_cast=True, state="A",
                 note="EYE LEVEL MEDIUM — a plain medium from the room, level with him. "
                      "Neutral, and the same camera beat 12's swivel could reuse."),
    "B4-C": dict(pos=(13.5, 8.8), eye=3.0, pitch=0, fill=0.96,
                 on=["three monitors"],
                 cast=[who("sean", 13.5, 3.6, seated=True), who("grok", 15.4, 7.0),
                       who("claude", 11.7, 6.9)], on_cast=True, state="A",
                 note="OVER THEIR SHOULDERS — Grok and Claude's backs in the bottom "
                      "corners of frame, Sean between them. The looking-at-him is in the shot."),
    # ── 5 · CLAUDE'S 40-PAGE DOC · the NW corner ──────────────────────────
    "B5-A": dict(pos=(3.6, 7.8), eye=0.8, pitch=10, fill=0.92,
                 on=["PAPER TOWER", "second stack"],
                 cast=[who("claude", 2.0, 4.8)],
                 note="WORM'S EYE UP THE TOWER — lens on the floor, the paper "
                      "canyon going out the top of frame, Claude small at its foot."),
    "B5-B": dict(pos=(4.6, 6.4), eye=9.3, pitch=-10, fill=0.92,
                 on=["supply desk", "PAPER TOWER", "second stack"],
                 cast=[who("claude", 2.0, 4.6)],
                 note="HIGH DOWN INTO THE NOOK — from above the filing cabinet, "
                      "Claude buried at the bottom of the frame, paper everywhere."),
    "B5-C": dict(pos=(5.2, 8.2), eye=2.6, pitch=0, fill=0.90,
                 on=["PAPER TOWER", "second stack", "binder shelf"],
                 cast=[who("claude", 2.2, 4.6)],
                 note="RAKING NORTH ALONG THE WEST WALL — from the doorway, low, "
                      "the stacks receding like a skyline."),

    # ── 6 · CODEX REBUILDS EVERYTHING · the code wall over the counter ────
    "B6-A": dict(pos=(8.4, 14.3), eye=5.5, pitch=-2, fill=0.90,
                 on=["THE CODE WALL", "coffee counter", "SERVER RACK", "water cooler"],
                 cast=[who("codex", 3.2, 14.2)],
                 note="SQUARE ON THE CODE WALL — the lit wall of scrolling code "
                      "fills the top of frame, Codex tiny at the counter beneath it."),
    "B6-B": dict(pos=(5.0, 12.4), eye=1.0, pitch=8, fill=0.92,
                 on=["SERVER RACK", "THE CODE WALL"],
                 cast=[who("codex", 3.0, 13.8)],
                 note="LOW UP THE RACK — the rack as a monolith, code wall lit "
                      "beside it, Codex at its foot."),
    # A raking angle from the doorway was tried and dropped: the rack stands between
    # the doorway and the code wall and hides it completely. Replaced with a high angle.
    "B6-C": dict(pos=(7.6, 15.8), eye=9.4, pitch=-8, fill=0.90,
                 on=["SERVER RACK", "coffee counter", "THE CODE WALL", "water cooler"],
                 cast=[who("codex", 3.3, 14.3)],
                 note="HIGH DOWN ON THE COUNTER — from above the cooler, the code wall "
                      "lit below the lens, Codex a dot at the counter, cables everywhere."),

    # ── 7 · GEMINI'S FIFTY CONCEPTS · the moodboard ───────────────────────
    "B7-A": dict(pos=(17.0, 10.4), eye=5.5, pitch=-7, fill=0.86,
                 on=["board wraps SE", "moodboard wraps"],
                 cast=[who("gemini", 21.4, 15.4)],
                 note="THE WRAP CORNER — concepts turning the SE corner onto the "
                      "CRT wall: the board has escaped its wall."),
    "B7-B": dict(pos=(4.4, 14.4), eye=4.0, pitch=-6, fill=0.92,
                 on=["GEMINI&#8217;S MOODBOARD", "worktable"],
                 cast=[who("gemini", 9.6, 16.0)],
                 note="RAKING EAST ALONG THE BOARD — fifty concepts receding to a "
                      "vanishing point, Gemini in the foreground."),
    "B7-C": dict(pos=(11.5, 8.0), eye=9.4, pitch=-12, fill=0.90,
                 on=["GEMINI&#8217;S MOODBOARD", "worktable"],
                 cast=[who("gemini", 10.6, 16.2)],
                 note="HIGH DOWN ON THE WORKTABLE — the wall, the table and the "
                      "floor all papered, seen from above the string lights."),

    # ── 8 · GROK DEMOLISHES THE WALL · THE HOLE in the NE corner ──────────
    "B8-A": dict(pos=(17.5, 7.2), pitch=-3, fill=0.82,
                 on=["side table", "DARTBOARD", "crates"],
                 cast=[who("grok", 23.4, 3.0)],
                 note="THE S06 CAMERA, WRECKED — the corner the audience knows, "
                      "with the hole where the side table was and the rocket leaning out."),
    "B8-B": dict(pos=(19.0, 2.0), eye=2.2, pitch=2, fill=0.85,
                 on=["THE HOLE", "DARTBOARD"],
                 cast=[who("grok", 22.8, 4.0)],
                 note="LOW AND SQUARE TO THE HOLE — along the north wall, the "
                      "breach face-on, the rocket nose coming at the lens."),
    "B8-C": dict(pos=(21.2, 6.0), eye=9.3, pitch=-14, fill=0.88,
                 on=["THE HOLE", "side table", "crates", "DARTBOARD"],
                 cast=[who("grok", 23.0, 3.8)],
                 note="HIGH DOWN ON THE RUBBLE — the hole, the debris field on the "
                      "floor, and Grok in the middle of it, from above."),
}
