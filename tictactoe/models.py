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
from .ai import DumbAgent, SmartAgent

author = 'qwiglydee@gmail.com'

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
    ai_class = models.StringField()

    def creating_session(self):
        self.ai_class = self.session.config.get('ai_class')
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

        if 'move' in message:
            return self.handle_move(game, message['move'])
        elif 'waitai' in message:
            return self.handle_aimove(game)

    def handle_move(self, game, move):
        try:
            game = game.move(move, self.symbol)
            completed, winner, pattern = game.completed()
            self.subsession.save_game(game)
            self.subsession.save()

            if completed:
                return {0: g.GameOverMessage(game, winner=winner, pattern=pattern)}
            else:
                return {0: g.GameMessage(game)}
        except g.GameError as e:
            return {self.id_in_group: g.GameErrorMessage(error=str(e))}

    def handle_aimove(self, game):

        if self.subsession.ai_class == 'smart':
            agent = SmartAgent()
        else:
            agent = DumbAgent()

        move = agent.decide(game, self.subsession.ai_plays)
        game = game.move(move, self.subsession.ai_plays)

        completed, winner, pattern = game.completed()
        self.subsession.save_game(game)
        self.subsession.save()

        if completed:
            return {0: g.GameOverMessage(game, winner=winner, pattern=pattern)}
        else:
            return {0: g.GameMessage(game)}
