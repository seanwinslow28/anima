from PIL import Image

def generate_ascii(path, cols=80):
    img = Image.open(path).convert('RGB')
    width, height = img.size
    
    # Bounding box of character
    ymin, ymax = 0, 1023
    xmin, xmax = 49, 974
    
    char_w = xmax - xmin + 1
    char_h = ymax - ymin + 1
    
    rows = int(cols * (char_h / char_w) * 0.5)
    
    targets = {
        'O': (232, 155, 107),  # primary_orange
        'C': (244, 221, 184),  # cream_highlight
        'S': (168, 107, 69),   # warm_brown_shadow
        'D': (92, 58, 36)      # deep_brown
    }
    
    # Let's see how to classify a pixel:
    def classify(p):
        r, g, b = p
        if r > 240 and g > 240 and b > 240:
            return '.'  # background
        
        # Check closest color
        closest = '?'
        min_dist = 999999
        for symbol, target in targets.items():
            dist = (r-target[0])**2 + (g-target[1])**2 + (b-target[2])**2
            if dist < min_dist:
                min_dist = dist
                closest = symbol
                
        # If the minimum distance is too large, we label it as '?' (violating)
        if min_dist > 1500: # Threshold for looking distinct from target
            return '?'
            
        return closest

    print(f"Resized ASCII representation of {path} ({cols}x{rows}):")
    print("O=Orange, C=Cream, S=Shadow, D=Deep brown, .=Background, ?=Violating/Other")
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
            line.append(classify(p))
        print("".join(line))
    print("-" * cols)

if __name__ == '__main__':
    generate_ascii('head-front.png')
