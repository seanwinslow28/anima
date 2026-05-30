import sys
from PIL import Image

def run_checks(img_path):
    img = Image.open(img_path)
    width, height = img.size
    
    # 1. Colors Vocabulary
    TARGETS = {
        'primary_orange': (232, 155, 107),       # #E89B6B
        'cream_highlight': (244, 221, 184),      # #F4DDB8
        'warm_brown_shadow': (168, 107, 69),     # #A86B45
        'deep_brown': (92, 58, 36)               # #5C3A24
    }
    TOLS = {
        'primary_orange': 10,
        'cream_highlight': 6,
        'warm_brown_shadow': 6,
        'deep_brown': 4
    }
    
    bg_ref = (247, 248, 242)
    
    # Identify bounds and check pixels
    ymin, ymax = height, 0
    xmin, xmax = width, 0
    
    # Quick pass to get bounding box
    bg_mask = {}
    for y in range(height):
        for x in range(width):
            p = img.getpixel((x, y))[:3]
            r, g, b = p
            is_bg = abs(r - bg_ref[0]) < 20 and abs(g - bg_ref[1]) < 20 and abs(b - bg_ref[2]) < 20
            bg_mask[(x, y)] = is_bg
            if not is_bg:
                if y < ymin: ymin = y
                if y > ymax: ymax = y
                if x < xmin: xmin = x
                if x > xmax: xmax = x
                
    char_width = xmax - xmin + 1
    char_height = ymax - ymin + 1
    
    print(f"Bounding Box: xmin={xmin}, xmax={xmax}, ymin={ymin}, ymax={ymax}")
    print(f"Dimensions: width={char_width}, height={char_height}")
    
    # Let's count colors inside the silhouette
    counts = {name: 0 for name in TARGETS}
    violating_count = 0
    
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            if bg_mask[(x, y)]:
                continue
            p = img.getpixel((x, y))[:3]
            r, g, b = p
            matched = False
            for name, target in TARGETS.items():
                tr, tg, tb = target
                tol = TOLS[name]
                if abs(r - tr) <= tol and abs(g - tg) <= tol and abs(b - tb) <= tol:
                    counts[name] += 1
                    matched = True
                    break
            if not matched:
                violating_count += 1
                
    total_silhouette = sum(counts.values()) + violating_count
    print(f"\n1. Palette Analysis:")
    print(f"Total silhouette pixels: {total_silhouette}")
    for name, count in counts.items():
        print(f"  - {name}: {count} ({count/total_silhouette:.2%})")
    print(f"  - Violating: {violating_count} ({violating_count/total_silhouette:.2%})")
    
    # Let's check cream highlight positions
    cream_ys = []
    for y in range(ymin, ymax + 1):
        row_cream = 0
        for x in range(xmin, xmax + 1):
            if bg_mask[(x, y)]:
                continue
            p = img.getpixel((x, y))[:3]
            r, g, b = p
            if abs(r - TARGETS['cream_highlight'][0]) <= TOLS['cream_highlight'] and \
               abs(g - TARGETS['cream_highlight'][1]) <= TOLS['cream_highlight'] and \
               abs(b - TARGETS['cream_highlight'][2]) <= TOLS['cream_highlight']:
                row_cream += 1
        if row_cream > 0:
            cream_ys.append(y)
            
    print(f"Cream height range: y={min(cream_ys)} to {max(cream_ys)} (rel {min(cream_ys)-ymin} to {max(cream_ys)-ymin})")
    
    # 2. Head-to-body proportion
    row_widths = []
    for y in range(ymin, ymax + 1):
        row_xs = [x for x in range(xmin, xmax + 1) if not bg_mask[(x, y)]]
        if row_xs:
            row_widths.append(max(row_xs) - min(row_xs) + 1)
        else:
            row_widths.append(0)
            
    # Search for neck between 30% and 55% of height
    search_start = int(0.30 * char_height)
    search_end = int(0.55 * char_height)
    
    min_w = 99999
    neck_idx = 0
    for i in range(search_start, search_end):
        if row_widths[i] < min_w and row_widths[i] > 0:
            min_w = row_widths[i]
            neck_idx = i
            
    neck_y = ymin + neck_idx
    neck_w = row_widths[neck_idx]
    
    head_height = neck_y - ymin + 1
    body_height = ymax - neck_y
    
    print(f"\n2. Proportions:")
    print(f"  Neck division: y={neck_y} (rel y={neck_idx}), width={neck_w}")
    print(f"  Head Height: {head_height} px ({head_height/char_height:.2%})")
    print(f"  Body Height: {body_height} px ({body_height/char_height:.2%})")
    print(f"  Head:Body Ratio: {head_height/body_height:.3f} (target 2:3 = 0.667, dev={abs(head_height/body_height - 0.667):.3f})")
    
    # Check if this deviation exceeds the 10% of total height tolerance:
    # "Tolerance is ±10% of total body height [measured crown-to-soles]."
    # Wait, 10% of total body height means 10% of char_height = 92.3 pixels.
    # Deviation in head height:
    # Target head height is 2/5 of total height = 0.40 * 923 = 369.2 pixels.
    # Actual head height is 424 pixels.
    # Deviation in pixels = 424 - 369.2 = 54.8 pixels.
    # This is 54.8 / 923 = 5.94% of total height, which is within the ±10% (92.3 px) tolerance.
    
    # Let's check shoulder width
    # Max head width in the head region (top to neck)
    max_head_w = max(row_widths[:neck_idx])
    # Max body width in the body region (neck to bottom)
    max_body_w = max(row_widths[neck_idx:])
    
    print(f"  Max Head Width: {max_head_w} px")
    print(f"  Max Body/Shoulder Width: {max_body_w} px")
    print(f"  Body to Head Width Ratio: {max_body_w/max_head_w:.3f} (target 1.2, dev={abs(max_body_w/max_head_w - 1.2):.3f})")
    
    # 3. Dither pattern verification
    # Count warm brown shadow pixels and see if they alternate.
    warm_brown_coords = set()
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            if bg_mask[(x, y)]:
                continue
            p = img.getpixel((x, y))[:3]
            r, g, b = p
            if abs(r - TARGETS['warm_brown_shadow'][0]) <= TOLS['warm_brown_shadow'] and \
               abs(g - TARGETS['warm_brown_shadow'][1]) <= TOLS['warm_brown_shadow'] and \
               abs(b - TARGETS['warm_brown_shadow'][2]) <= TOLS['warm_brown_shadow']:
                warm_brown_coords.add((x, y))
                
    n_pixels = len(warm_brown_coords)
    dist1_neighbors = 0
    dist2_neighbors = 0
    
    for (x, y) in warm_brown_coords:
        has_dist1 = (x, y-1) in warm_brown_coords or (x, y+1) in warm_brown_coords
        has_dist2 = (x, y-2) in warm_brown_coords or (x, y+2) in warm_brown_coords
        if has_dist1:
            dist1_neighbors += 1
        if has_dist2:
            dist2_neighbors += 1
            
    print(f"\n3. Dither Pattern:")
    print(f"  Warm Brown Shadow Pixels: {n_pixels}")
    print(f"  Pixels with warm brown neighbor at dist 1: {dist1_neighbors} ({dist1_neighbors/max(1, n_pixels):.2%})")
    print(f"  Pixels with warm brown neighbor at dist 2: {dist2_neighbors} ({dist2_neighbors/max(1, n_pixels):.2%})")
    
if __name__ == '__main__':
    run_checks('body-3quarter.png')
