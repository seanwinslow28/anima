import sys
from PIL import Image

TARGETS = {
    'primary_orange': (232, 155, 107),
    'cream_highlight': (244, 221, 184),
    'warm_brown_shadow': (168, 107, 69),
    'deep_brown': (92, 58, 36)
}

TOLS = {
    'primary_orange': 10,
    'cream_highlight': 6,
    'warm_brown_shadow': 6,
    'deep_brown': 4
}

def is_mascot_color(rgb):
    r, g, b = rgb
    for name, target in TARGETS.items():
        tr, tg, tb = target
        tol = TOLS[name]
        if abs(r - tr) <= tol and abs(g - tg) <= tol and abs(b - tb) <= tol:
            return name
    return None

def analyze_strict_profile(path):
    img = Image.open(path)
    width, height = img.size
    
    row_spans = []
    
    for y in range(height):
        row_xs = []
        for x in range(width):
            p = img.getpixel((x, y))[:3]
            if is_mascot_color(p):
                row_xs.append(x)
        if row_xs:
            left = min(row_xs)
            right = max(row_xs)
            row_spans.append((y, left, right, right - left + 1))
            
    if not row_spans:
        print("No strict mascot pixels found.")
        return
        
    ymin = row_spans[0][0]
    ymax = row_spans[-1][0]
    total_height = ymax - ymin + 1
    print(f"Strict Mascot Total Height: {total_height} (ymin={ymin}, ymax={ymax})")
    
    # Print the profile of strict pixels
    print("\nStrict Profile sample (every 10 rows):")
    for i in range(0, len(row_spans), 10):
        y, left, right, w = row_spans[i]
        bar = "#" * int(w / 10)
        print(f"Row {y:03d} (rel {y-ymin:03d}): width={w:3d} ({left:3d} to {right:3d}) {bar}")
        
    # Write to a file for complete inspection
    with open("profile_strict.txt", "w") as f:
        for y, left, right, w in row_spans:
            f.write(f"y={y}, rel_y={y-ymin}, left={left}, right={right}, width={w}\n")

if __name__ == '__main__':
    analyze_strict_profile('body-3quarter.png')
