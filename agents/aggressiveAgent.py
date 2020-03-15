import sys
from config import *
from .base import BasePlayer
from copy import deepcopy

class AgressiveAgent(BasePlayer):
    def __init__(self, game, color):
        BasePlayer.__init__(self, game, color)
        self.eval_color = color

    def step(self, state, return_count_nodes=False):
        return self.policy(state)

    def policy(self, state):
        bestFound = None
        bestFoundValue = -sys.maxsize - 1
        for action in state.getPossibleActions():
            copy_action = deepcopy(action)
            new_state = state.takeAction(copy_action)
            currentValue = self.evaluate(new_state.board)
            if currentValue > bestFoundValue:
                bestFound = action
                bestFoundValue = currentValue

        print(str(self.color) + " " + str(bestFound))
        new_state = state.takeAction(bestFound)
        return new_state


    def evaluate(self, board):
        score = 0
        if (self.eval_color == RED):
            for i in range(8):
                for j in range(8):
                    occupant = board.location(i, j).occupant
                    if (occupant is not None):
                        if occupant.color == self.eval_color:
                            score += 5 + j + 5 * (occupant.king)
                        else:
                            score -= 20 + (8 - j) + 2 * (occupant.king)
        else:
            for i in range(8):
                for j in range(8):
                    occupant = board.location(i, j).occupant
                    if (occupant is not None):
                        if occupant.color == self.eval_color:
                            score += 5 + (8 - j) + 5 * (occupant.king)
                        else:
                            score -= 20 + j + 2 * (occupant.king)
        return score