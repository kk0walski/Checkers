import unittest
from config import *
from board import Board, Square

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.new_board = Board()

    def test_str(self):
        new_board_string = ''
        new_board_string += " X  R  X  R  X  R  X  R \n"
        new_board_string += " R  X  R  X  R  X  R  X \n"
        new_board_string += ' X  R  X  R  X  R  X  R \n'
        new_board_string += ' X  X  X  X  X  X  X  X \n'
        new_board_string += ' X  X  X  X  X  X  X  X \n'
        new_board_string += ' B  X  B  X  B  X  B  X \n'
        new_board_string += ' X  B  X  B  X  B  X  B \n'
        new_board_string += ' B  X  B  X  B  X  B  X \n'
        assert new_board_string == self.new_board.__str__()

    def __test_repr(self):
        assert self.new_board.matrix == self.new_board.new_board()
        temp_matrix = [['X'] * 8 for _ in range(8)]
        for i in range(8):
            for j in range(8):
                if self.new_board.matrix[i][j].occupant != None:
                    if self.new_board.matrix[i][j].occupant.color == RED:
                        temp_matrix[i][j] == 'R'
                    elif self.new_board.matrix[i][j].occupant.color == BLUE:
                        temp_matrix[i][j] == 'B'
        assert temp_matrix == self.new_board.__repr__()

    def test_on_board(self):
        for i in range(8):
            for j in range(8):
                assert self.new_board.on_board(i,j)
        assert self.new_board.on_board(-2,0) == False
        assert self.new_board.on_board(3,9) == False

    def test_end_square(self):
        for i in range(8):
            for j in range(8):
                if j == 0 or j == 7:
                    assert self.new_board.is_end_square((i, j))
                else:
                    assert self.new_board.is_end_square((i, j)) == False

    def test_location(self):
        temp_matrix = self.new_board.matrix
        assert len(temp_matrix) == 8
        for i in range(8):
            for j in range(8):
                assert temp_matrix[i][j] == self.new_board.location(i,j)

    def test_adjacent(self):
        for i in range(8):
            for j in range(8):
                self.new_board.adjacent(i,j) == [self.new_board.rel(NORTHWEST, i, j),
                                                 self.new_board.rel(NORTHEAST, i, j),
                                                 self.new_board.rel(SOUTHWEST, i, j),
                                                 self.new_board.rel(SOUTHEAST, i, j)]

    def test_blind_legal_moves(self):
        for x in range(8):
            for y in range(8):
                if self.new_board.matrix[x][y].occupant != None:
                    if self.new_board.matrix[x][y].occupant.color  == BLUE:
                        assert self.new_board.blind_legal_moves(x,y) == [self.new_board.rel(NORTHWEST, x, y), self.new_board.rel(NORTHEAST, x, y)]
                    if self.new_board.matrix[x][y].occupant.color  == RED:
                        assert self.new_board.blind_legal_moves(x,y) == [self.new_board.rel(SOUTHWEST, x, y), self.new_board.rel(SOUTHEAST, x, y)]
                else:
                    assert self.new_board.blind_legal_moves(x, y) == []

    def test_rel(self):
        for i in range(8):
            for j in range(8):
                assert self.new_board.rel(NORTHWEST, i, j) == (i - 1, j - 1)
                assert self.new_board.rel(NORTHEAST, i, j) == (i + 1, j - 1)
                assert self.new_board.rel(SOUTHWEST, i, j) == (i - 1, j + 1)
                assert self.new_board.rel(SOUTHEAST, i, j) == (i + 1, j + 1)
                assert self.new_board.rel(FALSEREL, i, j) == 0

if __name__ == '__main__':
    unittest.main()
