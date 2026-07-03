#!/usr/bin/env python3
"""
OpenAI Universal Image Generator
Calls the OpenAI Image API (gpt-image-2) to generate images and save them as PNGs.

Usage:
    python3 generate_image.py "Editorial illustration of a typewriter" --output ./typewriter.png
    python3 generate_image.py "Substack header in Ralph Steadman style" \
      --output ./header.png --aspect-ratio 16:9 --reference ./steadman.png --quality high

Requires:
    python3 -m pip install openai
    OPENAI_API_KEY set in environment or .env file
"""

import argparse
import base64
import os
import sys
from pathlib import Path


# Friendly aspect ratio → OpenAI size string.
# All sizes are divisible by 16, max edge ≤ 3840, aspect ratio ≤ 3:1.
ASPECT_RATIO_TO_SIZE = {
    "1:1": "1024x1024",
    "3:2": "1536x1024",
    "2:3": "1024x1536",
    "4:3": "1408x1056",
    "3:4": "1056x1408",
    "16:9": "1536x864",
    "9:16": "864x1536",
    "21:9": "1792x768",
    "4:5": "1024x1280",
    "5:4": "1280x1024",
}

# Preset sizes universally accepted by the edit endpoint.
EDIT_ENDPOINT_PRESETS = {"1024x1024", "1536x1024", "1024x1536", "256x256", "512x512", "auto"}


def load_api_key(env_file: str = ".env") -> str:
    """Load OPENAI_API_KEY from environment or .env file."""
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key

    env_path = Path(env_file)
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("OPENAI_API_KEY="):
                    value = line.split("=", 1)[1].strip()
                    value = value.strip("'\"")
                    if value:
                        return value

    print("Error: OPENAI_API_KEY not found.", file=sys.stderr)
    print("Set it in your environment or add it to a .env file:", file=sys.stderr)
    print('  export OPENAI_API_KEY="your-key-here"', file=sys.stderr)
    print("  -- or --", file=sys.stderr)
    print('  echo \'OPENAI_API_KEY=your-key-here\' >> .env', file=sys.stderr)
    sys.exit(1)


def map_aspect_ratio(aspect_ratio: str, endpoint: str = "generate") -> str:
    """
    Map a friendly aspect ratio (e.g. "16:9") to an OpenAI size string.
    For the edit endpoint, fall back to the closest preset when the custom
    size isn't in the universally-accepted set.
    """
    size = ASPECT_RATIO_TO_SIZE.get(aspect_ratio, aspect_ratio)

    if endpoint != "edit":
        return size

    if size in EDIT_ENDPOINT_PRESETS:
        return size

    # Edit endpoint fallback: pick the preset with the closest aspect ratio.
    try:
        w, h = (int(x) for x in size.split("x"))
        target_ratio = w / h
    except (ValueError, ZeroDivisionError):
        return "1024x1024"

    presets = [
        ("1536x1024", 1536 / 1024),  # 3:2 landscape
        ("1024x1024", 1.0),           # 1:1 square
        ("1024x1536", 1024 / 1536),  # 2:3 portrait
    ]
    best = min(presets, key=lambda p: abs(p[1] - target_ratio))
    return best[0]


def generate_image(
    prompt: str,
    output_path: str = "./generated.png",
    aspect_ratio: str = "1:1",
    model: str = "gpt-image-2",
    quality: str = "medium",
    n: int = 1,
    env_file: str = ".env",
    reference_images: list = None,
    moderation: str = "auto",
) -> str:
    """
    Generate an image using the OpenAI Image API and save as PNG.

    Args:
        prompt: The image generation prompt
        output_path: Where to save the generated PNG
        aspect_ratio: Friendly aspect ratio (1:1, 16:9, etc.)
        model: OpenAI image model ID
        quality: low / medium / high / auto
        n: Number of variants to generate
        env_file: Path to .env file
        reference_images: List of file paths to reference images for style transfer

    Returns:
        The path to the saved image file (first variant when n > 1)
    """
    try:
        from openai import OpenAI
        from openai import APIError, BadRequestError, RateLimitError
    except ImportError:
        print("Error: openai package not installed.", file=sys.stderr)
        print("Install it with: python3 -m pip install openai", file=sys.stderr)
        sys.exit(1)

    api_key = load_api_key(env_file)
    client = OpenAI(api_key=api_key)

    using_edit = bool(reference_images)
    endpoint = "edit" if using_edit else "generate"
    size = map_aspect_ratio(aspect_ratio, endpoint=endpoint)

    print(f"Model: {model}")
    print(f"Endpoint: images.{endpoint}")
    print(f"Aspect ratio: {aspect_ratio} → {size}")
    print(f"Quality: {quality}")
    print(f"Variants: {n}")
    print(f"Output: {output_path}")
    if reference_images:
        print(f"Reference images: {', '.join(reference_images)}")
    print(f"Prompt: {prompt[:120]}{'...' if len(prompt) > 120 else ''}")
    print("Generating...")

    try:
        if using_edit:
            ref_files = []
            for ref_path in reference_images:
                ref_file = Path(ref_path)
                if not ref_file.exists():
                    print(f"Error: Reference image not found: {ref_path}", file=sys.stderr)
                    sys.exit(1)
                size_mb = ref_file.stat().st_size / (1024 * 1024)
                if size_mb > 50:
                    print(f"Error: Reference {ref_path} is {size_mb:.1f}MB — exceeds 50MB API limit.", file=sys.stderr)
                    sys.exit(1)
                ref_files.append(open(ref_file, "rb"))
                print(f"  Loaded reference: {ref_path} ({size_mb * 1024:.1f} KB)")

            # input_fidelity is supported on gpt-image-1.5 but not gpt-image-2 (verified 2026-05-23).
            # Pass it only for models documented to accept it.
            edit_kwargs = dict(
                model=model,
                image=ref_files[0] if len(ref_files) == 1 else ref_files,
                prompt=prompt,
                size=size,
                quality=quality,
                n=n,
            )
            # The Python SDK's images.edit() signature omits `moderation` (it's documented
            # for the API but not surfaced in SDK 2.38.0). Pass it through `extra_body`.
            if moderation and moderation != "auto":
                edit_kwargs["extra_body"] = {"moderation": moderation}
            if model.startswith("gpt-image-1"):
                edit_kwargs["input_fidelity"] = "high"
            try:
                response = client.images.edit(**edit_kwargs)
            finally:
                for fh in ref_files:
                    fh.close()
        else:
            gen_kwargs = dict(
                model=model,
                prompt=prompt,
                size=size,
                quality=quality,
                n=n,
            )
            if moderation and moderation != "auto":
                gen_kwargs["moderation"] = moderation
            response = client.images.generate(**gen_kwargs)
    except BadRequestError as e:
        msg = str(e)
        print(f"Error: 400 Bad Request — {msg}", file=sys.stderr)
        if "content_policy" in msg.lower() or "safety" in msg.lower():
            print("  → Prompt was blocked by the safety filter.", file=sys.stderr)
            print("  → Rephrase, remove flagged terms, or contact OpenAI for legitimate-use exceptions.", file=sys.stderr)
        elif "size" in msg.lower():
            print("  → Size constraint failure — try a different --aspect-ratio.", file=sys.stderr)
        sys.exit(1)
    except RateLimitError as e:
        print(f"Error: 429 Rate Limit — {e}", file=sys.stderr)
        print("  → Wait 30 seconds and retry. Reduce --n if running variants.", file=sys.stderr)
        sys.exit(1)
    except APIError as e:
        print(f"Error: OpenAI API error — {e}", file=sys.stderr)
        sys.exit(1)

    # Save each variant.
    output_base = Path(output_path)
    output_base.parent.mkdir(parents=True, exist_ok=True)
    saved_paths = []

    for idx, item in enumerate(response.data or []):
        b64 = item.b64_json
        if not b64:
            # Fallback path if API returned a URL instead.
            if item.url:
                print(f"  Variant {idx + 1}: URL response (download manually): {item.url}", file=sys.stderr)
                continue
            print(f"Error: Variant {idx + 1} returned no image data.", file=sys.stderr)
            continue

        try:
            image_bytes = base64.b64decode(b64)
        except (ValueError, TypeError) as decode_err:
            print(f"Error: Could not decode base64 for variant {idx + 1}: {decode_err}", file=sys.stderr)
            continue

        if idx == 0:
            out_path = output_base
        else:
            stem = output_base.stem
            suffix = output_base.suffix or ".png"
            out_path = output_base.with_name(f"{stem}-v{idx + 1}{suffix}")

        with open(out_path, "wb") as f:
            f.write(image_bytes)

        size_kb = len(image_bytes) / 1024
        print(f"Saved: {out_path} ({size_kb:.1f} KB)")
        saved_paths.append(str(out_path))

        revised = getattr(item, "revised_prompt", None)
        if revised:
            preview = revised[:200] + ("..." if len(revised) > 200 else "")
            print(f"  Revised prompt (auto-rewrite): {preview}")

    if not saved_paths:
        print("Error: No images saved.", file=sys.stderr)
        sys.exit(1)

    return saved_paths[0]


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using the OpenAI GPT Image 2 API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "A photo of a vintage typewriter on oak" --output typewriter.png
  %(prog)s "Editorial illustration in Steadman style" -o header.png \\
      --aspect-ratio 16:9 --reference steadman-ref.png --quality high
  %(prog)s "Concept art of a forest spirit" -o concept.png --quality high --n 4
        """,
    )

    parser.add_argument("prompt", help="The image generation prompt")
    parser.add_argument(
        "-o", "--output",
        default="./generated.png",
        help="Output file path (default: ./generated.png). For n>1, variants land at <stem>-v2.png, etc.",
    )
    parser.add_argument(
        "--aspect-ratio",
        default="1:1",
        choices=list(ASPECT_RATIO_TO_SIZE.keys()),
        help="Image aspect ratio (default: 1:1). Maps to OpenAI size strings.",
    )
    parser.add_argument(
        "--model",
        default="gpt-image-2",
        help="OpenAI image model ID (default: gpt-image-2)",
    )
    parser.add_argument(
        "--quality",
        default="medium",
        choices=["low", "medium", "high", "auto"],
        help="Quality tier (default: medium). Use 'high' for in-image text and fine detail.",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=1,
        choices=range(1, 11),
        metavar="{1..10}",
        help="Number of variants to generate (default: 1)",
    )
    parser.add_argument(
        "--env-file",
        default=".env",
        help="Path to .env file containing OPENAI_API_KEY (default: .env)",
    )
    parser.add_argument(
        "-r", "--reference",
        nargs="+",
        help="Reference image path(s) — routes to images.edit with input_fidelity=high for style transfer",
    )
    parser.add_argument(
        "--moderation",
        default="auto",
        choices=["auto", "low"],
        help="Safety filter strictness (default: auto). Use 'low' for legitimate editorial work that auto blocks.",
    )

    args = parser.parse_args()
    generate_image(
        prompt=args.prompt,
        output_path=args.output,
        aspect_ratio=args.aspect_ratio,
        model=args.model,
        quality=args.quality,
        n=args.n,
        env_file=args.env_file,
        reference_images=args.reference,
        moderation=args.moderation,
    )


if __name__ == "__main__":
    main()
