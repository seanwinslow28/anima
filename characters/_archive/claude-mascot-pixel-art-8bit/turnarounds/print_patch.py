from PIL import Image

img = Image.open('body-back.png')

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

x_start, x_end = 340, 400
y_start, y_end = 570, 610

print("Patch visualization (O=Orange, S=Shadow, C=Cream, D=Deep brown, .=BG, ?=Other):")
for y in range(y_start, y_end):
    row_chars = []
    for x in range(x_start, x_end):
        p = img.getpixel((x, y))[:3]
        r, g, b = p
        
        # Match color
        char = '?'
        is_bg = (r > 210 and g > 210 and b > 210 and abs(r - g) < 15 and abs(g - b) < 15)
        if is_bg:
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
    print(f"y={y:3d}: " + "".join(row_chars))
