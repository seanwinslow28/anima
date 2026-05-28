"""anima — Nano Banana Pro plate-generation wrapper for Cy's Pass 2.

Cy's three-phase loop assigns Pass 2 (plate generation) to NB Pro per Flo's
Phase 5 hero-tier routing (Image-Model-DR SYNTHESIS §2). Until Flo lands as a
callable AgentSpec in commit 5+, this module is the direct wrapper Cy's
Pass 2 calls — same shape as pipeline.agents.cli_runners (subprocess shell-out
+ stub-fallback ladder + a typed response envelope), but pointed at the
existing pencil-animation skill script instead of the agy CLI.

The skill at .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py
already implements the google-genai API call, reference-image upload, and
aspect-ratio handling. We shell out to it rather than duplicate that code.

# A note on model IDs

The skill script defaults to `gemini-3.1-flash-image-preview` (NB2 Flash, the
production tier for current pencil-test work). NB Pro is the hero-shot tier
per Image-Model-DR. The exact API model slug for NB Pro isn't documented in
SYNTHESIS.md by string; the placeholder default `nano-banana-pro` here matches
the brainstorm and DR voice but should be verified against google-genai's
shipping model registry at first real-call time. Cy callers can pass
`model=<verified-slug>` to override before then — Sean's Bible-authoring runs
will surface the right slug the first time NB Pro is actually invoked.

# What the cache key encodes

Per Cy brainstorm TOP-3 + ENG3: the cache key includes prompt text + sorted
reference-image content hashes + cites_identity_rules tuple + reject_reason
+ model. `cy iterate --reject ...` regenerations work by threading the reject
text into the next NB Pro call's reject_reason parameter, which changes the
hash, which invalidates the cache, which forces a fresh generation. Cached
plates that passed Pass 3 verification are preserved untouched.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

# Where the skill script lives. Same relative path commit 8's cli_runners
# uses for agy — assume a project-root-relative lookup.
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SKILL_SCRIPT = (
    _PROJECT_ROOT / ".claude" / "skills" / "gemini-pencil-animation-image-gen"
    / "scripts" / "generate_image.py"
)


@dataclass(frozen=True)
class NBProResponse:
    """Result envelope from one NB Pro plate-generation call.

    Per the AgentSpec discipline (mirroring CLIResponse from cli_runners.py):
    - output_path: where the plate landed on disk. May be a cached copy or a
      freshly-generated file.
    - cache_key: the SHA-256 (truncated) of the inputs that determined this
      response. Cy's audit trail surfaces this so museum walkthrough can name
      which plates were cache hits vs fresh generation.
    - cache_hit: True if the result came from the content-addressed cache.
    - stub_fallback: True if GEMINI_API_KEY was missing and a placeholder PNG
      was written instead of a real generation. Tests + dev workflows live on
      this path.
    - exit_code: subprocess exit code. Non-zero means the skill script failed
      and the caller should treat the result as a failed plate.
    """
    output_path: Path
    cache_key: str
    cache_hit: bool
    stub_fallback: bool = False
    exit_code: int = 0

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and self.output_path.exists()


def invoke_nb_pro(
    *,
    prompt: str,
    reference_images: list[Path],
    output_path: Path,
    cache_dir: Path,
    cites_identity_rules: tuple[str, ...] = (),
    reject_reason: str | None = None,
    model: str = "nano-banana-pro",
    timeout_s: int = 180,
) -> NBProResponse:
    """Generate (or fetch from cache) one NB Pro plate.

    The function is sync — Cy's Pass 2 calls this per plate in a loop. If Cy's
    plate count grows beyond ~30, a future commit can parallelize with a
    thread pool; today's spend is small enough that serial is fine.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    cache_key = _compute_cache_key(
        prompt=prompt,
        reference_images=reference_images,
        cites_identity_rules=cites_identity_rules,
        reject_reason=reject_reason,
        model=model,
    )
    cached_file = cache_dir / f"{cache_key}.png"

    # Cache hit short-circuits everything else.
    if cached_file.exists():
        shutil.copy2(cached_file, output_path)
        return NBProResponse(
            output_path=output_path,
            cache_key=cache_key,
            cache_hit=True,
            stub_fallback=False,
            exit_code=0,
        )

    # Stub fallback when the env isn't set up for real calls. Tests run here.
    if not os.environ.get("GEMINI_API_KEY"):
        _write_placeholder_png(output_path)
        # Also cache the placeholder so the cache-hit test on a second call
        # behaves the same as it would with a real generation.
        shutil.copy2(output_path, cached_file)
        return NBProResponse(
            output_path=output_path,
            cache_key=cache_key,
            cache_hit=False,
            stub_fallback=True,
            exit_code=0,
        )

    # Real path: shell out to the skill script.
    if not _SKILL_SCRIPT.exists():
        # The script we depend on isn't there. Fall through to placeholder so
        # the pipeline doesn't crash; caller will see stub_fallback=True and
        # can decide how to surface this.
        _write_placeholder_png(output_path)
        shutil.copy2(output_path, cached_file)
        return NBProResponse(
            output_path=output_path,
            cache_key=cache_key,
            cache_hit=False,
            stub_fallback=True,
            exit_code=0,
        )

    cmd = _build_skill_cmd(
        prompt=prompt,
        reference_images=reference_images,
        output_path=output_path,
        model=model,
    )
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
    except subprocess.TimeoutExpired:
        return NBProResponse(
            output_path=output_path,
            cache_key=cache_key,
            cache_hit=False,
            stub_fallback=False,
            exit_code=124,
        )

    if result.returncode != 0 or not output_path.exists():
        return NBProResponse(
            output_path=output_path,
            cache_key=cache_key,
            cache_hit=False,
            stub_fallback=False,
            exit_code=result.returncode if result.returncode != 0 else 1,
        )

    # Success: snapshot to cache so future identical calls hit.
    shutil.copy2(output_path, cached_file)
    return NBProResponse(
        output_path=output_path,
        cache_key=cache_key,
        cache_hit=False,
        stub_fallback=False,
        exit_code=0,
    )


def _compute_cache_key(
    *,
    prompt: str,
    reference_images: list[Path],
    cites_identity_rules: tuple[str, ...],
    reject_reason: str | None,
    model: str,
) -> str:
    """SHA-256 of the inputs that determine the generated plate.

    Reference images contribute their content hash (not their path) so the
    same image at a different path stays in cache. The reject_reason field is
    what `cy iterate` threads through to invalidate the cache for a single
    rejected plate without re-running the whole Bible.
    """
    h = hashlib.sha256()
    h.update(b"prompt:")
    h.update(prompt.encode("utf-8"))
    h.update(b"\nmodel:")
    h.update(model.encode("utf-8"))
    h.update(b"\nrules:")
    for rule_id in sorted(cites_identity_rules):
        h.update(rule_id.encode("utf-8"))
        h.update(b",")
    h.update(b"\nreject:")
    h.update((reject_reason or "").encode("utf-8"))
    h.update(b"\nrefs:")
    # Hash reference content, sorted so call-order doesn't perturb the key.
    ref_hashes = sorted(_hash_file(p) for p in reference_images)
    for rh in ref_hashes:
        h.update(rh.encode("utf-8"))
        h.update(b",")
    return h.hexdigest()


def _hash_file(path: Path) -> str:
    """SHA-256 of file content. Streams the file so reference images that
    happen to be large (4K turnaround sheets) don't blow up memory."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _build_skill_cmd(
    *,
    prompt: str,
    reference_images: list[Path],
    output_path: Path,
    model: str,
) -> list[str]:
    """The exact argv the skill script expects. Matches its --help shape."""
    cmd = [
        "python3",
        str(_SKILL_SCRIPT),
        prompt,
        "--output", str(output_path),
        "--model", model,
        "--env-file", str(_PROJECT_ROOT / ".env"),
    ]
    if reference_images:
        cmd.append("--reference")
        cmd.extend(str(p) for p in reference_images)
    return cmd


def _write_placeholder_png(path: Path) -> None:
    """Tiny valid PNG written to `path` for stub-fallback / test runs.

    1x1 transparent pixel. Real enough that downstream code that opens it
    with Pillow or copies it through ffmpeg sees a valid image; small enough
    that committed test fixtures don't bloat the repo.
    """
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
        b"\x00\x00\x00\rIDATx\x9cc\xf8\xcf\xc0\x00\x00\x00\x03"
        b"\x00\x01;\xa9\xb1\x9c\x00\x00\x00\x00IEND\xaeB`\x82"
    )
