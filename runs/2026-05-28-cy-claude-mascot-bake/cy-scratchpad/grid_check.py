import sys
from PIL import Image

def analyze_grid_and_pixels(path):
    im = Image.open(path).convert('RGB')
    width, height = im.size
    
    # White background check: let's assume background is white #FFFFFF
    # Find bounding box of non-white pixels (or pixels that are not close to white)
    non_white_pixels = []
    min_x, min_y = width, height
    max_x, max_y = -1, -1
    
    for y in range(height):
        for x in range(width):
            r, g, b = im.getpixel((x, y))
            # If not white
            if not (r > 240 and g > 240 and b > 240):
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)
    
    print(f"Character bounding box: x in [{min_x}, {max_x}], y in [{min_y}, {max_y}]")
    print(f"Bounding box dimensions: {max_x - min_x + 1} x {max_y - min_y + 1}")
    
    # Let's inspect a horizontal slice across the face/body to see if there are constant blocks of pixels.
    # We will compute the GCD of run-lengths of identical colors along rows/columns,
    # or look at the Fourier transform / auto-correlation to find if there is a grid cell size.
    # Alternatively, let's just print a small 20x20 grid from the center of the bounding box to see the pixel structure.
    cx = (min_x + max_x) // 2
    cy = (min_y + max_y) // 2
    print(f"Center: ({cx}, {cy})")
    
    print("Colors around center (20x20):")
    for y in range(cy - 10, cy + 10):
        row_str = ""
        for x in range(cx - 10, cx + 10):
            r, g, b = im.getpixel((x, y))
            # Format as short hex
            row_str += '#{:02x}{:02x}{:02x} '.format(r, g, b)
        # We won't print the whole grid if it's too long, but let's print a summary of how many unique colors there are in this 20x20 area
        # and see if there are many intermediate colors.
        
    # Let's count run lengths of identical or very similar colors.
    # If it is scaled up pixel art, we will see long runs of identical colors.
    # Let's compute run lengths of identical colors on rows inside the bounding box.
    run_lengths = []
    for y in range(min_y, max_y + 1):
        current_color = None
        current_run = 0
        for x in range(min_x, max_x + 1):
            color = im.getpixel((x, y))
            if color == current_color:
                current_run += 1
            else:
                if current_run > 0:
                    run_lengths.append(current_run)
                current_color = color
                current_run = 1
        if current_run > 0:
            run_lengths.append(current_run)
            
    # Find minimum and common run lengths
    run_lengths = [r for r in run_lengths if r > 1]
    if run_lengths:
        import collections
        counter = collections.Counter(run_lengths)
        print("Most common run lengths of identical pixels along rows:")
        print(counter.most_common(10))
    else:
        print("No run lengths > 1 found. It's likely not scaled up pixel art or has heavy anti-aliasing.")

if __name__ == '__main__':
    analyze_grid_and_pixels("surprised.png")
