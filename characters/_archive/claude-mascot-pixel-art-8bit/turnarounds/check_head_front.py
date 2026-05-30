import sys
from PIL import Image
from collections import Counter

def analyze_head_front(img_path):
    img = Image.open(img_path)
    width, height = img.size
    print(f"Image dimensions: {width}x{height}")
    
    # Get all colors
    pixels = list(img.getdata())
    color_counts = Counter(pixels)
    
    print("\nAll colors in image (top 20):")
    sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
    for color, count in sorted_colors[:20]:
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color[:3])
        alpha = color[3] if len(color) > 3 else "N/A"
        print(f" - {color} ({hex_color}), alpha={alpha}: count {count} ({count/len(pixels):.4%})")

    # Define color targets and tolerances
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
    
    # We want to identify the background. Let's look at the most common color.
    # Usually it's transparent (alpha=0) or a solid color.
    # Let's see what is background. We can check the corner pixel (0,0) or check the alpha.
    # We want to identify the background. Let's look at the most common color.
    # Usually it's transparent (alpha=0) or a solid color.
    # In this case, the most common color is (255, 255, 255) with alpha=255.
    bg_ref = (255, 255, 255)
    
    # Define criteria for background: either alpha == 0, or color is close to white (255, 255, 255)
    def is_background(p):
        if len(p) > 3 and p[3] == 0:
            return True
        r, g, b = p[:3]
        # Let's check if it is within a small distance to white.
        # Since it's a solid white background, let's say diff from (255, 255, 255) is very small.
        # If the image uses white as background, then background should be exactly or very close to (255, 255, 255).
        return r > 240 and g > 240 and b > 240

    ymin, ymax = height, 0
    xmin, xmax = width, 0
    character_pixels = []
    non_bg_coords = []
    
    for y in range(height):
        for x in range(width):
            p = img.getpixel((x, y))
            if not is_background(p):
                non_bg_coords.append((x, y))
                if y < ymin: ymin = y
                if y > ymax: ymax = y
                if x < xmin: xmin = x
                if x > xmax: xmax = x
                
    if not non_bg_coords:
        print("No character pixels found!")
        return
        
    print(f"\nCharacter Bounding Box: xmin={xmin}, xmax={xmax}, ymin={ymin}, ymax={ymax}")
    print(f"Character Dimensions: width={xmax - xmin + 1}, height={ymax - ymin + 1}")
    
    # Check each pixel against targets
    unknown_pixels = []
    categorized_pixels = {name: [] for name in TARGETS}
    
    for (x, y) in non_bg_coords:
        p = img.getpixel((x, y))
        r, g, b = p[:3]
        matched = False
        for name, target in TARGETS.items():
            tol = TOLS[name]
            if abs(r - target[0]) <= tol and abs(g - target[1]) <= tol and abs(b - target[2]) <= tol:
                categorized_pixels[name].append((x, y, p))
                matched = True
                break
        if not matched:
            unknown_pixels.append((x, y, p))
            
    print("\nClassification of character pixels:")
    total_char_pixels = len(non_bg_coords)
    for name, pixels in categorized_pixels.items():
        print(f"  - {name}: {len(pixels)} ({len(pixels)/total_char_pixels:.2%})")
    print(f"  - Unknown/Violating: {len(unknown_pixels)} ({len(unknown_pixels)/total_char_pixels:.2%})")
    
    if unknown_pixels:
        print("\nSome violating pixels (up to 20):")
        for x, y, p in unknown_pixels[:20]:
            print(f"  - ({x}, {y}): {p} (#{'%02x%02x%02x' % p[:3]})")
            
    # Check for anti-aliasing between steps:
    # Check if there are any pixels adjacent to transition borders that are intermediate values
    # Or just checking if there are ANY violating/unknown pixels inside the silhouette.
    # Also, we should inspect the grid alignment to see if there's a scaling factor.
    # Let's find the minimum run of identical pixels in rows/cols of the character to detect scaling.
    horizontal_runs = []
    for y in range(ymin, ymax + 1):
        current_color = None
        run_len = 0
        for x in range(xmin, xmax + 1):
            p = img.getpixel((x, y))
            if is_background(p):
                if run_len > 0:
                    horizontal_runs.append(run_len)
                    run_len = 0
                current_color = None
            else:
                p_color = p[:3]
                if current_color is None:
                    current_color = p_color
                    run_len = 1
                elif p_color == current_color:
                    run_len += 1
                else:
                    horizontal_runs.append(run_len)
                    current_color = p_color
                    run_len = 1
        if run_len > 0:
            horizontal_runs.append(run_len)
            
    vertical_runs = []
    for x in range(xmin, xmax + 1):
        current_color = None
        run_len = 0
        for y in range(ymin, ymax + 1):
            p = img.getpixel((x, y))
            if is_background(p):
                if run_len > 0:
                    vertical_runs.append(run_len)
                    run_len = 0
                current_color = None
            else:
                p_color = p[:3]
                if current_color is None:
                    current_color = p_color
                    run_len = 1
                elif p_color == current_color:
                    run_len += 1
                else:
                    vertical_runs.append(run_len)
                    current_color = p_color
                    run_len = 1
        if run_len > 0:
            vertical_runs.append(run_len)
            
    h_counter = Counter(horizontal_runs)
    v_counter = Counter(vertical_runs)
    print("\nHorizontal Run Lengths (top 10):")
    for r, c in sorted(h_counter.items(), key=lambda x: x[0])[:10]:
        print(f"  - {r}px: count {c}")
    print("Vertical Run Lengths (top 10):")
    for r, c in sorted(v_counter.items(), key=lambda x: x[0])[:10]:
        print(f"  - {r}px: count {c}")

    # Analyze deep brown pixels (eyes, mouth)
    deep_brown_pixels = categorized_pixels['deep_brown']
    print(f"\nDeep brown pixels count: {len(deep_brown_pixels)}")
    # Find contiguous clusters of deep brown pixels
    visited = set()
    clusters = []
    
    db_coords = set((x, y) for x, y, p in deep_brown_pixels)
    for x, y in db_coords:
        if (x, y) not in visited:
            # BFS/DFS to find cluster
            cluster = []
            queue = [(x, y)]
            visited.add((x, y))
            while queue:
                cx, cy = queue.pop(0)
                cluster.append((cx, cy))
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
                    nx, ny = cx + dx, cy + dy
                    if (nx, ny) in db_coords and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
            clusters.append(cluster)
            
    print(f"Found {len(clusters)} deep brown clusters:")
    for idx, c in enumerate(clusters):
        c_xmin = min(x for x, y in c)
        c_xmax = max(x for x, y in c)
        c_ymin = min(y for x, y in c)
        c_ymax = max(y for x, y in c)
        print(f"  Cluster {idx+1}: size={len(c)}, bounding box=[({c_xmin},{c_ymin}) to ({c_xmax},{c_ymax})]")
        # Print shape of cluster
        for cy in range(c_ymin, c_ymax + 1):
            row_str = ""
            for cx in range(c_xmin, c_xmax + 1):
                row_str += "X" if (cx, cy) in db_coords else "."
            print(f"    {row_str}")

    # Analyze cream highlight pixels (crown, fingertips, etc.)
    cream_pixels = categorized_pixels['cream_highlight']
    print(f"\nCream highlight pixels count: {len(cream_pixels)}")
    if cream_pixels:
        cream_coords = set((x, y) for x, y, p in cream_pixels)
        c_visited = set()
        cream_clusters = []
        for x, y in cream_coords:
            if (x, y) not in c_visited:
                cluster = []
                queue = [(x, y)]
                c_visited.add((x, y))
                while queue:
                    cx, cy = queue.pop(0)
                    cluster.append((cx, cy))
                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
                        nx, ny = cx + dx, cy + dy
                        if (nx, ny) in cream_coords and (nx, ny) not in c_visited:
                            c_visited.add((nx, ny))
                            queue.append((nx, ny))
                cream_clusters.append(cluster)
        print(f"Found {len(cream_clusters)} cream highlight clusters:")
        for idx, c in enumerate(cream_clusters):
            c_xmin = min(x for x, y in c)
            c_xmax = max(x for x, y in c)
            c_ymin = min(y for x, y in c)
            c_ymax = max(y for x, y in c)
            print(f"  Cluster {idx+1}: size={len(c)}, bounding box=[({c_xmin},{c_ymin}) to ({c_xmax},{c_ymax})]")

if __name__ == '__main__':
    img_path = 'head-front.png'
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
    analyze_head_front(img_path)
