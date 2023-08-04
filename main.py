import pygame
import random
import tile
from perlin_noise import PerlinNoise


COLS = ROWS = 100
CELL_SIZE = 10
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

MAP_SIZE = (ROWS, COLS)
FOREST_DENSITY = 0.0
WATER_THRESHOLD = 0.0
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
            else:
                row.append(tile.Tile(tile.TileType.LAND, x, y))
        grid.append(row)

    num_forests = int(width * height * FOREST_DENSITY)
    for _ in range(num_forests):
        forest_x = random.randint(0, width - 1)
        forest_y = random.randint(0, height - 1)
        if grid[forest_y][forest_x].type == tile.TileType.LAND:
            grid[forest_y][forest_x].set_type(tile.TileType.FOREST)

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


def save_to_file() -> None:
    pass


def main():
    pygame.init()

    # Create a window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2D Grid with Colors")

    height_map = make_height_map()
    grid = make_grid(height_map)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        draw_grid(screen, grid)
        pygame.display.flip() 

    pygame.quit()

if __name__ == "__main__":
    main()