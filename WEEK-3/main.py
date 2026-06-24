import pygame
from constants import *
from player import Player
from game import Game
from renderer import draw_grid_state, draw_player

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RL Arena - Territory")
clock = pygame.time.Clock()

player1 = Player(20, 20, RED)
player2 = Player(60, 60, BLUE)

game = Game(ROWS, COLS)
game.add_player(player1)
game.add_player(player2)

# dir tuples are (drow, dcol), matching player.pos == (row, col)
actions_wasd = {pygame.K_w: (-1, 0), pygame.K_a: (0, -1),
                pygame.K_s: (1, 0), pygame.K_d: (0, 1)}
actions_arrows = {pygame.K_UP: (-1, 0), pygame.K_DOWN: (1, 0),
                  pygame.K_RIGHT: (0, 1), pygame.K_LEFT: (0, -1)}

font = pygame.font.SysFont(None, 64)

running = True
game_over = False

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in actions_wasd:
                player1.dir = actions_wasd[event.key]
            elif event.key in actions_arrows:
                player2.dir = actions_arrows[event.key]
            elif event.key in (pygame.K_r, pygame.K_SPACE):
                game.reset()
                game_over = False

    if not game_over:
        game.update()
        if not player1.alive or not player2.alive:
            game_over = True

    draw_grid_state(screen, game.grid, game.players)
    for player in game.players:
        draw_player(screen, player)

    if game_over:
        text = font.render("GAME OVER - press R", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    pygame.display.update()

pygame.quit()
