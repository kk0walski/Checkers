from agents.randomAgent import RandomAgent
from agents.controllingAgent import ControllingAgent
from agents.aggressiveAgent import AgressiveAgent
from config import *
from game import Game
import time


def main():
    for i in range(3):
        game = Game(loop_mode=True)
        game.setup()
        controlling = ControllingAgent(game, RED)
        aggressive = AgressiveAgent(game, BLUE)
        while True:  # main game loop
            if game.state.turn == BLUE:
                # TO start player's turn uncomment the below line and comment a couple  of line below than that
                #game.player_turn()
                new_state = aggressive.step(game.state, True)
                game.state = new_state
                game.update()
            else:
                # TO start player's turn uncomment the below line and comment a couple  of line below than that
                # game.player_turn()
                new_state = controlling.step(game.state, True)
                game.state = new_state
                game.update()
            if game.state.endit:
                game.draw_message()
                break


if __name__ == "__main__":
    main()
    pass
