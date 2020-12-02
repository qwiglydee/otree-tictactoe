class GameError(Exception):
    pass


class Game(object):
    """Core game logic
    Independent from otree stuff
    Holds game state
    Implements all the game logic
    """

    SYMBOLS = ('x', 'o')
    EMPTY = '.'

    # game board encoded as string in row-major order
    board: str
    # symbol of current player
    turn: str

    def __init__(self, board=None, turn=None):
        self.board = board or self.EMPTY * 9
        self.turn = turn or self.SYMBOLS[0]

    def __repr__(self):
        return f"<Game {self.board}/{self.turn}>"

    @classmethod
    def opponent(cls, sym):
        """Return opponent symbol for given one"""
        return cls.SYMBOLS[(cls.SYMBOLS.index(sym) + 1) % 2]

    def places(self, sym):
        """Return indexes of cells containing given sym"""
        return tuple(i for i in range(len(self.board)) if self.board[i] == sym)

    def moves(self):
        """Returns possible moves"""
        return self.places(self.EMPTY)

    def move(self, place):
        """Makes a move and changes state"""
        if self.board[place] != self.EMPTY:
            raise GameError("Wrong move")

        self.board = self.board[:place] + self.turn + self.board[place+1:]
        self.turn = self.opponent(self.turn)

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

        Returns: bool, winner symbol, winning pattern
        """
        def win(pos):
            return list(filter(lambda win: pos >= win, self.WINNING))

        p1_win = win(set(self.places(self.SYMBOLS[0])))
        p2_win = win(set(self.places(self.SYMBOLS[1])))

        if p1_win:
            return True, self.SYMBOLS[0], [list(p) for p in p1_win]

        if p2_win:
            return True, self.SYMBOLS[1], [list(p) for p in p2_win]

        if len(self.places(self.EMPTY)) == 0:
            return True, None, None
        else:
            return False, None, None
