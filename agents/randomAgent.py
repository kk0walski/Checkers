import random

from .base import BasePlayer


class RandomAgent(BasePlayer):
    def __init__(self, game, color):
        BasePlayer.__init__(self, game, color)

    def step(self, state, return_count_nodes=False):
        possible_moves = state.getPossibleActions()
        if possible_moves == []:
            self.game.end_turn()
            return state
        random_move = random.choice(possible_moves)
        new_state = state.takeAction(random_move)
        return new_state
