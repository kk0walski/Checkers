from board import Board
from config import BLUE, RED, BLACK
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

class Action:
    def __init__(self, start_pos, end_pos):
        self.current_pos = start_pos
        self.final_pos = end_pos

    def perform(self, state):
        self._action(self.current_pos, self.final_pos, state)
        if not state.hop:
            state.turn = RED if state.turn == BLUE else BLUE

    def _action(self, current_pos, final_pos, state):
        if current_pos is None:
            state.end_turn()
            # state.board.repr_matrix()
            # print(self._generate_all_possible_moves(state.board))
            # print(current_pos, final_pos, state.board.location(current_pos[0], current_pos[1]).occupant)
        if state.hop == False:
            if state.board.location(final_pos[0], final_pos[1]).occupant != None \
                    and state.board.location(final_pos[0], final_pos[1]).occupant.color == state.turn:
                current_pos = final_pos

            elif current_pos != None and final_pos in state.board.legal_moves(current_pos[0], current_pos[1]):

                state.board.move_piece(
                    current_pos[0], current_pos[1], final_pos[0], final_pos[1])

                if final_pos not in state.board.adjacent(current_pos[0], current_pos[1]):
                    state.board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) //
                                             2, current_pos[1] + (final_pos[1] - current_pos[1]) // 2)

                    state.hop = True
                    current_pos = final_pos
                    final_pos = state.board.legal_moves(
                        current_pos[0], current_pos[1], True)
                    if final_pos != []:
                        # print("HOP in Action", current_pos, final_pos)
                        self._action(current_pos, final_pos[0], state)
                    state.end_turn()

        if state.hop == True:
            if current_pos != None and final_pos in state.board.legal_moves(current_pos[0], current_pos[1],
                                                                            state.hop):
                state.board.move_piece(
                    current_pos[0], current_pos[1], final_pos[0], final_pos[1])
                state.board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) //
                                         2, current_pos[1] + (final_pos[1] - current_pos[1]) // 2)

            if state.board.legal_moves(final_pos[0], final_pos[1], state.hop) == []:
                state.end_turn()
            else:
                current_pos = final_pos
                final_pos = state.board.legal_moves(
                    current_pos[0], current_pos[1], True)
                if final_pos != []:
                    # print("HOP in Action", current_pos, final_pos)
                    self._action(current_pos, final_pos[0], state)
                state.end_turn()

    def __str__(self):
        reasult = ""
        reasult += "curent_pos: " + str(self.current_pos) + "  \n"
        reasult += "final pos: " + str(self.final_pos) + " \n"
        return reasult

    def __repr__(self):
        return {'current_pos': self.current_pos, 'final_pos': self.final_pos}