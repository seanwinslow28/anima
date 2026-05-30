from PIL import Image

def run_checks(img_path):
    img = Image.open(img_path)
    width, height = img.size
    
    # 1. Colors Vocabulary
    # Target values from rules:
    # Primary orange: #E89B6B = (232, 155, 107) -> Tol = 10
    # Cream highlight: #F4DDB8 = (244, 221, 184) -> Tol = 6
    # Warm brown shadow: #A86B45 = (168, 107, 69) -> Tol = 6
    # Deep brown: #5C3A24 = (92, 58, 36) -> Tol = 4
    
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
    
    # Background in body-back.png appears to be around (231, 231, 231) / #e7e7e7.
    # Let's define is_bg by checking if it is very close to (231, 231, 231) or general light gray.
    # Let's inspect the corner pixels to be sure.
    bg_sample = img.getpixel((0, 0))[:3]
    print(f"Top-left pixel color (assumed BG): {bg_sample}")
    
    bg_mask = {}
    ymin, ymax = height, 0
    xmin, xmax = width, 0
    
    for y in range(height):
        for x in range(width):
            p = img.getpixel((x, y))[:3]
            r, g, b = p
            # Background is very light grey (almost white/grey).
            # The character consists of orange, cream, shadow (warm brown), deep brown.
            # Let's check if the pixel matches any of the character colors.
            # If it's close to light grey (r, g, b all > 210 and within 10 of each other), it's background.
            is_bg = (r > 210 and g > 210 and b > 210 and abs(r - g) < 15 and abs(g - b) < 15)
            # Alternatively, if it is close to bg_sample:
            # is_bg = abs(r - bg_sample[0]) < 20 and abs(g - bg_sample[1]) < 20 and abs(b - bg_sample[2]) < 20
            bg_mask[(x, y)] = is_bg
            if not is_bg:
                if y < ymin: ymin = y
                if y > ymax: ymax = y
                if x < xmin: xmin = x
                if x > xmax: xmax = x
                
    char_width = xmax - xmin + 1
    char_height = ymax - ymin + 1
    
    print(f"Corrected Bounding Box: xmin={xmin}, xmax={xmax}, ymin={ymin}, ymax={ymax}")
    print(f"Character Dimensions: width={char_width}, height={char_height}")
    
    counts = {name: 0 for name in TARGETS}
    violating_count = 0
    violating_pixels = {}
    
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
                violating_pixels[p] = violating_pixels.get(p, 0) + 1
                
    total_silhouette = sum(counts.values()) + violating_count
    print(f"\n1. Palette Analysis (Silhouette total pixels = {total_silhouette}):")
    for name, count in counts.items():
        print(f"  - {name}: {count} ({count/total_silhouette:.2%})")
    print(f"  - Violating: {violating_count} ({violating_count/total_silhouette:.2%})")
    
    print("\nTop violating colors inside silhouette:")
    sorted_viol = sorted(violating_pixels.items(), key=lambda x: x[1], reverse=True)
    for color, count in sorted_viol[:10]:
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
        # Find closest target
        closest = None
        min_d = 99999
        for name, target in TARGETS.items():
            d = sum((color[i] - target[i])**2 for i in range(3))**0.5
            if d < min_d:
                min_d = d
                closest = name
        print(f" - {color} ({hex_color}): count {count} ({count/total_silhouette:.2%}) - closest to {closest} (dist {min_d:.1f})")

    # Cream highlight check
    cream_count = counts['cream_highlight']
    print(f"\nCream Highlight Count: {cream_count}")
    
    # 2. Proportions:
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
    
    deviation_pct = (head_height - 0.40 * char_height) / char_height
    print(f"  Head Height deviation from 40% of total height: {deviation_pct:.2%}")
    
    # 3. Dither Pattern check:
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
    
    # Let's check isolated shadow pixels (dither checker)
    isolated_shadows = 0
    for (x, y) in warm_brown_coords:
        # Check if above and below are orange
        p_above = img.getpixel((x, y-1))[:3] if y-1 >= 0 else (0,0,0)
        p_below = img.getpixel((x, y+1))[:3] if y+1 < height else (0,0,0)
        
        is_orange_above = abs(p_above[0] - TARGETS['primary_orange'][0]) <= TOLS['primary_orange'] and \
                          abs(p_above[1] - TARGETS['primary_orange'][1]) <= TOLS['primary_orange'] and \
                          abs(p_above[2] - TARGETS['primary_orange'][2]) <= TOLS['primary_orange']
        is_orange_below = abs(p_below[0] - TARGETS['primary_orange'][0]) <= TOLS['primary_orange'] and \
                          abs(p_below[1] - TARGETS['primary_orange'][1]) <= TOLS['primary_orange'] and \
                          abs(p_below[2] - TARGETS['primary_orange'][2]) <= TOLS['primary_orange']
        if is_orange_above and is_orange_below:
            isolated_shadows += 1
            
    print(f"  Isolated shadow pixels (vertical dither candidates): {isolated_shadows} ({isolated_shadows/max(1, n_pixels):.2%})")

if __name__ == '__main__':
    run_checks('body-back.png')
