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

def get_char(rgb):
    r, g, b = rgb
    # Background check
    if abs(r - 247) <= 15 and abs(g - 248) <= 15 and abs(b - 242) <= 15:
        return '.'
        
    for name, target in TARGETS.items():
        tr, tg, tb = target
        tol = TOLS[name]
        if abs(r - tr) <= tol and abs(g - tg) <= tol and abs(b - tb) <= tol:
            if name == 'primary_orange': return 'O'
            if name == 'cream_highlight': return 'C'
            if name == 'warm_brown_shadow': return 'S'
            if name == 'deep_brown': return 'D'
            
    return '?'

def generate_ascii_exact(path, cols=80):
    img = Image.open(path)
    width, height = img.size
    
    ymin, ymax = 172, 864
    xmin, xmax = 229, 796
    
    char_w = xmax - xmin + 1
    char_h = ymax - ymin + 1
    
    rows = int(cols * (char_h / char_w) * 0.5)
    
    # We will sample pixels at step_x and step_y using nearest-neighbor
    print(f"Nearest-Neighbor sampled ASCII representation ({cols}x{rows}):")
    print("O = Orange, C = Cream, S = Shadow, D = Deep brown, . = Background, ? = Violating color")
    print("-" * cols)
    
    for r in range(rows):
        y = ymin + int(r * char_h / rows)
        line = []
        for c in range(cols):
            x = xmin + int(c * char_w / cols)
            if x >= width or y >= height:
                line.append('.')
                continue
            p = img.getpixel((x, y))
            line.append(get_char(p[:3]))
        print("".join(line))
    print("-" * cols)

if __name__ == '__main__':
    generate_ascii_exact('body-3quarter.png')
