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

def analyze_character(path):
    img = Image.open(path)
    width, height = img.size
    
    # Store mascot pixel coordinates and their matching category
    mascot_pixels = []
    
    for y in range(height):
        for x in range(width):
            p = img.getpixel((x, y))
            cat = is_mascot_color(p[:3])
            if cat:
                mascot_pixels.append((x, y, cat, p[:3]))
                
    if not mascot_pixels:
        print("No mascot pixels found using the strict color tolerances!")
        return
        
    print(f"Total strict mascot pixels: {len(mascot_pixels)}")
    
    xs = [p[0] for p in mascot_pixels]
    ys = [p[1] for p in mascot_pixels]
    
    ymin, ymax = min(ys), max(ys)
    xmin, xmax = min(xs), max(xs)
    
    char_width = xmax - xmin + 1
    char_height = ymax - ymin + 1
    print(f"Character bounding box: xmin={xmin}, xmax={xmax}, ymin={ymin}, ymax={ymax}")
    print(f"Character dimensions: width={char_width}, height={char_height}")
    
    # Let's count categories inside the bounding box
    bbox_counts = {'primary_orange': 0, 'cream_highlight': 0, 'warm_brown_shadow': 0, 'deep_brown': 0, 'other': 0}
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            p = img.getpixel((x, y))
            cat = is_mascot_color(p[:3])
            if cat:
                bbox_counts[cat] += 1
            else:
                bbox_counts['other'] += 1
                
    print("\nPixel counts within character bounding box:")
    bbox_total = char_width * char_height
    for cat, count in bbox_counts.items():
        print(f" - {cat}: {count} ({count/bbox_total:.2%})")
        
    # Silhouette area check: dominant silhouette color should be primary_orange
    silhouette_pixels = bbox_counts['primary_orange'] + bbox_counts['cream_highlight'] + bbox_counts['warm_brown_shadow'] + bbox_counts['deep_brown']
    print(f"Total silhouette pixels (strict): {silhouette_pixels}")
    if silhouette_pixels > 0:
        print(f"Orange ratio of silhouette: {bbox_counts['primary_orange'] / silhouette_pixels:.2%}")
        print(f"Cream ratio of silhouette: {bbox_counts['cream_highlight'] / silhouette_pixels:.2%}")
        print(f"Warm brown shadow ratio of silhouette: {bbox_counts['warm_brown_shadow'] / silhouette_pixels:.2%}")
        print(f"Deep brown ratio of silhouette: {bbox_counts['deep_brown'] / silhouette_pixels:.2%}")
        
    # Analyze vertical profile (width of character at each y coordinate)
    profile_width = []
    for y in range(ymin, ymax + 1):
        row_xs = [p[0] for p in mascot_pixels if p[1] == y]
        if row_xs:
            w = max(row_xs) - min(row_xs) + 1
        else:
            w = 0
        profile_width.append((y, w))
        
    # Print vertical profile in ranges to see where the head and body are
    print("\nVertical profile (y, width):")
    # Let's write the profile to a file or inspect some key regions.
    # Typically, the head is wide, neck is narrow, body is wide.
    # Let's find the minimum width in the neck area (around upper 1/3 of height).
    # Since head-to-body is approx 2:3, the neck should be around ymin + 0.4 * char_height
    neck_search_min = ymin + int(0.25 * char_height)
    neck_search_max = ymin + int(0.50 * char_height)
    
    neck_y = None
    min_neck_w = char_width
    for y, w in profile_width:
        if neck_search_min <= y <= neck_search_max:
            if w < min_neck_w and w > 0:
                min_neck_w = w
                neck_y = y
                
    print(f"Guessed neck/chin division: y={neck_y} (width={min_neck_w})")
    if neck_y:
        head_height = neck_y - ymin + 1
        body_height = ymax - neck_y
        print(f"Estimated Head Height (ymin to neck): {head_height} pixels ({head_height/char_height:.2%})")
        print(f"Estimated Body Height (neck to ymax): {body_height} pixels ({body_height/char_height:.2%})")
        print(f"Ratio Head-to-Body: {head_height}:{body_height} (approx {head_height/body_height:.2f} vs target 2:3 = 0.67)")
        
        # Max head width (should be in the head region)
        head_row_widths = [w for y, w in profile_width if ymin <= y < neck_y]
        max_head_w = max(head_row_widths) if head_row_widths else 0
        
        # Max body width (should be in the body region)
        body_row_widths = [w for y, w in profile_width if neck_y <= y <= ymax]
        max_body_w = max(body_row_widths) if body_row_widths else 0
        
        print(f"Max head width: {max_head_w} pixels")
        print(f"Max body/shoulder width: {max_body_w} pixels")
        print(f"Body width to head width ratio: {max_body_w/max_head_w:.2f} (target 1.2x)")
        
    # Check if there is dithering:
    # "vertical 2-pixel-spaced dots — single-pixel warm-brown marks on every second row along a vertical axis"
    # Let's scan the image for warm_brown_shadow pixels and check if they alternate vertically.
    # Let's count how many warm_brown_shadow pixels have another warm_brown_shadow pixel exactly 2 pixels above/below
    # vs 1 pixel above/below.
    warm_brown_coords = set((p[0], p[1]) for p in mascot_pixels if p[2] == 'warm_brown_shadow')
    if warm_brown_coords:
        dist_1 = 0
        dist_2 = 0
        for (x, y) in warm_brown_coords:
            if (x, y-1) in warm_brown_coords or (x, y+1) in warm_brown_coords:
                dist_1 += 1
            if (x, y-2) in warm_brown_coords or (x, y+2) in warm_brown_coords:
                dist_2 += 1
        print(f"\nDither analysis (warm brown shadow adjacencies):")
        print(f" - Warm brown pixels: {len(warm_brown_coords)}")
        print(f" - Pixels with vertical neighbor at dist 1: {dist_1} ({dist_1/len(warm_brown_coords):.2%})")
        print(f" - Pixels with vertical neighbor at dist 2: {dist_2} ({dist_2/len(warm_brown_coords):.2%})")

if __name__ == '__main__':
    analyze_character('body-3quarter.png')
