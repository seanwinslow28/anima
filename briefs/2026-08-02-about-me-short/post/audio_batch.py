#!/usr/bin/env python3
"""
AUDIO BATCH — generate the film's music and SFX from the prompt sheets, three transports, one cue file.

  eleven-sfx    ElevenLabs Sound Effects   POST /v1/sound-generation     (AUDIO-PROMPTS-v1.md § SOUND EFFECTS)
  eleven-music  ElevenLabs Music           POST /v1/music                (AUDIO-PROMPTS-v1.md § MUSIC)
  lyria         Google Lyria 3.5 / 3 Clip  client.interactions.create   (LYRIA-PROMPTS-2026-09-13.md)

Cues live in post/audio_cues.yaml. Every output is written next to a .txt sidecar carrying the exact prompt +
parameters, and a manifest line is appended to audio/_log.jsonl. Re-running skips cues whose output exists
(pass --force to regenerate; each run writes -tN so nothing is overwritten).

  Keys: ELEVENLABS_API_KEY and GEMINI_API_KEY from the repo .env (or the environment).
  Cost: ElevenLabs SFX/Music bill characters against the subscription; Lyria 3.5 ≈ $0.08/gen, Clip Preview ≈ $0.04.

    Usage:  audio_batch.py [--transport eleven-sfx|eleven-music|lyria|all] [--only ID[,ID]] [--takes N]
                           [--dry-run] [--force] [--lyria-model lyria-3.5|lyria-3-clip-preview]
"""
import argparse, base64, json, os, sys, time, datetime, pathlib
import yaml

HERE = pathlib.Path(__file__).resolve().parent
BRIEF = HERE.parent
REPO = BRIEF.parent.parent
CUES = HERE / "audio_cues.yaml"
OUT = BRIEF / "audio"
LOG = OUT / "_log.jsonl"

def load_env():
    p = REPO / ".env"
    if p.exists():
        for line in p.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

def next_path(d, stem, ext):
    d.mkdir(parents=True, exist_ok=True)
    n = 1
    while (d / f"{stem}-t{n}{ext}").exists(): n += 1
    return d / f"{stem}-t{n}{ext}"

def log(rec):
    rec["at"] = datetime.datetime.now().isoformat(timespec="seconds")
    with open(LOG, "a") as f: f.write(json.dumps(rec) + "\n")

def sidecar(path, cue, params):
    path.with_suffix(".txt").write_text(f"{cue['id']} · {cue.get('name','')}\n\n{cue['prompt']}\n\nparams: {json.dumps(params)}\n")

# ── ElevenLabs ─────────────────────────────────────────────────────────────────────────────────────────────────
def eleven(path, payload, key):
    import requests
    r = requests.post(f"https://api.elevenlabs.io/v1/{path}?output_format=mp3_44100_128",
                      headers={"xi-api-key": key, "Content-Type": "application/json"}, json=payload, timeout=600)
    if r.status_code != 200:
        raise RuntimeError(f"{path} {r.status_code}: {r.text[:300]}")
    return r.content

def run_eleven_sfx(cue, take, args, key):
    payload = {"text": cue["prompt"], "model_id": "eleven_text_to_sound_v2"}
    if cue.get("seconds"): payload["duration_seconds"] = float(cue["seconds"])
    if cue.get("influence") is not None: payload["prompt_influence"] = float(cue["influence"])
    if cue.get("loop"): payload["loop"] = True
    out = next_path(OUT / "SFX" / "eleven", cue["id"], ".mp3")
    if args.dry_run: print(f"  DRY {out.name}  {json.dumps(payload)[:120]}"); return
    out.write_bytes(eleven("sound-generation", payload, key)); sidecar(out, cue, payload)
    log({"transport": "eleven-sfx", "id": cue["id"], "file": str(out.relative_to(BRIEF)), "params": payload})
    print(f"  ✓ {out.relative_to(BRIEF)}")

def run_eleven_music(cue, take, args, key):
    payload = {"prompt": cue["prompt"], "force_instrumental": True}
    if cue.get("seconds"): payload["music_length_ms"] = int(float(cue["seconds"]) * 1000)
    if args.music_model: payload["model_id"] = args.music_model
    out = next_path(OUT / "Music" / "eleven", cue["id"], ".mp3")
    if args.dry_run: print(f"  DRY {out.name}  {json.dumps(payload)[:120]}"); return
    out.write_bytes(eleven("music", payload, key)); sidecar(out, cue, payload)
    log({"transport": "eleven-music", "id": cue["id"], "file": str(out.relative_to(BRIEF)), "params": payload})
    print(f"  ✓ {out.relative_to(BRIEF)}")

# ── Lyria ──────────────────────────────────────────────────────────────────────────────────────────────────────
def run_lyria(cue, take, args, key):
    from google import genai
    client = genai.Client(api_key=key)
    model = args.lyria_model
    inp = [{"type": "text", "text": cue["prompt"]}]
    for img in cue.get("images", []) or []:
        p = BRIEF / img
        mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
        inp.append({"type": "image", "mime_type": mime, "data": base64.b64encode(p.read_bytes()).decode()})
    params = {"model": model, "images": cue.get("images", [])}
    out = next_path(OUT / "Music" / "lyria", f"{cue['id']}-{model.replace('.', '')}", ".mp3")
    if args.dry_run: print(f"  DRY {out.name}  {model}  {cue['prompt'][:80]}…"); return
    t0 = time.time()
    it = client.interactions.create(model=model, input=inp if len(inp) > 1 else cue["prompt"])
    audio = getattr(it, "output_audio", None)
    if not audio or not getattr(audio, "data", None):
        raise RuntimeError(f"no audio in response: {str(it)[:300]}")
    out.write_bytes(base64.b64decode(audio.data)); sidecar(out, cue, params)
    txt = getattr(it, "output_text", None)
    if txt: out.with_suffix(".plan.txt").write_text(str(txt))
    log({"transport": "lyria", "id": cue["id"], "file": str(out.relative_to(BRIEF)), "params": params, "secs": round(time.time() - t0, 1)})
    print(f"  ✓ {out.relative_to(BRIEF)}  ({time.time() - t0:.0f}s)")

RUNNERS = {"eleven-sfx": run_eleven_sfx, "eleven-music": run_eleven_music, "lyria": run_lyria}
KEYS = {"eleven-sfx": "ELEVENLABS_API_KEY", "eleven-music": "ELEVENLABS_API_KEY", "lyria": "GEMINI_API_KEY"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transport", default="all")
    ap.add_argument("--only", default="")
    ap.add_argument("--takes", type=int, default=1)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--lyria-model", default="lyria-3.5")
    ap.add_argument("--music-model", default="")
    args = ap.parse_args()
    load_env()
    cues = yaml.safe_load(CUES.read_text())
    only = {s.strip() for s in args.only.split(",") if s.strip()}
    transports = list(RUNNERS) if args.transport == "all" else [args.transport]
    for tr in transports:
        rows = [c for c in cues.get(tr, []) if not only or c["id"] in only]
        if not rows: continue
        key = os.environ.get(KEYS[tr], "")
        print(f"\n== {tr}: {len(rows)} cues × {args.takes} take(s)" + ("" if key or args.dry_run else f"   [SKIP — {KEYS[tr]} not set]"))
        if not key and not args.dry_run: continue
        for c in rows:
            existing = list((OUT / ("SFX" if tr == "eleven-sfx" else "Music") / tr.split("-")[0]).glob(f"{c['id']}-*.mp3")) if not tr == "lyria" else list((OUT / "Music" / "lyria").glob(f"{c['id']}-*.mp3"))
            if existing and not args.force and not args.dry_run:
                print(f"  · {c['id']} exists ({len(existing)}), skip (--force to add takes)"); continue
            print(f"  {c['id']} · {c.get('name','')}")
            for t in range(args.takes):
                try: RUNNERS[tr](c, t, args, key)
                except Exception as e:
                    print(f"  ✗ {c['id']}: {e}"); log({"transport": tr, "id": c["id"], "error": str(e)[:300]})

if __name__ == "__main__":
    main()
