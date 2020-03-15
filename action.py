from config import BLUE, RED, BLACK

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