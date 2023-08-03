import pygame
import random
import tile


ROWS = 100
COLS = 100
CELL_SIZE = 10
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# Colors for each cell (you can modify this as per your choice)
cell_colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(ROWS * COLS)]

def make_grid2(rows, cols) -> list:

    grid = []
    for x in range(rows):
        row = []
        for y in range(cols):
            new_type = random.randint(0, 1)
            #print(new_type)
            if new_type == 0:
                new_tile = tile.Tile(tile.TileType.LAND, x, y)
            else: #1
                new_tile = tile.Tile(tile.TileType.WATER,x ,y)
            row.append(new_tile)

        grid.append(row)

    return grid

def make_grid(rows, cols) -> list:
    grid = []
    for x in range(rows):
        row = []
        for y in range(cols):
            row.append(tile.Tile(tile.TileType.WATER, x, y))
        grid.append(row)

    # Starting point for the island
    islands = 5
    x = 0
    while x < islands:
        start_x = random.randint(0, rows - 1)
        start_y = random.randint(0, cols - 1)

        # Perform Random Walk to create the island
        stack = [(start_x, start_y)]
        grid[start_x][start_y] = tile.Tile(tile.TileType.LAND, start_x, start_y)

        while stack:
            x, y = stack.pop()
            # Randomly select one of the neighbors to explore
            neighbors = [(x + dx, y + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
            random.shuffle(neighbors)
            for nx, ny in neighbors:
                if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny].type == tile.TileType.WATER:
                    grid[nx][ny] = tile.Tile(tile.TileType.LAND, nx, ny)
                    stack.append((nx, ny))
                    x = x + 1
                    break  # Stop exploring neighbors once we find a valid one


    return grid
        

# Function to draw the grid
def draw_grid(screen, grid):
    for col in grid:
        for cell in col:
            pygame.draw.rect(screen, cell.color, (cell.y * CELL_SIZE, cell.x * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Main function
def main():
    pygame.init()

    # Create a window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2D Grid with Colors")

    grid = make_grid(ROWS, COLS)

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