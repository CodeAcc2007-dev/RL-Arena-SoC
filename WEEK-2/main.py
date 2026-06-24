import pygame
from constants import *
from player import Player
from game import Game
from renderer import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RL Arena")
clock = pygame.time.Clock()

player1 = Player(5, 5, RED)
player2 = Player(15, 15, BLUE)

game = Game(ROWS, COLS)
game.add_player(player1)
game.add_player(player2)

# Original skeleton used (dx, dy) screen-pixel pairs here, but game.py's update()
# expects player.dir as (drow, dcol) to match player.pos == (row, col), so the
# values below were changed. Original:
# actions_wasd = {pygame.K_w: (0, -1), pygame.K_a: (-1, 0),
#                 pygame.K_s: (0, 1), pygame.K_d: (1, 0)}
# actions_arrows = {pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1),
#                   pygame.K_RIGHT: (1, 0), pygame.K_LEFT: (-1, 0)}
actions_wasd = {pygame.K_w: (-1, 0), pygame.K_a: (0, -1),
                pygame.K_s: (1, 0), pygame.K_d: (0, 1)}
actions_arrows = {pygame.K_UP: (-1, 0), pygame.K_DOWN: (1, 0),
                  pygame.K_RIGHT: (0, 1), pygame.K_LEFT: (0, -1)}

font = pygame.font.SysFont(None, 64)

running = True
game_over = False

while running:
    clock.tick(FPS)

    # Handle quit event
    # Read keyboard, update player directions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in actions_wasd:
                player1.dir = actions_wasd[event.key]
            elif event.key in actions_arrows:
                player2.dir = actions_arrows[event.key]

    # Call game.update()
    # If anyone died, change game_over var
    if not game_over:
        game.update()
        if not player1.alive or not player2.alive:
            game_over = True

    # Draw everything
    screen.fill(BACKGROUND_COLOR)
    draw_grid(screen)
    for player in game.players:
        draw_trail(screen, player)
        draw_player(screen, player)

    # If game over, render text on top
    if game_over:
        text = font.render("GAME OVER", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    pygame.display.update()

pygame.quit()