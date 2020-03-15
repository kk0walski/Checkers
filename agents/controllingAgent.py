import sys
from config import *
from .base import BasePlayer
from copy import deepcopy

class ControllingAgent(BasePlayer):
    def __init__(self, game, color):
        BasePlayer.__init__(self, game, color)
        self.eval_color = color

    def step(self, state, return_count_nodes=False):
        return self.policy(state)

    def policy(self, state):
        bestFound = None
        bestFoundValue = -sys.maxsize - 1
        for action in state.getPossibleActions():
            new_state = state.takeAction(action)
            currentValue = self.evaluate(new_state.board)
            if currentValue > bestFoundValue:
                bestFound = action
                bestFoundValue = currentValue

        print(str(self.color) + " " + str(bestFound))
        new_state = state.takeAction(bestFound)
        return new_state

    def evaluate(self, board):
        score = 0
        num_pieces = 0
        if (self.eval_color == RED):
            for i in range(8):
                for j in range(8):
                    occupant = board.location(i, j).occupant
                    if (occupant is not None):
                        num_pieces += 1
                        if occupant.color == self.eval_color and occupant.king:
                            score += 10
                        elif occupant.color != self.eval_color and occupant.king:
                            score -= 10
                        elif occupant.color == self.eval_color and j < 4:
                            score += 5
                        elif occupant.color != self.eval_color and j < 4:
                            score -= 7
                        elif occupant.color == self.eval_color and j >= 4:
                            score += 7
                        elif occupant.color != self.eval_color and j >= 4:
                            score -= 5
        else:
            for i in range(8):
                for j in range(8):
                    occupant = board.location(i, j).occupant
                    if (occupant is not None):
                        num_pieces += 1
                        if occupant.color == self.eval_color and occupant.king:
                            score += 10
                        elif occupant.color != self.eval_color and occupant.king:
                            score -= 10
                        elif occupant.color == self.eval_color and j < 4:
                            score += 7
                        elif occupant.color != self.eval_color and j < 4:
                            score -= 5
                        elif occupant.color == self.eval_color and j >= 4:
                            score += 7
                        elif occupant.color != self.eval_color and j >= 4:
                            score -= 5
        return score / num_pieces