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

def analyze_exact_matches(path):
    img = Image.open(path)
    width, height = img.size
    
    matches = {name: {} for name in TARGETS}
    others = {}
    
    for y in range(height):
        for x in range(width):
            p = img.getpixel((x, y))[:3]
            r, g, b = p
            
            matched = False
            for name, target in TARGETS.items():
                tr, tg, tb = target
                tol = TOLS[name]
                if abs(r - tr) <= tol and abs(g - tg) <= tol and abs(b - tb) <= tol:
                    matches[name][p] = matches[name].get(p, 0) + 1
                    matched = True
                    break
            if not matched:
                # exclude background (above 230 RGB distance from target)
                # Let's just track all other colors
                others[p] = others.get(p, 0) + 1
                
    for name in TARGETS:
        print(f"\nTarget {name}:")
        sorted_m = sorted(matches[name].items(), key=lambda x: x[1], reverse=True)
        total_m = sum(matches[name].values())
        print(f"Total matching pixels: {total_m}")
        for color, count in sorted_m[:5]:
            hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
            print(f" - {color} ({hex_color}): count {count} ({count/total_m:.2%})")
            
    print("\nNon-matching (excluding background-like colors with R,G,B > 220):")
    non_bg_others = {k: v for k, v in others.items() if not (k[0] > 220 and k[1] > 220 and k[2] > 210)}
    sorted_o = sorted(non_bg_others.items(), key=lambda x: x[1], reverse=True)
    total_o = sum(non_bg_others.values())
    print(f"Total non-matching non-background pixels: {total_o}")
    for color, count in sorted_o[:15]:
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
        # Find closest target
        closest = None
        min_d = 99999
        for name, target in TARGETS.items():
            d = sum((color[i] - target[i])**2 for i in range(3))**0.5
            if d < min_d:
                min_d = d
                closest = name
        print(f" - {color} ({hex_color}): count {count} ({count/total_o:.2%}) - closest to {closest} (dist {min_d:.1f})")

if __name__ == '__main__':
    analyze_exact_matches('body-3quarter.png')
