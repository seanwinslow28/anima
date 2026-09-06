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
SHOTS = [
    ("frame", L+"10_beat5_S12_claude-canyon.mp4", 6.4, 0.45, "11 · record scratch — route A freeze-cut (placeholder until Q2)"),
    ("frame", L+"11_beat6_S13_codex-screen-pop.mp4", 2.9, 0.45, "11 · record scratch — route A freeze-cut"),
    ("frame", L+"12_beat7_S14_gemini-whirlwind.mp4", 1.2, 0.45, "11 · record scratch — route A freeze-cut"),
    ("frame", L+"13_beat8_S06B_grok-demolition.mp4", 1.8, 0.85, "11 · record scratch — route A freeze-cut"),
    ("clip", M+"m3-beat12/S10-sean-swivel-v1.mp4", 0.5, 5.8, "12 · THE SWIVEL (protected)"),
    ("clip", M+"m3-beat13/S02-sean-types-v1.mp4", 0.5, 2.2, "13 · he types"),
    ("clip", M+"m3-beat13/S11-chat-typewriter-v1.mp4", 0.0, 4.7, "13 · the question (post typewriter)"),
    ("clip", M+"m3-beat14/S08-replay-cursor-v1.mp4", 0.0, 6.0, "14 · THE REPLAY (post cursor)"),
    ("clip", M+"m3-beat15/S03-claude-sigh-v1.mp4", 3.0, 0.9, "15 · the sigh — Claude"),
    ("clip", M+"m3-beat15/S04-codex-sigh-v1.mp4", 2.0, 0.9, "15 · the sigh — Codex"),
    ("clip", M+"m3-beat15/S05-gemini-sigh-v1.mp4", 2.8, 0.9, "15 · the sigh — Gemini"),
    ("clip", M+"m3-beat15/S06B-grok-sigh-v1.mp4", 2.2, 1.0, "15 · the sigh — Grok"),
    ("clip", M+"m3-beat16/S03-claude-pitstop-v1.mp4", 0.0, 1.3, "16 · PIT STOP — Claude: one line"),
    ("clip", M+"m3-beat16/S04-codex-pitstop-v1.mp4", 0.0, 1.3, "16 · PIT STOP — Codex: one line"),
    ("clip", M+"m3-beat16/S05-gemini-pitstop-v1.mp4", 0.0, 1.3, "16 · PIT STOP — Gemini: make it pretty"),
    ("clip", M+"m3-beat15/S06B-grok-sigh-v1.mp4", 5.3, 1.0, "16 · PIT STOP — Grok: PLACEHOLDER (old button held for Q3)"),
    ("clip", M+"m3-beat17/S08-graph-rockets-v1.mp4", 1.0, 2.0, "17 · the graph rockets"),
    ("clip", M+"m3-beat17/S02-earned-ship-it-v1.mp4", 0.2, 2.2, "17 · the earned SHIP IT"),
    ("clip", M+"m3-beat18/S08-user-colorizes-v1.mp4", 0.8, 4.0, "18 · the USER colorizes"),
    ("still", "refs/user-looktest/S08-green-v2.png", 4.0, "19 · THE BUTTON (VO runs here)"),
    ("still", N+"S08-alarm3-v1.png", 0.4, "20 · the sting"),
    ("red", N+"S08-alarm3-v1.png", 0.15, ""),
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
    print(f"{out}  {len(SHOTS)} segments, {total:.1f}s (beat sheet target ~37s)")

if __name__ == "__main__":
    main()
