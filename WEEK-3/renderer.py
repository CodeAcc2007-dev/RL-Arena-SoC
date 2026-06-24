import pygame
import numpy as np
from constants import WIDTH, HEIGHT, CELL_SIZE

def build_color_array(grid, players):
    # surfarray wants shape (width, height, 3) i.e. (cols, rows, 3) -> transpose grid axes
    colors = np.zeros((grid.shape[1], grid.shape[0], 3), dtype=np.uint8)
    g = grid.T
    for player in players:
        pid = player.id
        territory_mask = g == pid
        trail_mask = g == -pid
        colors[territory_mask] = player.color
        colors[trail_mask] = tuple(c // 2 for c in player.color)  # dimmer for trail
    return colors

def draw_grid_state(screen, grid, players):
    colors = build_color_array(grid, players)
    surf = pygame.surfarray.make_surface(colors)
    surf = pygame.transform.scale(surf, (WIDTH, HEIGHT))
    screen.blit(surf, (0, 0))

def draw_player(screen, player):
    if not player.alive:
        return
    row, col = player.pos
    cx = col * CELL_SIZE + CELL_SIZE // 2
    cy = row * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, player.color, (cx, cy), CELL_SIZE // 2 + 2)
