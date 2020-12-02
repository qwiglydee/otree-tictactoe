import random

from otree.api import (
    models,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    ExtraModel,
    # Currency as c,
    # currency_range,
)

from .ai import DumbAgent, SmartAgent
from .game import Game, GameError

author = 'qwiglydee@gmail.com'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'game'
    players_per_group = None
    num_rounds = 3


class GameSession(ExtraModel):
    """Persistent game state linked to session"""
    session = models.Link('Subsession')
    board = models.StringField()
    turn = models.StringField()
    winner = models.StringField()

    def __repr__(self):
        return f"<GameSession {repr(self.game)}>"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = Game(self.board, self.turn)

    def save(self, *args, **kwargs):
        self.board = self.game.board
        self.turn = self.game.turn
        super().save(*args, **kwargs)


class Subsession(BaseSubsession):
    """Game round
    Runs for 2 or 1 players.
    Implements all the treatment logic
    """

    ai_plays = models.StringField()
    ai_class = models.StringField()
    moves = models.IntegerField(initial=0)

    def game(self):
        gs = GameSession.objects.get(session=self)
        g = gs.game
        return gs, g

    def creating_session(self):
        players = self.get_players()
        GameSession.objects.create(session=self)

        if len(players) == 2:
            random.shuffle(players)
            players[0].symbol = Game.SYMBOLS[0]
            players[1].symbol = Game.SYMBOLS[1]
            self.ai_plays = None
        elif len(players) == 1:
            self.ai_class = self.session.config.get('ai_class', random.choice(('smart', 'dumb')))
            self.ai_plays = self.session.config.get('ai_plays', random.choice(Game.SYMBOLS))
            players[0].symbol = Game.opponent(self.ai_plays)
        else:
            raise ValueError("Invalid number of players")

    def play_ai(self):
        gamesession, game = self.game()
        print("game:", repr(game))
        if self.ai_plays != game.turn:
            raise GameError("Wrong turn")

        if self.ai_class == 'smart':
            agent = SmartAgent()
        else:
            agent = DumbAgent()

        move = agent.play(game)
        game.move(move)

        completed, winner, pattern = game.completed()
        if completed:
            gamesession.winner = winner
            self.gameover(winner)
        gamesession.save()

        self.moves += 1
        self.save()

        return game, completed, winner, pattern

    def play(self, player, move):
        gamesession, game = self.game()
        print("game:", repr(game))

        if player.symbol != game.turn:
            raise GameError("Wrong turn")

        game.move(move)
        completed, winner, pattern = game.completed()
        if completed:
            gamesession.winner = winner
            self.gameover(winner)
        gamesession.save()

        self.moves += 1
        self.save()

        return game, completed, winner, pattern

    def gameover(self, winner):
        for player in self.get_players():
            if winner is None:
                player.win = None
                player.save()
            else:
                player.win = winner == player.symbol
                player.save()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    """Player
    Holds playing parameter and result
    Implements communication
    """
    symbol = models.StringField(choices=Game.SYMBOLS)
    win = models.BooleanField()

    def game(self):
        gs, g = self.subsession.game()
        return g

    def handle_message(self, message):
        kind = message['type']
        if kind == 'move':
            return self.handle_move(message['place'])
        elif kind == 'ai':
            return self.handle_aimove()
        elif kind == 'start':
            return self.handle_start()
        else:
            raise ValueError("Invalid message", kind)

    def reply(self, message):
        return {self.id_in_group: message}

    def bcast(self, message):
        return {0: message}

    def game_message(self, game):
        return dict(type='game', board=game.board, turn=game.turn)

    def gameover_message(self, game, winner, pattern):
        msg = self.game_message(game)
        msg.update(type='gameover', winner=winner, pattern=pattern)
        return msg

    def error_message(self, error):
        return dict(type='error', error=error)

    def handle_start(self):
        return self.reply(self.game_message(self.game()))

    def handle_move(self, place):
        try:
            game, completed, winner, pattern = self.subsession.play(self, place)
            if completed:
                return self.bcast(self.gameover_message(game, winner, pattern))
            else:
                return self.bcast(self.game_message(game))
        except GameError as e:
            return self.reply(self.error_message(str(e)))

    def handle_aimove(self):
        try:
            game, completed, winner, pattern = self.subsession.play_ai()
            if completed:
                return self.bcast(self.gameover_message(game, winner, pattern))
            else:
                return self.bcast(self.game_message(game))
        except GameError as e:
            return self.reply(self.error_message(str(e)))
