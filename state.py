from board import Board
from config import BLUE, RED, BLACK
from copy import deepcopy

class State:
    def __init__(self, board=None, turn=BLUE, hop=False):
        if board
            self.board = deepcopy(board)
        else:
            self.board = Board()
        self.turn = turn
        self.hop = hop

    def getPossibleActions(self):
        possible_moves = []
        for i in range(8):
            for j in range(8):
                if (self.board.legal_moves(i, j, self.game.hop) != []
                        and self.board.location(i, j).occupant is not None
                        and self.board.location(i, j).occupant.color == self.game.turn):
                    for end_pos in self.board.legal_moves(i, j, self.game.hop):
                        possible_moves.append(Action((i,j), end_pos))
        return possible_moves

    def takeAction(self, action):
        current_pos = action.current_pos
        final_pos = action.final_pos
        if current_pos is None:
            self.end_turn()
            print(str(self.board))
            # print(self._generate_all_possible_moves(board))
        print(current_pos, final_pos, self.board.location(current_pos[0], current_pos[1]).occupant)
        if not self.hop:
            if self.board.location(final_pos[0], final_pos[1]).occupant is not None \
                    and self.board.location(final_pos[0], final_pos[1]).occupant.color == self.turn:
                current_pos = final_pos

            elif current_pos is not None and final_pos in self.board.legal_moves(current_pos[0], current_pos[1]):

                self.board.move_piece(
                    current_pos[0], current_pos[1], final_pos[0], final_pos[1])

                if final_pos not in self.board.adjacent(current_pos[0], current_pos[1]):
                    self.board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) //
                                       2, current_pos[1] + (final_pos[1] - current_pos[1]) // 2)
                    self.hop = True
                    current_pos = final_pos
                    final_pos = self.board.legal_moves(current_pos[0], current_pos[1], True)
                    if final_pos:
                        print("HOP in Action", current_pos, final_pos)
                        self.takeAction(current_pos, final_pos[0])
                    self.end_turn()

            new_state = deepcopy(self)
            return new_state


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
            print(self.turn)


class PlayerState(State):
    def __init__(self, board=None, turn=BLUE, hop=False, color=BLUE):
        super.__init__(board, turn, hop)
        self.color = color

    def getReward(self):
        if self.turn == self.color:
            return 1
        else:
            return -1

class Action:
    def __init__(self, start_pos, end_pos):
        self.current_pos = start_pos
        self.final_pos = end_pos