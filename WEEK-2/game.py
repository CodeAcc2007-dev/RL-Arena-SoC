from constants import *
import numpy as np

class Game:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)
        self.players = []

    def add_player(self, player):
        row, col = player.pos
        player_id = len(self.players) +1
        player.id = player_id
        self.grid[row, col] = player_id
        self.players.append(player)


    def update(self):
        # 1. compute next position for every alive player (based on OLD state only)
        next_positions = []
        for player in self.players:
            if not player.alive:
                next_positions.append(player.pos)
                continue
            row, col = player.pos
            drow, dcol = player.dir
            next_positions.append((row + drow, col + dcol))

        # 2. head-on collision: two alive players landing on the same next cell -> both die
        for i in range(len(self.players)):
            for j in range(i + 1, len(self.players)):
                p1, p2 = self.players[i], self.players[j]
                if p1.alive and p2.alive and next_positions[i] == next_positions[j]:
                    p1.alive = False
                    p2.alive = False

        # 3. wall + trail collision for everyone still alive after step 2
        for i, player in enumerate(self.players):
            if not player.alive:
                continue
            row, col = next_positions[i]
            if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
                player.alive = False
                continue
            if self.grid[row, col] != 0:
                player.alive = False

        # 4. move every player who survived steps 2 and 3
        for i, player in enumerate(self.players):
            if not player.alive:
                continue
            player.trail.append(player.pos)
            player.pos = next_positions[i]
            self.grid[player.pos] = player.id

    def reset(self):
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        for player in self.players:
            player.reset()
            row, col = player.pos
            self.grid[row, col] = player.id