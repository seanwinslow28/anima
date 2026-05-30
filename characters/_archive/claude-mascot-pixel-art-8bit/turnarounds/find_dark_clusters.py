from PIL import Image

def find_dark_clusters(path):
    img = Image.open(path)
    width, height = img.size
    
    # Let's count dark pixels in each row
    rows_with_dark = []
    for y in range(height):
        count = 0
        for x in range(width):
            p = img.getpixel((x, y))[:3]
            r, g, b = p
            if r < 110 and g < 75 and b < 50:
                count += 1
        if count > 0:
            rows_with_dark.append((y, count))
            
    print(f"Total rows with dark pixels: {len(rows_with_dark)}")
    if not rows_with_dark:
        return
        
    print(f"First row with dark pixels: y={rows_with_dark[0][0]} (count {rows_with_dark[0][1]})")
    print(f"Last row with dark pixels: y={rows_with_dark[-1][0]} (count {rows_with_dark[-1][1]})")
    
    # Let's print rows in clusters to see where they are
    # Typically we will have a cluster for the face (eyes, mouth) and then a cluster for the outlines/feet
    print("\nDark pixel row clusters:")
    # We can group contiguous rows
    clusters = []
    current_cluster = [rows_with_dark[0]]
    for item in rows_with_dark[1:]:
        y, count = item
        last_y = current_cluster[-1][0]
        if y - last_y <= 2:
            current_cluster.append(item)
        else:
            clusters.append(current_cluster)
            current_cluster = [item]
    clusters.append(current_cluster)
    
    for i, cl in enumerate(clusters):
        start_y = cl[0][0]
        end_y = cl[-1][0]
        total_p = sum(item[1] for item in cl)
        print(f"Cluster {i+1}: y={start_y} to y={end_y} (height {end_y - start_y + 1} px, total dark pixels: {total_p})")

if __name__ == '__main__':
    find_dark_clusters('body-3quarter.png')
