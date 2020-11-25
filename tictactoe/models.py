import random
import json

from otree.api import (
    models,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    # Currency as c,
    # currency_range,
)

from . import game as g
# from .ai import random_play

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'game'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    _game = models.StringField()
    ai_plays = models.StringField()

    def creating_session(self):
        players = self.get_players()

        if len(players) == 2:
            random.shuffle(players)
            players[0].symbol = g.Game.SYMBOLS[0]
            players[1].symbol = g.Game.SYMBOLS[1]
            self.ai_plays = None
        else:
            players[0].symbol = g.Game.SYMBOLS[0]
            self.ai_plays = g.Game.SYMBOLS[1]

        self.save_game(g.Game())

    def load_game(self):
        return g.Game.from_dict(json.loads(self._game))

    def save_game(self, game):
        self._game = json.dumps(game.to_dict())


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    symbol = models.StringField(choices=g.Game.SYMBOLS)
    rounds = models.IntegerField()
    wins = models.IntegerField()

    def handle_message(self, message):
        game = self.subsession.load_game()
        print(game, self.symbol, message)
        try:
            game = game.move(message['move'], self.symbol)
            print(">", game)

            completed, winner, pattern = game.completed()
            if completed:
                print("win", winner, pattern)

            self.subsession.save_game(game)
            self.subsession.save()

            if completed:
                return {0: g.GameOverMessage(game, winner=winner, pattern=pattern)}
            else:
                return {0: g.GameMessage(game)}
        except g.GameError as e:
            return {self.id_in_group: g.GameErrorMessage(error=str(e))}
