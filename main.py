import pygame
import random
import tile
import os
import json
from perlin_noise import PerlinNoise


COLS = ROWS = 100
CELL_SIZE = 8
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

MAP_SIZE = (ROWS, COLS)
FOREST_DENSITY = 0.0
WATER_THRESHOLD = 0.0
FOREST_THRESHOLD = 1.0
SEED = None

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

BUTTON_WIDTH = 100
BUTTON_HEIGHT = 30

BUTTON_X = 20
BUTTON_Y = HEIGHT - BUTTON_HEIGHT - 20



def generate_seed(seed: int = None) -> None:
    global SEED
    if seed:
        SEED = seed
    else:
        SEED = random.randint(0, 9999999)

def make_grid(heightmap) -> list:
    width = len(heightmap)
    height = len(heightmap[0])

    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            if heightmap[y][x] < WATER_THRESHOLD:
                row.append(tile.Tile(tile.TileType.WATER, x, y))
            elif heightmap[y][x] > FOREST_THRESHOLD:
                row.append(tile.Tile(tile.TileType.FOREST, x, y))
            else:
                row.append(tile.Tile(tile.TileType.LAND, x, y))
        grid.append(row)

    # num_forests = int(width * height * FOREST_DENSITY)
    # for _ in range(num_forests):
    #     forest_x = random.randint(0, width - 1)
    #     forest_y = random.randint(0, height - 1)
    #     if grid[forest_y][forest_x].type == tile.TileType.LAND:
    #         grid[forest_y][forest_x].set_type(tile.TileType.FOREST)

    return grid
        
def draw_grid(screen, grid):
    for col in grid:
        for cell in col:
            pygame.draw.rect(screen, cell.color, (cell.y * CELL_SIZE, cell.x * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def make_height_map() -> list:
    noise1 = PerlinNoise(octaves=3, seed=SEED)
    noise2 = PerlinNoise(octaves=6, seed=SEED)
    noise3 = PerlinNoise(octaves=12, seed=SEED)
    noise4 = PerlinNoise(octaves=24, seed=SEED)

    xpix, ypix = MAP_SIZE

    pic = []
    for i in range(xpix):
        row = []
        for j in range(ypix):
            noise_val = noise1([i/xpix, j/ypix])
            noise_val += 0.5 * noise2([i/xpix, j/ypix])
            noise_val += 0.25 * noise3([i/xpix, j/ypix])
            noise_val += 0.125 * noise4([i/xpix, j/ypix])

            row.append(noise_val)
        pic.append(row)

    return pic

def draw_toast(screen, message):
    if message is not None:
        toast_font = pygame.font.Font(None, 24)
        toast_text = toast_font.render(message, True, WHITE)  # White text
        toast_rect = toast_text.get_rect(center=(WIDTH // 2, HEIGHT - 30))
        pygame.draw.rect(screen, BLACK, (toast_rect.left - 5, toast_rect.top - 5, toast_rect.width + 10, toast_rect.height + 10))  # Black background
        screen.blit(toast_text, toast_rect)

def save_to_file(grid) -> None:
    new_directory_name = "maps"

    # Get the current working directory
    current_directory = os.getcwd()

    # Path to the new directory
    new_directory_path = os.path.join(current_directory, new_directory_name)

    # Create the directory if it doesn't exist
    if not os.path.exists(new_directory_path):
        os.makedirs(new_directory_path)

    # Path to the JSON file in the new directory
    json_file_path = os.path.join(new_directory_path, f"{SEED}.json")

    data = []

    for rows in grid:
        row = []
        for cell in rows:
            row.append(cell.get_id())
        data.append(row)

    # Save JSON data to the file
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

    print(f"JSON file saved to '{json_file_path}'")


def main():
    pygame.init()
    generate_seed()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2D Grid with Colors")

    height_map = make_height_map()
    grid = make_grid(height_map)
    print(f"Current Seed: {SEED}")

    toast_message = None
    toast_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5:  # Redraw on F5 key press
                    generate_seed()
                    height_map = make_height_map()
                    grid = make_grid(height_map)
                    print(f"New Seed: {SEED}")
                    toast_message = "Refreshed"
                    toast_timer = 60
                elif pygame.key.get_mods() and pygame.KMOD_CTRL and event.key == pygame.K_s :  # Ctrl+S combination
                        save_to_file(grid)
                        toast_message = f"Saved To File: {SEED}"
                        toast_timer = 120


        screen.fill((255, 255, 255))
        draw_grid(screen, grid)
        draw_toast(screen, toast_message)
        if toast_timer > 0:
            toast_timer -= 1
        else:
            toast_message = None  # Clear the toast message
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()