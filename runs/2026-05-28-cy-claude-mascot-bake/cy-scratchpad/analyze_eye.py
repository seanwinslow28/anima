from PIL import Image

def analyze_left_eye(path):
    im = Image.open(path).convert('RGB')
    # Bounding box of left eye: x in [282, 408], y in [282, 408]
    colors = {}
    for y in range(282, 409):
        for x in range(282, 409):
            color = im.getpixel((x, y))
            colors[color] = colors.get(color, 0) + 1
            
    print("Unique colors in the left eye region:")
    sorted_colors = sorted(colors.items(), key=lambda x: x[1], reverse=True)
    for c, count in sorted_colors[:15]:
        hex_color = '#{:02x}{:02x}{:02x}'.format(*c)
        print(f"  {hex_color} : {count} pixels")

if __name__ == '__main__':
    analyze_left_eye("surprised.png")
