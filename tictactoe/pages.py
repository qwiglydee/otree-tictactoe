# from otree.api import Currency as c, currency_range
# from .models import Constants
from ._builtin import Page


class Intro(Page):
    pass


class Game(Page):
    live_method = "handle_message"

    def js_vars(self):
        vars = {}
        vars['player_symbol'] = self.player.symbol
        if self.subsession.ai_class:
            vars['ai_symbol'] = self.subsession.ai_plays
        return vars


class Results(Page):
    pass


page_sequence = [Intro, Game, Results]
