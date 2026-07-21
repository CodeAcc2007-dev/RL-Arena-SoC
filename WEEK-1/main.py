from constants import *
from utils import *

# Player starting position
player_row = 0
player_col = 0

# Obstacles represented as a list of (row, col) tuples
obstacles = [(1, 1), (1, 2), (2, 5)]

running = True

while running:
    # 1. Reset grid to empty cells
    grid = [[EMPTY_CELL for _ in range(COLS)] for _ in range(ROWS)]

    # 2. Add obstacles to grid
    for ob_r, ob_c in obstacles:
        grid[ob_r][ob_c] = OBSTACLE_CELL

    # 3. Place player on grid
    grid[player_row][player_col] = PLAYER_CELL

    # 4. Display the grid (assumes print_grid in utils.py)
    print_grid(grid)

    # 5. Take user input
    action = input("Move (W/A/S/D or Q to quit): ").strip().lower()

    if action == 'q':
        print("Game Over!")
        running = False
        break

    # Determine position shift (delta) based on input
    dr, dc = 0, 0
    if action == 'w':
        dr = -1
    elif action == 's':
        dr = 1
    elif action == 'a':
        dc = -1
    elif action == 'd':
        dc = 1
    else:
        print("Invalid input! Use W, A, S, D, or Q.")
        continue

    # Compute candidate coordinates
    new_row = player_row + dr
    new_col = player_col + dc

    # 6. Boundary Checking
    if not (0 <= new_row < ROWS and 0 <= new_col < COLS):
        print("Invalid Move: Out of Bounds!")
        continue

    # 7. Obstacle Collision Checking
    if (new_row, new_col) in obstacles:
        print("Invalid Move: Hit an Obstacle!")
        continue

    # 8. Update position if all checks pass
    player_row = new_row
    player_col = new_col
