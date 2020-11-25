class GameError(Exception):
    pass


class WrongTurn(GameError):
    def __init__(self):
        super().__init__("Wrong turn")


class WrongMove(GameError):
    def __init__(self):
        super().__init__("Wrong move")


class Game(object):
    """Game state object
    Items:
    - field: a string of characters
    - turn: a symbol of current player
    """
    SYMBOLS = ('x', 'o')
    EMPTY = '.'

    def __init__(self, field=None, turn=None):
        self.field = field or self.EMPTY * 9
        self.turn = turn = turn or self.SYMBOLS[0]

    def move(self, place):
        """Makes a move and returns new game state"""
        if self.field[place] != self.EMPTY:
            raise WrongMove()

        return Game(
            field=self.field[:place] + self.turn + self.field[place+1:],
            turn=self.opponent(self.turn)
        )

    @classmethod
    def opponent(cls, player):
        return cls.SYMBOLS[(cls.SYMBOLS.index(player) + 1) % 2]

    def places(self, sym):
        return tuple(i for i in range(len(self.field)) if self.field[i] == sym)

    def moves(self):
        """Returns possible moves"""
        return self.places(self.EMPTY)

    WINNING = [
        {0, 1, 2},
        {3, 4, 5},
        {6, 7, 8},
        {0, 3, 6},
        {1, 4, 7},
        {2, 5, 8},
        {0, 4, 8},
        {2, 4, 6}
    ]

    def completed(self):
        """Checks if the game is completed and who is the winner

        Returns: bool, winner symbol, winner pattern
        """
        def win(pos):
            return list(filter(lambda win: pos >= win, self.WINNING))

        p1_win = win(set(self.places(self.SYMBOLS[0])))
        p2_win = win(set(self.places(self.SYMBOLS[1])))

        if p1_win:
            return True, self.SYMBOLS[0], p1_win

        if p2_win:
            return True, self.SYMBOLS[1], p2_win

        if len(self.places(self.EMPTY)) == 0:
            return True, None, None
        else:
            return False, None, None

    def __repr__(self):
        return f"""Game("{self.field}", '{self.turn}')"""

    def to_dict(self):
        return dict(field=self.field, turn=self.turn)

    @classmethod
    def from_dict(cls, d):
        return cls(d['field'], d['turn'])


class GameMessage(dict):
    TYPE = 'game'

    def __init__(self, game=None, **kwargs):
        super().__init__(**kwargs)
        self['type'] = self.TYPE
        if game:
            self.update(game.to_dict())


class GameOverMessage(GameMessage):
    TYPE = 'gameover'


class GameErrorMessage(GameMessage):
    TYPE = 'error'
