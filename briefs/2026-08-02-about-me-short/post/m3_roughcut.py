#!/usr/bin/env python3
"""
M3 ROUGH CUT — beats 11–20 assembled at the beat sheet's timings from the wave-3 material, so
Sean can judge the movement as a movement rather than as fourteen sheets. $0, deterministic.

Every clip is handed to the cut with its 7s intact elsewhere (motion/m3-beat*/); this file only
TRIMS. The trims are a first guess at the beat sheet's durations (beats-v1.md § Movement 3) and
exist to be argued with. Placeholders are labelled ON the picture: beat 11 plays route A (the
$0 freeze-cut) until Q2 is ruled; Grok's pit stop plays his sigh's tail until Q3 is ruled.

    Usage:  m3_roughcut.py <out.mp4>
"""
import os, subprocess, sys, tempfile

FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
W, H, FPS = 1280, 720, 24
L = "_LOCKED-M2/"; M = "motion/"; N = "normalised/"

# kind: clip (src, in, dur) | still (src, dur) | frame (src, t, dur) — a single frame held
# ── WAVE 3b running order (2026-09-06 PM): 9 → 10 → 10.5 → 11/12 (S15, PLACEHOLDER until Sean picks A/B) → 12 (S10, cut BEFORE the
#    eyes open) → 13.1 → 13.2 → 13.3 → 14 → 15 (four RELIEF sighs) → 16 (delegation, 10s) → 16.5 ×4 (+ Grok) → 17 (SHIP key) → 18 → 18.5 → 19 → 20.
#    Every trim is a first guess for Sean to argue with. SHIP = the single-image v2 if it landed, else the 2kf v1 (cut before the morph).
import os as _os
_SHIP = M+"m3-beat17/S18-ship-key-v2-single.mp4" if _os.path.exists(M+"m3-beat17/S18-ship-key-v2-single.mp4") else M+"m3-beat17/S18-ship-key-v1.mp4"
_WIDE = M+"m3-beat11/S15-wide-chaos-v1.mp4"
_WIDE_SHOTS = ([("clip", _WIDE, 0.3, 3.2, "11/12 · THE WIDE (S15-A): the chaos, the swivel"),
                ("frame", _WIDE, 3.5, 1.2, "11/12 · THE FREEZE (record scratch; frame = a first guess, Sean picks)")]
               if _os.path.exists(_WIDE) else
               [("frame", L+"10_beat5_S12_claude-canyon.mp4", 6.4, 0.45, "11/12 · THE WIDE — PLACEHOLDER"),
                ("frame", L+"11_beat6_S13_codex-screen-pop.mp4", 2.9, 0.45, "11/12 · THE WIDE — placeholder"),
                ("frame", L+"12_beat7_S14_gemini-whirlwind.mp4", 1.2, 0.45, "11/12 · THE WIDE — placeholder"),
                ("frame", L+"13_beat8_S06B_grok-demolition.mp4", 1.8, 0.65, "11/12 · THE WIDE — placeholder")])
_DELEG = M+"m3-beat16/S02-sean-delegation-v2-mime.mp4"   # Sean's 17:55 re-roll (v2, the calm still); v2b beside it
SHOTS = [
    ("clip", "_LOCKED-M3/16_beat10.5_S19_sean-notices.mp4", 1.6, 2.6, "10.5 · Sean alone notices (locked)"),
] + _WIDE_SHOTS + [
    ("clip", "_LOCKED-M3/18_beat12_S10_the-swivel.mp4", 0.5, 5.4, "12 · THE SWIVEL (locked; ends before the eyes open)"),
    ("clip", M+"m3-beat13/S16-sean-eyes-open-v1.mp4", 1.2, 3.6, "13.1 · turns back, eyes open on us (S16)"),
    ("clip", M+"m3-beat13/S17-hands-v1.mp4", 0.0, 2.4, "13.2 · the hands (S17)"),
    ("clip", "_LOCKED-M3/21_beat13.3_S11_chat-typewriter.mp4", 0.0, 4.7, "13.3 · THE QUESTION (locked; Sean crops in CapCut)"),
    ("clip", "_LOCKED-M3/22_beat14_S08_replay-cursor.mp4", 0.0, 6.0, "14 · THE REPLAY (locked)"),
    ("clip", M+"m3-beat15/S03-claude-relief-v2.mp4", 0.9, 1.1, "15 · RELIEF — Claude"),
    ("clip", M+"m3-beat15/S04-codex-relief-v2.mp4", 0.9, 1.1, "15 · RELIEF — Codex"),
    ("clip", M+"m3-beat15/S05-gemini-relief-v2.mp4", 0.9, 1.1, "15 · RELIEF — Gemini"),
    ("clip", M+"m3-beat15/S06B-grok-relief-v2.mp4", 0.9, 1.2, "15 · RELIEF — Grok"),
    ("clip", _DELEG, 0.6, 7.4, "16 · THE DELEGATION v2 mime (10s roll, trimmed)"),
    ("clip", "_LOCKED-M3/28_beat16.5_S03_claude-pitstop.mp4", 0.0, 1.3, "16.5 · PIT STOP — Claude (locked)"),
    ("clip", "_LOCKED-M3/29_beat16.5_S04_codex-pitstop.mp4", 0.0, 1.3, "16.5 · PIT STOP — Codex (locked)"),
    ("clip", "_LOCKED-M3/30_beat16.5_S05_gemini-pitstop.mp4", 0.0, 1.3, "16.5 · PIT STOP — Gemini (locked)"),
    ("clip", M+"m3-beat16/S06B-grok-pitstop-v1.mp4", 0.4, 1.4, "16.5 · PIT STOP — Grok: the BUY button"),
    ("clip", _SHIP, 1.4, 2.0, "17 · THE SHIP KEY (S18)"),
    ("clip", "_LOCKED-M3/33_beat18_S08_user-colorizes.mp4", 0.8, 4.0, "18 · the USER colorizes (locked)"),
    ("clip", M+"m3-beat18h/S09-team-celebrates-v1.mp4", 0.3, 3.2, "18.5 · THE CELEBRATION (S09 state C)"),
    ("still", "_LOCKED-M3/35_beat19_S08_the-button-hold.png", 4.0, "19 · THE BUTTON (VO runs here; locked)"),
    ("clip", M+"m3-beat20/S08-sting-transition-v1.mp4", 0.9, 1.3, "20 · the sting — flash + shake → ANOTHER PROBLEM!"),
    ("red", N+"S08-alarm4-v1.png", 0.15, ""),
    ("black", None, 1.0, ""),
]

def label_png(tmp, i, text):
    """This ffmpeg has no drawtext; burn the label with PIL and overlay it."""
    from PIL import Image, ImageDraw, ImageFont
    if not text: return None
    try: f = ImageFont.truetype(FONT, 22)
    except Exception: f = ImageFont.load_default()
    im = Image.new("RGBA", (W, 44), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    w = d.textlength(text, font=f); d.rectangle([0, 0, w + 24, 40], fill=(0, 0, 0, 140)); d.text((12, 8), text, fill=(255, 255, 255, 255), font=f)
    p = os.path.join(tmp, f"lab{i:02d}.png"); im.save(p); return p

def seg(i, tmp, s):
    out = os.path.join(tmp, f"seg{i:02d}.mp4")
    base = f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={FPS}"
    kind = s[0]; lab = None
    if kind == "clip":
        _, src, t0, dur, lab = s
        cmd = ["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t0:.2f}", "-t", f"{dur:.2f}", "-i", src]
    elif kind == "frame":
        _, src, t, dur, lab = s
        png = os.path.join(tmp, f"fr{i:02d}.png")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1", png], check=True)
        cmd = ["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-t", f"{dur:.2f}", "-i", png]
    elif kind == "still":
        _, src, dur, lab = s
        cmd = ["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-t", f"{dur:.2f}", "-i", src]
    if kind in ("clip", "frame", "still"):
        lp = label_png(tmp, i, lab)
        if lp: cmd += ["-loop", "1", "-i", lp, "-filter_complex", f"[0:v]{base}[v];[v][1:v]overlay=16:16:shortest=1"]
        else: cmd += ["-vf", base]
    elif kind == "red":
        _, src, dur, _ = s
        cmd = ["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-t", f"{dur:.2f}", "-i", src, "-vf", base + ",drawbox=c=red@0.5:t=fill"]
    else:  # black
        _, _, dur, _ = s
        cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-t", f"{dur:.2f}", "-i", f"color=black:s={W}x{H}:r={FPS}", "-vf", "setsar=1"]
    cmd += ["-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-r", str(FPS), out]
    subprocess.run(cmd, check=True)
    return out

def main():
    out = sys.argv[1]; tmp = tempfile.mkdtemp()
    segs = [seg(i, tmp, s) for i, s in enumerate(SHOTS)]
    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in segs))
    for p_ in segs:
        d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p_], capture_output=True, text=True).stdout.strip()
        print(f"  {os.path.basename(p_)}  {d}s")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-r", str(FPS), out], check=True)
    total = sum(s[3] if s[0] in ("clip", "frame") else s[2] for s in SHOTS)
    print(f"{out}  {len(SHOTS)} segments, {total:.1f}s (beat sheet target ~37s; M1 15s + M2 35s + this = {50+total:.1f}s of the 2:00 ceiling)")

if __name__ == "__main__":
    main()
