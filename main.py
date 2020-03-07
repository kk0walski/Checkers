from agents.randomAgent import RandomAgent
from config import *
from game import Game


def main():
    for i in range(3):
        game = Game(loop_mode=True)
        game.setup()
        bot = RandomAgent(game, RED)
        random_bot_blue = RandomAgent(game, BLUE)
        while True:  # main game loop
            if game.turn == BLUE:
                # TO start player's turn uncomment the below line and comment a couple  of line below than that
                # game.player_turn()
                count_nodes = random_bot_blue.step(game.board, True)
                print('Total nodes explored in this step are', count_nodes)
                game.update()
            else:
                # TO start player's turn uncomment the below line and comment a couple  of line below than that
                # game.player_turn()
                count_nodes = bot.step(game.board, True)
                print('Total nodes explored in this step are', count_nodes)
                game.update()
            if game.endit:
                break


if __name__ == "__main__":
    main()
    pass
