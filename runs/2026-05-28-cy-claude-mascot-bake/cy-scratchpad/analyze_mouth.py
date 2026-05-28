from PIL import Image

def analyze_mouth(path):
    im = Image.open(path).convert('RGB')
    # Bounding box of mouth: x in [461, 562], y in [436, 536]
    colors = {}
    for y in range(436, 537):
        for x in range(461, 563):
            color = im.getpixel((x, y))
            colors[color] = colors.get(color, 0) + 1
            
    print("Unique colors in the mouth region:")
    sorted_colors = sorted(colors.items(), key=lambda x: x[1], reverse=True)
    for c, count in sorted_colors[:15]:
        hex_color = '#{:02x}{:02x}{:02x}'.format(*c)
        print(f"  {hex_color} : {count} pixels")

if __name__ == '__main__':
    analyze_mouth("surprised.png")
