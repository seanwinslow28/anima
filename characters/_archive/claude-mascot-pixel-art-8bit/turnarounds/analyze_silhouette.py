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

def analyze_silhouette(path):
    img = Image.open(path)
    width, height = img.size
    
    # Background color is roughly (247, 248, 242)
    bg_ref = (247, 248, 242)
    
    # We will classify every pixel in the image
    bg_count = 0
    strict_mascot_count = 0
    non_bg_other_count = 0
    
    non_bg_others = {}
    
    for y in range(height):
        for x in range(width):
            p = img.getpixel((x, y))[:3]
            r, g, b = p
            
            # Check if background: let's use Euclidean distance in RGB space
            dist_to_bg = ((r - bg_ref[0])**2 + (g - bg_ref[1])**2 + (b - bg_ref[2])**2)**0.5
            
            # If distance to background is very small, it's background
            if dist_to_bg < 20:
                bg_count += 1
            else:
                cat = is_mascot_color(p)
                if cat:
                    strict_mascot_count += 1
                else:
                    non_bg_other_count += 1
                    non_bg_others[p] = non_bg_others.get(p, 0) + 1
                    
    total = width * height
    print(f"Total image pixels: {total}")
    print(f"Background pixels: {bg_count} ({bg_count/total:.2%})")
    print(f"Strict mascot pixels: {strict_mascot_count} ({strict_mascot_count/total:.2%})")
    print(f"Non-background other pixels (violating colors): {non_bg_other_count} ({non_bg_other_count/total:.2%})")
    
    # Check what portion of the non-background pixels are violating
    non_bg_total = strict_mascot_count + non_bg_other_count
    print(f"Total non-background pixels (character + halo): {non_bg_total}")
    print(f"Strict mascot percentage of character: {strict_mascot_count/non_bg_total:.2%}")
    print(f"Violating color percentage of character: {non_bg_other_count/non_bg_total:.2%}")
    
    # List top violating colors
    sorted_others = sorted(non_bg_others.items(), key=lambda x: x[1], reverse=True)
    print("\nTop violating colors in the character area:")
    for i, (color, count) in enumerate(sorted_others[:15]):
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
        print(f" - RGB {color} ({hex_color}): count {count} ({count/non_bg_total:.2%})")

if __name__ == '__main__':
    analyze_silhouette('body-3quarter.png')
