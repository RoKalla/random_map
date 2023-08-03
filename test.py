def create_dynamic_grid(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]

def print_grid(grid):
    for row in grid:
        print(" ".join(str(cell) for cell in row))

# Example: Create a dynamic grid with user-specified size and print it
rows = int(input("Enter the number of rows: "))
cols = int(input("Enter the number of columns: "))
grid = create_dynamic_grid(rows, cols)

print_grid(grid)