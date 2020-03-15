from board import Board
from config import BLUE, RED, BLACK
from action import Action
from copy import deepcopy

class State:
    def __init__(self, board=None, turn=BLUE, hop=False, loop_mode=False, endit=False):
        if board:
            self.board = deepcopy(board)
        else:
            self.board = Board()
        self.turn = turn
        self.hop = hop
        self.loop_mode = loop_mode
        self.endit = endit

    def getPossibleActions(self):
        possible_moves = []
        for i in range(8):
            for j in range(8):
                if (self.board.legal_moves(i, j, self.hop) != []
                        and self.board.location(i, j).occupant is not None
                        and self.board.location(i, j).occupant.color == self.turn):
                    for end_pos in self.board.legal_moves(i, j, self.hop):
                        possible_moves.append(Action((i,j), end_pos))
        return possible_moves

    def takeAction(self, action):
        newState = deepcopy(self)
        action.perform(newState)
        return newState



    def isTerminal(self):
        for x in range(8):
            for y in range(8):
                if self.board.location(x, y).color == BLACK and \
                        self.board.location(x, y).occupant is not None and \
                        self.board.location(x, y).occupant.color == self.turn:
                    if self.board.legal_moves(x, y):
                        return False

        return True

    def end_turn(self):
        """
        End the turn. Switches the current player.
        end_turn() also checks for and game and resets a lot of class attributes.
        """
        if self.turn == BLUE:
            self.turn = RED
        else:
            self.turn = BLUE

        self.hop = False
        if self.isTerminal():
            if self.turn == BLUE:
                print('RED WINS!')
            else:
                print('BLUE WINS!')
            if self.loop_mode:
                self.endit = True

class PlayerState(State):
    def __init__(self, board=None, turn=BLUE, hop=False, color=BLUE):
        super.__init__(board, turn, hop)
        self.color = color

    def getReward(self):
        if self.turn == self.color:
            return 1
        else:
            return -1