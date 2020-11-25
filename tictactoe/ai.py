from time import sleep
import random

from .game import Game


class DumbAgent(object):
    """dumb AI agent that plays randomly"""
    def decide(self, game):
        return random.choice(game.moves())


class SmartAgent(DumbAgent):
    def decide(self, game):
        return minmax_decision(game, game.turn)


def minmax_decision(state: Game, player: str):
    def terminal_test(state):
        completed, winner, _ = state.completed()
        if winner:
            utility = (+1 if winner == player else -1)
        else:
            utility = 0
        return completed, utility

    def max_value(state):
        completed, utility = terminal_test(state)
        if completed:
            return utility
        v = float("-inf")
        for a in state.moves():
            v = max(v, min_value(state.move(a)))
        return v

    def min_value(state):
        completed, utility = terminal_test(state)
        if completed:
            return utility
        v = float("inf")
        for a in state.moves():
            v = min(v, max_value(state.move(a)))
        return v

    return max(state.moves(), key=lambda a: min_value(state.move(a)))
