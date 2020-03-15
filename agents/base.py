from config import *


class BasePlayer:
    def __init__(self, game, color):
        self.game = game
        self.color = color
        if self.color == BLUE:
            self.adversary_color = RED
        else:
            self.adversary_color = BLUE

    def step(self, board, return_count_nodes=False):
        pass
