from PIL import Image

def inspect_dither(path):
    img = Image.open(path)
    width, height = img.size
    
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
    
    # Let's find a region with a high concentration of warm brown shadow pixels
    # specifically one that looks like a dither pattern (i.e. has orange and shadow mixed)
    best_region = None
    max_mix = 0
    
    step = 20
    for y in range(0, height - step, step):
        for x in range(0, width - step, step):
            orange_count = 0
            shadow_count = 0
            for dy in range(step):
                for dx in range(step):
                    p = img.getpixel((x + dx, y + dy))[:3]
                    r, g, b = p
                    if abs(r - TARGETS['primary_orange'][0]) <= TOLS['primary_orange'] and \
                       abs(g - TARGETS['primary_orange'][1]) <= TOLS['primary_orange'] and \
                       abs(b - TARGETS['primary_orange'][2]) <= TOLS['primary_orange']:
                        orange_count += 1
                    elif abs(r - TARGETS['warm_brown_shadow'][0]) <= TOLS['warm_brown_shadow'] and \
                         abs(g - TARGETS['warm_brown_shadow'][1]) <= TOLS['warm_brown_shadow'] and \
                         abs(b - TARGETS['warm_brown_shadow'][2]) <= TOLS['warm_brown_shadow']:
                        shadow_count += 1
            # We want a region where both orange and shadow are present
            mix = min(orange_count, shadow_count)
            if mix > max_mix:
                max_mix = mix
                best_region = (x, y)
                
    if not best_region:
        print("No mixed shadow/orange region found!")
        return
        
    rx, ry = best_region
    print(f"Printing 20x20 patch at x={rx}, y={ry}:")
    print("O = Orange, S = Shadow, C = Cream, D = Deep brown, . = Background, ? = Other")
    print("-" * 20)
    for dy in range(20):
        row_chars = []
        for dx in range(20):
            p = img.getpixel((rx + dx, ry + dy))[:3]
            r, g, b = p
            # Match color
            char = '?'
            # background check:
            if abs(r - 247) < 20 and abs(g - 248) < 20 and abs(b - 242) < 20:
                char = '.'
            elif abs(r - TARGETS['primary_orange'][0]) <= TOLS['primary_orange'] and \
                 abs(g - TARGETS['primary_orange'][1]) <= TOLS['primary_orange'] and \
                 abs(b - TARGETS['primary_orange'][2]) <= TOLS['primary_orange']:
                char = 'O'
            elif abs(r - TARGETS['cream_highlight'][0]) <= TOLS['cream_highlight'] and \
                 abs(g - TARGETS['cream_highlight'][1]) <= TOLS['cream_highlight'] and \
                 abs(b - TARGETS['cream_highlight'][2]) <= TOLS['cream_highlight']:
                char = 'C'
            elif abs(r - TARGETS['warm_brown_shadow'][0]) <= TOLS['warm_brown_shadow'] and \
                 abs(g - TARGETS['warm_brown_shadow'][1]) <= TOLS['warm_brown_shadow'] and \
                 abs(b - TARGETS['warm_brown_shadow'][2]) <= TOLS['warm_brown_shadow']:
                char = 'S'
            elif abs(r - TARGETS['deep_brown'][0]) <= TOLS['deep_brown'] and \
                 abs(g - TARGETS['deep_brown'][1]) <= TOLS['deep_brown'] and \
                 abs(b - TARGETS['deep_brown'][2]) <= TOLS['deep_brown']:
                char = 'D'
            row_chars.append(char)
        print("".join(row_chars))
    print("-" * 20)

if __name__ == '__main__':
    inspect_dither('body-3quarter.png')
