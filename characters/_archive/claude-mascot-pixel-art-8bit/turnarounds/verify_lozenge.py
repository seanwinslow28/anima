from PIL import Image

def verify_lozenge(path):
    img = Image.open(path)
    width, height = img.size
    
    # Bounding box coordinates from earlier check
    ymin, ymax = 30, 986
    xmin, xmax = 204, 872
    
    bbox = img.crop((xmin, ymin, xmax + 1, ymax + 1))
    
    # Calculate aspect ratio to resize to 32px height
    aspect = (xmax - xmin + 1) / (ymax - ymin + 1)
    thumb_w = int(32 * aspect)
    thumb_h = 32
    
    # Resize silhouette to thumbnail scale
    thumb = bbox.resize((thumb_w, thumb_h), Image.Resampling.BILINEAR)
    
    print(f"Resized thumbnail dimensions: {thumb_w}x{thumb_h}")
    
    # Render thumbnail silhouette as ASCII art using '.' for background-like pixels and '#' for character pixels
    # Background color is (247, 248, 242)
    bg_ref = (247, 248, 242)
    
    for y in range(thumb_h):
        line = []
        for x in range(thumb_w):
            p = thumb.getpixel((x, y))[:3]
            r, g, b = p
            # Calculate distance to background color
            dist = ((r - bg_ref[0])**2 + (g - bg_ref[1])**2 + (b - bg_ref[2])**2)**0.5
            if dist < 25:
                line.append('.')
            else:
                line.append('#')
        print("".join(line))

if __name__ == '__main__':
    verify_lozenge('body-3quarter.png')
