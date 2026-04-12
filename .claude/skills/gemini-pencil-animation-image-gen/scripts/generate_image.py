#!/usr/bin/env python3
"""
Gemini Pixel Art Image Generator
Calls the Gemini API directly to generate images and save them as PNGs.

Usage:
    python3 generate_image.py "A pixel art sprite of a robot" --output ./robot.png

Requires:
    pip install google-genai
    GEMINI_API_KEY set in environment or .env file
"""

import argparse
import base64
import os
import sys
from pathlib import Path


def load_api_key(env_file: str = ".env") -> str:
    """Load GEMINI_API_KEY from environment or .env file."""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key

    env_path = Path(env_file)
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("GEMINI_API_KEY="):
                    value = line.split("=", 1)[1].strip()
                    value = value.strip("'\"")
                    if value:
                        return value

    print("Error: GEMINI_API_KEY not found.", file=sys.stderr)
    print("Set it in your environment or add it to a .env file:", file=sys.stderr)
    print('  export GEMINI_API_KEY="your-key-here"', file=sys.stderr)
    print("  -- or --", file=sys.stderr)
    print('  echo \'GEMINI_API_KEY=your-key-here\' >> .env', file=sys.stderr)
    sys.exit(1)


def generate_image(
    prompt: str,
    output_path: str = "./generated.png",
    aspect_ratio: str = "1:1",
    model: str = "gemini-3.1-flash-image-preview",
    env_file: str = ".env",
    reference_images: list = None,
) -> str:
    """
    Generate an image using the Gemini API and save as PNG.

    Args:
        prompt: The image generation prompt
        output_path: Where to save the generated PNG
        aspect_ratio: Image aspect ratio (1:1, 16:9, 9:16, 3:2, 4:3, etc.)
        model: Gemini model name
        env_file: Path to .env file
        reference_images: List of file paths to reference images for identity locking

    Returns:
        The path to the saved image file
    """
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("Error: google-genai package not installed.", file=sys.stderr)
        print("Install it with: pip install google-genai", file=sys.stderr)
        sys.exit(1)

    api_key = load_api_key(env_file)
    client = genai.Client(api_key=api_key)

    print(f"Model: {model}")
    print(f"Aspect ratio: {aspect_ratio}")
    print(f"Output: {output_path}")
    if reference_images:
        print(f"Reference images: {', '.join(reference_images)}")
    print(f"Prompt: {prompt[:120]}{'...' if len(prompt) > 120 else ''}")
    print("Generating...")

    # Build contents list with optional reference images
    contents = []
    if reference_images:
        for ref_path in reference_images:
            ref_file = Path(ref_path)
            if not ref_file.exists():
                print(f"Error: Reference image not found: {ref_path}", file=sys.stderr)
                sys.exit(1)
            with open(ref_file, "rb") as f:
                img_bytes = f.read()
            # Detect mime type from extension
            ext = ref_file.suffix.lower()
            mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
            mime_type = mime_map.get(ext, "image/png")
            contents.append(types.Part.from_bytes(data=img_bytes, mime_type=mime_type))
            print(f"  Loaded reference: {ref_path} ({len(img_bytes) / 1024:.1f} KB)")
    contents.append(prompt)

    # Call the Gemini API
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
            ),
        ),
    )

    # Extract the image data
    image_bytes = None
    for part in response.candidates[0].content.parts:
        if part.inline_data and part.inline_data.mime_type.startswith("image/"):
            raw_data = part.inline_data.data

            # Handle both raw bytes and base64 string from SDK
            if isinstance(raw_data, bytes):
                image_bytes = raw_data
            elif isinstance(raw_data, str):
                image_bytes = base64.b64decode(raw_data)
            else:
                print(f"Error: Unexpected data type: {type(raw_data)}", file=sys.stderr)
                sys.exit(1)
            break

    if image_bytes is None:
        # Check if there's a text response explaining why
        for part in response.candidates[0].content.parts:
            if hasattr(part, "text") and part.text:
                print(f"Model returned text instead of image: {part.text}", file=sys.stderr)
        print("Error: No image found in the API response.", file=sys.stderr)
        print("Try rephrasing the prompt or adding 'Generate an image of...' prefix.", file=sys.stderr)
        sys.exit(1)

    # Validate raw image
    raw_size_kb = len(image_bytes) / 1024
    if len(image_bytes) < 100:
        print(f"Warning: Image data is only {len(image_bytes)} bytes — may be corrupt.", file=sys.stderr)
    if image_bytes[:4] == b'\x89PNG':
        fmt = "PNG"
    elif image_bytes[:2] == b'\xff\xd8':
        fmt = "JPEG"
    else:
        fmt = "Unknown"
        print(f"Warning: Unrecognized image format. First 20 bytes: {image_bytes[:20]}", file=sys.stderr)

    print(f"Received: {raw_size_kb:.1f} KB ({fmt})")

    # Save image
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with open(output, "wb") as f:
        f.write(image_bytes)

    final_size_kb = len(image_bytes) / 1024
    print(f"Saved: {output} ({final_size_kb:.1f} KB)")
    return str(output)


def main():
    parser = argparse.ArgumentParser(
        description="Generate pixel art images using the Gemini API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "A 16x32 pixel art character" --output character.png
  %(prog)s "A pixel sprite on hot pink #FF00FF background" -o sprite.png
        """,
    )

    parser.add_argument("prompt", help="The image generation prompt")
    parser.add_argument(
        "-o", "--output",
        default="./generated.png",
        help="Output file path (default: ./generated.png)",
    )
    parser.add_argument(
        "--aspect-ratio",
        default="1:1",
        choices=["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"],
        help="Image aspect ratio (default: 1:1)",
    )
    parser.add_argument(
        "--model",
        default="gemini-3.1-flash-image-preview",
        help="Gemini model name (default: gemini-3.1-flash-image-preview)",
    )
    parser.add_argument(
        "--env-file",
        default=".env",
        help="Path to .env file containing GEMINI_API_KEY (default: .env)",
    )
    parser.add_argument(
        "-r", "--reference",
        nargs="+",
        help="Reference image path(s) for identity locking",
    )

    args = parser.parse_args()
    generate_image(
        prompt=args.prompt,
        output_path=args.output,
        aspect_ratio=args.aspect_ratio,
        model=args.model,
        env_file=args.env_file,
        reference_images=args.reference,
    )


if __name__ == "__main__":
    main()
