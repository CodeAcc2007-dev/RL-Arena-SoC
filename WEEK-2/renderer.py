import pygame
from constants import *

def draw_grid(screen):
    for col in range(COLS + 1):
        x = col * CELL_SIZE
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for row in range(ROWS + 1):
        y = row * CELL_SIZE
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def draw_player(screen, player):
    row, col = player.pos
    rect = (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, player.color, rect)

def draw_trail(screen, player):
    for row, col in player.trail:
        rect = (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, player.color, rect)