# from otree.api import Currency as c, currency_range
# from .models import Constants
from ._builtin import Page


class Intro(Page):
    pass


class Game(Page):
    live_method = "handle_message"

    def js_vars(self):
        vars = {}
        vars['symbol'] = self.player.symbol
        if self.subsession.ai_class:
            vars['ai'] = True
        vars.update(self.subsession.load_game().to_dict())
        return vars


class Results(Page):
    pass


page_sequence = [Intro, Game, Results]
