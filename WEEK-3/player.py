class Player:
    def __init__(self, row, col, color):
        self.pos = (row, col)
        self.color = color
        self.dir = (1, 0)
        self.alive = True
        self.on_territory = True
        self.start_pos = (row, col)
        self.start_dir = (1, 0)

    def reset(self):
        self.pos = self.start_pos
        self.dir = self.start_dir
        self.alive = True
        self.on_territory = True
