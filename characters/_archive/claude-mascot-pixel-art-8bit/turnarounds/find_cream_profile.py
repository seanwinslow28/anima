from PIL import Image

def analyze_cream(path):
    img = Image.open(path).convert('RGB')
    width, height = img.size
    
    # Cream highlight target
    cream_target = (244, 221, 184)
    cream_tol = 6
    
    cream_pixels = []
    for y in range(height):
        for x in range(width):
            p = img.getpixel((x, y))
            r, g, b = p
            if abs(r - cream_target[0]) <= cream_tol and \
               abs(g - cream_target[1]) <= cream_tol and \
               abs(b - cream_target[2]) <= cream_tol:
                cream_pixels.append((x, y))
                
    print(f"Total cream pixels in {path}: {len(cream_pixels)}")
    if not cream_pixels:
        return
        
    # Group into contiguous regions
    visited = set()
    clusters = []
    for x, y in cream_pixels:
        if (x, y) not in visited:
            cluster = []
            queue = [(x, y)]
            visited.add((x, y))
            while queue:
                cx, cy = queue.pop(0)
                cluster.append((cx, cy))
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0: continue
                        nx, ny = cx + dx, cy + dy
                        if (nx, ny) in cream_pixels and (nx, ny) not in visited:
                            visited.add((nx, ny))
                            queue.append((nx, ny))
            clusters.append(cluster)
            
    print(f"Found {len(clusters)} cream highlight clusters:")
    # Sort clusters by size descending
    clusters = sorted(clusters, key=len, reverse=True)
    for idx, c in enumerate(clusters[:10]):
        cx_min = min(p[0] for p in c)
        cx_max = max(p[0] for p in c)
        cy_min = min(p[1] for p in c)
        cy_max = max(p[1] for p in c)
        print(f"  Cluster {idx+1}: size={len(c)} pixels (approx {len(c)/1024:.1f} grid units if 32x scaling), bounding box=[({cx_min},{cy_min}) to ({cx_max},{cy_max})]")

if __name__ == '__main__':
    analyze_cream('head-front.png')
