from PIL import Image
from collections import Counter
import math

def inspect_colors_exact(path):
    img = Image.open(path)
    width, height = img.size
    
    # Target colors
    targets = {
        'primary_orange': (232, 155, 107),       # #E89B6B
        'cream_highlight': (244, 221, 184),      # #F4DDB8
        'warm_brown_shadow': (168, 107, 69),     # #A86B45
        'deep_brown': (92, 58, 36)               # #5C3A24
    }
    
    tols = {
        'primary_orange': 10,
        'cream_highlight': 6,
        'warm_brown_shadow': 6,
        'deep_brown': 4
    }
    
    pixels = list(img.convert('RGB').getdata())
    total_pixels = len(pixels)
    
    # Identify background
    # Let's count pixels where R > 250 and G > 250 and B > 250
    bg_count = 0
    non_bg_pixels = []
    
    for p in pixels:
        r, g, b = p
        if r > 250 and g > 250 and b > 250:
            bg_count += 1
        else:
            non_bg_pixels.append(p)
            
    total_non_bg = len(non_bg_pixels)
    
    print(f"Total pixels: {total_pixels}")
    print(f"Background pixels (R,G,B > 250): {bg_count} ({bg_count/total_pixels:.2%})")
    print(f"Non-background pixels: {total_non_bg} ({total_non_bg/total_pixels:.2%})")
    
    # Check strict targets
    strict_counts = {name: 0 for name in targets}
    for p in non_bg_pixels:
        r, g, b = p
        for name, target in targets.items():
            tr, tg, tb = target
            tol = tols[name]
            if abs(r - tr) <= tol and abs(g - tg) <= tol and abs(b - tb) <= tol:
                strict_counts[name] += 1
                break
                
    print("\nStrict Match Counts (within specified tolerances):")
    total_strict_matched = 0
    for name, count in strict_counts.items():
        print(f"  - {name}: {count} ({count/total_non_bg:.2%} of non-bg)")
        total_strict_matched += count
        
    print(f"Total strict matched: {total_strict_matched} ({total_strict_matched/total_non_bg:.2%})")
    print(f"Strict Violating / Unmatched: {total_non_bg - total_strict_matched} ({(total_non_bg - total_strict_matched)/total_non_bg:.2%})")
    
    counter = Counter(non_bg_pixels)
    
    print("\nTop 30 non-background colors:")
    for color, count in counter.most_common(30):
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
        # Find distance to closest target
        closest_target = None
        min_dist = 99999.0
        for name, target in targets.items():
            dist = math.sqrt(sum((color[i] - target[i])**2 for i in range(3)))
            if dist < min_dist:
                min_dist = dist
                closest_target = name
        print(f"  - {color} ({hex_color}): count={count} ({count/total_non_bg:.2%}) -> closest to {closest_target} (Euclidean dist {min_dist:.1f})")

if __name__ == '__main__':
    import sys
    img_path = 'head-front.png'
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
    inspect_colors_exact(img_path)
