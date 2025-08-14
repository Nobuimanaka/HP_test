import numpy as np
from PIL import Image, ImageDraw
import random
import os

def create_maze_from_image_with_start_goal(image_path, maze_width, maze_height, threshold=128):
    
    img = Image.open(image_path).convert('L')

    img = img.resize((maze_width, maze_height), Image.Resampling.NEAREST)
    img_array = np.array(img)
    allowed_area = img_array > threshold

    grid_height, grid_width = maze_height * 2 + 1, maze_width * 2 + 1
    maze = np.ones((grid_height, grid_width), dtype=np.uint8)

    for y in range(maze_height):
        for x in range(maze_width):
            if allowed_area[y, x]:
                maze[y * 2 + 1, x * 2 + 1] = 0

    allowed_cells = np.argwhere(allowed_area)
    start_y_img, start_x_img = random.choice(allowed_cells)
    start_gx, start_gy = start_x_img * 2 + 1, start_y_img * 2 + 1

    stack = [(start_gx, start_gy)]
    visited = set([(start_gx, start_gy)])
    
    while stack:
        cx, cy = stack[-1]
        neighbors = []
        for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
            nx, ny = cx + dx, cy + dy
            if 0 < nx < grid_width and 0 < ny < grid_height and (nx, ny) not in visited:
                if allowed_area[(ny - 1) // 2, (nx - 1) // 2]:
                    neighbors.append((nx, ny))
        
        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[(cy + ny) // 2, (cx + nx) // 2] = 0
            visited.add((nx, ny))
            stack.append((nx, ny))
        else:
            stack.pop()

    path_coords = []
    for r, c in np.argwhere(maze == 0):
        if r > 0 and r < grid_height - 1 and c > 0 and c < grid_width - 1:
            img_y, img_x = (r - 1) // 2, (c - 1) // 2
            if allowed_area[img_y, img_x]:
                path_coords.append((r, c))

    if not path_coords:
        print("エラー: 有効な経路が見つかりませんでした。")
        return None

    start_point = random.choice(path_coords)
    
    farthest_dist = -1
    goal_point = None
    for point in path_coords:
        dist = np.sqrt((start_point[0] - point[0])**2 + (start_point[1] - point[1])**2)
        if dist > farthest_dist:
            farthest_dist = dist
            goal_point = point


    maze_rgb = np.zeros((grid_height, grid_width, 3), dtype=np.uint8)
    maze_rgb[maze == 1] = [0, 0, 0]
    maze_rgb[maze == 0] = [255, 255, 255]

    maze_rgb[start_point] = [0, 255, 0]
    if goal_point:
        maze_rgb[goal_point] = [255, 0, 0]

    maze_image = Image.fromarray(maze_rgb)
    return maze_image

if __name__ == '__main__':
    INPUT_IMAGE_PATH = 'input.png'
    OUTPUT_MAZE_PATH = 'generated.png'
    
    MAZE_WIDTH = 50
    MAZE_HEIGHT = 50
    BINARY_THRESHOLD = 200

    print("スタートとゴール付きの迷路を生成しています...")
    generated_maze = create_maze_from_image_with_start_goal(
        image_path=INPUT_IMAGE_PATH, 
        maze_width=MAZE_WIDTH, 
        maze_height=MAZE_HEIGHT,
        threshold=BINARY_THRESHOLD
    )

    if generated_maze:
        generated_maze.save(OUTPUT_MAZE_PATH)
        print(f"🎉 迷路が完成しました！ '{OUTPUT_MAZE_PATH}' として保存しました。")