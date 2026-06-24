import numpy as np
from constants import TERRITORY_RADIUS
from capture import capture_territory

class Game:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)
        self.players = []

    def add_player(self, player):
        player_id = len(self.players) + 1
        player.id = player_id
        self.players.append(player)
        self._stamp_territory(player)

    def _stamp_territory(self, player):
        row, col = player.start_pos
        r0, r1 = max(0, row - TERRITORY_RADIUS), min(self.rows, row + TERRITORY_RADIUS + 1)
        c0, c1 = max(0, col - TERRITORY_RADIUS), min(self.cols, col + TERRITORY_RADIUS + 1)
        self.grid[r0:r1, c0:c1] = player.id

    def update(self):
        for player in self.players:
            if not player.alive:
                continue

            row, col = player.pos
            drow, dcol = player.dir
            nrow, ncol = row + drow, col + dcol

            if nrow < 0 or nrow >= self.rows or ncol < 0 or ncol >= self.cols:
                continue  # blocked: out of bounds

            target = self.grid[nrow, ncol]

            if target > 0 and target != player.id:
                continue  # blocked: opponent territory

            if target == -player.id:
                player.alive = False  # death: own trail
                continue

            if target < 0 and target != -player.id:
                victim_id = -target  # cutting an opponent's trail kills them
                for other in self.players:
                    if other.id == victim_id:
                        other.alive = False

            player.pos = (nrow, ncol)

            if target == player.id:
                if not player.on_territory:
                    capture_territory(self.grid, player.id, self.rows, self.cols)
                player.on_territory = True
            else:
                player.on_territory = False
                self.grid[nrow, ncol] = -player.id

    def reset(self):
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        for player in self.players:
            player.reset()
            self._stamp_territory(player)
