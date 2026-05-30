import os
from PIL import Image

def analyze_all():
    files = sorted([f for f in os.listdir('.') if f.endswith('.png')])
    for f in files:
        try:
            img = Image.open(f)
            # count unique colors (limit to 10000)
            colors = img.getcolors(maxcolors=2000000)
            unique_count = len(colors) if colors else "More than 2M"
            print(f"File: {f}")
            print(f"  Format: {img.format}")
            print(f"  Size: {img.size}")
            print(f"  Mode: {img.mode}")
            print(f"  Unique colors: {unique_count}")
        except Exception as e:
            print(f"File: {f} - Error: {e}")

if __name__ == '__main__':
    analyze_all()
