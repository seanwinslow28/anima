#!/usr/bin/env python3
"""
CONTACT SHEETS for the wave-3b camera candidates — one sheet per new setup, $0. Same
idea as ../m2-candidates/make_sheets.py: a reference tile ("what we are recreating" or
"what the audience saw") beside the candidate roughs, a LEAN badge on the session's
recommendation. A proposal, never a decision.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); BRIEF = os.path.dirname(RB)
sys.path.insert(0, RB)
from m3_candidates import M3  # noqa: E402
sys.path.insert(0, os.path.join(RB, "m2-candidates"))
from make_sheets import fit, wrap, font, tile, TILE_W, TILE_H, CAP_H, GAP, PAD, PAPER, INK, INK2, RULE  # noqa: E402

LEANS = {"S15": "A", "S19": "A", "S16": "A"}
SHEETS = [
    ("S15", "11/12 · THE SUPER WIDE", "the wrecked room, Sean swivels to the chaos, record scratch, freeze · NOT the CRT's POV",
     "art-viz/route-c--gpt-ref.png", "THE INSPIRATION — art-viz/route-c--gpt-ref.png (an impossible camera)"),
    ("S19", "10.5 · SEAN ALONE NOTICES", "a side close-up of his desk from the CRT's side: fists-up → looks up at the CRT, confused",
     "normalised/S09-all-webapp-v2.png", "BEAT 3½ · the S09 CRT-POV wide (locked) — this camera walked in"),
    ("S16", "13.1 · THE MONITORS' POV", "a medium on his face from between the monitors: turns back calm, eyes open on us",
     "normalised/S10-sean-swivel-v1.png", "BEAT 12 · the S10 swivel start (locked) — the same face, from the room side"),
]

def sheet_for(key, head, sub, refimg, refcap):
    cands = [k for k in M3 if k.startswith(key + "-")]
    n = 1 + len(cands); cols = 2; rows = (n + 1) // 2
    W = PAD * 2 + cols * TILE_W + (cols - 1) * GAP
    H = PAD * 2 + 96 + rows * (TILE_H + CAP_H) + (rows - 1) * GAP
    s = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(s)
    d.text((PAD, PAD), head, font=font(34, True), fill=INK)
    d.text((PAD, PAD + 44), sub, font=font(19), fill=INK2)
    d.text((W - PAD - 470, PAD + 4), "camera roughs · $0 · make_shot_roughs.py m3", font=font(15), fill=INK2)
    d.text((W - PAD - 470, PAD + 26), "green = cast at real scale · red = M2 fixture", font=font(15), fill=INK2)
    d.line([PAD, PAD + 78, W - PAD, PAD + 78], fill=RULE, width=2)
    slots = [(PAD + (i % 2) * (TILE_W + GAP), PAD + 96 + (i // 2) * (TILE_H + CAP_H + GAP)) for i in range(n)]
    tile(s, *slots[0], os.path.join(BRIEF, refimg), "", refcap, "", ref=True)
    for (x, y), k in zip(slots[1:], cands):
        letter = k.split("-")[1]
        title, _, note = M3[k]["note"].partition(" — ")
        tile(s, x, y, os.path.join(HERE, f"SHOT-{k}-rough.png"), letter, title, note, lean=(LEANS[key] == letter))
    out = os.path.join(HERE, "sheets", f"{key}-sheet.jpg"); s.save(out, quality=88); print(" ", out)

if __name__ == "__main__":
    for a in SHEETS: sheet_for(*a)
