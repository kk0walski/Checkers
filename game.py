import sys

import pygame

from board import Board
from config import BLUE, RED, BLACK
from graphic import Graphics


class Game:
    """
    The main game control.
    """

    def __init__(self, loop_mode):
        self.graphics = Graphics()
        self.board = Board()
        self.endit = False
        self.turn = BLUE
        self.selected_piece = None  # a board location.
        self.hop = False
        self.loop_mode = loop_mode
        self.selected_legal_moves = []

    def setup(self):
        """Draws the window and board at the beginning of the game"""
        self.graphics.setup_window()

    def player_turn(self):
        """
        The event loop. This is where events are triggered
        (like a mouse click) and then effect the game state.
        """
        mouse_pos = tuple(map(int, pygame.mouse.get_pos()))
        self.mouse_pos = tuple(map(int, self.graphics.board_coords(
            mouse_pos[0], mouse_pos[1])))  # what square is the mouse in?
        if self.selected_piece != None:
            self.selected_legal_moves = self.board.legal_moves(
                self.selected_piece[0], self.selected_piece[1], self.hop)
            # print("selected_legal_moves: ", self.selected_legal_moves)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.terminate_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(self.hop)
                if self.hop == False:
                    if self.board.location(self.mouse_pos[0],
                                           self.mouse_pos[1]).occupant != None and self.board.location(
                        self.mouse_pos[0], self.mouse_pos[1]).occupant.color == self.turn:
                        self.selected_piece = self.mouse_pos

                    elif self.selected_piece != None and self.mouse_pos in self.board.legal_moves(
                            self.selected_piece[0], self.selected_piece[1]):

                        self.board.move_piece(
                            self.selected_piece[0], self.selected_piece[1], self.mouse_pos[0], self.mouse_pos[1])

                        if self.mouse_pos not in self.board.adjacent(self.selected_piece[0], self.selected_piece[1]):
                            self.board.remove_piece(
                                self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) // 2,
                                self.selected_piece[1] + (
                                        self.mouse_pos[1] - self.selected_piece[1]) // 2)

                            self.hop = True
                            self.selected_piece = self.mouse_pos
                        else:
                            self.end_turn()

                if self.hop == True:
                    if self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece[0],
                                                                                                self.selected_piece[1],
                                                                                                self.hop):
                        self.board.move_piece(
                            self.selected_piece[0], self.selected_piece[1], self.mouse_pos[0], self.mouse_pos[1])
                        self.board.remove_piece(self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) //
                                                2, self.selected_piece[1] + (
                                                        self.mouse_pos[1] - self.selected_piece[1]) // 2)

                    if self.board.legal_moves(self.mouse_pos[0], self.mouse_pos[1], self.hop) == []:
                        self.end_turn()

                    else:
                        self.selected_piece = self.mouse_pos

    def update(self):
        """Calls on the graphics class to update the game display."""
        self.graphics.update_display(
            self.board, self.selected_legal_moves, self.selected_piece)

    def terminate_game(self):
        """Quits the program and ends the game."""
        pygame.quit()
        sys.exit()

    def main(self):
        """"This executes the game and controls its flow."""
        self.setup()

        while True:  # main game loop
            self.player_turn()
            self.update()

    def end_turn(self):
        """
        End the turn. Switches the current player.
        end_turn() also checks for and game and resets a lot of class attributes.
        """
        if self.turn == BLUE:
            self.turn = RED
        else:
            self.turn = BLUE

        self.selected_piece = None
        self.selected_legal_moves = []
        self.hop = False

        if self.check_for_endgame():
            if self.turn == BLUE:
                print('RED WINS!')
                self.graphics.draw_message("RED WINS!")
            else:
                print('BLUE WINS!')
                self.graphics.draw_message("BLUE WINS!")
            print(self.turn)
            if (self.loop_mode):
                self.endit = True
            else:
                self.terminate_game()

    def check_for_endgame(self):
        """
        Checks to see if a player has run out of moves or pieces. If so, then return True. Else return False.
        """
        for x in range(8):
            for y in range(8):
                if self.board.location(x, y).color == BLACK and self.board.location(x,
                                                                                    y).occupant != None and self.board.location(
                    x, y).occupant.color == self.turn:
                    if self.board.legal_moves(x, y) != []:
                        return False

        return True
