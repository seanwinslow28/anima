from PIL import Image

def find_features(path):
    img = Image.open(path)
    width, height = img.size
    
    # Target deep brown is (92, 58, 36). Let's find any pixels with R < 120, G < 80, B < 60
    # that are not background
    dark_pixels = []
    
    for y in range(height):
        for x in range(width):
            p = img.getpixel((x, y))[:3]
            r, g, b = p
            # Avoid background or light pixels
            if r < 110 and g < 75 and b < 50:
                dark_pixels.append((x, y, p))
                
    if not dark_pixels:
        print("No dark pixels found!")
        return
        
    ys = [p[1] for p in dark_pixels]
    ymin, ymax = min(ys), max(ys)
    print(f"Dark pixels count: {len(dark_pixels)}")
    print(f"Vertical range of dark features: y={ymin} to y={ymax} (rel_y={ymin-172} to {ymax-172})")
    
    # Print the distribution of dark pixels by row
    from collections import Counter
    y_counts = Counter(ys)
    for y in sorted(y_counts.keys()):
        print(f"Row {y:3d} (rel {y-172:3d}): {y_counts[y]} dark pixels")

if __name__ == '__main__':
    find_features('body-3quarter.png')
