from PIL import Image

def inspect_bottom_dark_pixels(path):
    img = Image.open(path)
    width, height = img.size
    
    print("Inspecting dark pixels with y > 800:")
    for y in range(800, height):
        row_dark = []
        for x in range(width):
            p = img.getpixel((x, y))[:3]
            r, g, b = p
            if r < 110 and g < 75 and b < 50:
                row_dark.append(x)
        if row_dark:
            print(f"Row {y}: {len(row_dark)} dark pixels from x={min(row_dark)} to x={max(row_dark)}")

if __name__ == '__main__':
    inspect_bottom_dark_pixels('body-3quarter.png')
