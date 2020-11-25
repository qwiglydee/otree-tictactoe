import random

from .game import Game


def random_play(game: Game):
    places = game.places()
    return random.choice(places)
