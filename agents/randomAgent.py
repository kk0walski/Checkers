import random

from .base import BasePlayer


class RandomAgent(BasePlayer):
    def __init__(self, game, color):
        BasePlayer.__init__(self, game, color)

    def step(self, board, return_count_nodes=False):
        possible_moves = self._generate_all_possible_moves(board)
        if possible_moves == []:
            self.game.end_turn()
            return
        random_move = random.choice(possible_moves)
        rand_choice = random.choice(random_move[2])
        self._action(random_move, rand_choice, board)
        if return_count_nodes:
            return 0
