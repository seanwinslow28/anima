from PIL import Image

def analyze_vertical_profile(path):
    img = Image.open(path)
    width, height = img.size
    bg_ref = (247, 248, 242)
    
    row_spans = []
    
    for y in range(height):
        left = None
        right = None
        for x in range(width):
            p = img.getpixel((x, y))[:3]
            r, g, b = p
            dist_to_bg = ((r - bg_ref[0])**2 + (g - bg_ref[1])**2 + (b - bg_ref[2])**2)**0.5
            # Non-background
            if dist_to_bg >= 20:
                if left is None:
                    left = x
                right = x
        if left is not None:
            row_spans.append((y, left, right, right - left + 1))
            
    if not row_spans:
        print("No character pixels found.")
        return
        
    ymin = row_spans[0][0]
    ymax = row_spans[-1][0]
    total_height = ymax - ymin + 1
    print(f"Total Height: {total_height} (ymin={ymin}, ymax={ymax})")
    
    # Print the profile every 10 pixels to see the shape
    print("\nProfile sample (every 15 rows):")
    for i in range(0, len(row_spans), 15):
        y, left, right, w = row_spans[i]
        bar = "#" * int(w / 10)
        print(f"Row {y:03d} (rel {y-ymin:03d}): width={w:3d} ({left:3d} to {right:3d}) {bar}")
        
    # Let's write all row spans to a file so we can inspect it fully if needed
    with open("profile_full.txt", "w") as f:
        for y, left, right, w in row_spans:
            f.write(f"y={y}, rel_y={y-ymin}, left={left}, right={right}, width={w}\n")

if __name__ == '__main__':
    analyze_vertical_profile('body-3quarter.png')
