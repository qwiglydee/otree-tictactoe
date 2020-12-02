import random
from functools import lru_cache

from .game import Game


class Agent(object):
    def play(self, game):
        moves = game.moves()

        if len(moves) == 0:
            raise ValueError("invalid game state")
        if len(moves) == 1:
            return moves[0]

        return self.decide(game)


class DumbAgent(Agent):
    """dumb AI agent that plays randomly"""
    def decide(self, game):
        return random.choice(game.moves())


class SmartAgent(Agent):
    """smart AI agent that uses minimax algo"""
    def decide(self, game):
        moves = game.moves()

        onestep = [a for a in moves if game.advance(a).completed()[0]]
        if len(onestep) > 0:
            return onestep[0]

        return minmax_decision(GameState(game))


cache = lru_cache(10000)  # < 3^9


class GameState(Game):
    """Wrapper to return new state object on move"""
    def __init__(self, game):
        super().__init__(board=game.board, turn=game.turn)

    def advance(self, place):
        newstate = GameState(self)
        newstate.move(place)
        return newstate


def minmax_decision(state: Game):
    # assuming human player is not perfect and using avg instead of min
    player = state.turn

    def terminal_test(state):
        completed, winner, _ = state.completed()
        if winner:
            utility = (+1 if winner == player else -1)
        else:
            utility = 0
        return completed, utility

    @cache
    def max_value(state):
        completed, utility = terminal_test(state)
        if completed:
            return utility
        moves = state.moves()
        return max(avg_value(state.advance(a)) for a in moves)

    @cache
    def avg_value(state):
        completed, utility = terminal_test(state)
        if completed:
            return utility
        moves = state.moves()
        return sum(max_value(state.advance(a)) for a in moves) / len(moves)

    return max(state.moves(), key=lambda a: avg_value(state.advance(a)))
