from .mcts import mcts
from .base import BasePlayer
from state import MCTSState


class MctsAgent(BasePlayer):
    def __init__(self, game, color):
        BasePlayer.__init__(self, game, color)
        self.eval_color = color

    def step(self, state, return_count_nodes=False):
        mctsAI = mcts(timeLimit=20000)
        playerState = MCTSState(state, self.eval_color)
        bestAction = mctsAI.search(initialState=playerState)

        print(str(self.color) + " " + str(bestAction))

        new_player_state = playerState.takeAction(bestAction)
        new_state = new_player_state.state
        return new_state
