from PIL import Image

def analyze_vertical_profile(path):
    img = Image.open(path)
    width, height = img.size
    
    row_spans = []
    
    for y in range(height):
        left = None
        right = None
        for x in range(width):
            p = img.getpixel((x, y))[:3]
            r, g, b = p
            # Non-background check
            is_bg = (r > 210 and g > 210 and b > 210 and abs(r - g) < 15 and abs(g - b) < 15)
            if not is_bg:
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
    
    # Print the profile every 15 pixels to see the shape
    print("\nProfile sample (every 15 rows):")
    for i in range(0, len(row_spans), 15):
        y, left, right, w = row_spans[i]
        bar = "#" * int(w / 10)
        print(f"Row {y:03d} (rel {y-ymin:03d}): width={w:3d} ({left:3d} to {right:3d}) {bar}")
        
    # Write all row spans to profile_back.txt
    with open("profile_back.txt", "w") as f:
        for y, left, right, w in row_spans:
            f.write(f"y={y}, rel_y={y-ymin}, left={left}, right={right}, width={w}\n")

if __name__ == '__main__':
    analyze_vertical_profile('body-back.png')
