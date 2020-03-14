from config import *


class Board:
    def __init__(self, repr=None):
        if repr:
            self.matrix = self.new_board(repr)
        else:
            self.matrix = self.new_board()

    def new_board(self, board=None):
        """
        Create a new board matrix.
        """

        # initialize squares and place them in matrix

        matrix = [[None] * 8 for i in range(8)]

        # The following code block has been adapted from
        # http://itgirl.dreamhosters.com/itgirlgames/games/Program%20Leaders/ClareR/Checkers/checkers.py
        for x in range(8):
            for y in range(8):
                if (x % 2 != 0) and (y % 2 == 0):
                    matrix[y][x] = Square(BLACK)
                elif (x % 2 != 0) and (y % 2 != 0):
                    matrix[y][x] = Square(WHITE)
                elif (x % 2 == 0) and (y % 2 != 0):
                    matrix[y][x] = Square(BLACK)
                elif (x % 2 == 0) and (y % 2 == 0):
                    matrix[y][x] = Square(WHITE)

        # initialize the pieces and put them in the appropriate squares
        if board == None:
            for x in range(8):
                for y in range(3):
                    if matrix[x][y].color == BLACK:
                        matrix[x][y].occupant = Piece(RED)
                for y in range(5, 8):
                    if matrix[x][y].color == BLACK:
                        matrix[x][y].occupant = Piece(BLUE)
        else:
            for x in range(8):
                for y in range(8):
                    if board[x][y] == 'B' or board[x][y] == 'B:':
                        matrix[x][y].occupant = Piece(BLUE)
                    elif board[x][y] == 'R' or board[x][y] == 'R:':
                        matrix[x][y].occupant = Piece(RED)
                    if board[x][y][-1] == ':':
                        matrix[x][y].occupant.crown()

        return matrix

    def __repr__(self):
        temp_matrix = [['X'] * 8 for _ in range(8)]

        for j in range(8):
            for i in range(8):
                if self.matrix[i][j].occupant is not None:
                    temp_matrix[i][j] = self.matrix[i][j].occupant.__repr__()

        return temp_matrix

    def __str__(self):
        reasult = ""
        for j in range(8):
            for i in range(8):
                reasult += str(self.matrix[i][j])
            reasult += '\n'
        return reasult

    def remove_piece(self, x, y):
        """
		Removes a piece from the board at position (x,y).
		"""
        self.matrix[x][y].occupant = None

    def move_piece(self, start_x, start_y, end_x, end_y):
        """
		Move a piece from (start_x, start_y) to (end_x, end_y).
		"""

        self.matrix[end_x][end_y].occupant = self.matrix[start_x][start_y].occupant
        self.remove_piece(start_x, start_y)

        self.king(end_x, end_y)

    def rel(self, dir, x, y):
        if dir == NORTHWEST:
            return (x - 1, y - 1)
        elif dir == NORTHEAST:
            return (x + 1, y - 1)
        elif dir == SOUTHWEST:
            return (x - 1, y + 1)
        elif dir == SOUTHEAST:
            return (x + 1, y + 1)
        else:
            return 0

    def adjacent(self, x, y):
        """
		Returns a list of squares locations that are adjacent (on a diagonal) to (x,y).
		"""

        return [self.rel(NORTHWEST, x, y), self.rel(NORTHEAST, x, y), self.rel(SOUTHWEST, x, y),
                self.rel(SOUTHEAST, x, y)]

    def location(self, x, y):
        """
		Takes a set of coordinates as arguments and returns self.matrix[x][y]
		This can be faster than writing something like self.matrix[coords[0]][coords[1]]
		"""
        x = int(x)
        y = int(y)
        return self.matrix[x][y]

    def is_end_square(self, coords):
        """
		Is passed a coordinate tuple (x,y), and returns true or
		false depending on if that square on the board is an end square.
		===DOCTESTS===
		>>> board = Board()
		>>> board.is_end_square((2,7))
		True
		>>> board.is_end_square((5,0))
		True
		>>>board.is_end_square((0,5))
		False
		"""

        if coords[1] == 0 or coords[1] == 7:
            return True
        else:
            return False

    def on_board(self, x, y):
        """
		Checks to see if the given square (x,y) lies on the board.
		If it does, then on_board() return True. Otherwise it returns false.
		===DOCTESTS===
		#>>> board = Board()
		#>>> board.on_board((5,0)):
		True
		#>>> board.on_board(-2, 0):
		False
		#>>> board.on_board(3, 9):
		False
		"""

        if x < 0 or y < 0 or x > 7 or y > 7:
            return False
        else:
            return True

    def king(self, x, y):
        """
		Takes in (x,y), the coordinates of square to be considered for kinging.
		If it meets the criteria, then king() kings the piece in that square and kings it.
		"""
        if self.location(x, y).occupant != None:
            if (self.location(x, y).occupant.color == BLUE and y == 0) or (
                    self.location(x, y).occupant.color == RED and y == 7):
                self.location(x, y).occupant.crown()

    def blind_legal_moves(self, x, y):
        """
		Returns a list of blind legal move locations from a set of coordinates (x,y) on the board.
		If that location is empty, then blind_legal_moves() return an empty list.
		"""
        if self.matrix[x][y].occupant != None:

            if self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == BLUE:
                blind_legal_moves = [self.rel(NORTHWEST, x, y), self.rel(NORTHEAST, x, y)]

            elif self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == RED:
                blind_legal_moves = [self.rel(SOUTHWEST, x, y), self.rel(SOUTHEAST, x, y)]

            else:
                blind_legal_moves = [self.rel(NORTHWEST, x, y), self.rel(NORTHEAST, x, y), self.rel(SOUTHWEST, x, y),
                                     self.rel(SOUTHEAST, x, y)]

        else:
            blind_legal_moves = []

        return blind_legal_moves

    def legal_moves(self, x, y, hop=False):
        """
		Returns a list of legal move locations from a given set of coordinates (x,y) on the board.
		If that location is empty, then legal_moves() returns an empty list.
		"""
        # print(x, y)
        blind_legal_moves = self.blind_legal_moves(x, y)
        # print('BLind Legal moves', blind_legal_moves)
        legal_moves = []

        if hop == False:
            for move in blind_legal_moves:
                if hop == False:
                    if self.on_board(move[0], move[1]):
                        if self.location(move[0], move[1]).occupant == None:
                            legal_moves.append(move)

                        elif self.location(move[0], move[1]).occupant.color != self.location(x,
                                                                                             y).occupant.color and self.on_board(
                            move[0] + (move[0] - x), move[1] + (move[1] - y)) and self.location(
                            move[0] + (move[0] - x),
                            move[1] + (move[1] - y)).occupant == None:  # is this location filled by an enemy piece?
                            legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

        else:  # hop == True
            for move in blind_legal_moves:
                if self.on_board(move[0], move[1]) and self.location(move[0], move[1]).occupant != None:
                    if self.location(move[0], move[1]).occupant.color != self.location(x,
                                                                                       y).occupant.color and self.on_board(
                        move[0] + (move[0] - x), move[1] + (move[1] - y)) and self.location(move[0] + (move[0] - x),
                                                                                            move[1] + (move[
                                                                                                           1] - y)).occupant == None:  # is this location filled by an enemy piece?
                        legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

        return legal_moves


class Piece:
    def __init__(self, color, king=False):
        self.color = color
        self.king = king
        self.value = 1

    def crown(self):
        self.king = True
        self.value = 2

    def __repr__(self):
        piece = 'B' if self.color == BLUE else 'R'
        if self.king:
            piece += ':'
        return piece

    def __str__(self):
        piece = ' B' if self.color == BLUE else ' R'
        if self.king:
            piece += ': '
        else:
            piece += ' '
        return piece


class Square:
    def __init__(self, color=WHITE, occupant=None):
        self.color = color  # color is either BLACK or WHITE
        self.occupant = occupant  # occupant is a Square object

    def __repr__(self):
        if self.occupant:
            return self.occupant.__repr__()
        else:
            return 'X'

    def __str__(self):
        if self.occupant:
            return str(self.occupant)
        else:
            return ' X '