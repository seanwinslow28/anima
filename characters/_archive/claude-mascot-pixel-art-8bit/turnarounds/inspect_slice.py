from PIL import Image

def inspect_slice(path):
    img = Image.open(path).convert('RGB')
    width, height = img.size
    print(f"Slice from {path}:")
    for y in range(15):
        row_colors = []
        for x in range(350, 380):
            p = img.getpixel((x, y))
            hex_color = '#{:02x}{:02x}{:02x}'.format(*p)
            row_colors.append(hex_color)
        print(f"y={y:2d}: " + " ".join(row_colors[:10]) + " ... " + " ".join(row_colors[-10:]))

if __name__ == '__main__':
    inspect_slice('head-front.png')
